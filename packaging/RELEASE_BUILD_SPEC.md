# MyLoAI Release Build Specification

## Product identity

- Product: MyLoAI Control Center
- Short name: MyLoAI
- Repository: locallama-gui
- Canonical Linux command: `myloai`
- Canonical Python package namespace remains `locallama_gui` for compatibility with the existing application.

## Release principles

1. Preserve existing application behavior unless packaging explicitly requires an integration shim.
2. Build from the active production application path only.
3. Never package repository archives or development-only material.
4. Keep platform packaging separate from application runtime logic.
5. Validate staged payloads before generating final installer artifacts.
6. Produce reproducible, inspectable release metadata where the target platform permits it.

## Target artifacts

- Windows native installer and bundled application.
- macOS application bundle and disk image.
- Linux Debian package.
- Linux Arch package.
- Linux RPM package.
- Linux AppImage.

## End-user content allowed in release payloads

- Application help and usage documentation.
- Linux manual page.
- License and required third-party notices.
- Installer/uninstaller documentation required by the target platform.

All source-control, CI, tests, archive, agent, prompt, contributor, and internal analysis files remain repository-only.

## Verification gates

A release is not considered production-ready until:

- the Python distribution builds successfully;
- the application entry point launches from the installed package;
- the staged payload passes the exclusion check;
- each target package has its expected executable/launcher and documentation;
- package metadata identifies MyLoAI Control Center;
- the canonical `myloai` launcher works on Linux;
- existing `locallama-gui` compatibility is preserved unless intentionally changed in a separately reviewed release decision.
