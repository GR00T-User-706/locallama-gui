#!/usr/bin/env python3
"""
control_behavior_governor.py  (v5 — NEW FILE)
-----------------------------------------------
Rate Limiter / Behavior Governor.

Detects and prevents:
  - Rapid repeated identical calls (command spam)
  - Runaway tool usage loops (same tool called N times in a row)
  - Escalation chains (sequence of tools that together form a dangerous pattern)
  - Global call rate exceeding a burst threshold

This is SEPARATE from the orchestrator's per-window rate limiter.
The governor focuses on BEHAVIORAL patterns, not just raw counts.

Decisions:
  - Returns GovernorDecision: ALLOW | THROTTLE | BLOCK
  - THROTTLE: call is allowed but a warning is emitted
  - BLOCK: call is denied with an explanation

Integration point:
    ControlPipeline.dispatch() → Governor.evaluate() → (proceed or block)
"""

import hashlib
import json
import time
import logging
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Any, Deque, Dict, Optional, Tuple

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Known escalation chain patterns
# Each pattern is a sequence of (tool, operation) tuples.
# If the recent call history matches a pattern, it is flagged.
# ------------------------------------------------------------------

# Format: list of (tool_name, operation_keyword_or_None)
# None means "any operation for this tool"
ESCALATION_PATTERNS = [
    # Read memory → write file → execute command (classic exfil chain)
    [("memory", "recall"), ("sandbox_file", "write"), ("execute_system_command", None)],
    # Inspect tools → disable gatekeeper → execute command
    [("system_inspect", None), ("execute_system_command", None), ("execute_system_command", None)],
    # Rapid workspace write + execute
    [("workspace_manager", "write"), ("workspace_manager", "write"), ("execute_system_command", None)],
]

# How many recent calls to keep for pattern matching
HISTORY_WINDOW = 10


class GovernorDecision(str, Enum):
    ALLOW    = "ALLOW"
    THROTTLE = "THROTTLE"
    BLOCK    = "BLOCK"


@dataclass
class BehaviorVerdict:
    decision:  GovernorDecision
    reason:    str
    tool_name: str


class BehaviorGovernor:
    """
    Monitors call patterns and blocks or throttles suspicious behavior.

    Usage:
        gov = BehaviorGovernor()
        verdict = gov.evaluate("execute_system_command", {"command": "ls", "args": []})
        if verdict.decision == GovernorDecision.BLOCK:
            return f"Blocked: {verdict.reason}"
    """

    def __init__(
        self,
        max_identical_in_window: int   = 3,    # same exact call N times → block
        identical_window_sec:    float = 15.0,
        max_same_tool_streak:    int   = 5,    # same tool N times in a row → throttle
        global_burst_limit:      int   = 15,   # total calls in burst_window_sec → block
        burst_window_sec:        float = 10.0,
    ):
        self.max_identical_in_window = max_identical_in_window
        self.identical_window_sec    = identical_window_sec
        self.max_same_tool_streak    = max_same_tool_streak
        self.global_burst_limit      = global_burst_limit
        self.burst_window_sec        = burst_window_sec

        # { call_fingerprint: [timestamps] }
        self._identical_ts: Dict[str, list] = {}
        # Recent call history: deque of (tool_name, operation, timestamp)
        self._history: Deque[Tuple[str, Optional[str], float]] = deque(maxlen=HISTORY_WINDOW)
        # Global burst timestamps
        self._burst_ts: list = []

    # ------------------------------------------------------------------ public

    def evaluate(self, tool_name: str, args: dict) -> BehaviorVerdict:
        now = time.monotonic()

        # 1. Global burst check
        self._burst_ts = [t for t in self._burst_ts if now - t < self.burst_window_sec]
        if len(self._burst_ts) >= self.global_burst_limit:
            return BehaviorVerdict(
                GovernorDecision.BLOCK,
                f"Global burst limit: {self.global_burst_limit} calls in "
                f"{self.burst_window_sec:.0f}s. Possible runaway loop.",
                tool_name,
            )
        self._burst_ts.append(now)

        # 2. Identical call spam check
        fingerprint = self._fingerprint(tool_name, args)
        ts_list = self._identical_ts.setdefault(fingerprint, [])
        ts_list[:] = [t for t in ts_list if now - t < self.identical_window_sec]
        if len(ts_list) >= self.max_identical_in_window:
            return BehaviorVerdict(
                GovernorDecision.BLOCK,
                f"Identical call to '{tool_name}' repeated "
                f"{len(ts_list)+1} times in {self.identical_window_sec:.0f}s. "
                "Possible loop.",
                tool_name,
            )
        ts_list.append(now)

        # 3. Same-tool streak check
        operation = args.get("operation") or args.get("command") or None
        streak = self._streak(tool_name)
        if streak >= self.max_same_tool_streak:
            return BehaviorVerdict(
                GovernorDecision.THROTTLE,
                f"Tool '{tool_name}' called {streak} times in a row. "
                "Consider varying your approach.",
                tool_name,
            )

        # 4. Escalation chain check
        self._history.append((tool_name, operation, now))
        chain_match = self._check_escalation()
        if chain_match:
            return BehaviorVerdict(
                GovernorDecision.BLOCK,
                f"Escalation chain detected: {chain_match}",
                tool_name,
            )

        return BehaviorVerdict(GovernorDecision.ALLOW, "OK", tool_name)

    def reset(self) -> None:
        """Clear all state (e.g. at start of a new conversation)."""
        self._identical_ts.clear()
        self._history.clear()
        self._burst_ts.clear()

    def recent_summary(self) -> str:
        """Return a human-readable summary of recent tool calls."""
        if not self._history:
            return "No recent tool calls."
        lines = ["Recent tool calls (newest last):"]
        for tool, op, ts in self._history:
            age = time.monotonic() - ts
            lines.append(f"  {tool:<28} op={op or '—':<20} {age:.1f}s ago")
        return "\n".join(lines)

    # ------------------------------------------------------------------ internals

    @staticmethod
    def _fingerprint(tool_name: str, args: dict) -> str:
        try:
            payload = tool_name + json.dumps(args, sort_keys=True, ensure_ascii=False)
        except (TypeError, ValueError):
            payload = tool_name + str(args)
        return hashlib.md5(payload.encode("utf-8")).hexdigest()  # noqa: S324 — not crypto

    def _streak(self, tool_name: str) -> int:
        """Count how many of the most recent calls are the same tool."""
        count = 0
        for t, _, _ in reversed(self._history):
            if t == tool_name:
                count += 1
            else:
                break
        return count

    def _check_escalation(self) -> Optional[str]:
        """Check if the recent history matches any known escalation pattern."""
        history_list = list(self._history)  # oldest → newest
        for pattern in ESCALATION_PATTERNS:
            if len(history_list) < len(pattern):
                continue
            tail = history_list[-len(pattern):]
            match = True
            for (p_tool, p_op), (h_tool, h_op, _) in zip(pattern, tail):
                if p_tool != h_tool:
                    match = False; break
                if p_op is not None and p_op not in (h_op or ""):
                    match = False; break
            if match:
                desc = " → ".join(f"{t}:{o or '*'}" for t, o in pattern)
                return desc
        return None
