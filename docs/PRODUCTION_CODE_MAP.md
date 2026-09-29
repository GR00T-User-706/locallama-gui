# Production Code Map

Date: 2026-05-25
Scope: Baseline production map for Phase 1 documentation sync.

## Identity

### CONFIRMED
- Active production application package is `locallama_gui/`.
- Primary runtime entrypoint is `locallama_gui/app.py` via:
  - `locallama-gui` console script (`pyproject.toml`)
  - `python -m locallama_gui` (`locallama_gui/__main__.py`)

### CONFIRMED
- `archive/legacy_code/llm_studio/` and `archive/old_apps/ollama_GUI/` are not part of active production runtime.

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
| `archive/legacy_code/llm_studio/` | archived legacy/parallel tree | CONFIRMED_LEGACY | Historical only; not active entrypoint path. |
| `archive/old_apps/ollama_GUI/` | archived legacy/parallel tree | CONFIRMED_LEGACY | Historical only; contains legacy GUI variants. |

## Production Boundaries

### CONFIRMED
- Production feature development should target `locallama_gui/**`, `tests/**`, and documentation files.

### CONFIRMED
- Archived legacy trees are historical-only and excluded from CI lint/test validation.

### UNKNOWN
- Whether any files under `plugins/` beyond `sample_plugin.py` are used in individual user setups.

## TODO (Phase 1 follow-up only)
- Cross-link this map from `README.md` in a later, explicit docs-update task.
- Add per-menu ownership links once `docs/MENU_MAP.md` is validated.

---

# Incremental Production-Code API Audit

## AUDIT SEQUENCE: 1

- **Repository:** `GR00T-User-706/locallama-gui`
- **Repository-relative file:** `locallama_gui/__main__.py`
- **Filename:** `__main__.py`
- **Language:** Python
- **Package/module:** `locallama_gui.__main__`
- **Audit date:** 2026-09-29
- **Audit status:** Complete

### File Identity

- File contains 4 source lines.
- The file is the package module launcher for `python -m locallama_gui`, consistent with the existing production-code map.
- No explicit version information is present in this file.
- No module docstring is present.

### Imports

#### `from locallama_gui.app import main`

- Classification: internal project import.
- Package/module: `locallama_gui.app`
- Imported symbol: `main`
- Alias: none.
- The imported symbol is invoked when this module executes as `__main__`.
- The signature and implementation of `main` are not determined from this file and are therefore not expanded here because this audit execution is restricted to one production source file.

### Module-Level Definitions

None other than the imported name `main`.

### Functions

None defined in this file.

### Classes

None defined in this file.

### Methods

None defined in this file.

### Properties

None.

### Decorators

None.

### Constants / Variables

No explicitly assigned module-level constants or variables are present.

The imported name `main` is bound in the module namespace by the import statement.

### Type Aliases / Enums / Dataclasses / Protocols / Registries

None.

### Runtime / API Behavior

The file contains a standard Python module-entry guard:

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

Direct observations:

- The guarded block executes only when this module is run as the Python entry module.
- It calls the imported `locallama_gui.app.main` function.
- The return value from `main()` is passed to `SystemExit`.
- Therefore the process exits using the value returned by `main()` as the `SystemExit` argument.
- When the module is imported rather than executed as `__main__`, the guarded call is not executed.
- Importing this module still executes the top-level import of `locallama_gui.app.main`.

### Inputs

- No command-line arguments are explicitly parsed by this file.
- No environment variables are explicitly read by this file.
- No configuration values are explicitly read by this file.
- Any inputs consumed by `main()` are outside this file and are therefore not determinable from this source alone.

### Outputs

- No direct return value is produced by module-level code.
- The result of `main()` is forwarded to `SystemExit`.
- The resulting process-exit behavior therefore depends on the return value or exception behavior of `main()`.

### State Changes

- The import binds `main` in this module namespace.
- No mutable application state is explicitly created or modified by this file.

### Side Effects

Directly observable side effect:

- Calling `main()` when executed as `__main__`.
- Raising `SystemExit` with the return value of `main()`.

Potential side effects performed by `main()` itself are not determinable from this file.

### External Resources

- No direct file, network, database, subprocess, operating-system resource, or GUI resource access is implemented in this file.
- Resources accessed by `locallama_gui.app.main` are UNKNOWN / NOT DETERMINABLE FROM SOURCE in this file.

### Environment / Configuration Dependencies

- No direct environment-variable or configuration access is present.
- Indirect dependencies through `main()` are UNKNOWN / NOT DETERMINABLE FROM SOURCE.

### CLI / UI Integration

- This file is a CLI/module-launch integration point rather than a UI implementation.
- It provides the `python -m locallama_gui` execution path by delegating to `main()`.
- No UI widgets, signals, slots, callbacks, or event handlers are defined here.

### Error Handling

- No `try`/`except` handling is implemented.
- `main()` is invoked without local exception interception.
- Exceptions raised by the import or by `main()` are not caught in this file.
- `SystemExit` is explicitly raised using the result of `main()`.

### Types and Relationships

- Direct dependency: `locallama_gui.__main__` -> `locallama_gui.app.main`.
- Runtime relationship: module execution -> `main()` -> `SystemExit`.
- Inheritance: none.
- Composition: none.
- Instantiation: none.

### Public vs Internal Interface

- The file's effective public runtime interface is the package module-entry behavior invoked through `python -m locallama_gui`.
- The imported `main` name is not defined here and is not documented as a separate API by this file.
- No explicitly private symbols are present.

### Directly Observed vs Inferred

**DIRECTLY OBSERVED**

- `main` is imported from `locallama_gui.app`.
- The `__name__ == "__main__"` guard is present.
- `main()` is called inside that guard.
- Its return value is passed to `SystemExit`.

**INFERRED**

- The file functions as the package's module launcher. This is supported by its `__main__.py` location and the existing production map's statement that `python -m locallama_gui` delegates to `app.main()`.

**UNKNOWN / NOT DETERMINABLE FROM SOURCE**

- The signature, return semantics, exceptions, side effects, and resource usage of `locallama_gui.app.main`.
- Whether command-line arguments are consumed indirectly by `main()`.
- Whether environment variables or configuration are consumed indirectly by `main()`.
- Whether `main()` initializes a Qt application, performs logging setup, loads configuration, or performs other startup operations.

### Unresolved Items

- Full behavior of the imported `main` function requires a separate audit execution for `locallama_gui/app.py`.
- No other unresolved implementation details exist within `locallama_gui/__main__.py` itself.

STATUS: FULLY MAPPED
