"""
Modelfile Editor — full editor with syntax highlighting,
build, validate, and version history.
"""

import logging
from pathlib import Path
from typing import Optional, List

from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPushButton,
    QLabel, QFileDialog, QMessageBox, QPlainTextEdit, QTextEdit,
    QComboBox, QLineEdit, QGroupBox, QFormLayout, QDialog,
    QDialogButtonBox, QListWidget, QListWidgetItem, QProgressBar,
)

from app.ui.widgets.modelfile_highlighter import ModelfileHighlighter

log = logging.getLogger(__name__)

DEFAULT_MODELFILE = """\
FROM llama3.2

# System prompt — defines the AI's persona and behavior
SYSTEM \"\"\"You are a helpful, concise assistant. Answer clearly and directly.\"\"\"

# Chat template (optional — defaults to model's built-in template)
# TEMPLATE \"\"\"{{ if .System }}<|system|>
# {{ .System }}<|end|>
# {{ end }}{{ if .Prompt }}<|user|>
# {{ .Prompt }}<|end|>
# {{ end }}<|assistant|>
# \"\"\"

# Generation parameters
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 4096

# Stop sequences
PARAMETER stop \"<|end|>\"
PARAMETER stop \"<|user|>\"
PARAMETER stop \"<|assistant|>\"
"""

MODELFILE_REFERENCE = """
Modelfile Directives Reference
═══════════════════════════════

FROM <model>          Base model (required)
  e.g. FROM llama3.2  FROM mistral:7b  FROM ./my-model.gguf

SYSTEM "<text>"       System prompt (overrides model default)
  or SYSTEM \"\"\"multi-line text\"\"\"

TEMPLATE "<tmpl>"     Go template for prompt formatting
  Variables: .System .Prompt .Response

PARAMETER <key> <val> Generation parameters:
  temperature   float  [0.0–2.0]   Randomness
  top_k         int    [1–100]     Top-K sampling
  top_p         float  [0.0–1.0]   Nucleus sampling
  min_p         float  [0.0–1.0]   Min-P sampling
  repeat_penalty float [1.0–2.0]   Repetition penalty
  repeat_last_n int                Penalty lookback
  num_predict   int    (-1=inf)    Max tokens to generate
  num_ctx       int                Context window size
  num_batch     int                Batch size
  num_gpu       int    (-1=all)    GPU layers
  mirostat      int    [0–2]       Mirostat mode
  mirostat_tau  float              Mirostat tau
  mirostat_eta  float              Mirostat eta
  seed          int    (-1=rand)   Random seed
  stop          string             Stop sequence

MESSAGE <role> "<content>"   Pre-populate conversation
  role: user | assistant | system

ADAPTER <path>         LoRA adapter (GGUF format)

LICENSE "<text>"       Model license
"""


class BuildWorker(QThread):
    progress = Signal(dict)
    finished = Signal(bool, str)

    def __init__(self, backend, name: str, modelfile: str):
        super().__init__()
        self.backend = backend
        self.name = name
        self.modelfile = modelfile

    def run(self):
        try:
            last_status = ""
            for item in self.backend.create_model(self.name, self.modelfile):
                self.progress.emit(item)
                last_status = item.get("status", "")
            self.finished.emit(True, last_status)
        except Exception as e:
            self.finished.emit(False, str(e))


class ModelfileEditor(QWidget):
    """Full Modelfile editor with syntax highlighting and build support."""

    build_complete = Signal(str)   # model name built

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self._current_path: Optional[Path] = None
        self._modified = False
        self._history: List[str] = []   # version history
        self._history_index = -1
        self._worker: Optional[BuildWorker] = None
        self._setup_ui()
        self._editor.setPlainText(DEFAULT_MODELFILE)
        self._push_history(DEFAULT_MODELFILE)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Toolbar ────────────────────────────────────────────────────────
        toolbar = QWidget()
        toolbar.setStyleSheet(
            "background:#181825; border-bottom:1px solid #313244;"
        )
        toolbar.setFixedHeight(42)
        tb = QHBoxLayout(toolbar)
        tb.setContentsMargins(8, 4, 8, 4)
        tb.setSpacing(6)

        btn_new = QPushButton("⊕ New")
        btn_new.setToolTip("New Modelfile")
        btn_new.clicked.connect(self._on_new)
        btn_open = QPushButton("⊘ Open…")
        btn_open.clicked.connect(self._on_open)
        btn_save = QPushButton("⊙ Save")
        btn_save.clicked.connect(self._on_save)
        btn_save_as = QPushButton("Save As…")
        btn_save_as.clicked.connect(self._on_save_as)

        sep1 = QLabel("|")
        sep1.setStyleSheet("color:#45475a;")

        btn_undo = QPushButton("↩")
        btn_undo.setToolTip("Undo (Ctrl+Z)")
        btn_undo.setFixedWidth(30)
        btn_undo.clicked.connect(self._editor_undo if hasattr(self, '_editor') else lambda: None)
        btn_redo = QPushButton("↪")
        btn_redo.setToolTip("Redo (Ctrl+Y)")
        btn_redo.setFixedWidth(30)
        btn_redo.clicked.connect(lambda: None)  # connected after editor created

        sep2 = QLabel("|")
        sep2.setStyleSheet("color:#45475a;")

        btn_validate = QPushButton("✓ Validate")
        btn_validate.setToolTip("Validate Modelfile syntax")
        btn_validate.clicked.connect(self._on_validate)

        sep3 = QLabel("|")
        sep3.setStyleSheet("color:#45475a;")

        self._model_name_edit = QLineEdit()
        self._model_name_edit.setPlaceholderText("Model name for build…")
        self._model_name_edit.setFixedWidth(200)

        btn_build = QPushButton("⚙ Build")
        btn_build.setObjectName("primaryButton")
        btn_build.setToolTip("Build model from this Modelfile")
        btn_build.clicked.connect(self._on_build)

        self._path_lbl = QLabel("Unsaved")
        self._path_lbl.setObjectName("dimLabel")

        tb.addWidget(btn_new)
        tb.addWidget(btn_open)
        tb.addWidget(btn_save)
        tb.addWidget(btn_save_as)
        tb.addWidget(sep1)
        tb.addWidget(btn_undo)
        tb.addWidget(btn_redo)
        tb.addWidget(sep2)
        tb.addWidget(btn_validate)
        tb.addWidget(sep3)
        tb.addWidget(self._model_name_edit)
        tb.addWidget(btn_build)
        tb.addStretch()
        tb.addWidget(self._path_lbl)

        layout.addWidget(toolbar)

        # Fix undo/redo after editor is created
        btn_undo.clicked.disconnect()
        btn_redo.clicked.disconnect()

        # ── Main content: editor + reference/preview ───────────────────────
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Editor
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)

        self._editor = QPlainTextEdit()
        self._editor.setFont(QFont("JetBrains Mono, Consolas, Courier New", 12))
        self._editor.setStyleSheet(
            "QPlainTextEdit { background:#11111b; color:#cdd6f4; "
            "border:none; padding:10px; line-height:1.5; }"
        )
        self._editor.textChanged.connect(self._on_text_changed)
        self._highlighter = ModelfileHighlighter(self._editor.document())

        btn_undo.clicked.connect(self._editor.undo)
        btn_redo.clicked.connect(self._editor.redo)

        # Line number-like gutter (minimal version)
        editor_layout.addWidget(self._editor)

        # Build progress
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 0)
        self._progress_bar.setFixedHeight(6)
        self._progress_bar.setVisible(False)

        self._build_status = QLabel("")
        self._build_status.setObjectName("dimLabel")
        self._build_status.setVisible(False)

        editor_layout.addWidget(self._progress_bar)
        editor_layout.addWidget(self._build_status)

        splitter.addWidget(editor_widget)

        # Right panel: Reference + Preview tabs
        from PySide6.QtWidgets import QTabWidget
        right_tabs = QTabWidget()
        right_tabs.setStyleSheet("QTabWidget::pane { border:none; }")

        # Reference
        ref_view = QTextEdit()
        ref_view.setReadOnly(True)
        ref_view.setFont(QFont("Consolas, Courier New", 11))
        ref_view.setStyleSheet(
            "background:#11111b; color:#cdd6f4; border:none; padding:10px;"
        )
        ref_view.setPlainText(MODELFILE_REFERENCE)
        right_tabs.addTab(ref_view, "Reference")

        # Preview (raw JSON config from show)
        self._preview = QTextEdit()
        self._preview.setReadOnly(True)
        self._preview.setFont(QFont("Consolas, Courier New", 10))
        self._preview.setStyleSheet(
            "background:#11111b; color:#a6adc8; border:none; padding:10px;"
        )
        self._preview.setPlaceholderText("Model config preview appears here after build.")
        right_tabs.addTab(self._preview, "Config Preview")

        # Version history
        self._history_list = QListWidget()
        self._history_list.setStyleSheet("background:#11111b; border:none; color:#cdd6f4;")
        self._history_list.itemClicked.connect(self._on_history_restore)
        right_tabs.addTab(self._history_list, "History")

        splitter.addWidget(right_tabs)
        splitter.setSizes([600, 320])

        layout.addWidget(splitter, stretch=1)

    # ── Editor state ──────────────────────────────────────────────────────

    def _on_text_changed(self):
        self._modified = True
        self._push_history(self._editor.toPlainText())

    def _push_history(self, content: str):
        # Debounce: only push if different from last
        if self._history and self._history[-1] == content:
            return
        self._history.append(content)
        if len(self._history) > 50:
            self._history.pop(0)
        # Update history list widget
        ts = __import__("datetime").datetime.now().strftime("%H:%M:%S")
        lines = content.count("\n") + 1
        self._history_list.insertItem(0, f"v{len(self._history)}  [{ts}]  {lines} lines")

    def _on_history_restore(self, item: QListWidgetItem):
        row = self._history_list.row(item)
        idx = len(self._history) - 1 - row
        if 0 <= idx < len(self._history):
            self._editor.setPlainText(self._history[idx])

    def _editor_undo(self):
        self._editor.undo()

    # ── File operations ───────────────────────────────────────────────────

    def _on_new(self):
        if self._modified:
            r = QMessageBox.question(
                self, "Unsaved Changes", "Discard changes and create new?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if r != QMessageBox.StandardButton.Yes:
                return
        self._current_path = None
        self._modified = False
        self._editor.setPlainText(DEFAULT_MODELFILE)
        self._path_lbl.setText("Unsaved")

    def _on_open(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Modelfile", "",
            "Modelfile (Modelfile *.modelfile);;All Files (*)"
        )
        if path:
            self.load_file(Path(path))

    def load_file(self, path: Path):
        try:
            content = path.read_text(encoding="utf-8")
            self._editor.setPlainText(content)
            self._current_path = path
            self._modified = False
            self._path_lbl.setText(str(path))
        except Exception as e:
            QMessageBox.critical(self, "Open Failed", str(e))

    def load_modelfile_content(self, content: str, model_name: str = ""):
        self._editor.setPlainText(content)
        self._current_path = None
        self._modified = False
        self._path_lbl.setText(f"[{model_name}]" if model_name else "Loaded")
        if model_name:
            self._model_name_edit.setText(model_name)

    def _on_save(self):
        if self._current_path:
            self._save_to(self._current_path)
        else:
            self._on_save_as()

    def _on_save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Modelfile", "Modelfile",
            "Modelfile (Modelfile);;All Files (*)"
        )
        if path:
            self._save_to(Path(path))

    def _save_to(self, path: Path):
        try:
            path.write_text(self._editor.toPlainText(), encoding="utf-8")
            self._current_path = path
            self._modified = False
            self._path_lbl.setText(str(path))
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", str(e))

    # ── Validate ──────────────────────────────────────────────────────────

    def _on_validate(self):
        content = self._editor.toPlainText()
        errors = self._validate(content)
        if errors:
            QMessageBox.warning(self, "Validation Errors",
                                "\n".join(f"• {e}" for e in errors))
        else:
            QMessageBox.information(self, "Valid", "Modelfile syntax looks valid.")

    def _validate(self, content: str) -> List[str]:
        errors = []
        lines = content.strip().splitlines()
        has_from = False
        valid_directives = {
            "FROM", "SYSTEM", "TEMPLATE", "PARAMETER",
            "ADAPTER", "MESSAGE", "LICENSE",
        }
        valid_parameters = {
            "temperature", "top_k", "top_p", "min_p",
            "repeat_penalty", "repeat_last_n", "mirostat",
            "mirostat_eta", "mirostat_tau", "tfs_z",
            "num_predict", "seed", "stop", "num_ctx",
            "num_batch", "num_gpu",
        }
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            parts = stripped.split(None, 2)
            directive = parts[0].upper()
            if directive == "FROM":
                has_from = True
                if len(parts) < 2:
                    errors.append(f"Line {i}: FROM requires a model name")
            elif directive == "PARAMETER":
                if len(parts) < 3:
                    errors.append(f"Line {i}: PARAMETER requires name and value")
                elif parts[1].lower() not in valid_parameters:
                    errors.append(
                        f"Line {i}: Unknown parameter '{parts[1]}'"
                    )
            elif directive == "MESSAGE":
                if len(parts) < 3:
                    errors.append(f"Line {i}: MESSAGE requires role and content")
                elif parts[1].lower() not in ("user", "assistant", "system", "tool"):
                    errors.append(
                        f"Line {i}: Invalid MESSAGE role '{parts[1]}'"
                    )
            elif directive not in valid_directives:
                errors.append(f"Line {i}: Unknown directive '{directive}'")

        if not has_from:
            errors.append("Missing required FROM directive")
        return errors

    # ── Build ─────────────────────────────────────────────────────────────

    def _on_build(self):
        model_name = self._model_name_edit.text().strip()
        if not model_name:
            QMessageBox.warning(self, "No Model Name",
                                "Enter a model name before building.")
            return

        content = self._editor.toPlainText().strip()
        if not content:
            return

        errors = self._validate(content)
        if errors:
            reply = QMessageBox.question(
                self, "Validation Warnings",
                f"Modelfile has issues:\n" + "\n".join(errors[:5]) +
                "\n\nBuild anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        backend = self.app_state.get_backend()
        if not backend:
            QMessageBox.warning(self, "No Backend", "No backend connected.")
            return

        self._progress_bar.setVisible(True)
        self._build_status.setVisible(True)
        self._build_status.setText(f"Building {model_name}…")

        self._worker = BuildWorker(backend, model_name, content)
        self._worker.progress.connect(self._on_build_progress)
        self._worker.finished.connect(self._on_build_finished)
        self._worker.start()

    def _on_build_progress(self, data: dict):
        self._build_status.setText(data.get("status", "Building…"))

    def _on_build_finished(self, success: bool, message: str):
        self._progress_bar.setVisible(False)
        self._build_status.setVisible(False)
        self._worker = None

        if success:
            model_name = self._model_name_edit.text().strip()
            QMessageBox.information(self, "Build Complete",
                                    f"Model '{model_name}' built successfully.")
            self.build_complete.emit(model_name)
            # Load preview
            try:
                backend = self.app_state.get_backend()
                info = backend.show_model(model_name)
                import json
                self._preview.setPlainText(json.dumps(info, indent=2))
            except Exception:
                pass
        else:
            QMessageBox.critical(self, "Build Failed", f"Error: {message}")
