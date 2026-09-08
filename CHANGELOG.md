## [1.2.0] - 2026-09-08

### Added
- Added MyLoAI Control Center production packaging foundation while preserving the `locallama-gui` repository identity.
- Added canonical `myloai` and compatibility `locallama-gui` Python console entry points.
- Added Linux MyLoAI desktop entry and user manual.
- Added Debian and Arch packaging foundations.
- Added a release payload contract that excludes archived, development-only, CI, test, and internal project material from production installers.

### Changed
- Promoted package metadata to the MyLoAI Control Center product identity.
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
