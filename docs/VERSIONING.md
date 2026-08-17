# Versioning Policy

Date: 2026-08-17
Scope: Current repository versioning policy and synchronization rules.

## Current State Snapshot

### CONFIRMED
- `pyproject.toml` version: `1.1.8`
- `locallama_gui/__init__.py` version: `1.1.8`
- `CHANGELOG.md` latest version heading: `1.1.8` (dated 2026-08-17)

### Source of truth

`pyproject.toml` is the packaging/release version source. `locallama_gui/__init__.py` must remain synchronized with it for runtime metadata.

## Semantic Versioning Rules

Use `MAJOR.MINOR.PATCH`.

- PATCH: bug fixes, documentation corrections, lint/test/config fixes, and small security fixes that do not add backward-incompatible behavior.
- MINOR: backward-compatible user-facing features or workflows.
- MAJOR: breaking behavior, incompatible configuration changes, or architecture shifts.

## Sync Targets for Any Future Version Bump

Verify and update as needed:

1. `pyproject.toml`
2. `locallama_gui/__init__.py`
3. `CHANGELOG.md` with one new top-level entry
4. Any user-facing version references in docs/README
5. Any About/version display paths

Do not maintain a separate `VERSION` file unless the repository explicitly adopts one as a new source of truth.

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
