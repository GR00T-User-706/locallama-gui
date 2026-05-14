#!/usr/bin/env python3
"""
control_gatekeeper.py  (v5 — NEW FILE)
----------------------------------------
Tool Execution Gatekeeper.

Intercepts every tool call BEFORE it reaches the orchestrator.
Can DENY, MODIFY, or APPROVE execution based on configurable rules.

Responsibilities:
  - Validate tool name against a known registry
  - Validate argument structure (no null bytes, no path traversal patterns)
  - Enforce per-tool call frequency limits (distinct from rate limiter)
  - Apply per-tool sensitivity classification (LOW / MEDIUM / HIGH)
  - Return a GatekeeperVerdict: ALLOW | DENY | REQUIRE_APPROVAL

This module has NO knowledge of tool internals.
It only inspects tool_name and args at the surface level.

Integration point:
    ControlPipeline.dispatch() → Gatekeeper.evaluate() → (proceed or block)
"""

import re
import time
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Sensitivity classification
# ------------------------------------------------------------------

class Sensitivity(str, Enum):
    LOW    = "LOW"
    MEDIUM = "MEDIUM"
    HIGH   = "HIGH"

# Default sensitivity per tool name.
# HIGH = requires approval by default when approval layer is active.
TOOL_SENSITIVITY: Dict[str, Sensitivity] = {
    "execute_system_command": Sensitivity.HIGH,
    "sandbox_file":           Sensitivity.MEDIUM,
    "memory":                 Sensitivity.LOW,
    "book_writer":            Sensitivity.LOW,
    "app_adapter":            Sensitivity.MEDIUM,
    "context_builder":        Sensitivity.LOW,
    "system_inspect":         Sensitivity.LOW,
    "workspace_manager":      Sensitivity.MEDIUM,
}

# Per-tool max calls within a sliding window (seconds, count).
# Separate from the orchestrator's global rate limiter.
TOOL_FREQUENCY_LIMITS: Dict[str, Tuple[int, int]] = {
    # tool_name: (window_seconds, max_calls)
    "execute_system_command": (10, 4),
    "sandbox_file":           (10, 8),
    "memory":                 (10, 12),
    "book_writer":            (30, 6),
    "app_adapter":            (10, 6),
    "context_builder":        (10, 8),
    "system_inspect":         (10, 8),
    "workspace_manager":      (10, 6),
}

# Patterns that are always suspicious in any argument value.
_SUSPICIOUS_PATTERNS: List[re.Pattern] = [
    re.compile(r'\x00'),                    # null byte
    re.compile(r'\.\.[\\/]'),               # path traversal
    re.compile(r'[\r\n].*(?:rm|del|format)', re.IGNORECASE),  # newline + destructive
    re.compile(r';\s*(?:rm|del|mkfs|dd\s)', re.IGNORECASE),   # command chaining
    re.compile(r'\|\s*(?:bash|sh|zsh|fish)', re.IGNORECASE),  # pipe to shell
    re.compile(r'`[^`]+`'),                 # backtick execution
    re.compile(r'\$\([^)]+\)'),             # subshell $()
]


# ------------------------------------------------------------------
# Verdict
# ------------------------------------------------------------------

class Verdict(str, Enum):
    ALLOW            = "ALLOW"
    DENY             = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"

@dataclass
class GatekeeperVerdict:
    verdict:    Verdict
    reason:     str
    tool_name:  str
    args:       dict
    sensitivity: Sensitivity = Sensitivity.LOW


# ------------------------------------------------------------------
# Gatekeeper
# ------------------------------------------------------------------

class ToolGatekeeper:
    """
    Evaluates every tool call and returns a GatekeeperVerdict.

    Usage:
        gk = ToolGatekeeper(known_tools=set(orchestrator._registry.keys()))
        verdict = gk.evaluate("execute_system_command", {"command": "ls", "args": ["-l"]})
        if verdict.verdict == Verdict.DENY:
            return f"Blocked: {verdict.reason}"
    """

    def __init__(
        self,
        known_tools:          set,
        require_approval_for: Optional[set] = None,   # override: always require approval
        blocked_tools:        Optional[set] = None,   # hard-blocked tools
    ):
        self.known_tools          = known_tools
        self.require_approval_for = require_approval_for or set()
        self.blocked_tools        = blocked_tools or set()
        self._call_timestamps: Dict[str, List[float]] = {}

    # ------------------------------------------------------------------ public

    def evaluate(self, tool_name: str, args: dict) -> GatekeeperVerdict:
        sensitivity = TOOL_SENSITIVITY.get(tool_name, Sensitivity.MEDIUM)

        # 1. Hard block
        if tool_name in self.blocked_tools:
            return GatekeeperVerdict(
                Verdict.DENY, f"Tool '{tool_name}' is permanently blocked.",
                tool_name, args, sensitivity
            )

        # 2. Unknown tool
        if tool_name not in self.known_tools:
            return GatekeeperVerdict(
                Verdict.DENY, f"Unknown tool '{tool_name}'.",
                tool_name, args, sensitivity
            )

        # 3. Argument surface scan
        suspicious = self._scan_args(args)
        if suspicious:
            logger.warning("[Gatekeeper] Suspicious pattern in '%s' args: %s", tool_name, suspicious)
            return GatekeeperVerdict(
                Verdict.DENY,
                f"Suspicious pattern detected in arguments: {suspicious}",
                tool_name, args, sensitivity
            )

        # 4. Per-tool frequency check
        freq_ok, freq_msg = self._check_frequency(tool_name)
        if not freq_ok:
            return GatekeeperVerdict(
                Verdict.DENY, freq_msg, tool_name, args, sensitivity
            )

        # 5. Approval required?
        if tool_name in self.require_approval_for or sensitivity == Sensitivity.HIGH:
            return GatekeeperVerdict(
                Verdict.REQUIRE_APPROVAL,
                f"Tool '{tool_name}' (sensitivity={sensitivity.value}) requires user approval.",
                tool_name, args, sensitivity
            )

        return GatekeeperVerdict(
            Verdict.ALLOW, "OK", tool_name, args, sensitivity
        )

    def block_tool(self, tool_name: str) -> None:
        self.blocked_tools.add(tool_name)

    def unblock_tool(self, tool_name: str) -> None:
        self.blocked_tools.discard(tool_name)

    def set_approval_required(self, tool_name: str, required: bool) -> None:
        if required:
            self.require_approval_for.add(tool_name)
        else:
            self.require_approval_for.discard(tool_name)

    # ------------------------------------------------------------------ internals

    def _scan_args(self, args: Any, depth: int = 0) -> Optional[str]:
        """Recursively scan arg values for suspicious patterns."""
        if depth > 5:
            return None
        if isinstance(args, str):
            for pat in _SUSPICIOUS_PATTERNS:
                if pat.search(args):
                    return f"matched /{pat.pattern}/ in value {args[:60]!r}"
        elif isinstance(args, dict):
            for v in args.values():
                result = self._scan_args(v, depth + 1)
                if result:
                    return result
        elif isinstance(args, (list, tuple)):
            for item in args:
                result = self._scan_args(item, depth + 1)
                if result:
                    return result
        return None

    def _check_frequency(self, tool_name: str) -> Tuple[bool, str]:
        if tool_name not in TOOL_FREQUENCY_LIMITS:
            return True, ""
        window, max_calls = TOOL_FREQUENCY_LIMITS[tool_name]
        now = time.monotonic()
        ts  = self._call_timestamps.setdefault(tool_name, [])
        # Prune expired
        self._call_timestamps[tool_name] = [t for t in ts if now - t < window]
        ts = self._call_timestamps[tool_name]
        if len(ts) >= max_calls:
            return False, (
                f"Tool '{tool_name}' called {len(ts)} times in {window}s "
                f"(limit {max_calls}). Slow down."
            )
        self._call_timestamps[tool_name].append(now)
        return True, ""
