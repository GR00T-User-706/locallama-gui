# LocalLama GUI

A production-grade **native desktop UI** for managing local and remote LLMs. Built with PySide6—chat, model operations, Modelfiles, system prompts, agents, plugins, and full diagnostics all in one power-user workstation.

Works with **Ollama**, **OpenAI-compatible APIs**, and **llama.cpp** servers. Python 3.11+, Linux/macOS/Windows.

---

## Quick Start

```bash
# 1. Create venv and install
python3.11 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e .

# 2. Start your backend (example: Ollama)
ollama serve

# 3. Launch the GUI
locallama-gui
# or: python -m locallama_gui
```

**First time?**
1. Open **Settings → API Endpoints** to configure your backend
2. Click **Refresh Models** or **Models → Pull** to list available models
3. Create a chat tab, pick a model, send a message

---

## Features at a Glance

| Feature | Details |
|---------|---------|
| **Chat interface** | Multi-tab chat, streaming/non-streaming, persistent sessions, Markdown/JSON/TXT export |
| **Model operations** | Pull, push, clone, delete, inspect Ollama templates and metadata |
| **Modelfile editor** | Syntax highlighting, validation, version history, config preview |
| **System prompts** | Library with categories, favorites, import/export, search, version control |
| **Generation profiles** | Sampling, context, GPU layers, stop sequences, reasoning mode |
| **Agents** | Visual agent builder: model, tools, plugins, memory, reasoning, execution policy |
| **Plugins** | Drop-in Python modules for tools, commands, interceptors, UI panels, memory providers |
| **Diagnostics** | Structured logs, captured console output, model operations, request viewer, token stream, backend status |
| **Desktop UX** | Dockable panels, dark theme, keyboard shortcuts, menu bar, layout presets |

---

## Requirements

- **Python:** 3.11, 3.12, or 3.13 (tested in CI)
- **Backend (one of):**
  - Ollama at `http://localhost:11434` (default)
  - OpenAI-compatible `/v1` endpoint
  - llama.cpp OpenAI-compatible server

---

## Installation

### From repository (development)

```bash
git clone https://github.com/GR00T-User-706/locallama-gui.git
cd locallama-gui
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Desktop launcher (Linux/macOS)

```bash
# Install user-local launcher script
./scripts/install-launcher

# (Optional) Install Linux desktop entry
./scripts/install-desktop-entry
```

See [`docs/LAUNCHING.md`](docs/LAUNCHING.md) for full launcher and platform-specific details.

---

## Usage

### Run the application

```bash
locallama-gui
```

### Main menu overview

| Menu | Purpose |
|------|---------|
| **File** | New/open/save/import/export chats |
| **Models** | Pull, push, clone, create, delete, open Modelfiles, inspect templates |
| **Agents** | Create/manage/import/export agent profiles |
| **Plugins** | Manage, install, reload plugins |
| **Settings** | API endpoints, generation parameters, themes, keyboard shortcuts, model defaults |
| **View** | Panel visibility, layout presets |
| **Developer** | Diagnostics tabs, request viewer, token viewer, request inspector |
| **Help** | Documentation, diagnostics, about |

Diagnostics are separated by role: **Logs** shows structured Python logging records, **Console** captures stdout/stderr-style process output, and **Operations** tracks model lifecycle status. Pull, push, clone, create, delete, and template inspection write `[START]`, meaningful progress/status transitions, `[OK]`, and `[ERROR]` entries to Operations without flooding Console or chat token output. Ollama error payloads received during a successful HTTP stream are treated as operation failures, so they cannot be followed by a misleading success entry.

See [`docs/FEATURE_MATRIX.md`](docs/FEATURE_MATRIX.md) for the current status of visible application workflows.

### Data locations

The app uses platform-native directories via `platformdirs`:

- **Config:** `user_config_dir("locallama-gui", "LocalLama")`
- **Data:** `user_data_dir("locallama-gui", "LocalLama")`
- **Logs:** `user_log_dir("locallama-gui", "LocalLama")`

Use **Help → Diagnostics** to see exact paths on your system.

---

## Advanced Topics

### Plugin development

Drop plugin files into the user plugin directory or repository `plugins/` directory.

- Full SDK: [`docs/PLUGIN_SDK.md`](docs/PLUGIN_SDK.md)
- Sample: [`plugins/sample_plugin.py`](plugins/sample_plugin.py)

Plugins can provide:
- Custom tools and commands
- Chat interceptors
- UI panels
- Automation
- Memory providers
- Backend integrations

### Project structure

```
locallama_gui/
  app.py                 # Application entry point
  backends/              # Ollama / OpenAI-compatible backends
  core/                  # Config, domain models, managers, plugin registry
  ui/                    # PySide6 main window, dialogs, workers, theming
plugins/                 # Development and sample plugins
docs/                    # SDK and user documentation
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Model refresh fails | Confirm backend is running (e.g., `ollama serve`) |
| Can't connect to remote server | Open **Settings → API Endpoints** and verify the base URL and port |
| Plugins fail to load | Disable untrusted plugins; review diagnostics logs in **Developer → Logs** |

---

## Project governance

- **Code of Conduct:** [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)
- **License:** [`LICENSE`](LICENSE)
- **Security:** [`SECURITY.md`](SECURITY.md)
- **Issue templates:** [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/)

### Legacy code

Older experimental Tkinter and Qt5/QML artifacts are archived under `archive/old_apps/ollama_GUI/` for historical reference.  
Additional legacy code is archived under `archive/legacy_code/` with an index at [`archive/ARCHIVE_INDEX.md`](archive/ARCHIVE_INDEX.md).

---

## Screenshots

<img width="1453" height="979" alt="LocalLama GUI chat interface" src="https://github.com/user-attachments/assets/64dca141-3edf-4d59-9093-c78629dcd7e7" />

<img width="1920" height="1023" alt="LocalLama GUI model and plugin management" src="https://github.com/user-attachments/assets/20f4e35c-8989-4e62-8d90-20255fe75b99" />

---

## Versioning and changelog

This project uses **semantic versioning** (`MAJOR.MINOR.PATCH`):
- **PATCH:** bug fixes, documentation, test improvements
- **MINOR:** new backward-compatible features
- **MAJOR:** breaking changes

See [`CHANGELOG.md`](CHANGELOG.md) for release history.  
See [`docs/REPO_ANALYSIS.md`](docs/REPO_ANALYSIS.md) for architecture and cleanup status.
