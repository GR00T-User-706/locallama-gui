# Active Code Audit

Date: 2026-09-24
Branch: feat/myloai-production-packaging
Scope: Active repository paths only. `archive/**` was excluded completely.

## Findings

### AUDIT-003 — Syntax error in first-run setup wizard
- **Status:** fixed
- **Severity:** critical
- **File:** `locallama_gui/ui/setup_wizard.py`
- **Symbol:** `FirstRunWizard._check_backend()` / local callback `done`
- **Finding:** `def done(status) -> None` was missing its trailing colon, preventing parsing/import.
- **Evidence:** CI run `35612497283` failed during Ruff parsing at `locallama_gui/ui/setup_wizard.py:150:33` with `invalid-syntax: Expected ':', found newline`.
- **Fix:** Added only the missing `:`.
- **Validation:** Static syntax inspection; repository CI required for full Ruff/pytest validation.

### AUDIT-004 — About dialog reported stale application version
- **Status:** fixed
- **Severity:** medium
- **File:** `locallama_gui/ui/production_fixes.py`
- **Symbol:** `_show_about`
- **Finding:** About dialog hard-coded `1.2.8` while active package/module version was `1.2.9`.
- **Fix:** Uses canonical `locallama_gui.__version__`; application version was subsequently bumped to `1.2.10` as required by the implementation change.
- **Validation:** Static inspection confirmed version source and synchronized version documentation.

### AUDIT-005 — Plugin SDK documentation action resolved wrong source-tree path
- **Status:** fixed
- **Severity:** medium
- **File:** `locallama_gui/ui/production_fixes.py`
- **Symbols:** `_resource_path`, `_open_bundled_document`, `apply_production_fixes`
- **Finding:** Source-tree lookup sent documentation requests to `packaging/`, while active `PLUGIN_SDK.md` is under `docs/`.
- **Fix:** Source-tree resolver maps `PLUGIN_SDK.md` to `docs/`; existing packaging lookup for the user manual was preserved.
- **Validation:** Static inspection of source-tree and frozen resource paths.

### AUDIT-006 — Production packaging workflow still asserts version 1.2.9
- **Status:** open
- **Severity:** high
- **File:** `.github/workflows/release-packaging.yml`
- **Symbol:** `python-package` / `Validate distribution identity and entry points`
- **Finding:** Workflow asserts both `data['project']['version'] == '1.2.9'` and `dist['Version'] == '1.2.9'`, while canonical version is `1.2.10`.
- **Impact:** Python distribution validation fails for the current release.
- **Evidence:** `pyproject.toml` and `docs/VERSIONING.md` report `1.2.10`; workflow remains hard-coded to `1.2.9`.
- **Recommended fix:** Derive the expected version from the canonical version source or synchronize the assertion with the release process. No code was changed during this audit.

### AUDIT-007 — Arch PKGBUILD is pinned to stale application version 1.2.9
- **Status:** open
- **Severity:** high
- **File:** `packaging/linux/PKGBUILD`
- **Symbol:** `pkgver`, `source`
- **Finding:** `pkgver=1.2.9`, and the source archive URL is constructed from that value, while the active release is `1.2.10`.
- **Impact:** The PKGBUILD targets the wrong release archive and metadata.
- **Evidence:** `pyproject.toml`/`docs/VERSIONING.md` are `1.2.10`; PKGBUILD remains `1.2.9`.
- **Recommended fix:** Synchronize `pkgver` with the canonical application version.

### AUDIT-008 — Linux man page reports stale application version
- **Status:** open
- **Severity:** medium
- **File:** `packaging/linux/myloai.1`
- **Symbol:** `.TH` header
- **Finding:** Reports `MyLoAI Control Center 1.2.9` dated `2026-09-21`; active release is `1.2.10` dated `2026-09-22`.
- **Impact:** Packaged user documentation reports incorrect version metadata.
- **Recommended fix:** Synchronize the man-page version/date during the next version-synchronization change.

### AUDIT-009 — Windows installer fallback version is stale
- **Status:** open
- **Severity:** low
- **File:** `packaging/windows/MyLoAI.iss`
- **Symbol:** `MyLoAIVersion` fallback
- **Finding:** Direct Inno Setup invocation defaults to `1.2.9`; the normal `build-installer.ps1` path overrides it from `pyproject.toml`.
- **Impact:** Standard CI is not currently affected, but direct standalone compilation can produce an installer labeled `1.2.9`.
- **Recommended fix:** Synchronize the fallback with the canonical version or eliminate silent drift.

### AUDIT-010 — Routine CI lints the archived tree despite the active-code validation policy
- **Status:** open
- **Severity:** medium
- **File:** `.github/workflows/ci.yml`
- **Symbol:** `tests` job / `Lint` step
- **Finding:** CI runs `ruff check .` from repository root without excluding `archive/**`. `pyproject.toml` also has no Ruff `exclude` configuration.
- **Impact:** Historical archive content can affect routine CI even though repository policy explicitly excludes archived trees from routine lint/test validation.
- **Evidence:** Active workflow contains `ruff check .`; `AGENTS.md` requires active-path-only routine validation and explicit archive exclusion.
- **Recommended fix:** Scope routine Ruff validation to active paths or configure Ruff to exclude `archive/**`. Do not inspect or modify archived files for this fix.

## Existing documented bugs reviewed

### BUG-001 — Diagnostics appears in multiple menus
- **Status:** fixed / stale finding
- **Verification:** `app.main()` applies `apply_production_fixes()` before the window is shown; that function removes Diagnostics from Help/View and rebuilds the Developer submenu. No code change required in this audit.

### BUG-002 — Light theme makes prompt output text unreadable
- **Status:** authorization required
- **Severity:** high
- **Verification:** Active code still has a plausible basis for the documented symptom: chat rendering uses hard-coded dark HTML backgrounds while System theme clears the global stylesheet.
- **Constraint:** No code changed because the intended System/Light chat-output styling has not been specified. Human authorization is required before changing the theme behavior.

### BUG-003 — Model Settings has no observable effect during initial GUI testing
- **Status:** fixed / stale finding
- **Verification:** Current production path replaces the legacy action with `AI Model Settings...`, persists `config.parameters`, and generation consumes `to_backend_options()`. No code change required.

### BUG-004 — Invalid import syntax in Ollama backend
- **Status:** fixed
- **Verification:** Active `locallama_gui/backends/ollama.py` now begins with valid `from __future__ import annotations` syntax.

### BUG-005 — Invalid import syntax in OpenAI-compatible backend
- **Status:** fixed
- **Verification:** Active OpenAI-compatible backend was previously corrected to valid future-import syntax.

## Branch and scope

- Default branch: `main`.
- Production packaging branch audited: `feat/myloai-production-packaging`, commit `5f6485d3c7c1df2a232f001feee3ae9769730374`.
- `main` and the production packaging branch are substantially divergent (248 commits ahead, 12 behind). The configured production packaging branch was treated as authoritative for packaging/runtime audit scope.
- Other feature branches were not treated as production packaging targets because no repository configuration identifies them as such.
- `archive/**` was excluded completely. No archived file contents were inspected, audited, or used as evidence.

## Versioning and changelog

- Current application version: `1.2.10`.
- This audit made no application source, packaging, workflow, version, or changelog changes.
- Per `docs/VERSIONING.md`, audit-only work does not bump the version.
- `CONTRIBUTORS.md` does not exist; `CONTRIBUTING.md` does.

## Validation

- Read-only inspection performed before documenting findings.
- Inspected `AGENTS.md`, `CODE_OF_CONDUCT.md`, `docs/VERSIONING.md`, `pyproject.toml`, `CODE_AUDIT.md`, `docs/BUGS/KNOWN_BUGS.md`, active CI workflows, production packaging workflow, active Ollama backend, and relevant Linux/Windows packaging files.
- Confirmed AUDIT-006 through AUDIT-010 against the current production branch.
- GitHub workflow execution was not claimed as passed because the available connector did not expose a current status for the audited commit.
- Local Ruff/pytest execution was not performed; this audit tool has no repository execution environment.

## Authorization-required items

- BUG-002 remains unchanged and requires human approval of intended System/Light chat-output styling before implementation.
- AUDIT-006 through AUDIT-010 are documented findings only; no fixes were applied during this read-only audit.

## Repository instructions

`AGENTS.md` requires minimal changes, version synchronization for implementation changes, changelog maintenance for implementation changes, and exclusion of `archive/**` from routine validation. `CODE_OF_CONDUCT.md` provides contributor conduct requirements. `docs/VERSIONING.md` confirms `pyproject.toml` as the application version source and states that audit-only work must not bump versions.
