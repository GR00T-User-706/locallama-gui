# Windows native installer

This directory contains the end-user Windows distribution layer for LocalLama Control Center.

## What it produces

The GitHub Actions workflow builds two layers:

1. A PyInstaller application bundle containing the Python runtime, LocalLama GUI package, PySide6, and runtime dependencies.
2. An Inno Setup installer named `LocalLama-Control-Center-Setup.exe`.

The installed application does not require the end user to install Python, pip, Git, or use a terminal.

## Build workflow

The workflow is `.github/workflows/windows-installer.yml`.

It runs on a Windows GitHub-hosted runner and:

- installs Python 3.13
- installs PyInstaller
- builds `packaging/windows/locallama-gui.spec`
- installs Inno Setup
- reads the application version from `pyproject.toml`
- builds the graphical Windows installer
- verifies that the expected installer exists
- uploads the installer as a workflow artifact

The workflow runs for relevant pull requests, can be started manually with `workflow_dispatch`, and also runs for version tags beginning with `v`.

## Installer behavior

The installer:

- installs LocalLama Control Center into the user's application directory
- creates a Start Menu shortcut
- offers an optional Desktop shortcut
- provides an uninstaller
- offers to launch LocalLama Control Center after installation

It does not install Ollama, collect API keys, or modify LocalLama application configuration.

## Developer/source installation

This native installer does not replace `scripts/install-wizard.py`. The Python installer remains the developer/source installation path for contributors and advanced users.

## Current limitations

- Windows packaging is the first native distribution target.
- The application bundle and installer must be validated on a real Windows machine before a public release is declared production-ready.
- Code signing is not configured yet.
- Native Linux and macOS packaging are separate future work.
