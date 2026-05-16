# LocalLama GUI

LocalLama GUI is a production-oriented PySide6 desktop control center for local and remote LLMs. It is designed as a power-user workstation: chat client, model manager, Modelfile editor, prompt library, agent builder, diagnostics console, and plugin-capable AI environment in one native desktop app.

## Highlights

- **Native desktop UI** built with PySide6: dockable panels, menu bar, tabs, dark theme, keyboard-friendly layout.
- **Multi-provider backends** for Ollama-compatible APIs, OpenAI-compatible APIs, and llama.cpp OpenAI-compatible servers.
- **Full chat workflow** with multi-chat tabs, streaming/non-streaming generation, persistent sessions, stop/regenerate/retry, role-aware history, and Markdown/JSON/TXT export.
- **Model operations** for Ollama: list, pull, push, clone, delete, inspect templates/metadata, and build from Modelfiles.
- **Modelfile editor** with syntax highlighting, validation, save/duplicate/version history, and generated config preview.
- **System prompt manager** with persistent prompt library, categories, favorites, import/export, search-ready storage, and version history.
- **Parameter profiles** covering sampling, generation, context, GPU layers, stop sequences, and reasoning mode toggles.
- **Plugin system** with drop-in Python modules for tools, commands, chat interceptors, UI panels, automation, memory providers, and backend integrations.
- **Agent builder** for visual agent profile creation with model, tools, plugin assignment, memory mode, reasoning mode, behavior, and execution policy.
- **Developer diagnostics**: request viewer, token stream viewer, backend status, latency, logs, terminal diagnostics, and plugin errors.

## Requirements

- Python 3.13+
- A local or remote LLM backend:
  - Ollama at `http://localhost:11434` by default, or
  - OpenAI-compatible `/v1` endpoint, or
  - llama.cpp server exposing OpenAI-compatible endpoints.

## Installation

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e .
```

If your platform uses `python3` for Python 3.13, substitute accordingly.

## Run

```bash
locallama-gui
```

or

```bash
python -m locallama_gui
```

## First Use

1. Start your backend, for example `ollama serve`.
2. Launch `locallama-gui`.
3. Open **Settings → API Endpoints** to add or edit provider profiles.
4. Click **Refresh Models** or use **Models** menu actions.
5. Create a chat tab, select a model, and send a message.

## Core Menus

- **File**: new/open/save/save-as/import/export chats and exit.
- **Models**: pull, push, clone, create, delete, open Modelfiles, inspect templates.
- **Agents**: create/manage/import/export agent profiles.
- **Plugins**: manage, install, reload, and open developer SDK docs.
- **Settings**: API endpoints, generation parameters, themes, shortcuts, model settings.
- **View**: panel visibility, layout presets, logs, terminal.
- **Developer**: logs, request viewer, token viewer, API inspector, debug console.
- **Help**: documentation, about, diagnostics.

## Data Locations

The app uses platform-native directories via `platformdirs`:

- Config: `user_config_dir("locallama-gui", "LocalLama")`
- Data: `user_data_dir("locallama-gui", "LocalLama")`
- Logs: `user_log_dir("locallama-gui", "LocalLama")`

Use **Help → Diagnostics** inside the app to see exact paths on your system.

## Plugin Development

Drop plugin files into the user plugin directory or repository `plugins/` directory. See [`docs/PLUGIN_SDK.md`](docs/PLUGIN_SDK.md) and [`plugins/sample_plugin.py`](plugins/sample_plugin.py). Plugins can register tools, commands, chat interceptors, custom panels, automation hooks, memory providers, and integrations.

## Project Structure

```text
locallama_gui/
  app.py                 # application entry point
  backends/              # Ollama/OpenAI-compatible backend implementations
  core/                  # config, domain models, managers, plugin registry
  ui/                    # PySide6 main window, dialogs, workers, theme
plugins/                 # development/sample plugins
docs/                    # plugin SDK and user documentation
```

## Legacy Code

The older experimental Tkinter and Qt5/QML artifacts remain under `ollama_GUI/` for historical reference. The supported production application is the PySide6 package exposed by `locallama-gui`.
