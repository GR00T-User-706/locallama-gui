# Known Bugs

This document is the working tracker for defects discovered during manual testing, especially live GUI testing.

## How to use this file

- Keep each confirmed defect as a separate entry.
- Record what was actually observed. Do not infer a root cause unless it has been verified.
- Use the status values: `open`, `investigating`, `fixed`, `wont-fix`, or `cannot-reproduce`.
- When fixing a bug, record the relevant files, tests performed, and the commit/PR when available.
- Keep this document synchronized with related project documentation when a bug changes the documented behavior of a feature.
- An AI agent should inspect this file before changing code related to a listed defect.

## Bug template

```markdown
### BUG-### — Short title

- **Status:** open
- **Severity:** low | medium | high | critical
- **Area:** UI | theme | menus | settings | backend | plugins | models | etc.
- **Observed:** What was actually seen during testing.
- **Expected:** What should happen.
- **Reproduction:** Minimal steps to reproduce.
- **Evidence:** Screenshot, log, or other evidence if available.
- **Likely code areas:** Files/modules worth inspecting. Mark as `unconfirmed` until verified.
- **Fix notes:** Leave blank until a fix is made.
- **Verification:** How the fix should be tested.
```

## Fixed bugs

### BUG-004 — Invalid import syntax in Ollama backend

- **Status:** fixed
- **Severity:** critical
- **Area:** backend / Ollama
- **Observed:** The module began with invalid Python syntax in the future-import statement.
- **Expected:** The backend module must be valid Python and importable.
- **Fix notes:** Corrected the import to `from __future__ import annotations`.
- **Verification:** Active source inspection confirms the corrected syntax; repository CI remains the final automated validation.

### BUG-005 — Invalid import syntax in OpenAI-compatible backend

- **Status:** fixed
- **Severity:** critical
- **Area:** backend / OpenAI-compatible
- **Observed:** The module began with invalid Python syntax in the future-import statement.
- **Expected:** The backend module must be valid Python and importable.
- **Fix notes:** Corrected the import to `from __future__ import annotations`.
- **Verification:** Active source inspection confirms the corrected syntax; repository CI remains the final automated validation.

### BUG-001 — Diagnostics appears in multiple menus

- **Status:** fixed
- **Severity:** low
- **Area:** UI / menus
- **Observed:** The `Diagnostics` action was previously visible in multiple menus and opened the same diagnostics panel.
- **Expected:** Diagnostics should have a clear, intentional menu placement without redundant duplicate entries.
- **Reproduction:** Launch the application and inspect the `Help`, `Developer`, and `View` menus.
- **Evidence:** The current production startup calls `apply_production_fixes()`, which removes the redundant Help/View actions and rebuilds the Developer diagnostics submenu.
- **Likely code areas:** `locallama_gui/ui/main_window.py`, `locallama_gui/ui/production_fixes.py`.
- **Fix notes:** Production menu cleanup is present in active code.
- **Verification:** Static verification of the menu-building and production-fix paths.

### BUG-003 — Model Settings has no observable effect during initial GUI testing

- **Status:** fixed
- **Severity:** medium
- **Area:** Settings / models / generation
- **Observed:** Opening `Model Settings` did not produce an obvious observable effect during live GUI testing.
- **Expected:** Model/generation settings should visibly persist or affect the next backend request.
- **Fix notes:** The production path exposes `AI Model Settings...`, persists `config.parameters`, and the generation path consumes `to_backend_options()`.
- **Verification:** Static verification confirmed the settings-to-request path.

### BUG-002 — Light theme makes prompt output text unreadable

- **Status:** fixed
- **Severity:** high
- **Area:** UI / themes
- **Observed:** Switching to a light system palette could leave chat message blocks using a dark hard-coded background without a corresponding light text color.
- **Expected:** Chat output must remain readable under both the custom dark theme and the native System/light theme.
- **Reproduction:** Launch the application, switch the theme to System/light, then inspect the prompt/output panel.
- **Evidence:** `ChatTab.render()` previously hard-coded `background:#171a21` and relied on the surrounding stylesheet for text color. The System theme clears that stylesheet.
- **Likely code areas:** `locallama_gui/ui/main_window.py`, `locallama_gui/ui/theme.py`, `_choose_theme()` in `locallama_gui/ui/production_fixes.py`.
- **Fix notes:** `ChatTab.render()` now reads the active Qt palette and applies its base/text colors to each rendered message block. The custom dark theme continues to provide the dark palette while System/light uses the native palette.
- **Verification:** Static verification confirms the renderer no longer hard-codes the message-block background and text pair. Dark and System/light GUI smoke testing should be included in the next native desktop validation run.

## Open bugs

No currently documented open bugs remain in this tracker.
