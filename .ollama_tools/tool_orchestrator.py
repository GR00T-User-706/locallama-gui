#!/usr/bin/env python3
"""
tool_orchestrator.py  (v4 — NEW FILE)
---------------------------------------
Central Orchestrator Layer for the Ollama Tool Framework.

Receives ALL tool calls from the LLM and routes them to the correct
isolated tool module. Enforces:
  - Rate limits (per-window call cap)
  - Permission checks (session mode)
  - Input validation (tool name and operation exist)
  - Logging of every dispatched call

Architecture:
  LLM → OllamaToolEngine.chat() → ToolOrchestrator.dispatch() → Tool Module

The orchestrator is the ONLY path to any tool. No tool is called directly
by the engine after v4 — all calls go through here.

Session modes (inherited from v3):
  full        — all tools enabled
  restricted  — system commands disabled
  read-only   — sandbox file writes disabled

Rate limiting:
  Default: 20 calls per 60-second window (configurable).
  Prevents runaway loops even if the per-turn cap is bypassed.
"""

import time
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Imports from existing v3 modules (UNCHANGED)
# ------------------------------------------------------------------
from tool_memory        import MemoryStore,        MEMORY_TOOL_SCHEMA,       dispatch_memory_tool
from tool_sandbox_files import SandboxedFileStore, SANDBOX_FILE_TOOL_SCHEMA, dispatch_sandbox_file_tool
from ollama_tools       import (
    execute_system_command, SYSTEM_COMMAND_TOOL_SCHEMA,
    SESSION_PERMISSION_MODES,
)

# ------------------------------------------------------------------
# Imports from new v4 tool modules
# ------------------------------------------------------------------
from tool_book_writer      import BookWriterStore,       BOOK_WRITER_TOOL_SCHEMA,      dispatch_book_writer_tool
from tool_app_adapter      import AppAdapterStore,       APP_ADAPTER_TOOL_SCHEMA,      dispatch_app_adapter_tool
from tool_context_builder  import ContextBuilderStore,   CONTEXT_BUILDER_TOOL_SCHEMA,  dispatch_context_builder_tool
from tool_system_inspect   import SystemInspectStore,    SYSTEM_INSPECT_TOOL_SCHEMA,   dispatch_system_inspect_tool
from tool_workspace_manager import WorkspaceManagerStore, WORKSPACE_MANAGER_TOOL_SCHEMA, dispatch_workspace_manager_tool


# ------------------------------------------------------------------
# Rate limiter
# ------------------------------------------------------------------

class _RateLimiter:
    """
    Simple sliding-window rate limiter.
    Counts tool calls within a rolling time window.
    """
    def __init__(self, max_calls: int = 20, window_seconds: int = 60):
        self.max_calls      = max_calls
        self.window_seconds = window_seconds
        self._timestamps: List[float] = []

    def check(self) -> Tuple[bool, str]:
        """
        Returns (allowed: bool, message: str).
        Prunes expired timestamps before checking.
        """
        now = time.monotonic()
        self._timestamps = [t for t in self._timestamps if now - t < self.window_seconds]
        if len(self._timestamps) >= self.max_calls:
            oldest   = self._timestamps[0]
            wait_sec = self.window_seconds - (now - oldest)
            return False, (
                f"Rate limit reached: {self.max_calls} tool calls per "
                f"{self.window_seconds}s window. "
                f"Try again in {wait_sec:.0f}s."
            )
        self._timestamps.append(now)
        return True, ""

    def status(self) -> dict:
        now = time.monotonic()
        self._timestamps = [t for t in self._timestamps if now - t < self.window_seconds]
        oldest = self._timestamps[0] if self._timestamps else now
        return {
            "calls_this_window":   len(self._timestamps),
            "max_calls_per_window": self.max_calls,
            "seconds_until_reset": max(0.0, self.window_seconds - (now - oldest)),
        }


# ------------------------------------------------------------------
# ToolOrchestrator
# ------------------------------------------------------------------

class ToolOrchestrator:
    """
    Central routing and enforcement layer for all tool calls.

    Usage:
        orch = ToolOrchestrator(sandbox_dir=..., memory_path=...)
        result = orch.dispatch("memory", {"operation": "recall"})
        schemas = orch.active_schemas()
    """

    def __init__(
        self,
        sandbox_dir:             Path = None,
        memory_path:             Path = None,
        session_mode:            str  = "full",
        rate_limit_calls:        int  = 20,
        rate_limit_window:       int  = 60,
        allow_firejail_fallback: bool = False,
    ):
        base = Path.home() / ".ollama_tools"

        # ---- instantiate stores ----
        self.memory_store  = MemoryStore(
            path=memory_path or base / "memory.json"
        )
        self.sandbox_store = SandboxedFileStore(
            sandbox_dir=sandbox_dir or base / "sandbox",
            allow_firejail_fallback=allow_firejail_fallback,
        )
        book_sandbox = (sandbox_dir or base / "sandbox") / "books"
        self.book_store      = BookWriterStore(sandbox=book_sandbox)
        self.app_store       = AppAdapterStore(sandbox=sandbox_dir or base / "sandbox")
        self.context_store   = ContextBuilderStore(self.memory_store, self.sandbox_store)
        self.workspace_store = WorkspaceManagerStore(sandbox=sandbox_dir or base / "sandbox")

        # system_inspect needs a reference to self (the orchestrator)
        self.inspect_store = SystemInspectStore(self, self.memory_store, self.sandbox_store)

        self._rate_limiter = _RateLimiter(rate_limit_calls, rate_limit_window)
        self.session_mode  = "full"

        # ---- tool registry ----
        # Each entry: schema, dispatcher callable, enabled flag, description
        self._registry: Dict[str, Dict] = {
            # --- v3 tools ---
            "execute_system_command": {
                "schema":      SYSTEM_COMMAND_TOOL_SCHEMA,
                "dispatch":    self._dispatch_system_command,
                "enabled":     True,
                "description": "Run approved Linux system commands",
            },
            "memory": {
                "schema":      MEMORY_TOOL_SCHEMA,
                "dispatch":    lambda args: dispatch_memory_tool(args, self.memory_store),
                "enabled":     True,
                "description": "Persistent key/value and structured memory",
            },
            "sandbox_file": {
                "schema":      SANDBOX_FILE_TOOL_SCHEMA,
                "dispatch":    lambda args: dispatch_sandbox_file_tool(args, self.sandbox_store),
                "enabled":     True,
                "description": "Read/write files in the secure sandbox",
            },
            # --- v4 tools ---
            "book_writer": {
                "schema":      BOOK_WRITER_TOOL_SCHEMA,
                "dispatch":    lambda args: dispatch_book_writer_tool(args, self.book_store),
                "enabled":     True,
                "description": "Structured long-form book/document writing",
            },
            "app_adapter": {
                "schema":      APP_ADAPTER_TOOL_SCHEMA,
                "dispatch":    lambda args: dispatch_app_adapter_tool(args, self.app_store),
                "enabled":     True,
                "description": "Controlled interaction with registered apps",
            },
            "context_builder": {
                "schema":      CONTEXT_BUILDER_TOOL_SCHEMA,
                "dispatch":    lambda args: dispatch_context_builder_tool(args, self.context_store),
                "enabled":     True,
                "description": "Fetch and summarize context from memory and files",
            },
            "system_inspect": {
                "schema":      SYSTEM_INSPECT_TOOL_SCHEMA,
                "dispatch":    lambda args: dispatch_system_inspect_tool(args, self.inspect_store),
                "enabled":     True,
                "description": "Inspect available tools, permissions, and sandbox state",
            },
            "workspace_manager": {
                "schema":      WORKSPACE_MANAGER_TOOL_SCHEMA,
                "dispatch":    lambda args: dispatch_workspace_manager_tool(args, self.workspace_store),
                "enabled":     True,
                "description": "Manage multi-file project workspaces in the sandbox",
            },
        }

        # Apply session mode now that _registry is built
        self._apply_session_mode(session_mode)

        print(f"  [Orchestrator] {len(self._registry)} tools registered, mode='{self.session_mode}'")

    # ------------------------------------------------------------------ session mode

    def _apply_session_mode(self, mode: str) -> None:
        if mode not in SESSION_PERMISSION_MODES:
            logger.warning("[Orchestrator] Unknown session mode '%s', defaulting to 'full'.", mode)
            mode = "full"
        self.session_mode = mode
        policy = SESSION_PERMISSION_MODES[mode]
        # Apply v3 policy to the three original tools; new tools follow full access
        for tool_name, allowed in policy.items():
            if tool_name in self._registry:
                self._registry[tool_name]["enabled"] = allowed
        logger.info("[Orchestrator] Session mode set to '%s'.", mode)

    def set_session_mode(self, mode: str) -> None:
        self._apply_session_mode(mode)

    # ------------------------------------------------------------------ system command wrapper

    def _dispatch_system_command(self, args: dict) -> str:
        return execute_system_command(args.get("command", ""), args.get("args", []))

    # ------------------------------------------------------------------ public API

    def dispatch(self, tool_name: str, args: dict) -> str:
        """
        Main entry point.  Called by OllamaToolEngine for every tool call.
        Enforces: rate limit → permission check → validation → dispatch.
        """
        # 1. Rate limit
        allowed, msg = self._rate_limiter.check()
        if not allowed:
            logger.warning("[Orchestrator] Rate limit hit for tool '%s'.", tool_name)
            return f"Error: {msg}"

        # 2. Tool exists?
        if tool_name not in self._registry:
            available = ", ".join(self._registry.keys())
            return f"Error: Unknown tool '{tool_name}'. Available: {available}"

        entry = self._registry[tool_name]

        # 3. Permission check
        if not entry["enabled"]:
            return (
                f"Error: Tool '{tool_name}' is disabled in '{self.session_mode}' mode. "
                "Ask the user to change the session mode to access this tool."
            )

        # 4. Input validation — args must be a dict
        if not isinstance(args, dict):
            return f"Error: Tool arguments must be a JSON object, got {type(args).__name__}."

        # 5. Dispatch
        logger.info("[Orchestrator] Dispatching '%s' with args: %s", tool_name, str(args)[:120])
        try:
            result = entry["dispatch"](args)
            logger.info("[Orchestrator] '%s' returned: %s", tool_name, str(result)[:120])
            return result
        except Exception as e:
            logger.error("[Orchestrator] '%s' raised exception: %s", tool_name, e)
            return f"Error: Tool '{tool_name}' encountered an unexpected error: {e}"

    def active_schemas(self) -> List[dict]:
        """Return Ollama-compatible tool schemas for all enabled tools."""
        return [
            entry["schema"]
            for entry in self._registry.values()
            if entry["enabled"]
        ]

    def list_tools(self, enabled_only: bool = False) -> List[dict]:
        """Return tool metadata for introspection / GUI display."""
        return [
            {
                "name":        name,
                "description": entry["description"],
                "enabled":     entry["enabled"],
            }
            for name, entry in self._registry.items()
            if not enabled_only or entry["enabled"]
        ]

    def toggle_tool(self, tool_name: str, enabled: bool) -> None:
        """Enable or disable a tool at runtime."""
        if tool_name in self._registry:
            self._registry[tool_name]["enabled"] = enabled

    def get_rate_limit_status(self) -> dict:
        return self._rate_limiter.status()
