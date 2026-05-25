#!/usr/bin/env python3
"""
tool_system_inspect.py  (v4 — NEW FILE)
-----------------------------------------
System Introspection Tool for Ollama LLMs.

Lets the LLM understand its own environment safely.
Exposes ONLY controlled metadata — no host-level introspection,
no sensitive system information, no raw filesystem access.

Operations:
  list_available_tools  — all tools registered in the orchestrator
  show_enabled_tools    — only currently enabled tools
  show_permissions      — current session permission mode
  list_sandbox_files    — files in the sandbox directory
  list_memory_keys      — keys stored in persistent memory

Constraints:
  - No sensitive system exposure (no /etc, no env vars, no secrets)
  - No host-level introspection (no raw /proc, no netstat, no uid/gid)
  - Only controlled metadata from the orchestrator and stores
  - No shell calls
"""

from typing import Dict, Any


class SystemInspectStore:
    """
    Provides read-only introspection of the agent's own state.
    Receives references to the orchestrator and stores — does not own them.
    """

    def __init__(self, orchestrator, memory_store, sandbox_store):
        """
        orchestrator  : ToolOrchestrator instance (from tool_orchestrator.py)
        memory_store  : MemoryStore instance
        sandbox_store : SandboxedFileStore instance
        """
        self.orchestrator = orchestrator
        self.memory       = memory_store
        self.sandbox      = sandbox_store

    # ------------------------------------------------------------------ operations

    def list_available_tools(self) -> str:
        """Return all tools registered in the orchestrator (enabled or not)."""
        tools = self.orchestrator.list_tools(enabled_only=False)
        if not tools:
            return "No tools are registered."
        lines = ["All registered tools:"]
        for t in tools:
            status = "ON " if t["enabled"] else "OFF"
            lines.append(f"  [{status}] {t['name']:<28} {t['description']}")
        return "\n".join(lines)

    def show_enabled_tools(self) -> str:
        """Return only currently enabled tools."""
        tools = self.orchestrator.list_tools(enabled_only=True)
        if not tools:
            return "No tools are currently enabled."
        lines = ["Enabled tools:"]
        for t in tools:
            lines.append(f"  • {t['name']:<28} {t['description']}")
        return "\n".join(lines)

    def show_permissions(self) -> str:
        """Return the current session permission mode."""
        mode  = getattr(self.orchestrator, "session_mode", "unknown")
        rates = self.orchestrator.get_rate_limit_status()
        lines = [
            f"Session mode    : {mode}",
            f"Rate limit      : {rates['calls_this_window']} / {rates['max_calls_per_window']} calls this window",
            f"Window resets in: {rates['seconds_until_reset']:.0f}s",
        ]
        return "\n".join(lines)

    def list_sandbox_files(self) -> str:
        """Return the list of files in the sandbox directory."""
        return self.sandbox.list_files()

    def list_memory_keys(self) -> str:
        """Return all keys stored in persistent memory."""
        return self.memory.recall(key=None)


# ------------------------------------------------------------------
# Ollama tool schema
# ------------------------------------------------------------------

SYSTEM_INSPECT_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "system_inspect",
        "description": (
            "Inspect your own environment: see what tools are available, "
            "what permissions you have, what files are in the sandbox, "
            "and what you have stored in memory."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": [
                        "list_available_tools",
                        "show_enabled_tools",
                        "show_permissions",
                        "list_sandbox_files",
                        "list_memory_keys",
                    ],
                    "description": "The introspection operation to perform.",
                },
            },
            "required": ["operation"],
        },
    },
}


def dispatch_system_inspect_tool(args: dict, store: SystemInspectStore) -> str:
    op = args.get("operation", "").strip().lower()
    try:
        if op == "list_available_tools":
            return store.list_available_tools()
        elif op == "show_enabled_tools":
            return store.show_enabled_tools()
        elif op == "show_permissions":
            return store.show_permissions()
        elif op == "list_sandbox_files":
            return store.list_sandbox_files()
        elif op == "list_memory_keys":
            return store.list_memory_keys()
        else:
            return (
                f"Error: Unknown system_inspect operation '{op}'. "
                "Use list_available_tools, show_enabled_tools, show_permissions, "
                "list_sandbox_files, or list_memory_keys."
            )
    except Exception as e:
        return f"Error: {e}"
