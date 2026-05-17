"""
Model Management Panel.
Displays installed models, model details, and allows pull/delete/create/copy.
Uses a background QThread for all API operations.
"""

import logging
from typing import Optional, List

from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QGroupBox, QFormLayout,
    QLineEdit, QProgressBar, QTextEdit, QSplitter, QComboBox,
    QMessageBox, QDialog, QDialogButtonBox, QPlainTextEdit,
)

from app.models.model_info import ModelInfo

log = logging.getLogger(__name__)


class ModelWorker(QThread):
    """Generic worker for model operations."""
    progress = Signal(dict)
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def run(self):
        try:
            result = self._fn(*self._args, **self._kwargs)
            # If it's a generator (pull/create), iterate and emit progress
            if hasattr(result, "__iter__") and not isinstance(result, (list, dict)):
                last = None
                for item in result:
                    self.progress.emit(item)
                    last = item
                self.finished.emit(last)
            else:
                self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class PullModelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pull Model")
        self.setFixedWidth(440)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        info = QLabel("Enter the model name to pull from Ollama Hub.\n"
                      "Examples: llama3.2, mistral, qwen2.5:7b, phi4:latest")
        info.setWordWrap(True)
        info.setObjectName("dimLabel")

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("e.g. llama3.2:latest")

        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setVisible(False)

        self._status_lbl = QLabel("")
        self._status_lbl.setObjectName("dimLabel")
        self._status_lbl.setWordWrap(True)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        layout.addWidget(info)
        layout.addWidget(self._name_edit)
        layout.addWidget(self._progress)
        layout.addWidget(self._status_lbl)
        layout.addWidget(btns)

    def model_name(self) -> str:
        return self._name_edit.text().strip()

    def set_progress(self, pct: int, status: str):
        self._progress.setVisible(True)
        self._progress.setValue(pct)
        self._status_lbl.setText(status)


class ModelPanel(QWidget):
    """Left-side model management panel."""

    model_selected = Signal(str)     # emitted when user selects a model
    status_message = Signal(str)

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self._models: List[ModelInfo] = []
        self._selected: Optional[ModelInfo] = None
        self._worker: Optional[ModelWorker] = None
        self._setup_ui()
        self._start_status_timer()
        QTimer.singleShot(200, self.refresh_models)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Connection status bar ─────────────────────────────────────────
        self._status_bar = QWidget()
        self._status_bar.setFixedHeight(36)
        self._status_bar.setStyleSheet("background:#11111b; border-bottom:1px solid #313244;")
        sb_layout = QHBoxLayout(self._status_bar)
        sb_layout.setContentsMargins(10, 4, 10, 4)

        self._conn_indicator = QLabel("●")
        self._conn_indicator.setStyleSheet("color:#f38ba8; font-size:10px;")
        self._conn_lbl = QLabel("Checking…")
        self._conn_lbl.setObjectName("dimLabel")
        self._latency_lbl = QLabel("")
        self._latency_lbl.setObjectName("dimLabel")

        sb_layout.addWidget(self._conn_indicator)
        sb_layout.addWidget(self._conn_lbl)
        sb_layout.addStretch()
        sb_layout.addWidget(self._latency_lbl)

        layout.addWidget(self._status_bar)

        # ── Splitter: model list / detail ─────────────────────────────────
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setStyleSheet("QSplitter::handle { background:#313244; }")

        # Model list panel
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(8, 8, 8, 4)
        list_layout.setSpacing(6)

        # Search + refresh
        search_row = QHBoxLayout()
        self._search = QLineEdit()
        self._search.setPlaceholderText("Filter models…")
        self._search.textChanged.connect(self._filter_models)
        btn_refresh = QPushButton("⟳")
        btn_refresh.setFixedWidth(30)
        btn_refresh.setToolTip("Refresh model list")
        btn_refresh.clicked.connect(self.refresh_models)
        search_row.addWidget(self._search)
        search_row.addWidget(btn_refresh)

        self._model_list = QListWidget()
        self._model_list.setAlternatingRowColors(True)
        self._model_list.currentRowChanged.connect(self._on_model_selected)
        self._model_list.itemDoubleClicked.connect(self._on_model_double_click)

        list_layout.addLayout(search_row)
        list_layout.addWidget(self._model_list)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(4)
        self._btn_pull = QPushButton("⇓ Pull")
        self._btn_pull.setToolTip("Pull a model from Ollama Hub")
        self._btn_pull.clicked.connect(self._on_pull)
        self._btn_delete = QPushButton("✕ Delete")
        self._btn_delete.setObjectName("dangerButton")
        self._btn_delete.setToolTip("Delete selected model")
        self._btn_delete.clicked.connect(self._on_delete)
        self._btn_copy = QPushButton("⧉ Copy")
        self._btn_copy.setToolTip("Copy/clone selected model")
        self._btn_copy.clicked.connect(self._on_copy_model)

        btn_row.addWidget(self._btn_pull)
        btn_row.addWidget(self._btn_copy)
        btn_row.addStretch()
        btn_row.addWidget(self._btn_delete)
        list_layout.addLayout(btn_row)

        # Progress area
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setVisible(False)
        self._progress_bar.setFixedHeight(6)
        self._progress_lbl = QLabel("")
        self._progress_lbl.setObjectName("dimLabel")
        self._progress_lbl.setVisible(False)
        list_layout.addWidget(self._progress_bar)
        list_layout.addWidget(self._progress_lbl)

        splitter.addWidget(list_widget)

        # Model detail panel
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(8, 8, 8, 8)
        detail_layout.setSpacing(6)

        detail_title = QLabel("Model Details")
        detail_title.setObjectName("sectionLabel")
        detail_layout.addWidget(detail_title)

        form = QFormLayout()
        form.setSpacing(4)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._det_name = QLabel("—")
        self._det_size = QLabel("—")
        self._det_quant = QLabel("—")
        self._det_params = QLabel("—")
        self._det_ctx = QLabel("—")
        self._det_family = QLabel("—")
        self._det_digest = QLabel("—")
        self._det_ram = QLabel("—")

        for lbl_text, widget in [
            ("Name:", self._det_name), ("Size:", self._det_size),
            ("Quantization:", self._det_quant), ("Parameters:", self._det_params),
            ("Context:", self._det_ctx), ("Family:", self._det_family),
            ("RAM Est.:", self._det_ram), ("Digest:", self._det_digest),
        ]:
            form.addRow(QLabel(lbl_text), widget)

        detail_layout.addLayout(form)
        detail_layout.addStretch()

        # Detail action buttons
        detail_btns = QHBoxLayout()
        btn_use = QPushButton("▶ Use Model")
        btn_use.setObjectName("primaryButton")
        btn_use.clicked.connect(self._on_use_model)
        btn_show_mf = QPushButton("✎ Modelfile")
        btn_show_mf.setToolTip("View/edit this model's Modelfile")
        btn_show_mf.clicked.connect(self._on_show_modelfile)
        detail_btns.addWidget(btn_use)
        detail_btns.addWidget(btn_show_mf)
        detail_btns.addStretch()
        detail_layout.addLayout(detail_btns)

        splitter.addWidget(detail_widget)
        splitter.setSizes([300, 220])

        layout.addWidget(splitter, stretch=1)

    # ── Timer for connection status ────────────────────────────────────────

    def _start_status_timer(self):
        self._status_timer = QTimer(self)
        self._status_timer.timeout.connect(self._check_status)
        self._status_timer.start(5000)   # every 5 s
        QTimer.singleShot(100, self._check_status)

    def _check_status(self):
        backend = self.app_state.get_backend()
        if not backend:
            self._set_conn_state(False, "No backend", 0)
            return

        def _do():
            try:
                return backend.get_status()
            except Exception:
                return {"connected": False, "version": "", "latency_ms": 0}

        w = ModelWorker(_do)
        w.finished.connect(self._on_status_result)
        w.start()

    def _on_status_result(self, status):
        if isinstance(status, dict):
            connected = status.get("connected", False)
            version = status.get("version", "")
            latency = status.get("latency_ms", 0)
            label = f"{self.app_state.config.active_backend}"
            if version:
                label += f" {version}"
            self._set_conn_state(connected, label, latency)
        else:
            self._set_conn_state(False, "Error", 0)

    def _set_conn_state(self, connected: bool, label: str, latency: int):
        color = "#a6e3a1" if connected else "#f38ba8"
        self._conn_indicator.setStyleSheet(f"color:{color}; font-size:10px;")
        self._conn_lbl.setText(label)
        if connected:
            self._latency_lbl.setText(f"{latency}ms")
        else:
            self._latency_lbl.setText("")

    # ── Model list ─────────────────────────────────────────────────────────

    def refresh_models(self):
        backend = self.app_state.get_backend()
        if not backend:
            return
        w = ModelWorker(backend.list_models)
        w.finished.connect(self._on_models_loaded)
        w.error.connect(lambda e: log.error("list_models error: %s", e))
        w.start()

    def _on_models_loaded(self, models):
        if not isinstance(models, list):
            return
        self._models = models
        self._fill_list(models)
        self.app_state.on_models_refreshed(models)
        self.status_message.emit(f"{len(models)} models available")

    def _fill_list(self, models: List[ModelInfo]):
        current_text = (self._model_list.currentItem().text()
                        if self._model_list.currentItem() else "")
        self._model_list.clear()
        for m in models:
            item = QListWidgetItem()
            item.setText(f"{m.display_name}")
            item.setData(Qt.ItemDataRole.UserRole, m)
            tooltip = (f"Size: {m.size_str}  |  "
                       f"Params: {m.parameter_size}  |  "
                       f"Quant: {m.quantization_level}")
            item.setToolTip(tooltip)
            self._model_list.addItem(item)
        # Restore selection
        for i in range(self._model_list.count()):
            if self._model_list.item(i).text() == current_text:
                self._model_list.setCurrentRow(i)
                break

    def _filter_models(self, query: str):
        q = query.lower()
        filtered = [m for m in self._models
                    if q in m.name.lower()] if q else self._models
        self._fill_list(filtered)

    def _on_model_selected(self, row: int):
        item = self._model_list.item(row)
        if not item:
            return
        m = item.data(Qt.ItemDataRole.UserRole)
        if m:
            self._selected = m
            self._update_details(m)

    def _on_model_double_click(self, item: QListWidgetItem):
        self._on_use_model()

    def _update_details(self, m: ModelInfo):
        self._det_name.setText(m.name)
        self._det_size.setText(m.size_str)
        self._det_quant.setText(m.quantization_level or "—")
        self._det_params.setText(m.parameter_size or "—")
        self._det_ctx.setText(str(m.context_length) if m.context_length else "—")
        self._det_family.setText(m.family or "—")
        self._det_ram.setText(f"{m.ram_estimate_gb():.1f} GB" if m.size else "—")
        digest = m.digest[:20] + "…" if len(m.digest) > 20 else m.digest
        self._det_digest.setText(digest or "—")

    # ── Actions ───────────────────────────────────────────────────────────

    def _on_use_model(self):
        if not self._selected:
            return
        self.app_state.config.active_model = self._selected.name
        self.model_selected.emit(self._selected.name)
        self.status_message.emit(f"Active model: {self._selected.name}")

    def _on_pull(self):
        dlg = PullModelDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        model_name = dlg.model_name()
        if not model_name:
            return

        backend = self.app_state.get_backend()
        if not backend:
            return

        self._progress_bar.setVisible(True)
        self._progress_lbl.setVisible(True)
        self._progress_bar.setValue(0)
        self._progress_lbl.setText(f"Pulling {model_name}…")

        w = ModelWorker(backend.pull_model, model_name)
        w.progress.connect(self._on_pull_progress)
        w.finished.connect(self._on_pull_done)
        w.error.connect(self._on_pull_error)
        w.start()
        self._worker = w

    def _on_pull_progress(self, data: dict):
        status = data.get("status", "")
        completed = data.get("completed", 0)
        total = data.get("total", 0)
        if total > 0:
            pct = int(completed / total * 100)
            self._progress_bar.setValue(pct)
        self._progress_lbl.setText(status)

    def _on_pull_done(self, _):
        self._progress_bar.setVisible(False)
        self._progress_lbl.setVisible(False)
        self.refresh_models()
        QMessageBox.information(self, "Pull Complete", "Model pulled successfully.")

    def _on_pull_error(self, err: str):
        self._progress_bar.setVisible(False)
        self._progress_lbl.setVisible(False)
        QMessageBox.critical(self, "Pull Failed", f"Error: {err}")

    def _on_delete(self):
        if not self._selected:
            QMessageBox.information(self, "No Selection", "Select a model first.")
            return
        reply = QMessageBox.question(
            self, "Delete Model",
            f"Delete model '{self._selected.name}'?\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return
        backend = self.app_state.get_backend()
        if not backend:
            return
        w = ModelWorker(backend.delete_model, self._selected.name)
        w.finished.connect(lambda _: self.refresh_models())
        w.error.connect(lambda e: QMessageBox.critical(self, "Delete Failed", e))
        w.start()

    def _on_copy_model(self):
        if not self._selected:
            return
        from PySide6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(
            self, "Clone Model", "New model name:",
            text=f"{self._selected.name}-copy"
        )
        if not ok or not name.strip():
            return
        backend = self.app_state.get_backend()
        if not backend:
            return
        w = ModelWorker(backend.copy_model, self._selected.name, name.strip())
        w.finished.connect(lambda _: self.refresh_models())
        w.error.connect(lambda e: QMessageBox.critical(self, "Clone Failed", e))
        w.start()

    def _on_show_modelfile(self):
        if not self._selected:
            return
        self.app_state.show_modelfile_for(self._selected.name)

    def get_model_names(self) -> List[str]:
        return [m.name for m in self._models]
