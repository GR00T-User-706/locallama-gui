# Repository Analysis Report

Date: 2026-05-24

## 1. Current project structure

Primary maintained runtime package:
- `locallama_gui/` (PySide6 desktop app, backends, core config/domain, controllers, workers).

Supporting project files:
- `pyproject.toml` (packaging + version + scripts)
- `requirements.txt`
- `README.md`
- `tests/`
- `docs/`

Archived legacy/parallel trees:
- `archive/old_apps/ollama_GUI/` (legacy Python + Qt/QML implementations)
- `archive/legacy_code/llm_studio/` (parallel app and harvested experimental modules)

## 2. Entry points

- Console script: `locallama-gui = locallama_gui.app:main` (`pyproject.toml`)
- Module execution: `python -m locallama_gui` (`locallama_gui/__main__.py`)

## 3. Main GUI files

- `locallama_gui/ui/main_window.py` — main window, menus, dock panels, model table, chat tabs, diagnostics panels.
- `locallama_gui/ui/dialogs.py` — dialogs for endpoints/parameters/plugins/agent builder/modelfile editor.
- `locallama_gui/ui/workers.py` — background async/thread workers for non-blocking operations.
- `locallama_gui/ui/controllers/*.py` — chat/model/plugin actions and wiring.

## 4. Ollama integration files

- `locallama_gui/backends/ollama.py` — Ollama API implementation (tags/chat/pull/push/delete/copy/create/show).
- `locallama_gui/backends/manager.py` — backend factory selection.
- `locallama_gui/backends/base.py` — backend interface + status contracts.

## 5. Config/settings files

- `locallama_gui/core/config.py` — persisted config, provider profiles, generation parameters, plugin trust/settings, UI state.
- Runtime data directories created through `platformdirs`.

## 6. Usable as-is

- `locallama_gui/backends/ollama.py`: broad CLI-parity API feature surface through HTTP endpoints.
- `locallama_gui/core/config.py`: robust dataclass-based settings persistence.
- `locallama_gui/ui/workers.py`: async-safe background execution pattern to avoid UI freezes.
- `locallama_gui/ui/controllers/`: separate action handlers reduce direct UI coupling.

## 7. Needs repair/refactor (incremental)

- `locallama_gui/ui/main_window.py` is very large and mixes responsibilities (UI build, orchestration, backend lifecycle, diagnostics logging).
  - Recommendation: incremental extraction into helper methods/controllers without behavior changes.
- Tests currently emphasize controller regressions but need stronger backend/config coverage.

## 8. Dead/duplicate/experimental/obsolete candidates

- `archive/old_apps/ollama_GUI/`: archived legacy codebase not used by current entrypoint.
- `archive/legacy_code/llm_studio/`: archived parallel code tree and experimental content.

These are now archived and should remain preserved for historical reference.

## 9. Archive status

Previously recommended archive candidates have now been physically moved under `archive/` in this repository state.

Maintain `archive/ARCHIVE_INDEX.md` for any additional future archive moves with provenance and reason.

## 10. Security, stability, packaging issues

- Dynamic plugin loading is powerful but assumes trusted local code. Continue to enforce trust lists and explicit enablement.
- Large monolithic main window increases maintenance risk and regression surface.
- Multiple parallel trees increase contributor confusion and accidental import risk.
- Packaging for active runtime is clean in `pyproject.toml`, but documentation must clearly define active vs legacy trees.

## 11. Recommended next steps

1. Stabilize documentation/process first:
   - Add this analysis report, archive index, changelog discipline, and versioning policy.
2. Expand test coverage:
   - Ollama model parsing and API error behavior via mocks.
   - Config load/save roundtrip and invalid-state guard tests.
3. Perform incremental archival of clearly non-runtime experimental code.
4. Begin targeted refactor of `main_window.py` in small behavior-preserving commits.
5. Continue feature completion against Ollama CLI parity via existing backend abstraction.
