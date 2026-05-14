#!/usr/bin/env python3
"""
test_tools_v4.py  (v4 — NEW FILE)
-----------------------------------
Full test suite for all v4 additions.
Does NOT require Ollama to be running.

Coverage:
  tool_book_writer      — all 7 operations
  tool_app_adapter      — calculator, notes, system_info, unknown rejection
  tool_context_builder  — all 3 operations
  tool_system_inspect   — all 5 operations
  tool_workspace_manager— all 5 operations
  tool_orchestrator     — routing, rate limiting, permission checks, toggle
  ollama_tools_v4       — engine wiring, orchestrator injection
"""

import sys, os, types, tempfile, shutil, time
from pathlib import Path

# Stub ollama so we can import without it installed
sys.modules.setdefault("ollama", types.ModuleType("ollama"))

TEST_DIR = Path(tempfile.mkdtemp(prefix="ollama_v4_test_"))

# ---- import all modules ----
from tool_book_writer       import BookWriterStore,        dispatch_book_writer_tool
from tool_app_adapter       import AppAdapterStore,        dispatch_app_adapter_tool
from tool_context_builder   import ContextBuilderStore,    dispatch_context_builder_tool
from tool_system_inspect    import SystemInspectStore,     dispatch_system_inspect_tool
from tool_workspace_manager import WorkspaceManagerStore,  dispatch_workspace_manager_tool
from tool_orchestrator      import ToolOrchestrator,       _RateLimiter
from tool_memory            import MemoryStore
from tool_sandbox_files     import SandboxedFileStore

# ---- test helpers ----
GREEN = "\033[92m"; RED = "\033[91m"; RESET = "\033[0m"
passed = 0; failed = 0

def test(name, result, expect_error=False, expect_contains=None, expect_not_contains=None, expect_true=None):
    global passed, failed
    r  = str(result)
    ok = True; reason = ""
    if expect_true is not None:
        if not expect_true:
            ok = False; reason = f"Expected True condition, got False. result={r!r}"
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


# ==============================================================================
section("TOOL: book_writer")
# ==============================================================================

bw = BookWriterStore(sandbox=TEST_DIR / "books")

r = dispatch_book_writer_tool({"operation": "list_projects"}, bw)
test("list_projects on empty store", r, expect_contains="No book projects")

r = dispatch_book_writer_tool({"operation": "create_project", "project": "my_novel", "title": "My Novel"}, bw)
test("create_project succeeds", r, expect_contains="Created")

r = dispatch_book_writer_tool({"operation": "create_project", "project": "my_novel"}, bw)
test("create_project duplicate rejected", r, expect_error=True)

r = dispatch_book_writer_tool({"operation": "list_projects"}, bw)
test("list_projects shows project", r, expect_contains="my_novel")

r = dispatch_book_writer_tool({"operation": "update_outline", "project": "my_novel",
                                "chapters": ["Chapter 1: The Beginning", "Chapter 2: The Middle"]}, bw)
test("update_outline succeeds", r, expect_contains="Outline updated")

r = dispatch_book_writer_tool({"operation": "write_section", "project": "my_novel",
                                "section": "chapter_1", "content": "It was a dark and stormy night."}, bw)
test("write_section succeeds", r, expect_contains="Wrote section")

r = dispatch_book_writer_tool({"operation": "summarize_section", "project": "my_novel",
                                "section": "chapter_1"}, bw)
test("summarize_section returns content", r, expect_contains="dark and stormy")

r = dispatch_book_writer_tool({"operation": "revise_section", "project": "my_novel",
                                "section": "chapter_1", "revision_note": "Add more tension."}, bw)
test("revise_section appends note", r, expect_contains="Revision appended")

r = dispatch_book_writer_tool({"operation": "summarize_section", "project": "my_novel",
                                "section": "chapter_1"}, bw)
test("summarize after revision contains revision note", r, expect_contains="Add more tension")

r = dispatch_book_writer_tool({"operation": "track_character", "project": "my_novel",
                                "name": "Alice", "attributes": {"role": "protagonist", "age": 30}}, bw)
test("track_character succeeds", r, expect_contains="tracked")

r = dispatch_book_writer_tool({"operation": "write_section", "project": "my_novel",
                                "section": "../escape", "content": "bad"}, bw)
test("path traversal in section name rejected", r, expect_error=True)

r = dispatch_book_writer_tool({"operation": "write_section", "project": "my_novel",
                                "section": "ch1", "content": "x" * (64 * 1024 + 1)}, bw)
test("oversized section content rejected", r, expect_error=True)

r = dispatch_book_writer_tool({"operation": "create_project", "project": "../escape"}, bw)
test("path traversal in project name rejected", r, expect_error=True)


# ==============================================================================
section("TOOL: app_adapter")
# ==============================================================================

aa = AppAdapterStore(sandbox=TEST_DIR / "app_sandbox")

r = dispatch_app_adapter_tool({"operation": "list_apps"}, aa)
test("list_apps returns available apps", r, expect_contains="calculator")

r = dispatch_app_adapter_tool({"operation": "call", "app": "calculator",
                                "action": "evaluate", "params": {"expression": "2 + 2"}}, aa)
test("calculator evaluate 2+2", r, expect_contains="4")

r = dispatch_app_adapter_tool({"operation": "call", "app": "calculator",
                                "action": "evaluate", "params": {"expression": "10 / 2"}}, aa)
test("calculator evaluate 10/2", r, expect_contains="5")

r = dispatch_app_adapter_tool({"operation": "call", "app": "calculator",
                                "action": "evaluate", "params": {"expression": "1/0"}}, aa)
test("calculator division by zero handled", r, expect_error=True)

r = dispatch_app_adapter_tool({"operation": "call", "app": "calculator",
                                "action": "evaluate", "params": {"expression": "__import__('os').system('id')"}}, aa)
test("calculator injection attempt blocked", r, expect_error=True)

r = dispatch_app_adapter_tool({"operation": "call", "app": "notes",
                                "action": "add", "params": {"note_name": "shopping", "content": "milk, eggs, bread"}}, aa)
test("notes add succeeds", r, expect_contains="saved")

r = dispatch_app_adapter_tool({"operation": "call", "app": "notes",
                                "action": "list", "params": {}}, aa)
test("notes list shows note", r, expect_contains="shopping")

r = dispatch_app_adapter_tool({"operation": "call", "app": "notes",
                                "action": "read", "params": {"note_name": "shopping"}}, aa)
test("notes read returns content", r, expect_contains="milk")

r = dispatch_app_adapter_tool({"operation": "call", "app": "notes",
                                "action": "read", "params": {"note_name": "../../../etc/passwd"}}, aa)
test("notes path traversal blocked", r, expect_error=True)

r = dispatch_app_adapter_tool({"operation": "call", "app": "system_info",
                                "action": "uptime", "params": {}}, aa)
test("system_info uptime returns result", r)

r = dispatch_app_adapter_tool({"operation": "call", "app": "unknown_app",
                                "action": "do_something", "params": {}}, aa)
test("unknown app rejected", r, expect_error=True)

r = dispatch_app_adapter_tool({"operation": "call", "app": "calculator",
                                "action": "unknown_action", "params": {}}, aa)
test("unknown action rejected", r, expect_error=True)


# ==============================================================================
section("TOOL: context_builder")
# ==============================================================================

mem_cb   = MemoryStore(path=TEST_DIR / "mem_cb.json", namespace="t")
sbox_cb  = SandboxedFileStore(sandbox_dir=TEST_DIR / "sbox_cb")
cb       = ContextBuilderStore(mem_cb, sbox_cb)

r = dispatch_context_builder_tool({"operation": "fetch_memory_context"}, cb)
test("fetch_memory_context on empty memory", r, expect_contains="empty")

mem_cb.remember("user_name", "Bob")
r = dispatch_context_builder_tool({"operation": "fetch_memory_context"}, cb)
test("fetch_memory_context returns stored key", r, expect_contains="Bob")

sbox_cb.write_file("ctx_test.txt", "Hello from sandbox")
r = dispatch_context_builder_tool({"operation": "fetch_file_context",
                                    "filename": "ctx_test.txt"}, cb)
test("fetch_file_context returns file content", r, expect_contains="Hello from sandbox")

r = dispatch_context_builder_tool({"operation": "fetch_file_context",
                                    "filename": "nonexistent.txt"}, cb)
test("fetch_file_context on missing file returns error", r, expect_error=True)

r = dispatch_context_builder_tool({"operation": "summarize_context"}, cb)
test("summarize_context returns combined snapshot", r, expect_contains="Bob")

r = dispatch_context_builder_tool({"operation": "summarize_context",
                                    "max_chars": 50}, cb)
test("summarize_context respects max_chars", r, expect_true=len(r) <= 200)  # trimmed + label


# ==============================================================================
section("TOOL: workspace_manager")
# ==============================================================================

wm = WorkspaceManagerStore(sandbox=TEST_DIR / "wm_sandbox")

r = dispatch_workspace_manager_tool({"operation": "list_projects"}, wm)
test("list_projects on empty store", r, expect_contains="No workspace")

r = dispatch_workspace_manager_tool({"operation": "create_project", "project": "proj_alpha",
                                      "description": "Test project"}, wm)
test("create_project succeeds", r, expect_contains="Created")

r = dispatch_workspace_manager_tool({"operation": "create_project", "project": "proj_alpha"}, wm)
test("create_project duplicate rejected", r, expect_error=True)

r = dispatch_workspace_manager_tool({"operation": "list_projects"}, wm)
test("list_projects shows project", r, expect_contains="proj_alpha")

r = dispatch_workspace_manager_tool({"operation": "write_project_file", "project": "proj_alpha",
                                      "filename": "README.md", "content": "# Alpha Project"}, wm)
test("write_project_file succeeds", r, expect_contains="Wrote")

r = dispatch_workspace_manager_tool({"operation": "read_project_file", "project": "proj_alpha",
                                      "filename": "README.md"}, wm)
test("read_project_file returns content", r, expect_contains="Alpha Project")

r = dispatch_workspace_manager_tool({"operation": "snapshot_project", "project": "proj_alpha"}, wm)
test("snapshot_project lists files", r, expect_contains="README.md")

r = dispatch_workspace_manager_tool({"operation": "write_project_file", "project": "proj_alpha",
                                      "filename": "script.sh", "content": "#!/bin/bash"}, wm)
test("blocked extension rejected", r, expect_error=True)

r = dispatch_workspace_manager_tool({"operation": "write_project_file", "project": "proj_alpha",
                                      "filename": "../escape.txt", "content": "bad"}, wm)
test("path traversal in filename rejected", r, expect_error=True)

r = dispatch_workspace_manager_tool({"operation": "write_project_file", "project": "proj_alpha",
                                      "filename": "big.txt", "content": "x" * (128 * 1024 + 1)}, wm)
test("oversized file content rejected", r, expect_error=True)

r = dispatch_workspace_manager_tool({"operation": "read_project_file", "project": "proj_alpha",
                                      "filename": "missing.txt"}, wm)
test("read missing file returns error", r, expect_error=True)


# ==============================================================================
section("TOOL: system_inspect (via orchestrator)")
# ==============================================================================

orch_si = ToolOrchestrator(
    sandbox_dir=TEST_DIR / "si_sandbox",
    memory_path=TEST_DIR / "si_mem.json",
    session_mode="full",
)
si = orch_si.inspect_store

r = dispatch_system_inspect_tool({"operation": "list_available_tools"}, si)
test("list_available_tools returns all tools", r, expect_contains="book_writer")
test("list_available_tools includes v3 tools", r, expect_contains="memory")

r = dispatch_system_inspect_tool({"operation": "show_enabled_tools"}, si)
test("show_enabled_tools returns enabled tools", r, expect_contains="Enabled tools")

r = dispatch_system_inspect_tool({"operation": "show_permissions"}, si)
test("show_permissions returns session mode", r, expect_contains="full")
test("show_permissions includes rate limit info", r, expect_contains="Rate limit")

r = dispatch_system_inspect_tool({"operation": "list_sandbox_files"}, si)
test("list_sandbox_files returns sandbox listing", r)

r = dispatch_system_inspect_tool({"operation": "list_memory_keys"}, si)
test("list_memory_keys returns memory listing", r)

r = dispatch_system_inspect_tool({"operation": "unknown_op"}, si)
test("unknown system_inspect operation rejected", r, expect_error=True)


# ==============================================================================
section("ORCHESTRATOR: routing, rate limiting, permissions")
# ==============================================================================

orch = ToolOrchestrator(
    sandbox_dir=TEST_DIR / "orch_sandbox",
    memory_path=TEST_DIR / "orch_mem.json",
    session_mode="full",
)

# Basic routing
r = orch.dispatch("memory", {"operation": "remember", "key": "test_key", "value": "test_val"})
test("orchestrator routes memory tool", r, expect_contains="Remembered")

r = orch.dispatch("memory", {"operation": "recall", "key": "test_key"})
test("orchestrator routes memory recall", r, expect_contains="test_val")

r = orch.dispatch("execute_system_command", {"command": "date", "args": []})
test("orchestrator routes system command", r)

# Unknown tool
r = orch.dispatch("nonexistent_tool", {})
test("unknown tool rejected by orchestrator", r, expect_error=True)

# Non-dict args
r = orch.dispatch("memory", "not a dict")
test("non-dict args rejected by orchestrator", r, expect_error=True)

# Permission check — restricted mode disables system commands
orch.set_session_mode("restricted")
r = orch.dispatch("execute_system_command", {"command": "date", "args": []})
test("restricted mode blocks system commands", r, expect_error=True)

r = orch.dispatch("memory", {"operation": "recall"})
test("restricted mode allows memory", r)

orch.set_session_mode("full")
r = orch.dispatch("execute_system_command", {"command": "date", "args": []})
test("full mode re-enables system commands", r)

# Toggle tool
orch.toggle_tool("book_writer", False)
r = orch.dispatch("book_writer", {"operation": "list_projects"})
test("toggled-off tool is blocked", r, expect_error=True)

orch.toggle_tool("book_writer", True)
r = orch.dispatch("book_writer", {"operation": "list_projects"})
test("re-enabled tool works again", r)

# active_schemas returns only enabled tools
orch.toggle_tool("workspace_manager", False)
schemas = orch.active_schemas()
names   = [s["function"]["name"] for s in schemas]
test("active_schemas excludes disabled tools", "workspace_manager" not in names)
test("active_schemas includes enabled tools", "memory" in names)
orch.toggle_tool("workspace_manager", True)

# Rate limiter unit test
rl = _RateLimiter(max_calls=3, window_seconds=5)
ok1, _ = rl.check()
ok2, _ = rl.check()
ok3, _ = rl.check()
ok4, msg = rl.check()
test("rate limiter allows calls up to max", ok1 and ok2 and ok3)
test("rate limiter blocks at max+1", not ok4)
test("rate limiter error message is informative", msg, expect_contains="Rate limit")

time.sleep(5.1)
ok5, _ = rl.check()
test("rate limiter resets after window expires", ok5)


# ==============================================================================
section("ENGINE v4: orchestrator injection")
# ==============================================================================

import types as _types, sys as _sys
_ollama_stub = _sys.modules["ollama"]
_ollama_stub.ResponseError = Exception

from ollama_tools_v4 import OllamaToolEngine as EngineV4

# Engine with auto-created orchestrator
eng = EngineV4(model="mistral", session_mode="full", verbose=False)
test("engine creates orchestrator automatically", eng.orchestrator is not None)
test("engine.get_tool_info() returns 8 tools", len(eng.get_tool_info()) == 8)

# Engine with injected orchestrator
orch_inj = ToolOrchestrator(
    sandbox_dir=TEST_DIR / "inj_sandbox",
    memory_path=TEST_DIR / "inj_mem.json",
    session_mode="restricted",
)
eng_inj = EngineV4(model="mistral", orchestrator=orch_inj, verbose=False)
test("injected orchestrator is used", eng_inj.orchestrator is orch_inj)
test("injected orchestrator session mode respected",
     eng_inj.session_mode == "restricted")

# toggle_tool delegates to orchestrator
eng.toggle_tool("book_writer", False)
test("toggle_tool delegates to orchestrator",
     not eng.orchestrator._registry["book_writer"]["enabled"])
eng.toggle_tool("book_writer", True)

# set_session_mode delegates to orchestrator
eng.set_session_mode("read-only")
test("set_session_mode delegates to orchestrator",
     eng.orchestrator.session_mode == "read-only")
eng.set_session_mode("full")


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
