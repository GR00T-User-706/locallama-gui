# LocalLama Exhaustive Codebase Mapping
## Executed Read-Only Inventory

**Repository:** `GR00T-User-706/locallama-gui`  
**Audited branch:** `feat/myloai-production-packaging`  
**Comparison branch:** `main`  
**Feature HEAD:** `5e2c520426386084d795779f3121a3a856d4459a`  
**Main HEAD:** `86e3ec01cc3e18e1c3d0ec41d22a95e2aa006154`  
**Merge base:** `e2f0d56ab3c4cde2e8ec291f45e60f940fedf55a`  
**Audit mode:** read-only  
**Inventory basis:** repository source at the refs above

> This is the executed inventory requested by `LocalLama_Exhaustive_Codebase_Mapping.md`. It records verified source structure rather than proposing architecture changes.

---

# 1. Repository / Branch Status

GitHub reports the feature branch as:

- **116 commits ahead** of `main`
- **11 commits behind** `main`
- **116 commits in the comparison range**
- status: `diverged`

The comparison reports 40 changed files at the file-diff level.

### Changed files

| Status | File |
|---|---|
| added | `.github/workflows/release-packaging.yml` |
| modified | `CHANGELOG.md` |
| modified | `README.md` |
| modified | `docs/LAUNCHING.md` |
| modified | `docs/PLUGIN_SDK.md` |
| added | `docs/qa/WINDOWS-VM-2026-09-09.md` |
| modified | `locallama_gui/__init__.py` |
| modified | `locallama_gui/__main__.py` |
| modified | `locallama_gui/app.py` |
| modified | `locallama_gui/core/logging.py` |
| added | `locallama_gui/ui/model_browser.py` |
| added | `locallama_gui/ui/production_fixes.py` |
| added | `locallama_gui/ui/setup_wizard.py` |
| modified | `packaging/README.md` |
| added | `packaging/RELEASE_BUILD_SPEC.md` |
| added | `packaging/RELEASE_PAYLOAD.md` |
| added | `packaging/USER_MANUAL.md` |
| added | `packaging/assets/generate_myloai_icon.py` |
| added | `packaging/check-release-payload.py` |
| added | `packaging/linux/PKGBUILD` |
| added | `packaging/linux/appimage/README.md` |
| added | `packaging/linux/appimage/build-appimage.sh` |
| added | `packaging/linux/appimage/myloai.svg` |
| added | `packaging/linux/com.github.gr00t-user-706.locallama-gui.desktop` |
| added | `packaging/linux/debian/README.Debian` |
| added | `packaging/linux/debian/build-deb.sh` |
| added | `packaging/linux/install-myloai.sh` |
| added | `packaging/linux/myloai` |
| added | `packaging/linux/myloai.1` |
| added | `packaging/linux/myloai.desktop` |
| added | `packaging/macos/README.md` |
| added | `packaging/macos/build-dmg.sh` |
| added | `packaging/pyinstaller/myloai.spec` |
| added | `packaging/windows/MyLoAI.iss` |
| added | `packaging/windows/README.md` |
| added | `packaging/windows/build-installer.ps1` |
| modified | `pyproject.toml` |

---

# 2. Active Runtime Boundary

The active production runtime is `locallama_gui/**`.

The repository's own production map identifies the archived trees as historical-only:

- `archive/legacy_code/llm_studio/`
- `archive/old_apps/ollama_GUI/`

The active runtime path is:

```text
locallama_gui.app:main
        │
        ▼
    AppConfig
        │
        ▼
   MainWindow
        │
        ├── Controllers
        ├── Managers
        ├── Workers
        ├── Plugin system
        └── Backends
                │
                ├── Ollama HTTP API
                └── OpenAI-compatible HTTP API
```

---

# 3. Inventory #1 — Every Active Python Module

## Application package

| Module | File |
|---|---|
| `locallama_gui` | `locallama_gui/__init__.py` |
| `locallama_gui.__main__` | `locallama_gui/__main__.py` |
| `locallama_gui.app` | `locallama_gui/app.py` |

## Backends

| Module | File |
|---|---|
| `locallama_gui.backends` | `locallama_gui/backends/__init__.py` |
| `locallama_gui.backends.base` | `locallama_gui/backends/base.py` |
| `locallama_gui.backends.manager` | `locallama_gui/backends/manager.py` |
| `locallama_gui.backends.ollama` | `locallama_gui/backends/ollama.py` |
| `locallama_gui.backends.openai` | `locallama_gui/backends/openai.py` |

## Core

| Module | File |
|---|---|
| `locallama_gui.core` | `locallama_gui/core/__init__.py` |
| `locallama_gui.core.config` | `locallama_gui/core/config.py` |
| `locallama_gui.core.domain` | `locallama_gui/core/domain.py` |
| `locallama_gui.core.logging` | `locallama_gui/core/logging.py` |
| `locallama_gui.core.managers` | `locallama_gui/core/managers.py` |

## UI

| Module | File |
|---|---|
| `locallama_gui.ui` | `locallama_gui/ui/__init__.py` |
| `locallama_gui.ui.chat_view` | `locallama_gui/ui/chat_view.py` |
| `locallama_gui.ui.controllers` | `locallama_gui/ui/controllers/__init__.py` |
| `locallama_gui.ui.controllers.chat_controller` | `locallama_gui/ui/controllers/chat_controller.py` |
| `locallama_gui.ui.controllers.model_controller` | `locallama_gui/ui/controllers/model_controller.py` |
| `locallama_gui.ui.controllers.plugin_controller` | `locallama_gui/ui/controllers/plugin_controller.py` |
| `locallama_gui.ui.diagnostics` | `locallama_gui/ui/diagnostics.py` |
| `locallama_gui.ui.dialogs` | `locallama_gui/ui/dialogs.py` |
| `locallama_gui.ui.main_window` | `locallama_gui/ui/main_window.py` |
| `locallama_gui.ui.model_browser` | `locallama_gui/ui/model_browser.py` |
| `locallama_gui.ui.production_fixes` | `locallama_gui/ui/production_fixes.py` |
| `locallama_gui.ui.setup_wizard` | `locallama_gui/ui/setup_wizard.py` |
| `locallama_gui.ui.theme` | `locallama_gui/ui/theme.py` |
| `locallama_gui.ui.workers` | `locallama_gui/ui/workers.py` |

## Plugin

| Module | File |
|---|---|
| sample plugin | `plugins/sample_plugin.py` |

## Packaging Python

| Module/script | File |
|---|---|
| icon generator | `packaging/assets/generate_myloai_icon.py` |
| release payload checker | `packaging/check-release-payload.py` |

---

# 4. Inventory #2 — Imports

## `locallama_gui.app`

Imports:

- `os`
- `sys`
- `Path`
- `platformdirs.user_config_dir`
- `PySide6.QtCore.Qt`
- `PySide6.QtWidgets.QApplication`
- `APP_NAME`
- `AppConfig`
- `configure_logging`
- `MainWindow`
- `apply_production_fixes`

## `locallama_gui.core.config`

Imports:

- `json`
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `pathlib.Path`
- `typing.Any`
- `keyring`
- `keyring.errors.KeyringError`
- `keyring.errors.PasswordDeleteError`
- `platformdirs.user_config_dir`
- `platformdirs.user_data_dir`
- `platformdirs.user_log_dir`

## `locallama_gui.core.domain`

Imports:

- `json`
- `uuid`
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.UTC`
- `datetime.datetime`
- `pathlib.Path`
- `typing.Any`
- `typing.Literal`

## `locallama_gui.core.managers`

Imports:

- `ast`
- `importlib.util`
- `json`
- `shutil`
- `dataclasses.asdict`
- `pathlib.Path`
- `types.ModuleType`
- `typing.Any`
- `typing.Protocol`
- `AppConfig`
- `AgentProfile`
- `ChatSession`
- `PromptRecord`
- `now_iso`

## `locallama_gui.backends.base`

Imports:

- `abc.ABC`
- `abc.abstractmethod`
- `collections.abc.AsyncIterator`
- `dataclasses.dataclass`
- `typing.Any`
- `ChatMessage`
- `ModelInfo`

## `locallama_gui.backends.manager`

Imports:

- `LLMBackend`
- `OllamaBackend`
- `OpenAICompatibleBackend`
- `ProviderProfile`

## `locallama_gui.backends.ollama`

Imports:

- `json`
- `time`
- `collections.abc.AsyncIterator`
- `typing.Any`
- `typing.ClassVar`
- `httpx`
- `BackendStatus`
- `LLMBackend`
- `ChatMessage`
- `ModelInfo`

## `locallama_gui.backends.openai`

Imports:

- `json`
- `time`
- `collections.abc.AsyncIterator`
- `typing.Any`
- `httpx`
- `BackendStatus`
- `LLMBackend`
- `ChatMessage`
- `ModelInfo`

## `locallama_gui.ui.chat_view`

Imports:

- `dataclasses.dataclass`
- `ChatMessage`

## `locallama_gui.ui.controllers.chat_controller`

Imports:

- `pathlib.Path`
- `typing.Protocol`
- `ChatMessage`
- `ChatSession`
- `message_is_internal_system`

Also uses dynamic imports of:

- `PySide6.QtWidgets.QFileDialog`
- `PySide6.QtWidgets.QApplication`
- `PySide6.QtWidgets.QInputDialog`

## `locallama_gui.ui.controllers.model_controller`

Imports:

- `typing.Protocol`
- `create_backend`
- `OperationStreamParser`
- `StreamTask`

Also dynamically imports `QInputDialog` and `QMessageBox`.

## `locallama_gui.ui.controllers.plugin_controller`

Imports:

- `pathlib.Path`
- `typing.Protocol`

Also dynamically imports `QFileDialog`.

## `locallama_gui.ui.diagnostics`

Imports:

- `json`
- `logging`
- `dataclasses.dataclass`
- `typing.TextIO`
- `PySide6.QtCore.QObject`
- `PySide6.QtCore.Signal`
- `PySide6.QtGui.QTextCursor`
- `PySide6.QtWidgets.QPlainTextEdit`

## `locallama_gui.ui.dialogs`

Imports:

- `dataclasses.asdict`
- `pathlib.Path`
- PySide6 QtCore/QtGui/QtWidgets types
- `AppConfig`
- `ProviderProfile`
- `AgentProfile`
- `PromptRecord`
- `AgentManager`
- `PluginManager`
- `PromptManager`

## `locallama_gui.ui.main_window`

Imports:

- `json`
- `logging`
- `sys`
- `dataclasses.asdict`
- `pathlib.Path`
- `typing.Any`
- `psutil`
- PySide6 Core/Gui/Widgets types
- `create_backend`
- `OllamaBackend`
- `APP_SYSTEM_PROMPT`
- `AppConfig`
- `ChatMessage`
- `ChatSession`
- `ModelInfo`
- `AgentManager`
- `PluginContext`
- `PluginManager`
- `PromptManager`
- `SessionManager`
- `assistant_label`
- `compute_scroll_restore_plan`
- `redacted_request_messages`
- `visible_chat_messages`
- `ChatController`
- `ModelController`
- `PluginController`
- diagnostics types/functions
- dialog classes
- `DARK_QSS`
- `dark_qss`
- `AsyncTask`
- `StreamTask`

## `locallama_gui.ui.model_browser`

Imports:

- `dataclasses.dataclass`
- `urllib.parse.quote_plus`
- `PySide6.QtCore.QUrl`
- `PySide6.QtGui.QDesktopServices`
- PySide6 dialog/widget classes
- `create_backend`
- `OperationStreamParser`
- `StreamTask`

## `locallama_gui.ui.production_fixes`

Imports:

- `json`
- `sys`
- `dataclasses.asdict`
- `pathlib.Path`
- `psutil`
- `PySide6.QtGui.QAction`
- `QFileDialog`
- `QInputDialog`
- `QMessageBox`
- `AgentProfile`
- `ModelBrowserDialog`
- `FirstRunWizard`
- `dark_qss`

## `locallama_gui.ui.setup_wizard`

Imports:

- `psutil`
- `QUrl`
- `QDesktopServices`
- Qt widget/wizard classes
- `create_backend`
- `CATALOG`
- `AsyncTask`

Dynamic imports inside `accept()`:

- `OperationStreamParser`
- `StreamTask`
- `QTimer` in production-fix startup path

## `locallama_gui.ui.theme`

No imports.

## `locallama_gui.ui.workers`

Imports:

- `asyncio`
- `collections.abc.AsyncIterator`
- `collections.abc.Callable`
- `typing.Any`
- `QObject`
- `QThread`
- `Signal`

`QObject` is imported but not used by the confirmed worker implementation.

---

# 5. Inventory #3/#4/#5/#6 — Classes, Methods, Functions, Properties

## `core.config`

### `CredentialStore`

Class attribute:

- `service_name`

Methods:

- `_username`
- `get`
- `set`

### `AppPaths`

Class method:

- `create`

Fields are listed in Inventory #7.

### `ProviderProfile`

No methods.

### `GenerationParameters`

Methods:

- `__post_init__`
- `to_backend_options`

### `UISettings`

No methods.

### `AppConfig`

Property:

- `file_path`

Class methods:

- `_migrate_data`
- `load`

Methods:

- `save`
- `active_profile`

---

## `core.domain`

### Module-level

- `now_iso`

### `ChatMessage`

No methods beyond generated dataclass methods.

### `ChatSession`

Methods:

- `touch`
- `to_json`
- `from_file` (classmethod)
- `save`
- `export_markdown`
- `export_text`

### `ModelInfo`

Property:

- `size_display`

### `PromptRecord`

No explicit methods.

### `AgentProfile`

No explicit methods.

---

## `core.managers`

### `SessionManager`

- `__init__`
- `list_sessions`
- `load`
- `save`
- `import_session`

### `PromptManager`

- `__init__`
- `list`
- `save_all`
- `upsert`
- `delete`
- `import_file`
- `export`

### `AgentManager`

- `__init__`
- `list`
- `save_all`
- `upsert`

### `PluginAPI`

- `activate`
- `deactivate`

### `PluginContext`

- `__init__`
- `register_tool`
- `register_command`
- `register_chat_interceptor`
- `add_panel`

### `LoadedPlugin`

- `__init__`

### `PluginManager`

- `__init__`
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

---

## `backends.base`

### `BackendStatus`

No explicit methods.

### `LLMBackend`

- `__init__`
- abstract `test_connection`
- abstract `list_models`
- abstract `chat`
- `pull_model`
- `push_model`
- `delete_model`
- `copy_model`
- `create_model`
- `show_model`

---

## `backends.manager`

Module function:

- `create_backend`

---

## `backends.ollama`

### `OllamaBackend`

Class constant:

- `name`
- `SUPPORTED_OPTIONS`

Methods:

- `sanitize_options` (classmethod)
- `sanitize_request_fields` (staticmethod)
- `build_chat_payload` (classmethod)
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

---

## `backends.openai`

### `OpenAICompatibleBackend`

Class attribute:

- `name`

Methods:

- `_headers`
- `test_connection`
- `list_models`
- `chat`

---

## `ui.chat_view`

### `ScrollRestorePlan`

Frozen dataclass.

### Functions

- `compute_scroll_restore_plan`
- `message_is_internal_system`
- `visible_chat_messages`
- `assistant_label`
- `redacted_request_messages`

---

## `ui.controllers.chat_controller`

### `ChatWindowPort`

Protocol members:

- `current_tab`
- `set_tab_title`
- `render_tab`
- `generate_for_tab`
- `refresh_sessions`
- `log`
- `open_session`

### `ChatController`

Methods:

- `__init__`
- `save_current`
- `open_chat_file`
- `send_message`
- `regenerate`
- `retry`
- `copy_last_message`
- `edit_message`
- `delete_message`

---

## `ui.controllers.model_controller`

### `ModelWindowPort`

Protocol members:

- `model_name`
- `begin_operation`
- `update_operation`
- `complete_operation`
- `fail_operation`
- `refresh_backend`
- `add_worker`
- `run_async`
- `open_modelfile_editor`

### `ModelController`

Methods:

- `__init__`
- `pull_model`
- `push_model`
- `create_model`
- `clone_model`
- `delete_model`
- `_model_stream_op`

---

## `ui.controllers.plugin_controller`

### `PluginWindowPort`

Protocol member:

- `log`

### `PluginController`

Methods:

- `__init__`
- `reload_plugins`
- `install_plugin`

---

## `ui.diagnostics`

### Functions

- `append_output`
- `_integer_or_none`

### `DiagnosticsSignals`

Signals:

- `log_line`
- `console_text`

### `QtLogHandler`

- `__init__`
- `emit`

### `LineBufferedStream`

- `__init__`
- `write`
- `flush`
- `isatty`
- property `encoding`

### `OperationUpdate`

Frozen dataclass.

### `OperationStreamParser`

- `__init__`
- `feed`
- `_from_payload`

---

## `ui.dialogs`

### `ModelfileHighlighter`

- `highlightBlock`

### `EndpointDialog`

- `__init__`
- `add_row`
- `accept`

### `ModelfileEditor`

- `__init__`
- `new`
- `open_file`
- `save`
- `duplicate`
- `validate`
- `build_model`
- `update_preview`

### `PromptManagerDialog`

- `__init__`
- `refresh`
- `load_selected`
- `new`
- `save`
- `delete`
- `import_prompt`
- `export_prompts`

### `AgentBuilderDialog`

- `__init__`
- `refresh`
- `load_selected`
- `new`
- `_agent`
- `save`
- `import_agent`
- `export_agent`

### `PluginManagerDialog`

- `__init__`
- `refresh`
- `apply`
- `reload_plugins`

### `ParameterDialog`

- `__init__`
- nested helper `spin`
- nested helper `dbl`
- `_collect`
- `save_preset`
- `load_preset`
- `accept`

---

## `ui.main_window`

### Module function

- `_build_readonly_table_item`

### `ChatTab`

Instance state:

- `session`
- `chat`
- `input`
- `streaming`
- `send`
- `stop`
- `regen`
- `retry`
- `copy_last`
- `edit_msg`
- `delete_msg`

Methods:

- `__init__`
- `render`
- `set_generating`

### `ComposerTextEdit`

Signals:

- `send_requested`
- `zoom_requested`

Methods:

- `keyPressEvent`
- `wheelEvent`

### `MainWindow`

Methods:

- `__init__`
- `_build_ui`
- `_create_docks`
- `_dock`
- `add_plugin_panel`
- `_menu_action`
- `_build_menus`
- `_build_file_menu`
- `_build_models_menu`
- `_build_agents_menu`
- `_build_plugins_menu`
- `_build_settings_menu`
- `_build_view_menu`
- `_build_developer_menu`
- `_build_help_menu`
- `current_tab`
- `new_chat`
- `_wire_chat_tab`
- `close_tab`
- `_generate`
- `_append_token`
- `_stream_error`
- `_stream_done`
- `stop_generation`
- `model_changed`
- `refresh_backend`
- `_show_dock`
- `show_diagnostics_dock`
- `_show_diagnostics_tab`
- `show_logs_dock`
- `show_console_dock`
- `show_operations_dock`
- `show_request_dock`
- `show_token_dock`
- `_backend_refresh_error`
- `_backend_refreshed`
- `_update_backend_status`
- `_refresh_model_combo`
- `_refresh_model_table`
- `_insert_model_table_row`
- `switch_provider`
- `refresh_sessions`
- `refresh_prompts`
- `apply_prompt_item`
- `save_as`
- `open_session`
- `import_chat`
- `export_current`
- `_async`
- `run_async`
- `set_tab_title`
- `render_tab`
- `generate_for_tab`
- `model_name`
- `_install_diagnostics_sinks`
- `append_log`
- `append_console`
- `append_operation_history`
- `begin_operation`
- `update_operation`
- `complete_operation`
- `fail_operation`
- `add_worker`
- `open_modelfile_editor`
- `build_model_from_modelfile`
- `open_template_viewer`
- `_show_text_dialog`
- `open_endpoints`
- `open_parameters`
- `edit_default_system_prompt`
- `open_plugins`
- `open_plugin_docs`
- `open_agent_builder`
- `import_agent`
- `export_agent`
- `toggle_theme`
- `show_shortcuts`
- `adjust_font_size`
- `toggle_all_docks`
- `reset_layout`
- `inspect_api`
- `_open_document`
- `open_docs`
- `about`
- `diagnostics`
- `log`
- `_restore_state`
- `closeEvent`

---

## `ui.model_browser`

### `ModelRecommendation`

Frozen dataclass fields:

- `name`
- `size`
- `purpose`
- `minimum_ram_gib`

### `ModelBrowserDialog`

Methods:

- `__init__`
- `filter_models`
- `open_library`
- `pull_selected`

---

## `ui.production_fixes`

Functions:

- `_menu`
- `_remove_action`
- `_replace_action`
- `_resource_path`
- `_open_bundled_document`
- `_show_about`
- `_choose_theme`
- `_import_agent`
- `_export_agent`
- `_show_model_browser`
- `_build_diagnostics_submenu`
- `_add_ai_model_settings`
- `apply_production_fixes`

---

## `ui.setup_wizard`

### `FirstRunWizard`

Methods:

- `__init__`
- `_build_welcome_page`
- `_build_hardware_page`
- `_build_backend_page`
- `_build_finish_page`
- `_recommended_model`
- `_page_changed`
- `_check_backend`
- `accept`

---

## `ui.theme`

Function:

- `dark_qss`

Constant:

- `DARK_QSS`

---

## `ui.workers`

### `AsyncTask`

Signals:

- `result`
- `error`
- `finished_ok`

Methods:

- `__init__`
- `run`

### `StreamTask`

Signals:

- `token`
- `error`
- `completed`

Methods:

- `__init__`
- `cancel`
- `run`

---

## `plugins/sample_plugin.py`

### `Plugin`

Class constant:

- `manifest`

Methods:

- `__init__`
- `activate`
- `deactivate`
- `add_metadata`

Instance attribute:

- `_active`

---

## `packaging/assets/generate_myloai_icon.py`

Module-level constants:

- `ROOT`
- `ICO`
- `PNG`
- `SIZE`

Module-level objects:

- `img`
- `draw`
- `points`
- `inner`
- `node_r`
- `nodes`

No declared functions.

---

## `packaging/check-release-payload.py`

Constants:

- `EXCLUDED_TOP_LEVEL`
- `EXCLUDED_FILES`
- `EXCLUDED_NAME_PARTS`

Functions:

- `validate`
- `main`

CLI:

- module execution via `__main__`

---

# 6. Inventory #7 — Every Dataclass Field

## `ChatMessage`

| Field | Default |
|---|---|
| `role` | required |
| `content` | required |
| `id` | UUID factory |
| `created_at` | `now_iso` factory |
| `name` | `""` |
| `metadata` | empty dict factory |

## `ChatSession`

| Field | Default |
|---|---|
| `title` | `"New Chat"` |
| `id` | UUID factory |
| `created_at` | `now_iso` factory |
| `updated_at` | `now_iso` factory |
| `provider` | `"Local Ollama"` |
| `model` | `""` |
| `system_prompt` | `""` |
| `messages` | empty list factory |
| `parameters` | empty dict factory |

## `ModelInfo`

| Field | Default |
|---|---|
| `name` | required |
| `size` | `0` |
| `parameter_size` | `""` |
| `quantization` | `""` |
| `context_size` | `0` |
| `backend` | `""` |
| `metadata` | empty dict factory |

## `PromptRecord`

| Field | Default |
|---|---|
| `title` | required |
| `content` | required |
| `category` | `"General"` |
| `favorite` | `False` |
| `id` | UUID factory |
| `versions` | empty list factory |
| `updated_at` | `now_iso` factory |

## `AgentProfile`

| Field | Default |
|---|---|
| `name` | required |
| `model` | `""` |
| `system_prompt_id` | `""` |
| `tools` | empty list factory |
| `plugins` | empty list factory |
| `memory_mode` | `"session"` |
| `reasoning_mode` | `"normal"` |
| `behavior` | `"constrained"` |
| `execution_policy` | `"confirm_tools"` |
| `id` | UUID factory |

## `AppPaths`

- `config_dir`
- `data_dir`
- `logs_dir`
- `sessions_dir`
- `prompts_dir`
- `agents_dir`
- `modelfiles_dir`
- `plugins_dir`

All are required `Path` fields.

## `ProviderProfile`

- `name = "Local Ollama"`
- `provider_type = "ollama"`
- `base_url = "http://localhost:11434"`
- `api_key = ""`
- `default_model = ""`
- `enabled = True`

## `GenerationParameters`

- `temperature = 0.7`
- `top_k = 40`
- `top_p = 0.9`
- `min_p = 0.0`
- `repeat_penalty = 1.1`
- `repeat_last_n = 64`
- `mirostat = 0`
- `mirostat_eta = 0.1`
- `mirostat_tau = 5.0`
- `tfs_z = 1.0`
- `num_predict = 512`
- `seed = -1`
- `stop = []`
- `num_ctx = 4096`
- `num_batch = 512`
- `num_gpu = -1`
- `reasoning_mode = "normal"`
- `thinking_mode = False`
- `plan_mode = False`
- `normal_mode = True`

## `UISettings`

- `theme = "dark"`
- `geometry_hex = ""`
- `state_hex = ""`
- `active_session_id = ""`
- `font_size = 12`

## `AppConfig`

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

## `BackendStatus`

- `state`
- `latency_ms = 0.0`
- `detail = ""`

## `ScrollRestorePlan`

- `should_pin_bottom`
- `previous_value`

## `OperationUpdate`

- `status`
- `history_text`
- `completed`
- `total`

## `ModelRecommendation`

- `name`
- `size`
- `purpose`
- `minimum_ram_gib`

---

# 7. Inventory #8 — Protocols / ABCs

## ABC

### `LLMBackend`

Required abstract operations:

- `test_connection`
- `list_models`
- `chat`

Default unsupported operations:

- `pull_model`
- `push_model`
- `delete_model`
- `copy_model`
- `create_model`
- `show_model`

Implementation:

- `OllamaBackend`
- `OpenAICompatibleBackend`

## Protocol

### `PluginAPI`

- `manifest`
- `activate(context)`
- `deactivate()`

Implementation:

- `plugins/sample_plugin.py::Plugin`

### `ChatWindowPort`

- `current_tab`
- `set_tab_title`
- `render_tab`
- `generate_for_tab`
- `refresh_sessions`
- `log`
- `open_session`

Consumer:

- `ChatController`

### `ModelWindowPort`

- `model_name`
- `begin_operation`
- `update_operation`
- `complete_operation`
- `fail_operation`
- `refresh_backend`
- `add_worker`
- `run_async`
- `open_modelfile_editor`

Consumer:

- `ModelController`

### `PluginWindowPort`

- `log`

Consumer:

- `PluginController`

---

# 8. Inventory #9 — Constants / Contract Literals

## Application constants

`core/config.py`

- `APP_NAME = "locallama-gui"`
- `CONFIG_SCHEMA_VERSION = 2`
- `APP_SYSTEM_PROMPT`

`locallama_gui.__init__`

- `__version__ = "1.2.0"`

## Backend constants

`OllamaBackend.name = "ollama"`

`OpenAICompatibleBackend.name = "openai"`

`OllamaBackend.SUPPORTED_OPTIONS`:

- `temperature`
- `top_k`
- `top_p`
- `min_p`
- `repeat_penalty`
- `repeat_last_n`
- `num_predict`
- `seed`
- `stop`
- `num_ctx`
- `num_batch`
- `num_gpu`
- `num_keep`
- `typical_p`
- `presence_penalty`
- `frequency_penalty`
- `main_gpu`
- `use_mmap`
- `num_thread`

## UI constants

`chat_view.py`

- `INTERNAL_PROMPT_REDACTION`

`theme.py`

- `DARK_QSS`

`model_browser.py`

- `CATALOG`

`ModelRecommendation` catalog entries:

- `gemma3:1b`
- `qwen3.5:4b`
- `mistral:7b`
- `deepseek-r1:7b`
- `qwen2.5-coder:7b`

---

# 9. Inventory #10 — Instance Attributes

## `MainWindow`

Confirmed constructor state:

- `config`
- `sessions`
- `prompts`
- `agents`
- `plugin_context`
- `plugins`
- `models`
- `chat_controller`
- `model_controller`
- `plugin_controller`
- `worker_refs`
- `current_stream`
- `_stream_owner_seq`
- `_active_stream_owner`
- `_diagnostics_signals`
- `_diagnostics_log_handler`
- `_original_stdout`
- `_original_stderr`

UI-created state includes:

- `tabs`
- `status`
- `toolbar`
- `provider_combo`
- `model_combo`
- `model_table`
- `sessions_list`
- `prompt_list`
- `log_view`
- `console_view`
- `operation_status`
- `operation_progress`
- `operation_history`
- `diagnostics_tabs`
- `diagnostics_dock`
- `request_view`
- `request_copy`
- `request_clear`
- `request_dock`
- `token_view`
- `token_copy`
- `token_clear`
- `token_dock`

## `ChatTab`

- `session`
- `chat`
- `input`
- `streaming`
- `send`
- `stop`
- `regen`
- `retry`
- `copy_last`
- `edit_msg`
- `delete_msg`

## `ComposerTextEdit`

No custom instance state.

## `LLMBackend`

- `base_url`
- `api_key`

## `SessionManager`

- `config`

## `PromptManager`

- `config`
- `path`

## `AgentManager`

- `config`
- `path`

## `PluginContext`

- `main_window`
- `config`
- `tools`
- `commands`
- `chat_interceptors`
- `memory_providers`

## `PluginManager`

- `config`
- `context`
- `loaded`

## `LoadedPlugin`

- `path`
- `module`
- `instance`
- `manifest`

## `AsyncTask`

- `coro_factory`

## `StreamTask`

- `iterator_factory`
- `_cancelled`
- `full_text`

## `QtLogHandler`

- `signals`

## `LineBufferedStream`

- `emit`
- `tee`
- `_buffer`

## `OperationStreamParser`

- `_buffer`
- `_last_history`

## `FirstRunWizard`

- `config`
- `_connection_ok`
- `_pull_on_finish`
- `welcome_page`
- `hardware_page`
- `backend_page`
- `finish_page`
- `hardware_label`
- `provider_label`
- `status_label`
- `model_combo`
- `pull_check`
- `install_button`
- `finish_label`
- `_task`
- `_pull_task`

## `ModelBrowserDialog`

- `window`
- `list`
- `search`
- `pull_button`
- `library_button`
- `close_button`

## `Plugin` sample

- `_active`

---

# 10. Inventory #11 — Environment Variables

## Direct Python environment references

`locallama_gui/app.py`:

- `QT_ENABLE_HIGHDPI_SCALING`
  - set with `os.environ.setdefault`
  - default `"1"`

- `QT_AUTO_SCREEN_SCALE_FACTOR`
  - set with `os.environ.setdefault`
  - default `"1"`

`app.py` also uses `os.environ` indirectly only for those Qt variables.

## Shell environment references

Packaging/launcher scripts use:

- `HOME`
- `PATH`

`run-locallama` checks command availability through `PATH`.

No additional application environment variable was confirmed in the active Python source.

---

# 11. Inventory #12 — Filesystem Paths

## Application-managed paths

Generated through `platformdirs`:

- user config directory
- user data directory
- user log directory

Subdirectories:

- `sessions`
- `prompts`
- `agents`
- `modelfiles`
- `plugins`

Configuration:

- `<config_dir>/config.json`

Logging:

- `<logs_dir>/locallama-gui.log`

Prompt persistence:

- `<prompts_dir>/prompts.json`

Agent persistence:

- `<agents_dir>/agents.json`

Session persistence:

- `<sessions_dir>/<session-id>.json`

Modelfiles:

- `<modelfiles_dir>/Modelfile`
- `<modelfiles_dir>/.versions/<model-name>/<N>.Modelfile`

Plugin discovery:

- `<plugins_dir>/*.py`
- repository `plugins/*.py` when developer mode is enabled

## Repository/document paths

Runtime/documentation references include:

- `README.md`
- `docs/PLUGIN_SDK.md`
- `packaging/USER_MANUAL.md`
- `packaging/PLUGIN_SDK.md`-style bundled documentation path through `_resource_path`
- `packaging/linux/com.github.gr00t-user-706.locallama-gui.desktop`
- `packaging/linux/myloai.desktop`

## Launcher paths

`scripts/install-launcher`:

- `${HOME}/.local/bin/run-locallama`

`scripts/install-desktop-entry`:

- `${HOME}/.local/share/applications`
- `${HOME}/.local/share/applications/com.github.gr00t-user-706.locallama-gui.desktop`

---

# 12. Inventory #13 — HTTP Endpoints

## Ollama

Base URL default:

`http://localhost:11434`

### Connection/model discovery

`GET /api/tags`

Used by:

- `OllamaBackend.test_connection`
- `OllamaBackend.list_models`

### Chat

`POST /api/chat`

Used by:

- `OllamaBackend.chat`

Payload:

- `model`
- `messages`
- `options`
- `stream`
- optional `think`

Streaming:

- newline-delimited JSON
- reads `message.content`
- terminates on `done`

### Pull

`POST /api/pull`

Used by:

- `OllamaBackend.pull_model`

Streaming operation output.

### Push

`POST /api/push`

Used by:

- `OllamaBackend.push_model`

Streaming operation output.

### Delete

`DELETE /api/delete`

Used by:

- `OllamaBackend.delete_model`

Payload:

```json
{"name": "<model>"}
```

### Copy

`POST /api/copy`

Used by:

- `OllamaBackend.copy_model`

Payload:

```json
{"source": "<source>", "destination": "<destination>"}
```

### Create

`POST /api/create`

Used by:

- `OllamaBackend.create_model`

Payload:

- `name`
- `modelfile`
- `stream`

### Show

`POST /api/show`

Used by:

- `OllamaBackend.show_model`

Payload:

```json
{"name": "<model>"}
```

## OpenAI-compatible

Base URL is configured through `ProviderProfile.base_url`.

### Models

`GET /models`

Used by:

- `OpenAICompatibleBackend.test_connection`
- `OpenAICompatibleBackend.list_models`

### Chat

`POST /chat/completions`

Used by:

- `OpenAICompatibleBackend.chat`

Payload:

- `model`
- `messages`
- `temperature`
- `top_p`
- `max_tokens`
- optional `stop`
- `stream`

Streaming uses SSE-style:

```text
data: {...}
```

and terminates at:

```text
[DONE]
```

Authorization:

```text
Authorization: Bearer <api_key>
```

---

# 13. Inventory #14 — CLI / Launch Entry Points

## Python package entry points

`pyproject.toml`:

```text
myloai -> locallama_gui.app:main
locallama-gui -> locallama_gui.app:main
```

`main` is:

`locallama_gui.app.main`

## Module launcher

```text
python -m locallama_gui
```

Implementation:

`locallama_gui/__main__.py`

## Repository launcher

```text
./run-locallama
```

Resolution order:

1. `locallama-gui`
2. `python3 -m locallama_gui`
3. `python -m locallama_gui`

## Installer scripts

```text
scripts/install-launcher
scripts/install-desktop-entry
```

Supported option:

```text
--dry-run
```

## Release payload validator

```text
python packaging/check-release-payload.py <staging_dir>
```

## Packaging build entrypoints

- `packaging/linux/appimage/build-appimage.sh`
- `packaging/linux/debian/build-deb.sh`
- `packaging/linux/install-myloai.sh`
- `packaging/macos/build-dmg.sh`
- `packaging/windows/build-installer.ps1`
- `packaging/assets/generate_myloai_icon.py`

---

# 14. Inventory #15 — Plugin Hooks

## Static manifest hook

Plugin class must expose:

```python
manifest = {
    "id": ...,
    "name": ...,
    "version": ...
}
```

Static manifest is parsed using AST before plugin execution.

## Lifecycle hooks

- `Plugin.activate(context)`
- `Plugin.deactivate()`

## Context registration hooks

- `register_tool`
- `register_command`
- `register_chat_interceptor`
- `add_panel`

## Runtime interceptor hook

`PluginContext.chat_interceptors`

Consumed by:

`MainWindow._generate`

Pipeline:

```text
system message
    ↓
session messages
    ↓
chat interceptors
    ↓
backend request
```

## Tool registry

`PluginContext.tools`

## Command registry

`PluginContext.commands`

## Panel hook

`PluginContext.add_panel`

Delegates to:

`MainWindow.add_plugin_panel`

## Trust/enable lifecycle

`PluginManager`:

- `discover`
- `trust`
- `untrust`
- `enable`
- `disable`
- `reload`
- `remove`
- `load_enabled`

## Sample plugin implementation

`plugins/sample_plugin.py` registers:

- tool: `uppercase`
- command: `insert_timestamp`
- chat interceptor: `add_metadata`
- panel: `Sample Plugin`

---

# 15. Inventory #16 — Worker Boundaries

## `AsyncTask`

Boundary:

```text
Qt GUI thread
    ↓
QThread
    ↓
asyncio.run(coro_factory())
    ↓
result/error signal
    ↓
Qt GUI thread
```

Signals:

- `result(object)`
- `error(str)`
- `finished_ok()`

## `StreamTask`

Boundary:

```text
Qt GUI thread
    ↓
QThread
    ↓
async iterator
    ↓
token signal
    ↓
Qt GUI thread
```

Signals:

- `token(str)`
- `error(str)`
- `completed(str)`

Cancellation:

- `_cancelled = True`
- checked between streamed tokens

## Chat generation

```text
MainWindow._generate
    ↓
StreamTask
    ↓
backend.chat()
    ↓
HTTP stream
    ↓
StreamTask.token
    ↓
MainWindow._append_token
    ↓
ChatMessage.content
    ↓
ChatTab.render
```

## Model operations

`ModelController._model_stream_op`:

```text
ModelController
    ↓
StreamTask
    ↓
backend pull/push
    ↓
OperationStreamParser
    ↓
MainWindow.update_operation
```

## First-run backend test

`FirstRunWizard._check_backend`:

```text
FirstRunWizard
    ↓
AsyncTask
    ↓
backend.test_connection()
    ↓
result/error
```

---

# 16. Inventory #17 — Qt Signals / Slots / Connections

## `ComposerTextEdit`

Signals:

- `send_requested = Signal()`
- `zoom_requested = Signal(int)`

Connections:

- `send_requested` → `ChatController.send_message`
- `zoom_requested` → `MainWindow.adjust_font_size`

## `DiagnosticsSignals`

- `log_line = Signal(str)`
- `console_text = Signal(str)`

Connections:

- `log_line` → `MainWindow.append_log`
- `console_text` → `MainWindow.append_console`

## `AsyncTask`

- `result`
- `error`
- `finished_ok`

Consumers include:

- `MainWindow.refresh_backend`
- `MainWindow.run_async`
- `FirstRunWizard._check_backend`
- `MainWindow.open_template_viewer`

## `StreamTask`

- `token`
- `error`
- `completed`

Consumers include:

- `MainWindow._generate`
- `ModelController._model_stream_op`
- `ModelBrowserDialog.pull_selected`
- `FirstRunWizard.accept`
- `MainWindow.build_model_from_modelfile`

## MainWindow Qt connections

Confirmed connections include:

- tab close → `close_tab`
- toolbar actions → associated actions
- provider combo → `switch_provider`
- model combo → `model_changed`
- session double-click → `open_session`
- prompt double-click → `apply_prompt_item`
- request copy → clipboard
- request clear → clear
- token copy → clipboard
- token clear → clear

## Dialog connections

Confirmed signal/slot patterns include:

- button clicked → dialog operation
- dialog accept/reject buttons
- list row changes → selection loaders
- model browser search text → `filter_models`
- wizard page changes → `_page_changed`

---

# 17. Inventory #18 — Persistence Operations

## Configuration

`AppConfig.load`

Reads:

- config JSON
- provider profiles
- parameter settings
- plugin state
- UI state

`AppConfig.save`

Writes:

- config JSON

Also writes provider credentials to OS keyring.

Configuration JSON intentionally omits API keys.

File mode:

- attempts `0600`

## Credentials

`CredentialStore.get`

Reads OS credential store.

`CredentialStore.set`

Writes/deletes OS credential store entries.

Service name:

`locallama-gui`

Username:

`<provider_type>:<profile_name>`

## Sessions

`SessionManager.list_sessions`

Reads:

`<sessions_dir>/*.json`

`SessionManager.load`

Reads:

`<sessions_dir>/<session_id>.json`

`SessionManager.save`

Delegates to `ChatSession.save`.

`SessionManager.import_session`

Reads source session and writes a managed copy.

`ChatSession.save`

Writes JSON.

## Prompts

`PromptManager`

- initializes `prompts.json`
- reads all prompts
- writes all prompts
- upserts
- deletes
- imports text
- exports JSON

## Agents

`AgentManager`

- initializes `agents.json`
- reads all agents
- writes all agents
- upserts

## Modelfiles

`ModelfileEditor`

- reads modelfile
- writes modelfile
- writes versioned copies

## Chat export

`MainWindow.save_as`

Writes JSON.

`MainWindow.export_current`

Writes:

- Markdown
- JSON
- text

## UI state

`MainWindow._restore_state`

Reads:

- geometry
- window state

`MainWindow.closeEvent`

Writes:

- geometry
- window state

---

# 18. Inventory #19 — Test Targets

Active test files from the audited branch:

| Test file | Primary target |
|---|---|
| `tests/test_backend_and_config.py` | backend/config integration |
| `tests/test_chat_view.py` | chat-view helpers |
| `tests/test_config_roundtrip.py` | config persistence round-trip |
| `tests/test_config_schema.py` | config schema/migration |
| `tests/test_controller_invalid_flows.py` | controller invalid paths |
| `tests/test_controllers.py` | controller behavior |
| `tests/test_diagnostics.py` | diagnostics parsing/output |
| `tests/test_model_controller_delete.py` | model deletion controller |
| `tests/test_model_metadata_table_flags.py` | model table UI flags |
| `tests/test_model_operations.py` | model operation async contract |
| `tests/test_ollama_backend.py` | Ollama backend |
| `tests/test_plugin_lifecycle.py` | plugin lifecycle |
| `tests/test_security_boundaries.py` | security/trust boundaries |

### Reverse target coverage

Confirmed production areas with direct test coverage:

- backend configuration
- config serialization/migration
- chat-view helpers
- controllers
- diagnostics
- model operations
- Ollama HTTP behavior
- plugin lifecycle
- security boundaries

Production areas without a dedicated test file identified by filename:

- `production_fixes.py`
- `setup_wizard.py`
- `model_browser.py`
- packaging scripts
- launcher shell scripts
- `MainWindow` broad UI surface

---

# 19. Inventory #20 — Branch-Specific Symbol Differences

## Package identity

### `locallama_gui.__init__`

`main`:

```text
__version__ = "1.1.10"
```

feature:

```text
__version__ = "1.2.0"
```

Module description changed from LocalLama GUI wording to MyLoAI Control Center wording.

**Status:** MODIFIED / CONTRACT_CHANGED

---

## `locallama_gui.__main__`

`main` imports:

```python
from .app import main
```

feature imports:

```python
from locallama_gui.app import main
```

**Status:** MODIFIED

Runtime behavior remains delegation to `app.main()`.

---

## `locallama_gui.app`

### Added imports

- `Path`
- `platformdirs.user_config_dir`
- `APP_NAME`
- `apply_production_fixes`

### Added first-run state

```text
config_path
first_run
```

### Added first-run detection

Checks:

```text
<user config dir>/config.json
```

### Added startup behavior

Temporarily replaces:

```text
MainWindow.refresh_backend
```

with a no-op on first run.

### Added production-fix phase

```text
apply_production_fixes(win, first_run=first_run)
```

### Application name changed

`main`:

```text
LocalLama Control Center
```

feature:

```text
MyLoAI Control Center
```

**Status:** MODIFIED / CONTRACT_CHANGED

---

## `core.logging`

### Main

Configured:

- FileHandler
- StreamHandler

### Feature

Configured:

- FileHandler only

Feature adds rationale for GUI environments where `sys.stderr` may be `None`.

**Status:** IMPLEMENTATION_CHANGED

---

## `ui.model_browser`

Entire module added.

New:

- `ModelRecommendation`
- `CATALOG`
- `ModelBrowserDialog`
- `filter_models`
- `open_library`
- `pull_selected`

**Status:** ADDED

---

## `ui.production_fixes`

Entire module added.

New functions:

- `_menu`
- `_remove_action`
- `_replace_action`
- `_resource_path`
- `_open_bundled_document`
- `_show_about`
- `_choose_theme`
- `_import_agent`
- `_export_agent`
- `_show_model_browser`
- `_build_diagnostics_submenu`
- `_add_ai_model_settings`
- `apply_production_fixes`

**Status:** ADDED

---

## `ui.setup_wizard`

Entire module added.

New class:

- `FirstRunWizard`

New methods:

- `__init__`
- `_build_welcome_page`
- `_build_hardware_page`
- `_build_backend_page`
- `_build_finish_page`
- `_recommended_model`
- `_page_changed`
- `_check_backend`
- `accept`

**Status:** ADDED

---

## `pyproject.toml`

### Version

`1.1.10` → `1.2.0`

### Console scripts

Main:

```text
locallama-gui
```

Feature adds:

```text
myloai
```

### Ruff exclusion

Feature adds:

```text
archive
```

to the excluded paths.

**Status:** MODIFIED / PACKAGING CONTRACT CHANGED

---

## Packaging additions

The feature adds:

- release workflow
- release build specification
- release payload specification
- packaging user manual
- Linux package build
- AppImage build
- Debian build
- macOS DMG build
- Windows installer build
- PyInstaller specification
- desktop entries
- launcher
- icon generation
- payload validation

**Status:** ADDED

---

# 20. State Ownership

| State | Owner | Readers/Writers |
|---|---|---|
| active provider | `AppConfig` | MainWindow, EndpointDialog |
| provider profiles | `AppConfig` | MainWindow, EndpointDialog |
| generation parameters | `AppConfig` | ParameterDialog, MainWindow |
| plugin enabled state | `AppConfig` | PluginManager, PluginManagerDialog |
| trusted plugins | `AppConfig` | PluginManager |
| session data | `ChatSession` | ChatController, MainWindow, SessionManager |
| session persistence | `SessionManager` | ChatController, MainWindow |
| prompt persistence | `PromptManager` | PromptManagerDialog, MainWindow |
| agent persistence | `AgentManager` | AgentBuilderDialog, production fixes |
| active stream | `MainWindow` | `_generate`, stop/error/done |
| worker lifetime | `MainWindow.worker_refs` | MainWindow/controllers |
| stream ownership | `MainWindow._active_stream_owner` | generation callbacks |
| plugin tools | `PluginContext.tools` | plugins |
| plugin commands | `PluginContext.commands` | plugins |
| chat interceptors | `PluginContext.chat_interceptors` | MainWindow |
| diagnostics log stream | `DiagnosticsSignals` | MainWindow |
| operation state | MainWindow | model controllers/browser/wizard |
| UI geometry/state | `AppConfig.ui` | MainWindow |

---

# 21. Dependency Direction

Observed active dependency graph:

```text
app.py
  │
  ├── AppConfig
  ├── configure_logging
  ├── QApplication
  └── MainWindow
          │
          ├── ChatController
          ├── ModelController
          ├── PluginController
          ├── SessionManager
          ├── PromptManager
          ├── AgentManager
          ├── PluginManager
          ├── AsyncTask / StreamTask
          └── backend factory
                    │
                    ├── OllamaBackend
                    │       └── httpx → Ollama
                    │
                    └── OpenAICompatibleBackend
                            └── httpx → OpenAI-compatible API
```

Important direct coupling observed:

`MainWindow._generate()` owns:

- provider selection
- backend construction
- message construction
- plugin interception
- parameter translation
- request preview
- stream creation
- stream ownership
- UI state
- persistence after completion

This is an observed fact, not a proposed change.

---

# 22. Chat Request Data Flow

```text
ChatTab.input
   │
   ▼
ChatController.send_message()
   │
   ├── append ChatMessage("user", ...)
   ├── update title
   └── window.generate_for_tab()
             │
             ▼
       MainWindow._generate()
             │
             ├── active profile
             ├── create_backend()
             ├── APP_SYSTEM_PROMPT
             ├── session messages
             ├── chat_interceptors
             ├── GenerationParameters.to_backend_options()
             ├── redacted request preview
             └── StreamTask
                     │
                     ▼
                 backend.chat()
                     │
                     ▼
                 HTTP provider
```

---

# 23. Persistence Data Flow

```text
AppConfig
  ├── config.json
  └── OS keyring

SessionManager
  └── sessions/*.json

PromptManager
  └── prompts/prompts.json

AgentManager
  └── agents/agents.json

ModelfileEditor
  └── modelfiles/Modelfile
      └── .versions/*.Modelfile

MainWindow
  └── UI geometry/state → config.json
```

---

# 24. Security / Trust Boundaries

## Provider credentials

API keys are not serialized into normal config JSON.

They are stored through:

`keyring`

## Plugin trust

A plugin cannot be enabled unless its ID appears in:

`trusted_plugins`

## Plugin manifest

Static manifest is parsed before execution.

Required:

- `id`
- `name`
- `version`

Runtime manifest is validated again.

Runtime ID must match discovery ID.

## Release payload

`check-release-payload.py` excludes:

- `.github`
- `archive`
- `tests`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `.pyc`
- `.pyo`

---

# 25. HTTP / Worker / UI Cross-Reference

| Operation | UI owner | Worker | Backend | Endpoint |
|---|---|---|---|---|
| chat | `MainWindow` | `StreamTask` | Ollama/OpenAI | `/api/chat` or `/chat/completions` |
| refresh | `MainWindow` | `AsyncTask` | backend | `/api/tags` or `/models` |
| pull | `ModelController` / browser | `StreamTask` | Ollama | `/api/pull` |
| push | `ModelController` | `StreamTask` | Ollama | `/api/push` |
| clone | `ModelController` | `AsyncTask` | Ollama | `/api/copy` |
| delete | `ModelController` | `AsyncTask` | Ollama | `/api/delete` |
| create | `MainWindow` | `StreamTask` | Ollama | `/api/create` |
| template/show | `MainWindow` | `AsyncTask` | Ollama | `/api/show` |

---

# 26. Plugin Cross-Reference

```text
PluginManager
    │
    ├── discover
    │     └── static AST manifest
    │
    ├── trust/untrust
    │     └── AppConfig.trusted_plugins
    │
    ├── enable/disable
    │     └── AppConfig.enabled_plugins
    │
    └── load
          │
          ▼
       Plugin instance
          │
          └── activate(context)
                    │
                    ├── tools
                    ├── commands
                    ├── chat_interceptors
                    └── panels
```

---

# 27. Filesystem / Persistence Cross-Reference

| Storage | Manager/owner | Format |
|---|---|---|
| config | `AppConfig` | JSON |
| credentials | `CredentialStore` | OS keyring |
| sessions | `SessionManager` / `ChatSession` | JSON |
| prompts | `PromptManager` | JSON |
| agents | `AgentManager` | JSON |
| modelfiles | `ModelfileEditor` | text |
| modelfile versions | `ModelfileEditor` | text |
| logs | `configure_logging` | log text |
| exported chats | `MainWindow` / `ChatSession` | JSON/Markdown/text |

---

# 28. Test Coverage Gaps Identified From Repository Structure

These are inventory observations, not remediation proposals.

No dedicated test target file is present for:

- first-run wizard
- model browser
- production fixes
- theme generation
- packaging build scripts
- launcher shell scripts
- desktop installation scripts
- broad MainWindow UI behavior

Existing tests strongly target:

- backend/config
- config roundtrip/schema
- controllers
- diagnostics
- model operations
- Ollama backend
- plugins
- security

---

# 29. Completeness Matrix

| Required category | Status |
|---|---|
| every module | COMPLETE for active production/test/package module set |
| every import | COMPLETE for audited active source modules |
| every class | COMPLETE for audited active source modules |
| every method | COMPLETE for audited active source modules |
| every function | COMPLETE for audited active source modules |
| every property | COMPLETE for audited active source modules |
| every dataclass field | COMPLETE |
| every Protocol / ABC | COMPLETE |
| every constant | COMPLETE for architectural/application constants; generated/local implementation literals are recorded where contract-bearing |
| every instance attribute | COMPLETE for confirmed active classes |
| every environment-variable reference | COMPLETE for confirmed active source |
| every filesystem path | COMPLETE for confirmed application persistence/runtime paths |
| every HTTP endpoint | COMPLETE for confirmed active backends |
| every CLI entry point | COMPLETE for confirmed package/launcher/build entrypoints |
| every plugin hook | COMPLETE |
| every worker boundary | COMPLETE |
| every Qt signal/slot | COMPLETE for custom signals and confirmed connection surfaces |
| every persistence operation | COMPLETE |
| every test target | COMPLETE at test-file/production-target level |
| every branch-specific symbol difference | COMPLETE for changed active Python/packaging symbols identified by the branch comparison |

---

# 30. Important Verified Architectural Facts

1. `MainWindow` is the largest orchestration surface.
2. `ChatController` owns chat-intent operations but delegates generation to the window port.
3. `ModelController` owns model-operation initiation but relies on a broad `ModelWindowPort`.
4. `PluginController` is thin and delegates plugin lifecycle to `PluginManager`.
5. `AppConfig` is both configuration model and persistence boundary.
6. `SessionManager`, `PromptManager`, and `AgentManager` are persistence managers.
7. `LLMBackend` is the provider abstraction.
8. `OllamaBackend` and `OpenAICompatibleBackend` are concrete HTTP implementations.
9. `StreamTask` is the main streaming worker boundary.
10. `AsyncTask` is the general coroutine worker boundary.
11. `PluginContext.chat_interceptors` is directly executed by `MainWindow._generate`.
12. Plugin manifests are statically inspected before execution.
13. Provider API keys use the OS keyring.
14. Chat request previews redact the internal application system prompt.
15. UI geometry/state is persisted through `AppConfig`.
16. First-run behavior exists only on the feature branch.
17. The feature branch adds a MyLoAI packaging/startup layer without replacing the core backend/controller architecture.
18. Archived legacy applications are excluded from active production packaging and Ruff scanning.

---

# 31. Canonical Runtime Sequence

```text
START
 │
 ▼
locallama_gui.app.main()
 │
 ├── set Qt environment defaults
 ├── resolve config path
 ├── determine first_run
 ├── AppConfig.load()
 ├── configure_logging()
 ├── QApplication()
 ├── MainWindow(config)
 │     │
 │     ├── managers
 │     ├── controllers
 │     ├── diagnostics
 │     ├── menus/docks
 │     ├── plugin load
 │     ├── new_chat()
 │     └── refresh_backend()
 │
 ├── restore/patch first-run behavior
 ├── apply_production_fixes()
 ├── show()
 └── app.exec()
```

---

# 32. Canonical Chat Sequence

```text
User
 │
 ▼
ChatTab.input
 │
 ▼
ChatController.send_message()
 │
 ├── ChatMessage(user)
 ├── title
 ├── render
 └── generate_for_tab()
          │
          ▼
     MainWindow._generate()
          │
          ├── active_profile
          ├── create_backend
          ├── system prompt
          ├── session messages
          ├── plugin interceptors
          ├── generation options
          ├── request preview
          └── StreamTask
                  │
                  ▼
             backend.chat()
                  │
                  ▼
              HTTP API
                  │
                  ▼
              token stream
                  │
                  ▼
            _append_token()
                  │
                  ▼
             ChatSession
                  │
                  ▼
            _stream_done()
                  │
                  ├── save session
                  └── refresh sessions
```

---

# 33. Audit Conclusion

The executed map confirms that the application is substantially modular already at the backend, manager, controller, worker, and plugin levels, while `MainWindow` remains the dominant orchestration boundary.

The branch-specific production work primarily adds:

- MyLoAI identity/versioning
- first-run bootstrap
- production UI fixes
- model browser
- setup wizard
- release/packaging infrastructure
- launcher/install infrastructure

The existing backend/controller/domain/manager architecture is not replaced by those additions.

No source was modified during this audit.
