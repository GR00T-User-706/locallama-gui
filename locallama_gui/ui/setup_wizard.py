from __future__ import annotations

import psutil
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWizard,
    QWizardPage,
)

from locallama_gui.backends.manager import create_backend
from locallama_gui.ui.model_browser import CATALOG
from locallama_gui.ui.workers import AsyncTask


class FirstRunWizard(QWizard):
    def __init__(self, config, parent=None) -> None:
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("Welcome to MyLoAI")
        self.setMinimumSize(720, 520)
        self._connection_ok = False
        self._pull_on_finish = False

        self.welcome_page = self._build_welcome_page()
        self.hardware_page = self._build_hardware_page()
        self.backend_page = self._build_backend_page()
        self.finish_page = self._build_finish_page()
        self.addPage(self.welcome_page)
        self.addPage(self.hardware_page)
        self.addPage(self.backend_page)
        self.addPage(self.finish_page)
        self.currentIdChanged.connect(self._page_changed)

    def _build_welcome_page(self) -> QWizardPage:
        page = QWizardPage()
        page.setTitle("Welcome to MyLoAI")
        layout = QVBoxLayout(page)
        layout.addWidget(
            QLabel(
                "MyLoAI is ready. This short setup checks your hardware, verifies the local Ollama connection, "
                "and can install a sensible starter model. You can change everything later."
            )
        )
        return page

    def _build_hardware_page(self) -> QWizardPage:
        page = QWizardPage()
        page.setTitle("Hardware check")
        layout = QVBoxLayout(page)
        self.hardware_label = QLabel()
        self.hardware_label.setWordWrap(True)
        layout.addWidget(self.hardware_label)
        layout.addWidget(
            QLabel(
                "This is a conservative recommendation based on system RAM and CPU count. "
                "It does not pretend to know your GPU when the platform does not expose reliable GPU telemetry."
            )
        )
        return page

    def _build_backend_page(self) -> QWizardPage:
        page = QWizardPage()
        page.setTitle("Local AI service")
        layout = QVBoxLayout(page)
        form = QFormLayout()
        self.provider_label = QLabel(self.config.active_profile().name)
        self.status_label = QLabel("Checking localhost:11434...")
        self.model_combo = QComboBox()
        self.model_combo.addItems([item.name for item in CATALOG])
        form.addRow("Provider", self.provider_label)
        form.addRow("Connection", self.status_label)
        form.addRow("Starter model", self.model_combo)
        layout.addLayout(form)
        self.pull_check = QCheckBox("Pull the starter model after setup when Ollama is available")
        self.pull_check.setChecked(True)
        layout.addWidget(self.pull_check)
        self.install_button = QPushButton("Open Ollama download page")
        self.install_button.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://ollama.com/download"))
        )
        layout.addWidget(self.install_button)
        return page

    def _build_finish_page(self) -> QWizardPage:
        page = QWizardPage()
        page.setTitle("Ready")
        layout = QVBoxLayout(page)
        self.finish_label = QLabel()
        self.finish_label.setWordWrap(True)
        layout.addWidget(self.finish_label)
        return page

    def _recommended_model(self) -> str:
        ram = psutil.virtual_memory().total / 1024**3
        if ram < 6:
            return "gemma3:1b"
        if ram < 12:
            return "qwen3.5:4b"
        if ram < 24:
            return "mistral:7b"
        return "deepseek-r1:7b"

    def _page_changed(self, index: int) -> None:
        if index == 1:
            ram = psutil.virtual_memory().total / 1024**3
            cores = psutil.cpu_count(logical=True) or 1
            recommended = self._recommended_model()
            self.hardware_label.setText(
                f"Detected: {cores} logical CPU cores and {ram:.1f} GiB system RAM.\n\n"
                f"Recommended starter model: {recommended}."
            )
            self.model_combo.setCurrentText(recommended)
        elif index == 2:
            self._check_backend()
        elif index == 3:
            model = self.model_combo.currentText()
            if self._connection_ok and self.pull_check.isChecked():
                self.finish_label.setText(
                    f"Ollama is available. MyLoAI will save {model} as the starter model and pull it when you finish."
                )
            elif self._connection_ok:
                self.finish_label.setText(
                    f"Ollama is available. MyLoAI will save {model} as the starter model."
                )
            else:
                self.finish_label.setText(
                    "Ollama is not reachable yet. MyLoAI will still save your provider settings. "
                    "Install/start Ollama and use Models → Browse & Pull Models when it is ready."
                )

    def _check_backend(self) -> None:
        self.status_label.setText("Checking localhost:11434...")
        self._connection_ok = False

        async def work():
            return await create_backend(self.config.active_profile()).test_connection()

        task = AsyncTask(work)
        self._task = task

        def done(status) -> None:
            self._connection_ok = status.state == "connected"
            if self._connection_ok:
                self.status_label.setText(f"Connected ({status.latency_ms:.0f} ms)")
            else:
                self.status_label.setText("Not connected. Ollama may not be installed or running.")

        def failed(error: str) -> None:
            self._connection_ok = False
            self.status_label.setText("Not connected. Ollama may not be installed or running.")

        task.result.connect(done)
        task.error.connect(failed)
        task.start()

    def accept(self) -> None:
        model = self.model_combo.currentText().strip()
        profile = self.config.active_profile()
        profile.default_model = model
        self.config.save()
        self._pull_on_finish = self._connection_ok and self.pull_check.isChecked()
        if not self._pull_on_finish:
            super().accept()
            return

        self.setEnabled(False)
        self.parent().begin_operation(f"Pull starter model: {model}")
        from locallama_gui.ui.diagnostics import OperationStreamParser
        from locallama_gui.ui.workers import StreamTask

        parser = OperationStreamParser()
        task = StreamTask(lambda: create_backend(profile).pull_model(model))
        self._pull_task = task
        self.parent().add_worker(task)
        task.token.connect(lambda chunk: [self.parent().update_operation(update) for update in parser.feed(chunk)])

        def done(_output: str) -> None:
            self.parent().complete_operation(f"Pull starter model: {model}")
            self.parent().refresh_backend()
            self.setEnabled(True)
            super(FirstRunWizard, self).accept()

        def failed(error: str) -> None:
            self.parent().fail_operation(f"Pull starter model: {model}", error)
            self.setEnabled(True)
            QMessageBox.warning(
                self,
                "Starter model not installed",
                f"MyLoAI was configured successfully, but the starter model could not be pulled.\n\n{error}",
            )
            super(FirstRunWizard, self).accept()

        task.completed.connect(done)
        task.error.connect(failed)
        task.start()
