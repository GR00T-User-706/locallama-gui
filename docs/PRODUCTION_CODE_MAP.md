# Production Code Map

Date: 2026-05-25
Scope: Baseline production map for Phase 1 documentation sync.

## Identity

### CONFIRMED
- Active production application package is `locallama_gui/`.
- Primary runtime entrypoint is `locallama_gui/app.py` via:
  - `locallama-gui` console script (`pyproject.toml`)
  - `python -m locallama_gui` (`locallama_gui/__main__.py`)

### LIKELY
- `llm_studio/` and `ollama_GUI/` are not part of active production runtime.

### UNKNOWN
- Whether any external user launchers still invoke legacy paths in local environments.

## Runtime Path Map

| Path | Role | Status | Notes |
|---|---|---|---|
| `locallama_gui/app.py` | QApplication bootstrap | CONFIRMED_ACTIVE | Loads config, logging, `MainWindow`. |
| `locallama_gui/__main__.py` | module launcher | CONFIRMED_ACTIVE | Delegates to `app.main()`. |
| `locallama_gui/ui/main_window.py` | main UI surface | CONFIRMED_ACTIVE | Menus, docks, tabs, orchestration. |
| `locallama_gui/ui/dialogs.py` | dialogs | CONFIRMED_ACTIVE | Parameters/plugins/agent/modelfile dialogs. |
| `locallama_gui/ui/controllers/` | action routing | CONFIRMED_ACTIVE | Chat/model/plugin controllers. |
| `locallama_gui/ui/workers.py` | background tasks | CONFIRMED_ACTIVE | Stream/async operations. |
| `locallama_gui/backends/` | provider backends | CONFIRMED_ACTIVE | Ollama + OpenAI-compatible backends. |
| `locallama_gui/core/config.py` | config + settings persistence | CONFIRMED_ACTIVE | App paths, providers, parameters, UI state. |
| `locallama_gui/core/managers.py` | session/prompt/agent/plugin managers | CONFIRMED_ACTIVE | Core manager layer. |
| `locallama_gui/core/domain.py` | domain models | CONFIRMED_ACTIVE | Dataclasses for runtime objects. |
| `plugins/sample_plugin.py` | sample plugin | LIKELY_OPTIONAL | Not required for app startup. |
| `tests/` | active test suite | CONFIRMED_ACTIVE | Production-focused tests. |
| `llm_studio/` | legacy/parallel tree | LIKELY_LEGACY | Not active entrypoint path. |
| `ollama_GUI/` | legacy/parallel tree | LIKELY_LEGACY | Contains legacy GUI variants. |

## Production Boundaries

### CONFIRMED
- Production feature development should target `locallama_gui/**`, `tests/**`, and documentation files.

### LIKELY
- Legacy trees should remain read-only until archival actions are explicitly approved.

### UNKNOWN
- Whether any files under `plugins/` beyond `sample_plugin.py` are used in individual user setups.

## TODO (Phase 1 follow-up only)
- Cross-link this map from `README.md` in a later, explicit docs-update task.
- Add per-menu ownership links once `docs/MENU_MAP.md` is validated.
