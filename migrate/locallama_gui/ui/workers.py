from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable
from typing import Any

from PySide6.QtCore import QThread, Signal


class AsyncTask(QThread):
    result = Signal(object)
    error = Signal(str)
    finished_ok = Signal()

    def __init__(self, coro_factory: Callable[[], Any]) -> None:
        super().__init__()
        self.coro_factory = coro_factory
        self._loop: asyncio.AbstractEventLoop | None = None
        self._task: asyncio.Task[Any] | None = None

    def cancel(self) -> None:
        loop = self._loop
        task = self._task
        if loop is None or task is None or task.done():
            return
        try:
            loop.call_soon_threadsafe(task.cancel)
        except RuntimeError:
            pass

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._loop = loop
        self._task = loop.create_task(self.coro_factory())
        try:
            result = loop.run_until_complete(self._task)
            self.result.emit(result)
            self.finished_ok.emit()
        except asyncio.CancelledError:
            return
        except Exception as exc:  # noqa: BLE001
            self.error.emit(str(exc))
        finally:
            self._task = None
            self._loop = None
            loop.close()


class StreamTask(QThread):
    token = Signal(str)
    error = Signal(str)
    completed = Signal(str)

    def __init__(self, iterator_factory: Callable[[], AsyncIterator[str]]) -> None:
        super().__init__()
        self.iterator_factory = iterator_factory
        self._cancelled = False
        self.full_text = ""
        self._loop: asyncio.AbstractEventLoop | None = None
        self._task: asyncio.Task[None] | None = None

    def cancel(self) -> None:
        self._cancelled = True
        loop = self._loop
        task = self._task
        if loop is None or task is None or task.done():
            return
        try:
            loop.call_soon_threadsafe(task.cancel)
        except RuntimeError:
            pass

    def run(self) -> None:
        async def consume() -> None:
            async for token in self.iterator_factory():
                if self._cancelled:
                    break
                self.full_text += token
                self.token.emit(token)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._loop = loop
        self._task = loop.create_task(consume())
        try:
            loop.run_until_complete(self._task)
            if not self._cancelled:
                self.completed.emit(self.full_text)
        except asyncio.CancelledError:
            return
        except Exception as exc:  # noqa: BLE001
            self.error.emit(str(exc))
        finally:
            self._task = None
            self._loop = None
            loop.close()
