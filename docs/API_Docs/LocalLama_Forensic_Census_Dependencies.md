# LocalLama Forensic Census Dependencies

## Static and dynamic imports

Static application dependencies include:
- `locallama_gui.app -> core.config, core.logging, ui.main_window, ui.production_fixes`
- `MainWindow -> backends, config, domain, managers, chat_view, controllers, diagnostics, dialogs, theme, workers`
- controllers -> backend factory / diagnostics / workers / Qt dialogs
- managers -> config/domain plus `ast`, `importlib.util`, `json`, `shutil`
- backends -> `httpx`, domain/backend abstractions

Dynamic import boundaries:
- controller-local `PySide6.QtWidgets` imports
- `__import__("json")` in agent export/import
- `importlib.util.spec_from_file_location` for plugins
- local diagnostic/worker imports inside first-run wizard

## HTTP

Ollama:
- `GET /api/tags`
- `POST /api/chat`
- `POST /api/pull`
- `POST /api/push`
- `DELETE /api/delete`
- `POST /api/copy`
- `POST /api/create`
- `POST /api/show`

OpenAI-compatible:
- `GET /models`
- `POST /chat/completions`

## Worker boundaries

1. `MainWindow._generate -> StreamTask -> backend.chat`
2. `MainWindow.refresh_backend -> AsyncTask -> test_connection/list_models`
3. `MainWindow._async -> AsyncTask`
4. `MainWindow.run_async -> AsyncTask`
5. `MainWindow.build_model_from_modelfile -> StreamTask -> create_model`
6. `MainWindow.open_template_viewer -> AsyncTask -> show_model`
7. `ModelController._model_stream_op -> StreamTask`
8. `ModelBrowserDialog.pull_selected -> StreamTask -> pull_model`
9. `FirstRunWizard._check_backend -> AsyncTask`
10. `FirstRunWizard.accept -> StreamTask`

`AsyncTask.run()` uses `asyncio.run` in a `QThread`.
`StreamTask.run()` consumes async iterators and emits token/error/completion signals.
`MainWindow.worker_refs` retains workers.
Chat streams use `_stream_owner_seq` and `_active_stream_owner` for stale-result suppression.

## Filesystem

Primary paths:
- config dir from `platformdirs.user_config_dir`
- data dir from `platformdirs.user_data_dir`
- logs dir from `platformdirs.user_log_dir`
- sessions JSON
- prompts JSON
- agents JSON
- modelfiles and `.versions`
- plugin Python files
- config JSON
- user-selected import/export destinations
- bundled documentation paths

## Environment

- `QT_ENABLE_HIGHDPI_SCALING=1`
- `QT_AUTO_SCREEN_SCALE_FACTOR=1`

## Plugin boundary

`discover -> static AST manifest -> trust -> dynamic import -> instantiate -> runtime manifest validation -> activate(context)`

Context registries:
- `tools`
- `commands`
- `chat_interceptors`
- `memory_providers`

Verified invocation:
- chat interceptors run in `_generate`
- panels call `MainWindow.add_plugin_panel`
- deactivate runs during disable/reload/untrust/remove

No verified active dispatcher for arbitrary registered tools/commands.
No `register_memory_provider` method exists.

## Persistence

- config JSON
- OS keyring
- sessions JSON
- prompts JSON
- agents JSON
- Modelfiles/version copies
- chat exports
- log file
- Qt geometry/state encoded into config

## Trust boundaries

- provider API key -> keyring -> backend auth header
- plugin source -> AST validation -> trust -> dynamic import
- user/session messages -> request payload
- streamed model output -> `ChatMessage` -> UI/session
- file-dialog paths -> JSON/text serializers
