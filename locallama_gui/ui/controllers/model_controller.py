from __future__ import annotations

from typing import Protocol


from locallama_gui.backends.manager import create_backend
from locallama_gui.ui.workers import StreamTask


class ModelWindowPort(Protocol):
    def model_name(self) -> str: ...
    def append_terminal(self, text: str) -> None: ...
    def refresh_backend(self) -> None: ...
    def add_worker(self, worker) -> None: ...
    def run_async(self, coro_factory, done_msg: str) -> None: ...
    def open_modelfile_editor(self) -> None: ...


class ModelController:
    def __init__(self, config, window: ModelWindowPort) -> None:
        self.config = config
        self.window = window

    def pull_model(self, parent) -> None:
        self._model_stream_op(parent, "Pull model", "pull_model")

    def push_model(self, parent) -> None:
        self._model_stream_op(parent, "Push model", "push_model")

    def create_model(self) -> None:
        self.window.open_modelfile_editor()

    def clone_model(self, parent) -> None:
        source = self.window.model_name()
        dest, ok = __import__("PySide6.QtWidgets", fromlist=["QInputDialog"]).QInputDialog.getText(parent, "Clone Model", "Destination model name:")
        if ok and source and dest:
            self.window.run_async(lambda: create_backend(self.config.active_profile()).copy_model(source, dest), "Model cloned")

    def delete_model(self, parent) -> None:
        name = self.window.model_name().strip()
        if not name:
            __import__("PySide6.QtWidgets", fromlist=["QMessageBox"]).QMessageBox.information(
                parent,
                "Delete Model",
                "Select a model before attempting deletion.",
            )
            return

        confirm = __import__("PySide6.QtWidgets", fromlist=["QMessageBox"]).QMessageBox.question(
            parent,
            "Delete Model",
            f"Delete model '{name}'? This action cannot be undone.",
            __import__("PySide6.QtWidgets", fromlist=["QMessageBox"]).QMessageBox.StandardButton.Yes
            | __import__("PySide6.QtWidgets", fromlist=["QMessageBox"]).QMessageBox.StandardButton.No,
            __import__("PySide6.QtWidgets", fromlist=["QMessageBox"]).QMessageBox.StandardButton.No,
        )
        if confirm != __import__("PySide6.QtWidgets", fromlist=["QMessageBox"]).QMessageBox.StandardButton.Yes:
            return

        self.window.run_async(
            lambda: create_backend(self.config.active_profile()).delete_model(name),
            f"Model deleted: {name}",
        )

    def _model_stream_op(self, parent, title: str, method: str) -> None:
        name, ok = __import__("PySide6.QtWidgets", fromlist=["QInputDialog"]).QInputDialog.getText(parent, title, "Model name:", text=self.window.model_name())
        if not ok or not name:
            return
        backend = create_backend(self.config.active_profile())
        task = StreamTask(lambda: getattr(backend, method)(name))
        self.window.add_worker(task)
        task.token.connect(lambda t: self.window.append_terminal(t + "\n"))
        task.completed.connect(lambda _: self.window.refresh_backend())
        task.error.connect(lambda e: __import__("PySide6.QtWidgets", fromlist=["QMessageBox"]).QMessageBox.critical(parent, title, e))
        task.start()
