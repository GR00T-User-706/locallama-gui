from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable
from typing import Any

from PySide6.QtCore import QObject, QThread, Signal


class AsyncTask(QThread):
    result = Signal(object)
    error = Signal(str)
    finished_ok = Signal()

    def __init__(self, coro_factory: Callable[[], Any]) -> None:
        super().__init__()
        self.coro_factory = coro_factory

    def run(self) -> None:
        try:
            result = asyncio.run(self.coro_factory())
            self.result.emit(result)
            self.finished_ok.emit()
        except Exception as exc:  # noqa: BLE001
            self.error.emit(str(exc))


class StreamTask(QThread):
    token = Signal(str)
    error = Signal(str)
    completed = Signal(str)

    def __init__(self, iterator_factory: Callable[[], AsyncIterator[str]]) -> None:
        super().__init__()
        self.iterator_factory = iterator_factory
        self._cancelled = False
        self.full_text = ""

    def cancel(self) -> None:
        self._cancelled = True

    def run(self) -> None:
        async def consume() -> None:
            async for token in self.iterator_factory():
                if self._cancelled:
                    break
                self.full_text += token
                self.token.emit(token)
        try:
            asyncio.run(consume())
            self.completed.emit(self.full_text)
        except Exception as exc:  # noqa: BLE001
            self.error.emit(str(exc))
