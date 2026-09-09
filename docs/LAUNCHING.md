# Launching MyLoAI Control Center

MyLoAI Control Center is the end-user product name. The repository and Python
module namespace remain `locallama-gui` / `locallama_gui` for compatibility.

## Native installers

Production releases provide native installation media for supported platforms:

- Windows: MyLoAI Control Center `.exe` installer
- macOS: MyLoAI Control Center `.dmg`
- Linux: AppImage and amd64 Debian `.deb`
- Arch Linux: `PKGBUILD`

Native installers bundle the application runtime and do not require Python,
pip, Git, or a terminal.

## Launch methods

- Canonical package command: `myloai`
- Compatibility command: `locallama-gui`
- Module: `python -m locallama_gui`
- Repository launcher: `./run-locallama`

## Install user launcher

```bash
./scripts/install-launcher
```

Default target: `${HOME}/.local/bin/run-locallama`

Dry run:

```bash
./scripts/install-launcher --dry-run
```

## Install desktop entry

```bash
./scripts/install-desktop-entry
```

Default target: `${HOME}/.local/share/applications/com.github.gr00t-user-706.locallama-gui.desktop`

Dry run:

```bash
./scripts/install-desktop-entry --dry-run
```
