## [1.2.1] - 2026-08-15

### Fixed
- Made the installation wizard reject Android and Termux before creating a virtual environment or making installation changes.
- Added a clear explanation that the current PySide6 desktop installation path is not supported on Android/Termux.

## [1.2.0] - 2026-08-15

### Added
- Added `scripts/install-wizard.py` for cross-platform repository installation.
- Added Windows Start Menu shortcut creation without adding a `pywin32` dependency.
- Added optional Linux desktop-entry installation through the existing canonical launcher scripts.
- Added optional backend reachability checks without storing backend credentials.

### Documentation
- Added `docs/INSTALLER.md` covering installer usage, options, platform behavior, backend configuration, and future native packaging.
- Updated README installation guidance to include the installation wizard.

## [1.1.7] - 2026-06-08

### Fixed
- Made streamed Ollama error payloads fail pull, push, and create operations instead of recording a contradictory success and refreshing models.

### Documentation
- Clarified that Ollama stream errors are recorded as failed model operations.

## [1.1.6] - 2026-06-08

### Added
- Added centralized diagnostics helpers for structured log records, line-buffered console capture, cursor-safe text appends, and model-operation stream parsing.
- Added focused diagnostics tests for logging sinks, stdout/stderr-style capture, cursor-safe appends, partial stream assembly, and repeated status collapse.

### Changed
- Replaced overlapping Logs/Terminal model-operation output with a Diagnostics dock containing Logs, Console, and Operations tabs with distinct responsibilities.
- Routed pull, push, create, delete, clone, and template lifecycle events through Operations instead of dumping raw stream chunks into the terminal.
- Collapsed repeated model-operation stream statuses and retained only meaningful durable history transitions while keeping live status/progress current.
- Preserved Request Viewer for outbound payload inspection and Token/Response Viewer for active chat generation output.

### Fixed
- Captured Python logging records, including library loggers such as `httpx`, in the Logs diagnostics tab.
- Captured stdout/stderr-style app output in the Console diagnostics tab with line buffering.
- Ensured diagnostics text appends are cursor-safe and append at the document end.

### Documentation
- Updated README and feature matrix diagnostics terminology for Logs, Console, and Operations.
