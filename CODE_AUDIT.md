# Active Code Audit

Date: 2026-09-22
Branch: feat/myloai-production-packaging
Scope: Active repository paths only. `archive/**` was excluded.

## Audit result

### AUDIT-003 — Syntax error in first-run setup wizard

- **Status:** fixed
- **Severity:** critical
- **File:** `locallama_gui/ui/setup_wizard.py`
- **Symbol:** `FirstRunWizard._check_backend()` / local callback `done`
- **Observed:** The callback declaration was `def done(status) -> None` without the required trailing colon.
- **Impact:** `locallama_gui.ui.setup_wizard` could not be parsed/imported. This made the first-run wizard unusable and caused active CI Ruff parsing failures.
- **Evidence:** The finding was verified against the active production-packaging branch before modification. GitHub Actions run `35612497283` for commit `7e9c52add78267f3eb2f799529602c00c329ddda` failed in all Python matrix jobs during Ruff parsing with `invalid-syntax: Expected ':', found newline` at `locallama_gui/ui/setup_wizard.py:150:33`.
- **Minimal fix:** Added only the missing `:` to the callback declaration.
- **Validation:** The corrected module was inspected for the syntax defect. Repository CI is required for full Ruff/pytest validation after this commit.

### AUDIT-004 — About dialog reports stale application version

- **Status:** fixed
- **Severity:** medium
- **File:** `locallama_gui/ui/production_fixes.py`
- **Symbol:** `_show_about`
- **Observed:** The About dialog hard-coded `Version 1.2.8`, while the active package metadata and module version were `1.2.9`.
- **Impact:** Users saw an incorrect application version in the production UI.
- **Evidence:** `pyproject.toml` and `locallama_gui/__init__.py` were verified at `1.2.9` before modification. The active `_show_about()` displayed `Version 1.2.8`.
- **Minimal fix:** `_show_about()` now displays the canonical `locallama_gui.__version__` value. The application version was bumped from `1.2.9` to `1.2.10` as required for the implementation change.
- **Validation:** Static inspection confirms the About dialog imports and uses `__version__`; `pyproject.toml`, `locallama_gui/__init__.py`, and `docs/VERSIONING.md` are synchronized to `1.2.10`.

### AUDIT-005 — Plugin SDK documentation action resolves the wrong source-tree path

- **Status:** fixed
- **Severity:** medium
- **File:** `locallama_gui/ui/production_fixes.py`
- **Symbols:** `_resource_path`, `_open_bundled_document`, `apply_production_fixes`
- **Observed:** In a non-frozen/source-tree run, `_resource_path()` resolved every requested document to `<repo>/packaging/<name>`. The production menu opened `PLUGIN_SDK.md`, but the active document is `docs/PLUGIN_SDK.md`.
- **Impact:** The Developer Mode/Plugin SDK documentation action failed in source-tree runs with an unable-to-open-document warning.
- **Evidence:** The active source path and frozen PyInstaller layout were verified before modification. Frozen builds use `<MEIPASS>/docs`, while the active repository stores `docs/PLUGIN_SDK.md`.
- **Minimal fix:** The non-frozen resource resolver now maps only `PLUGIN_SDK.md` to the active `docs/` path and preserves the existing `packaging/` lookup for the user manual.
- **Validation:** Static inspection confirms source-tree and frozen lookup paths remain distinct and the Developer Mode action still requests `PLUGIN_SDK.md`. Repository CI is required for full validation after this commit.

## Existing documented findings reviewed

### BUG-001 — Diagnostics appears in multiple menus

- **Status:** fixed without source change in this run.
- **Verification:** `MainWindow` initially creates Diagnostics actions in Help, View, and Developer, but `app.main()` calls `apply_production_fixes()` before showing the window. That function removes Diagnostics from Help and View and rebuilds the Developer diagnostics submenu. The documented duplicate state is therefore stale on the current production path.

### BUG-002 — Light theme makes prompt output text unreadable

- **Status:** authorization required
- **Severity:** high
- **Verification:** Current active code confirms the symptom has a plausible active-code basis: `ChatTab.render()` hard-codes dark HTML backgrounds while `_choose_theme()` clears the global stylesheet for the System theme. A minimal correction requires choosing whether chat blocks should follow the native palette or retain the existing dark styling. That behavior choice is not established by the current documentation, so no code was changed.
- **Required authorization:** Human approval of the intended light/System chat-output appearance before changing `locallama_gui/ui/main_window.py`, `locallama_gui/ui/theme.py`, or `_choose_theme()` behavior.

### BUG-003 — Model Settings has no observable effect during initial GUI testing

- **Status:** fixed without source change in this run.
- **Verification:** `apply_production_fixes()` replaces the legacy `Model Settings` action with `AI Model Settings...` connected to `window.open_parameters()`. `ParameterDialog.accept()` saves the collected values into `config.parameters`, and `MainWindow._generate()` reads `config.parameters.to_backend_options()` for the next request. The original documented observation is stale relative to this active production wiring.

## Versioning and changelog

- Application version bumped from `1.2.9` to `1.2.10` because implementation changes were made.
- Updated `pyproject.toml` and `locallama_gui/__init__.py` to `1.2.10`.
- Updated `docs/VERSIONING.md` current-state snapshot to `1.2.10`.
- Added the `1.2.10` entry to `CHANGELOG.md`.
- No configuration schema change was made.

## Validation

- `archive/**` was completely excluded from implementation and validation scope.
- Pre-change findings were verified against current active code before modification.
- The missing-colon syntax defect was corrected.
- Version synchronization was statically verified across package metadata, runtime metadata, versioning documentation, and changelog.
- Plugin SDK source-tree and frozen resource-path logic was statically verified.
- Full `ruff check .` and `pytest` execution is delegated to the repository's GitHub Actions CI because the GitHub connector cannot execute the repository test suite directly.

## Authorization-required items

- BUG-002 remains unchanged in source code. Human authorization is required to choose the intended System/Light chat-output styling before implementing a narrowly scoped theme correction.

## Repository instruction note

`AGENTS.md` and `CODE_OF_CONDUCT.md` were inspected before implementation. `CONTRIBUTORS.md` does not exist on the active branch, so no contributor-specific instructions could be read from that filename. `AGENTS.md` requires minimal changes, synchronized versioning, changelog maintenance for implementation changes, and explicit exclusion of `archive/**` from routine validation.
