# Active Code Audit

Date: 2026-09-23
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

### AUDIT-006 — Production packaging workflow still asserts version 1.2.9

- **Status:** open
- **Severity:** high
- **File:** `.github/workflows/release-packaging.yml`
- **Symbol:** `python-package` / `Validate distribution identity and entry points`
- **Observed:** The active production-packaging branch is version `1.2.10` in `pyproject.toml`, but the workflow contains two hard-coded assertions for `1.2.9`: `data['project']['version'] == '1.2.9'` and `dist['Version'] == '1.2.9'`.
- **Impact:** The Python distribution packaging job will fail its validation step whenever it builds the current `1.2.10` package. This is a directly demonstrable CI/package validation mismatch and is a likely explanation for a CI failure notification on the production branch.
- **Evidence:** `pyproject.toml` currently declares `version = "1.2.10"`; `docs/VERSIONING.md` records `1.2.10` as the current state; the workflow still asserts `1.2.9`. The workflow runs on pull requests and therefore validates the active production branch.
- **Recommended next investigation/fix:** Replace the stale hard-coded validation value with a check derived from the repository's canonical version source, or otherwise synchronize the workflow assertion to the current release process. Do not change source code during this audit.

### AUDIT-007 — Arch PKGBUILD is pinned to stale application version 1.2.9

- **Status:** open
- **Severity:** high
- **File:** `packaging/linux/PKGBUILD`
- **Symbol:** `pkgver` and `source`
- **Observed:** `pkgver=1.2.9` while the active package source of truth is `1.2.10`.
- **Impact:** The Arch package definition requests the `v1.2.9` source archive and therefore does not describe the current active application release. Attempting to package the current `1.2.10` tree with this PKGBUILD would target the wrong release source and package metadata.
- **Evidence:** `pyproject.toml` and `docs/VERSIONING.md` are `1.2.10`; `packaging/linux/PKGBUILD` remains `1.2.9` and constructs its source URL directly from `${pkgver}`.
- **Recommended next investigation/fix:** Synchronize `pkgver` with the canonical application version before using this PKGBUILD for a release. Keep the existing source URL structure unless the packaging contract is intentionally changed.

### AUDIT-008 — Linux man page reports stale application version

- **Status:** open
- **Severity:** medium
- **File:** `packaging/linux/myloai.1`
- **Symbol:** `.TH` header
- **Observed:** The man page identifies itself as `MyLoAI Control Center 1.2.9` with a `2026-09-21` date, while the active application version is `1.2.10` dated 2026-09-22.
- **Impact:** Installed Linux users can receive incorrect version information from the packaged `myloai(1)` documentation. The stale version also violates the repository's documented version synchronization target for user-facing version references.
- **Evidence:** `docs/VERSIONING.md` requires user-facing version references to be checked during version bumps. The active man page still contains `1.2.9`; `pyproject.toml` is `1.2.10`.
- **Recommended next investigation/fix:** Update the man-page version/date as part of the next version-synchronization change. No source/package file was modified by this audit.

### AUDIT-009 — Windows installer fallback version is stale

- **Status:** open
- **Severity:** low
- **File:** `packaging/windows/MyLoAI.iss`
- **Symbol:** `MyLoAIVersion` fallback definition
- **Observed:** The Inno Setup script defaults `MyLoAIVersion` to `1.2.9`, while the active application version is `1.2.10`.
- **Impact:** The normal `build-installer.ps1` path explicitly passes the version read from `pyproject.toml`, so the standard CI build is not currently affected. However, invoking `MyLoAI.iss` directly without `/DMyLoAIVersion=...` produces an installer labeled `1.2.9`, creating a stale packaging fallback and inconsistent standalone installer behavior.
- **Evidence:** `packaging/windows/build-installer.ps1` reads the version from `pyproject.toml` and passes it to Inno Setup. `packaging/windows/MyLoAI.iss` still defines the fallback as `1.2.9`.
- **Recommended next investigation/fix:** Synchronize the fallback with the canonical version or replace the fallback with a mechanism that cannot silently drift. No packaging source was modified during this audit.

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

- Current application version: `1.2.10`.
- This audit did not modify application source, package definitions, or version numbers.
- The newly confirmed version-sync findings above require a separate fix pass if changes are authorized.

## Validation

- `archive/**` was completely excluded from implementation and validation scope.
- Active production branch resolved to commit `18b2d39317c2327c8322c32380e4943f4215007d`.
- `pyproject.toml`, `docs/VERSIONING.md`, active packaging workflow, Arch PKGBUILD, Linux man page, and Windows installer script were inspected.
- Static inspection confirmed the stale `1.2.9` references described in AUDIT-006 through AUDIT-009.
- GitHub commit status for `18b2d39317c2327c8322c32380e4943f4215007d` currently returns no status entries through the available connector; therefore this audit does not claim a current CI result beyond the demonstrable workflow/version mismatch.
- Full `ruff check .` and `pytest` execution is delegated to repository GitHub Actions because the GitHub connector cannot execute the repository test suite directly.

## Authorization-required items

- BUG-002 remains unchanged in source code. Human authorization is required to choose the intended System/Light chat-output styling before implementing a narrowly scoped theme correction.
- AUDIT-006 through AUDIT-009 are documented only. No source, packaging, or workflow file was modified during this audit.

## Repository instruction note

`AGENTS.md` and `CODE_OF_CONDUCT.md` were inspected before implementation. `CONTRIBUTORS.md` does not exist on the active branch; `CONTRIBUTING.md` does exist. No contributor-specific instructions were invented or inferred from the missing filename. `AGENTS.md` requires minimal changes, synchronized versioning, changelog maintenance for implementation changes, and explicit exclusion of `archive/**` from routine validation.
