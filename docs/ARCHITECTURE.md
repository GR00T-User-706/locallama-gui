# LocalLama Control Center Architecture

Date: 2026-08-17
Status: Canonical architecture reference for the active application.

## 1. Purpose and scope

LocalLama Control Center is a PySide6 desktop application that provides one UI over local Ollama and remote/provider-compatible LLM backends. The active implementation lives under `locallama_gui/`. The `archive/` tree is historical material and is not part of the production runtime.

This document describes the architecture that the current source implements. It is not a roadmap and does not grant archived code production status.

## 2. Runtime entry point

The supported Python entry point is:

```text
locallama-gui
```

which resolves to `locallama_gui.app:main`. The module entry point `python -m locallama_gui` is also supported by the package.

Startup flow:

```text
launcher / module
      |
      v
locallama_gui.app.main()
      |
      +--> AppConfig.load()
      |       |
      |       +--> configuration + schema migration
      |       +--> OS credential store for provider secrets
      |
      +--> configure_logging()
      |
      +--> QApplication
      |
      +--> MainWindow(config)
              |
              +--> managers
              +--> controllers
              +--> backend
              +--> UI / diagnostics
              |
              +--> restore state
              +--> load enabled plugins
              +--> create initial chat
              +--> refresh backend
```

## 3. Package boundaries

```text
locallama_gui/
├── app.py                         Application bootstrap
├── __main__.py                    Module launcher
├── backends/
│   ├── base.py                    Backend interface and common status
│   ├── manager.py                 Provider/backend selection
│   ├── ollama.py                  Ollama HTTP implementation
│   └── openai.py                  OpenAI-compatible implementation
├── core/
│   ├── config.py                  Persistent configuration and credentials
│   ├── domain.py                  Chat/model/agent/prompt data models
│   ├── logging.py                 Python logging configuration
│   └── managers.py                Sessions, prompts, agents, plugins
├── plugins/
│   └── __init__.py                Package boundary for plugin-related code
└── ui/
    ├── main_window.py             Main Qt composition root
    ├── chat_view.py               Chat rendering helpers
    ├── dialogs.py                 Feature dialogs
    ├── diagnostics.py             Logs, console, operations and stream parsing
    ├── theme.py                   UI stylesheet/theme helpers
    ├── workers.py                 Asynchronous Qt worker tasks
    └── controllers/
        ├── chat_controller.py     Chat/session actions
        ├── model_controller.py    Model operations
        └── plugin_controller.py   Plugin UI actions
```

## 4. Dependency direction

The intended dependency direction is:

```text
UI widgets
   |
   v
controllers
   |
   +--> managers/domain
   +--> backend factory
   |
   v
backends
```

`core.config` supplies persistent configuration and application paths. `core.domain` contains data structures shared by persistence, controllers, and UI. Backends expose the common `LLMBackend` interface defined in `backends/base.py`.

The `MainWindow` is the composition root. It constructs managers, controllers, the plugin context, and the backend-facing UI and wires Qt signals to those components.

## 5. Backend abstraction

`LLMBackend` defines the common operations used by the application:

- connection test
- model listing
- chat streaming
- model pull
- model push
- model delete
- model copy/clone
- model creation
- model metadata

Operations unsupported by a backend raise `NotImplementedError` rather than being silently emulated.

The backend manager selects the implementation from the active `ProviderProfile`. The active profile contains provider type, endpoint, default model and enablement state. Provider secrets are retrieved from the operating-system credential store rather than persisted in `config.json`.

## 6. Asynchronous execution

Network and model operations must not block the Qt event loop. Model streaming and asynchronous actions use the worker abstractions in `ui/workers.py` and controllers expose completion/error callbacks to the main window.

Model operations additionally feed `OperationStreamParser` and the Diagnostics Operations view so pull/push/clone/create/delete have observable lifecycle state.

## 7. Persistence model

Application configuration is stored under the platform-specific `platformdirs` configuration location.

Application data is separated into directories for:

- sessions
- prompts
- agents
- Modelfiles
- plugins
- logs

Chat sessions are serialized through `ChatSession`. Prompt and agent managers own their JSON data files. Modelfile versions are stored below the Modelfiles data directory.

The configuration file has an explicit `schema_version`. `pyproject.toml` remains the application/package version source, while configuration schema version is independent and tracks persisted-data compatibility.

## 8. Configuration and credentials

The current configuration schema version is `2`.

`AppConfig.load()`:

1. creates platform paths;
2. loads `config.json` when present;
3. validates the top-level JSON object;
4. rejects unsupported future schema versions;
5. migrates known older schema versions;
6. loads provider metadata;
7. retrieves provider secrets from the OS credential store;
8. rewrites migrated configuration in the current schema.

`AppConfig.save()` always emits the current schema version and excludes API keys from the JSON representation.

## 9. Plugin trust boundary

Plugins are Python modules and therefore have arbitrary code-execution capability once imported. Discovery must not import plugin code.

The production lifecycle is:

```text
plugin file
   |
   v
static AST manifest discovery
   |
   v
manifest validation
   |
   +--> trust decision
   |
   v
explicit enable
   |
   v
module import
   |
   v
runtime manifest validation
   |
   v
Plugin.activate(context)
```

The manager therefore separates metadata discovery from execution. An untrusted plugin cannot be enabled. Invalid plugins are isolated from automatic startup loading.

Supported lifecycle operations are:

```text
discover -> validate -> trust -> enable -> disable -> reload
                                      |
                                      +-> untrust -> remove
```

`remove` disables/untrusts the plugin, removes its persisted enablement/trust state, and deletes the plugin file when present.

## 10. Plugin capability surface

`PluginContext` is the application boundary exposed to loaded plugins. It currently provides registration points for:

- tools
- commands
- chat interceptors
- memory providers
- UI panels

Plugin code should use this context rather than reaching into unrelated application internals.

## 11. UI composition

`MainWindow` owns the primary Qt surface and creates:

- chat tabs
- model table
- chat-session list
- system-prompt dock
- diagnostics docks
- request viewer
- token/response viewer
- toolbar
- menus

Menus expose File, Models, Agents, Plugins, Settings, View, Developer and Help workflows. Feature-specific dialogs live in `ui/dialogs.py`.

## 12. Chat and session flow

```text
user input
   |
   v
ChatController
   |
   +--> current ChatSession
   +--> active ProviderProfile
   +--> GenerationParameters
   |
   v
backend.chat(...)
   |
   v
StreamTask / response stream
   |
   +--> chat rendering
   +--> token viewer
   +--> request diagnostics
   |
   v
session state
   |
   v
SessionManager.save()
```

Internal application system context is kept distinct from user-visible chat content and request diagnostics support redaction of that internal system prompt.

## 13. Diagnostics

Diagnostics has three principal surfaces:

- Logs: structured Python logging records;
- Console: captured stdout/stderr;
- Operations: model-operation lifecycle and status history.

Request and token viewers are separate diagnostic surfaces. Diagnostics should report failures without crashing the main application.

## 14. Themes and UI state

Theme selection is persisted through `UISettings`. Main-window geometry/state and the active session are restored through the same settings model. The current UI stylesheet implementation is in `ui/theme.py` and is applied by `MainWindow`.

## 15. Packaging boundary

Packaging metadata is defined in `pyproject.toml`. The project installs the `locallama-gui` console entry point. Linux desktop integration is kept under `packaging/linux/` and the launcher installation helpers are under `scripts/`.

## 16. Testing boundary

Tests live under `tests/` and cover backend behavior, configuration, chat view/controller behavior, diagnostics, model operations and security boundaries. P1 plugin lifecycle tests exercise discovery, validation, trust, enable, disable, reload, untrust and removal.

## 17. Architectural invariants

1. Archived code is not production code.
2. UI actions should delegate feature behavior to controllers/managers rather than duplicating backend logic.
3. Backend-specific behavior belongs behind `LLMBackend` implementations.
4. Network/model work must not block the Qt event loop.
5. Plugin discovery must not execute plugin code.
6. Plugin execution requires explicit trust.
7. Provider API keys must not be persisted in `config.json`.
8. Configuration schema changes require a migration boundary and regression coverage.
9. Persistent data compatibility must be treated separately from application package versioning.
10. Diagnostics should make asynchronous operations and failures observable.
