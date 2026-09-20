# MyLoAI Production Packaging

This directory contains release packaging definitions for **MyLoAI Control Center**.

The repository remains `locallama-gui`; the installed product is MyLoAI Control Center, the canonical short Linux command is `myloai`, and the filesystem-safe application executable identity is `MyLoAI_Control_Center`. Production filesystem paths must not contain spaces.

Release packages must contain only the production application, required runtime resources, required third-party runtime dependencies, license/notices required for redistribution, and concise user-facing documentation appropriate to the platform.

They must not include repository archives, development agents/prompts, CI configuration, tests, historical code, contributor documentation, internal analysis, or unrelated project material.

## Package targets

- Python: wheel and source distribution
- Debian-family Linux: `.deb`
- Arch-family Linux: `PKGBUILD` / `.pkg.tar.zst`
- Portable Linux: AppImage
- Windows: native installer/bundled application
- macOS: `.app` and `.dmg` for arm64 and x86_64

The package build definitions are intentionally separate from the active runtime package so that distribution concerns do not alter application behavior.

## Product command

Linux packages expose:

```text
myloai
```

For Debian, `/usr/bin/myloai` launches the bundled `/opt/myloai/MyLoAI_Control_Center`. For AppImage, `AppRun` launches `usr/bin/MyLoAI_Control_Center`. Native production launchers do not depend on the source-tree `run-locallama` launcher.

The legacy `locallama-gui` entry point remains available during the transition unless a future compatibility decision explicitly removes it.
