# Installation Wizard

LocalLama GUI includes `scripts/install-wizard.py` for a safe, repeatable installation from a repository checkout.

This is the **repository/source installer**. It creates an isolated virtual environment, installs the package, verifies runtime imports, and integrates existing launch mechanisms. It does not install Ollama, other AI servers, or API credentials.

## Supported Python versions

The repository supports Python 3.11, 3.12, and 3.13. The wizard rejects versions outside that range.

## Quick start

From the repository root:

```bash
python3 scripts/install-wizard.py
```

On Windows:

```powershell
py -3.12 scripts\install-wizard.py
```

The wizard creates `.venv` by default and installs the project with `pip install -e .`.

## Options

```text
--venv DIR             Use a different virtual-environment directory.
--python EXECUTABLE    Select the Python interpreter used to create the venv.
--dry-run              Show planned actions without making installation changes.
--no-launcher          Skip Unix launcher integration.
--desktop-entry        Also install the Linux desktop entry.
--windows-desktop      Also create a Windows desktop shortcut.
--check-backend [URL]  Test a backend after installation. Without a URL,
                       checks the default local Ollama API.
```

Examples:

```bash
python3 scripts/install-wizard.py --dry-run
python3 scripts/install-wizard.py --desktop-entry
python3 scripts/install-wizard.py --check-backend
python3 scripts/install-wizard.py --check-backend http://127.0.0.1:8080/v1/models
```

## Platform behavior

### Linux

The wizard reuses the canonical repository scripts instead of duplicating desktop integration logic:

- `scripts/install-launcher`
- `scripts/install-desktop-entry` when `--desktop-entry` is supplied

The launcher and desktop entry remain user-local.

### macOS

The wizard installs the Python application and reuses the canonical launcher integration. It does not create a Linux `.desktop` entry or attempt to install a native `.app` bundle.

### Windows

The wizard creates a Start Menu shortcut targeting the installed virtual-environment Python interpreter and `python -m locallama_gui`. A desktop shortcut can be added with `--windows-desktop`.

PowerShell's built-in Windows Script Host COM interface is used for `.lnk` creation, so no `pywin32` dependency is required.

## Backend configuration

The installer does **not** install or configure an AI backend. After installation, configure one from **Settings → API Endpoints**.

Supported backend families documented by the application include Ollama, OpenAI-compatible APIs, and llama.cpp servers.

API credentials are deliberately not collected or written by the installer.

## Native distribution

The wizard is not the final native application installer. Future platform-native artifacts such as a Windows installer, macOS application bundle, or Linux package/AppImage can be added separately without changing this source-install workflow.

## Safety and behavior

- Commands are executed with argument lists rather than `shell=True`.
- Existing virtual environments are reused rather than deleted or silently replaced.
- The wizard does not modify application configuration files.
- `--dry-run` is available before installation changes.
- Backend connectivity checks are optional and do not affect installation success.
