## [1.1.10] - 2026-09-09

### Added
- Added a complete scalable Linux application icon at `packaging/linux/icons/com.github.gr00t-user-706.locallama-gui.svg` for desktop packaging and installer integration.

### Changed
- Wired the Linux desktop entry to the canonical LocalLama application icon.
- Synchronized package/runtime version metadata to `1.1.10`.

### Documentation
- Documented the packaged Linux icon path in the README.

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