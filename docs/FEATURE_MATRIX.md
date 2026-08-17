# Feature Matrix and Application Contract

Date: 2026-08-17
Scope: Entire active application under `locallama_gui/`.

This is the canonical contract for visible application capabilities. A row describes behavior the application is expected to provide. Status reflects the current implementation state, not a promise about every backend/environment.

## Status meanings

- **implemented** — the active code contains the complete application path for the action.
- **partial** — the visible workflow exists but an important part is intentionally incomplete or backend-dependent.
- **blocked** — the UI/path exists but cannot complete the requested contract yet.
- **hidden** — implementation exists without an appropriate primary visible entry point.

Backend availability, authentication, model availability, desktop environment, and external services can still determine runtime success.

## 1. Application lifecycle

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Launch | `locallama-gui` | implemented | Starts the Qt application through the package console entry point. | `app.py`, `pyproject.toml` |
| Launch | `python -m locallama_gui` | implemented | Starts the same application module entry point. | `app.py`, `__main__.py` |
| Startup | Configuration load | implemented | Loads/migrates current configuration before the main window is constructed. | `core/config.py` |
| Startup | Logging setup | implemented | Configures application logging before window creation. | `core/logging.py` |
| Startup | Initial chat | implemented | Main window creates an initial chat tab. | `ui/main_window.py` |
| Startup | Backend refresh | implemented | Startup initiates backend/model refresh. | `ui/main_window.py` |
| Startup | Missing backend | implemented | Backend failure must remain non-crashing and visible through status/diagnostics. | `ui/main_window.py`, `backends/` |

## 2. Providers and backend connectivity

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Providers | Active provider selection | implemented | User can select an enabled provider profile from the toolbar. | `ui/main_window.py`, `core/config.py` |
| Providers | Ollama backend | implemented | Uses the common backend interface for connection, models and chat/model operations. | `backends/ollama.py` |
| Providers | OpenAI-compatible backend | implemented | Uses the common backend interface for connection/model/chat behavior supported by the implementation. | `backends/openai.py` |
| Providers | Connection test | implemented | Backend exposes an asynchronous connection test/status model. | `backends/base.py`, backend implementations |
| Providers | Endpoint configuration | implemented | Endpoint dialog creates/updates/removes provider profiles. | `ui/dialogs.py` |
| Providers | API credential storage | implemented | API keys are stored through the OS credential store and omitted from `config.json`. | `core/config.py` |

## 3. Models

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Models | Refresh | implemented | Refreshes backend model list asynchronously and updates model UI. | `ui/main_window.py`, backend implementations |
| Models | Select | implemented | Toolbar model selection changes the active chat model. | `ui/main_window.py` |
| Models | Pull | implemented | Prompts for model name, streams operation status, reports errors, then refreshes. | `ui/controllers/model_controller.py` |
| Models | Push | implemented | Prompts for model name, streams operation status and reports errors. | `ui/controllers/model_controller.py` |
| Models | Clone | implemented | Requires source selection and destination name, then runs backend copy asynchronously. | `ui/controllers/model_controller.py` |
| Models | Delete | implemented | Requires selection and destructive confirmation before asynchronous deletion. | `ui/controllers/model_controller.py` |
| Models | Create | implemented | Opens Modelfile editor and delegates build to the backend path. | `ui/dialogs.py`, `ui/main_window.py` |
| Models | Modelfile New/Open/Save | implemented | Editor supports file creation, opening and saving. | `ui/dialogs.py` |
| Models | Modelfile Duplicate | implemented | Duplicates current editor content into a new version/name path. | `ui/dialogs.py` |
| Models | Modelfile Validate | implemented | Validates required/recognized directives and reports errors. | `ui/dialogs.py` |
| Models | Modelfile Preview | implemented | Displays parsed system/parameter/template content. | `ui/dialogs.py` |
| Models | Model metadata/Templates | implemented | Selected model metadata can be loaded and displayed through the model UI. | `ui/main_window.py`, backend implementations |

## 4. Chat

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Chat | New chat | implemented | Creates a new `ChatSession` and tab. | `ui/main_window.py`, `core/domain.py` |
| Chat | Send | implemented | Sends the visible conversation through the active backend. | `ui/controllers/chat_controller.py` |
| Chat | Streaming | implemented | Streams backend output through Qt worker infrastructure. | `ui/workers.py`, `ui/main_window.py` |
| Chat | Stop | implemented | Stops active generation and releases active stream ownership. | `ui/main_window.py` |
| Chat | Retry | implemented | Reuses the expected prior user turn and regenerates. | `ui/controllers/chat_controller.py` |
| Chat | Regenerate | implemented | Regenerates the last assistant response from conversation state. | `ui/controllers/chat_controller.py` |
| Chat | Edit message | implemented | Edits a selected visible message without exposing internal system messages. | `ui/controllers/chat_controller.py` |
| Chat | Delete message | implemented | Deletes a selected visible message without deleting internal system messages. | `ui/controllers/chat_controller.py` |
| Chat | Copy last | implemented | Copies the latest visible response to the clipboard. | `ui/main_window.py` |
| Chat | Request viewer | implemented | Displays a redacted outbound request representation. | `ui/main_window.py`, `ui/chat_view.py` |
| Chat | Token/response viewer | implemented | Displays active streamed response/token output. | `ui/main_window.py` |

## 5. Sessions and persistence

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Sessions | Save | implemented | Persists the current `ChatSession`. | `chat_controller.py`, `core/managers.py` |
| Sessions | Save As | implemented | Saves the current session to a user-selected destination. | `ui/main_window.py` |
| Sessions | Open | implemented | Loads a session file and opens it in the UI. | `ui/main_window.py`, `SessionManager` |
| Sessions | Session list | implemented | Lists valid saved sessions and ignores malformed entries. | `SessionManager` |
| Sessions | Import | implemented | Imports a valid session into application session storage. | `SessionManager`, `ui/main_window.py` |
| Sessions | Export | implemented | Writes session data for external use. | `ui/main_window.py` |
| Sessions | Active session restoration | implemented | UI settings persist the active session identifier. | `core/config.py`, `ui/main_window.py` |

## 6. Prompts

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Prompts | Prompt dock | implemented | Lists stored prompts and applies a selected prompt to current chat. | `ui/main_window.py` |
| Prompts | Create | implemented | Prompt Manager creates a new prompt. | `ui/dialogs.py`, `PromptManager` |
| Prompts | Save/update | implemented | Saves prompt content and records prior content in version history. | `PromptManager` |
| Prompts | Delete | implemented | Removes a prompt by ID. | `PromptManager` |
| Prompts | Import | implemented | Imports text into a prompt record. | `PromptManager` |
| Prompts | Export | implemented | Exports stored prompt data. | `PromptManager` |
| Prompts | Version history | implemented | Prompt updates retain prior content with timestamps. | `PromptManager` |

## 7. Agents

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Agents | Create | implemented | Agent Builder creates an `AgentProfile`. | `ui/dialogs.py`, `AgentManager` |
| Agents | Manage | implemented | Existing agent profiles can be loaded and edited. | `AgentBuilderDialog` |
| Agents | Save | implemented | Agent profiles persist to JSON. | `AgentManager` |
| Agents | Import | implemented | Agent JSON can be imported. | `AgentBuilderDialog` |
| Agents | Export | implemented | Current agent can be exported as JSON. | `AgentBuilderDialog` |
| Agents | Execution integration | partial | Profiles contain model/reasoning/behavior/memory/tool/plugin policy fields, but the active chat path does not yet make those profiles the generation/execution authority. | `core/domain.py`, `ui/dialogs.py`, chat/controller paths |

## 8. Plugins

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Plugins | Install | partial | Copies a selected Python file into the configured plugin directory; trust/enable remain separate lifecycle operations. | `ui/controllers/plugin_controller.py` |
| Plugins | Discover | implemented | Reads static manifests without importing plugin code. | `PluginManager` |
| Plugins | Validate | implemented | Requires manifest `id`, `name`, and `version`, with runtime ID consistency validation. | `PluginManager` |
| Plugins | Trust | implemented | Explicitly records trust for a valid discovered plugin. | `PluginManager` |
| Plugins | Enable | implemented | Requires trust, then imports and activates the plugin. | `PluginManager` |
| Plugins | Disable | implemented | Calls plugin deactivation and persists disabled state. | `PluginManager` |
| Plugins | Reload | implemented | Disables loaded plugins and reloads enabled plugins. | `PluginManager` |
| Plugins | Untrust | implemented | Disables the plugin and removes persisted trust. | `PluginManager` |
| Plugins | Remove | implemented | Disables/untrusts, clears persisted state, and removes the plugin file. | `PluginManager` |
| Plugins | Plugin context | implemented | Provides tool, command, chat-interceptor, memory-provider and UI-panel registration points. | `PluginContext` |
| Plugins | Startup isolation | implemented | Invalid or failing enabled plugins are skipped instead of preventing application startup. | `PluginManager.load_enabled()` |

## 9. Parameters

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Parameters | Edit | implemented | Parameter dialog edits generation parameters. | `ui/dialogs.py` |
| Parameters | Save | implemented | Parameter values persist through `AppConfig`. | `core/config.py` |
| Parameters | Presets | implemented | Presets can be saved and loaded. | `ParameterDialog` |
| Parameters | Reasoning mode | implemented | Reasoning mode is represented by a controlled enum and maps to supported backend options. | `GenerationParameters` |

## 10. Themes and view

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Themes | Theme toggle | implemented | Settings exposes theme switching and the selected theme is persisted. | `ui/main_window.py`, `ui/theme.py` |
| View | Docks | implemented | Models, sessions, prompts, diagnostics, request and token views are dockable. | `ui/main_window.py` |
| View | Window state | implemented | Geometry/state is persisted through `UISettings`. | `core/config.py`, `ui/main_window.py` |
| View | Font size | implemented | UI font size is part of persisted UI settings. | `core/config.py`, `ui/theme.py` |

## 11. Diagnostics and developer tools

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Diagnostics | Logs | implemented | Structured Python logging is displayed in the Logs dock. | `ui/diagnostics.py` |
| Diagnostics | Console | implemented | stdout/stderr capture is displayed in the Console dock. | `ui/diagnostics.py`, `ui/main_window.py` |
| Diagnostics | Operations | implemented | Model operation lifecycle/status history is displayed separately. | `ui/diagnostics.py`, `ui/main_window.py` |
| Diagnostics | Request copy/clear | implemented | Request Viewer provides copy and clear actions. | `ui/main_window.py` |
| Diagnostics | Token copy/clear | implemented | Token Viewer provides copy and clear actions. | `ui/main_window.py` |
| Developer | Plugin SDK documentation | implemented | Plugin documentation can be opened when available. | `ui/main_window.py` |
| Developer | Documentation/help | implemented | Help paths report missing/unreadable documentation without crashing. | `ui/main_window.py` |

## 12. Configuration and security

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Config | Schema version | implemented | Persisted config includes an explicit schema version independent of package version. | `core/config.py` |
| Config | Migration | implemented | Known older configuration is normalized to the current schema. | `AppConfig._migrate_data()` |
| Config | Future-version rejection | implemented | Config written by a newer unsupported schema is rejected rather than silently corrupted. | `AppConfig._migrate_data()` |
| Security | API-key persistence | implemented | API keys are excluded from `config.json` and stored through keyring. | `CredentialStore`, `AppConfig` |
| Security | Config permissions | implemented | Config file attempts to use mode `0600` on supported platforms. | `AppConfig.save()` |
| Security | Plugin discovery boundary | implemented | Static AST inspection separates discovery from executable plugin import. | `PluginManager` |

## 13. Desktop integration

| Area | Action | Status | Contract / current behavior | Primary implementation |
|---|---|---|---|---|
| Desktop | Launcher script | implemented | Repository launcher delegates to the application entry point. | `run-locallama` |
| Desktop | Linux desktop entry | implemented | Desktop-entry metadata is maintained under packaging. | `packaging/linux/` |
| Desktop | Launcher installation | implemented | Installation helper installs the launcher into the user environment. | `scripts/install-launcher` |
| Desktop | Desktop-entry installation | implemented | Installation helper installs the Linux desktop entry. | `scripts/install-desktop-entry` |

## 14. Contract rules

1. Rows marked **implemented** must remain represented by active production code under `locallama_gui/`.
2. Archived implementations must not be used as evidence that a current feature works.
3. A backend-dependent operation is implemented when the application path validates input, delegates through the backend abstraction, handles asynchronous completion/error, and updates relevant UI state. Backend availability is an environmental prerequisite.
4. A feature marked **partial** must not be described elsewhere as fully integrated.
5. Changes to visible capabilities must update this matrix and the QA checklist in the same change set.
6. Configuration schema changes require migration coverage and documentation.
7. Plugin lifecycle changes require lifecycle regression coverage.
