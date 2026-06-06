## 1.1.3 - 2026-06-06

### Fixed
- Made Developer menu panel actions reliably show their stored dock widgets.
- Renamed misleading API Inspector and Debug Console actions to Request Inspector and Diagnostics Terminal to match their actual behavior.
- Made Help diagnostics automatically reveal the Terminal panel containing its output.

## 1.1.2 - 2026-05-27

### Changed
- Updated code-of-conduct enforcement reporting to use a private conduct-reporting channel (`conduct@locallama-gui.org`) instead of public issue reporting.
- Updated security policy with a concrete private fallback channel (`security@locallama-gui.org`) when GitHub Security Advisories are unavailable.
- Updated GitHub issue-template contact links to include both private security fallback guidance and a private conduct-reporting contact.
- Bumped project version from `1.1.1` to `1.1.2`.

## 1.1.1 - 2026-05-27

### Changed
- Corrected package metadata license declaration in `pyproject.toml` to reference the repository `LICENSE` file instead of incorrectly declaring MIT.
- Bumped project version from `1.1.0` to `1.1.1` for this metadata correction.

## 1.1.0 - 2026-05-27

### Added
- Added a repository `CODE_OF_CONDUCT.md` using Contributor Covenant 2.1 language for contributor behavior standards and enforcement.
- Added a `SECURITY.md` policy describing private vulnerability reporting expectations and response targets.
- Added GitHub issue templates for bug reports and feature requests, plus issue-template configuration to disable blank issues and direct security reports to private channels.

### Changed
- Added a `LICENSE` file using a custom community/commercial license aligned with maintainer-requested terms (public no-charge redistribution, attribution/upstream submission requirements, and commercial revenue-share requirement).
- Bumped project version from `1.0.17` to `1.1.0` in package metadata and runtime version constant.

### Documentation
- Updated `README.md` with a new Community and Governance section linking code of conduct, license, security policy, and issue templates.

# Changelog

## 1.0.17 - 2026-05-26

### Fixed
- Aligned chat edit/delete dialog indexing with visible chat turns by excluding app-internal hidden system messages from selection and targeting.

## 1.0.16 - 2026-05-26

### Changed
- Updated chat transcript rendering to hide app-internal system prompts, keep visible turn numbering aligned to visible messages only, and label assistant turns with the active model name when available.
- Clarified panel titles/placeholders so Request Viewer is explicitly redacted outbound payload and Token Viewer is current streamed response output.

### Fixed
- Fixed chat redraw/stream updates to preserve scroll position and pin to bottom only when user is already near the bottom.
- Redacted app-internal system prompt content in Request Viewer output while preserving full backend request payload behavior.
- Added Ollama option sanitization so unsupported options (`mirostat*`, `tfs_z`, `think`) are not sent, and stop sequences are cleaned to non-empty complete strings.

## 1.0.15 - 2026-05-26

### Fixed
- Reworked generation stop/shutdown handling to avoid UI-thread blocking waits (`wait(...)`) while still issuing cancellation to active stream workers.
- Added stream ownership tracking so only the currently active generation stream is allowed to mutate chat/token UI state or finalize generation state.
- Limited stop-generation to the active owned stream lifecycle, preventing stale stream callbacks from overriding current UI state.

## 1.0.14 - 2026-05-26

### Fixed
- Prevented shutdown crashes by canceling and waiting for active generation/background `QThread` workers during window close and stop-generation handling.
- Cleared `current_stream` on stream completion/error to avoid stale running-thread references.
- Set an explicit toolbar object name (`mainToolbar`) so `QMainWindow::saveState()` no longer warns about unnamed toolbars.

## 1.0.13 - 2026-05-26

### Added
- Added active-path Linux launcher integration artifacts: `run-locallama`, `scripts/install-launcher`, `scripts/install-desktop-entry`, and `packaging/linux/com.github.gr00t-user-706.locallama-gui.desktop`.
- Added `docs/LAUNCHING.md` with practical launch and installer usage, including dry-run commands.

### Changed
- Updated README run instructions with a concise launcher/desktop section linking `docs/LAUNCHING.md`.
- Added explicit AGENTS policy for canonical launcher naming and routine CI scope limited to active production paths (excluding archive/legacy trees).

### Fixed
- Hardened model deletion UX with explicit no-model guard, unambiguous destructive confirmation text, and success message including target model name.
- Surfaced backend refresh task failures to users with a visible error dialog in addition to logs/status updates.
- Rewired View/Developer dock actions to explicit helpers so actions reliably open/raise intended panels.

## 1.0.12 - 2026-05-25

### Fixed
- Synchronized `docs/VERSIONING.md` current-state snapshot with actual repository version metadata and latest changelog heading.

### Documentation
- Corrected version references in `docs/VERSIONING.md` to reflect reality after the 1.0.11 release.

## 1.0.11 - 2026-05-25

### Changed
- Reconciled `docs/STATE_OF_REPO.md` with current docs inventory and corrected stale version references from 1.0.9 to 1.0.10.
- Updated `docs/VERSIONING.md` snapshot values to match the 1.0.10 baseline before this release bump.

### Documentation
- Completed a read-only documentation reconciliation pass for the `docs/` folder and aligned status tables with files that now exist.

## 1.0.10 - 2026-05-25

### Changed
- Reconciled documentation references to archived legacy trees so active docs point to `archive/old_apps/ollama_GUI/` and `archive/legacy_code/llm_studio/`.
- Updated audit/analysis docs to reflect that legacy trees are already archived in the current repository state.

### Archived
- Updated `archive/ARCHIVE_INDEX.md` with a completed archive move reconciliation table including original paths, archive destinations, dates, reasons, and retention notes.

### Documentation
- Clarified legacy code location in `README.md` and synchronized archive status language across repository docs.

## 1.0.9 - 2026-05-24

### Fixed
- Made model metadata table cells explicitly non-editable while keeping item selection and enabled behavior intact.
- Kept model lifecycle actions (create/copy/delete) on explicit dialogs/actions rather than inline table edits.
### Added
- Added a new **UI Action Integrity** section in `AGENTS.md` near the existing UI guidance to require explicit control state clarity, ban active dead placeholders, and ban ambiguous dialogs.

### Changed
- Added explicit delivery checklist requirements for new UI actions (logic wiring, error handling, logs/status updates, docs, tests, version bump, and changelog updates).
- Added a scope guardrail reinforcing minimal-change behavior for small UI requests to prevent rewrite-the-universe responses.
- Added tests covering reasoning-mode exclusivity, config persistence, and request payload mapping.

### Changed
- Replaced independent thinking/plan/normal checkboxes in Generation Parameters with a single reasoning-mode dropdown and explicit default (`normal`).
- Added reasoning mode tooltip text that clarifies Ollama mapping (`think`/`plan`) versus app default behavior.

### Fixed
- Ensured request options emit at most one reasoning mode flag and omit flags for `normal`.
- Added backward-compatible migration from legacy boolean mode fields to the new persisted `reasoning_mode` value.

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
