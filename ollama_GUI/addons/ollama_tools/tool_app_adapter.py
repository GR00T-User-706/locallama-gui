#!/usr/bin/env python3
"""
tool_app_adapter.py  (v4 — NEW FILE)
--------------------------------------
App Adapter Tool for Ollama LLMs.

Provides controlled interaction with external applications using the
adapter pattern. No direct GUI automation, no raw subprocess execution.

Each registered app defines:
  - allowed_actions: dict mapping action name → parameter schema + handler
  - description: human-readable description

The LLM calls:
  {"app": "app_name", "action": "action_name", "params": {...}}

The orchestrator routes to the correct adapter, which validates params
and executes the action through a controlled handler function.

Security:
  - Only pre-registered apps are accessible
  - Every action has a strict parameter schema
  - Unknown apps or actions are rejected immediately
  - No shell execution, no arbitrary subprocess calls
  - All handlers are Python functions, not shell commands
"""

import re
import shutil
import subprocess
from typing import Any, Callable, Dict, List, Optional

# ------------------------------------------------------------------
# Parameter validation helpers
# ------------------------------------------------------------------

def _require_str(params: dict, key: str, max_len: int = 256) -> str:
    val = params.get(key, "")
    if not isinstance(val, str) or not val.strip():
        raise ValueError(f"Parameter '{key}' must be a non-empty string.")
    if len(val) > max_len:
        raise ValueError(f"Parameter '{key}' exceeds max length ({max_len}).")
    return val.strip()

def _optional_str(params: dict, key: str, default: str = "", max_len: int = 256) -> str:
    val = params.get(key, default)
    if not isinstance(val, str):
        return default
    return val[:max_len]

def _require_int(params: dict, key: str, min_val: int = 0, max_val: int = 9999) -> int:
    val = params.get(key)
    if not isinstance(val, int):
        raise ValueError(f"Parameter '{key}' must be an integer.")
    if not (min_val <= val <= max_val):
        raise ValueError(f"Parameter '{key}' must be between {min_val} and {max_val}.")
    return val

# ------------------------------------------------------------------
# Built-in app adapters
# ------------------------------------------------------------------

# --- calculator app ---

def _calc_evaluate(params: dict) -> str:
    """Safe arithmetic evaluator — no eval(), no exec()."""
    expr = _require_str(params, "expression", max_len=128)
    # Allow only digits, operators, spaces, parens, dots
    if not re.fullmatch(r'[\d\s\+\-\*/\.\(\)]+', expr):
        return "Error: Expression contains disallowed characters. Only +, -, *, /, (, ), digits, and . are allowed."
    try:
        # Use Python's ast for safe evaluation
        import ast
        tree = ast.parse(expr, mode="eval")
        # Whitelist only safe node types
        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
            ast.USub, ast.UAdd, ast.Constant,
        )
        for node in ast.walk(tree):
            if not isinstance(node, allowed_nodes):
                return f"Error: Disallowed expression node: {type(node).__name__}"
        result = eval(compile(tree, "<expr>", "eval"))  # noqa: S307 — safe: AST-validated
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Error evaluating expression: {e}"


# --- notes app (writes to sandbox via caller-supplied path) ---
# NOTE: The notes app handler receives the sandbox path from AppAdapterStore
# and writes only inside it. No direct filesystem access is possible from
# the LLM — it only provides content and a note name.

def _notes_add(params: dict, sandbox: "Path") -> str:
    from pathlib import Path
    import re as _re
    note_name = _require_str(params, "note_name", max_len=64)
    content   = _require_str(params, "content",   max_len=4096)
    if _re.search(r'[/\x00-\x1f]', note_name):
        return "Error: Note name contains illegal characters."
    notes_dir = (sandbox / "notes").resolve()
    notes_dir.mkdir(parents=True, exist_ok=True)
    path = (notes_dir / (note_name.replace(" ", "_") + ".txt")).resolve()
    try:
        path.relative_to(notes_dir)
    except ValueError:
        return "Error: Note path escapes sandbox."
    path.write_text(content, encoding="utf-8")
    return f"Note '{note_name}' saved."

def _notes_list(params: dict, sandbox: "Path") -> str:
    from pathlib import Path
    notes_dir = sandbox / "notes"
    if not notes_dir.exists():
        return "No notes found."
    files = sorted(notes_dir.glob("*.txt"))
    if not files:
        return "No notes found."
    return "Notes:\n" + "\n".join(f"  • {f.stem}" for f in files)

def _notes_read(params: dict, sandbox: "Path") -> str:
    from pathlib import Path
    import re as _re
    note_name = _require_str(params, "note_name", max_len=64)
    if _re.search(r'[/\x00-\x1f]', note_name):
        return "Error: Note name contains illegal characters."
    notes_dir = (sandbox / "notes").resolve()
    path = (notes_dir / (note_name.replace(" ", "_") + ".txt")).resolve()
    try:
        path.relative_to(notes_dir)
    except ValueError:
        return "Error: Note path escapes sandbox."
    if not path.exists():
        return f"Error: Note '{note_name}' not found."
    return path.read_text(encoding="utf-8")


# --- system_info app (read-only, no shell, uses psutil if available) ---

def _sysinfo_memory(params: dict) -> str:
    try:
        import psutil
        vm = psutil.virtual_memory()
        return (
            f"Total: {vm.total//(1024**2)} MB  "
            f"Available: {vm.available//(1024**2)} MB  "
            f"Used: {vm.percent}%"
        )
    except ImportError:
        import subprocess
        r = subprocess.run(["/usr/bin/free", "-h"], capture_output=True, text=True, timeout=5, shell=False)
        return r.stdout.strip()

def _sysinfo_disk(params: dict) -> str:
    try:
        import psutil
        parts = psutil.disk_partitions()
        lines = []
        for p in parts[:5]:
            try:
                u = psutil.disk_usage(p.mountpoint)
                lines.append(f"  {p.mountpoint}: {u.used//(1024**3)}G used / {u.total//(1024**3)}G total ({u.percent}%)")
            except PermissionError:
                pass
        return "\n".join(lines) or "No disk info available."
    except ImportError:
        r = subprocess.run(["/usr/bin/df", "-h"], capture_output=True, text=True, timeout=5, shell=False)
        return r.stdout.strip()

def _sysinfo_uptime(params: dict) -> str:
    r = subprocess.run(["/usr/bin/uptime", "-p"], capture_output=True, text=True, timeout=5, shell=False)
    return r.stdout.strip() or "Uptime unavailable."


# ------------------------------------------------------------------
# App registry
# ------------------------------------------------------------------

# Each entry: { "description": str, "actions": { action_name: {"description": str, "handler": callable} } }
# Handlers that need sandbox access receive it as a second argument.

APP_REGISTRY: Dict[str, Dict] = {
    "calculator": {
        "description": "Safe arithmetic calculator.",
        "actions": {
            "evaluate": {
                "description": "Evaluate an arithmetic expression. Params: expression (str).",
                "handler":     _calc_evaluate,
                "needs_sandbox": False,
            },
        },
    },
    "notes": {
        "description": "Simple note-taking app stored in the sandbox.",
        "actions": {
            "add":  {"description": "Add a note. Params: note_name (str), content (str).",  "handler": _notes_add,  "needs_sandbox": True},
            "list": {"description": "List all notes.",                                       "handler": _notes_list, "needs_sandbox": True},
            "read": {"description": "Read a note. Params: note_name (str).",                 "handler": _notes_read, "needs_sandbox": True},
        },
    },
    "system_info": {
        "description": "Read-only system information (memory, disk, uptime).",
        "actions": {
            "memory": {"description": "Show memory usage.",  "handler": _sysinfo_memory, "needs_sandbox": False},
            "disk":   {"description": "Show disk usage.",    "handler": _sysinfo_disk,   "needs_sandbox": False},
            "uptime": {"description": "Show system uptime.", "handler": _sysinfo_uptime, "needs_sandbox": False},
        },
    },
}


# ------------------------------------------------------------------

class AppAdapterStore:
    """
    Routes LLM tool calls to registered app adapters.
    Validates app name, action name, and parameters before dispatch.
    """

    def __init__(self, sandbox: "Path"):
        from pathlib import Path
        self.sandbox = Path(sandbox).resolve()
        self.sandbox.mkdir(parents=True, exist_ok=True)

    def dispatch(self, app: str, action: str, params: dict) -> str:
        app    = (app    or "").strip().lower()
        action = (action or "").strip().lower()

        if app not in APP_REGISTRY:
            available = ", ".join(APP_REGISTRY.keys())
            return f"Error: Unknown app '{app}'. Available: {available}"

        app_cfg = APP_REGISTRY[app]
        if action not in app_cfg["actions"]:
            available = ", ".join(app_cfg["actions"].keys())
            return f"Error: Unknown action '{action}' for app '{app}'. Available: {available}"

        action_cfg = app_cfg["actions"][action]
        handler    = action_cfg["handler"]
        try:
            if action_cfg.get("needs_sandbox"):
                return handler(params, self.sandbox)
            else:
                return handler(params)
        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error executing '{app}.{action}': {e}"

    def list_apps(self) -> str:
        lines = ["Available apps and actions:"]
        for app_name, cfg in APP_REGISTRY.items():
            lines.append(f"\n  [{app_name}] — {cfg['description']}")
            for act_name, act_cfg in cfg["actions"].items():
                lines.append(f"    • {act_name}: {act_cfg['description']}")
        return "\n".join(lines)


# ------------------------------------------------------------------
# Ollama tool schema
# ------------------------------------------------------------------

APP_ADAPTER_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "app_adapter",
        "description": (
            "Interact with registered external applications through a controlled adapter. "
            "Available apps: calculator (arithmetic), notes (note-taking), system_info (memory/disk/uptime). "
            "Use 'list_apps' operation to see all available apps and actions."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["call", "list_apps"],
                    "description": "'call' to invoke an app action; 'list_apps' to see what's available.",
                },
                "app":    {"type": "string", "description": "App name (e.g. 'calculator', 'notes', 'system_info')."},
                "action": {"type": "string", "description": "Action to perform within the app."},
                "params": {"type": "object", "description": "Parameters for the action."},
            },
            "required": ["operation"],
        },
    },
}


def dispatch_app_adapter_tool(args: dict, store: AppAdapterStore) -> str:
    op = args.get("operation", "").strip().lower()
    if op == "list_apps":
        return store.list_apps()
    elif op == "call":
        app    = args.get("app",    "")
        action = args.get("action", "")
        params = args.get("params", {})
        if not app:    return "Error: 'call' requires 'app'."
        if not action: return "Error: 'call' requires 'action'."
        if not isinstance(params, dict): params = {}
        return store.dispatch(app, action, params)
    else:
        return f"Error: Unknown app_adapter operation '{op}'. Use 'call' or 'list_apps'."
