from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(log_dir: Path) -> None:
    """Configure file logging without assuming a console exists.

    Native GUI builds can have ``sys.stderr is None``. A standard
    StreamHandler created against that stream causes the logging module to
    raise secondary ``NoneType.write`` errors, which obscures the real error.
    The application installs its Qt diagnostics handler after startup, so a
    console handler is unnecessary here.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[logging.FileHandler(log_dir / "locallama-gui.log", encoding="utf-8")],
        force=True,
    )
