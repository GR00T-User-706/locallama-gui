from __future__ import annotations

import sys
from pathlib import Path

import psutil
from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtWidgets import QInputDialog, QMessageBox

from locallama_gui.ui.model_browser import ModelBrowserDialog
from locallama_gui.ui.setup_wizard import FirstRunWizard
from locallama_gui.ui.theme import dark_qss


def _menu(window, title: str):
    for action in window.menuBar().actions():
        menu = action.menu()
        if menu and menu.title() == title:
            return menu
    return None


def _remove_action(menu, text: str) -> None:
    if menu is None:
        return
    for action in list(menu.actions()):
        if action.text() == text:
            menu.removeAction(action)
            action.deleteLater()


def _replace_action(menu, text: str, callback) -> None:
    if menu is None:
        return
    for action in menu.actions():
        if action.text() == text:
            try:
                action.triggered.disconnect()
            except (RuntimeError, TypeError):
                pass
            action.triggered.connect(callback)
            return


def _resource_path(name: str) -> Path:
    frozen_root = getattr(sys, "_MEIPASS", "")
    if frozen_root:
        return Path(frozen_root) / "docs" / name
    return Path(__file__).resolve().parents[2] / "packaging" / name


def _open_bundled_document(window, title: str, name: str) -> None:
    path = _resource_path(name)
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        QMessageBox.warning(window, title, f"Unable to open bundled documentation:\n{error}")
        return
    window._show_text_dialog(title, content[:20000])


def _choose_theme(window) -> None:
    choice, ok = QInputDialog.getItem(
        window,
        "Theme",
        "Select application theme:",
        ["MyLoAI Dark", "System"],
        0 if window.config.ui.theme == "dark" else 1,
        False,
    )
    if not ok:
        return
    if choice == "MyLoAI Dark":
        window.config.ui.theme = "dark"
        window.setStyleSheet(dark_qss(window.config.ui.font_size))
    else:
        window.config.ui.theme = "system"
        window.setStyleSheet("")
    window.config.save()


def _import_agent(window) -> None:
    from PySide6.QtWidgets import QFileDialog
    from locallama_gui.core.domain import AgentProfile

    path, _ = QFileDialog.getOpenFileName(window, "Import Agent", "", "JSON (*.json)")
    if not path:
        return
    try:
        agent = AgentProfile(**__import__("json").loads(Path(path).read_text(encoding="utf-8")))
        window.agents.upsert(agent)
        QMessageBox.information(window, "Import Agent", f"Imported agent: {agent.name}")
    except (OSError, ValueError, TypeError, KeyError) as error:
        QMessageBox.critical(window, "Import Agent", str(error))


def _export_agent(window) -> None:
    from PySide6.QtWidgets import QFileDialog
    import json

    agents = window.agents.list()
    if not agents:
        QMessageBox.information(window, "Export Agent", "There are no saved agents to export.")
        return
    names = [agent.name for agent in agents]
    name, ok = QInputDialog.getItem(window, "Export Agent", "Agent:", names, 0, False)
    if not ok:
        return
    agent = agents[names.index(name)]
    path, _ = QFileDialog.getSaveFileName(window, "Export Agent", f"{agent.name}.json", "JSON (*.json)")
    if not path:
        return
    try:
        Path(path).write_text(json.dumps(agent.__dict__, indent=2), encoding="utf-8")
        QMessageBox.information(window, "Export Agent", f"Exported agent: {agent.name}")
    except OSError as error:
        QMessageBox.critical(window, "Export Agent", str(error))


def _show_model_browser(window) -> None:
    ram = psutil.virtual_memory().total / 1024**3
    recommended = "gemma3:1b" if ram < 6 else "qwen3.5:4b" if ram < 12 else "mistral:7b" if ram < 24 else "deepseek-r1:7b"
    ModelBrowserDialog(window, recommended).exec()


def apply_production_fixes(window, first_run: bool = False) -> None:
    window.setWindowTitle("MyLoAI Control Center")

    developer = _menu(window, "Developer")
    _remove_action(developer, "Request Inspector")
    _remove_action(developer, "Diagnostics")

    help_menu = _menu(window, "Help")
    _remove_action(help_menu, "Diagnostics")

    settings = _menu(window, "Settings")
    _remove_action(settings, "Model Settings")
    _replace_action(settings, "Themes", lambda: _choose_theme(window))

    agents = _menu(window, "Agents")
    _replace_action(agents, "Import", lambda: _import_agent(window))
    _replace_action(agents, "Export", lambda: _export_agent(window))

    models = _menu(window, "Models")
    if models is not None:
        browser_action = QAction("Browse & Pull Models...", window)
        browser_action.triggered.connect(lambda: _show_model_browser(window))
        models.insertAction(models.actions()[0] if models.actions() else None, browser_action)

    window.open_docs = lambda: _open_bundled_document(window, "Documentation", "USER_MANUAL.md")
    window.open_plugin_docs = lambda: _open_bundled_document(window, "Plugin SDK", "PLUGIN_SDK.md")
    window.about = lambda: QMessageBox.about(
        window,
        "About MyLoAI",
        "MyLoAI Control Center\n\nA desktop control center for local and remote LLM services.\n\nVersion 1.2.0",
    )

    if first_run:
        from PySide6.QtCore import QTimer
        QTimer.singleShot(250, lambda: FirstRunWizard(window.config, window).exec())
