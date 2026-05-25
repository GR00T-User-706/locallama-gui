#!/usr/bin/env python3
"""
ollama_tools_v4.py  (v4 — MODIFIED)
--------------------------------------
Drop-in replacement for ollama_tools.py that wires in the ToolOrchestrator.

v4 changes to OllamaToolEngine (MINIMAL — all existing code preserved):
  - Constructor now accepts an optional pre-built ToolOrchestrator instance.
  - If no orchestrator is provided, one is created automatically (backward-compatible).
  - _dispatch_tool() now routes through the orchestrator instead of calling
    tool dispatchers directly.
  - active_schemas() now delegates to orchestrator.active_schemas().
  - set_session_mode() and toggle_tool() delegate to orchestrator.
  - All other methods (chat, _single_turn, _agent_turn, etc.) are UNCHANGED.

Everything in ollama_tools.py (ALLOWED_COMMANDS, _normalize_flags,
_CommandCache, _parse_structured_prefix, SESSION_PERMISSION_MODES,
TOOL_REGISTRY, etc.) is still importable from ollama_tools.py directly.
This file only overrides OllamaToolEngine.
"""

import argparse
import json
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import ollama
except ImportError:
    print("ERROR: pip install ollama")
    raise SystemExit(1)

# Import everything from v3 (unchanged)
from ollama_tools import (
    SYSTEM_PROMPT_BASE,
    DEFAULT_MAX_TOOL_CALLS,
    AGENT_MAX_ITERATIONS,
    _parse_structured_prefix,
    _STRUCTURED_OUTPUT_PROMPT,
)
from tool_orchestrator import ToolOrchestrator


class OllamaToolEngine:
    """
    v4 OllamaToolEngine — all existing public methods preserved.
    The only internal change is that _dispatch_tool() routes through
    the ToolOrchestrator instead of calling dispatchers directly.
    """

    def __init__(
        self,
        model:             str  = "mistral",
        memory_path:       Path = None,
        sandbox_dir:       Path = None,
        keep_history:      bool = True,
        verbose:           bool = True,
        max_tool_calls:    int  = DEFAULT_MAX_TOOL_CALLS,
        session_mode:      str  = "full",
        agent_mode:        bool = False,
        structured_output: bool = False,
        # --- NEW (v4): accept a pre-built orchestrator ---
        orchestrator:      Optional[ToolOrchestrator] = None,
    ):
        self.model             = model
        self.keep_history      = keep_history
        self.verbose           = verbose
        self.max_tool_calls    = max_tool_calls
        self.agent_mode        = agent_mode
        self.structured_output = structured_output
        self._history: List[dict] = []

        if orchestrator is not None:
            self.orchestrator = orchestrator
        else:
            self.orchestrator = ToolOrchestrator(
                sandbox_dir=sandbox_dir,
                memory_path=memory_path,
                session_mode=session_mode,
            )

        self.session_mode = self.orchestrator.session_mode

    # ------------------------------------------------------------------ internal

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def _build_system_prompt(self, extra: str = "") -> str:
        parts = [SYSTEM_PROMPT_BASE]
        mem_ctx    = self.orchestrator.memory_store.all_as_context()
        struct_ctx = self.orchestrator.memory_store.struct_as_context()
        if mem_ctx:    parts.append(mem_ctx)
        if struct_ctx: parts.append(struct_ctx)
        if extra:      parts.append(extra)
        if self.structured_output:
            parts.append(_STRUCTURED_OUTPUT_PROMPT)
        return "\n\n".join(parts)

    def _active_tools(self) -> List[dict]:
        """Delegate to orchestrator — single source of truth."""
        return self.orchestrator.active_schemas()

    def _dispatch_tool(self, tool_name: str, args: dict) -> str:
        """Route ALL tool calls through the orchestrator."""
        return self.orchestrator.dispatch(tool_name, args)

    # ------------------------------------------------------------------ public API (UNCHANGED signatures)

    def chat(self, user_prompt: str) -> str:
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
            self._history.append({"role": "user",     "content": user_prompt})
            self._history.append({"role": "assistant", "content": answer})
            if len(self._history) > 40:
                self._history = self._history[-40:]

        return answer

    def _single_turn(self, messages: List[dict]) -> Tuple[str, List[dict]]:
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

        if self.structured_output:
            intent_obj, answer = _parse_structured_prefix(answer)
            if intent_obj:
                self._log(f"  [Intent] {intent_obj}")

        return answer, messages

    def _agent_turn(self, user_prompt: str, base_messages: List[dict]) -> str:
        messages    = base_messages[:]
        plan_prompt = (
            f"The user asked: {user_prompt}\n\n"
            "First, briefly state your plan (1-2 sentences), then execute it step by step."
        )
        messages.append({"role": "user", "content": plan_prompt})
        answer = ""
        for iteration in range(1, AGENT_MAX_ITERATIONS + 1):
            self._log(f"\n  [Agent] Iteration {iteration}/{AGENT_MAX_ITERATIONS}")
            answer, messages = self._single_turn(messages)
            needs_more = (
                answer.rstrip().endswith("?") or
                any(p in answer.lower() for p in ["need to", "should also", "let me also"])
            )
            if not needs_more or iteration == AGENT_MAX_ITERATIONS:
                break
            messages.append({
                "role": "user",
                "content": "Is there anything else you need to do to fully answer the original request? If yes, continue. If no, give your final answer."
            })
        return answer

    def clear_history(self) -> None:
        self._history = []

    def get_tool_info(self) -> List[dict]:
        return self.orchestrator.list_tools()

    def toggle_tool(self, tool_name: str, enabled: bool) -> None:
        self.orchestrator.toggle_tool(tool_name, enabled)

    def set_session_mode(self, mode: str) -> None:
        self.orchestrator.set_session_mode(mode)
        self.session_mode = self.orchestrator.session_mode


# ------------------------------------------------------------------
# CLI entry point
# ------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ollama Tool Framework v4")
    parser.add_argument("--model",      type=str, default="mistral")
    parser.add_argument("--mode",       type=str, default="full",
                        choices=["full", "restricted", "read-only"])
    parser.add_argument("--agent",      action="store_true")
    parser.add_argument("--structured", action="store_true")
    parser.add_argument("--list-tools", action="store_true")
    parser.add_argument("prompt",       nargs="*")
    args = parser.parse_args()

    engine = OllamaToolEngine(
        model=args.model,
        session_mode=args.mode,
        agent_mode=args.agent,
        structured_output=args.structured,
    )

    if args.list_tools:
        print("\nRegistered tools:\n")
        for t in engine.get_tool_info():
            status = "ON " if t["enabled"] else "OFF"
            print(f"  [{status}] {t['name']:<28} {t['description']}")
        print()
        raise SystemExit(0)

    prompt = " ".join(args.prompt).strip() or (
        "What tools do you have available? List them and describe what you can do."
    )
    answer = engine.chat(prompt)
    print("\n" + "=" * 60)
    print(answer)
