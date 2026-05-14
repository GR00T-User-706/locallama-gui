# locallama-gui

A dual-frontend GUI application for managing and interacting with Ollama (local LLM self-hosting service). Choose between a lightweight Python/Tkinter implementation or a feature-rich Qt5/QML interface.

## Overview

**locallama-gui** provides two distinct graphical interfaces to interact with Ollama, a framework for running large language models locally. Both implementations share a common backend architecture while offering different UX paradigms optimized for different use cases.

## Features

- **Dual GUI Options**: Select the interface that best fits your workflow
  - **Tkinter Frontend** (`ollama-gui-py`): Lightweight, minimal dependencies, quick startup
  - **Qt5/QML Frontend** (`ollama-gui-qt`): Rich UI, advanced features, native desktop integration
- **Backend Support**: Unified backend architecture supporting both frontends
- **Local LLM Integration**: Direct integration with Ollama self-hosting service
- **Network Capabilities**: Built-in networking support for remote Ollama instances
- **Cross-Platform**: Designed to run on Linux, macOS, and Windows

## Repository Structure

```
locallama-gui/
├── ollama_GUI/
│   ├── ollama-gui-py/          # Python Tkinter implementation
│   │   ├── bin/                # Executable entry points
│   │   ├── lib/                # Python libraries and utilities
│   │   └── data/               # Data files and resources
│   │
│   ├── ollama-gui-qt/          # Qt5/QML implementation
│   │   ├── src/                # C++ source files
│   │   │   ├── main.cpp        # Application entry point
│   │   │   ├── backend.cpp/.h  # Backend logic
│   │   │   └── OllamaManager.cpp/.h  # Ollama API wrapper
│   │   ├── assets/             # Icons and desktop integration files
│   │   ├── ollama-gui-qt.pro   # Qt project file (QMake)
│   │   └── resources.qrc       # Qt resource configuration
│   │
│   └── addons/                 # Optional extensions
│       ├── ai-mon.py           # AI monitoring utility
│       └── ollama_tools/       # Additional Ollama tools
```

## Getting Started

### Prerequisites

#### For Qt5/QML Implementation
- Qt 5.x or higher (with QML support)
- C++17 compatible compiler
- CMake or QMake build system
- libqt5core, libqt5gui, libqt5qml, libqt5network

#### For Tkinter Implementation
- Python 3.7+
- tkinter (usually included with Python)
- Additional Python dependencies (see requirements)

#### System Requirements
- Ollama service running locally or accessible via network
- Linux, macOS, or Windows

### Installation

#### Qt5/QML Frontend

```bash
cd ollama_GUI/ollama-gui-qt
qmake ollama-gui-qt.pro
make
./ollama-gui-qt
```

Or using CMake (if available):
```bash
cd ollama_GUI/ollama-gui-qt
mkdir build && cd build
cmake ..
make
./ollama-gui-qt
```

#### Tkinter Frontend

```bash
cd ollama_GUI/ollama-gui-py
python3 bin/main.py
```

## Technology Stack

| Component | Technology | Usage |
|-----------|-----------|-------|
| Qt Frontend | C++17, Qt5, QML | Rich desktop UI |
| Python Frontend | Python 3, Tkinter | Lightweight alternative |
| Backend | C++ (Qt) / Python | Ollama API abstraction |
| Networking | Qt Network, Python sockets | Remote Ollama communication |
| Build System | QMake, CMake | Project compilation |

## Architecture

### Backend
- **OllamaManager**: Centralized wrapper for Ollama REST API communication
- **backend.cpp/backend.h**: Core business logic and state management
- Supports network operations for both local and remote Ollama instances

### Frontend (Qt5/QML)
- Modern QML-based interface
- Native desktop file integration for application menu/launcher
- Asynchronous network operations to prevent UI blocking
- Resource embedding for standalone deployment

### Frontend (Python/Tkinter)
- Cross-platform Tkinter widgets
- Minimal startup overhead
- Pure Python implementation for portability

## Addons

- **ai-mon.py**: System monitoring utility for AI workloads
- **ollama_tools**: Additional utilities for Ollama management and scripting

## Building

### Qt Frontend (QMake)
```bash
qmake CONFIG+=release
make
make install  # Optional: installs desktop file and icon to /usr/local/share/
```

### Qt Frontend (CMake)
```bash
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make
make install
```

## Usage

1. **Start Ollama Service**:
   ```bash
   ollama serve
   ```

2. **Launch GUI** (choose one):
   ```bash
   # Qt interface
   ./ollama-gui-qt
   
   # Or Tkinter interface
   python3 ollama-gui-py/bin/main.py
   ```

3. **Configure Ollama Connection**: 
   - Specify Ollama host (default: localhost:11434)
   - Select available models
   - Adjust inference parameters

## Development

### Project Files
- **ollama-gui-qt.pro**: Qt project configuration (QMake)
- **ollama-gui-qt.kdev4**: KDevelop IDE configuration

### Build Artifacts
The `.gitignore` excludes:
- Compiled objects and libraries
- Qt meta-object compiler output (moc_*.cpp/h)
- Build directories and CMake files
- IDE temporary files

### Code Organization
- Source files: `src/` directory
- Resource files: `resources.qrc` (icons, assets)
- Desktop integration: `assets/` directory

## Contributing

Contributions are welcome. Focus areas:
- UI/UX improvements for both frontends
- Additional Ollama API features
- Cross-platform compatibility testing
- Performance optimization

## License

See repository for license details.

## Related Projects

- **Ollama**: https://ollama.ai/ - Local LLM framework
- **Qt**: https://www.qt.io/ - Cross-platform GUI framework
- **Tkinter**: https://docs.python.org/3/library/tkinter.html - Python GUI toolkit

## Language Composition

- **C++**: 48.4% (Qt frontend implementation)
- **Python**: 47.9% (Tkinter frontend + utilities)
- **QML**: 3.6% (Qt interface markup)
- **QMake**: 0.1% (Build configuration)

---

**Status**: Early development 
**Repository**: https://github.com/GR00T-User-706/locallama-gui
