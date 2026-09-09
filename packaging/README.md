# MyLoAI Production Packaging

This directory contains release packaging definitions for **MyLoAI Control Center**.

The repository remains `locallama-gui`; the installed product is MyLoAI Control Center and the canonical short command is `myloai`.

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

The legacy `locallama-gui` entry point remains available during the transition unless a future compatibility decision explicitly removes it.
