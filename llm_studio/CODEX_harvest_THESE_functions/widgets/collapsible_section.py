"""Collapsible section widget for parameter panels."""

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QSizePolicy,
)


class CollapsibleSection(QWidget):
    """A titled section that can be collapsed/expanded."""

    def __init__(self, title: str, parent=None, collapsed: bool = False):
        super().__init__(parent)
        self._collapsed = collapsed
        self._setup_ui(title)

    def _setup_ui(self, title: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QPushButton(f"▾  {title}")
        header.setCheckable(True)
        header.setChecked(not self._collapsed)
        header.setStyleSheet(
            "QPushButton { background:#252535; color:#a6adc8; border:none; "
            "border-radius:4px; padding:6px 10px; text-align:left; "
            "font-weight:600; font-size:11px; letter-spacing:0.5px; } "
            "QPushButton:hover { background:#313244; } "
            "QPushButton:checked { color:#cdd6f4; }"
        )
        header.clicked.connect(self._toggle)

        # Content widget
        self._content = QWidget()
        self._content.setSizePolicy(QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Minimum)

        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(4, 4, 4, 4)
        self._content_layout.setSpacing(6)

        if self._collapsed:
            self._content.setVisible(False)
            header.setChecked(False)
            header.setText(header.text().replace("▾", "▸"))

        self._header_btn = header
        layout.addWidget(header)
        layout.addWidget(self._content)

    def _toggle(self):
        self._collapsed = not self._collapsed
        self._content.setVisible(not self._collapsed)
        arrow = "▸" if self._collapsed else "▾"
        text = self._header_btn.text()
        # Replace arrow character
        if len(text) > 2:
            self._header_btn.setText(f"{arrow}  {text[3:]}")

    def add_widget(self, widget: QWidget):
        self._content_layout.addWidget(widget)

    def add_layout(self, layout):
        self._content_layout.addLayout(layout)

    def content_layout(self):
        return self._content_layout
