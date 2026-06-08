from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import TextIO

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QPlainTextEdit


def append_output(widget: QPlainTextEdit, text: str) -> None:
    """Append text at the document end regardless of the user's cursor or selection."""
    if not text:
        return
    cursor = widget.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    cursor.clearSelection()
    cursor.insertText(text)
    widget.setTextCursor(cursor)
    widget.ensureCursorVisible()


class DiagnosticsSignals(QObject):
    log_line = Signal(str)
    console_text = Signal(str)


class QtLogHandler(logging.Handler):
    def __init__(self, signals: DiagnosticsSignals) -> None:
        super().__init__()
        self.signals = signals
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.signals.log_line.emit(self.format(record) + "\n")
        except Exception:  # noqa: BLE001 - logging handlers must not escape
            self.handleError(record)


class LineBufferedStream:
    def __init__(self, emit, tee: TextIO | None = None) -> None:
        self.emit = emit
        self.tee = tee
        self._buffer = ""

    def write(self, text: str) -> int:
        if not isinstance(text, str):
            text = str(text)
        if self.tee is not None:
            self.tee.write(text)
        self._buffer += text
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            self.emit(line + "\n")
        return len(text)

    def flush(self) -> None:
        if self._buffer:
            self.emit(self._buffer)
            self._buffer = ""
        if self.tee is not None:
            self.tee.flush()

    def isatty(self) -> bool:
        return bool(self.tee and self.tee.isatty())

    @property
    def encoding(self) -> str:
        return getattr(self.tee, "encoding", "utf-8") or "utf-8"


@dataclass(frozen=True)
class OperationUpdate:
    status: str
    history_text: str
    completed: int | None = None
    total: int | None = None


class OperationStreamParser:
    """Assemble streamed JSON fragments and collapse repeated operation statuses."""

    def __init__(self) -> None:
        self._buffer = ""
        self._last_history = ""

    def feed(self, chunk: str) -> list[OperationUpdate]:
        if not chunk:
            return []
        self._buffer += chunk
        updates: list[OperationUpdate] = []
        decoder = json.JSONDecoder()

        while self._buffer:
            candidate = self._buffer.lstrip()
            if not candidate:
                self._buffer = ""
                break
            if not candidate.startswith("{"):
                self._buffer = ""
                update = self._from_payload({"status": candidate.strip()})
                if update:
                    updates.append(update)
                break
            try:
                payload, end = decoder.raw_decode(candidate)
            except json.JSONDecodeError:
                break
            consumed_prefix = len(self._buffer) - len(candidate)
            self._buffer = self._buffer[consumed_prefix + end :]
            update = self._from_payload(payload)
            if update:
                updates.append(update)

        return updates

    def _from_payload(self, payload: dict) -> OperationUpdate | None:
        error = str(payload.get("error") or "").strip()
        status = str(payload.get("status") or error).strip()
        if not status:
            return None
        digest = str(payload.get("digest") or "").strip()
        history = status
        if digest and digest not in status:
            history = f"{status} {digest[:12]}"
        completed = _integer_or_none(payload.get("completed"))
        total = _integer_or_none(payload.get("total"))
        if history == self._last_history:
            history = ""
        else:
            self._last_history = history
        return OperationUpdate(status, history, completed, total)


def _integer_or_none(value) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None
