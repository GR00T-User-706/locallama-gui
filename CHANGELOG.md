## [1.2.12] - 2026-09-24

### Fixed
- Restored the active `PromptManagerDialog` entry point from the MainWindow so the implemented prompt-management workflow is reachable.
- Added Prompt Manager access to the main toolbar and Settings menu, and refresh the System Prompts dock after prompt-management changes.
- Preserved unused MainWindow UI imports as commented placeholders instead of deleting them while the GUI remains untested.
- Restored the original user chat-role accent color `#a3be8c`.

### Documentation
- Kept Prompt Manager functionality aligned with the existing feature matrix and QA expectations.

## [1.2.11] - 2026-09-24

### Fixed
- Fixed light/system theme chat output so message blocks use the active Qt palette instead of a hard-coded dark background.
- Fixed the production packaging workflow so distribution validation derives the expected version from `pyproject.toml` instead of a stale hard-coded release value.
- Synchronized Linux Arch packaging, Linux man-page metadata, Windows installer fallback metadata, and the Linux packaging bundle manifest to `1.2.11`.
- Excluded `archive/**` from routine Ruff validation so historical code cannot fail active CI.

### Documentation
- Updated the versioning policy to require unified application version metadata across packaging and release validation.
- Resolved the documented production-packaging audit findings and updated the known-bugs tracker.

## [1.2.10] - 2026-09-22

### Fixed
- Fixed the first-run setup wizard syntax error so the backend connection callback is valid Python.
- Made the About dialog display the canonical application version.
- Fixed source-tree Plugin SDK documentation lookup while preserving the frozen-package documentation path.

### Documentation
- Recorded the verified fixes for the active code audit findings and the remaining authorization-required light-theme issue.
- Marked stale Diagnostics and Model Settings findings as fixed after verification against the current production menu wiring.

## [1.2.9] - 2026-09-21

### Fixed
- Restored valid `from __future__ import annotations` syntax in the Ollama and OpenAI-compatible backend modules so the active backend package can be parsed and imported.
- Synchronized the release-packaging workflow and platform packaging version references with application version `1.2.9`.

### Documentation
- Recorded the active production-packaging audit findings and their verification requirements.

## [1.2.8] - 2026-09-20

### Fixed
- Validated and normalized chat message roles/content before sending requests to Ollama or OpenAI-compatible backends.
- Added server response details to chat HTTP errors so a `400 Bad Request` now exposes the backend's actual error message instead of only the status code.
- Added regression tests for user prompt serialization, empty requests, and invalid message roles.

## [1.2.7] - 2026-09-20

### Documentation
- Corrected Markdown escaping in the production build guide so the documented commands and paths render correctly.

## [1.2.6] - 2026-09-20

### Fixed
- Corrected shell variable expansion in the canonical Linux production build script so it executes correctly under Bash.

## [1.2.5] - 2026-09-20

### Fixed
- Tracked the first-run setup connectivity worker in the main window worker registry so closing the application cannot destroy the wizard's active thread.

## [1.2.4] - 2026-09-20

### Fixed
- Made asynchronous worker cancellation interrupt the active asyncio task instead of waiting indefinitely for a network operation to return during application shutdown.

## [1.2.3] - 2026-09-20

### Fixed
- Added an offline AppImage build path that accepts a locally supplied AppImage runtime through `APPIMAGERUNTIME`.

### Documentation
- Documented the complete Linux production build prerequisites and offline AppImage runtime requirement.

## [1.2.2] - 2026-09-20

### Fixed
- Included keyring backend modules and package metadata in PyInstaller bundles so credential-store discovery is preserved in frozen builds.
- Synchronized the Windows installer fallback version and Linux man-page version with the application version.
- Clarified that the Arch package recipe uses system Python dependencies while the Debian, AppImage, Windows, and macOS artifacts bundle the runtime.

### Documentation
- Added a canonical Linux production build path and explicit build prerequisites for the generated `.deb` and AppImage artifacts.

## [1.2.1] - 2026-09-20

### Changed