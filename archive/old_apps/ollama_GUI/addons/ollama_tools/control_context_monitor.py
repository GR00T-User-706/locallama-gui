#!/usr/bin/env python3
"""
control_context_monitor.py  (v5 — NEW FILE)
---------------------------------------------
State & Context Monitor.

Tracks what the LLM has done recently and provides a short-term
"working memory" of actions within the current session.

Responsibilities:
  - Record every tool call and its outcome
  - Detect redundant operations (calling the same thing twice in a row
    when the first already succeeded)
  - Detect contradictory operations (e.g. write then immediately delete
    the same file, or remember then immediately forget the same key)
  - Provide a formatted context summary the LLM or GUI can read
  - Expose a "what did I just do?" summary for injection into the system prompt

This module does NOT block calls — it only observes and flags.
Blocking decisions are made by the Gatekeeper and Governor.
The ControlPipeline reads monitor.warnings after each call and can
include them in the next system prompt.

Integration point:
    ControlPipeline.dispatch()
      → after execution: monitor.record(...)
      → before next LLM call: monitor.context_summary() injected into system prompt
"""

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional, Tuple


MAX_HISTORY = 50   # entries kept in working memory


@dataclass
class ActionRecord:
    seq:        int
    timestamp:  float
    tool_name:  str
    operation:  Optional[str]   # extracted from args if present
    args_key:   str             # short fingerprint of args for dedup
    result:     str
    verdict:    str             # ALLOW / DENY / REQUIRE_APPROVAL / APPROVED / DENIED
    warnings:   List[str] = field(default_factory=list)


# Pairs of (tool, operation) that are contradictory when applied to the same target.
# Format: ((tool_a, op_a), (tool_b, op_b))
CONTRADICTORY_PAIRS: List[Tuple] = [
    (("memory",           "remember"), ("memory",           "forget")),
    (("sandbox_file",     "write"),    ("sandbox_file",     "delete")),
    (("workspace_manager","write"),    ("workspace_manager","delete")),
    (("book_writer",      "write_section"), ("book_writer", "revise_section")),  # not truly contradictory but worth noting
]


class ContextMonitor:
    """
    Short-term working memory of tool actions in the current session.

    Usage:
        cm = ContextMonitor()
        cm.record("memory", {"operation": "remember", "key": "x"}, "Remembered.", "ALLOW")
        print(cm.context_summary())
        print(cm.warnings)   # list of warning strings from the last record() call
    """

    def __init__(self, max_history: int = MAX_HISTORY):
        self.max_history = max_history
        self._history: Deque[ActionRecord] = deque(maxlen=max_history)
        self._seq       = 0
        self.warnings:  List[str] = []   # populated by the most recent record() call

    # ------------------------------------------------------------------ public

    def record(
        self,
        tool_name: str,
        args:      dict,
        result:    str,
        verdict:   str,
    ) -> List[str]:
        """
        Record a completed tool call.
        Returns a list of warning strings (may be empty).
        """
        self._seq += 1
        operation = self._extract_operation(args)
        args_key  = self._args_key(tool_name, args)

        warnings: List[str] = []

        # 1. Redundancy check — same call already succeeded recently
        if verdict in ("ALLOW", "APPROVED"):
            for prev in reversed(self._history):
                if (prev.tool_name == tool_name and
                        prev.args_key == args_key and
                        prev.verdict in ("ALLOW", "APPROVED") and
                        not prev.result.startswith("Error:")):
                    age = time.monotonic() - prev.timestamp
                    warnings.append(
                        f"Redundant call: '{tool_name}' with the same arguments "
                        f"already succeeded {age:.1f}s ago (seq={prev.seq}). "
                        "Result may be identical."
                    )
                    break

        # 2. Contradiction check
        if verdict in ("ALLOW", "APPROVED"):
            for (t_a, op_a), (t_b, op_b) in CONTRADICTORY_PAIRS:
                if tool_name == t_b and operation == op_b:
                    # Look for a recent matching t_a / op_a
                    for prev in reversed(self._history):
                        if prev.tool_name == t_a and prev.operation == op_a:
                            age = time.monotonic() - prev.timestamp
                            warnings.append(
                                f"Contradictory sequence: '{t_a}.{op_a}' was called "
                                f"{age:.1f}s ago, now '{t_b}.{op_b}' is being called. "
                                "Verify this is intentional."
                            )
                            break

        record = ActionRecord(
            seq=self._seq,
            timestamp=time.monotonic(),
            tool_name=tool_name,
            operation=operation,
            args_key=args_key,
            result=str(result)[:200],
            verdict=verdict,
            warnings=warnings,
        )
        self._history.append(record)
        self.warnings = warnings
        return warnings

    def context_summary(self, n: int = 10) -> str:
        """
        Return a concise summary of the last n actions.
        Suitable for injection into the LLM system prompt.
        """
        recent = list(self._history)[-n:]
        if not recent:
            return ""
        lines = ["[Recent Actions (this session)]"]
        for r in recent:
            age    = time.monotonic() - r.timestamp
            status = "✓" if r.verdict in ("ALLOW", "APPROVED") else "✗"
            op_str = f".{r.operation}" if r.operation else ""
            result_short = r.result[:60].replace("\n", " ")
            lines.append(
                f"  {status} {r.tool_name}{op_str:<32} "
                f"{age:>6.1f}s ago → {result_short}"
            )
            for w in r.warnings:
                lines.append(f"    ⚠ {w}")
        return "\n".join(lines)

    def get_warnings_for_prompt(self) -> str:
        """
        Return all pending warnings as a string to prepend to the next LLM prompt.
        Clears the warning list after reading.
        """
        if not self.warnings:
            return ""
        text = "[Control Layer Warnings]\n" + "\n".join(f"  ⚠ {w}" for w in self.warnings)
        self.warnings = []
        return text

    def reset(self) -> None:
        """Clear working memory (e.g. at start of a new conversation)."""
        self._history.clear()
        self._seq    = 0
        self.warnings = []

    def last_n(self, n: int = 5) -> List[ActionRecord]:
        return list(self._history)[-n:]

    # ------------------------------------------------------------------ internals

    @staticmethod
    def _extract_operation(args: dict) -> Optional[str]:
        return args.get("operation") or args.get("command") or None

    @staticmethod
    def _args_key(tool_name: str, args: dict) -> str:
        """Short fingerprint for dedup — not cryptographic."""
        try:
            import json, hashlib
            payload = tool_name + json.dumps(args, sort_keys=True, ensure_ascii=False)
            return hashlib.md5(payload.encode()).hexdigest()[:12]  # noqa: S324
        except Exception:
            return str(args)[:32]
