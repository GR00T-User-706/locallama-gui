#!/usr/bin/env python3
"""
ollama_tools.py  (v3)
---------------------
Ollama tool framework — surgical upgrade from v2.

v3 changes:
  FIX 2     — Tool call limiting: per-turn cap (default 3) prevents infinite loops.
  FIX 3     — Argument normalization: split flags (["-la"] → ["-l", "-a"]) and
               normalise before allow-list check. Security unchanged.
  UPGRADE 1 — Agent mode: optional PLAN→EXECUTE→REFLECT loop (max 3 iterations).
  UPGRADE 3 — Command result caching: TTL-based cache for read-only commands.
  UPGRADE 4 — Session-based tool permissions: read-only / restricted / full modes.
  UPGRADE 5 — Structured LLM output control: optional intent/confidence layer.

All existing class names, method signatures, and TOOL_REGISTRY structure preserved.
"""

import argparse
import json
import re
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

try:
    import ollama
except ImportError:
    print("ERROR: pip install ollama")
    raise SystemExit(1)

from tool_memory        import MemoryStore,        MEMORY_TOOL_SCHEMA,       dispatch_memory_tool
from tool_sandbox_files import SandboxedFileStore, SANDBOX_FILE_TOOL_SCHEMA, dispatch_sandbox_file_tool


# ==============================================================================
#  ALLOW-LIST  (UNCHANGED from v2)
# ==============================================================================

ALLOWED_COMMANDS: Dict[str, Dict] = {
    "ls":     {"description": "List directory contents.",          "path": "/usr/bin/ls",     "allowed_flags": ["-l","-a","-la","-al","-lh","-lah","-h"],  "allow_path_args": True,  "path_arg_must_exist": True,  "read_only": True},
    "cat":    {"description": "Print file contents.",              "path": "/usr/bin/cat",    "allowed_flags": [],                                          "allow_path_args": True,  "path_arg_must_exist": True,  "read_only": True},
    "find":   {"description": "Search for files.",                 "path": "/usr/bin/find",   "allowed_flags": ["-name","-type","-maxdepth"],               "allow_path_args": True,  "path_arg_must_exist": True,  "read_only": True},
    "date":   {"description": "Current date and time.",            "path": "/usr/bin/date",   "allowed_flags": [],                                          "allow_path_args": False, "path_arg_must_exist": False, "read_only": True},
    "uname":  {"description": "System/kernel information.",        "path": "/usr/bin/uname",  "allowed_flags": ["-a","-r","-m","-s"],                       "allow_path_args": False, "path_arg_must_exist": False, "read_only": True},
    "uptime": {"description": "System uptime.",                    "path": "/usr/bin/uptime", "allowed_flags": ["-p","-s"],                                 "allow_path_args": False, "path_arg_must_exist": False, "read_only": True},
    "df":     {"description": "Disk space usage.",                 "path": "/usr/bin/df",     "allowed_flags": ["-h","-H"],                                 "allow_path_args": False, "path_arg_must_exist": False, "read_only": True},
    "free":   {"description": "Memory usage.",                     "path": "/usr/bin/free",   "allowed_flags": ["-h","-m","-g"],                            "allow_path_args": False, "path_arg_must_exist": False, "read_only": True},
    "lscpu":  {"description": "CPU architecture info.",            "path": "/usr/bin/lscpu",  "allowed_flags": [],                                          "allow_path_args": False, "path_arg_must_exist": False, "read_only": True},
    "lsblk":  {"description": "Block device info.",                "path": "/usr/bin/lsblk",  "allowed_flags": ["-f","-o"],                                 "allow_path_args": False, "path_arg_must_exist": False, "read_only": True},
    "ps":     {"description": "Running processes.",                "path": "/usr/bin/ps",     "allowed_flags": ["aux","-e","-f"],                           "allow_path_args": False, "path_arg_must_exist": False, "read_only": True},
    "ping":   {"description": "Ping a network host.",              "path": "/usr/bin/ping",   "allowed_flags": ["-c"],                                      "allow_path_args": True,  "path_arg_must_exist": False, "read_only": True},
    "ss":     {"description": "Socket statistics.",                "path": "/usr/bin/ss",     "allowed_flags": ["-tuln","-tlnp","-s"],                      "allow_path_args": False, "path_arg_must_exist": False, "read_only": True},
    "echo":   {"description": "Print a line of text.",             "path": "/usr/bin/echo",   "allowed_flags": [],                                          "allow_path_args": True,  "path_arg_must_exist": False, "read_only": True},
    "wc":     {"description": "Word/line/char count.",             "path": "/usr/bin/wc",     "allowed_flags": ["-l","-w","-c"],                            "allow_path_args": True,  "path_arg_must_exist": True,  "read_only": True},
    "grep":   {"description": "Search for a pattern in a file.",   "path": "/usr/bin/grep",   "allowed_flags": ["-i","-n","-r","-l","-c"],                  "allow_path_args": True,  "path_arg_must_exist": False, "read_only": True},
    "git":    {"description": "Git read-only commands.",           "path": "/usr/bin/git",    "allowed_flags": ["status","log","diff","branch","--oneline","--short","-n"], "allow_path_args": True, "path_arg_must_exist": False, "read_only": True},
}

_DANGEROUS_CHARS_RE = re.compile(r'[;&|`$<>\\!]')

def _sanitize_arg(arg: str) -> Optional[str]:
    return None if _DANGEROUS_CHARS_RE.search(arg) else arg


# --- NEW (FIX 3): argument normalization ---
# Expand combined short flags like "-la" into ["-l", "-a"] so they match
# the per-command allowed_flags list without weakening validation.

def _normalize_flags(args: List[str], allowed_flags: List[str]) -> List[str]:
    """
    For each argument that starts with '-' and is NOT already in allowed_flags,
    attempt to split it into individual single-char flags.
    e.g. "-la" → ["-l", "-a"] if both are in allowed_flags.
    Non-flag args and already-valid flags are passed through unchanged.
    """
    result = []
    for arg in args:
        if arg.startswith("-") and arg not in allowed_flags and not arg.startswith("--"):
            # Try splitting: "-la" → ["-l", "-a"]
            chars = list(arg[1:])
            expanded = [f"-{c}" for c in chars]
            if all(e in allowed_flags for e in expanded):
                result.extend(expanded)
                continue
        result.append(arg)
    return result


# --- NEW (UPGRADE 3): command result cache ---

class _CommandCache:
    """
    Simple TTL cache for read-only command results.
    Key = (command, tuple(args)).  Value = (result_str, expiry_timestamp).
    """
    def __init__(self, default_ttl: int = 15):
        self._store: Dict[Tuple, Tuple[str, float]] = {}
        self.default_ttl = default_ttl

    def get(self, command: str, args: List[str]) -> Optional[str]:
        key    = (command, tuple(args))
        entry  = self._store.get(key)
        if entry and time.monotonic() < entry[1]:
            return entry[0]
        return None

    def set(self, command: str, args: List[str], result: str, ttl: Optional[int] = None) -> None:
        key = (command, tuple(args))
        self._store[key] = (result, time.monotonic() + (ttl or self.default_ttl))

    def invalidate(self, command: str = None) -> None:
        if command:
            self._store = {k: v for k, v in self._store.items() if k[0] != command}
        else:
            self._store.clear()

_cmd_cache = _CommandCache(default_ttl=15)


def execute_system_command(command: str, args: List[str] = None,
                           cache_ttl: Optional[int] = None) -> str:
    if args is None:
        args = []
    if command not in ALLOWED_COMMANDS:
        return (
            f"Error: Command '{command}' is not in the allow-list. "
            f"Allowed: {', '.join(ALLOWED_COMMANDS.keys())}"
        )
    cfg             = ALLOWED_COMMANDS[command]
    cmd_path        = cfg["path"]
    allowed_flags   = cfg.get("allowed_flags", [])
    allow_path_args = cfg.get("allow_path_args", False)
    path_must_exist = cfg.get("path_arg_must_exist", False)
    is_read_only    = cfg.get("read_only", False)

    # FIX 3: normalize flags before validation
    args = _normalize_flags(args, allowed_flags)

    # UPGRADE 3: check cache for read-only commands
    if is_read_only:
        cached = _cmd_cache.get(command, args)
        if cached is not None:
            print(f"  [TOOL] Cache hit: {command} {' '.join(args)}")
            return cached

    validated = []
    for arg in args:
        clean = _sanitize_arg(arg)
        if clean is None:
            return f"Error: Argument '{arg}' contains disallowed characters."
        if arg.startswith("-"):
            if arg not in allowed_flags:
                return f"Error: Flag '{arg}' is not permitted for '{command}'."
        else:
            if not allow_path_args:
                return f"Error: '{command}' does not accept non-flag arguments."
            if path_must_exist and not os.path.exists(arg):
                return f"Error: Path '{arg}' does not exist."
        validated.append(clean)

    try:
        full_cmd = [cmd_path] + validated
        print(f"  [TOOL] Running: {' '.join(full_cmd)}")
        result = subprocess.run(full_cmd, capture_output=True, text=True, timeout=15, shell=False)
        out = result.stdout
        if result.stderr:
            out += f"\nstderr:\n{result.stderr}"
        out = out.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: '{command}' timed out."
    except FileNotFoundError:
        return f"Error: Executable not found at '{cmd_path}'."
    except Exception as e:
        return f"Error: {e}"

    # UPGRADE 3: store in cache if read-only
    if is_read_only:
        _cmd_cache.set(command, args, out, ttl=cache_ttl)

    return out


SYSTEM_COMMAND_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "execute_system_command",
        "description": (
            "Execute an approved system command on the user's Linux machine.\n"
            "Available commands:\n"
            + "\n".join(f"  - {n}: {c['description']}" for n, c in ALLOWED_COMMANDS.items())
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Command to run. Must be one of: " + ", ".join(ALLOWED_COMMANDS.keys())},
                "args":    {"type": "array", "items": {"type": "string"}, "description": "Flags and arguments."},
            },
            "required": ["command"],
        },
    },
}


# ==============================================================================
#  UPGRADE 4 — Session-based tool permissions
# ==============================================================================

# Which tools are available in each permission mode.
# "full" = everything; "restricted" = no system commands; "read-only" = no writes.
SESSION_PERMISSION_MODES = {
    "full": {
        "execute_system_command": True,
        "memory":                 True,
        "sandbox_file":           True,
    },
    "restricted": {
        "execute_system_command": False,   # no shell access
        "memory":                 True,
        "sandbox_file":           True,
    },
    "read-only": {
        "execute_system_command": True,    # system commands are all read-only anyway
        "memory":                 True,    # recall allowed; remember/forget still possible
        "sandbox_file":           False,   # no file writes
    },
}


# ==============================================================================
#  TOOL REGISTRY  (UNCHANGED structure from v2)
# ==============================================================================

TOOL_REGISTRY = {
    "execute_system_command": {
        "label":       "System Commands",
        "description": "Run approved Linux commands (ls, df, free, uname, etc.)",
        "schema":      SYSTEM_COMMAND_TOOL_SCHEMA,
        "enabled":     True,
        "details":     {"type": "system_command", "commands": list(ALLOWED_COMMANDS.keys())},
    },
    "memory": {
        "label":       "Persistent Memory",
        "description": "Remember, recall, and forget facts across conversations",
        "schema":      MEMORY_TOOL_SCHEMA,
        "enabled":     True,
        "details":     {"type": "memory", "operations": ["remember","recall","forget","remember_struct","recall_struct","forget_struct"]},
    },
    "sandbox_file": {
        "label":       "Sandboxed Files",
        "description": "Read and write files inside a secure sandbox directory",
        "schema":      SANDBOX_FILE_TOOL_SCHEMA,
        "enabled":     True,
        "details":     {"type": "sandbox_file", "operations": ["list","read","write","append","delete"]},
    },
}


# ==============================================================================
#  UPGRADE 5 — Structured LLM output control (lightweight)
# ==============================================================================

_STRUCTURED_OUTPUT_PROMPT = """
Before answering, output a JSON block on a single line with this exact format:
{"intent": "<brief intent>", "tool_needed": true/false, "confidence": 0.0-1.0}
Then on the next line, give your normal response.
"""

def _parse_structured_prefix(text: str) -> Tuple[Optional[dict], str]:
    """
    Try to extract a leading JSON intent block from the model's response.
    Returns (parsed_dict_or_None, remaining_text).
    Fails gracefully — if parsing fails, returns (None, original_text).
    """
    if not text:
        return None, text
    first_line = text.split("\n", 1)[0].strip()
    rest       = text.split("\n", 1)[1] if "\n" in text else text
    try:
        obj = json.loads(first_line)
        if "intent" in obj and "tool_needed" in obj and "confidence" in obj:
            return obj, rest.strip()
    except (json.JSONDecodeError, ValueError):
        pass
    return None, text


# ==============================================================================
#  ENGINE  (UNCHANGED class name and public interface)
# ==============================================================================

SYSTEM_PROMPT_BASE = (
    "You are a helpful AI assistant running on a Linux system. "
    "You have access to tools that let you run approved system commands, "
    "remember facts between conversations, and read/write files in a secure sandbox. "
    "Use these tools proactively when they would help answer the user's request. "
    "After using a tool, always explain what you found or did in plain language."
)

# Per-turn tool call cap (FIX 2)
DEFAULT_MAX_TOOL_CALLS = 3

# Agent mode iteration cap (UPGRADE 1)
AGENT_MAX_ITERATIONS = 3


class OllamaToolEngine:
    """
    Main engine class.  All existing public methods preserved.

    v3 new constructor parameters (all optional, all backward-compatible):
      max_tool_calls (int)    — per-turn tool call cap (FIX 2)
      session_mode   (str)    — "full" / "restricted" / "read-only" (UPGRADE 4)
      agent_mode     (bool)   — enable PLAN→EXECUTE→REFLECT loop (UPGRADE 1)
      structured_output (bool)— request structured intent prefix (UPGRADE 5)
    """

    def __init__(
        self,
        model:             str  = "mistral",
        memory_path:       Path = None,
        sandbox_dir:       Path = None,
        keep_history:      bool = True,
        verbose:           bool = True,
        # --- NEW v3 parameters ---
        max_tool_calls:    int  = DEFAULT_MAX_TOOL_CALLS,   # FIX 2
        session_mode:      str  = "full",                   # UPGRADE 4
        agent_mode:        bool = False,                    # UPGRADE 1
        structured_output: bool = False,                    # UPGRADE 5
    ):
        self.model             = model
        self.keep_history      = keep_history
        self.verbose           = verbose
        self.max_tool_calls    = max_tool_calls
        self.session_mode      = session_mode
        self.agent_mode        = agent_mode
        self.structured_output = structured_output

        self.memory_store  = MemoryStore(
            path=memory_path or Path.home() / ".ollama_tools" / "memory.json"
        )
        self.sandbox_store = SandboxedFileStore(
            sandbox_dir=sandbox_dir or Path.home() / ".ollama_tools" / "sandbox"
        )
        self._history: List[dict] = []
        self._apply_session_mode(session_mode)

    # ------------------------------------------------------------------ internal

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def _build_system_prompt(self, extra: str = "") -> str:
        parts = [SYSTEM_PROMPT_BASE]
        mem_ctx    = self.memory_store.all_as_context()
        struct_ctx = self.memory_store.struct_as_context()
        if mem_ctx:    parts.append(mem_ctx)
        if struct_ctx: parts.append(struct_ctx)
        if extra:      parts.append(extra)
        if self.structured_output:
            parts.append(_STRUCTURED_OUTPUT_PROMPT)
        return "\n\n".join(parts)

    def _active_tools(self) -> List[dict]:
        return [
            entry["schema"]
            for name, entry in TOOL_REGISTRY.items()
            if entry["enabled"]
        ]

    def _dispatch_tool(self, tool_name: str, args: dict) -> str:
        if tool_name == "execute_system_command":
            return execute_system_command(args.get("command",""), args.get("args",[]))
        elif tool_name == "memory":
            return dispatch_memory_tool(args, self.memory_store)
        elif tool_name == "sandbox_file":
            return dispatch_sandbox_file_tool(args, self.sandbox_store)
        return f"Error: Unknown tool '{tool_name}'."

    # ------------------------------------------------------------------ UPGRADE 4: session mode

    def _apply_session_mode(self, mode: str) -> None:
        if mode not in SESSION_PERMISSION_MODES:
            self._log(f"  [Permissions] Unknown mode '{mode}', defaulting to 'full'.")
            mode = "full"
        self.session_mode = mode
        policy = SESSION_PERMISSION_MODES[mode]
        for tool_name, allowed in policy.items():
            if tool_name in TOOL_REGISTRY:
                TOOL_REGISTRY[tool_name]["enabled"] = allowed
        self._log(f"  [Permissions] Session mode set to '{mode}'.")

    def set_session_mode(self, mode: str) -> None:
        """Change the session permission mode at runtime."""
        self._apply_session_mode(mode)

    # ------------------------------------------------------------------ core chat (FIX 2 applied here)

    def _single_turn(self, messages: List[dict]) -> Tuple[str, List[dict]]:
        """
        One round-trip to Ollama with tool handling.
        Returns (final_answer_text, updated_messages).
        FIX 2: enforces max_tool_calls per turn.
        """
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                tools=self._active_tools(),
            )
        except ollama.ResponseError as e:
            return f"Ollama error: {e}", messages
        except Exception as e:
            return f"Unexpected error: {e}", messages

        messages.append(response["message"])
        tool_calls = response["message"].get("tool_calls") or []

        # FIX 2: cap tool calls per turn
        if len(tool_calls) > self.max_tool_calls:
            self._log(
                f"  [Safety] Model requested {len(tool_calls)} tool calls; "
                f"capping at {self.max_tool_calls}."
            )
            tool_calls = tool_calls[:self.max_tool_calls]

        for call in tool_calls:
            fn_name = call["function"]["name"]
            fn_args = call["function"].get("arguments", {})
            self._log(f"  [Tool] {fn_name}({json.dumps(fn_args)[:120]})")
            result = self._dispatch_tool(fn_name, fn_args)
            self._log(f"  [Result] {str(result)[:200]}")
            messages.append({"role": "tool", "content": result, "name": fn_name})

        if tool_calls:
            try:
                final = ollama.chat(model=self.model, messages=messages)
                messages.append(final["message"])
                answer = final["message"].get("content", "").strip()
            except Exception as e:
                answer = f"Error getting final response: {e}"
        else:
            answer = response["message"].get("content", "").strip()

        # UPGRADE 5: parse and strip structured prefix if present
        if self.structured_output:
            intent_obj, answer = _parse_structured_prefix(answer)
            if intent_obj:
                self._log(f"  [Intent] {intent_obj}")

        return answer, messages

    # ------------------------------------------------------------------ UPGRADE 1: agent mode

    def _agent_turn(self, user_prompt: str, base_messages: List[dict]) -> str:
        """
        PLAN → EXECUTE → REFLECT loop (max AGENT_MAX_ITERATIONS).
        Each iteration may use tools. The loop continues if the reflection
        step indicates more work is needed (heuristic: answer ends with '?'
        or contains 'need to' / 'should also').
        """
        messages = base_messages[:]
        plan_prompt = (
            f"The user asked: {user_prompt}\n\n"
            "First, briefly state your plan (1-2 sentences), then execute it step by step."
        )
        messages.append({"role": "user", "content": plan_prompt})

        answer = ""
        for iteration in range(1, AGENT_MAX_ITERATIONS + 1):
            self._log(f"\n  [Agent] Iteration {iteration}/{AGENT_MAX_ITERATIONS}")
            answer, messages = self._single_turn(messages)

            # Simple heuristic: if the answer seems incomplete, continue
            needs_more = (
                answer.rstrip().endswith("?") or
                any(phrase in answer.lower() for phrase in ["need to", "should also", "let me also"])
            )
            if not needs_more or iteration == AGENT_MAX_ITERATIONS:
                break

            # Reflect: ask model if it's done
            messages.append({
                "role": "user",
                "content": "Is there anything else you need to do to fully answer the original request? If yes, continue. If no, give your final answer."
            })

        return answer

    # ------------------------------------------------------------------ public API (UNCHANGED)

    def chat(self, user_prompt: str) -> str:
        """
        Send a prompt to the model, handle tool calls, return final answer.
        This is the main method for the GUI to call.  (UNCHANGED signature)
        """
        self._log(f"\n[Engine] Model={self.model}  mode={self.session_mode}  agent={self.agent_mode}")
        self._log(f"[Engine] Prompt: {user_prompt[:80]}...")

        base_messages = [{"role": "system", "content": self._build_system_prompt()}]
        if self.keep_history:
            base_messages += self._history

        if self.agent_mode:
            answer = self._agent_turn(user_prompt, base_messages)
        else:
            base_messages.append({"role": "user", "content": user_prompt})
            answer, _ = self._single_turn(base_messages)

        if self.keep_history:
            self._history.append({"role": "user",      "content": user_prompt})
            self._history.append({"role": "assistant",  "content": answer})
            if len(self._history) > 40:
                self._history = self._history[-40:]

        return answer

    def clear_history(self) -> None:
        """Clear conversation history.  (UNCHANGED)"""
        self._history = []

    def get_tool_info(self) -> List[dict]:
        """Return tool info for the GUI Tools dropdown.  (UNCHANGED)"""
        return [
            {
                "name":        name,
                "label":       entry["label"],
                "description": entry["description"],
                "enabled":     entry["enabled"],
                "details":     entry["details"],
            }
            for name, entry in TOOL_REGISTRY.items()
        ]

    def toggle_tool(self, tool_name: str, enabled: bool) -> None:
        """Enable or disable a tool at runtime.  (UNCHANGED)"""
        if tool_name in TOOL_REGISTRY:
            TOOL_REGISTRY[tool_name]["enabled"] = enabled


# ==============================================================================
#  CLI ENTRY POINT  (UNCHANGED, new flags added)
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ollama Tool Framework v3")
    parser.add_argument("--model",      type=str, default="mistral")
    parser.add_argument("--mode",       type=str, default="full",
                        choices=["full","restricted","read-only"],
                        help="Session permission mode (default: full)")
    parser.add_argument("--agent",      action="store_true",
                        help="Enable agent mode (PLAN→EXECUTE→REFLECT)")
    parser.add_argument("--structured", action="store_true",
                        help="Request structured intent output from model")
    parser.add_argument("--list-tools", action="store_true")
    parser.add_argument("prompt",       nargs="*")
    args = parser.parse_args()

    if args.list_tools:
        print("\nRegistered tools:\n")
        for name, entry in TOOL_REGISTRY.items():
            print(f"  {'ON ' if entry['enabled'] else 'OFF'} {entry['label']:<25} {entry['description']}")
        print()
        raise SystemExit(0)

    engine = OllamaToolEngine(
        model=args.model,
        session_mode=args.mode,
        agent_mode=args.agent,
        structured_output=args.structured,
    )
    prompt = " ".join(args.prompt).strip() or (
        "What is today's date, how much free memory do I have, "
        "and do you remember anything about me?"
    )
    answer = engine.chat(prompt)
    print("\n" + "=" * 60)
    print(answer)
