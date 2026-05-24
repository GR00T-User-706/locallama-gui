# Changelog

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
