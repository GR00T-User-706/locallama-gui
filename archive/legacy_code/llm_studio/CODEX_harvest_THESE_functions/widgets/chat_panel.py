"""
ChatPanel — multi-tab chat interface with full streaming support.

Architecture:
  ChatPanel
    └── QTabWidget
          └── ChatTab (one per session)
                ├── toolbar (streaming toggle, model selector, actions)
                ├── QScrollArea → QVBoxLayout → [ChatBubble, ...]
                └── input area (QPlainTextEdit + send/stop buttons)

Threading:
  ChatStreamWorker(QThread) performs the blocking HTTP stream call
  and emits token_received(str) / stream_finished(dict) / stream_error(str)
  back to the main thread via Qt signals.
"""

import logging
from datetime import datetime
from typing import Dict, Optional

from PySide6.QtCore import Qt, Signal, QThread, QTimer, QObject
from PySide6.QtGui import QKeySequence, QShortcut, QClipboard, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton,
    QPlainTextEdit, QScrollArea, QLabel, QComboBox, QToolButton,
    QCheckBox, QSizePolicy, QSpacerItem, QFrame, QApplication,
    QSplitter, QFileDialog, QMessageBox,
)

from app.models.chat_message import ChatMessage
from app.models.session import ChatSession
from app.ui.widgets.chat_bubble import ChatBubble

log = logging.getLogger(__name__)


# ── Worker thread for streaming ────────────────────────────────────────────────

class ChatStreamWorker(QThread):
    token_received = Signal(str)
    stream_finished = Signal(dict)   # stats dict
    stream_error = Signal(str)

    def __init__(self, backend, messages, model, params, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.messages = messages
        self.model = model
        self.params = params
        self._stop_flag = False

    def request_stop(self):
        self._stop_flag = True

    def run(self):
        import time
        t0 = time.time()
        try:
            for token in self.backend.stream_chat(
                    self.messages, self.model, self.params):
                if self._stop_flag:
                    break
                self.token_received.emit(token)
            elapsed = int((time.time() - t0) * 1000)
            self.stream_finished.emit({"duration_ms": elapsed})
        except Exception as e:
            self.stream_error.emit(str(e))


class ChatNonStreamWorker(QThread):
    response_ready = Signal(dict)
    request_error = Signal(str)

    def __init__(self, backend, messages, model, params, parent=None):
        super().__init__(parent)
        self.backend = backend
        self.messages = messages
        self.model = model
        self.params = params

    def run(self):
        try:
            result = self.backend.chat(self.messages, self.model, self.params)
            self.response_ready.emit(result)
        except Exception as e:
            self.request_error.emit(str(e))


# ── Single chat tab ────────────────────────────────────────────────────────────

class ChatTab(QWidget):
    """Represents one open chat session."""

    session_changed = Signal(str)   # session_id — emitted when title/messages change

    def __init__(self, session: ChatSession, app_state, parent=None):
        super().__init__(parent)
        self.session = session
        self.app_state = app_state   # AppState / main controller
        self._bubbles: Dict[str, ChatBubble] = {}
        self._stream_worker: Optional[ChatStreamWorker] = None
        self._current_stream_bubble: Optional[ChatBubble] = None
        self._streaming_content = ""
        self._generating = False
        self._setup_ui()
        self._reload_messages()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Toolbar ───────────────────────────────────────────────────────
        toolbar = QWidget()
        toolbar.setObjectName("chatToolbar")
        toolbar.setStyleSheet(
            "QWidget#chatToolbar { background:#181825; border-bottom:1px solid #313244; }"
        )
        toolbar.setFixedHeight(42)
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(8, 4, 8, 4)
        tb_layout.setSpacing(6)

        # Model selector
        model_lbl = QLabel("Model:")
        model_lbl.setObjectName("dimLabel")
        self._model_combo = QComboBox()
        self._model_combo.setFixedWidth(220)
        self._model_combo.setToolTip("Select model for this chat")
        self._populate_models()
        self._model_combo.currentTextChanged.connect(self._on_model_changed)

        # Streaming toggle
        self._stream_chk = QCheckBox("Stream")
        self._stream_chk.setChecked(self.app_state.config.streaming_enabled)
        self._stream_chk.setToolTip("Enable streaming token output")
        self._stream_chk.toggled.connect(
            lambda v: setattr(self.app_state.config, "streaming_enabled", v)
        )

        # Reasoning mode
        mode_lbl = QLabel("Mode:")
        mode_lbl.setObjectName("dimLabel")
        self._mode_combo = QComboBox()
        self._mode_combo.addItems(["Normal", "Thinking", "Plan"])
        self._mode_combo.setFixedWidth(100)
        current_mode = self.app_state.config.get("reasoning_mode", "normal").capitalize()
        idx = self._mode_combo.findText(current_mode)
        if idx >= 0:
            self._mode_combo.setCurrentIndex(idx)

        # System prompt indicator
        sys_lbl = QLabel("⚙")
        sys_lbl.setToolTip(f"System: {self.session.system_prompt[:60]}..."
                           if self.session.system_prompt else "No system prompt")
        sys_lbl.setStyleSheet("color:#f9e2af; font-size:14px; padding:0 4px;")

        # Actions
        btn_clear = QPushButton("⌫ Clear")
        btn_clear.setToolTip("Clear chat history")
        btn_clear.clicked.connect(self._on_clear)

        btn_export = QPushButton("⇓ Export")
        btn_export.setToolTip("Export this chat")
        btn_export.clicked.connect(self._on_export)

        btn_dupe = QPushButton("⧉ Fork")
        btn_dupe.setToolTip("Duplicate this session")
        btn_dupe.clicked.connect(self._on_fork)

        tb_layout.addWidget(model_lbl)
        tb_layout.addWidget(self._model_combo)
        tb_layout.addWidget(QFrame())  # spacer via Frame (invisible sep)
        tb_layout.addWidget(mode_lbl)
        tb_layout.addWidget(self._mode_combo)
        tb_layout.addWidget(self._stream_chk)
        tb_layout.addWidget(sys_lbl)
        tb_layout.addStretch()
        tb_layout.addWidget(btn_clear)
        tb_layout.addWidget(btn_export)
        tb_layout.addWidget(btn_dupe)

        layout.addWidget(toolbar)

        # ── Message scroll area ───────────────────────────────────────────
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setStyleSheet("QScrollArea { border:none; }")

        self._msg_container = QWidget()
        self._msg_container.setStyleSheet("background:#1e1e2e;")
        self._msg_layout = QVBoxLayout(self._msg_container)
        self._msg_layout.setContentsMargins(16, 12, 16, 12)
        self._msg_layout.setSpacing(4)
        self._msg_layout.addStretch()   # pushes messages to top

        self._scroll_area.setWidget(self._msg_container)
        layout.addWidget(self._scroll_area, stretch=1)

        # ── Input area ────────────────────────────────────────────────────
        input_widget = QWidget()
        input_widget.setStyleSheet(
            "background:#181825; border-top:1px solid #313244;"
        )
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(12, 8, 12, 10)
        input_layout.setSpacing(6)

        # Status line
        self._status_lbl = QLabel("Ready")
        self._status_lbl.setObjectName("dimLabel")

        # Text input
        self._input = QPlainTextEdit()
        self._input.setPlaceholderText("Type a message…  (Ctrl+Enter to send)")
        self._input.setMaximumHeight(160)
        self._input.setMinimumHeight(64)
        self._input.setStyleSheet(
            "QPlainTextEdit { background:#11111b; border:1px solid #313244; "
            "border-radius:6px; padding:8px; font-size:13px; }"
            "QPlainTextEdit:focus { border-color:#89b4fa; }"
        )

        # Button row
        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 0, 0, 0)
        btn_row.setSpacing(6)

        self._token_lbl = QLabel("")
        self._token_lbl.setObjectName("dimLabel")

        self._btn_stop = QPushButton("⏹ Stop")
        self._btn_stop.setObjectName("dangerButton")
        self._btn_stop.setVisible(False)
        self._btn_stop.clicked.connect(self._on_stop)

        self._btn_send = QPushButton("▶ Send")
        self._btn_send.setObjectName("primaryButton")
        self._btn_send.setFixedWidth(90)
        self._btn_send.clicked.connect(self._on_send)

        btn_row.addWidget(self._status_lbl)
        btn_row.addWidget(self._token_lbl)
        btn_row.addStretch()
        btn_row.addWidget(self._btn_stop)
        btn_row.addWidget(self._btn_send)

        input_layout.addWidget(self._input)
        input_layout.addLayout(btn_row)
        layout.addWidget(input_widget)

        # ── Keyboard shortcuts ────────────────────────────────────────────
        send_sc = QShortcut(QKeySequence("Ctrl+Return"), self)
        send_sc.activated.connect(self._on_send)

    # ── Model management ──────────────────────────────────────────────────

    def _populate_models(self):
        self._model_combo.clear()
        try:
            models = self.app_state.get_model_names()
            self._model_combo.addItems(models)
            # Set current model
            current = self.session.model or self.app_state.config.active_model
            idx = self._model_combo.findText(current)
            if idx >= 0:
                self._model_combo.setCurrentIndex(idx)
        except Exception as e:
            log.debug("Could not populate models: %s", e)

    def refresh_models(self):
        current = self._model_combo.currentText()
        self._model_combo.blockSignals(True)
        self._populate_models()
        idx = self._model_combo.findText(current)
        if idx >= 0:
            self._model_combo.setCurrentIndex(idx)
        self._model_combo.blockSignals(False)

    def _on_model_changed(self, model_name: str):
        self.session.model = model_name
        self.app_state.session_manager.save_session(self.session)

    # ── Message rendering ─────────────────────────────────────────────────

    def _reload_messages(self):
        """Re-render all messages in the session."""
        # Remove all bubble widgets
        for bubble in self._bubbles.values():
            bubble.setParent(None)
        self._bubbles.clear()
        # Remove non-stretch items
        while self._msg_layout.count() > 1:
            item = self._msg_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for msg in self.session.messages:
            self._add_bubble(msg)

    def _add_bubble(self, msg: ChatMessage) -> ChatBubble:
        ts = msg.timestamp.strftime("%H:%M")
        bubble = ChatBubble(
            message_id=msg.id,
            role=msg.role,
            content=msg.content,
            model=msg.model,
            timestamp=ts,
            tokens=msg.tokens,
            duration_ms=msg.duration_ms,
        )
        bubble.edit_requested.connect(self._on_bubble_edit)
        bubble.delete_requested.connect(self._on_bubble_delete)
        bubble.copy_requested.connect(self._on_bubble_copy)
        bubble.regenerate_requested.connect(self._on_regen)
        bubble.retry_requested.connect(self._on_retry)

        # Insert before the stretch (last item)
        count = self._msg_layout.count()
        self._msg_layout.insertWidget(count - 1, bubble)
        self._bubbles[msg.id] = bubble
        self._scroll_to_bottom()
        return bubble

    def _scroll_to_bottom(self):
        QTimer.singleShot(50, lambda: self._scroll_area.verticalScrollBar().setValue(
            self._scroll_area.verticalScrollBar().maximum()
        ))

    # ── Send / Stop / Generate ────────────────────────────────────────────

    def _on_send(self):
        text = self._input.toPlainText().strip()
        if not text or self._generating:
            return

        model = self._model_combo.currentText()
        if not model:
            self._set_status("⚠ No model selected", error=True)
            return

        self._input.clear()

        # Add user message
        user_msg = ChatMessage(role="user", content=text)
        self.session.add_message(user_msg)
        self.app_state.session_manager.save_session(self.session)
        self._add_bubble(user_msg)

        # Prepare assistant placeholder
        asst_msg = ChatMessage(role="assistant", content="", model=model)
        self.session.add_message(asst_msg)
        self.app_state.session_manager.save_session(self.session)
        asst_bubble = self._add_bubble(asst_msg)

        self._current_stream_bubble = asst_bubble
        self._streaming_content = ""
        self._generating = True
        self._set_generating(True)
        self.session_changed.emit(self.session.id)

        # Build API messages
        api_messages = self.session.get_api_messages()
        # Remove the empty assistant message (last one) — backend adds it
        api_messages = api_messages[:-1]

        params = {**self.app_state.config.parameters,
                  **self.session.parameters}
        # Inject reasoning mode
        mode = self._mode_combo.currentText().lower()
        if mode == "thinking":
            params["thinking"] = True

        backend = self.app_state.get_backend()
        if backend is None:
            self._set_status("⚠ No backend connected", error=True)
            self._set_generating(False)
            return

        if self._stream_chk.isChecked():
            self._stream_worker = ChatStreamWorker(
                backend, api_messages, model, params, parent=self
            )
            self._stream_worker.token_received.connect(self._on_token)
            self._stream_worker.stream_finished.connect(self._on_stream_done)
            self._stream_worker.stream_error.connect(self._on_stream_error)
            self._stream_worker.start()
        else:
            self._ns_worker = ChatNonStreamWorker(
                backend, api_messages, model, params, parent=self
            )
            self._ns_worker.response_ready.connect(self._on_nonstream_done)
            self._ns_worker.request_error.connect(self._on_stream_error)
            self._ns_worker.start()

    def _on_stop(self):
        if self._stream_worker and self._stream_worker.isRunning():
            self._stream_worker.request_stop()
        self._finalize_stream()

    def _on_token(self, token: str):
        self._streaming_content += token
        if self._current_stream_bubble:
            self._current_stream_bubble.append_token(token)
        self._scroll_to_bottom()
        # Show token count estimate
        approx_tokens = len(self._streaming_content) // 4
        self._token_lbl.setText(f"~{approx_tokens} tokens")

    def _on_stream_done(self, stats: dict):
        # Update the last assistant message with final content and stats
        for msg in reversed(self.session.messages):
            if msg.role == "assistant" and not msg.content:
                msg.content = self._streaming_content
                msg.duration_ms = stats.get("duration_ms", 0)
                break
            elif msg.role == "assistant":
                msg.content = self._streaming_content
                msg.duration_ms = stats.get("duration_ms", 0)
                break

        if self._current_stream_bubble:
            self._current_stream_bubble.update_stats(
                duration_ms=stats.get("duration_ms", 0)
            )

        self.app_state.session_manager.save_session(self.session)
        self._finalize_stream()
        self.session_changed.emit(self.session.id)

    def _on_nonstream_done(self, result: dict):
        content = result.get("content", "")
        usage = result.get("usage", {})

        for msg in reversed(self.session.messages):
            if msg.role == "assistant":
                msg.content = content
                msg.tokens = usage.get("completion_tokens", 0)
                msg.duration_ms = usage.get("total_duration_ms", 0)
                break

        if self._current_stream_bubble:
            self._current_stream_bubble.set_content(content)
            self._current_stream_bubble.update_stats(
                tokens=usage.get("completion_tokens", 0),
                duration_ms=usage.get("total_duration_ms", 0),
            )

        self.app_state.session_manager.save_session(self.session)
        self._finalize_stream()
        self.session_changed.emit(self.session.id)

    def _on_stream_error(self, error: str):
        log.error("Stream error: %s", error)
        self._set_status(f"⚠ Error: {error}", error=True)
        if self._current_stream_bubble:
            self._current_stream_bubble.set_content(
                f"**Error:** {error}"
            )
        self._finalize_stream()

    def _finalize_stream(self):
        self._generating = False
        self._current_stream_bubble = None
        self._streaming_content = ""
        self._set_generating(False)
        self._stream_worker = None
        self._scroll_to_bottom()

    def _set_generating(self, generating: bool):
        self._btn_send.setEnabled(not generating)
        self._btn_stop.setVisible(generating)
        self._input.setReadOnly(generating)
        if generating:
            self._set_status("Generating…")
        else:
            self._set_status("Ready")
            self._token_lbl.setText("")

    def _set_status(self, text: str, error: bool = False):
        self._status_lbl.setText(text)
        color = "#f38ba8" if error else "#6c7086"
        self._status_lbl.setStyleSheet(f"color:{color}; font-size:11px;")

    # ── Bubble actions ────────────────────────────────────────────────────

    def _on_bubble_edit(self, message_id: str, new_content: str):
        self.app_state.session_manager.update_message(
            self.session.id, message_id, new_content
        )
        # Reload session from manager
        updated = self.app_state.session_manager.get(self.session.id)
        if updated:
            self.session = updated

    def _on_bubble_delete(self, message_id: str):
        self.app_state.session_manager.delete_message(self.session.id, message_id)
        bubble = self._bubbles.pop(message_id, None)
        if bubble:
            bubble.setParent(None)
            bubble.deleteLater()
        updated = self.app_state.session_manager.get(self.session.id)
        if updated:
            self.session = updated

    def _on_bubble_copy(self, content: str):
        QApplication.clipboard().setText(content)

    def _on_regen(self, message_id: str):
        """Regenerate the last assistant response."""
        if self._generating:
            return
        # Remove last assistant message and regenerate
        self.session.messages = [
            m for m in self.session.messages if m.id != message_id
        ]
        bubble = self._bubbles.pop(message_id, None)
        if bubble:
            bubble.setParent(None)
            bubble.deleteLater()
        self.app_state.session_manager.save_session(self.session)
        # Trigger generation by calling internal generate
        self._trigger_generation()

    def _on_retry(self, message_id: str):
        """Resend from the user message with given id."""
        if self._generating:
            return
        # Keep messages up to and including this user message
        idx = next((i for i, m in enumerate(self.session.messages)
                    if m.id == message_id), None)
        if idx is None:
            return
        # Remove all after this message
        msgs_to_remove = self.session.messages[idx + 1:]
        self.session.messages = self.session.messages[:idx + 1]
        for m in msgs_to_remove:
            bubble = self._bubbles.pop(m.id, None)
            if bubble:
                bubble.setParent(None)
                bubble.deleteLater()
        self.app_state.session_manager.save_session(self.session)
        self._trigger_generation()

    def _trigger_generation(self):
        """Generate assistant response for the current session messages."""
        model = self._model_combo.currentText()
        if not model:
            return

        asst_msg = ChatMessage(role="assistant", content="", model=model)
        self.session.add_message(asst_msg)
        self.app_state.session_manager.save_session(self.session)
        asst_bubble = self._add_bubble(asst_msg)

        self._current_stream_bubble = asst_bubble
        self._streaming_content = ""
        self._generating = True
        self._set_generating(True)

        api_messages = self.session.get_api_messages()[:-1]
        params = {**self.app_state.config.parameters, **self.session.parameters}
        backend = self.app_state.get_backend()
        if not backend:
            return

        if self._stream_chk.isChecked():
            self._stream_worker = ChatStreamWorker(
                backend, api_messages, model, params, parent=self
            )
            self._stream_worker.token_received.connect(self._on_token)
            self._stream_worker.stream_finished.connect(self._on_stream_done)
            self._stream_worker.stream_error.connect(self._on_stream_error)
            self._stream_worker.start()
        else:
            self._ns_worker = ChatNonStreamWorker(
                backend, api_messages, model, params, parent=self
            )
            self._ns_worker.response_ready.connect(self._on_nonstream_done)
            self._ns_worker.request_error.connect(self._on_stream_error)
            self._ns_worker.start()

    # ── Clear / Export / Fork ─────────────────────────────────────────────

    def _on_clear(self):
        if QMessageBox.question(
            self, "Clear Chat", "Clear all messages in this chat?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self.session.messages.clear()
            self.app_state.session_manager.save_session(self.session)
            self._reload_messages()

    def _on_export(self):
        path, fmt_filter = QFileDialog.getSaveFileName(
            self, "Export Chat", f"{self.session.title}",
            "Markdown (*.md);;JSON (*.json);;Text (*.txt)",
        )
        if path:
            fmt = "markdown" if path.endswith(".md") else \
                  "json" if path.endswith(".json") else "txt"
            from pathlib import Path
            ok = self.app_state.session_manager.export_session(
                self.session.id, Path(path), fmt
            )
            if not ok:
                QMessageBox.warning(self, "Export Failed", "Could not export chat.")

    def _on_fork(self):
        new_s = self.app_state.session_manager.duplicate_session(self.session.id)
        if new_s:
            # Signal the chat panel to open the new session
            self.parent().parent().open_session(new_s)

    def set_system_prompt(self, prompt: str):
        self.session.system_prompt = prompt
        self.app_state.session_manager.save_session(self.session)


# ── Chat Panel (tab manager) ───────────────────────────────────────────────────

class ChatPanel(QWidget):
    """Hosts multiple ChatTabs in a QTabWidget."""

    status_message = Signal(str)

    def __init__(self, app_state, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self._tabs: Dict[str, ChatTab] = {}  # session_id → ChatTab
        self._setup_ui()
        self._restore_sessions()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._tab_widget = QTabWidget()
        self._tab_widget.setTabsClosable(True)
        self._tab_widget.setMovable(True)
        self._tab_widget.setDocumentMode(True)
        self._tab_widget.tabCloseRequested.connect(self._on_tab_close)
        self._tab_widget.currentChanged.connect(self._on_tab_changed)

        # New chat button in tab bar
        new_btn = QPushButton("+")
        new_btn.setFixedSize(28, 28)
        new_btn.setToolTip("New Chat (Ctrl+N)")
        new_btn.setStyleSheet(
            "QPushButton { background:#313244; border:none; border-radius:4px; "
            "color:#cdd6f4; font-size:16px; font-weight:700; } "
            "QPushButton:hover { background:#45475a; }"
        )
        new_btn.clicked.connect(self.new_chat)
        self._tab_widget.setCornerWidget(new_btn, Qt.Corner.TopRightCorner)

        layout.addWidget(self._tab_widget)

    def _restore_sessions(self):
        sessions = self.app_state.session_manager.list_sessions()
        if sessions:
            # Show only last 10 sessions to avoid overwhelming
            for s in sessions[:10]:
                self._open_session_tab(s, switch=False)
            self._tab_widget.setCurrentIndex(0)
        else:
            self.new_chat()

    def new_chat(self, model: str = "", system_prompt: str = "") -> ChatTab:
        model = model or self.app_state.config.active_model
        session = self.app_state.session_manager.new_session(
            model=model,
            backend=self.app_state.config.active_backend,
            system_prompt=system_prompt,
        )
        return self._open_session_tab(session, switch=True)

    def open_session(self, session: ChatSession) -> ChatTab:
        if session.id in self._tabs:
            idx = self._find_tab_index(session.id)
            if idx >= 0:
                self._tab_widget.setCurrentIndex(idx)
            return self._tabs[session.id]
        return self._open_session_tab(session, switch=True)

    def _open_session_tab(self, session: ChatSession,
                           switch: bool = True) -> ChatTab:
        tab = ChatTab(session, self.app_state, parent=self)
        tab.session_changed.connect(self._on_session_changed)
        self._tabs[session.id] = tab
        title = session.title[:22] + "…" if len(session.title) > 22 else session.title
        idx = self._tab_widget.addTab(tab, title)
        if switch:
            self._tab_widget.setCurrentIndex(idx)
        return tab

    def _find_tab_index(self, session_id: str) -> int:
        for i in range(self._tab_widget.count()):
            w = self._tab_widget.widget(i)
            if isinstance(w, ChatTab) and w.session.id == session_id:
                return i
        return -1

    def _on_tab_close(self, index: int):
        tab = self._tab_widget.widget(index)
        if isinstance(tab, ChatTab):
            self._tabs.pop(tab.session.id, None)
        self._tab_widget.removeTab(index)
        if self._tab_widget.count() == 0:
            self.new_chat()

    def _on_tab_changed(self, index: int):
        tab = self._tab_widget.widget(index)
        if isinstance(tab, ChatTab):
            self.status_message.emit(
                f"Session: {tab.session.title}  |  "
                f"Model: {tab.session.model or 'none'}"
            )

    def _on_session_changed(self, session_id: str):
        idx = self._find_tab_index(session_id)
        if idx >= 0:
            tab = self._tab_widget.widget(idx)
            if isinstance(tab, ChatTab):
                title = tab.session.title
                short = title[:22] + "…" if len(title) > 22 else title
                self._tab_widget.setTabText(idx, short)

    def current_tab(self) -> Optional[ChatTab]:
        w = self._tab_widget.currentWidget()
        return w if isinstance(w, ChatTab) else None

    def current_session(self) -> Optional[ChatSession]:
        tab = self.current_tab()
        return tab.session if tab else None

    def refresh_all_model_lists(self):
        for tab in self._tabs.values():
            tab.refresh_models()

    def set_system_prompt_for_current(self, prompt: str):
        tab = self.current_tab()
        if tab:
            tab.set_system_prompt(prompt)
