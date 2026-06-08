from __future__ import annotations

from typing import Protocol

from locallama_gui.backends.manager import create_backend
from locallama_gui.ui.workers import StreamTask


class ModelWindowPort(Protocol):
    def model_name(self) -> str: ...
    def append_terminal(self, text: str) -> None: ...
    def refresh_backend(self) -> None: ...
    def add_worker(self, worker) -> None: ...
    def run_async(
        self,
        coro_factory,
        done_msg: str,
        *,
        start_msg: str,
        error_title: str,
        parent,
    ) -> None: ...
    def open_modelfile_editor(self) -> None: ...


class ModelController:
    def __init__(self, config, window: ModelWindowPort) -> None:
        self.config = config
        self.window = window

    def pull_model(self, parent) -> None:
        self._model_stream_op(parent, "Pull Model", "pull_model")

    def push_model(self, parent) -> None:
        self._model_stream_op(parent, "Push Model", "push_model")

    def create_model(self) -> None:
        self.window.open_modelfile_editor()

    def clone_model(self, parent) -> None:
        widgets = __import__("PySide6.QtWidgets", fromlist=["QInputDialog", "QMessageBox"])
        source = self.window.model_name().strip()
        if not source:
            widgets.QMessageBox.information(
                parent,
                "Clone Model",
                "Select a model before attempting to clone it.",
            )
            return

        destination, ok = widgets.QInputDialog.getText(
            parent,
            "Clone Model",
            "Destination model name:",
        )
        if not ok:
            return
        destination = destination.strip()
        if not destination:
            widgets.QMessageBox.information(
                parent,
                "Clone Model",
                "Destination model name is required.",
            )
            return

        operation = f"Clone model {source} -> {destination}"
        self.window.run_async(
            lambda: create_backend(self.config.active_profile()).copy_model(
                source, destination
            ),
            operation,
            start_msg=operation,
            error_title="Clone Model",
            parent=parent,
        )

    def delete_model(self, parent) -> None:
        widgets = __import__("PySide6.QtWidgets", fromlist=["QMessageBox"])
        name = self.window.model_name().strip()
        if not name:
            widgets.QMessageBox.information(
                parent,
                "Delete Model",
                "Select a model before attempting deletion.",
            )
            return

        confirm = widgets.QMessageBox.question(
            parent,
            "Delete Model",
            f"Delete model '{name}'? This action cannot be undone.",
            widgets.QMessageBox.StandardButton.Yes
            | widgets.QMessageBox.StandardButton.No,
            widgets.QMessageBox.StandardButton.No,
        )
        if confirm != widgets.QMessageBox.StandardButton.Yes:
            return

        operation = f"Delete model {name}"
        self.window.run_async(
            lambda: create_backend(self.config.active_profile()).delete_model(name),
            operation,
            start_msg=operation,
            error_title="Delete Model",
            parent=parent,
        )

    def _model_stream_op(self, parent, title: str, method: str) -> None:
        widgets = __import__("PySide6.QtWidgets", fromlist=["QInputDialog", "QMessageBox"])
        name, ok = widgets.QInputDialog.getText(
            parent,
            title,
            "Model name:",
            text=self.window.model_name().strip(),
        )
        if not ok:
            return
        name = name.strip()
        if not name:
            widgets.QMessageBox.information(parent, title, "Model name is required.")
            return

        operation = f"{title}: {name}"
        self.window.append_terminal(f"[START] {operation}\n")
        task = StreamTask(
            lambda: getattr(create_backend(self.config.active_profile()), method)(name)
        )
        self.window.add_worker(task)
        task.token.connect(lambda text: self.window.append_terminal(text + "\n"))

        def on_completed(_output: str) -> None:
            self.window.append_terminal(f"[OK] {operation}\n")
            self.window.refresh_backend()

        def on_error(error: str) -> None:
            self.window.append_terminal(f"[ERROR] {operation}: {error}\n")
            widgets.QMessageBox.critical(parent, title, error)

        task.completed.connect(on_completed)
        task.error.connect(on_error)
        task.start()
