from __future__ import annotations

import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import psutil
from PySide6.QtCore import QByteArray, Qt, Signal
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDockWidget,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from locallama_gui.backends.manager import create_backend
from locallama_gui.backends.ollama import OllamaBackend
from locallama_gui.core.config import APP_SYSTEM_PROMPT, AppConfig
from locallama_gui.core.domain import ChatMessage, ChatSession, ModelInfo
from locallama_gui.core.managers import (
    AgentManager,
    PluginContext,
    PluginManager,
    PromptManager,
    SessionManager,
)
from locallama_gui.ui.chat_view import (
    assistant_label,
    compute_scroll_restore_plan,
    redacted_request_messages,
    visible_chat_messages,
)
from locallama_gui.ui.controllers import ChatController, ModelController, PluginController
from locallama_gui.ui.diagnostics import (
    DiagnosticsSignals,
    LineBufferedStream,
    OperationStreamParser,
    OperationUpdate,
    QtLogHandler,
    append_output,
)
from locallama_gui.ui.dialogs import (
    AgentBuilderDialog,
    EndpointDialog,
    ModelfileEditor,
    ParameterDialog,
    PluginManagerDialog,
    PromptManagerDialog,
)
from locallama_gui.ui.theme import DARK_QSS, dark_qss
from locallama_gui.ui.workers import AsyncTask, StreamTask

LOG = logging.getLogger(__name__)


def _build_readonly_table_item(value: str) -> QTableWidgetItem:
    item = QTableWidgetItem(value)
    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    return item


class ChatTab(QWidget):
    def __init__(self, session: ChatSession) -> None:
        super().__init__()
        self.session = session
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.input = ComposerTextEdit()
        self.input.setPlaceholderText("Write a message. Press Ctrl+Enter (or Ctrl+Return) to send.")
        self.input.setMaximumHeight(140)
        self.streaming = QCheckBox("Stream")
        self.streaming.setChecked(True)
        self.send = QPushButton("Send")
        self.stop = QPushButton("Stop")
        self.regen = QPushButton("Regenerate")
        self.retry = QPushButton("Retry")
        self.copy_last = QPushButton("Copy Last")
        self.edit_msg = QPushButton("Edit Message")
        self.delete_msg = QPushButton("Delete Message")
        row = QHBoxLayout()
        row.addWidget(self.streaming)
        row.addStretch()
        row.addWidget(self.copy_last)
        row.addWidget(self.edit_msg)
        row.addWidget(self.delete_msg)
        row.addWidget(self.retry)
        row.addWidget(self.regen)
        row.addWidget(self.stop)
        row.addWidget(self.send)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(self.chat)
        layout.addWidget(self.input)
        layout.addLayout(row)
        self.render()
        self.set_generating(False)

    def render(self, active_model: str = "") -> None:
        scroll = self.chat.verticalScrollBar()
        plan = compute_scroll_restore_plan(scroll.value(), scroll.maximum())
        palette = QApplication.palette()
        base_color = palette.base().color().name()
        text_color = palette.text().color().name()
        html = []
        colors = {"system": "#8fbcbb", "user": "#a3be8c", "assistant": "#81a1c1", "tool": "#d08770"}
        for idx, msg in enumerate(visible_chat_messages(self.session.messages)):
            safe = (
                msg.content.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "<br>")
            )
            html.append(
                f"<div style='margin:10px 0;padding:10px;border-left:3px solid {colors.get(msg.role, '#ccc')};background:{base_color};color:{text_color};border-radius:6px'><b>{idx + 1}. {assistant_label(msg, active_model)}</b><br>{safe}</div>"
            )
        self.chat.setHtml("".join(html))
        if plan.should_pin_bottom:
            scroll.setValue(scroll.maximum())
        else:
            scroll.setValue(min(plan.previous_value, scroll.maximum()))

    def set_generating(self, generating: bool) -> None:
        self.send.setEnabled(not generating)
        self.stop.setEnabled(generating)
        self.retry.setEnabled(not generating)
        self.regen.setEnabled(not generating)
        self.input.setReadOnly(generating)


class ComposerTextEdit(QPlainTextEdit):
    send_requested = Signal()
    zoom_requested = Signal(int)

    def keyPressEvent(self, event) -> None:
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.send_requested.emit()
                event.accept()
                return
            if event.key() in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
                self.zoom_requested.emit(1)
                event.accept()
                return
            if event.key() == Qt.Key.Key_Minus:
                self.zoom_requested.emit(-1)
                event.accept()
                return
            if event.key() == Qt.Key.Key_0:
                self.zoom_requested.emit(0)
                event.accept()
                return
        super().keyPressEvent(event)

    def wheelEvent(self, event) -> None:
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta:
                self.zoom_requested.emit(1 if delta > 0 else -1)
                event.accept()
                return
        super().wheelEvent(event)


class MainWindow(QMainWindow):
