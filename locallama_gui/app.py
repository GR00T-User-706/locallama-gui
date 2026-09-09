from __future__ import annotations

import os
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from platformdirs import user_config_dir
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from locallama_gui.core.config import APP_NAME, AppConfig
from locallama_gui.core.logging import configure_logging
from locallama_gui.ui.main_window import MainWindow
from locallama_gui.ui.production_fixes import apply_production_fixes


def main() -> int:
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")
    config_path = Path(user_config_dir(APP_NAME, "LocalLama")) / "config.json"
    first_run = not config_path.exists()
    config = AppConfig.load()
    configure_logging(config.paths.logs_dir)
    app = QApplication(sys.argv)
    app.setApplicationName("MyLoAI Control Center")
    app.setOrganizationName("LocalLama")
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings, True)
    win = MainWindow(config)
    apply_production_fixes(win, first_run=first_run)
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
