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
