#!/usr/bin/env python3
"""
control_pipeline.py  (v5 — NEW FILE)
--------------------------------------
Control Pipeline — the middleware wrapper.

This is the SINGLE integration point that sits between the LLM engine
and the ToolOrchestrator. It chains all 5 control modules in order:

    LLM → ControlPipeline.dispatch()
              ├── 1. BehaviorGovernor.evaluate()     (loop/spam detection)
              ├── 2. ToolGatekeeper.evaluate()        (arg scan, frequency, sensitivity)
              ├── 3. ApprovalLayer.request_approval() (human-in-the-loop, if needed)
              ├── 4. ToolOrchestrator.dispatch()      (actual execution)
              ├── 5. ContextMonitor.record()          (working memory update)
              └── 6. AuditLogger.log_call()           (append-only audit log)

The ControlPipeline is designed to be a DROP-IN replacement for
ToolOrchestrator.dispatch() in OllamaToolEngineV5.

NOTHING in v4 is modified. The v5 engine (ollama_tools_v5.py) simply
passes a ControlPipeline instance to OllamaToolEngine as its orchestrator
proxy, overriding only the dispatch() call path.

GUI integration:
  - pipeline.audit_logger.tail(n)        → live log panel
  - pipeline.context_monitor.context_summary() → activity panel
  - pipeline.gatekeeper.block_tool(name) → toggle switch
  - pipeline.approval_layer.set_mode("gui") + register_gui_callback()
  - pipeline.governor.reset()            → clear session state

Extensibility:
  New tools register with the ToolOrchestrator (v4) as before.
  The ControlPipeline picks them up automatically via orchestrator.active_schemas()
  and orchestrator._registry. No changes to the pipeline are needed.
"""

import time
import logging
from pathlib import Path
from typing import Callable, List, Optional

from tool_orchestrator        import ToolOrchestrator
from control_gatekeeper       import ToolGatekeeper,    Verdict
from control_audit_logger     import AuditLogger
from control_behavior_governor import BehaviorGovernor, GovernorDecision
from control_approval_layer   import ApprovalLayer,     ApprovalDecision
from control_context_monitor  import ContextMonitor

logger = logging.getLogger(__name__)


class ControlPipeline:
    """
    Middleware layer that wraps ToolOrchestrator with full control and observability.

    Usage:
        orch     = ToolOrchestrator(...)
        pipeline = ControlPipeline(orchestrator=orch)
        result   = pipeline.dispatch("memory", {"operation": "recall"})

    The pipeline exposes the same dispatch() interface as ToolOrchestrator,
    so it can be injected into OllamaToolEngineV5 transparently.
    """

    def __init__(
        self,
        orchestrator:        ToolOrchestrator,
        audit_log_path:      Optional[Path] = None,
        approval_mode:       str            = "cli",   # "cli" | "gui" | "off"
        approval_timeout:    float          = 30.0,
        enable_governor:     bool           = True,
        enable_gatekeeper:   bool           = True,
        enable_approval:     bool           = True,
        enable_monitor:      bool           = True,
        enable_audit:        bool           = True,
        session_id:          Optional[str]  = None,
    ):
        self.orchestrator = orchestrator
        self.session_id   = session_id

        base = Path.home() / ".ollama_tools"

        # ---- instantiate control modules ----
        self.governor = BehaviorGovernor() if enable_governor else _PassthroughGovernor()
        self.gatekeeper = ToolGatekeeper(
            known_tools=set(orchestrator._registry.keys())
        ) if enable_gatekeeper else _PassthroughGatekeeper(set(orchestrator._registry.keys()))

        self.approval_layer = ApprovalLayer(
            mode=approval_mode,
            timeout_sec=approval_timeout,
        ) if enable_approval else _PassthroughApproval()

        self.context_monitor = ContextMonitor() if enable_monitor else _PassthroughMonitor()

        self.audit_logger = AuditLogger(
            log_path=audit_log_path or base / "audit.jsonl"
        ) if enable_audit else _PassthroughAudit()

        # ---- feature flags (can be toggled at runtime) ----
        self._enable_governor   = enable_governor
        self._enable_gatekeeper = enable_gatekeeper
        self._enable_approval   = enable_approval
        self._enable_monitor    = enable_monitor
        self._enable_audit      = enable_audit

        print(
            f"  [ControlPipeline] Active: "
            f"governor={enable_governor} gatekeeper={enable_gatekeeper} "
            f"approval={enable_approval}({approval_mode}) "
            f"monitor={enable_monitor} audit={enable_audit}"
        )

    # ------------------------------------------------------------------ main dispatch

    def dispatch(self, tool_name: str, args: dict) -> str:
        """
        Full control pipeline dispatch.
        This is the method called instead of orchestrator.dispatch().
        """
        t_start  = time.monotonic()
        verdict_str = "ALLOW"
        result      = ""

        # ---- Step 1: Behavior Governor ----
        gov_verdict = self.governor.evaluate(tool_name, args)
        if gov_verdict.decision == GovernorDecision.BLOCK:
            result = f"Error: [Governor] {gov_verdict.reason}"
            self._audit(tool_name, args, "GOVERNOR_BLOCK", result, t_start)
            self.context_monitor.record(tool_name, args, result, "GOVERNOR_BLOCK")
            return result
        if gov_verdict.decision == GovernorDecision.THROTTLE:
            logger.warning("[Pipeline] Governor throttle: %s", gov_verdict.reason)
            # Throttle = warn but allow

        # ---- Step 2: Gatekeeper ----
        gk_verdict = self.gatekeeper.evaluate(tool_name, args)
        if gk_verdict.verdict == Verdict.DENY:
            result = f"Error: [Gatekeeper] {gk_verdict.reason}"
            self._audit(tool_name, args, "GATEKEEPER_DENY", result, t_start)
            self.context_monitor.record(tool_name, args, result, "GATEKEEPER_DENY")
            return result

        # ---- Step 3: Approval (if required) ----
        if gk_verdict.verdict == Verdict.REQUIRE_APPROVAL:
            decision = self.approval_layer.request_approval(
                tool_name, args, gk_verdict.reason
            )
            if decision != ApprovalDecision.APPROVED:
                result = f"Error: [Approval] Tool call denied by user (decision={decision.value})."
                self._audit(tool_name, args, f"APPROVAL_{decision.value}", result, t_start)
                self.context_monitor.record(tool_name, args, result, f"APPROVAL_{decision.value}")
                return result
            verdict_str = "APPROVED"

        # ---- Step 4: Execute via Orchestrator ----
        try:
            result = self.orchestrator.dispatch(tool_name, args)
        except Exception as e:
            result = f"Error: Orchestrator raised exception: {e}"
            logger.error("[Pipeline] Orchestrator exception for '%s': %s", tool_name, e)

        # ---- Step 5: Context Monitor ----
        warnings = self.context_monitor.record(tool_name, args, result, verdict_str)
        if warnings:
            for w in warnings:
                logger.warning("[Pipeline] ContextMonitor: %s", w)

        # ---- Step 6: Audit Log ----
        self._audit(tool_name, args, verdict_str, result, t_start)

        return result

    # ------------------------------------------------------------------ passthrough to orchestrator

    def active_schemas(self) -> List[dict]:
        return self.orchestrator.active_schemas()

    def list_tools(self, enabled_only: bool = False) -> List[dict]:
        return self.orchestrator.list_tools(enabled_only=enabled_only)

    def toggle_tool(self, tool_name: str, enabled: bool) -> None:
        self.orchestrator.toggle_tool(tool_name, enabled)
        # Also update gatekeeper's known_tools
        if enabled:
            self.gatekeeper.known_tools.add(tool_name)
        else:
            self.gatekeeper.known_tools.discard(tool_name)

    def set_session_mode(self, mode: str) -> None:
        self.orchestrator.set_session_mode(mode)

    def get_rate_limit_status(self) -> dict:
        return self.orchestrator.get_rate_limit_status()

    @property
    def session_mode(self) -> str:
        return self.orchestrator.session_mode

    @property
    def memory_store(self):
        return self.orchestrator.memory_store

    # ------------------------------------------------------------------ GUI helpers

    def register_gui_approval_callback(self, callback: Callable) -> None:
        """Register a Tkinter (or other GUI) approval callback."""
        self.approval_layer.register_gui_callback(callback)
        self.approval_layer.set_mode("gui")

    def set_approval_mode(self, mode: str) -> None:
        self.approval_layer.set_mode(mode)

    def get_audit_tail(self, n: int = 20) -> str:
        """Return formatted audit log tail for GUI display."""
        return self.audit_logger.format_tail(n)

    def get_activity_summary(self, n: int = 10) -> str:
        """Return context monitor summary for GUI display."""
        return self.context_monitor.context_summary(n)

    def verify_audit_chain(self) -> tuple:
        """Verify audit log hash chain integrity."""
        return self.audit_logger.verify_chain()

    def reset_session(self) -> None:
        """Reset governor and monitor state for a new conversation."""
        self.governor.reset()
        self.context_monitor.reset()

    # ------------------------------------------------------------------ internals

    def _audit(self, tool_name: str, args: dict, verdict: str, result: str, t_start: float) -> None:
        duration_ms = (time.monotonic() - t_start) * 1000
        self.audit_logger.log_call(
            tool_name=tool_name,
            args=args,
            verdict=verdict,
            result=result,
            duration_ms=duration_ms,
            session_id=self.session_id,
        )


# ------------------------------------------------------------------
# Passthrough stubs (used when a control module is disabled)
# ------------------------------------------------------------------

class _PassthroughGovernor:
    def evaluate(self, tool_name, args):
        class _V:
            decision = GovernorDecision.ALLOW
            reason   = "governor disabled"
        return _V()
    def reset(self): pass

class _PassthroughGatekeeper:
    def __init__(self, known_tools):
        self.known_tools = known_tools
        self.blocked_tools = set()
    def evaluate(self, tool_name, args):
        class _V:
            verdict  = Verdict.ALLOW
            reason   = "gatekeeper disabled"
        return _V()
    def block_tool(self, t): self.blocked_tools.add(t)
    def unblock_tool(self, t): self.blocked_tools.discard(t)
    def set_approval_required(self, t, r): pass

class _PassthroughApproval:
    def request_approval(self, *a, **kw): return ApprovalDecision.APPROVED
    def set_mode(self, m): pass
    def register_gui_callback(self, cb): pass

class _PassthroughMonitor:
    warnings = []
    def record(self, *a, **kw): return []
    def context_summary(self, n=10): return ""
    def get_warnings_for_prompt(self): return ""
    def reset(self): pass

class _PassthroughAudit:
    def log_call(self, *a, **kw): pass
    def tail(self, n=20): return []
    def format_tail(self, n=10): return "Audit logging disabled."
    def verify_chain(self): return True, None, "Audit logging disabled."
