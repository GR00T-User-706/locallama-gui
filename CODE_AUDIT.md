# Active Code Audit

Date: 2026-09-24
Branch: main
Scope: Active repository paths only. `archive/**` was excluded completely.

## Findings

### AUDIT-003 — Syntax error in first-run setup wizard
- **Status:** fixed
- **Severity:** critical
- **File:** `locallama_gui/ui/setup_wizard.py`
- **Finding:** `def done(status) -> None` was missing its trailing colon, preventing parsing/import.
- **Fix:** Added only the missing `:`.
- **Validation:** Static syntax inspection; repository CI remains required for full Ruff/pytest validation.

### AUDIT-004 — About dialog reported stale application version
- **Status:** fixed
- **Severity:** medium
- **File:** `locallama_gui/ui/production_fixes.py`
- **Finding:** About dialog previously hard-coded an older version.
- **Fix:** Uses canonical `locallama_gui.__version__`.
- **Validation:** Active source inspection confirms canonical version display.

### AUDIT-005 — Plugin SDK documentation action resolved wrong source-tree path
- **Status:** fixed
- **Severity:** medium
- **File:** `locallama_gui/ui/production_fixes.py`
- **Finding:** Source-tree lookup previously sent Plugin SDK documentation requests to `packaging/` instead of `docs/`.
- **Fix:** Source-tree resolver maps `PLUGIN_SDK.md` to `docs/`; frozen-package documentation remains under bundled `docs/`.
- **Validation:** Static inspection of source-tree and frozen resource paths.

### AUDIT-006 — Production packaging workflow asserted stale version
- **Status:** fixed
- **Severity:** high
- **File:** `.github/workflows/release-packaging.yml`
- **Finding:** Distribution validation hard-coded `1.2.9` while the canonical version had moved on.
- **Fix:** Workflow now derives `expected_version` from `pyproject.toml` and validates the built distribution against it.
- **Validation:** Workflow definition inspected after change; CI execution is the final validation.

### AUDIT-007 — Arch PKGBUILD was pinned to stale application version
- **Status:** fixed
- **Severity:** high
- **File:** `packaging/linux/PKGBUILD`
- **Finding:** `pkgver` was stale and therefore constructed the wrong release archive URL.
- **Fix:** Synchronized `pkgver` to `1.2.11`.
- **Validation:** Active package recipe now resolves its source URL from the canonical release version.

### AUDIT-008 — Linux man page reported stale application version
- **Status:** fixed
- **Severity:** medium
- **File:** `packaging/linux/myloai.1`
- **Finding:** `.TH` metadata reported an older release.
- **Fix:** Synchronized the man page to `1.2.11` and dated it `2026-09-24`.
- **Validation:** Active file inspection confirms the synchronized metadata.

### AUDIT-009 — Windows installer fallback version was stale
- **Status:** fixed
- **Severity:** low
- **File:** `packaging/windows/MyLoAI.iss`
- **Finding:** Direct Inno Setup invocation could fall back to an older version.
- **Fix:** Synchronized `MyLoAIVersion` fallback to `1.2.11`.
- **Validation:** Active installer script inspection confirms the fallback value.

### AUDIT-010 — Routine CI linted the archived tree
- **Status:** fixed
- **Severity:** medium
- **Files:** `.github/workflows/ci.yml`, `pyproject.toml`
- **Finding:** `ruff check .` could include `archive/**` even though routine validation policy excludes historical code.
- **Fix:** Added `archive/**` to Ruff's configured exclusion set in `pyproject.toml`. The existing `ruff check .` command therefore remains valid while respecting repository scope.
- **Validation:** Configuration and workflow paths inspected; CI execution remains the final validation.

## Existing documented bugs reviewed

### BUG-001 — Diagnostics appears in multiple menus
- **Status:** fixed
- **Verification:** Production startup applies `apply_production_fixes()` before the window is shown and removes the redundant Help/View actions.

### BUG-002 — Light theme makes prompt output text unreadable
- **Status:** fixed
- **Severity:** high
- **Verification:** `ChatTab.render()` now obtains the active Qt palette and applies palette base/text colors to message blocks. The renderer no longer couples chat output to the dark-only `#171a21` background.

### BUG-003 — Model Settings has no observable effect during initial GUI testing
- **Status:** fixed
- **Verification:** Current production path exposes `AI Model Settings...`, persists `config.parameters`, and generation consumes `to_backend_options()`.

### BUG-004 — Invalid import syntax in Ollama backend
- **Status:** fixed
- **Verification:** Active backend source contains valid future-import syntax.

### BUG-005 — Invalid import syntax in OpenAI-compatible backend
- **Status:** fixed
- **Verification:** Active backend source contains valid future-import syntax.

## Version synchronization

- **Current application version:** `1.2.11`.
- **Canonical source:** `pyproject.toml`.
- **Runtime source:** `locallama_gui/__init__.py` is synchronized to `1.2.11`.
- **Packaging references:** Arch PKGBUILD, Linux man page, Windows installer fallback, and `packaging/myloai-package.yaml` are synchronized to `1.2.11`.
- **Release workflow:** derives the expected Python distribution version from `pyproject.toml` rather than duplicating a release number.
- **Configuration schema:** remains independently versioned at `2`.

## Branch and scope

- Default branch: `main`.
- Production packaging changes are now represented on the merged default branch.
- `archive/**` remains excluded from routine validation and was not inspected as part of this active-code cleanup.

## Validation

- Read-only audit was performed before implementation changes.
- Reviewed `AGENTS.md`, `docs/VERSIONING.md`, `docs/BUGS/KNOWN_BUGS.md`, `pyproject.toml`, `CODE_AUDIT.md`, release CI, active theme/chat rendering, and platform packaging metadata.
- Applied the documented packaging/version/CI fixes and resolved the documented light-theme defect.
- Repository execution was not available through the GitHub file connector, so local Ruff/pytest/compileall results are not claimed here.
- GitHub Actions must provide the final automated validation of the resulting commit.

## Remaining issues

No previously documented open audit or known-bug items remain. Native GUI smoke testing for Dark and System/light themes and full CI validation remain required evidence for release confidence.

## Repository instructions

`AGENTS.md` requires minimal changes, version synchronization for implementation changes, changelog maintenance for implementation changes, and exclusion of `archive/**` from routine validation. `docs/VERSIONING.md` confirms `pyproject.toml` as the application version source and now documents the broader synchronization targets.
