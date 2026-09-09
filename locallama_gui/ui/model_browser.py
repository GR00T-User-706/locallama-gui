from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote_plus

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from locallama_gui.backends.manager import create_backend
from locallama_gui.ui.diagnostics import OperationStreamParser
from locallama_gui.ui.workers import StreamTask


@dataclass(frozen=True)
class ModelRecommendation:
    name: str
    size: str
    purpose: str
    minimum_ram_gib: float


CATALOG = (
    ModelRecommendation("gemma3:1b", "~0.8 GB", "Very small general-purpose starter", 4),
    ModelRecommendation("qwen3.5:4b", "~3.4 GB", "Small general-purpose + vision starter", 8),
    ModelRecommendation("mistral:7b", "~4.1 GB", "Classic 7B general-purpose model", 12),
    ModelRecommendation("deepseek-r1:7b", "~4.7 GB", "7B reasoning model", 12),
    ModelRecommendation("qwen2.5-coder:7b", "~4.7 GB", "7B coding-focused model", 12),
)


class ModelBrowserDialog(QDialog):
    def __init__(self, window, recommended_name: str | None = None) -> None:
        super().__init__(window)
        self.window = window
        self.setWindowTitle("Model Browser")
        self.resize(760, 520)
        self.list = QListWidget()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Filter recommended models...")
        self.pull_button = QPushButton("Pull Selected")
        self.library_button = QPushButton("Open Ollama Model Library")
        self.close_button = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.close_button.rejected.connect(self.reject)
        self.pull_button.clicked.connect(self.pull_selected)
        self.library_button.clicked.connect(self.open_library)
        self.search.textChanged.connect(self.filter_models)

        top = QHBoxLayout()
        top.addWidget(QLabel("Model:"))
        top.addWidget(self.search)
        buttons = QHBoxLayout()
        buttons.addWidget(self.pull_button)
        buttons.addWidget(self.library_button)
        buttons.addStretch()
        buttons.addWidget(self.close_button)
        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.list)
        layout.addLayout(buttons)

        for model in CATALOG:
            item = QListWidgetItem(f"{model.name}   |   {model.size}   |   {model.purpose}")
            item.setData(256, model.name)
            self.list.addItem(item)
        if recommended_name:
            for index in range(self.list.count()):
                if self.list.item(index).data(256) == recommended_name:
                    self.list.setCurrentRow(index)
                    break
        if self.list.currentRow() < 0:
            self.list.setCurrentRow(0)

    def filter_models(self, text: str) -> None:
        needle = text.strip().lower()
        for index in range(self.list.count()):
            item = self.list.item(index)
            item.setHidden(bool(needle and needle not in item.text().lower()))

    def open_library(self) -> None:
        query = self.search.text().strip()
        url = "https://ollama.com/search"
        if query:
            url += f"?q={quote_plus(query)}"
        QDesktopServices.openUrl(QUrl(url))

    def pull_selected(self) -> None:
        item = self.list.currentItem()
        if item is None:
            QMessageBox.information(self, "Model Browser", "Select a model first.")
            return
        name = str(item.data(256) or "").strip()
        if not name:
            return
        operation = f"Pull model: {name}"
        parser = OperationStreamParser()
        self.window.begin_operation(operation)
        self.pull_button.setEnabled(False)
        task = StreamTask(
            lambda: create_backend(self.window.config.active_profile()).pull_model(name)
        )
        self.window.add_worker(task)

        def on_stream(chunk: str) -> None:
            for update in parser.feed(chunk):
                self.window.update_operation(update)

        def on_completed(_output: str) -> None:
            self.window.complete_operation(operation)
            self.window.refresh_backend()
            self.pull_button.setEnabled(True)
            QMessageBox.information(self, "Model Browser", f"{name} is ready to use.")

        def on_error(error: str) -> None:
            self.window.fail_operation(operation, error)
            self.pull_button.setEnabled(True)
            QMessageBox.critical(self, "Pull Model", error)

        task.token.connect(on_stream)
        task.completed.connect(on_completed)
        task.error.connect(on_error)
        task.start()
