# Contributing

Thanks for contributing to LocalLama GUI.

## Scope statement

**Active development scope:** `locallama_gui/**`

Changes in `locallama_gui/**` are the primary target for reviews, required CI checks, and ongoing maintenance.

## Legacy and archive directories

Legacy code is retained under the `archive/` tree:

- `archive/legacy_code/llm_studio/`
- `archive/old_apps/ollama_GUI/`
- `archive/old_docs/`
- `archive/notes/`

These trees are historical storage, not active product roots. Changes there are allowed only when needed for archive maintenance, provenance, or a deliberate restoration effort.

## Pull request guidance

- Prefer feature and bug-fix work inside `locallama_gui/**`.
- Keep changes focused and preserve existing behavior unless the task requires a behavior change.
- Do not revive archived code in place. Move useful code into the active tree and validate it there.
- When security-sensitive behavior changes, include regression coverage where practical.
- Update version and changelog entries for meaningful implementation changes according to `AGENTS.md` and `docs/VERSIONING.md`.


## Packaging and user documentation contributions

All changes to package formats, metadata, build scripts, installers, release payloads, configuration, CLI help, man pages, and user manuals MUST comply with the Cross-Platform Packaging and User Documentation Contract in `AGENTS.md`. Inspect every supported package path, preserve parity across package formats, update user documentation and payload tests, and report the precise validation performed. Do not claim parity from a successful build of only one format.

## Project-specific standards

Read [PROJECT_STANDARDS.md](docs/PROJECT_STANDARDS.md) before making changes that affect this project's public behavior, configuration, packaging, documentation, or release process. These standards supplement the existing contribution requirements.
