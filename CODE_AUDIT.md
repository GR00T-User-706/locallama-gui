# Active Code Audit

Date: 2026-09-22
Branch: feat/myloai-production-packaging
Scope: Active repository paths only. `archive/**` was excluded.

## Audit result

### AUDIT-003 — Syntax error in first-run setup wizard

- **Status:** open
- **Severity:** critical
- **File:** `locallama_gui/ui/setup_wizard.py`
- **Symbol:** `FirstRunWizard._check_backend()` / local callback `done`
- **Observed:** The callback declaration is `def done(status) -> None` without the required trailing colon.
- **Impact:** `locallama_gui.ui.setup_wizard` cannot be parsed/imported. This makes the first-run wizard unusable and can prevent packaging/import validation from completing when the module is collected.
- **Evidence:** Direct inspection of the active production-packaging branch. GitHub Actions run `35612497283` for commit `7e9c52add78267f3eb2f799529602c00c329ddda` failed in all Python matrix jobs during Ruff parsing with `invalid-syntax: Expected ':', found newline` at `locallama_gui/ui/setup_wizard.py:150:33`.
- **Recommended next investigation/fix:** Add only the missing `:` to the callback declaration, then run `ruff check .`, `pytest`, and active-package compile/import validation. No source change was made by this audit.

### AUDIT-004 — About dialog reports stale application version

- **Status:** open
- **Severity:** medium
- **File:** `locallama_gui/ui/production_fixes.py`
- **Symbol:** `_show_about`
- **Observed:** The About dialog hard-codes `Version 1.2.8`, while the active package metadata and module version are `1.2.9`.
- **Impact:** Users see an incorrect application version in the production UI. This also violates the repository's version synchronization requirement and can make support/debugging harder when users report the displayed version.
- **Evidence:** `pyproject.toml` declares `version = "1.2.9"`; `locallama_gui/__init__.py` declares `__version__ = "1.2.9"`; `locallama_gui/ui/production_fixes.py::_show_about()` displays `Version 1.2.8`.
- **Recommended next investigation/fix:** Replace the hard-coded About-dialog version with the canonical application version source or update the literal to the current version, then verify all version references remain synchronized. No source change was made by this audit.

### AUDIT-005 — Plugin SDK documentation action resolves the wrong source-tree path

- **Status:** open
- **Severity:** medium
- **File:** `locallama_gui/ui/production_fixes.py`
- **Symbols:** `_resource_path`, `_open_bundled_document`, `apply_production_fixes`
- **Observed:** In a non-frozen/source-tree run, `_resource_path()` resolves every requested document to `<repo>/packaging/<name>`. The production menu replaces the `Developer Mode` action with `_open_bundled_document(..., "PLUGIN_SDK.md")`, but the active file is `docs/PLUGIN_SDK.md`, not `packaging/PLUGIN_SDK.md`.
- **Impact:** The Developer Mode/Plugin SDK documentation action shows an "Unable to open bundled documentation" error when running from the source tree. The frozen PyInstaller path is different and bundles `docs/PLUGIN_SDK.md` correctly, so this is a source-mode packaging/path mismatch rather than a universal failure.
- **Evidence:** `locallama_gui/ui/production_fixes.py::_resource_path()` returns `Path(__file__).resolve().parents[2] / "packaging" / name` when not frozen. `apply_production_fixes()` invokes `_open_bundled_document(window, "Plugin SDK", "PLUGIN_SDK.md")`. The active repository contains `docs/PLUGIN_SDK.md`; there is no active `packaging/PLUGIN_SDK.md`. `packaging/pyinstaller/myloai.spec` separately bundles `docs/PLUGIN_SDK.md` into the frozen `docs` directory, confirming the source/frozen path mismatch.
- **Recommended next investigation/fix:** Make the non-frozen document lookup distinguish the packaging `USER_MANUAL.md` from the repository `docs/PLUGIN_SDK.md`, while preserving the existing frozen bundle layout. Validate the action in a source-tree launch and a frozen build. No source change was made by this audit.

## Previous audit history

### AUDIT-001 — Invalid Python import syntax in Ollama backend

- **Status:** fixed
- **Severity:** critical
- **File:** `locallama_gui/backends/ollama.py`
- **Observed:** The first import line was `rrom __ruture__ import annotations` instead of `from __future__ import annotations`.
- **Impact:** The module could not be parsed/imported by Python, so the Ollama backend was unusable and active-package compilation/import validation failed.
- **Evidence:** Direct inspection of the production-packaging branch at the time of the prior audit.
- **Minimal fix:** Correct the malformed import statement only.
- **Validation:** Run `python -m compileall -q locallama_gui` and the relevant backend tests after the change.

### AUDIT-002 — Invalid Python import syntax in OpenAI-compatible backend

- **Status:** fixed
- **Severity:** critical
- **File:** `locallama_gui/backends/openai.py`
- **Observed:** The first import line was `rrom __ruture__ import annotations` instead of `from __future__ import annotations`.
- **Impact:** The module could not be parsed/imported by Python, so the OpenAI-compatible backend was unusable and active-package compilation/import validation failed.
- **Evidence:** Direct inspection of the production-packaging branch at the time of the prior audit.
- **Minimal fix:** Correct the malformed import statement only.
- **Validation:** Run `python -m compileall -q locallama_gui` and the relevant backend tests after the change.

## Prior fix pass

- AUDIT-001 and AUDIT-002 were fixed with one-line import corrections.
- Application version was bumped from `1.2.8` to `1.2.9`.
- Required versioning, changelog, CI, and platform packaging version references were synchronized.
- GitHub connector access does not provide a way to execute the repository's test suite directly in the audit pass; validation remained pending CI.

## Existing documented findings reviewed

The existing `docs/BUGS/KNOWN_BUGS.md` was reviewed previously. BUG-001 through BUG-003 remain documented as open/investigating findings and were not changed because their entries explicitly require additional GUI/backend verification before making changes.

## Current validation notes

- The active production-packaging branch is `feat/myloai-production-packaging`, which is currently the repository's dedicated production distribution path and is the head branch of open PR #39.
- GitHub Actions run `35612497283` on commit `7e9c52add78267f3eb2f799529602c00c329ddda` failed in the Python 3.11, 3.12, and 3.13 CI jobs at the Ruff step because of AUDIT-003; tests were skipped as a consequence.
- No source code was modified during this audit.
- `archive/**` was excluded from the audit and was not used as evidence for any active-code finding.

## Repository instruction note

`AGENTS.md` was inspected before the audit. It requires minimal changes, active-path validation, synchronized versioning, changelog maintenance for completed changes, and explicit exclusion of `archive/**` from routine validation. The audit itself made only the requested audit-document update and did not implement any source fixes.
