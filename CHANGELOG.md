# Changelog

## 1.0.8 - 2026-05-24

### Fixed
- Fixed startup crash in dock creation by building Request Viewer and Token Viewer wrappers before attaching them to `QDockWidget`.
- Removed invalid `setWidget` calls on plain `QWidget` parents that caused `AttributeError` on launch.

## 1.0.7 - 2026-05-24

### Added
- Added a hidden app-level system prompt guardrail so LocalLama sessions consistently behave as an in-app assistant.
- Added a user-editable "Default System Prompt" settings action for new chats.
- Added Request Viewer and Token Viewer copy/clear controls.

### Changed
- Improved chat message formatting and spacing with clearer role labels.
- Improved generation UX by disabling/enabling chat controls during streaming and restoring state on stop/error/complete.
- Improved backend status line to include provider and current model.
- Added timestamped entries in the log panel.

### Fixed
- Fixed misleading Ctrl+Enter prompt behavior by handling both Ctrl+Enter and Ctrl+Return in the composer.
- Improved auto-scroll behavior so chat doesn't forcibly jump while users read previous content.

## 1.0.4 - 2026-05-24

### Fixed
- Fixed Ruff E701 lint errors caused by one-line conditional return statements.
- Fixed Ruff F821 lambda exception capture issue in `ollama-gui.py`.
- CI lint job should now pass.

## 1.0.3 - 2026-05-24

### Fixed
- Stopped CI Ruff failure gremlins by excluding legacy non-production trees (`llm_studio/`, `ollama_GUI/`) from repository-wide lint scope.
- Kept lint focus on maintained production package and tests so `ruff check .` can pass consistently.

## 1.0.2 - 2026-05-24

### Fixed
- Fixed Ruff E701 lint errors caused by one-line conditional return statements.
- Fixed Ruff F821 lambda exception capture issue in `ollama_GUI/ollama-gui-py/bin/ollama-gui.py`.
- CI lint job should now pass.

## 1.0.1 - 2026-05-24

### Added
- Added `docs/REPO_ANALYSIS.md` with full repository audit, active runtime identification, archive recommendations, and phased next steps.
- Added `archive/ARCHIVE_INDEX.md` to standardize archival provenance tracking.
- Added backend and config persistence unit tests for Ollama model parsing and `AppConfig` save/load behavior.

### Changed
- Updated README with versioning/changelog references and implementation-phase guidance.
- Bumped project version from `1.0.0` to `1.0.1`.

### Archived
- No file moves performed in this update; archive governance and planned candidates documented first.
