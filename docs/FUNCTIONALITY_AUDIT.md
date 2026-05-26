# Functionality Audit (Baseline)

Date: 2026-05-25
Scope: Baseline feature-state matrix for the active production app.

## Classification

- CONFIRMED: directly supported by observed code/tests/docs.
- LIKELY: strong evidence exists but not fully runtime-verified in this pass.
- UNKNOWN: requires manual validation or deeper trace.

## Feature Matrix

| Feature Area | State | Confidence | Evidence | Notes |
|---|---|---|---|---|
| App bootstrap (`locallama_gui/app.py`) | present | CONFIRMED | entrypoint wiring | Active runtime identified. |
| PySide6 main window + docks | present | CONFIRMED | `ui/main_window.py` | Central UI surface is active. |
| Provider profiles/config persistence | present | CONFIRMED | `core/config.py` | Config load/save implemented. |
| Ollama backend integration | present | CONFIRMED | `backends/ollama.py` + manager wiring | Core model/chat API surface exists. |
| OpenAI-compatible backend integration | present | CONFIRMED | `backends/openai.py` | Alternate provider path exists. |
| Async/stream worker support | present | CONFIRMED | `ui/workers.py` | Supports non-blocking operations. |
| Session/prompt/agent/plugin managers | present | CONFIRMED | `core/managers.py` | Core workflow managers exist. |
| Menu/action clarity and duplication | needs audit | UNKNOWN | mission + monolithic menu file | Requires `MENU_MAP` expansion. |
| Create model UX clarity | needs audit | UNKNOWN | mission concerns | Needs dialog/action walkthrough. |
| Delete model UX safety/reliability | needs audit | UNKNOWN | mission concerns | Needs explicit destructive-flow QA. |
| Developer terminal usefulness | needs audit | UNKNOWN | mission concerns | Validate practical utility and messaging. |
| Parameter UX documentation quality | incomplete docs | CONFIRMED | missing doc baseline before this phase | Now baseline doc exists; deeper guide pending. |

## Confirmed Non-Production/Parallel Trees

### CONFIRMED
- `archive/old_apps/ollama_GUI/` and `archive/legacy_code/llm_studio/` are archived legacy/parallel code, not active runtime.

### UNKNOWN
- Whether selected utilities within those trees still provide maintainer-only value.

## Baseline Gaps

### CONFIRMED
- Missing docs now created in Phase 1 baseline:
  - `PRODUCTION_CODE_MAP.md`
  - `VERSIONING.md`
  - `UI_ACTION_AUDIT.md`
  - `MENU_MAP.md`
  - `PARAMETERS.md`
  - `QA_CHECKLIST.md`
  - `FUNCTIONALITY_AUDIT.md`

### UNKNOWN
- Exact UI action failure inventory until dedicated manual audit pass.

## TODO
- Add per-feature test case links and ownership mapping.
- Split UNKNOWN items into prioritized fix candidates after UI action audit pass.
