"""
ChatBubble — widget for a single chat message in the conversation view.
Renders markdown, shows action buttons on hover, supports editing.
"""

import html
import logging
from typing import Callable, Optional

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QColor, QTextCursor
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextBrowser, QSizePolicy, QFrame, QPlainTextEdit,
    QStackedWidget,
)

log = logging.getLogger(__name__)

try:
    import markdown as md_lib
    _MARKDOWN_AVAILABLE = True
except ImportError:
    _MARKDOWN_AVAILABLE = False
    log.warning("markdown package not available; falling back to plain text.")


def _render_markdown(text: str) -> str:
    if _MARKDOWN_AVAILABLE:
        try:
            return md_lib.markdown(
                text,
                extensions=["fenced_code", "tables", "nl2br"],
            )
        except Exception:
            pass
    return f"<pre style='white-space:pre-wrap'>{html.escape(text)}</pre>"


ROLE_COLORS = {
    "user":      "#89b4fa",
    "assistant": "#a6e3a1",
    "system":    "#f9e2af",
    "tool":      "#cba6f7",
}

ROLE_ICONS = {
    "user":      "👤",
    "assistant": "🤖",
    "system":    "⚙️",
    "tool":      "🔧",
}

MESSAGE_CSS = """
<style>
body { font-family: 'Segoe UI', system-ui, sans-serif; color: #cdd6f4; margin: 0; padding: 0; }
p { margin: 0 0 8px 0; line-height: 1.6; }
p:last-child { margin-bottom: 0; }
pre { background: #11111b; border: 1px solid #313244; border-radius: 6px;
      padding: 10px 14px; overflow-x: auto; margin: 8px 0; }
code { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
       font-size: 12px; background: #11111b; padding: 2px 5px;
       border-radius: 3px; color: #cba6f7; }
pre code { background: transparent; padding: 0; color: #cdd6f4; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; }
th { background: #313244; padding: 6px 12px; border: 1px solid #45475a;
     text-align: left; font-weight: 600; }
td { padding: 5px 12px; border: 1px solid #313244; }
tr:nth-child(even) { background: #11111b; }
ul, ol { margin: 4px 0 8px 0; padding-left: 24px; }
li { margin: 3px 0; line-height: 1.5; }
blockquote { border-left: 3px solid #89b4fa; margin: 8px 0;
             padding: 4px 12px; color: #a6adc8; background: #11111b;
             border-radius: 0 4px 4px 0; }
h1, h2, h3, h4 { color: #cdd6f4; margin: 12px 0 6px 0; }
a { color: #89b4fa; }
strong { color: #f5c2e7; }
em { color: #f9e2af; }
hr { border: none; border-top: 1px solid #313244; margin: 12px 0; }
</style>
"""


class ChatBubble(QWidget):
    """One message in the chat view."""

    # Signals for parent to handle
    edit_requested = Signal(str, str)    # message_id, new_content
    delete_requested = Signal(str)       # message_id
    copy_requested = Signal(str)         # content
    regenerate_requested = Signal(str)   # message_id (assistant only)
    retry_requested = Signal(str)        # message_id (user only)

    def __init__(
        self,
        message_id: str,
        role: str,
        content: str,
        model: str = "",
        timestamp: str = "",
        tokens: int = 0,
        duration_ms: int = 0,
        parent=None,
    ):
        super().__init__(parent)
        self.message_id = message_id
        self.role = role
        self._content = content
        self.model = model
        self.timestamp = timestamp
        self.tokens = tokens
        self.duration_ms = duration_ms
        self._editing = False
        self._setup_ui()
        self.set_content(content)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(0)

        # ── Header row ──────────────────────────────────────────────────
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 4)
        header.setSpacing(6)

        icon_lbl = QLabel(ROLE_ICONS.get(self.role, "?"))
        icon_lbl.setFixedWidth(22)

        role_color = ROLE_COLORS.get(self.role, "#cdd6f4")
        role_lbl = QLabel(self.role.upper())
        role_lbl.setStyleSheet(
            f"color: {role_color}; font-weight: 700; font-size: 11px; "
            f"letter-spacing: 0.8px;"
        )

        self._meta_lbl = QLabel()
        self._meta_lbl.setObjectName("dimLabel")
        self._update_meta()

        header.addWidget(icon_lbl)
        header.addWidget(role_lbl)
        header.addWidget(self._meta_lbl)
        header.addStretch()

        # Action buttons (shown on hover)
        self._btn_copy = self._make_action_btn("⧉ Copy", self._on_copy)
        self._btn_edit = self._make_action_btn("✎ Edit", self._on_edit_click)
        self._btn_del  = self._make_action_btn("✕", self._on_delete)
        if self.role == "assistant":
            self._btn_regen = self._make_action_btn("↺ Regen", self._on_regen)
            header.addWidget(self._btn_regen)
        if self.role == "user":
            self._btn_retry = self._make_action_btn("↺ Retry", self._on_retry)
            header.addWidget(self._btn_retry)
        header.addWidget(self._btn_copy)
        header.addWidget(self._btn_edit)
        header.addWidget(self._btn_del)

        self._toggle_action_btns(False)
        layout.addLayout(header)

        # ── Content area ─────────────────────────────────────────────────
        # Stack: view mode (QTextBrowser) / edit mode (QPlainTextEdit)
        self._stack = QStackedWidget()

        self._view = QTextBrowser()
        self._view.setOpenExternalLinks(True)
        self._view.setReadOnly(True)
        self._view.setSizePolicy(QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Minimum)
        self._view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._view.document().setDocumentMargin(0)
        self._view.setStyleSheet("background:transparent; border:none; padding:0;")

        self._editor = QPlainTextEdit()
        self._editor.setPlaceholderText("Edit message…")
        self._editor.setStyleSheet(
            "background:#181825; border:1px solid #313244; border-radius:5px; padding:8px;"
        )

        edit_btns = QHBoxLayout()
        edit_btns.setContentsMargins(0, 4, 0, 0)
        btn_save = QPushButton("Save")
        btn_save.setObjectName("primaryButton")
        btn_cancel = QPushButton("Cancel")
        btn_save.clicked.connect(self._on_edit_save)
        btn_cancel.clicked.connect(self._on_edit_cancel)
        edit_btns.addStretch()
        edit_btns.addWidget(btn_save)
        edit_btns.addWidget(btn_cancel)

        edit_container = QWidget()
        edit_layout = QVBoxLayout(edit_container)
        edit_layout.setContentsMargins(0, 0, 0, 0)
        edit_layout.addWidget(self._editor)
        edit_layout.addLayout(edit_btns)

        self._stack.addWidget(self._view)
        self._stack.addWidget(edit_container)
        layout.addWidget(self._stack)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color:#313244; background:#313244; max-height:1px; margin-top:4px;")
        layout.addWidget(sep)

        # Mouse tracking for hover
        self.setMouseTracking(True)
        self._view.setMouseTracking(True)

    # ── Action buttons ────────────────────────────────────────────────────

    def _make_action_btn(self, label: str, slot: Callable) -> QPushButton:
        btn = QPushButton(label)
        btn.setFixedHeight(22)
        btn.setStyleSheet(
            "QPushButton { background:transparent; color:#6c7086; border:none; "
            "font-size:11px; padding:0 4px; border-radius:3px; } "
            "QPushButton:hover { color:#cdd6f4; background:#313244; }"
        )
        btn.clicked.connect(slot)
        return btn

    def _toggle_action_btns(self, visible: bool):
        self._btn_copy.setVisible(visible)
        self._btn_edit.setVisible(visible)
        self._btn_del.setVisible(visible)
        if hasattr(self, "_btn_regen"):
            self._btn_regen.setVisible(visible)
        if hasattr(self, "_btn_retry"):
            self._btn_retry.setVisible(visible)

    def enterEvent(self, event):
        self._toggle_action_btns(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self._editing:
            self._toggle_action_btns(False)
        super().leaveEvent(event)

    # ── Content ───────────────────────────────────────────────────────────

    def set_content(self, content: str):
        self._content = content
        rendered = MESSAGE_CSS + _render_markdown(content)
        self._view.setHtml(rendered)
        # Auto-size the view
        self._view.document().setTextWidth(self._view.viewport().width())
        doc_h = self._view.document().size().height()
        self._view.setFixedHeight(min(int(doc_h) + 4, 900))

    def append_token(self, token: str):
        """Append a streamed token to the current content."""
        self._content += token
        # Update efficiently — only re-render periodically
        self.set_content(self._content)

    def get_content(self) -> str:
        return self._content

    def _update_meta(self):
        parts = []
        if self.timestamp:
            parts.append(self.timestamp)
        if self.model:
            parts.append(self.model)
        if self.tokens:
            parts.append(f"{self.tokens} tok")
        if self.duration_ms:
            parts.append(f"{self.duration_ms}ms")
        self._meta_lbl.setText("  ·  ".join(parts))

    def update_stats(self, tokens: int = 0, duration_ms: int = 0, model: str = ""):
        self.tokens = tokens
        self.duration_ms = duration_ms
        if model:
            self.model = model
        self._update_meta()

    # ── Edit ──────────────────────────────────────────────────────────────

    def _on_edit_click(self):
        self._editing = True
        self._editor.setPlainText(self._content)
        self._stack.setCurrentIndex(1)

    def _on_edit_save(self):
        new_content = self._editor.toPlainText().strip()
        self._editing = False
        self._stack.setCurrentIndex(0)
        self._toggle_action_btns(False)
        if new_content and new_content != self._content:
            self.edit_requested.emit(self.message_id, new_content)
            self.set_content(new_content)

    def _on_edit_cancel(self):
        self._editing = False
        self._stack.setCurrentIndex(0)
        self._toggle_action_btns(False)

    # ── Slots ─────────────────────────────────────────────────────────────

    def _on_copy(self):
        self.copy_requested.emit(self._content)

    def _on_delete(self):
        self.delete_requested.emit(self.message_id)

    def _on_regen(self):
        self.regenerate_requested.emit(self.message_id)

    def _on_retry(self):
        self.retry_requested.emit(self.message_id)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._content:
            self._view.document().setTextWidth(self._view.viewport().width())
            doc_h = self._view.document().size().height()
            self._view.setFixedHeight(min(int(doc_h) + 4, 900))
