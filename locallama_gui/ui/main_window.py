from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any
from dataclasses import asdict

import psutil
from PySide6.QtCore import QByteArray, Qt
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
    QPushButton,
    QSplitter,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from locallama_gui.backends.manager import create_backend
from locallama_gui.core.config import AppConfig
from locallama_gui.core.domain import ChatMessage, ChatSession, ModelInfo
from locallama_gui.core.managers import AgentManager, PluginContext, PluginManager, PromptManager, SessionManager
from locallama_gui.ui.controllers import ChatController, ModelController, PluginController
from locallama_gui.ui.dialogs import AgentBuilderDialog, EndpointDialog, ModelfileEditor, ParameterDialog, PluginManagerDialog, PromptManagerDialog
from locallama_gui.ui.theme import DARK_QSS
from locallama_gui.ui.workers import AsyncTask, StreamTask

LOG = logging.getLogger(__name__)


class ChatTab(QWidget):
    def __init__(self, session: ChatSession) -> None:
        super().__init__()
        self.session = session
        self.chat = QTextEdit(); self.chat.setReadOnly(True)
        self.input = QPlainTextEdit(); self.input.setPlaceholderText("Write a message. Ctrl+Enter sends."); self.input.setMaximumHeight(140)
        self.streaming = QCheckBox("Stream"); self.streaming.setChecked(True)
        self.send = QPushButton("Send"); self.stop = QPushButton("Stop"); self.regen = QPushButton("Regenerate"); self.retry = QPushButton("Retry")
        self.copy_last = QPushButton("Copy Last"); self.edit_msg = QPushButton("Edit Message"); self.delete_msg = QPushButton("Delete Message")
        row = QHBoxLayout(); row.addWidget(self.streaming); row.addStretch(); row.addWidget(self.copy_last); row.addWidget(self.edit_msg); row.addWidget(self.delete_msg); row.addWidget(self.retry); row.addWidget(self.regen); row.addWidget(self.stop); row.addWidget(self.send)
        layout = QVBoxLayout(self); layout.setContentsMargins(6, 6, 6, 6); layout.addWidget(self.chat); layout.addWidget(self.input); layout.addLayout(row)
        self.render()

    def render(self) -> None:
        html = []
        colors = {"system": "#8fbcbb", "user": "#a3be8c", "assistant": "#81a1c1", "tool": "#d08770"}
        for idx, msg in enumerate(self.session.messages):
            safe = msg.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            html.append(f"<div style='margin:8px 0;padding:8px;border-left:3px solid {colors.get(msg.role, '#ccc')};background:#171a21'><b>{idx+1}. {msg.role}</b><br>{safe}</div>")
        self.chat.setHtml("".join(html))
        self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())


class MainWindow(QMainWindow):
    def __init__(self, config: AppConfig) -> None:
        super().__init__()
        self.config = config
        self.setWindowTitle("LocalLama Control Center")
        self.resize(1440, 900)
        self.setStyleSheet(DARK_QSS)
        self.sessions = SessionManager(config)
        self.prompts = PromptManager(config)
        self.agents = AgentManager(config)
        self.plugin_context = PluginContext(self, config)
        self.plugins = PluginManager(config, self.plugin_context)
        self.models: list[ModelInfo] = []
        self.chat_controller = ChatController(self.sessions, self.config, self)
        self.model_controller = ModelController(self.config, self)
        self.plugin_controller = PluginController(self.plugins, self.config, self)
        self.worker_refs: list[Any] = []
        self.current_stream: StreamTask | None = None
        self._build_ui()
        self._build_menus()
        self._restore_state()
        self.plugins.load_enabled()
        self.new_chat()
        self.refresh_backend()

    def _build_ui(self) -> None:
        self.tabs = QTabWidget(); self.tabs.setTabsClosable(True); self.tabs.tabCloseRequested.connect(self.close_tab); self.setCentralWidget(self.tabs)
        self.status = self.statusBar(); self.status.showMessage("Disconnected")
        self.toolbar = QToolBar("Main"); self.addToolBar(self.toolbar)
        for label, slot in [("New Chat", self.new_chat), ("Save", self.save_current), ("Refresh Models", self.refresh_backend), ("Parameters", self.open_parameters), ("Plugins", self.open_plugins)]:
            action = QAction(label, self); action.triggered.connect(slot); self.toolbar.addAction(action)
        self.provider_combo = QComboBox(); self.provider_combo.addItems([p.name for p in self.config.provider_profiles]); self.provider_combo.setCurrentText(self.config.active_provider); self.provider_combo.currentTextChanged.connect(self.switch_provider); self.toolbar.addWidget(QLabel(" Provider ")); self.toolbar.addWidget(self.provider_combo)
        self.model_combo = QComboBox(); self.model_combo.currentTextChanged.connect(self.model_changed); self.toolbar.addWidget(QLabel(" Model ")); self.toolbar.addWidget(self.model_combo)
        self._create_docks()

    def _create_docks(self) -> None:
        self.model_table = QTableWidget(0, 8); self.model_table.setHorizontalHeaderLabels(["Name", "Size", "Quant", "Params", "Ctx", "Backend", "RAM/VRAM", "Metadata"])
        self._dock("Models", self.model_table, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.sessions_list = QListWidget(); self.sessions_list.itemDoubleClicked.connect(lambda item: self.open_session(item.data(Qt.ItemDataRole.UserRole)))
        self._dock("Chat Sessions", self.sessions_list, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.prompt_list = QListWidget(); self.prompt_list.itemDoubleClicked.connect(self.apply_prompt_item); self._dock("System Prompts", self.prompt_list, Qt.DockWidgetArea.RightDockWidgetArea)
        self.log_view = QPlainTextEdit(); self.log_view.setReadOnly(True); self._dock("Logs", self.log_view, Qt.DockWidgetArea.BottomDockWidgetArea)
        self.request_view = QPlainTextEdit(); self.request_view.setReadOnly(True); self._dock("Request Viewer", self.request_view, Qt.DockWidgetArea.BottomDockWidgetArea)
        self.token_view = QPlainTextEdit(); self.token_view.setReadOnly(True); self._dock("Token Viewer", self.token_view, Qt.DockWidgetArea.BottomDockWidgetArea)
        self.terminal = QPlainTextEdit(); self.terminal.setReadOnly(True); self.terminal.setPlainText("LocalLama diagnostics terminal. Menu actions append operational output here.\n"); self._dock("Terminal", self.terminal, Qt.DockWidgetArea.BottomDockWidgetArea)
        self.refresh_sessions(); self.refresh_prompts()

    def _dock(self, title: str, widget: QWidget, area: Qt.DockWidgetArea) -> QDockWidget:
        dock = QDockWidget(title, self); dock.setWidget(widget); dock.setObjectName(title); self.addDockWidget(area, dock); return dock

    def add_plugin_panel(self, title: str, widget: QWidget, area: Any = None) -> None:
        self._dock(title, widget, area or Qt.DockWidgetArea.RightDockWidgetArea)

    def _menu_action(self, menu, text, slot, shortcut: str | None = None):
        action = QAction(text, self)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        menu.addAction(action)
        return action

    def _build_menus(self) -> None:
        self._build_file_menu()
        self._build_models_menu()
        self._build_agents_menu()
        self._build_plugins_menu()
        self._build_settings_menu()
        self._build_view_menu()
        self._build_developer_menu()
        self._build_help_menu()

    def _build_file_menu(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        self._menu_action(file_menu, "New Chat", self.new_chat, "Ctrl+N")
        self._menu_action(file_menu, "Open Chat", lambda: self.chat_controller.open_chat_file(self), "Ctrl+O")
        self._menu_action(file_menu, "Save", self.chat_controller.save_current, "Ctrl+S")
        self._menu_action(file_menu, "Save As", self.save_as)
        self._menu_action(file_menu, "Export", self.export_current)
        self._menu_action(file_menu, "Import", self.import_chat)
        file_menu.addSeparator()
        self._menu_action(file_menu, "Exit", self.close, "Ctrl+Q")

    def _build_models_menu(self) -> None:
        models_menu = self.menuBar().addMenu("Models")
        self._menu_action(models_menu, "Pull", lambda: self.model_controller.pull_model(self))
        self._menu_action(models_menu, "Push", lambda: self.model_controller.push_model(self))
        self._menu_action(models_menu, "Clone", lambda: self.model_controller.clone_model(self))
        self._menu_action(models_menu, "Create", self.model_controller.create_model)
        self._menu_action(models_menu, "Delete", lambda: self.model_controller.delete_model(self))
        self._menu_action(models_menu, "Modelfiles", self.open_modelfile_editor)
        self._menu_action(models_menu, "Templates", self.open_template_viewer)

    def _build_agents_menu(self) -> None:
        agents_menu = self.menuBar().addMenu("Agents")
        self._menu_action(agents_menu, "Create", self.open_agent_builder)
        self._menu_action(agents_menu, "Manage", self.open_agent_builder)
        self._menu_action(agents_menu, "Import", self.import_agent)
        self._menu_action(agents_menu, "Export", self.export_agent)

    def _build_plugins_menu(self) -> None:
        plugins_menu = self.menuBar().addMenu("Plugins")
        self._menu_action(plugins_menu, "Plugin Manager", self.open_plugins)
        self._menu_action(plugins_menu, "Install", lambda: self.plugin_controller.install_plugin(self))
        self._menu_action(plugins_menu, "Reload", self.plugin_controller.reload_plugins)
        self._menu_action(plugins_menu, "Developer Mode", self.open_plugin_docs)

    def _build_settings_menu(self) -> None:
        settings_menu = self.menuBar().addMenu("Settings")
        self._menu_action(settings_menu, "API Endpoints", self.open_endpoints)
        self._menu_action(settings_menu, "Parameters", self.open_parameters)
        self._menu_action(settings_menu, "Themes", self.toggle_theme)
        self._menu_action(settings_menu, "Keyboard Shortcuts", self.show_shortcuts)
        self._menu_action(settings_menu, "Model Settings", self.refresh_backend)

    def _build_view_menu(self) -> None:
        view_menu = self.menuBar().addMenu("View")
        self._menu_action(view_menu, "Toggle Panels", self.toggle_all_docks)
        self._menu_action(view_menu, "Layout Presets", self.reset_layout)
        self._menu_action(view_menu, "Logs", lambda: self.log_view.parent().show())
        self._menu_action(view_menu, "Terminal", lambda: self.terminal.parent().show())

    def _build_developer_menu(self) -> None:
        developer_menu = self.menuBar().addMenu("Developer")
        self._menu_action(developer_menu, "Logs", lambda: self.log_view.parent().show())
        self._menu_action(developer_menu, "Request Viewer", lambda: self.request_view.parent().show())
        self._menu_action(developer_menu, "Token Viewer", lambda: self.token_view.parent().show())
        self._menu_action(developer_menu, "API Inspector", self.inspect_api)
        self._menu_action(developer_menu, "Debug Console", lambda: self.terminal.parent().show())

    def _build_help_menu(self) -> None:
        help_menu = self.menuBar().addMenu("Help")
        self._menu_action(help_menu, "Documentation", self.open_docs)
        self._menu_action(help_menu, "About", self.about)
        self._menu_action(help_menu, "Diagnostics", self.diagnostics)

    def current_tab(self) -> ChatTab | None:
        w = self.tabs.currentWidget(); return w if isinstance(w, ChatTab) else None

    def new_chat(self) -> None:
        session = ChatSession(provider=self.config.active_provider, model=self.model_combo.currentText(), system_prompt=self.config.global_system_prompt)
        if session.system_prompt:
            session.messages.append(ChatMessage("system", session.system_prompt))
        tab = ChatTab(session); self._wire_chat_tab(tab); self.tabs.addTab(tab, session.title); self.tabs.setCurrentWidget(tab)


    def _wire_chat_tab(self, tab: ChatTab) -> None:
        tab.send.clicked.connect(self.chat_controller.send_message)
        tab.stop.clicked.connect(self.stop_generation)
        tab.regen.clicked.connect(self.chat_controller.regenerate)
        tab.retry.clicked.connect(self.chat_controller.retry)
        tab.copy_last.clicked.connect(self.chat_controller.copy_last_message)
        tab.edit_msg.clicked.connect(lambda: self.chat_controller.edit_message(self))
        tab.delete_msg.clicked.connect(lambda: self.chat_controller.delete_message(self))


    def close_tab(self, idx: int) -> None:
        if self.tabs.count() > 1:
            self.tabs.removeTab(idx)

    def _generate(self, tab: ChatTab) -> None:
        profile = self.config.active_profile(); backend = create_backend(profile); model = self.model_combo.currentText() or profile.default_model
        if not model:
            QMessageBox.warning(self, "No model", "Select or configure a model before generating."); return
        tab.session.model = model; tab.session.provider = profile.name
        messages = list(tab.session.messages)
        for interceptor in self.plugin_context.chat_interceptors:
            messages = interceptor(messages)
        self.request_view.setPlainText(json.dumps({"provider": profile.name, "url": profile.base_url, "model": model, "messages": [asdict(m) for m in messages], "options": self.config.parameters.to_backend_options()}, indent=2, default=str))
        self.status.showMessage("generating" if not tab.streaming.isChecked() else "streaming")
        assistant = ChatMessage("assistant", ""); tab.session.messages.append(assistant); tab.render()
        task = StreamTask(lambda: backend.chat(model, messages, self.config.parameters.to_backend_options(), tab.streaming.isChecked()))
        self.current_stream = task; self.worker_refs.append(task)
        task.token.connect(lambda tok: self._append_token(tab, assistant, tok)); task.error.connect(self._stream_error); task.completed.connect(lambda _: self._stream_done(tab))
        task.start()

    def _append_token(self, tab: ChatTab, msg: ChatMessage, token: str) -> None:
        msg.content += token; self.token_view.insertPlainText(token); tab.render()

    def _stream_error(self, error: str) -> None:
        self.status.showMessage("idle"); self.log(f"Generation error: {error}"); QMessageBox.critical(self, "Generation Error", error)

    def _stream_done(self, tab: ChatTab) -> None:
        self.status.showMessage("idle"); self.sessions.save(tab.session); self.refresh_sessions(); tab.render()

    def stop_generation(self) -> None:
        if self.current_stream:
            self.current_stream.cancel()
            self.status.showMessage("idle")

    def model_changed(self, text: str) -> None:
        tab = self.current_tab()
        if tab:
            tab.session.model = text

    def refresh_backend(self) -> None:
        profile = self.config.active_profile(); self.status.showMessage(f"testing {profile.base_url}")
        backend = create_backend(profile)
        async def work():
            status = await backend.test_connection(); models = await backend.list_models() if status.state == "connected" else [] ; return status, models
        task = AsyncTask(work); self.worker_refs.append(task); task.result.connect(self._backend_refreshed); task.error.connect(lambda e: self.log(f"Backend refresh error: {e}")); task.start()

    def _backend_refreshed(self, result: Any) -> None:
        status, self.models = result
        self._update_backend_status(status.state, status.latency_ms, status.detail)
        self._refresh_model_combo()
        self._refresh_model_table()

    def _update_backend_status(self, state: str, latency_ms: float, detail: str) -> None:
        self.status.showMessage(f"{state} | {latency_ms:.0f} ms | {self.config.active_profile().base_url}")
        self.log(f"Backend {state}: {detail}")

    def _refresh_model_combo(self) -> None:
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        self.model_combo.addItems([model.name for model in self.models])
        self.model_combo.blockSignals(False)

    def _refresh_model_table(self) -> None:
        self.model_table.setRowCount(0)
        for model in self.models:
            self._insert_model_table_row(model)

    def _insert_model_table_row(self, model: ModelInfo) -> None:
        row = self.model_table.rowCount()
        self.model_table.insertRow(row)
        ram = model.size_display if model.size else "backend reported"
        values = [
            model.name,
            model.size_display,
            model.quantization,
            model.parameter_size,
            str(model.context_size or ""),
            model.backend,
            ram,
            json.dumps(model.metadata)[:400],
        ]
        for column, value in enumerate(values):
            self.model_table.setItem(row, column, QTableWidgetItem(value))

    def switch_provider(self, name: str) -> None:
        self.config.active_provider = name; self.config.save(); self.refresh_backend()

    def refresh_sessions(self) -> None:
        self.sessions_list.clear()
        for s in self.sessions.list_sessions():
            item = QTreeWidgetItem() if False else None
            self.sessions_list.addItem(f"{s.updated_at[:19]}  {s.title}"); self.sessions_list.item(self.sessions_list.count()-1).setData(Qt.ItemDataRole.UserRole, s.id)

    def refresh_prompts(self) -> None:
        self.prompt_list.clear()
        for p in self.prompts.list():
            self.prompt_list.addItem(("★ " if p.favorite else "") + f"{p.category}: {p.title}")
            self.prompt_list.item(self.prompt_list.count()-1).setData(Qt.ItemDataRole.UserRole, p.content)

    def apply_prompt_item(self, item) -> None:
        tab = self.current_tab()
        if not tab:
            return
        content = item.data(Qt.ItemDataRole.UserRole); tab.session.system_prompt = content
        if tab.session.messages and tab.session.messages[0].role == "system":
            tab.session.messages[0].content = content
        else:
            tab.session.messages.insert(0, ChatMessage("system", content))
        tab.render()

    def save_as(self) -> None:
        tab = self.current_tab();
        if not tab:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Chat As", f"{tab.session.title}.json", "JSON (*.json)")
        if path:
            Path(path).write_text(tab.session.to_json(), encoding="utf-8")

    def open_session(self, session_id: str) -> None:
        session = self.sessions.load(session_id); tab = ChatTab(session); self._wire_chat_tab(tab); self.tabs.addTab(tab, session.title); self.tabs.setCurrentWidget(tab)

    def import_chat(self) -> None: self.chat_controller.open_chat_file(self)
    def export_current(self) -> None:
        tab = self.current_tab();
        if not tab:
            return
        path, selected = QFileDialog.getSaveFileName(self, "Export Chat", f"{tab.session.title}.md", "Markdown (*.md);;JSON (*.json);;Text (*.txt)")
        if not path:
            return
        p = Path(path)
        content = tab.session.to_json() if p.suffix == ".json" else tab.session.export_text() if p.suffix == ".txt" else tab.session.export_markdown()
        p.write_text(content, encoding="utf-8")

    def _async(self, coro_factory, done_msg: str) -> None:
        task = AsyncTask(coro_factory); self.worker_refs.append(task); task.finished_ok.connect(lambda: (self.log(done_msg), self.refresh_backend())); task.error.connect(lambda e: QMessageBox.critical(self, "Error", e)); task.start()

    def set_tab_title(self, title: str) -> None:
        self.tabs.setTabText(self.tabs.currentIndex(), title)

    def render_tab(self, tab: ChatTab) -> None:
        tab.render()

    def generate_for_tab(self, tab: ChatTab) -> None:
        self._generate(tab)

    def model_name(self) -> str:
        return self.model_combo.currentText()

    def append_terminal(self, text: str) -> None:
        self.terminal.insertPlainText(text)

    def add_worker(self, worker: Any) -> None:
        self.worker_refs.append(worker)

    def open_modelfile_editor(self) -> None: ModelfileEditor(self.config, self).exec()

    def build_model_from_modelfile(self, name: str, modelfile: str) -> None:
        if not name.strip():
            QMessageBox.warning(self, "Create Model", "Model name is required.")
            return
        backend = create_backend(self.config.active_profile())
        task = StreamTask(lambda: backend.create_model(name.strip(), modelfile))
        self.worker_refs.append(task)
        task.token.connect(lambda t: self.terminal.insertPlainText(t + "\n"))
        task.completed.connect(lambda _: self.refresh_backend())
        task.error.connect(lambda e: QMessageBox.critical(self, "Create Model", e))
        task.start()
    def open_template_viewer(self) -> None:
        model = self.model_combo.currentText();
        if not model:
            return
        async def show(): return await create_backend(self.config.active_profile()).show_model(model)
        task = AsyncTask(show); self.worker_refs.append(task); task.result.connect(lambda data: self._show_text_dialog("Template Viewer", json.dumps(data, indent=2))); task.error.connect(lambda e: QMessageBox.critical(self, "Template Viewer", e)); task.start()
    def _show_text_dialog(self, title: str, text: str) -> None:
        d = QMessageBox(self); d.setWindowTitle(title); d.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse); d.setDetailedText(text); d.setText(text[:1000]); d.exec()

    def open_endpoints(self) -> None:
        if EndpointDialog(self.config, self).exec():
            self.provider_combo.clear()
            self.provider_combo.addItems([p.name for p in self.config.provider_profiles])
            self.refresh_backend()
    def open_parameters(self) -> None: ParameterDialog(self.config, self).exec()
    def open_plugins(self) -> None: PluginManagerDialog(self.plugins, self).exec()
    def open_plugin_docs(self) -> None: self._show_text_dialog("Plugin SDK", (Path.cwd()/"docs"/"PLUGIN_SDK.md").read_text(encoding="utf-8"))
    def open_agent_builder(self) -> None: AgentBuilderDialog(self.agents, [m.name for m in self.models], list(self.plugins.loaded), self).exec()
    def import_agent(self) -> None: self.open_agent_builder()
    def export_agent(self) -> None: self.open_agent_builder()
    def toggle_theme(self) -> None: self.setStyleSheet("" if self.styleSheet() else DARK_QSS)
    def show_shortcuts(self) -> None: self._show_text_dialog("Keyboard Shortcuts", "Ctrl+N New Chat\nCtrl+O Open Chat\nCtrl+S Save\nCtrl+Q Exit\nCtrl+Enter Send from composer")
    def toggle_all_docks(self) -> None:
        docks = self.findChildren(QDockWidget); visible = not all(d.isVisible() for d in docks)
        for d in docks: d.setVisible(visible)
    def reset_layout(self) -> None:
        for d in self.findChildren(QDockWidget): d.show()
    def inspect_api(self) -> None: self.request_view.parent().show(); self.request_view.setFocus()
    def open_docs(self) -> None: self._show_text_dialog("Documentation", (Path.cwd()/"README.md").read_text(encoding="utf-8")[:12000])
    def about(self) -> None: QMessageBox.about(self, "About", "LocalLama Control Center\nA PySide6 IDE-grade desktop application for local and remote LLMs.")
    def diagnostics(self) -> None:
        mem = psutil.virtual_memory(); self.terminal.appendPlainText(f"CPU cores: {psutil.cpu_count()}\nRAM: {mem.available/1024**3:.1f} GiB available / {mem.total/1024**3:.1f} GiB total\nConfig: {self.config.file_path}\nData: {self.config.paths.data_dir}\nLogs: {self.config.paths.logs_dir}\n")
    def log(self, text: str) -> None: LOG.info(text); self.log_view.appendPlainText(text)
    def _restore_state(self) -> None:
        if self.config.ui.geometry_hex:
            self.restoreGeometry(QByteArray.fromHex(self.config.ui.geometry_hex.encode()))
        if self.config.ui.state_hex:
            self.restoreState(QByteArray.fromHex(self.config.ui.state_hex.encode()))
    def closeEvent(self, event) -> None:
        self.config.ui.geometry_hex = bytes(self.saveGeometry().toHex()).decode(); self.config.ui.state_hex = bytes(self.saveState().toHex()).decode(); self.config.save(); super().closeEvent(event)
