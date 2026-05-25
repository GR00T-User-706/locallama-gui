"""Log Panel — real-time application log viewer with filtering."""

import logging
from PySide6.QtCore import Qt, Signal, QObject, Slot
from PySide6.QtGui import QColor, QTextCharFormat, QFont, QTextCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QComboBox, QCheckBox, QLabel, QFileDialog,
)
from app.core.app_logger import get_memory_handler


LEVEL_COLORS = {
    logging.DEBUG:    "#6c7086",
    logging.INFO:     "#cdd6f4",
    logging.WARNING:  "#f9e2af",
    logging.ERROR:    "#f38ba8",
    logging.CRITICAL: "#f38ba8",
}

LEVEL_LABELS = {
    logging.DEBUG:    "DEBUG",
    logging.INFO:     "INFO",
    logging.WARNING:  "WARN",
    logging.ERROR:    "ERROR",
    logging.CRITICAL: "CRIT",
}


class LogSignalBridge(QObject):
    """Bridge between the logging thread and Qt main thread."""
    new_record = Signal(object)


class LogPanel(QWidget):
    """Real-time log viewer panel."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._min_level = logging.DEBUG
        self._auto_scroll = True
        self._bridge = LogSignalBridge()
        self._bridge.new_record.connect(self._append_record)
        self._setup_ui()
        self._connect_handler()
        self._load_existing()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QWidget()
        toolbar.setStyleSheet("background:#181825; border-bottom:1px solid #313244;")
        toolbar.setFixedHeight(38)
        tb = QHBoxLayout(toolbar)
        tb.setContentsMargins(8, 4, 8, 4)
        tb.setSpacing(6)

        lbl = QLabel("Level:")
        lbl.setObjectName("dimLabel")
        self._level_combo = QComboBox()
        self._level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self._level_combo.setCurrentText("DEBUG")
        self._level_combo.setFixedWidth(90)
        self._level_combo.currentTextChanged.connect(self._on_level_changed)

        self._auto_scroll_chk = QCheckBox("Auto-scroll")
        self._auto_scroll_chk.setChecked(True)
        self._auto_scroll_chk.toggled.connect(lambda v: setattr(self, "_auto_scroll", v))

        btn_clear = QPushButton("⌫ Clear")
        btn_clear.clicked.connect(self._on_clear)
        btn_save = QPushButton("⇓ Save…")
        btn_save.clicked.connect(self._on_save)

        self._count_lbl = QLabel("0 lines")
        self._count_lbl.setObjectName("dimLabel")

        tb.addWidget(lbl)
        tb.addWidget(self._level_combo)
        tb.addWidget(self._auto_scroll_chk)
        tb.addStretch()
        tb.addWidget(self._count_lbl)
        tb.addWidget(btn_clear)
        tb.addWidget(btn_save)

        layout.addWidget(toolbar)

        self._view = QTextEdit()
        self._view.setReadOnly(True)
        self._view.setFont(QFont("JetBrains Mono, Consolas, Courier New", 11))
        self._view.setStyleSheet(
            "QTextEdit { background:#11111b; color:#cdd6f4; border:none; padding:6px; }"
        )
        layout.addWidget(self._view, stretch=1)

        self._line_count = 0

    def _connect_handler(self):
        mem = get_memory_handler()
        mem.add_listener(self._on_log_record)

    def _on_log_record(self, record: logging.LogRecord):
        """Called from any thread — bridge to main thread via signal."""
        try:
            self._bridge.new_record.emit(record)
        except Exception:
            pass

    @Slot(object)
    def _append_record(self, record: logging.LogRecord):
        if record.levelno < self._min_level:
            return
        self._write_record(record)

    def _write_record(self, record: logging.LogRecord):
        color = LEVEL_COLORS.get(record.levelno, "#cdd6f4")
        level_str = LEVEL_LABELS.get(record.levelno, record.levelname)
        name_short = record.name.split(".")[-1][:20]
        try:
            msg = record.getMessage()
        except Exception:
            msg = str(record.msg)

        line = (
            f'<span style="color:#6c7086">'
            f'{record.asctime if hasattr(record, "asctime") else ""}'
            f'</span> '
            f'<span style="color:{color};font-weight:600">[{level_str}]</span> '
            f'<span style="color:#89b4fa">{name_short}</span> '
            f'<span style="color:{color}">{self._escape(msg)}</span>'
        )

        cursor = self._view.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self._view.setTextCursor(cursor)
        self._view.insertHtml(line + "<br>")

        self._line_count += 1
        self._count_lbl.setText(f"{self._line_count} lines")

        if self._auto_scroll:
            sb = self._view.verticalScrollBar()
            sb.setValue(sb.maximum())

    def _load_existing(self):
        """Load records already in the memory handler."""
        mem = get_memory_handler()
        for record in mem.get_records():
            try:
                logging.Formatter("%(asctime)s").format(record)
            except Exception:
                pass
            self._write_record(record)

    @staticmethod
    def _escape(text: str) -> str:
        return (text.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace("\n", "<br>"))

    def _on_level_changed(self, level_name: str):
        levels = {"DEBUG": logging.DEBUG, "INFO": logging.INFO,
                  "WARNING": logging.WARNING, "ERROR": logging.ERROR}
        self._min_level = levels.get(level_name, logging.DEBUG)

    def _on_clear(self):
        self._view.clear()
        self._line_count = 0
        self._count_lbl.setText("0 lines")
        get_memory_handler().clear()

    def _on_save(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Logs", "llm_studio.log", "Log Files (*.log);;Text (*.txt)"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self._view.toPlainText())
            except Exception as e:
                logging.getLogger(__name__).error("Failed to save logs: %s", e)
