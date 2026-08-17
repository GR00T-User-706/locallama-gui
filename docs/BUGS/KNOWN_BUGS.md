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

## Open bugs

### BUG-001 — Diagnostics appears in multiple menus

- **Status:** open
- **Severity:** low
- **Area:** UI / menus
- **Observed:** The `Diagnostics` action is visible in multiple menus (`Help`, `Developer`, and `View`) and opens the same diagnostics panel.
- **Expected:** Diagnostics should have a clear, intentional menu placement without redundant duplicate entries unless the duplicates are explicitly designed as shortcuts.
- **Reproduction:** Launch the application and inspect the `Help`, `Developer`, and `View` menus. Activate each `Diagnostics` action.
- **Evidence:** Found during live GUI testing in the GitHub Codespaces + noVNC environment.
- **Likely code areas:** `locallama_gui/ui/main_window.py` — **unconfirmed**; inspect menu construction before changing anything.
- **Fix notes:** Do not remove or relocate actions until the intended menu organization is confirmed.
- **Verification:** Confirm the final menu layout contains only the intentional Diagnostics entry/entries and that the remaining action opens the expected diagnostics panel.

### BUG-002 — Light theme makes prompt output text unreadable

- **Status:** open
- **Severity:** high
- **Area:** UI / themes
- **Observed:** Switching the application from Dark theme to Light theme changes the background, but text in the prompt/output panel becomes unreadable or effectively invisible.
- **Expected:** All visible text and controls should remain readable in Light theme with sufficient contrast.
- **Reproduction:** Launch the application, switch the theme from Dark to Light, then inspect the prompt/output panel.
- **Evidence:** Found during live GUI testing in the GitHub Codespaces + noVNC environment.
- **Likely code areas:** `locallama_gui/ui/theme.py` and theme-toggle logic in `locallama_gui/ui/main_window.py` — **unconfirmed**; inspect stylesheet/palette and any widget-level formatting before changing anything.
- **Fix notes:** Determine whether the problem comes from global stylesheet/palette handling, widget-specific formatting, or both. Do not assume root cause from appearance alone.
- **Verification:** Test the affected panel in both Dark and Light themes and confirm text/background contrast remains readable after toggling themes repeatedly.

### BUG-003 — Model Settings has no observable effect during initial GUI testing

- **Status:** investigating
- **Severity:** medium
- **Area:** Settings / models / generation
- **Observed:** Opening `Model Settings` did not produce an obvious observable effect during live GUI testing.
- **Expected:** Model/generation settings should either visibly change application state or affect the next backend request in a verifiable way.
- **Reproduction:** Open the relevant Model Settings/Parameters UI and change settings. Observe the application behavior.
- **Evidence:** Found during live GUI testing in the GitHub Codespaces + noVNC environment. Backend functionality was not connected during this observation, so end-to-end request behavior was not verified.
- **Likely code areas:** `locallama_gui/ui/dialogs.py`, `locallama_gui/core/config.py`, `locallama_gui/ui/main_window.py`, and backend request builders — **unconfirmed**.
- **Fix notes:** First verify whether values are saved into `AppConfig.parameters`, then verify whether those values are included in the backend request. This bug should remain `investigating` until the backend path is tested.
- **Verification:** Change a parameter, confirm it persists, inspect the outbound request, and confirm the backend receives the expected value.
