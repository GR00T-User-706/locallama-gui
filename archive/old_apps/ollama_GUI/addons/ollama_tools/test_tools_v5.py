#!/usr/bin/env python3
"""
test_tools_v5.py  (v5 — NEW FILE)
-----------------------------------
Full test suite for all v5 control layer additions.
Does NOT require Ollama to be running.

Coverage:
  control_gatekeeper       — allow, deny, suspicious args, frequency, sensitivity
  control_audit_logger     — append-only writes, hash chain, tail, verify
  control_behavior_governor— spam block, burst block, streak throttle, escalation chain
  control_approval_layer   — off mode, cli timeout, gui callback
  control_context_monitor  — record, redundancy, contradiction, summary
  control_pipeline         — full dispatch flow, each block path, passthrough
  ollama_tools_v5          — engine wiring, pipeline injection
"""

import sys, os, types, tempfile, shutil, time, json
from pathlib import Path

# Stub ollama
sys.modules.setdefault("ollama", types.ModuleType("ollama"))
sys.modules["ollama"].ResponseError = Exception

TEST_DIR = Path(tempfile.mkdtemp(prefix="ollama_v5_test_"))

from control_gatekeeper        import ToolGatekeeper, Verdict, Sensitivity
from control_audit_logger      import AuditLogger
from control_behavior_governor import BehaviorGovernor, GovernorDecision
from control_approval_layer    import ApprovalLayer, ApprovalDecision
from control_context_monitor   import ContextMonitor
from control_pipeline          import ControlPipeline
from tool_orchestrator         import ToolOrchestrator
from ollama_tools_v5           import OllamaToolEngineV5

GREEN = "\033[92m"; RED = "\033[91m"; RESET = "\033[0m"
passed = 0; failed = 0

def test(name, result=None, expect_error=False, expect_contains=None,
         expect_not_contains=None, expect_true=None):
    global passed, failed
    r  = str(result) if result is not None else ""
    ok = True; reason = ""
    if expect_true is not None:
        if not expect_true:
            ok = False; reason = f"Expected True condition. result={r!r}"
    else:
        if expect_error and not r.startswith("Error:"):
            ok = False; reason = f"Expected error, got: {r!r}"
        if not expect_error and r.startswith("Error:"):
            ok = False; reason = f"Unexpected error: {r!r}"
        if expect_contains and expect_contains not in r:
            ok = False; reason = f"Expected {expect_contains!r} in: {r!r}"
        if expect_not_contains and expect_not_contains in r:
            ok = False; reason = f"Did NOT expect {expect_not_contains!r} in: {r!r}"
    status = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
    print(f"  [{status}] {name}")
    if not ok: print(f"         {reason}")
    if ok: passed += 1
    else:  failed += 1

def section(t): print(f"\n{'='*60}\n  {t}\n{'='*60}")


KNOWN_TOOLS = {"execute_system_command", "memory", "sandbox_file",
               "book_writer", "app_adapter", "context_builder",
               "system_inspect", "workspace_manager"}

# ==============================================================================
section("CONTROL: Gatekeeper")
# ==============================================================================

gk = ToolGatekeeper(known_tools=KNOWN_TOOLS)

v = gk.evaluate("memory", {"operation": "recall", "key": "x"})
test("clean memory call → ALLOW", expect_true=v.verdict == Verdict.ALLOW)

v = gk.evaluate("unknown_tool", {})
test("unknown tool → DENY", expect_true=v.verdict == Verdict.DENY)
test("unknown tool reason mentions tool name", v.reason, expect_contains="unknown_tool")

v = gk.evaluate("execute_system_command", {"command": "ls", "args": []})
test("execute_system_command (HIGH sensitivity) → REQUIRE_APPROVAL",
     expect_true=v.verdict == Verdict.REQUIRE_APPROVAL)
test("verdict sensitivity is HIGH",
     expect_true=v.sensitivity == Sensitivity.HIGH)

v = gk.evaluate("memory", {"operation": "recall", "key": "x\x00y"})
test("null byte in arg → DENY", expect_true=v.verdict == Verdict.DENY)
test("null byte reason mentions suspicious", v.reason, expect_contains="Suspicious")

v = gk.evaluate("sandbox_file", {"operation": "read", "filename": "../../etc/passwd"})
test("path traversal in arg → DENY", expect_true=v.verdict == Verdict.DENY)

v = gk.evaluate("memory", {"operation": "recall", "key": "x; rm -rf /"})
test("shell chaining in arg → DENY", expect_true=v.verdict == Verdict.DENY)

# Frequency limit: memory allows 12 calls in 10s, so 13th should block
gk2 = ToolGatekeeper(known_tools=KNOWN_TOOLS)
for _ in range(12):
    gk2.evaluate("memory", {"operation": "recall", "key": "x"})
v = gk2.evaluate("memory", {"operation": "recall", "key": "x"})
test("per-tool frequency limit fires at max+1", expect_true=v.verdict == Verdict.DENY)
test("frequency limit reason is informative", v.reason, expect_contains="limit")

# Block/unblock
gk3 = ToolGatekeeper(known_tools=KNOWN_TOOLS)
gk3.block_tool("book_writer")
v = gk3.evaluate("book_writer", {"operation": "list_projects"})
test("blocked tool → DENY", expect_true=v.verdict == Verdict.DENY)
gk3.unblock_tool("book_writer")
v = gk3.evaluate("book_writer", {"operation": "list_projects"})
test("unblocked tool → ALLOW", expect_true=v.verdict == Verdict.ALLOW)

# Explicit approval required
gk4 = ToolGatekeeper(known_tools=KNOWN_TOOLS, require_approval_for={"memory"})
v = gk4.evaluate("memory", {"operation": "recall"})
test("explicit approval_for → REQUIRE_APPROVAL", expect_true=v.verdict == Verdict.REQUIRE_APPROVAL)


# ==============================================================================
section("CONTROL: AuditLogger")
# ==============================================================================

log_path = TEST_DIR / "test_audit.jsonl"
al = AuditLogger(log_path=log_path)

al.log_call("memory", {"operation": "recall"}, "ALLOW", "value: hello", 5.2)
al.log_call("sandbox_file", {"operation": "write", "filename": "f.txt"}, "ALLOW", "Written.", 12.1)
al.log_call("execute_system_command", {"command": "ls"}, "GATEKEEPER_DENY", "Error: blocked", 0.5)

entries = al.tail(10)
test("audit log has 3 entries", expect_true=len(entries) == 3)
test("first entry has correct tool", expect_true=entries[0]["tool"] == "memory")
test("entries have seq numbers", expect_true=entries[0]["seq"] == 1)
test("entries have timestamps", expect_true="ts" in entries[0])
test("entries have entry_hash", expect_true="entry_hash" in entries[0])
test("entries have prev_hash", expect_true="prev_hash" in entries[0])
test("first entry prev_hash is genesis", expect_true=entries[0]["prev_hash"] == AuditLogger.GENESIS_HASH)
test("second entry prev_hash matches first entry_hash",
     expect_true=entries[1]["prev_hash"] == entries[0]["entry_hash"])

ok, broken_seq, msg = al.verify_chain()
test("hash chain verifies as intact", expect_true=ok)
test("verify_chain message says intact", msg, expect_contains="intact")

# Tamper with the log
lines = log_path.read_text().splitlines()
tampered = json.loads(lines[0])
tampered["result"] = "TAMPERED"
lines[0] = json.dumps(tampered)
log_path.write_text("\n".join(lines) + "\n")
al2 = AuditLogger(log_path=log_path)
ok2, broken_seq2, msg2 = al2.verify_chain()
test("tampered entry detected by chain verification", expect_true=not ok2)

# format_tail
al3 = AuditLogger(log_path=TEST_DIR / "fmt_audit.jsonl")
al3.log_call("memory", {}, "ALLOW", "ok", 1.0)
fmt = al3.format_tail(5)
test("format_tail returns human-readable string", fmt, expect_contains="memory")
test("format_tail includes verdict", fmt, expect_contains="ALLOW")

# Persistence: new AuditLogger picks up existing seq and hash
al4 = AuditLogger(log_path=TEST_DIR / "persist_audit.jsonl")
al4.log_call("memory", {}, "ALLOW", "first", 1.0)
al5 = AuditLogger(log_path=TEST_DIR / "persist_audit.jsonl")
al5.log_call("memory", {}, "ALLOW", "second", 1.0)
entries5 = al5.tail(5)
test("persisted log has 2 entries", expect_true=len(entries5) == 2)
test("second entry seq is 2", expect_true=entries5[1]["seq"] == 2)
ok5, _, _ = al5.verify_chain()
test("persisted chain is valid", expect_true=ok5)


# ==============================================================================
section("CONTROL: BehaviorGovernor")
# ==============================================================================

gov = BehaviorGovernor(
    max_identical_in_window=3,
    identical_window_sec=60,
    max_same_tool_streak=4,
    global_burst_limit=10,
    burst_window_sec=5,
)

v = gov.evaluate("memory", {"operation": "recall", "key": "x"})
test("first call → ALLOW", expect_true=v.decision == GovernorDecision.ALLOW)

# Identical call spam
for _ in range(3):
    gov.evaluate("memory", {"operation": "recall", "key": "spam"})
v = gov.evaluate("memory", {"operation": "recall", "key": "spam"})
test("identical call spam → BLOCK", expect_true=v.decision == GovernorDecision.BLOCK)
test("spam block reason mentions loop", v.reason, expect_contains="loop")

# Same-tool streak
gov2 = BehaviorGovernor(max_same_tool_streak=3, global_burst_limit=100)
for i in range(3):
    gov2.evaluate("sandbox_file", {"operation": "read", "filename": f"f{i}.txt"})
v = gov2.evaluate("sandbox_file", {"operation": "read", "filename": "f99.txt"})
test("same-tool streak → THROTTLE", expect_true=v.decision == GovernorDecision.THROTTLE)

# Global burst
gov3 = BehaviorGovernor(global_burst_limit=5, burst_window_sec=60)
for i in range(5):
    gov3.evaluate(f"tool_{i}", {})
v = gov3.evaluate("memory", {})
test("global burst limit → BLOCK", expect_true=v.decision == GovernorDecision.BLOCK)
test("burst block reason mentions burst", v.reason, expect_contains="burst")

# Escalation chain: memory.recall → sandbox_file.write → execute_system_command
gov4 = BehaviorGovernor(global_burst_limit=100)
gov4.evaluate("memory",        {"operation": "recall"})
gov4.evaluate("sandbox_file",  {"operation": "write"})
v = gov4.evaluate("execute_system_command", {"command": "ls"})
test("escalation chain detected → BLOCK", expect_true=v.decision == GovernorDecision.BLOCK)
test("escalation reason mentions chain", v.reason, expect_contains="Escalation")

# Reset clears state
gov4.reset()
v = gov4.evaluate("execute_system_command", {"command": "ls"})
test("after reset, escalation chain no longer fires", expect_true=v.decision != GovernorDecision.BLOCK)

# recent_summary
gov5 = BehaviorGovernor(global_burst_limit=100)
gov5.evaluate("memory", {"operation": "recall"})
summary = gov5.recent_summary()
test("recent_summary returns string", summary, expect_contains="memory")


# ==============================================================================
section("CONTROL: ApprovalLayer")
# ==============================================================================

# Off mode — always approved
al_off = ApprovalLayer(mode="off")
d = al_off.request_approval("execute_system_command", {}, "test")
test("off mode → APPROVED", expect_true=d == ApprovalDecision.APPROVED)

# GUI mode with callback returning True
al_gui = ApprovalLayer(mode="gui")
al_gui.register_gui_callback(lambda tool, args: True)
d = al_gui.request_approval("execute_system_command", {}, "test")
test("gui callback True → APPROVED", expect_true=d == ApprovalDecision.APPROVED)

# GUI mode with callback returning False
al_gui2 = ApprovalLayer(mode="gui")
al_gui2.register_gui_callback(lambda tool, args: False)
d = al_gui2.request_approval("execute_system_command", {}, "test")
test("gui callback False → DENIED", expect_true=d == ApprovalDecision.DENIED)

# GUI mode with no callback falls back to CLI — skip actual CLI test in automated suite
# but verify it doesn't crash
al_gui3 = ApprovalLayer(mode="gui", timeout_sec=0.1,
                         default_on_timeout=ApprovalDecision.DENIED)
# No callback registered — will try CLI fallback, which will timeout immediately
d = al_gui3.request_approval("execute_system_command", {}, "test")
test("gui fallback to cli with timeout → DENIED (timeout)",
     expect_true=d == ApprovalDecision.DENIED)

# Invalid mode
try:
    ApprovalLayer(mode="invalid")
    test("invalid mode raises ValueError", expect_true=False)
except ValueError:
    test("invalid mode raises ValueError", expect_true=True)

# set_mode
al_m = ApprovalLayer(mode="off")
al_m.set_mode("gui")
al_m.register_gui_callback(lambda t, a: True)
d = al_m.request_approval("memory", {})
test("set_mode switches mode correctly", expect_true=d == ApprovalDecision.APPROVED)


# ==============================================================================
section("CONTROL: ContextMonitor")
# ==============================================================================

cm = ContextMonitor()

warnings = cm.record("memory", {"operation": "remember", "key": "x", "value": "1"}, "Remembered.", "ALLOW")
test("first record returns no warnings", expect_true=len(warnings) == 0)

# Redundancy: same call again
warnings = cm.record("memory", {"operation": "remember", "key": "x", "value": "1"}, "Remembered.", "ALLOW")
test("identical call returns redundancy warning", expect_true=len(warnings) > 0)
test("redundancy warning text is informative", warnings[0], expect_contains="Redundant")

# Contradiction: remember then forget same key
cm2 = ContextMonitor()
cm2.record("memory", {"operation": "remember", "key": "y"}, "ok", "ALLOW")
warnings2 = cm2.record("memory", {"operation": "forget", "key": "y"}, "ok", "ALLOW")
test("contradiction detected (remember → forget)", expect_true=len(warnings2) > 0)
test("contradiction warning is informative", warnings2[0], expect_contains="Contradictory")

# context_summary
cm3 = ContextMonitor()
cm3.record("memory",    {"operation": "recall"}, "val", "ALLOW")
cm3.record("sandbox_file", {"operation": "read", "filename": "f.txt"}, "content", "ALLOW")
summary = cm3.context_summary()
test("context_summary returns string", summary, expect_contains="memory")
test("context_summary includes sandbox_file", summary, expect_contains="sandbox_file")

# get_warnings_for_prompt
cm4 = ContextMonitor()
cm4.record("memory", {"operation": "remember", "key": "z"}, "ok", "ALLOW")
cm4.record("memory", {"operation": "remember", "key": "z"}, "ok", "ALLOW")  # triggers redundancy
prompt_warn = cm4.get_warnings_for_prompt()
test("get_warnings_for_prompt returns warning text", prompt_warn, expect_contains="Redundant")
# Calling again should be empty (consumed)
prompt_warn2 = cm4.get_warnings_for_prompt()
test("get_warnings_for_prompt clears after read", expect_true=prompt_warn2 == "")

# reset
cm5 = ContextMonitor()
cm5.record("memory", {}, "ok", "ALLOW")
cm5.reset()
test("reset clears history", expect_true=len(cm5.last_n(10)) == 0)


# ==============================================================================
section("CONTROL: Pipeline (full dispatch flow)")
# ==============================================================================

def _make_pipeline(approval_mode="off", **kwargs):
    orch = ToolOrchestrator(
        sandbox_dir=TEST_DIR / "pipe_sandbox",
        memory_path=TEST_DIR / "pipe_mem.json",
        session_mode="full",
    )
    return ControlPipeline(
        orchestrator=orch,
        audit_log_path=TEST_DIR / "pipe_audit.jsonl",
        approval_mode=approval_mode,
        **kwargs,
    )

pipe = _make_pipeline()

# Normal allowed call
r = pipe.dispatch("memory", {"operation": "remember", "key": "pipe_test", "value": "hello"})
test("pipeline: normal call dispatches and returns result", r, expect_contains="Remembered")

# Audit log was written
entries = pipe.audit_logger.tail(5)
test("pipeline: audit log has entry after dispatch", expect_true=len(entries) >= 1)
test("pipeline: audit entry has correct tool", expect_true=entries[-1]["tool"] == "memory")

# Context monitor recorded it
summary = pipe.get_activity_summary()
test("pipeline: activity summary includes tool call", summary, expect_contains="memory")

# Gatekeeper blocks suspicious arg
r = pipe.dispatch("memory", {"operation": "remember", "key": "x\x00y", "value": "v"})
test("pipeline: gatekeeper blocks null byte in arg", r, expect_error=True)
test("pipeline: block reason mentions Gatekeeper", r[7:] if r.startswith("Error:") else r, expect_contains="Gatekeeper")

# Governor blocks spam
pipe2 = _make_pipeline()
for _ in range(3):
    pipe2.dispatch("memory", {"operation": "recall", "key": "spam_key"})
r = pipe2.dispatch("memory", {"operation": "recall", "key": "spam_key"})
test("pipeline: governor blocks spam", r, expect_error=True)
test("pipeline: governor block reason in result", r[7:] if r.startswith("Error:") else r, expect_contains="Governor")

# Approval layer: off mode lets HIGH sensitivity through
pipe3 = _make_pipeline(approval_mode="off")
r = pipe3.dispatch("execute_system_command", {"command": "date", "args": []})
test("pipeline: approval=off lets HIGH sensitivity through", r, expect_not_contains="Error:")

# Approval layer: gui mode with deny callback blocks HIGH sensitivity
pipe4 = _make_pipeline(approval_mode="gui")
pipe4.approval_layer.register_gui_callback(lambda t, a: False)
r = pipe4.dispatch("execute_system_command", {"command": "date", "args": []})
test("pipeline: approval=gui with deny callback blocks call", r, expect_error=True)
test("pipeline: approval deny reason in result", r[7:] if r.startswith("Error:") else r, expect_contains="Approval")

# Approval layer: gui mode with approve callback allows HIGH sensitivity
pipe5 = _make_pipeline(approval_mode="gui")
pipe5.approval_layer.register_gui_callback(lambda t, a: True)
r = pipe5.dispatch("execute_system_command", {"command": "date", "args": []})
test("pipeline: approval=gui with approve callback allows call", r, expect_not_contains="Error:")

# toggle_tool
pipe6 = _make_pipeline()
pipe6.toggle_tool("book_writer", False)
r = pipe6.dispatch("book_writer", {"operation": "list_projects"})
test("pipeline: toggle_tool disables tool", r, expect_error=True)
pipe6.toggle_tool("book_writer", True)
r = pipe6.dispatch("book_writer", {"operation": "list_projects"})
test("pipeline: toggle_tool re-enables tool", r)

# session mode
pipe7 = _make_pipeline()
pipe7.set_session_mode("restricted")
r = pipe7.dispatch("execute_system_command", {"command": "date", "args": []})
test("pipeline: restricted mode blocks system commands", r, expect_error=True)

# verify audit chain
ok, _, msg = pipe.verify_audit_chain()
test("pipeline: audit chain is valid after normal use", expect_true=ok)

# reset_session clears governor and monitor
pipe8 = _make_pipeline()
for _ in range(3):
    pipe8.dispatch("memory", {"operation": "recall", "key": "rs_key"})
pipe8.reset_session()
r = pipe8.dispatch("memory", {"operation": "recall", "key": "rs_key"})
test("pipeline: reset_session clears governor spam state", r, expect_not_contains="Governor")


# ==============================================================================
section("ENGINE v5: wiring")
# ==============================================================================

eng = OllamaToolEngineV5(
    model="mistral",
    session_mode="full",
    approval_mode="off",
    verbose=False,
    audit_log_path=TEST_DIR / "v5_audit.jsonl",
)

test("v5 engine has pipeline attribute", expect_true=hasattr(eng, "pipeline"))
test("v5 engine pipeline is ControlPipeline", expect_true=isinstance(eng.pipeline, ControlPipeline))
test("v5 engine orchestrator is pipeline", expect_true=eng.orchestrator is eng.pipeline)
test("v5 engine has 8 tools", expect_true=len(eng.get_tool_info()) == 8)

# block/unblock passthrough
eng.block_tool("book_writer")
test("v5 engine block_tool works",
     expect_true=eng.pipeline.gatekeeper.blocked_tools == {"book_writer"})
eng.unblock_tool("book_writer")
test("v5 engine unblock_tool works",
     expect_true="book_writer" not in eng.pipeline.gatekeeper.blocked_tools)

# audit log via engine
eng2 = OllamaToolEngineV5(
    model="mistral", approval_mode="off", verbose=False,
    audit_log_path=TEST_DIR / "v5_eng_audit.jsonl",
)
# Manually dispatch through the pipeline
eng2.pipeline.dispatch("memory", {"operation": "remember", "key": "eng_test", "value": "ok"})
log_str = eng2.get_audit_log(5)
test("v5 engine get_audit_log returns entries", log_str, expect_contains="memory")

ok, _, _ = eng2.verify_audit_integrity()
test("v5 engine verify_audit_integrity passes", expect_true=ok)

activity = eng2.get_activity_summary()
test("v5 engine get_activity_summary returns string", activity, expect_contains="memory")

# set_approval_mode
eng2.set_approval_mode("off")
test("v5 engine set_approval_mode works",
     expect_true=eng2.pipeline.approval_layer.mode == "off")


# ==============================================================================
# Cleanup
# ==============================================================================

shutil.rmtree(TEST_DIR, ignore_errors=True)

total = passed + failed
print(f"\n{'='*60}")
print(f"Results: {passed}/{total} tests passed")
if failed == 0:
    print(f"{GREEN}All tests passed!{RESET}")
else:
    print(f"{RED}{failed} test(s) failed.{RESET}")
    sys.exit(1)
