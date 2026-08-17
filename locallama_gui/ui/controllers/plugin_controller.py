from __future__ import annotations

from pathlib import Path
from typing import Protocol


class PluginWindowPort(Protocol):
    def log(self, text: str) -> None: ...


class PluginController:
    def __init__(self, plugins, config, window: PluginWindowPort) -> None:
        self.plugins = plugins
        self.config = config
        self.window = window

    def reload_plugins(self) -> None:
        self.plugins.reload()
        self.window.log("Plugins reloaded")

    def install_plugin(self, parent) -> None:
        path, _ = __import__("PySide6.QtWidgets", fromlist=["QFileDialog"]).QFileDialog.getOpenFileName(parent, "Install Plugin", filter="Python (*.py)")
        if path:
            dest = self.config.paths.plugins_dir / Path(path).name
            dest.write_text(Path(path).read_text(encoding="utf-8"), encoding="utf-8")
            self.window.log(f"Installed plugin {dest}")
