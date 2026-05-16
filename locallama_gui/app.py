from __future__ import annotations

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from locallama_gui.core.config import AppConfig
from locallama_gui.core.logging import configure_logging
from locallama_gui.ui.main_window import MainWindow


def main() -> int:
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")
    config = AppConfig.load()
    configure_logging(config.paths.logs_dir)
    app = QApplication(sys.argv)
    app.setApplicationName("LocalLama Control Center")
    app.setOrganizationName("LocalLama")
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings, True)
    win = MainWindow(config)
    win.show()
    return app.exec()
