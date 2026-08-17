# Repository Analysis Report

Date: 2026-08-17
Scope: Current-state read-only audit findings and stabilization status.

## 1. Current project structure

Primary maintained runtime package:
- `locallama_gui/` (PySide6 desktop app, backends, core config/domain/managers, controllers, workers, diagnostics, UI).

Supporting project files:
- `pyproject.toml` (packaging + version + scripts)
- `requirements.txt` (runtime dependency mirror; keep synchronized or retire)
- `README.md`
- `tests/`
- `docs/`
- `packaging/linux/`
- `scripts/`

Archived legacy tree:
- `archive/old_apps/ollama_GUI/`
- `archive/legacy_code/llm_studio/`
- `archive/old_docs/`
- `archive/notes/`

## 2. Current version

- `pyproject.toml`: `1.1.8`
- `locallama_gui/__init__.py`: `1.1.8`
- Changelog latest release: `1.1.8`

## 3. Security stabilization completed in 1.1.8

- API keys are no longer serialized into `config.json`; provider credentials are stored through the OS credential store using `keyring`.
- Existing plaintext `api_key` fields are migrated to the credential store during configuration load.
- The configuration file is written with restrictive `0600` permissions where supported.
- Plugin discovery parses a static `Plugin.manifest` literal with Python AST instead of importing plugin modules.
- Plugin enablement validates the static manifest and trust list before importing plugin code.
- Security regression tests cover credential persistence and plugin import boundaries.

## 4. Documentation reconciliation completed in 1.1.8

- `docs/VERSIONING.md` now reflects version `1.1.8` and current synchronization rules.
- `CONTRIBUTING.md` now references the actual archive paths instead of retired top-level legacy roots.
- The duplicate `1.1.3` changelog entries were merged into one historical release entry.

## 5. Remaining architecture hotspots

- `locallama_gui/ui/main_window.py` remains large and mixes UI construction, lifecycle orchestration, diagnostics, backend refresh, and generation state.
- Agent profiles are persisted and editable but remain only partially integrated with chat generation/tool execution.
- Plugin trust is an explicit in-process trust boundary; plugins are not sandboxed.
- OpenAI-compatible and llama.cpp providers intentionally share one backend implementation, but their feature parity with Ollama generation controls is narrower.
- Configuration persistence still has no formal schema-version migration framework beyond field-level compatibility logic.

## 6. Remaining documentation/process gaps

Recommended follow-up documents/processes:
- `docs/ARCHITECTURE.md`
- `docs/DATA_LAYOUT.md`
- `docs/RELEASING.md`
- expanded `docs/FEATURE_MATRIX.md` coverage for all visible workflows
- cross-platform CI validation if Linux/macOS/Windows support is to remain a tested claim

## 7. Testing status

The repository has backend, configuration, controller, diagnostics, model-operation, and chat-view regression tests. Version 1.1.8 adds security-boundary coverage for credential serialization and plugin trust/import behavior.

Continue expanding coverage for:
- configuration corruption and migration
- OpenAI-compatible backend streaming/error behavior
- plugin discovery/enable/disable failure paths
- credential-store failures
- GUI theme switching and other known manual-test defects

## 8. Archive policy

Archived code under `archive/**` is historical storage and excluded from routine production CI. If code is revived, move it into the active runtime tree and validate it there. Maintain `archive/ARCHIVE_INDEX.md` for provenance.
