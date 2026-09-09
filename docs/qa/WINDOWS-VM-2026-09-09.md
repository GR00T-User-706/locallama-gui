# Windows VM QA Findings - 2026-09-09

This document records defects observed during clean Windows 10 VM acceptance testing of the MyLoAI Control Center production installer.

## Confirmed defects

### Packaging/runtime

- The first Windows production artifact installed successfully but crashed at launch because `locallama_gui/__main__.py` used a package-relative import when frozen by PyInstaller.
- The frozen application now uses an absolute package import for the entry point.
- The native GUI logging configuration produced secondary `NoneType.write` errors when no console stream existed. The console `StreamHandler` has been removed; the GUI diagnostics handler and file logger remain.
- Installed documentation actions attempted to read `README.md` and `docs/PLUGIN_SDK.md` from the current working directory. Those files were not present in the installed application. Native packaging now bundles the user manual and Plugin SDK and the application resolves them from the frozen resource directory.

### Navigation and menu duplication

- View → Diagnostics, Developer → Diagnostics, and Help → Diagnostics exposed the same diagnostics surface. Only one Diagnostics entry is retained in the production UI.
- Developer → Request Inspector opened the same Request Viewer dock. The duplicate Request Inspector action is removed until a genuinely distinct inspector surface exists.
- Settings → Model Settings was wired to backend refresh rather than a distinct model-settings surface. The misleading duplicate action is removed.
- Agents → Create, Manage, Import, and Export all opened the same Agent Builder. Import and Export now have distinct file-based behavior; Create/Manage remain builder entry points until a dedicated agent manager surface is implemented.

### Model discovery and onboarding

- Models → Pull required users to already know the exact Ollama model name. A discoverable **Browse & Pull Models...** surface is now added with curated starter models and a direct link to the official Ollama model library.
- A first-run setup wizard is now added. It reports CPU/RAM, chooses a conservative starter model, checks the local Ollama endpoint, and can pull the starter model when Ollama is available.
- The wizard does not pretend to know GPU capability when reliable cross-platform GPU telemetry is unavailable.

## Deferred functional testing

- Chat generation against a live Ollama service on Windows remains to be tested after Ollama is installed in the VM.
- Remote OpenAI-compatible provider testing remains deferred.
- Linux packaging failures are tracked separately and are not treated as Windows defects.
- Theme design is a separate UI pass. The current production patch makes the existing Theme action functional without expanding the scope into a wholesale visual redesign.

## Acceptance rule

A Windows build is not release-ready until a clean Windows VM can install it, launch it without a traceback, display branded application identity, access bundled documentation, complete first-run setup, discover/pull a starter model, and complete a basic chat generation test against the configured backend.
