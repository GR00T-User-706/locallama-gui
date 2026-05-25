# QA Checklist (Baseline)

Date: 2026-05-25
Scope: Baseline validation checklist for active production app.

## Static/Automated Checks

Run these in repo root:

1. `ruff check .`
2. `python -m compileall -q locallama_gui`
3. `pytest tests` (preferred scoped suite; avoid repo-wide pytest until CI scoping is repaired)

## Smoke Checklist (Manual)

### Launch & Stability
- [ ] App launches from `locallama-gui`
- [ ] App launches from `python -m locallama_gui`
- [ ] Startup with unavailable backend shows clear non-crashing status/error

### Chat Core
- [ ] New chat tab creates successfully
- [ ] Send message works
- [ ] Stop generation works
- [ ] Retry/regenerate work and update chat state correctly

### Model Ops
- [ ] Refresh model list works without UI freeze
- [ ] Pull model flow handles success and errors
- [ ] Create model flow has clear prompts and error handling
- [ ] Delete model flow is explicit and safe

### Parameters
- [ ] Reasoning mode persists across restart
- [ ] Reasoning mode sends expected backend flags
- [ ] Parameter presets save/load correctly

### Plugins
- [ ] Plugin manager opens
- [ ] Enable/disable plugin state persists
- [ ] Plugin load errors are surfaced to user logs/status

### Developer/Diagnostics
- [ ] Logs panel updates
- [ ] Request Viewer copy/clear works
- [ ] Token Viewer copy/clear works

## CONFIRMED
- Static checks #1 and #2 are suitable for Phase 1 and do not require CI/app refactor work.

## LIKELY
- `pytest tests` is the correct scoped test invocation for production package validation.

## UNKNOWN
- Full manual pass/fail outcomes for the checklist items in this baseline document.

## TODO
- Add per-item expected result text and failure triage links.
