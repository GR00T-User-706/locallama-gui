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
- **Observed:** The module began with `rrom __ruture__ import annotations`, which is invalid Python syntax.
- **Expected:** The backend module must be valid Python and importable.
- **Fix notes:** Corrected the import to `from __future__ import annotations`.
- **Verification:** Pending repository CI validation.

### BUG-005 — Invalid import syntax in OpenAI-compatible backend

- **Status:** fixed
- **Severity:** critical
- **Area:** backend / OpenAI-compatible
- **Observed:** The module began with `rrom __ruture__ import annotations`, which is invalid Python syntax.
- **Expected:** The backend module must be valid Python and importable.
- **Fix notes:** Corrected the import to `from __future__ import annotations`.
- **Verification:** Pending repository CI validation.

### BUG-001 — Diagnostics appears in multiple menus

- **Status:** fixed
- **Severity:** low
- **Area:** UI / menus
- **Observed:** The `Diagnostics` action was previously visible in multiple menus (`Help`, `Developer`, and `View`) and opened the same diagnostics panel.
- **Expected:** Diagnostics should have a clear, intentional menu placement without redundant duplicate entries unless the duplicates are explicitly designed as shortcuts.
- **Reproduction:** Launch the application and inspect the `Help`, `Developer`, and `View` menus. Activate each `Diagnostics` action.
- **Evidence:** The current production startup calls `apply_production_fixes()`. That function removes `Diagnostics` from `Help` and `View` and rebuilds the `Developer` diagnostics submenu, so the documented duplicate state is stale.
- **Likely code areas:** `locallama_gui/ui/main_window.py`, `locallama_gui/ui/production_fixes.py`.
- **Fix notes:** No code change was required in this run because the production menu correction is already present in active code. Marked fixed after verification.
- **Verification:** Static verification of `MainWindow._build_view_menu()`, `_build_developer_menu()`, `_build_help_menu()`, `apply_production_fixes()`, and `app.main()` confirmed the production menu cleanup is applied before the window is shown.

### BUG-003 — Model Settings has no observable effect during initial GUI testing

- **Status:** fixed
- **Severity:** medium
- **Area:** Settings / models / generation
- **Observed:** Opening `Model Settings` did not produce an obvious observable effect during live GUI testing.
- **Expected:** Model/generation settings should either visibly change application state or affect the next backend request in a verifiable way.
- **Reproduction:** Open the relevant Model Settings/Parameters UI and change settings. Observe the application behavior.
- **Evidence:** The current production startup replaces the legacy `Model Settings` action with `AI Model Settings...`, wired directly to `window.open_parameters()`. `ParameterDialog.accept()` writes the collected values to `config.parameters` and saves the configuration. `MainWindow._generate()` reads `self.config.parameters.to_backend_options()` for the next backend request. The documented observation was made before this production menu wiring was verified.
- **Likely code areas:** `locallama_gui/ui/dialogs.py`, `locallama_gui/core/config.py`, `locallama_gui/ui/main_window.py`, backend request builders.
- **Fix notes:** No code change was required in this run because the current active path is wired and the documented symptom is stale. Marked fixed after static verification of the save-to-request path.
- **Verification:** Static verification confirmed the settings dialog is reachable through `AI Model Settings...`, persists `AppConfig.parameters`, and the generation path consumes `to_backend_options()`.

## Open bugs

### BUG-002 — Light theme makes prompt output text unreadable

- **Status:** investigating
- **Severity:** high
- **Area:** UI / themes
- **Observed:** Switching the application from Dark theme to Light theme changes the background, but text in the prompt/output panel becomes unreadable or effectively invisible.
- **Expected:** All visible text and controls should remain readable in Light theme with sufficient contrast.
- **Reproduction:** Launch the application, switch the theme from Dark to Light, then inspect the prompt/output panel.
- **Evidence:** Found during live GUI testing in the GitHub Codespaces + noVNC environment. Current active code confirms the prompt/output renderer uses hard-coded dark HTML block backgrounds while the System theme clears the global stylesheet.
- **Likely code areas:** `locallama_gui/ui/theme.py`, `locallama_gui/ui/main_window.py`, and `_choose_theme()` in `locallama_gui/ui/production_fixes.py`.
- **Fix notes:** Human authorization is required before changing this behavior. The current renderer and theme model do not establish a single minimal correction that preserves both the existing dark styling and the intended native System theme without deciding how chat/output colors should be themed. Do not change code until that behavior choice is authorized.
- **Verification:** After an authorized fix, test the affected panel in both Dark and System/Light themes and confirm text/background contrast remains readable after toggling themes repeatedly.
