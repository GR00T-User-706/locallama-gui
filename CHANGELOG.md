## [1.2.0] - 2026-09-08

### Added
- Added MyLoAI Control Center production packaging and installation media while preserving the `locallama-gui` repository and Python distribution identity.
- Added canonical `myloai` and compatibility `locallama-gui` Python console entry points.
- Added Linux MyLoAI desktop entry, launcher, man page, Debian package, Arch package, and AppImage build.
- Added Windows PyInstaller bundle and Inno Setup installer.
- Added macOS PyInstaller application bundle and DMG build.
- Added an end-user manual to production installers.
- Added a release payload contract that excludes archived, development-only, CI, test, and internal project material from production installers.

### Changed
- Promoted the installed application and installer identity to MyLoAI Control Center without changing the existing Python module or distribution namespace.
- Synchronized runtime version metadata to `1.2.0`.
- Extended routine Ruff exclusion to the repository archive while keeping existing active application paths unchanged.

### Documentation
- Added production packaging and release build specifications under `packaging/`.

## [1.1.9] - 2026-08-17

### Added
- Added canonical application architecture documentation in `docs/ARCHITECTURE.md`.
- Expanded `docs/QA_CHECKLIST.md` into the application-wide regression and release checklist.
- Expanded `docs/FEATURE_MATRIX.md` into the application capability contract.
- Added explicit configuration schema documentation in `docs/CONFIG_SCHEMA.md`.
- Added configuration schema version `2`, migration handling, and future-version rejection.
- Added plugin lifecycle regression coverage for discover, validate, trust, enable, disable, reload, untrust, and remove.
- Added configuration schema migration regression coverage.

### Changed
- Added explicit plugin `trust`, `untrust`, and `remove` lifecycle operations to `PluginManager`.
- Kept configuration schema versioning independent from package/release versioning.
- Synchronized package/runtime version metadata to `1.1.9`.

### Documentation
- Updated `docs/VERSIONING.md` with the independent configuration-schema versioning policy.

## [1.1.8] - 2026-08-17

### Fixed
- Prevented plugin discovery from importing or executing plugin modules just to inspect metadata.
- Enforced the plugin trust check before any trusted plugin module import.
- Stopped API keys from being serialized into `config.json` and migrated legacy plaintext provider keys to the operating system credential store.
- Applied restrictive permissions to the configuration file where supported.
- Corrected stale archive-path documentation in `CONTRIBUTING.md`.
- Corrected the versioning policy snapshot to reflect the current release.
- Merged the duplicate historical `1.1.3` changelog entries into one release entry.

### Security
- Added OS credential-store support through `keyring` for provider API keys.
- Added regression coverage proving plugin discovery and untrusted-plugin rejection do not execute plugin module code.

### Documentation
- Updated `docs/PLUGIN_SDK.md` with the static manifest and pre-import trust boundary.
- Refreshed `docs/REPO_ANALYSIS.md` with the current 1.1.8 state and remaining architecture gaps.

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

## [1.1.5] - 2026-06-08

### Added
- Added a feature matrix that classifies visible workflows as working, partial, blocked, or hidden.
- Added focused regression coverage for the MainWindow/ModelController async contract and model-operation terminal lifecycle.

### Changed
- Made the diagnostics terminal the operational record for model pull, push, clone, create, delete, and template inspection.
- Normalized model names and rejected empty or whitespace-only model-operation input.
- Guarded README and Plugin SDK loading so missing or unreadable documentation is reported without crashing.

### Fixed
- Added the public MainWindow async scheduler required by clone and delete model actions.
- Ensured model-operation errors are written to the terminal before user-facing error dialogs.
- Added explicit selected-model feedback for template inspection.

### Documentation
- Documented model-operation terminal behavior and the current feature-loop status.

## [1.1.4] - 2026-06-06

### Added
- Added `.github/agents/repo-code-risk-reviewer.agent.md` and `.github/prompts/repo-code-risk-reviewer.prompt.md`.

### Changed
- Updated the changelog and synchronized the package/runtime version metadata.

## [1.1.3] - 2026-06-06

### Changed
- Restricted the visible Ollama generation-parameter dialog to supported controls while retaining legacy config fields for backward-compatible loading.
- Updated the diagnostics request preview to reflect the corrected Ollama payload shape.
- Moved Ollama `think=true` from the runtime `options` object to the top-level chat request payload.
- Removed invalid Ollama `plan` forwarding from the strict runtime option path.
- Expanded the Ollama runtime-option allow-list with current server-defined keys for backend callers.

### Fixed
- Made Developer menu panel actions reliably show their stored dock widgets.
- Renamed misleading API Inspector and Debug Console actions to Request Inspector and Diagnostics Terminal to match their actual behavior.
- Made Help diagnostics automatically reveal the Terminal panel containing its output.

### Documentation
- Updated README parameter-profile documentation and synchronized the versioning snapshot.

## [1.1.2] - 2026-05-27

### Changed
- Updated code-of-conduct enforcement reporting to use a private conduct-reporting channel (`conduct@locallama-gui.org`) instead of public issue reporting.
- Updated security policy with a concrete private fallback channel (`security@locallama-gui.org`) when GitHub Security Advisories are unavailable.
- Updated GitHub issue-template contact links to include both private security fallback guidance and a private conduct-reporting contact.
- Bumped project version from `1.1.1` to `1.1.2`.

## [1.1.1] - 2026-05-27

### Changed
- Corrected package metadata license declaration in `pyproject.toml` to reference the repository `LICENSE` file instead of incorrectly declaring MIT.
- Bumped project version from `1.1.0` to `1.1.1` for this metadata correction.

## [1.1.0] - 2026-05-27

### Added
- Added a repository `CODE_OF_CONDUCT.md` using Contributor Covenant 2.1 language for contributor behavior standards and enforcement.
- Added a `SECURITY.md` policy describing private vulnerability reporting expectations and response targets.
- Added GitHub issue templates for bug reports and feature requests, plus issue-template configuration to disable blank issues and direct security reports to private channels.

### Changed
- Added a `LICENSE` file using a custom community/commercial license aligned with maintainer-requested terms (public no-charge redistribution, attribution/upstream submission requirements, and commercial revenue-share requirement).
- Bumped project version from `1.0.17` to `1.1.0` in package metadata and runtime version constant.

### Documentation
- Updated `README.md` with a new Community and Governance section linking code of conduct, security policy, and issue templates.
