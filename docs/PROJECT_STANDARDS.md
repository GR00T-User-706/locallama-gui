# MyLoAI Control Center Project Standards

The repository is named `locallama-gui`; the user-facing application name is MyLoAI Control Center. These standards supplement `AGENTS.md`, `CONTRIBUTING.md`, the architecture and configuration references, and the packaging/user-manual documentation.

## Product identity and interface

Treat this project as a desktop GUI application. Document actual workflows through the GUI, including navigation, dialogs, settings, model operations, chat behavior, plugin management, diagnostics, and error recovery. The user manual must describe what is present in the current application, not planned interface concepts.

Keep the repository/package identifier distinct from the product display name where platform conventions require it. Do not rename identifiers or files as part of documentation work.

## Backend and provider behavior

Document each implemented backend and its real capabilities, prerequisites, configuration, authentication requirements, error handling, and limitations. Distinguish local model hosting from remote API providers. Do not claim provider parity where capabilities differ.

Explain model discovery, download/pull, selection, runtime availability, and failure states according to observed implementation. Document security boundaries around credentials, local configuration, network requests, and plugin execution.

## Configuration and plugins

Maintain a complete configuration reference tied to the actual schema and defaults. Cover setting names, types, defaults, validation, persistence, precedence, and restart/reload requirements.

Document the plugin lifecycle, discovery locations, manifest/entry-point expectations, permissions or trust assumptions, compatibility boundaries, and error behavior. Do not describe sample plugins as a complete plugin ecosystem.

## Packaging and release payload

For each distribution format actually supported by the project, document prerequisites, build process, runtime model, installed files, launcher behavior, configuration locations, and limitations. Keep the user-visible application behavior and required resources consistent across supported formats.

The existence of a build script or packaging recipe alone does not prove a release artifact is successfully built or installable. Separate source packaging, native builds, payload inspection, and clean installation tests in validation reports. Keep the canonical release payload documentation authoritative and update every affected supported format when that payload changes.

## User documentation

The user manual must cover first launch, backend setup, model management, chat workflows, settings, plugins, diagnostics, data locations, troubleshooting, upgrades, and removal to the extent those features exist. Include screenshots or examples only when verified against the current UI.

## Versioning and documentation-only changes

Follow the existing repository version source and SemVer rules for implementation changes. Documentation-only changes do not require a version bump unless existing policy explicitly says otherwise. Record documentation additions in the changelog without implying application behavior changed.
