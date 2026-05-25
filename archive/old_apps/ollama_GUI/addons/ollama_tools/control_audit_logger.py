#!/usr/bin/env python3
"""
control_audit_logger.py  (v5 — NEW FILE)
------------------------------------------
Action Audit Logger.

Logs every tool call, argument set, result, and timestamp.
Designed to be:
  - Append-only (never overwrites or deletes entries)
  - Tamper-resistant (each entry includes a chained SHA-256 hash)
  - Human-readable (JSONL: one JSON object per line)
  - Machine-parseable (structured fields, ISO timestamps)

Log format (one JSON object per line):
{
  "seq":        1,
  "ts":         "2026-04-28T10:00:00.123456",
  "tool":       "execute_system_command",
  "args":       {"command": "ls", "args": ["-l"]},
  "verdict":    "ALLOW",
  "result":     "total 12\\n...",
  "duration_ms": 42,
  "prev_hash":  "0000000000000000",
  "entry_hash": "a3f9c1..."
}

Tamper resistance:
  Each entry's hash covers: seq + ts + tool + args + verdict + result + prev_hash.
  Any modification to a past entry breaks the hash chain.
  This does NOT prevent a determined attacker with filesystem access from
  rewriting the log, but it makes casual tampering immediately detectable.

Integration point:
    ControlPipeline.dispatch() → AuditLogger.log_call() after every execution.
"""

import hashlib
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

MAX_RESULT_LOG_CHARS = 2_000   # truncate long results in the log
MAX_ARGS_LOG_CHARS   = 1_000   # truncate huge arg dumps


class AuditLogger:
    """
    Append-only audit logger with SHA-256 hash chaining.

    Usage:
        al = AuditLogger(log_path=Path("~/.ollama_tools/audit.jsonl"))
        al.log_call(
            tool_name="memory",
            args={"operation": "remember", "key": "x", "value": "y"},
            verdict="ALLOW",
            result="Remembered 'x'.",
            duration_ms=3,
        )
    """

    GENESIS_HASH = "0" * 64   # sentinel for the first entry

    def __init__(self, log_path: Path):
        self.log_path = Path(log_path).expanduser().resolve()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._seq       = self._load_last_seq()
        self._prev_hash = self._load_last_hash()

    # ------------------------------------------------------------------ public

    def log_call(
        self,
        tool_name:   str,
        args:        dict,
        verdict:     str,
        result:      str,
        duration_ms: float = 0.0,
        session_id:  Optional[str] = None,
    ) -> None:
        self._seq += 1
        ts = datetime.now(timezone.utc).isoformat(timespec="microseconds")

        # Sanitise for log (truncate, ensure serialisable)
        safe_args   = self._safe_truncate(args,   MAX_ARGS_LOG_CHARS)
        safe_result = str(result)[:MAX_RESULT_LOG_CHARS]
        if len(str(result)) > MAX_RESULT_LOG_CHARS:
            safe_result += f"  [truncated {len(str(result))} chars]"

        entry = {
            "seq":         self._seq,
            "ts":          ts,
            "tool":        tool_name,
            "args":        safe_args,
            "verdict":     verdict,
            "result":      safe_result,
            "duration_ms": round(duration_ms, 2),
            "session_id":  session_id,
            "prev_hash":   self._prev_hash,
        }

        entry_hash = self._hash_entry(entry)
        entry["entry_hash"] = entry_hash

        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError as e:
            logger.error("[AuditLogger] Failed to write log entry: %s", e)

        self._prev_hash = entry_hash

    def tail(self, n: int = 20) -> list:
        """Return the last n log entries as dicts."""
        entries = []
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        except FileNotFoundError:
            return []
        return entries[-n:]

    def verify_chain(self) -> tuple:
        """
        Verify the hash chain integrity.
        Returns (is_valid: bool, first_broken_seq: int | None, message: str).
        """
        prev = self.GENESIS_HASH
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        return False, None, "Malformed JSON line in log."
                    stored_hash = entry.pop("entry_hash", None)
                    if entry.get("prev_hash") != prev:
                        return False, entry.get("seq"), (
                            f"Hash chain broken at seq={entry.get('seq')}."
                        )
                    computed = self._hash_entry(entry)
                    if computed != stored_hash:
                        return False, entry.get("seq"), (
                            f"Entry hash mismatch at seq={entry.get('seq')}."
                        )
                    prev = stored_hash
        except FileNotFoundError:
            return True, None, "Log file does not exist yet (empty chain)."
        return True, None, "Chain intact."

    def format_tail(self, n: int = 10) -> str:
        """Return last n entries as a human-readable string for GUI display."""
        entries = self.tail(n)
        if not entries:
            return "No audit log entries yet."
        lines = []
        for e in entries:
            ts_short = e.get("ts", "")[:19].replace("T", " ")
            verdict  = e.get("verdict", "?")
            tool     = e.get("tool", "?")
            result   = str(e.get("result", ""))[:80].replace("\n", " ")
            lines.append(f"  [{ts_short}] [{verdict:<18}] {tool:<28} → {result}")
        return "\n".join(lines)

    # ------------------------------------------------------------------ internals

    def _hash_entry(self, entry: dict) -> str:
        """SHA-256 of the canonical JSON representation (sorted keys, no hash field)."""
        payload = json.dumps(
            {k: v for k, v in entry.items() if k != "entry_hash"},
            sort_keys=True, ensure_ascii=False
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _load_last_seq(self) -> int:
        entries = self.tail(1)
        return entries[-1].get("seq", 0) if entries else 0

    def _load_last_hash(self) -> str:
        entries = self.tail(1)
        return entries[-1].get("entry_hash", self.GENESIS_HASH) if entries else self.GENESIS_HASH

    @staticmethod
    def _safe_truncate(obj: Any, max_chars: int) -> Any:
        """Truncate a dict/list/str to fit within max_chars when serialised."""
        try:
            s = json.dumps(obj, ensure_ascii=False)
        except (TypeError, ValueError):
            return str(obj)[:max_chars]
        if len(s) <= max_chars:
            return obj
        return s[:max_chars] + "…"
