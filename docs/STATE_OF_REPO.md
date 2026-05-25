# State of the Repo Audit

Date: 2026-05-25
Scope: Audit and synchronization report only (no refactor/moves/deletes/CI edits/version bump).

## Current Repository Structure

Top-level structure (apparent purpose):

- `.github/` — GitHub Actions workflows (`ci.yml`, `active-ci.yml`, `archive-lint.yml`).
- `locallama_gui/` — active PySide6 production package.
- `tests/` — active pytest suite for production package.
- `docs/` — project docs (currently partial).
- `archive/` — archive policy docs/manifests and archived legacy trees.
- `plugins/` — sample/development plugin(s) for active app.
- `archive/legacy_code/llm_studio/` — archived parallel/legacy experimental code tree.
- `archive/old_apps/ollama_GUI/` — archived legacy GUI trees (Python and Qt/QML variants).
- `pyproject.toml` — packaging, script entry point, Ruff config, version.
- `requirements.txt` — dependency list.
- `README.md` — user/developer high-level documentation.
- `CHANGELOG.md` — release history.
- `AGENTS.md` — contributor/agent operating rules.
- `CONTRIBUTING.md`, `FUNCTIONALITY_STATUS.md`, `HUMAN_REVIEW.md`, `SECURITY_REVIEW.md` — process/status docs.
- Generated/cache folders observed: `.git/` only at top-level (runtime caches likely under user config/data dirs at execution time).

App entry point candidates discovered:
- `locallama_gui/app.py`
- `locallama_gui/__main__.py`
- console script in `pyproject.toml`: `locallama-gui = locallama_gui.app:main`

## Active Production App Map

| File/Folder | Role | Used By | Confidence | Notes |
| ----------- | ---- | ------- | ---------- | ----- |
| `pyproject.toml` | Declares install/run entrypoint | launcher/CLI (`locallama-gui`) | HIGH | `[project.scripts]` points to `locallama_gui.app:main`. |
| `locallama_gui/app.py` | Runtime application bootstrap (`QApplication`, config, logging, `MainWindow`) | `locallama_gui.__main__`, console script | HIGH | Strongest active runtime entrypoint. |
| `locallama_gui/__main__.py` | `python -m locallama_gui` module entry | Python module launcher | HIGH | Delegates to `app.main()`. |
| `locallama_gui/ui/main_window.py` | Main window, menus, docks, most UI actions | `app.py` | HIGH | Central production UI surface. |
| `locallama_gui/ui/controllers/` | Chat/model/plugin action orchestration | `main_window.py` | HIGH | Active behavior routing layer. |
| `locallama_gui/ui/dialogs.py` | UI dialogs (parameters/plugins/agent builder/modelfile/etc.) | `main_window.py` | HIGH | Active modal workflows. |
| `locallama_gui/ui/workers.py` | Background async/stream tasks | `main_window.py`, controllers | HIGH | Non-blocking operations path. |
| `locallama_gui/backends/ollama.py` | Ollama backend implementation | backend manager/controllers | HIGH | Production Ollama integration. |
| `locallama_gui/backends/openai.py` | OpenAI-compatible backend | backend manager/controllers | HIGH | Active alternative provider path. |
| `locallama_gui/backends/manager.py` | Backend factory/selection | `main_window.py` via controllers | HIGH | Selects provider backend. |
| `locallama_gui/core/config.py` | Persistent settings, paths, parameters, provider profiles | `app.py`, controllers/ui | HIGH | Active config source. |
| `locallama_gui/core/managers.py` | session/prompt/agent/plugin managers | `main_window.py` | HIGH | Active persistence and feature logic. |
| `locallama_gui/core/domain.py` | Dataclasses/domain models | controllers/managers/ui | HIGH | Active data model definitions. |
| `locallama_gui/core/logging.py` | Logging setup | `app.py` | HIGH | Active logging bootstrap. |
| `locallama_gui/ui/theme.py` | Theme QSS generation | `main_window.py` | HIGH | Active styling path. |
| `plugins/sample_plugin.py` | Example plugin | plugin framework | MEDIUM | Optional sample; not auto-required for app boot. |
| `locallama_gui/plugins/__init__.py` | Package marker | import system | MEDIUM | Thin; core plugin logic is in `core/managers.py`. |
| assets/icons/resources inside active package | UI resources | main UI | LOW | No dedicated `resources/` tree found in active package; mostly code-defined UI. |

Verified active app identity conclusion:
- **Active production app = `locallama_gui` package**.
- **Entry point = `locallama_gui/app.py` (via console script and `python -m`).**
- The historical command `/usr/bin/python3 ~/my-ollama/locallama-gui/app.py` is **not** currently matched by repo layout (no top-level `app.py` present).

## Archive Candidates

| Original Path | Type | Reason It Appears Legacy/Unused | Evidence | Risk If Archived | Recommended Archive Path | Status |
| ------------- | ---- | ------------------------------- | -------- | ---------------- | ------------------------ | ------ |
| `ollama_GUI/ollama-gui-qt/` | legacy app | Legacy Qt/QML app not referenced by active package entrypoints | not in `project.scripts`; legacy desktop file naming | LOW-MEDIUM (historical value) | `archive/old_apps/ollama_GUI/ollama-gui-qt/` | SHOULD_ARCHIVE |
| `ollama_GUI/ollama-gui-py/` | legacy app | Older parallel Python GUI tree; not active runtime target | active runtime points to `locallama_gui` | MEDIUM | `archive/old_apps/ollama_GUI/ollama-gui-py/` | SHOULD_ARCHIVE |
| `ollama_GUI/addons/ollama_tools/test_tools_v4.py` | legacy tests/tools | Executes `sys.exit(1)` during pytest collection; breaks repo-wide pytest | observed pytest INTERNALERROR trace | LOW if archived with parent legacy tree | `archive/broken/ollama_GUI/addons/ollama_tools/test_tools_v4.py` | SHOULD_ARCHIVE |
| `llm_studio/CODEX_harvest_THESE_functions/` | experiment | Explicitly called out as experimental harvested code | archive index planned candidates | LOW-MEDIUM | `archive/experiments/llm_studio/CODEX_harvest_THESE_functions/` | SHOULD_ARCHIVE |
| `llm_studio/` (remainder) | parallel app/prototype | Appears parallel app ecosystem not used by active entrypoint | no active references from `locallama_gui` boot path | MEDIUM-HIGH (unknown utility) | `archive/legacy_code/llm_studio/` | NEEDS_HUMAN_REVIEW |
| `FUNCTIONALITY_STATUS.md` | doc | Potentially stale compared to current UI/changelog | not wired to current requested audit outputs | LOW | `archive/old_docs/FUNCTIONALITY_STATUS.md` | POSSIBLY_ARCHIVE |
| `HUMAN_REVIEW.md` | doc | Could be one-off process artifact | unclear ongoing workflow usage | MEDIUM | `archive/notes/HUMAN_REVIEW.md` | NEEDS_HUMAN_REVIEW |
| `SECURITY_REVIEW.md` | doc | Could be stale or still relevant | unknown freshness and owner intent | HIGH if archived incorrectly | `archive/old_docs/SECURITY_REVIEW.md` | NEEDS_HUMAN_REVIEW |
| `archive/manifests/duplicate_manifest.md` | archive metadata | Unknown if current/maintained | not referenced in primary docs except archive index note | LOW | keep in archive docs | DO_NOT_ARCHIVE |

## Archive State

| Item | Exists | Complete | Problems |
| ---- | ------ | -------- | -------- |
| `archive/` directory | Yes | Partial | Present but not yet used for full physical relocation of legacy trees. |
| archive subfolders per requested target taxonomy (`legacy_code`, `old_apps`, `old_docs`, `experiments`, `broken`, `duplicate`, `obsolete_ci`, `notes`) | No (as named) | No | Current archive naming in docs uses different labels (`old`, `experimental`, etc.), so taxonomy mismatch exists. |
| `archive/ARCHIVE_INDEX.md` | Yes | Partial | Contains governance + planned moves but no substantial completed move inventory. |
| Archive index coverage of archived files | Partial | No | Existing index references manifests and planned candidates, but no exhaustive mapping of all legacy trees. |
| CI excludes archive from production checks | Mixed | No | `ci.yml` runs repo-wide `ruff check .` and `pytest`; archive/legacy still affect pytest due to collection. |
| Docs explain archive purpose | Yes | Partial | `archive/README.md` exists, but practical archive execution appears incomplete. |

## CI and Tooling State

| Tool/Workflow | Config File | Command/Behavior | Archive Ignored | Legacy Ignored | Problems | Recommended Fix |
| ------------- | ----------- | ---------------- | --------------- | -------------- | -------- | --------------- |
| Main CI | `.github/workflows/ci.yml` | install dev deps; `ruff check .`; `pytest` across repo | No explicit pytest ignore | Ruff excludes some legacy via config | Pytest collects legacy tests; currently fails in `ollama_GUI/addons/.../test_tools_v4.py` due to `sys.exit(1)`. | Restrict pytest paths to active tests or configure ignore for legacy/archive trees. |
| Active CI | `.github/workflows/active-ci.yml` | compileall only for `locallama_gui` on path-filtered changes | N/A | Yes by path filter | Very limited signal (syntax only, no lint/tests). | Expand active workflow later to include targeted lint/tests on active package. |
| Archive lint | `.github/workflows/archive-lint.yml` | compileall on `llm_studio` and `ollama_GUI` when those paths change | N/A | N/A | Syntax-only; does not solve pytest collection conflicts in main CI. | Keep as archive syntax gate, but separate from production CI scope. |
| Ruff | `pyproject.toml` `[tool.ruff]` | `ruff check .`; `extend-exclude = ["llm_studio", "ollama_GUI"]` | Yes (implicitly if under excluded trees? archive not excluded explicitly) | Yes (`llm_studio`, `ollama_GUI`) | Ruff passes locally; archive not explicitly excluded. | Add explicit archive exclusions later for clarity/consistency. |
| Pytest | default discovery (no `pytest.ini`) | `pytest` from repo root | No | No | Discovers non-production tests/scripts in legacy trees. | Add `testpaths = tests` or equivalent ignore rules. |
| Pre-commit/tox/setup.cfg/Makefile configs | not present | N/A | N/A | N/A | Tooling surface incomplete for standardized local dev workflow. | Optional future: add minimal standardized dev commands. |

Current likely CI failure reason:
- **Primary drift**: CI test phase includes legacy path `ollama_GUI/addons/ollama_tools/test_tools_v4.py` that calls `sys.exit(1)` at import time, aborting pytest collection.

## Versioning State

| Location | Version Found | Should Be Source of Truth | In Sync | Notes |
| -------- | ------------- | ------------------------- | ------- | ----- |
| `pyproject.toml` | `1.0.12` | Yes (primary package metadata) | Yes | Packaging/source of release metadata. |
| `locallama_gui/__init__.py` | `1.0.12` | Secondary mirrored runtime constant | Yes | Matches `pyproject.toml`. |
| `CHANGELOG.md` latest heading | `1.0.12` | Release history source | Yes (number/date) | Contains duplicate `### Changed` blocks within 1.0.9 section (format quality issue). |
| `VERSION` file | Missing | Optional single-source file | N/A | No standalone `VERSION` file. |
| `setup.py` | Missing | Not needed if using pyproject-only packaging | N/A | Expected absence for modern PEP 621 layout. |
| `setup.cfg` | Missing | Optional | N/A | Not used currently. |
| README explicit numeric version | None | Not required but optional | N/A | README references semver policy, not current numeric tag. |
| GUI About/version display | Unknown/unverified | Should expose app version in UI | UNKNOWN | Need explicit UI audit pass to verify display. |
| `docs/VERSIONING.md` | Present | Recommended by AGENTS policy | Yes | Dedicated versioning policy document exists. |

Answers:
- Current version appears to be **1.0.12**.
- Main authoritative version locations (`pyproject`, `__init__`, changelog latest entry) are aligned on 1.0.12.
- A dedicated explicit version policy doc (`docs/VERSIONING.md`) is present.

## Changelog State

- `CHANGELOG.md` exists.
- Latest listed version: `1.0.12` (dated 2026-05-25).
- Latest version matches package metadata (`1.0.12`).
- Format mostly consistent but has structural quality issues (duplicate section headers under 1.0.9 and mixed chronology depth/detail).

| Expected Entry | Present | Notes |
| -------------- | ------- | ----- |
| AGENTS.md added | Partial | AGENTS updates are recorded in 1.0.9; initial add not clearly traceable as a dedicated entry. |
| functionality audit added | Partial | `docs/REPO_ANALYSIS.md` mentioned at 1.0.1, but no dedicated `FUNCTIONALITY_AUDIT.md`. |
| production cleanup planned | Partial | Archive plans are referenced, but no consolidated execution tracker doc. |
| archive changes | Partial | Governance/plans listed; substantial physical moves not recorded. |
| launcher scripts | No | No launcher script change entries found. |
| desktop entry scripts | No | No entry found. |
| CI archive exclusions | Partial | Mentions Ruff scope fixes; pytest legacy collection issue remains. |
| UI action repair | Partial | Several UI fixes recorded (1.0.7-1.0.9), but broader action audit doc absent. |
| parameter docs | No | No dedicated `docs/PARAMETERS.md`. |
| menu map | No | No dedicated `docs/MENU_MAP.md`. |
| bug fixes | Yes | Multiple bug-fix entries present. |

## Documentation State

| Document | Exists | Current/Stale/Missing | Purpose | Problems | Recommended Action |
| -------- | ------ | --------------------- | ------- | -------- | ------------------ |
| `README.md` | Yes | Current (partial) | User/developer overview + run instructions | Doesn’t include launcher/install integration docs requested in mission. | Expand after audit phase. |
| `AGENTS.md` | Yes | Current | Repository operating policy | Missing explicit desktop naming scheme + explicit CI-ignore-archive rule language. | Update policy in a follow-up governance patch. |
| `docs/STATE_OF_REPO.md` | Yes (this file) | Current | Full repo state audit | New baseline only; requires maintenance. | Keep as live status doc. |
| `docs/PRODUCTION_CODE_MAP.md` | Yes | Current | Canonical active code map | None identified in this RO pass. | Keep updated as code map evolves. |
| `docs/FUNCTIONALITY_AUDIT.md` | Yes | Current | Detailed feature status | None identified in this RO pass. | Keep synchronized with UI changes. |
| `docs/UI_ACTION_AUDIT.md` | Yes | Current | UI action integrity matrix | None identified in this RO pass. | Continue using as action integrity tracker. |
| `docs/QA_CHECKLIST.md` | Yes | Current | Validation process checklist | None identified in this RO pass. | Keep release checks aligned with reality. |
| `docs/MENU_MAP.md` | Yes | Current | Menu/action ownership map | None identified in this RO pass. | Keep aligned with `MainWindow` action wiring. |
| `docs/PARAMETERS.md` | Yes | Current | Parameter semantics and backend mapping | None identified in this RO pass. | Keep in sync with settings UI and backend behavior. |
| `docs/LAUNCHING.md` | No | Missing | launcher/desktop install/run guide | Missing. | Create in launcher phase. |
| `docs/VERSIONING.md` | Yes | Current | explicit versioning process | Version snapshot references required periodic refresh. | Updated in this RO pass. |
| `docs/ARCHITECTURE.md` | No | Missing | architecture reference | Missing (only `REPO_ANALYSIS.md` exists). | Add scoped architecture doc later. |
| `archive/ARCHIVE_INDEX.md` | Yes | Current (partial) | archival provenance tracking | Tracks plans more than completed moves. | Update during archive sweep. |

## Launcher and Desktop Integration State

| Item | Exists | Works/Unknown | Problems | Recommended Action |
| ---- | ------ | ------------- | -------- | ------------------ |
| `run-locallama` | No | Unknown | Missing launcher wrapper. | Add in Phase 4. |
| `scripts/install-launcher` | No | Unknown | Missing installer helper. | Add in Phase 4. |
| `scripts/install-desktop-entry` | No | Unknown | Missing desktop installer helper. | Add in Phase 4. |
| `packaging/linux/com.github.gr00t-user-706.locallama-gui.desktop` | No | Unknown | Missing desired desktop entry in active packaging path. | Add in Phase 4 with naming convention. |
| Legacy `.desktop` files under `ollama_GUI` | Yes | Legacy only | Wrong location/identity for active app and likely stale Exec paths. | Treat as archive/legacy artifacts. |
| README launch docs | Partial | Works for Python/package launch | No desktop integration/install path documentation. | Add `docs/LAUNCHING.md` + README links. |

## UI Functionality State

High-level audit based on code/test/docs (not full manual GUI runbook test in this task).

| Area | Known Problem | Evidence | Severity | Recommended Next Task |
| ---- | ------------- | -------- | -------- | --------------------- |
| Create Model dialog clarity | Ambiguity risk in user prompts/flows remains possible | Mission notes + no dedicated UI action audit doc | HIGH | Build `docs/UI_ACTION_AUDIT.md` then tighten copy/flow. |
| Agent Builder clarity | Possible ambiguity in expected behavior | Large dialog surface, no dedicated spec doc | MEDIUM | Document intended behaviors in `FUNCTIONALITY_AUDIT.md`. |
| View/Developer menu duplication risk | Complex menu surface in monolithic main window may duplicate actions | `main_window.py` centralizes many actions; no menu map doc | MEDIUM | Create `docs/MENU_MAP.md` and reconcile duplicates. |
| Debug terminal usefulness | Unknown practical utility; may be partially wired | Mentioned in mission + no dedicated QA artifact | MEDIUM | Audit each developer panel action with outcomes. |
| Font size/theme interaction | Historically sensitive area; possible reset regressions | Theme applied from config; no dedicated parameter/theme QA checklist | MEDIUM | Add regression checks in `QA_CHECKLIST.md`. |
| Model metadata table editability | Previously broken; now fixed | 1.0.9 changelog says made non-editable + tests added | LOW | Keep test coverage and verify in GUI smoke test. |
| Delete model reliability | Potentially broken/ambiguous per mission | Needs scenario validation against backend error handling | HIGH | Add explicit delete workflow validation cases. |
| Silent model crash/error handling | Risk of non-obvious errors | Mission concern + complex async paths | HIGH | Add explicit surfaced error checks in UI action audit. |
| Parameter clarity | Reasoning mode recently changed; user docs missing | changelog shows control changes but no `docs/PARAMETERS.md` | MEDIUM | Write parameter semantics doc before further UI changes. |
| Think/Plan/Normal exclusivity | Addressed in code but needs user-facing documentation consistency | changelog + config model shows `reasoning_mode` | LOW-MEDIUM | Document behavior and add UI QA steps. |
| Ambiguous windows/dialogs generally | No centralized UX contract | missing `UI_ACTION_AUDIT.md` | HIGH | Create action contract matrix and prune ambiguity. |

## AGENTS.md State

| Rule Area | Present | Missing/Weak | Recommended Update |
| --------- | ------- | ------------ | ------------------ |
| No rewrite-the-universe | Yes | — | Keep as-is. |
| Archive instead of delete | Yes | Archive taxonomy differs from requested current plan | Align taxonomy names or document alias mapping. |
| Version bumps required | Yes | — | Keep as-is. |
| Changelog updates required | Yes | — | Keep as-is. |
| Docs updates required | Yes | — | Keep as-is. |
| CI must ignore archive | Weak/implicit | Not explicitly mandated as a hard rule | Add explicit CI scoping rule for archive/legacy paths. |
| Launcher documentation | Weak/missing | No launcher/desktop naming/install standard | Add explicit launcher + desktop spec section. |
| Desktop naming scheme | Missing | Desired reverse-domain filename not codified | Add explicit required name/path policy. |
| No dead UI buttons | Yes (strong) | — | Keep and cross-link to UI action audit doc. |

## Drift Summary

What appears to have been expected but not actually completed:

- Archive governance docs were added, but **legacy trees were mostly not moved**.
- CI lint scoping improved for Ruff, but **pytest still scans legacy code and can fail for non-production reasons**.
- Version/changelog discipline exists, but **supporting docs promised by policy are still missing** (`VERSIONING`, QA/UI/menu/parameters docs).
- Active app is clearly `locallama_gui`, yet repository still contains multiple legacy app trees that create maintenance and CI confusion.
- Launcher/desktop integration for active app appears **not implemented** in the expected standardized form.
- UI action integrity policy is strong in AGENTS, but **no concrete UI action audit artifact exists** to enforce it.

Missing/stale pieces (high confidence):
- Missing: `docs/LAUNCHING.md`, `docs/ARCHITECTURE.md`.
- Pending archive moves: `ollama_GUI/*` (except maybe selected retained references), experimental `llm_studio` regions, with human review for any still-useful subsets.
- Pending CI fixes: pytest discovery scoping/ignores for legacy+archive trees.
- Pending launcher pieces: executable launcher + installers + canonical desktop file.
- Most likely broken/drift-prone behavior right now: delete-model UX clarity/reliability, ambiguous dialogs, developer/debug action usefulness, and unverified error surfacing in some async flows.

## Recovery Plan

### Phase 1: Repo Sync and Safety
- **Goal**: create missing audit/docs baselines; lock production map; define archive and versioning policy artifacts.
- **Likely files**: `docs/PRODUCTION_CODE_MAP.md`, `docs/FUNCTIONALITY_AUDIT.md`, `docs/UI_ACTION_AUDIT.md`, `docs/VERSIONING.md`, `docs/QA_CHECKLIST.md`, `docs/MENU_MAP.md`, `README.md` (links only), `CHANGELOG.md`.
- **Risk**: LOW.
- **Validation commands**:
  - `ruff check .`
  - `python -m compileall -q locallama_gui`
- **Version/changelog impact**: PATCH bump + changelog docs entries.

### Phase 2: Archive Sweep
- **Goal**: move confirmed legacy/unused paths into archive taxonomy; keep provenance.
- **Likely files/paths**: `archive/**`, `ollama_GUI/**`, `llm_studio/**`, `archive/ARCHIVE_INDEX.md`, `archive/manifests/*`, `README.md` (legacy path notes), `CHANGELOG.md`.
- **Risk**: MEDIUM (accidental breakage if active refs are missed).
- **Validation commands**:
  - `rg -n "ollama_GUI|llm_studio" locallama_gui tests pyproject.toml README.md`
  - `python -m compileall -q locallama_gui`
- **Version/changelog impact**: PATCH or MINOR depending user-visible behavior changes (likely PATCH if no features).

### Phase 3: CI Repair
- **Goal**: ensure CI checks active production by default and treats archive separately.
- **Likely files**: `.github/workflows/ci.yml`, `.github/workflows/active-ci.yml`, `.github/workflows/archive-lint.yml`, `pyproject.toml` (pytest config/testpaths), optionally `pytest.ini`.
- **Risk**: MEDIUM (false green if over-excluded).
- **Validation commands**:
  - `ruff check .`
  - `pytest`
  - `pytest tests`
- **Version/changelog impact**: PATCH.

### Phase 4: Launcher/Desktop Integration
- **Goal**: add canonical launch/install scripts and desktop file naming/paths.
- **Likely files**: `run-locallama`, `scripts/install-launcher`, `scripts/install-desktop-entry`, `packaging/linux/com.github.gr00t-user-706.locallama-gui.desktop`, `docs/LAUNCHING.md`, `README.md`, `CHANGELOG.md`.
- **Risk**: MEDIUM (platform path assumptions).
- **Validation commands**:
  - `bash -n run-locallama scripts/install-launcher scripts/install-desktop-entry`
  - manual dry-run options (no write) if implemented
- **Version/changelog impact**: MINOR if user-facing installer workflow added.

### Phase 5: UI Action Repair
- **Goal**: fix/disable ambiguous or dead actions; improve error signaling and dialog clarity.
- **Likely files**: `locallama_gui/ui/main_window.py`, `locallama_gui/ui/dialogs.py`, `locallama_gui/ui/controllers/*.py`, `tests/*ui*`, `docs/UI_ACTION_AUDIT.md`, `docs/PARAMETERS.md`, `docs/MENU_MAP.md`, `CHANGELOG.md`.
- **Risk**: MEDIUM-HIGH (UI regression surface).
- **Validation commands**:
  - `ruff check .`
  - `pytest tests`
  - `python -m compileall -q locallama_gui`
- **Version/changelog impact**: PATCH (fixes) or MINOR (significant UX additions).

### Phase 6: Production Polish
- **Goal**: release readiness, docs completeness, smoke-test discipline, packaging confidence.
- **Likely files**: `README.md`, `docs/ARCHITECTURE.md`, `docs/QA_CHECKLIST.md`, CI docs/workflows, packaging metadata, `CHANGELOG.md`.
- **Risk**: LOW-MEDIUM.
- **Validation commands**:
  - `ruff check .`
  - `pytest tests`
  - `python -m compileall -q locallama_gui`
- **Version/changelog impact**: PATCH for polish cycle.

