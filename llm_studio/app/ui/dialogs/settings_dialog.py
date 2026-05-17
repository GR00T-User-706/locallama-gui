"""Settings Dialog — API endpoints, themes, shortcuts."""

import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
    QFormLayout, QDialogButtonBox, QGroupBox, QSpinBox,
    QMessageBox, QFrame, QScrollArea,
)

log = logging.getLogger(__name__)


class SettingsDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("Settings")
        self.setMinimumSize(640, 520)
        self._setup_ui()
        self._load()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 12)

        tabs = QTabWidget()

        # ── Backend / API ──────────────────────────────────────────────────
        api_page = self._make_api_page()
        tabs.addTab(api_page, "API / Backend")

        # ── UI ─────────────────────────────────────────────────────────────
        ui_page = self._make_ui_page()
        tabs.addTab(ui_page, "Interface")

        # ── Shortcuts ──────────────────────────────────────────────────────
        sc_page = self._make_shortcut_page()
        tabs.addTab(sc_page, "Shortcuts")

        layout.addWidget(tabs)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._on_accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    # ── API Page ──────────────────────────────────────────────────────────

    def _make_api_page(self):
        page = QScrollArea()
        page.setWidgetResizable(True)
        page.setStyleSheet("QScrollArea { border:none; }")
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Ollama
        ollama_group = QGroupBox("Ollama")
        ollama_form = QFormLayout(ollama_group)
        self._ollama_url = QLineEdit()
        self._ollama_key = QLineEdit()
        self._ollama_key.setEchoMode(QLineEdit.EchoMode.Password)
        self._ollama_enabled = QCheckBox("Enabled")

        btn_test_ollama = QPushButton("Test Connection")
        btn_test_ollama.clicked.connect(lambda: self._test_backend("ollama"))

        ollama_form.addRow("Base URL:", self._ollama_url)
        ollama_form.addRow("API Key (optional):", self._ollama_key)
        ollama_form.addRow("", self._ollama_enabled)
        ollama_form.addRow("", btn_test_ollama)
        layout.addWidget(ollama_group)

        # OpenAI-compatible
        oai_group = QGroupBox("OpenAI-Compatible")
        oai_form = QFormLayout(oai_group)
        self._oai_url = QLineEdit()
        self._oai_key = QLineEdit()
        self._oai_key.setEchoMode(QLineEdit.EchoMode.Password)
        self._oai_key.setPlaceholderText("sk-…")
        self._oai_enabled = QCheckBox("Enabled")

        oai_note = QLabel(
            "Works with: OpenAI, Groq, Together AI, LM Studio, vLLM, llama.cpp server"
        )
        oai_note.setObjectName("dimLabel")
        oai_note.setWordWrap(True)

        btn_test_oai = QPushButton("Test Connection")
        btn_test_oai.clicked.connect(lambda: self._test_backend("openai"))

        oai_form.addRow("Base URL:", self._oai_url)
        oai_form.addRow("API Key:", self._oai_key)
        oai_form.addRow("", self._oai_enabled)
        oai_form.addRow("Note:", oai_note)
        oai_form.addRow("", btn_test_oai)
        layout.addWidget(oai_group)

        # Active backend selector
        active_group = QGroupBox("Active Backend")
        active_form = QFormLayout(active_group)
        self._active_backend_combo = QComboBox()
        self._active_backend_combo.addItems(["ollama", "openai"])
        active_form.addRow("Use backend:", self._active_backend_combo)
        layout.addWidget(active_group)

        layout.addStretch()
        page.setWidget(inner)
        return page

    # ── UI Page ───────────────────────────────────────────────────────────

    def _make_ui_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        ui_group = QGroupBox("Interface")
        form = QFormLayout(ui_group)

        self._theme_combo = QComboBox()
        self._theme_combo.addItems(["dark", "light"])

        self._font_size_spin = QSpinBox()
        self._font_size_spin.setRange(9, 20)

        self._streaming_chk = QCheckBox("Enable streaming by default")

        form.addRow("Theme:", self._theme_combo)
        form.addRow("Font Size:", self._font_size_spin)
        form.addRow("", self._streaming_chk)

        layout.addWidget(ui_group)

        # Paths
        paths_group = QGroupBox("Paths")
        paths_form = QFormLayout(paths_group)

        sessions_row = QHBoxLayout()
        self._sessions_path = QLineEdit()
        self._sessions_path.setReadOnly(True)
        sessions_row.addWidget(self._sessions_path)

        plugins_row = QHBoxLayout()
        self._plugins_path = QLineEdit()
        self._plugins_path.setReadOnly(True)
        plugins_row.addWidget(self._plugins_path)

        paths_form.addRow("Sessions Dir:", self._sessions_path)
        paths_form.addRow("Plugins Dir:", self._plugins_path)

        layout.addWidget(paths_group)
        layout.addStretch()
        return page

    # ── Shortcuts Page ────────────────────────────────────────────────────

    def _make_shortcut_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        note = QLabel("Keyboard shortcut customization — restart required for changes.")
        note.setObjectName("dimLabel")
        layout.addWidget(note)

        shortcuts = self.config.get("shortcuts", {})
        self._shortcut_edits = {}
        for key, default in shortcuts.items():
            row = QHBoxLayout()
            lbl = QLabel(key.replace("_", " ").title() + ":")
            lbl.setFixedWidth(200)
            edit = QLineEdit(default)
            self._shortcut_edits[key] = edit
            row.addWidget(lbl)
            row.addWidget(edit)
            layout.addLayout(row)

        layout.addStretch()
        return page

    # ── Load / Save ───────────────────────────────────────────────────────

    def _load(self):
        o = self.config.get_backend_config("ollama")
        self._ollama_url.setText(o.get("base_url", "http://localhost:11434"))
        self._ollama_key.setText(o.get("api_key", ""))
        self._ollama_enabled.setChecked(o.get("enabled", True))

        oa = self.config.get_backend_config("openai")
        self._oai_url.setText(oa.get("base_url", "https://api.openai.com/v1"))
        self._oai_key.setText(oa.get("api_key", ""))
        self._oai_enabled.setChecked(oa.get("enabled", False))

        ab = self.config.active_backend
        idx = self._active_backend_combo.findText(ab)
        if idx >= 0:
            self._active_backend_combo.setCurrentIndex(idx)

        self._theme_combo.setCurrentText(self.config.get("theme", "dark"))
        self._font_size_spin.setValue(self.config.get("font_size", 13))
        self._streaming_chk.setChecked(self.config.streaming_enabled)
        self._sessions_path.setText(str(self.config.sessions_dir))
        self._plugins_path.setText(str(self.config.plugins_dir))

    def _on_accept(self):
        self.config.set_backend_config("ollama", {
            "base_url": self._ollama_url.text().strip(),
            "api_key": self._ollama_key.text().strip(),
            "enabled": self._ollama_enabled.isChecked(),
        })
        self.config.set_backend_config("openai", {
            "base_url": self._oai_url.text().strip(),
            "api_key": self._oai_key.text().strip(),
            "enabled": self._oai_enabled.isChecked(),
        })
        self.config.active_backend = self._active_backend_combo.currentText()
        self.config.set("theme", self._theme_combo.currentText())
        self.config.set("font_size", self._font_size_spin.value())
        self.config.streaming_enabled = self._streaming_chk.isChecked()

        shortcuts = {k: v.text().strip()
                     for k, v in self._shortcut_edits.items()}
        self.config.set("shortcuts", shortcuts)
        self.config.save()
        self.accept()

    def _test_backend(self, name: str):
        from app.backend import create_backend
        if name == "ollama":
            url = self._ollama_url.text().strip()
            key = self._ollama_key.text().strip()
        else:
            url = self._oai_url.text().strip()
            key = self._oai_key.text().strip()

        try:
            b = create_backend(name, url, key)
            status = b.get_status()
            if status["connected"]:
                QMessageBox.information(
                    self, "Connection OK",
                    f"Connected! Version: {status.get('version', 'unknown')}  "
                    f"Latency: {status.get('latency_ms', 0)}ms"
                )
            else:
                QMessageBox.warning(
                    self, "Not Connected",
                    f"Could not connect to {url}"
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
