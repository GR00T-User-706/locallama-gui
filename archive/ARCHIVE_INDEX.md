# Archive Index

This file tracks archival moves and archive decisions.

## 2026-05-25

### Completed archive move reconciliation

- Reason: synchronize archive records with completed local archival moves now present in this repository state.
- Scope: documentation/records reconciliation only; no additional archive move actions performed in this pass.

| Original path | Archived path | Date archived | Reason archived | Useful logic remains? | Related version/changelog entry |
|---|---|---|---|---|---|
| `ollama_GUI/` | `archive/old_apps/ollama_GUI/` | 2026-05-25 | Legacy Tkinter and Qt/QML app trees superseded by active PySide6 runtime in `locallama_gui/`. | Yes (historical implementation reference) | 1.0.10 (documentation reconciliation) |
| `llm_studio/` | `archive/legacy_code/llm_studio/` | 2026-05-25 | Parallel legacy/experimental tree not part of active production runtime. | Yes (reference patterns and historical modules) | 1.0.10 (documentation reconciliation) |
| `FUNCTIONALITY_STATUS.md` | `archive/old_docs/FUNCTIONALITY_STATUS.md` | 2026-05-25 | Historical status snapshot retained as non-active documentation. | Yes (historical context) | 1.0.10 (documentation reconciliation) |
| `SECURITY_REVIEW.md` | `archive/old_docs/SECURITY_REVIEW.md` | 2026-05-25 | Historical review artifact retained for provenance. | Yes (historical context) | 1.0.10 (documentation reconciliation) |
| `HUMAN_REVIEW.md` | `archive/notes/HUMAN_REVIEW.md` | 2026-05-25 | Human-process note preserved in archive notes namespace. | Yes (process context) | 1.0.10 (documentation reconciliation) |

### Archive manifests

- `archive/manifests/ARCHIVE_MANIFEST.md`
- `archive/manifests/duplicate_manifest.md`
