# LocalLama Control Center
## Read-Only Architecture & Codebase Audit

**Repository:** `GR00T-User-706/locallama-gui`  
**Branch:** `feat/myloai-production-packaging`  
**Audit mode:** READ-ONLY  
**Generated:** 2026-09-10

> No repository files were modified by this audit.

## 1. Executive Architecture

```text
Chat UI
  -> ChatController
  -> MainWindow._generate()
  -> AppConfig.active_profile()
  -> create_backend()
  -> logical message assembly
  -> PluginContext.chat_interceptors
  -> GenerationParameters.to_backend_options()
  -> backend request construction
  -> LLMBackend.chat()
  -> HTTP provider
  -> StreamTask
  -> token/error/completion callbacks
  -> session persistence
```

The existing `chat_interceptors` hook occurs after the application system prompt and session messages are assembled, but before backend-specific request construction. This is currently the strongest existing hook for a provider-independent memory plugin.

## 2. Configuration

### `locallama_gui/core/config.py`

**Constants**
- `APP_NAME = "locallama-gui"`
- `CONFIG_SCHEMA_VERSION = 2`
- `APP_SYSTEM_PROMPT`

**CredentialStore**
- `_username(profile)`
- `get(profile)`
- `set(profile, api_key)`
- Uses OS keyring storage.

**AppPaths**
- `config_dir`
- `data_dir`
- `logs_dir`
- `sessions_dir`
- `prompts_dir`
- `agents_dir`
- `modelfiles_dir`
- `plugins_dir`

**ProviderProfile**
- `name`
- `provider_type`
- `base_url`
- `api_key`
- `default_model`
- `enabled`

**GenerationParameters**
- `temperature`
- `top_k`
- `top_p`
- `min_p`
- `repeat_penalty`
- `repeat_last_n`
- `mirostat`
- `mirostat_eta`
- `mirostat_tau`
- `tfs_z`
- `num_predict`
- `seed`
- `stop`
- `num_ctx`
- `num_batch`
- `num_gpu`
- `reasoning_mode`
- `thinking_mode`
- `plan_mode`
- `normal_mode`

Methods:
- `__post_init__`
- `to_backend_options`

**UISettings**
- `theme`
- `geometry_hex`
- `state_hex`
- `active_session_id`
- `font_size`

**AppConfig**
- `paths`
- `schema_version`
- `provider_profiles`
- `active_provider`
- `parameters`
- `parameter_presets`
- `enabled_plugins`
- `trusted_plugins`
- `developer_mode`
- `ui`
- `global_system_prompt`

Methods:
- `file_path`
- `_migrate_data`
- `load`
- `save`
- `active_profile`

Configuration JSON excludes API keys and the file is chmod'ed to `0600` where supported.

## 3. Persistence Managers

### `SessionManager`
Methods:
- `list_sessions`
- `load`
- `save`
- `import_session`

Sessions are stored as JSON files under the sessions directory.

### `PromptManager`
Methods:
- `list`
- `save_all`
- `upsert`
- `delete`
- `import_file`
- `export`

### `AgentManager`
Methods:
- `list`
- `save_all`
- `upsert`

## 4. Plugin API

### `PluginAPI`
- `manifest`
- `activate(context)`
- `deactivate()`

### `PluginContext`
Exposes:
- `main_window`
- `config`
- `tools`
- `commands`
- `chat_interceptors`
- `memory_providers`

Registration:
- `register_tool`
- `register_command`
- `register_chat_interceptor`
- `add_panel`

### Important finding

`memory_providers` already exists, but there is no corresponding `register_memory_provider()` method.

**Classification:** PLUGIN API / IMPLEMENTATION GAP

The intended memory-provider contract therefore needs to be determined before implementation.

## 5. Plugin Lifecycle

`PluginManager` methods:
- `_validate_manifest`
- `_read_static_manifest`
- `plugin_paths`
- `discover`
- `load_enabled`
- `trust`
- `untrust`
- `enable`
- `disable`
- `reload`
- `remove`
- `_load_module`

Notable behavior:
1. Plugin manifests are parsed with AST before execution.
2. Required manifest keys are `id`, `name`, and `version`.
3. Plugins must be trusted before enabling.
4. Runtime manifests are revalidated.
5. Runtime and discovered plugin IDs must match.
6. Activation receives the shared `PluginContext`.

## 6. Backend API

### `LLMBackend`

Abstract:
- `test_connection()`
- `list_models()`
- `chat(model, messages, options, stream)`

Default unsupported operations:
- `pull_model`
- `push_model`
- `delete_model`
- `copy_model`
- `create_model`
- `show_model`

### Backend factory

`create_backend(profile)` maps:
- `openai` -> `OpenAICompatibleBackend`
- `llama.cpp` -> `OpenAICompatibleBackend`
- everything else -> `OllamaBackend`

### Ollama backend

Key methods:
- `sanitize_options`
- `sanitize_request_fields`
- `build_chat_payload`
- `test_connection`
- `list_models`
- `chat`
- `pull_model`
- `push_model`
- `delete_model`
- `copy_model`
- `create_model`
- `show_model`
- `_stream_endpoint`

Endpoints include:
- `/api/tags`
- `/api/chat`
- `/api/pull`
- `/api/push`
- `/api/delete`
- `/api/copy`
- `/api/create`
- `/api/show`

## 7. Chat Controller

### `ChatWindowPort`
- `current_tab`
- `set_tab_title`
- `render_tab`
- `generate_for_tab`
- `refresh_sessions`
- `log`
- `open_session`

### `ChatController`
- `save_current`
- `open_chat_file`
- `send_message`
- `regenerate`
- `retry`
- `copy_last_message`
- `edit_message`
- `delete_message`

`send_message()` appends the user message, updates the tab title, renders, and requests generation.

`regenerate()` removes the final assistant message when present and requests generation again.

`retry()` delegates to `regenerate()`.

## 8. Main Window

### `ChatTab`
State/widgets:
- session
- chat
- input
- streaming
- send
- stop
- regen
- retry
- copy_last
- edit_msg
- delete_msg

Methods:
- `render`
- `set_generating`

### `ComposerTextEdit`
Signals:
- `send_requested`
- `zoom_requested`

Overrides:
- `keyPressEvent`
- `wheelEvent`

### `MainWindow`
Important state:
- config
- sessions
- prompts
- agents
- plugin_context
- plugins
- models
- chat_controller
- model_controller
- plugin_controller
- worker_refs
- current_stream
- `_stream_owner_seq`
- `_active_stream_owner`
- diagnostics state
- original stdout/stderr

Initialization:
```text
_build_ui()
_install_diagnostics_sinks()
_build_menus()
_restore_state()
plugins.load_enabled()
new_chat()
refresh_backend()
```

## 9. Exact Current Request Path

```text
ChatTab
  |
  v
ChatController.send_message()
  |
  v
MainWindow.generate_for_tab()
  |
  v
MainWindow._generate(tab)
  |
  +--> config.active_profile()
  |
  +--> create_backend(profile)
  |
  +--> select model
  |
  +--> update session model/provider
  |
  +--> create APP_SYSTEM_PROMPT message
  |
  +--> append session messages
  |
  +--> run chat_interceptors
  |
  +--> GenerationParameters.to_backend_options()
  |
  +--> backend-specific request payload
  |
  +--> redacted diagnostics request
  |
  +--> create StreamTask
  |
  v
backend.chat()
  |
  v
provider HTTP endpoint
```

## 10. Streaming

```text
StreamTask
  -> token callback
  -> _append_token()
  -> assistant message accumulation
  -> token viewer

error
  -> _stream_error()
  -> clear state
  -> log/display error

completion
  -> _stream_done()
  -> save session
  -> refresh sessions

stop
  -> stop_generation()
  -> cancel current stream
```

## 11. Diagnostics

Current UI includes:
- Models
- Chat Sessions
- System Prompts
- Logs
- Console
- Operations
- Redacted Request Viewer
- Token/Response Viewer

Diagnostics classes/functions include:
- `DiagnosticsSignals`
- `LineBufferedStream`
- `OperationStreamParser`
- `OperationUpdate`
- `QtLogHandler`
- `append_output`

A memory plugin must respect the existing request-redaction boundary and should not dump raw sensitive memory into diagnostics.

## 12. Branch State

Previously established branch state:

```text
main
  HEAD: 86e3ec01cc3e18e1c3d0ec41d22a95e2aa006154

feat/myloai-production-packaging
  HEAD: 5e2c520426386084d795779f3121a3a856d4459a

merge base:
  e2f0d56...
```

The live branch was previously measured as:
- 116 commits ahead of `main`
- 11 commits behind `main`

The live branch contains production packaging, release CI, setup wizard work, model browser work, production fixes, plugin SDK/docs, configuration, startup/runtime work, and other changes beyond the older branch state.

## 13. Major Production Tree Areas

```text
.github/
  agents/
  prompts/
  workflows/

archive/
docs/

locallama_gui/
  backends/
  core/
  ui/

packaging/
scripts/
tests/
```

Important UI modules identified:
```text
ui/chat_view.py
ui/controllers/chat_controller.py
ui/controllers/model_controller.py
ui/controllers/plugin_controller.py
ui/diagnostics.py
ui/dialogs.py
ui/main_window.py
ui/model_browser.py
ui/production_fixes.py
ui/setup_wizard.py
ui/theme.py
ui/workers.py
```

## 14. Memory Plugin Architectural Finding

The current architecture already supports:

```text
Memory provider
      |
      v
chat interceptor
      |
      v
logical ChatMessage list
      |
      v
backend adapter
```

The strongest existing interception layer is the chat-interceptor stage immediately before backend request construction.

Avoid putting memory logic directly inside `OllamaBackend` or `OpenAICompatibleBackend`, because that would couple memory behavior to transport/provider implementations.

Before changing code, the remaining architectural questions are:
- memory-provider protocol
- provider registration API
- memory record schema
- persistence ownership
- retrieval/ranking contract
- injection policy
- memory privacy boundary
- deletion/forgetting semantics
- session versus global memory
- regenerate/retry semantics
- whether a dedicated context builder should eventually replace the raw interceptor

## 15. Complete Inventory Still Required for a Truly Exhaustive Map

The final machine-generated inventory should enumerate across both refs:

```text
every module
every import
every class
every method
every function
every property
every dataclass and field
every Protocol / ABC
every constant
every class attribute
every instance attribute assignment
every environment-variable reference
every filesystem path construction
every HTTP endpoint
every CLI entry point
every plugin hook
every backend method
every worker boundary
every Qt signal/slot
every persistence operation
every test target
every branch-specific symbol difference
```

This is best generated with AST analysis rather than maintained manually.

## 16. Audit Integrity

This is an audit/report only. No source code, configuration, branch, commit, or repository state was changed.
