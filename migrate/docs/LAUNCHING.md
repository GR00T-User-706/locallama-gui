# Launching MyLoAI Control Center

MyLoAI Control Center is the end-user product name. The repository and Python
module namespace remain `locallama-gui` / `locallama_gui` for compatibility.

## Native installers

Production releases provide native installation media for supported platforms:

- Windows: MyLoAI Control Center `.exe` installer
- macOS: MyLoAI Control Center `.dmg`
- Linux: AppImage and amd64 Debian `.deb`
- Arch Linux: `PKGBUILD` source package recipe

Debian, AppImage, Windows, and macOS production artifacts bundle the application runtime and do not require Python, pip, Git, or PyInstaller at runtime. The Arch `PKGBUILD` is a native Arch Python package recipe and intentionally uses system Python/runtime dependencies.

## Production launch methods

- Canonical Linux command: `myloai`
- Debian installed executable: `/opt/myloai/MyLoAI_Control_Center`
- AppImage entry point: `AppRun`
- Filesystem-safe executable identity: `MyLoAI_Control_Center`
- Compatibility Python command: `locallama-gui`

The production Linux desktop entry uses `Exec=myloai`. Native package launch
paths do not invoke the repository source-tree launcher.

## Source/development launch methods

These methods are for repository development only:

- `python -m locallama_gui`
- `./run-locallama`
- `./scripts/install-launcher`
- `./scripts/install-desktop-entry`

The source-tree launcher and its installation helpers are not part of the
native production runtime path.

## Development launcher dry runs

```bash
./scripts/install-launcher --dry-run
```
The desktop entry references the scalable application icon:

```text
packaging/linux/icons/com.github.gr00t-user-706.locallama-gui.svg
```

The desktop installer must install that icon into an XDG icon-theme location before refreshing the desktop database so the entry resolves its `Icon=` name correctly.

Dry run:

```bash
./scripts/install-desktop-entry --dry-run
```

Production users should install the generated native artifact instead of using
these source-tree helpers.
