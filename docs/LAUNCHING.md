# Launching LocalLama GUI

## Launch methods

- Package script: `locallama-gui`
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

The desktop entry references the scalable application icon:

```text
packaging/linux/icons/com.github.gr00t-user-706.locallama-gui.svg
```

The desktop installer must install that icon into an XDG icon-theme location before refreshing the desktop database so the entry resolves its `Icon=` name correctly.

Dry run:

```bash
./scripts/install-desktop-entry --dry-run
```
