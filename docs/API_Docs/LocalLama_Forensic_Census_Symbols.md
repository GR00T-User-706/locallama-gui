# LocalLama Forensic Census Symbols

Repository: `GR00T-User-706/locallama-gui`
Feature ref: `5e2c520426386084d795779f3121a3a856d4459a`
Mode: READ-ONLY

## Core data/domain symbols

| Qualified symbol | Kind | Signature/fields | Evidence |
|---|---|---|---|
| `locallama_gui.core.config.CredentialStore` | class | class methods `_username`, `get`, `set` | STATIC_VERIFIED |
| `locallama_gui.core.config.AppPaths` | dataclass | 8 `Path` fields; `create()` | STATIC_VERIFIED |
| `locallama_gui.core.config.ProviderProfile` | dataclass | 6 fields | STATIC_VERIFIED |
| `locallama_gui.core.config.GenerationParameters` | dataclass | 20 fields; `__post_init__`, `to_backend_options` | STATIC_VERIFIED |
| `locallama_gui.core.config.UISettings` | dataclass | 5 fields | STATIC_VERIFIED |
| `locallama_gui.core.config.AppConfig` | dataclass | 11 fields; `file_path`, `_migrate_data`, `load`, `save`, `active_profile` | STATIC_VERIFIED |
| `locallama_gui.core.domain.ChatMessage` | dataclass | 6 fields | STATIC_VERIFIED |
| `locallama_gui.core.domain.ChatSession` | dataclass | 9 fields; touch/serialization/import/export | STATIC_VERIFIED |
| `locallama_gui.core.domain.ModelInfo` | dataclass | 7 fields; `size_display` | STATIC_VERIFIED |
| `locallama_gui.core.domain.PromptRecord` | dataclass | 7 fields | STATIC_VERIFIED |
| `locallama_gui.core.domain.AgentProfile` | dataclass | 10 fields | STATIC_VERIFIED |
| `locallama_gui.backends.base.BackendStatus` | dataclass | 3 fields | STATIC_VERIFIED |
| `locallama_gui.ui.chat_view.ScrollRestorePlan` | frozen dataclass | 2 fields | STATIC_VERIFIED |
| `locallama_gui.ui.diagnostics.OperationUpdate` | frozen dataclass | 4 fields | STATIC_VERIFIED |
| `locallama_gui.ui.model_browser.ModelRecommendation` | frozen dataclass | 4 fields | STATIC_VERIFIED |

## Interfaces

- `LLMBackend(ABC)`
- `PluginAPI(Protocol)`
- `ChatWindowPort(Protocol)`
- `ModelWindowPort(Protocol)`
- `PluginWindowPort(Protocol)`

## UI classes

- `ChatTab(QWidget)`
- `ComposerTextEdit(QPlainTextEdit)`
- `MainWindow(QMainWindow)`
- `ModelfileHighlighter(QSyntaxHighlighter)`
- `EndpointDialog(QDialog)`
- `ModelfileEditor(QDialog)`
- `PromptManagerDialog(QDialog)`
- `AgentBuilderDialog(QDialog)`
- `PluginManagerDialog(QDialog)`
- `ParameterDialog(QDialog)`
- `ModelBrowserDialog(QDialog)`
- `FirstRunWizard(QWizard)`

## Backend / manager / worker classes

- `LLMBackend`
- `BackendStatus`
- `OllamaBackend`
- `OpenAICompatibleBackend`
- `SessionManager`
- `PromptManager`
- `AgentManager`
- `PluginContext`
- `LoadedPlugin`
- `PluginManager`
- `DiagnosticsSignals`
- `QtLogHandler`
- `LineBufferedStream`
- `OperationStreamParser`
- `AsyncTask`
- `StreamTask`
- `plugins.sample_plugin.Plugin`

## MainWindow method inventory

The source-complete `main_window.py` method inventory is preserved in section 31.3 of the canonical census. It includes every method from `__init__` through `closeEvent`, including nested callback functions created inside generation, model-operation, template, and async paths.

## Dialog method inventory

`dialogs.py` source-complete method inventory:

- `ModelfileHighlighter.highlightBlock`
- `EndpointDialog.__init__`, `add_row`, `accept`
- `ModelfileEditor.__init__`, `new`, `open_file`, `save`, `duplicate`, `validate`, `build_model`, `update_preview`
- `PromptManagerDialog.__init__`, `refresh`, `load_selected`, `new`, `save`, `delete`, `import_prompt`, `export_prompts`
- `AgentBuilderDialog.__init__`, `refresh`, `load_selected`, `new`, `_agent`, `save`, `import_agent`, `export_agent`
- `PluginManagerDialog.__init__`, `refresh`, `apply`, `reload_plugins`
- `ParameterDialog.__init__`, nested `spin`, nested `dbl`, `_collect`, `save_preset`, `load_preset`, `accept`

## Added production UI

`ModelBrowserDialog`:
- `__init__`
- `filter_models`
- `open_library`
- `pull_selected`

`FirstRunWizard`:
- `__init__`
- `_build_welcome_page`
- `_build_hardware_page`
- `_build_backend_page`
- `_build_finish_page`
- `_recommended_model`
- `_page_changed`
- `_check_backend`
- `accept`

`production_fixes.py` module functions:
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

## Line metadata limitation

The source connector exposes complete source and file boundaries but not structured AST line/column metadata. The two formerly truncated large files are now verified to end at:
- `locallama_gui/ui/main_window.py`: line 1,050
- `locallama_gui/ui/dialogs.py`: line 600

No source line offset is invented where the connector does not expose it.
