# Versioning Policy (Baseline)

Date: 2026-05-25
Scope: Documentation-only baseline policy reference.

## Current State Snapshot

### CONFIRMED
- `pyproject.toml` version: `1.1.3`
- `locallama_gui/__init__.py` version: `1.1.3`
- `CHANGELOG.md` latest version heading: `1.1.3` (dated 2026-06-02)

### LIKELY
- `pyproject.toml` is the practical source of truth for packaging/release version metadata.

### UNKNOWN
- Whether GUI About/Help surfaces version number consistently in all runtime states.

## Semantic Versioning Rules

Use `MAJOR.MINOR.PATCH`.

- PATCH: bug fixes, docs-only sync, lint/test/config fixes without new features.
- MINOR: backward-compatible user-facing features/workflows.
- MAJOR: breaking behavior, incompatible configs, or architecture shifts.

## Sync Targets for Any Future Version Bump

When bumping version in a future task, verify and update as needed:

1. `pyproject.toml`
2. `locallama_gui/__init__.py`
3. `CHANGELOG.md` (new top entry)
4. Any user-facing version references in docs/README
5. Any About/version display paths (if confirmed in UI)

## Changelog Format Baseline

Use:

```markdown
## x.y.z - YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Archived
- ...

### Documentation
- ...
```

Include only applicable sections.

## Guardrails

### CONFIRMED
- Do not bump versions in audit-only tasks unless explicitly requested.

### LIKELY
- Docs-only baseline phase should defer version bump and changelog edits until implementation tasks begin.

### UNKNOWN
- Whether maintainers want a standalone `VERSION` file long-term.
