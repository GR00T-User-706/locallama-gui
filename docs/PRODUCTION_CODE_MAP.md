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

---

## AUDIT SEQUENCE: 2

- **Repository:** `GR00T-User-706/locallama-gui`
- **Repository-relative file:** `locallama_gui/app.py`
- **Filename:** `app.py`
- **Language:** Python
- **Package/module:** `locallama_gui.app`
- **Audit date:** 2026-09-29
- **Audit status:** Complete
- **Source revision audited:** `6ff7759dafa38f8c1243cf57e64917702dd99d4d`

### File Identity

- Complete source file parsed.
- Application bootstrap module for the desktop GUI.
- No explicit module-level version declaration is present.
- No module docstring is present.

### Imports

#### `from __future__ import annotations`
- Classification: Python language feature import.
- Effect: postpones evaluation of annotations.

#### `import os`
- Classification: standard library.
- Used for environment-variable manipulation and path-related access through `os.path.dirname`.

#### `import sys`
- Classification: standard library.
- Used for `sys.path`, `sys.argv`, and process exit via `SystemExit`.

#### `from pathlib import Path`
- Classification: standard library.
- Imported symbol: `Path`.
- Used to construct the configuration-file path.

#### `from platformdirs import user_config_dir`
- Classification: third-party.
- Used to obtain the platform-specific per-user configuration directory.

#### `from PySide6.QtCore import Qt`
- Classification: third-party GUI framework.
- Used for the `AA_DontCreateNativeWidgetSiblings` application attribute.

#### `from PySide6.QtWidgets import QApplication`
- Classification: third-party GUI framework.
- Used to construct the Qt application object.

#### `from locallama_gui.core.config import APP_NAME, AppConfig`
- Classification: internal project import.
- Imported symbols: `APP_NAME`, `AppConfig`.
- Used for application configuration loading and configuration-directory naming.

#### `from locallama_gui.core.logging import configure_logging`
- Classification: internal project import.
- Imported symbol: `configure_logging`.
- Used to configure application logging using the configured logs directory.

#### `from locallama_gui.ui.main_window import MainWindow`
- Classification: internal project import.
- Imported symbol: `MainWindow`.
- Used to create the main application window and temporarily replace its `refresh_backend` method during first-run startup.

#### `from locallama_gui.ui.production_fixes import apply_production_fixes`
- Classification: internal project import.
- Imported symbol: `apply_production_fixes`.
- Used after window construction and before display.

### Module-Level Definitions

No explicit module-level constants, variables, classes, or type aliases are defined beyond imported names.

### Functions

#### `main`

- Location: module-level function.
- Parameters: none.
- Return annotation: `int`.
- Decorators: none.
- Purpose: initializes the application environment, configuration, logging, Qt application, main window, production fixes, and event loop, then returns the Qt event-loop exit code.

##### Implementation sequence

1. Calls `os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")`.
   - Reads the existing environment mapping entry if present.
   - Sets `QT_ENABLE_HIGHDPI_SCALING` to `"1"` only when absent.
2. Calls `os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")` with the same set-if-absent behavior.
3. Constructs `config_path` as `Path(user_config_dir(APP_NAME, "LocalLama")) / "config.json"`.
4. Computes `first_run` as the negation of `config_path.exists()`.
5. Calls `AppConfig.load()` and stores the resulting object in `config`.
6. Calls `configure_logging(config.paths.logs_dir)`.
7. Constructs `QApplication(sys.argv)`.
8. Sets the Qt application name to `"MyLoAI Control Center"`.
9. Sets the Qt organization name to `"LocalLama"`.
10. Sets `Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings` on the application.
11. Saves the original `MainWindow.refresh_backend` attribute in `original_refresh_backend`.
12. If `first_run` is true, replaces `MainWindow.refresh_backend` with a lambda accepting `self` and returning `None`.
13. Enters a `try` block and constructs `MainWindow(config)`, storing the instance in `win`.
14. The `finally` block restores `MainWindow.refresh_backend` to `original_refresh_backend` regardless of whether window construction succeeds or raises.
15. Calls `apply_production_fixes(win, first_run=first_run)`.
16. Calls `win.show()`.
17. Calls `app.exec()` and returns its result.

##### Variables read

- `os.environ`
- `sys.argv`
- `APP_NAME`
- `AppConfig`
- `configure_logging`
- `MainWindow`
- `apply_production_fixes`
- `Qt`
- `QApplication`
- `Path`
- `user_config_dir`

##### Variables / state modified

- Environment variables may be modified through the two `setdefault` calls when the keys are absent.
- `MainWindow.refresh_backend` is temporarily replaced during first-run window construction and restored in `finally`.
- Local variables created: `config_path`, `first_run`, `config`, `app`, `original_refresh_backend`, `win`.
- Qt application object state is modified through application name, organization name, and application attribute configuration.

##### Side effects

- May set two process environment variables.
- Reads the user-specific configuration directory and checks whether `config.json` exists.
- Loads application configuration through `AppConfig.load()`.
- Configures application logging.
- Creates the Qt application object.
- Mutates the `MainWindow.refresh_backend` class attribute temporarily during first-run construction.
- Constructs and displays the main window.
- Enters the Qt event loop.

##### External resources

Directly observed:
- User configuration filesystem path through `user_config_dir` and `Path.exists()`.
- Application logging destination through `config.paths.logs_dir` passed to `configure_logging`.
- Qt GUI subsystem through `QApplication` and `win.show()`.

Potential resources used by imported functions/classes are not expanded beyond this file's direct implementation.

##### Exceptions

- No explicit `raise` statement appears inside `main`.
- No exception types are caught.
- The `finally` block guarantees restoration of `MainWindow.refresh_backend` if `MainWindow(config)` raises.
- Exceptions from configuration loading, logging configuration, Qt initialization, window construction, production-fix application, window display, or the event loop are not caught here and therefore propagate outward.

### Classes

None defined in this file.

### Methods

No methods are defined in this file.

External method calls made by `main` include:
- `Path.exists()`
- `AppConfig.load()`
- `configure_logging(...)`
- `QApplication(...)`
- `app.setApplicationName(...)`
- `app.setOrganizationName(...)`
- `app.setAttribute(...)`
- `MainWindow(...)`
- `apply_production_fixes(...)`
- `win.show()`
- `app.exec()`

### Properties

No properties are defined in this file.

### Decorators

None.

### Types / Type Aliases / Enums / Dataclasses / Protocols / Registries

- Return type annotation `int` is present on `main`.
- No type aliases, enums, dataclasses, protocols, abstract classes, or registries are defined here.

### Inheritance / Composition / Dependency Relationships

- `main` composes the startup sequence from `AppConfig`, `configure_logging`, `QApplication`, `MainWindow`, and `apply_production_fixes`.
- Direct internal dependency relationships:
  - `locallama_gui.app` -> `locallama_gui.core.config.APP_NAME`
  - `locallama_gui.app` -> `locallama_gui.core.config.AppConfig`
  - `locallama_gui.app` -> `locallama_gui.core.logging.configure_logging`
  - `locallama_gui.app` -> `locallama_gui.ui.main_window.MainWindow`
  - `locallama_gui.app` -> `locallama_gui.ui.production_fixes.apply_production_fixes`
- Third-party dependencies:
  - `platformdirs`
  - `PySide6`

### Public / Internal API

- Public module-level function: `main()`.
- Imported symbols are dependencies rather than definitions originating in this file.
- No explicitly private functions/classes are defined.
- The `if __name__ == "__main__"` block exposes direct script execution and raises `SystemExit(main())`.

### Runtime / API Behavior

- Direct execution of the file invokes `main()` and passes its integer result to `SystemExit`.
- The startup path is intentionally sensitive to whether the user configuration file exists.
- First-run mode temporarily disables `MainWindow.refresh_backend` during construction by assigning a lambda, then restores the original method before continuing.
- Normal and first-run startup both call `apply_production_fixes`, `show`, and the Qt event loop.

### CLI / UI / Events

- CLI integration: uses `sys.argv` when constructing `QApplication`.
- UI integration: creates `MainWindow`, applies production fixes, shows the window.
- Event integration: starts the Qt event loop through `app.exec()`.
- No Qt signals, slots, callbacks, or event handlers are declared directly in this file.
- The temporary `refresh_backend` lambda is a callable substitution, but it is not declared as a Qt signal/slot/callback API.

### Configuration / Environment Dependencies

Direct environment dependencies:
- `QT_ENABLE_HIGHDPI_SCALING`, defaulted to `"1"` if absent.
- `QT_AUTO_SCREEN_SCALE_FACTOR`, defaulted to `"1"` if absent.

Direct configuration dependencies:
- `APP_NAME` is passed to `user_config_dir`.
- Literal organization name `"LocalLama"` is also passed to `user_config_dir`.
- `config.json` is used as the existence test for first-run detection.
- `AppConfig.load()` supplies the runtime configuration.
- `config.paths.logs_dir` supplies the logging destination.

### Error Handling

- A `try/finally` surrounds `MainWindow(config)`.
- Its purpose is to restore the original `MainWindow.refresh_backend` whether construction succeeds or fails.
- No exception is swallowed or transformed by this file.
- Other startup failures propagate to the caller.

### Directly Observed vs Inferred

**DIRECTLY OBSERVED**

- Both Qt scaling environment variables are set with `setdefault`.
- `config_path` is based on `user_config_dir(APP_NAME, "LocalLama") / "config.json"`.
- `first_run` is true exactly when that path does not exist at the time of the check.
- `AppConfig.load()` is called before `configure_logging`.
- `QApplication` is created with `sys.argv`.
- The application name is set to `MyLoAI Control Center`.
- The organization name is set to `LocalLama`.
- The Qt application attribute `AA_DontCreateNativeWidgetSiblings` is set.
- `MainWindow.refresh_backend` is temporarily replaced only when `first_run` is true.
- The original `refresh_backend` object is restored in `finally`.
- `apply_production_fixes` receives the window and `first_run` flag.
- The window is shown and the Qt event loop is executed.
- The event-loop result is returned from `main`.

**INFERRED**

- The `config.json` existence test is intended to distinguish first-run initialization from subsequent launches.
- The temporary `refresh_backend` replacement is intended to prevent backend refresh during first-run window construction, because the replacement is conditional on `first_run` and returns `None`.
- `main()` is the application's primary GUI startup routine, based on its orchestration of configuration, logging, Qt application creation, main-window construction, fixes, display, and event-loop execution.

**UNKNOWN / NOT DETERMINABLE FROM SOURCE**

- The exact configuration fields loaded by `AppConfig.load()`.
- Whether `AppConfig.load()` creates the configuration file when missing.
- The exact logging behavior and files opened by `configure_logging`.
- The exact behavior of `MainWindow.refresh_backend` outside this file.
- The exact behavior of `MainWindow(config)` and the resources it accesses.
- The exact behavior of `apply_production_fixes`.
- Whether the `Qt` environment variables affect this specific PySide6 runtime in all supported environments.
- The exact integer semantics returned by `QApplication.exec()` beyond the fact that the result is returned by `main`.

### Unresolved Items

- `AppConfig.load()` requires its own production-file audit for complete configuration API mapping.
- `configure_logging` requires its own production-file audit for complete logging behavior mapping.
- `MainWindow` requires its own production-file audit for complete UI startup and `refresh_backend` mapping.
- `apply_production_fixes` requires its own production-file audit for complete startup-fix behavior mapping.

STATUS: FULLY MAPPED
