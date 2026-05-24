# Repository Analysis

## Project Structure

This repository currently contains one active desktop application path plus two legacy code trees retained for reference.

| Path | Purpose | Current posture |
|---|---|---|
| `locallama_gui/` | Active PySide6 GUI app and supporting backend/core modules | Primary development target |
| `tests/` | Current pytest coverage focused on controller regressions | Minimal but active regression checks |
| `docs/` | Active docs for policies and SDK notes | Actively maintained documentation area |
| `plugins/` | Sample plugin and plugin development staging area | Active extension surface |
| `ollama_GUI/` | Legacy GUI/tooling trees (Py + Qt/QML) | Deprecated; historical reference |
| `llm_studio/` | Parallel/legacy app and harvested modules | Deprecated; historical reference |
| `archive/` | Explicit archive policy/manifests | Canonical archive guidance |

## Entry Points

Primary executable path for the supported app:

- `locallama_gui/__main__.py` → imports `main` from `locallama_gui/app.py` and exits via `SystemExit(main())`.
- `locallama_gui/app.py` → loads app config, initializes logging, creates `QApplication`, and shows `MainWindow`.
- CLI entry described in `README.md`: `locallama-gui` and `python -m locallama_gui`.

## Active GUI Path (`locallama_gui/`)

`locallama_gui/` is the only path described as production-supported in repository-level documentation. Core composition:

- `app.py`: runtime bootstrap and Qt app startup.
- `ui/`: main window, dialogs, workers, and controllers.
- `core/`: configuration, logging, domain models, and manager utilities.
- `backends/`: provider abstraction and concrete Ollama/OpenAI-compatible clients.

## Backend Integrations (`locallama_gui/backends/`)

Current integration shape is stable and intentionally small:

- `base.py`: common backend interface contract.
- `ollama.py`: Ollama implementation.
- `openai.py`: OpenAI-compatible implementation.
- `manager.py`: provider-type dispatch (`openai`/`llama.cpp` -> OpenAI-compatible backend; default -> Ollama backend).

This pattern is usable now, but extension pressure should be handled by explicit provider capability metadata before adding more special-case provider strings.

## Config / Settings Modules (`locallama_gui/core/config.py`)

`config.py` centralizes runtime settings and filesystem paths via dataclasses:

- `AppPaths` auto-creates config/data/log/session/prompt/agent/modelfile/plugin directories.
- `ProviderProfile`, `GenerationParameters`, and `UISettings` define typed settings structures.
- `AppConfig.load()` and `save()` persist JSON config under platformdirs config location.
- `active_profile()` provides active provider selection fallback behavior.

Strength: one clear source of truth for app settings.

Risk: JSON schema evolution is currently implicit (no explicit versioning/migration marker), so future config changes should include migration logic.

## Test Status (`tests/`)

Current tests are limited and controller-focused:

- `tests/test_controllers.py` validates chat send/regenerate flow, save flow, model create delegation, and plugin reload behavior using fakes.

Interpretation:

- Good for catching recent controller regressions.
- Not sufficient for end-to-end runtime confidence (UI event loop paths, backend HTTP interactions, plugin sandboxing, config migration).

## Archive Candidates (`ollama_GUI/`, `llm_studio/`)

Archive guidance already exists and marks both trees as deprecated. They should remain non-blocking historical artifacts unless explicitly re-adopted through a dedicated restoration plan.

---

## Classification Tables

### Usable as-is

| File/Path | Why it is usable now | Recommendation |
|---|---|---|
| `locallama_gui/__main__.py` | Clean, minimal module entrypoint forwarding to supported app bootstrap | Keep unchanged; only touch if startup contract changes |
| `locallama_gui/app.py` | Centralized Qt startup and app wiring with config/logging initialization | Keep as primary runtime bootstrap |
| `locallama_gui/backends/manager.py` | Explicit provider dispatch logic is readable and operationally clear | Keep; add tests when new providers are introduced |
| `locallama_gui/core/config.py` | Structured dataclass-based config and path provisioning already functional | Keep as canonical config module |
| `tests/test_controllers.py` | Active regression checks for core controller behaviors | Keep and grow incrementally |

### Needs repair

| File/Path | Technical reason | Recommended repair |
|---|---|---|
| `tests/` (overall) | Coverage scope is narrow and mostly unit-level fake-driven tests; lacks integration/E2E confidence | Add backend contract tests, config migration tests, and smoke UI startup tests |
| `locallama_gui/core/config.py` | Config persistence has no explicit schema version/migration path | Introduce `config_version`, migration map, and backward-compat load adapters |
| `locallama_gui/backends/manager.py` | Provider routing relies on string matching without capability validation | Add provider registry/capability model and defensive validation |

### Archive recommended

| File/Path | Technical reason | Recommended action |
|---|---|---|
| `ollama_GUI/` | Legacy parallel GUI/tool stack; not active support path; high drift risk vs `locallama_gui/` | Keep in archive-only mode; block new feature work there |
| `llm_studio/` | Deprecated alternate architecture with overlapping responsibilities and stale dependencies | Freeze and archive; only touch for extraction/migration tasks |
| `ollama_GUI/addons/ollama_tools/` | Tooling appears disconnected from active runtime path and support model | Move to explicit archive manifest entry if still needed for reference |

### Do not touch yet

| File/Path | Why to defer edits | Trigger to unlock |
|---|---|---|
| `ollama_GUI/ollama-gui-qt/` | Large legacy Qt/QML subtree likely to create accidental maintenance burden if modified ad hoc | Only modify under approved restoration project with dedicated test harness |
| `llm_studio/CODEX_harvest_THESE_functions/` | Harvest snapshot intent suggests reference extraction, not active execution path | Edit only when extracting specific validated modules into `locallama_gui/` |
| `archive/manifests/*` | Archive manifests should remain stable unless formal archive policy changes are approved | Update only during explicit archive governance changes |

---

## Recommended Phased Next Steps

### Phase 1 (Stabilize active path)

1. Expand `tests/` with:
   - backend manager/provider contract tests,
   - config load/save backward-compat tests,
   - smoke test for `AppConfig.load()` + `create_backend()` combinations.
2. Add config schema versioning in `locallama_gui/core/config.py`.
3. Document supported provider types and fallback behavior in docs.

### Phase 2 (Harden integration boundaries)

1. Introduce provider capability registry (streaming support, model listing support, auth requirements).
2. Add plugin loading trust/validation checks and explicit failure telemetry.
3. Add CI target for fast regression suite (`tests/test_controllers.py` + new config/backend tests).

### Phase 3 (Archive governance and extraction)

1. Freeze `ollama_GUI/` and `llm_studio/` with explicit read-only policy in docs.
2. Build a controlled extraction backlog: only migrate small, validated units from legacy trees into `locallama_gui/`.
3. Remove duplicate functionality after parity verification to reduce long-term drift.
