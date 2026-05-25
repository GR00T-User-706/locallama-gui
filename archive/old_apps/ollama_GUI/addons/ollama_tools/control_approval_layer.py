#!/usr/bin/env python3
"""
control_approval_layer.py  (v5 — NEW FILE)
--------------------------------------------
Interactive Approval Layer (Human-in-the-Loop).

Allows optional user confirmation before executing sensitive tool calls.
Supports two backends:
  - CLI:    prints a prompt to stdout and reads from stdin
  - GUI:    calls a registered Tkinter callback (messagebox.askyesno or custom)

When approval_mode is OFF, all calls pass through immediately.
When approval_mode is ON, calls flagged REQUIRE_APPROVAL by the Gatekeeper
are held until the user responds.

Timeout behaviour:
  If the user does not respond within `timeout_sec`, the default_on_timeout
  decision is applied (default: DENY for safety).

Integration point:
    ControlPipeline.dispatch()
      → Gatekeeper returns REQUIRE_APPROVAL
      → ApprovalLayer.request_approval()
      → (APPROVED | DENIED)
"""

import logging
import threading
import time
from enum import Enum
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class ApprovalDecision(str, Enum):
    APPROVED = "APPROVED"
    DENIED   = "DENIED"
    TIMEOUT  = "TIMEOUT"


class ApprovalLayer:
    """
    Manages human-in-the-loop approval for sensitive tool calls.

    Usage (CLI mode):
        al = ApprovalLayer(mode="cli")
        decision = al.request_approval("execute_system_command", {"command": "df", "args": []})

    Usage (GUI mode — register a callback first):
        al = ApprovalLayer(mode="gui")
        al.register_gui_callback(lambda tool, args: messagebox.askyesno(...))
        decision = al.request_approval("execute_system_command", {...})

    Usage (disabled — all pass through):
        al = ApprovalLayer(mode="off")
    """

    def __init__(
        self,
        mode:              str   = "cli",      # "cli" | "gui" | "off"
        timeout_sec:       float = 30.0,
        default_on_timeout: ApprovalDecision = ApprovalDecision.DENIED,
    ):
        if mode not in ("cli", "gui", "off"):
            raise ValueError(f"ApprovalLayer mode must be 'cli', 'gui', or 'off'. Got: {mode!r}")
        self.mode               = mode
        self.timeout_sec        = timeout_sec
        self.default_on_timeout = default_on_timeout
        self._gui_callback: Optional[Callable[[str, dict], bool]] = None
        self._pending_lock      = threading.Lock()

    # ------------------------------------------------------------------ public

    def register_gui_callback(self, callback: Callable[[str, dict], bool]) -> None:
        """
        Register a GUI approval callback.
        The callback receives (tool_name: str, args: dict) and must return
        True (approved) or False (denied).

        Example Tkinter integration:
            def my_approval(tool_name, args):
                import tkinter.messagebox as mb
                msg = f"Allow tool call?\\n\\nTool: {tool_name}\\nArgs: {args}"
                return mb.askyesno("Tool Approval Required", msg)

            approval_layer.register_gui_callback(my_approval)
        """
        self._gui_callback = callback

    def request_approval(
        self,
        tool_name: str,
        args:      dict,
        reason:    str = "",
    ) -> ApprovalDecision:
        """
        Request user approval for a tool call.
        Returns ApprovalDecision.APPROVED or DENIED (or TIMEOUT).
        """
        if self.mode == "off":
            return ApprovalDecision.APPROVED

        if self.mode == "gui":
            return self._gui_approval(tool_name, args, reason)

        # Default: CLI
        return self._cli_approval(tool_name, args, reason)

    def set_mode(self, mode: str) -> None:
        if mode not in ("cli", "gui", "off"):
            raise ValueError(f"Invalid mode: {mode!r}")
        self.mode = mode

    # ------------------------------------------------------------------ backends

    def _cli_approval(self, tool_name: str, args: dict, reason: str) -> ApprovalDecision:
        """
        Prompt the user on the terminal with a timeout.
        Uses a background thread to read stdin so we can enforce the timeout.
        """
        prompt_lines = [
            "\n" + "!" * 60,
            "  TOOL APPROVAL REQUIRED",
            f"  Tool    : {tool_name}",
            f"  Args    : {str(args)[:200]}",
        ]
        if reason:
            prompt_lines.append(f"  Reason  : {reason}")
        prompt_lines += [
            f"  Timeout : {self.timeout_sec:.0f}s (default: {self.default_on_timeout.value})",
            "!" * 60,
            "  Allow this tool call? [y/N] ",
        ]
        print("\n".join(prompt_lines), end="", flush=True)

        result_holder = [None]

        def _read():
            try:
                ans = input().strip().lower()
                result_holder[0] = ans
            except (EOFError, OSError):
                result_holder[0] = ""

        t = threading.Thread(target=_read, daemon=True)
        t.start()
        t.join(timeout=self.timeout_sec)

        if result_holder[0] is None:
            print(f"\n[Approval] Timed out → {self.default_on_timeout.value}")
            return self.default_on_timeout

        if result_holder[0] in ("y", "yes"):
            print("[Approval] APPROVED")
            return ApprovalDecision.APPROVED
        else:
            print("[Approval] DENIED")
            return ApprovalDecision.DENIED

    def _gui_approval(self, tool_name: str, args: dict, reason: str) -> ApprovalDecision:
        """
        Delegate to the registered GUI callback.
        Falls back to CLI if no callback is registered.
        """
        if self._gui_callback is None:
            logger.warning(
                "[ApprovalLayer] GUI mode but no callback registered. "
                "Falling back to CLI."
            )
            return self._cli_approval(tool_name, args, reason)

        try:
            approved = self._gui_callback(tool_name, args)
            return ApprovalDecision.APPROVED if approved else ApprovalDecision.DENIED
        except Exception as e:
            logger.error("[ApprovalLayer] GUI callback raised: %s. Denying.", e)
            return ApprovalDecision.DENIED


# ------------------------------------------------------------------
# Ready-made Tkinter callback factory
# ------------------------------------------------------------------

def make_tkinter_approval_callback(parent_widget=None) -> Callable:
    """
    Returns a GUI callback that shows a Tkinter messagebox.

    Usage in your Tkinter app:
        from control_approval_layer import make_tkinter_approval_callback
        approval_layer.register_gui_callback(
            make_tkinter_approval_callback(parent_widget=root)
        )
    """
    def _callback(tool_name: str, args: dict) -> bool:
        try:
            import tkinter.messagebox as mb
            msg = (
                f"The LLM wants to call a tool.\n\n"
                f"Tool:  {tool_name}\n"
                f"Args:  {str(args)[:300]}\n\n"
                "Allow this?"
            )
            return mb.askyesno(
                "Tool Approval Required",
                msg,
                parent=parent_widget,
                icon="warning",
            )
        except Exception as e:
            logger.error("[ApprovalLayer] Tkinter callback error: %s", e)
            return False   # deny on error

    return _callback
