"""
Application-wide logging setup.
Logs to both file and in-memory buffer for the log panel.
"""

import logging
import logging.handlers
from pathlib import Path
from collections import deque
from typing import List, Callable


class InMemoryHandler(logging.Handler):
    """Stores recent log records in memory for the log panel."""

    def __init__(self, capacity: int = 2000):
        super().__init__()
        self._records: deque = deque(maxlen=capacity)
        self._listeners: List[Callable] = []

    def emit(self, record: logging.LogRecord):
        self._records.append(record)
        for listener in self._listeners:
            try:
                listener(record)
            except Exception:
                pass

    def get_records(self) -> List[logging.LogRecord]:
        return list(self._records)

    def add_listener(self, fn: Callable):
        self._listeners.append(fn)

    def remove_listener(self, fn: Callable):
        self._listeners = [l for l in self._listeners if l is not fn]

    def clear(self):
        self._records.clear()


# Singleton in-memory handler accessible by the log panel
_memory_handler: InMemoryHandler = InMemoryHandler()


def get_memory_handler() -> InMemoryHandler:
    return _memory_handler


def setup_logging(log_dir: Path = None):
    """Configure root logger with console, file, and in-memory handlers."""
    if log_dir is None:
        log_dir = Path.home() / ".llm_studio" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Console handler (INFO+)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    # Rotating file handler (DEBUG+)
    fh = logging.handlers.RotatingFileHandler(
        log_dir / "llm_studio.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    # In-memory handler (DEBUG+)
    _memory_handler.setLevel(logging.DEBUG)
    _memory_handler.setFormatter(fmt)

    # Avoid duplicate handlers on reload
    if not root.handlers:
        root.addHandler(ch)
        root.addHandler(fh)
        root.addHandler(_memory_handler)
    else:
        # Ensure memory handler is always present
        if _memory_handler not in root.handlers:
            root.addHandler(_memory_handler)
