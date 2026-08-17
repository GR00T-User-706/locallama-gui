# Versioning Policy

Date: 2026-08-17
Scope: Current repository versioning policy and synchronization rules.

## Current State Snapshot

### CONFIRMED
- `pyproject.toml` version: `1.1.8`
- `locallama_gui/__init__.py` version: `1.1.8`
- `CHANGELOG.md` latest version heading: `1.1.8` (dated 2026-08-17)
- persisted configuration schema: `2`

### Source of truth

`pyproject.toml` is the packaging/release version source. `locallama_gui/__init__.py` must remain synchronized with it for runtime metadata.

The persisted configuration schema has a separate source of truth: `CONFIG_SCHEMA_VERSION` in `locallama_gui/core/config.py`. Configuration schema versions describe persisted-data compatibility and must not be treated as application release versions.

See `docs/CONFIG_SCHEMA.md` for the persisted configuration contract and migration policy.

## Semantic Versioning Rules

Use `MAJOR.MINOR.PATCH`.

- PATCH: bug fixes, documentation corrections, lint/test/config fixes, and small security fixes that do not add backward-incompatible behavior.
- MINOR: backward-compatible user-facing features or workflows.
- MAJOR: breaking behavior, incompatible configuration changes, or architecture shifts.

## Sync Targets for Any Future Application Version Bump

Verify and update as needed:

1. `pyproject.toml`
2. `locallama_gui/__init__.py`
3. `CHANGELOG.md` with one new top-level entry
4. Any user-facing version references in docs/README
5. Any About/version display paths

Do not maintain a separate `VERSION` file unless the repository explicitly adopts one as a new source of truth.

## Configuration Schema Versioning

Configuration schema versioning is independent from application release versioning.

When persisted configuration changes incompatibly:

1. increment `CONFIG_SCHEMA_VERSION`;
2. add an explicit migration step in `AppConfig._migrate_data()`;
3. add migration/round-trip regression tests;
4. update `docs/CONFIG_SCHEMA.md`;
5. reject unsupported future schemas instead of guessing their meaning.

A package release does not require a schema increment when the persisted representation remains compatible. A schema increment does not imply a major application release when the application can safely migrate existing data.

## Changelog Format

Use:

```markdown
## [x.y.z] - YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Security
- ...

### Archived
- ...

### Documentation
- ...
```

Include only applicable sections.

## Audit and documentation rules

- Audit-only work must not bump versions unless implementation changes are also made.
- When an implementation task changes behavior, synchronize the version and changelog in the same change set.
- Historical version snapshots must be labeled with their historical date instead of being presented as current state.
- There must be only one changelog entry for each released version number.
