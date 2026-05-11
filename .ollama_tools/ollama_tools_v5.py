#!/usr/bin/env python3
"""
ollama_tools_v5.py  (v5 — NEW FILE)
--------------------------------------
v5 Engine — OllamaToolEngine with full Control Pipeline.

This is the production entry point. It:
  1. Creates a ToolOrchestrator (v4, unchanged)
  2. Wraps it in a ControlPipeline (v5 middleware)
  3. Passes the pipeline to OllamaToolEngine (v4) as the orchestrator

The v4 engine sees the ControlPipeline as if it were the orchestrator
because ControlPipeline exposes the same interface:
  - dispatch(tool_name, args)
  - active_schemas()
  - list_tools()
  - toggle_tool()
  - set_session_mode()
  - session_mode property
  - memory_store property

NOTHING in v4 is modified.

Call flow:
    User prompt
      → OllamaToolEngineV5.chat()          [v4 engine, unchanged]
        → ollama.chat() with tool schemas
          → LLM returns tool_calls
            → engine._dispatch_tool()
              → ControlPipeline.dispatch()  [v5 middleware]
                → BehaviorGovernor
                → ToolGatekeeper
                → ApprovalLayer
                → ToolOrchestrator.dispatch() [v4, unchanged]
                → ContextMonitor.record()
                → AuditLogger.log_call()
              ← result string
            ← result injected into messages
          ← final LLM response
        ← answer string
      ← answer returned to user

GUI integration:
    engine.pipeline.get_audit_tail(20)         → live log panel content
    engine.pipeline.get_activity_summary()     → activity panel content
    engine.pipeline.gatekeeper.block_tool(t)   → toggle switch
    engine.pipeline.set_approval_mode("gui")   → switch to GUI approval dialogs
    engine.pipeline.register_gui_approval_callback(cb)
    engine.pipeline.verify_audit_chain()       → integrity check button
"""

import argparse
import sys
import types
from pathlib import Path
from typing import Optional

try:
    import ollama
except ImportError:
    print("ERROR: pip install ollama")
    raise SystemExit(1)

from tool_orchestrator  import ToolOrchestrator
from control_pipeline   import ControlPipeline
from ollama_tools_v4    import OllamaToolEngine   # v4 engine, unchanged


class OllamaToolEngineV5(OllamaToolEngine):
    """
    v5 engine: identical to v4 except it wraps the orchestrator in a ControlPipeline.
    All existing public methods (chat, clear_history, get_tool_info, etc.) are inherited.
    """

    def __init__(
        self,
        model:             str   = "mistral",
        memory_path:       Path  = None,
        sandbox_dir:       Path  = None,
        keep_history:      bool  = True,
        verbose:           bool  = True,
        max_tool_calls:    int   = 3,
        session_mode:      str   = "full",
        agent_mode:        bool  = False,
        structured_output: bool  = False,
        # v5 control layer options
        approval_mode:     str   = "cli",   # "cli" | "gui" | "off"
        approval_timeout:  float = 30.0,
        enable_governor:   bool  = True,
        enable_gatekeeper: bool  = True,
        enable_approval:   bool  = True,
        enable_monitor:    bool  = True,
        enable_audit:      bool  = True,
        audit_log_path:    Optional[Path] = None,
        session_id:        Optional[str]  = None,
    ):
        # Build orchestrator (v4, unchanged)
        orch = ToolOrchestrator(
            sandbox_dir=sandbox_dir,
            memory_path=memory_path,
            session_mode=session_mode,
        )

        # Wrap in control pipeline (v5)
        self.pipeline = ControlPipeline(
            orchestrator=orch,
            audit_log_path=audit_log_path,
            approval_mode=approval_mode,
            approval_timeout=approval_timeout,
            enable_governor=enable_governor,
            enable_gatekeeper=enable_gatekeeper,
            enable_approval=enable_approval,
            enable_monitor=enable_monitor,
            enable_audit=enable_audit,
            session_id=session_id,
        )

        # Inject pipeline as the orchestrator seen by the v4 engine
        super().__init__(
            model=model,
            keep_history=keep_history,
            verbose=verbose,
            max_tool_calls=max_tool_calls,
            session_mode=session_mode,
            agent_mode=agent_mode,
            structured_output=structured_output,
            orchestrator=self.pipeline,   # <-- the only v5 change
        )

    # ---- convenience passthrough methods for GUI ----

    def get_audit_log(self, n: int = 20) -> str:
        return self.pipeline.get_audit_tail(n)

    def get_activity_summary(self, n: int = 10) -> str:
        return self.pipeline.get_activity_summary(n)

    def verify_audit_integrity(self) -> tuple:
        return self.pipeline.verify_audit_chain()

    def reset_session(self) -> None:
        self.pipeline.reset_session()
        self.clear_history()

    def block_tool(self, tool_name: str) -> None:
        self.pipeline.gatekeeper.block_tool(tool_name)

    def unblock_tool(self, tool_name: str) -> None:
        self.pipeline.gatekeeper.unblock_tool(tool_name)

    def set_approval_mode(self, mode: str) -> None:
        self.pipeline.set_approval_mode(mode)

    def register_gui_approval_callback(self, callback) -> None:
        self.pipeline.register_gui_approval_callback(callback)


# ------------------------------------------------------------------
# CLI entry point
# ------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ollama Tool Framework v5")
    parser.add_argument("--model",        type=str,   default="mistral")
    parser.add_argument("--mode",         type=str,   default="full",
                        choices=["full", "restricted", "read-only"])
    parser.add_argument("--agent",        action="store_true")
    parser.add_argument("--structured",   action="store_true")
    parser.add_argument("--approval",     type=str,   default="off",
                        choices=["cli", "gui", "off"],
                        help="Human-in-the-loop approval mode (default: off)")
    parser.add_argument("--no-governor",  action="store_true")
    parser.add_argument("--no-gatekeeper",action="store_true")
    parser.add_argument("--no-audit",     action="store_true")
    parser.add_argument("--list-tools",   action="store_true")
    parser.add_argument("--audit-tail",   type=int,   default=0,
                        help="Print last N audit log entries and exit")
    parser.add_argument("--verify-audit", action="store_true")
    parser.add_argument("prompt",         nargs="*")
    args = parser.parse_args()

    engine = OllamaToolEngineV5(
        model=args.model,
        session_mode=args.mode,
        agent_mode=args.agent,
        structured_output=args.structured,
        approval_mode=args.approval,
        enable_governor=not args.no_governor,
        enable_gatekeeper=not args.no_gatekeeper,
        enable_audit=not args.no_audit,
    )

    if args.list_tools:
        print("\nRegistered tools:\n")
        for t in engine.get_tool_info():
            status = "ON " if t["enabled"] else "OFF"
            print(f"  [{status}] {t['name']:<28} {t['description']}")
        print()
        raise SystemExit(0)

    if args.audit_tail > 0:
        print(engine.get_audit_log(args.audit_tail))
        raise SystemExit(0)

    if args.verify_audit:
        ok, seq, msg = engine.verify_audit_integrity()
        print(f"Audit chain: {'VALID' if ok else 'BROKEN'} — {msg}")
        raise SystemExit(0 if ok else 1)

    prompt = " ".join(args.prompt).strip() or (
        "What tools do you have available? Use system_inspect to find out."
    )
    answer = engine.chat(prompt)
    print("\n" + "=" * 60)
    print(answer)
    print("\n" + "=" * 60)
    print("[Activity Summary]")
    print(engine.get_activity_summary())
