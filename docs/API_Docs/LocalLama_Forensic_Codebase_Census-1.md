# LocalLama Forensic Codebase Census

## Census identity
- Repository: `GR00T-User-706/locallama-gui`
- Branch inspected: `feat/myloai-production-packaging`
- HEAD: `5e2c520426386084d795779f3121a3a856d4459a`
- Comparison branch: `main`
- Main HEAD: `86e3ec01cc3e18e1c3d0ec41d22a95e2aa006154`
- Merge base: `e2f0d56ab3c4cde2e8ec291f45e60f940fedf55a`
- Git comparison: 116 commits ahead, 11 behind; diverged
- Scope: every tracked file outside `archive/`
- Mode: read-only
- Evidence classification: VERIFIED / PARTIALLY VERIFIED / UNVERIFIED / NOT PRESENT
- Important limitation: the GitHub connector supplied the complete recursive tree, but several large source blobs were returned as excerpts rather than complete text. Those files are listed and marked PARTIALLY VERIFIED instead of fabricating missing AST records.

## Executive index
- Tracked files outside `archive/`: **106**
- Total recorded bytes: **420,262**
- Python files: **44**
- Test files: **13**
- Packaging/build files under `packaging/`: **20**
- GitHub metadata/workflow files: **9**
- QML/C++/Qt-resource files outside `archive/`: **0 verified in the recursive tree**
- Binary assets outside `archive/`: no binary blob was listed by the recursive tree; SVG is text
- Files omitted from scope: every path beginning `archive/`

## 1. Complete tracked-file census

| # | Path | Type | Format | Bytes | Git mode | Tracked | Runtime | Build/Release | Tests | Config | Docs | Verification |
|---:|---|---|---|---:|---|---|---|---|---|---|---|---|
| 1 | `.github/ISSUE_TEMPLATE/bug_report.yml` | YAML | YAML | 1,125 | `100644` | YES | NO/UNVERIFIED | NO | NO | YES | NO | VERIFIED TREE |
| 2 | `.github/ISSUE_TEMPLATE/config.yml` | YAML | YAML | 418 | `100644` | YES | NO/UNVERIFIED | NO | NO | YES | NO | VERIFIED TREE |
| 3 | `.github/ISSUE_TEMPLATE/feature_request.yml` | YAML | YAML | 739 | `100644` | YES | NO/UNVERIFIED | NO | NO | YES | NO | VERIFIED TREE |
| 4 | `.github/agents/repo-code-risk-reviewer.agent.md` | Markdown | Markdown | 1,282 | `100644` | YES | NO/UNVERIFIED | NO | NO | YES | YES | VERIFIED TREE |
| 5 | `.github/prompts/repo-code-risk-reviewer.prompt.md` | Markdown | Markdown | 579 | `100644` | YES | NO/UNVERIFIED | NO | NO | YES | YES | VERIFIED TREE |
| 6 | `.github/workflows/active-ci.yml` | YAML | YAML | 676 | `100644` | YES | NO/UNVERIFIED | YES | NO | YES | NO | VERIFIED TREE |
| 7 | `.github/workflows/archive-lint.yml` | YAML | YAML | 377 | `100644` | YES | NO/UNVERIFIED | YES | NO | YES | NO | VERIFIED TREE |
| 8 | `.github/workflows/ci.yml` | YAML | YAML | 852 | `100644` | YES | NO/UNVERIFIED | YES | NO | YES | NO | VERIFIED TREE |
| 9 | `.github/workflows/release-packaging.yml` | YAML | YAML | 6,400 | `100644` | YES | NO/UNVERIFIED | YES | NO | YES | NO | VERIFIED TREE |
| 10 | `.gitignore` | gitignore | gitignore | 908 | `100644` | YES | NO/UNVERIFIED | NO | NO | YES | NO | VERIFIED TREE |
| 11 | `AGENTS.md` | Markdown | Markdown | 14,550 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 12 | `CHANGELOG.md` | Markdown | Markdown | 8,805 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 13 | `CODE_OF_CONDUCT.md` | Markdown | Markdown | 4,187 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 14 | `CONTRIBUTING.md` | Markdown | Markdown | 1,121 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 15 | `LICENSE` | license | license | 3,552 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 16 | `README.md` | Markdown | Markdown | 8,893 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 17 | `SECURITY.md` | Markdown | Markdown | 853 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 18 | `docs/ARCHITECTURE.md` | Markdown | Markdown | 9,898 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 19 | `docs/BUGS/KNOWN_BUGS.md` | Markdown | Markdown | 4,883 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 20 | `docs/CONFIG_SCHEMA.md` | Markdown | Markdown | 2,970 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 21 | `docs/FEATURE_MATRIX.md` | Markdown | Markdown | 15,519 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 22 | `docs/FUNCTIONALITY_AUDIT.md` | Markdown | Markdown | 2,639 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 23 | `docs/LAUNCHING.md` | Markdown | Markdown | 1,141 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 24 | `docs/MENU_MAP.md` | Markdown | Markdown | 1,678 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 25 | `docs/MODULE_INTAKE_POLICY.md` | Markdown | Markdown | 1,073 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 26 | `docs/PARAMETERS.md` | Markdown | Markdown | 1,469 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 27 | `docs/PLUGIN_SDK.md` | Markdown | Markdown | 2,700 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 28 | `docs/PRODUCTION_CODE_MAP.md` | Markdown | Markdown | 2,751 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 29 | `docs/QA_CHECKLIST.md` | Markdown | Markdown | 7,838 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 30 | `docs/REPO_ANALYSIS.md` | Markdown | Markdown | 3,566 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 31 | `docs/STATE_OF_REPO.md` | Markdown | Markdown | 24,036 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 32 | `docs/UI_ACTION_AUDIT.md` | Markdown | Markdown | 2,189 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 33 | `docs/VERSIONING.md` | Markdown | Markdown | 2,890 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 34 | `docs/deep-research-report-ollama.md` | Markdown | Markdown | 36,077 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 35 | `docs/deep-research-report.md` | Markdown | Markdown | 15,844 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 36 | `docs/qa/WINDOWS-VM-2026-09-09.md` | Markdown | Markdown | 3,152 | `100644` | YES | NO/UNVERIFIED | NO | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 37 | `locallama_gui/__init__.py` | Python | Python 3 | 112 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 38 | `locallama_gui/__main__.py` | Python | Python 3 | 92 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 39 | `locallama_gui/app.py` | Python | Python 3 | 1,480 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 40 | `locallama_gui/backends/__init__.py` | Python | Python 3 | 0 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 41 | `locallama_gui/backends/base.py` | Python | Python 3 | 1,783 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 42 | `locallama_gui/backends/manager.py` | Python | Python 3 | 620 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 43 | `locallama_gui/backends/ollama.py` | Python | Python 3 | 6,740 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 44 | `locallama_gui/backends/openai.py` | Python | Python 3 | 3,129 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 45 | `locallama_gui/core/__init__.py` | Python | Python 3 | 0 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 46 | `locallama_gui/core/config.py` | Python | Python 3 | 10,323 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 47 | `locallama_gui/core/domain.py` | Python | Python 3 | 3,321 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 48 | `locallama_gui/core/logging.py` | Python | Python 3 | 816 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 49 | `locallama_gui/core/managers.py` | Python | Python 3 | 11,465 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 50 | `locallama_gui/plugins/__init__.py` | Python | Python 3 | 0 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 51 | `locallama_gui/ui/__init__.py` | Python | Python 3 | 0 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 52 | `locallama_gui/ui/chat_view.py` | Python | Python 3 | 1,758 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 53 | `locallama_gui/ui/controllers/__init__.py` | Python | Python 3 | 207 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 54 | `locallama_gui/ui/controllers/chat_controller.py` | Python | Python 3 | 3,991 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 55 | `locallama_gui/ui/controllers/model_controller.py` | Python | Python 3 | 5,025 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 56 | `locallama_gui/ui/controllers/plugin_controller.py` | Python | Python 3 | 897 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 57 | `locallama_gui/ui/diagnostics.py` | Python | Python 3 | 4,413 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 58 | `locallama_gui/ui/dialogs.py` | Python | Python 3 | 22,055 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 59 | `locallama_gui/ui/main_window.py` | Python | Python 3 | 41,757 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 60 | `locallama_gui/ui/model_browser.py` | Python | Python 3 | 4,805 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 61 | `locallama_gui/ui/production_fixes.py` | Python | Python 3 | 6,778 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 62 | `locallama_gui/ui/setup_wizard.py` | Python | Python 3 | 7,831 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 63 | `locallama_gui/ui/theme.py` | Python | Python 3 | 1,063 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 64 | `locallama_gui/ui/workers.py` | Python | Python 3 | 1,508 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 65 | `packaging/README.md` | Markdown | Markdown | 1,311 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 66 | `packaging/RELEASE_BUILD_SPEC.md` | Markdown | Markdown | 1,951 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 67 | `packaging/RELEASE_PAYLOAD.md` | Markdown | Markdown | 1,202 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 68 | `packaging/USER_MANUAL.md` | Markdown | Markdown | 3,095 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 69 | `packaging/assets/generate_myloai_icon.py` | Python | Python 3 | 1,646 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 70 | `packaging/check-release-payload.py` | Python | Python 3 | 1,394 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 71 | `packaging/linux/PKGBUILD` | other | other | 1,293 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 72 | `packaging/linux/appimage/README.md` | Markdown | Markdown | 463 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 73 | `packaging/linux/appimage/build-appimage.sh` | script | script | 1,748 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 74 | `packaging/linux/appimage/myloai.svg` | SVG | SVG | 1,504 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 75 | `packaging/linux/com.github.gr00t-user-706.locallama-gui.desktop` | desktop-entry | desktop-entry | 211 | `100644` | YES | NO/UNVERIFIED | YES | NO | YES | NO | VERIFIED TREE |
| 76 | `packaging/linux/debian/README.Debian` | other | other | 763 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 77 | `packaging/linux/debian/build-deb.sh` | script | script | 2,299 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 78 | `packaging/linux/install-myloai.sh` | script | script | 620 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 79 | `packaging/linux/myloai` | other | other | 54 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 80 | `packaging/linux/myloai.1` | man-page | man-page | 1,017 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 81 | `packaging/linux/myloai.desktop` | desktop-entry | desktop-entry | 231 | `100644` | YES | NO/UNVERIFIED | YES | NO | YES | NO | VERIFIED TREE |
| 82 | `packaging/macos/README.md` | Markdown | Markdown | 620 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 83 | `packaging/macos/build-dmg.sh` | script | script | 952 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 84 | `packaging/pyinstaller/myloai.spec` | PyInstaller spec | PyInstaller spec | 1,919 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 85 | `packaging/windows/MyLoAI.iss` | Inno Setup | Inno Setup | 1,649 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 86 | `packaging/windows/README.md` | Markdown | Markdown | 592 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | YES | VERIFIED TREE |
| 87 | `packaging/windows/build-installer.ps1` | script | script | 1,861 | `100644` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 88 | `plugins/sample_plugin.py` | Python | Python 3 | 1,220 | `100644` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 89 | `pyproject.toml` | TOML | TOML | 1,029 | `100644` | YES | NO/UNVERIFIED | YES | NO | YES | NO | VERIFIED TREE |
| 90 | `requirements.txt` | requirements/text | requirements/text | 109 | `100644` | YES | NO/UNVERIFIED | YES | NO | YES | NO | VERIFIED TREE |
| 91 | `run-locallama` | script | script | 392 | `100755` | YES | YES | NO | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 92 | `scripts/install-desktop-entry` | other | other | 1,176 | `100755` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 93 | `scripts/install-launcher` | other | other | 676 | `100755` | YES | NO/UNVERIFIED | YES | NO | NO/UNVERIFIED | NO | VERIFIED TREE |
| 94 | `tests/test_backend_and_config.py` | Python | Python 3 | 3,035 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 95 | `tests/test_chat_view.py` | Python | Python 3 | 1,842 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 96 | `tests/test_config_roundtrip.py` | Python | Python 3 | 4,040 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 97 | `tests/test_config_schema.py` | Python | Python 3 | 1,831 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 98 | `tests/test_controller_invalid_flows.py` | Python | Python 3 | 2,754 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 99 | `tests/test_controllers.py` | Python | Python 3 | 4,765 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 100 | `tests/test_diagnostics.py` | Python | Python 3 | 3,158 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 101 | `tests/test_model_controller_delete.py` | Python | Python 3 | 2,901 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 102 | `tests/test_model_metadata_table_flags.py` | Python | Python 3 | 395 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 103 | `tests/test_model_operations.py` | Python | Python 3 | 10,905 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 104 | `tests/test_ollama_backend.py` | Python | Python 3 | 6,224 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 105 | `tests/test_plugin_lifecycle.py` | Python | Python 3 | 2,730 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |
| 106 | `tests/test_security_boundaries.py` | Python | Python 3 | 3,086 | `100644` | YES | NO/UNVERIFIED | NO | YES | NO/UNVERIFIED | NO | VERIFIED TREE |

### File-census reconciliation
- Recursive Git tree entries outside `archive/`: 106 blobs.
- Recursive tree reported `truncated: false`.
- Every row above was taken from the repository tree at the feature HEAD, not from README claims.
- Line counts are not asserted for files whose complete text was not retrieved. Their byte sizes and Git modes are verified from the Git tree.
- Git executable bit is verified as `100755` for `run-locallama`, `scripts/install-launcher`, and `scripts/install-desktop-entry`; the listed packaging shell files are `100644` in the tree.

## 2. Python module census

### `locallama_gui/__init__.py`
- Importable-name candidate: `locallama_gui`
- Size: 112 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/__main__.py`
- Importable-name candidate: `locallama_gui.__main__`
- Size: 92 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/app.py`
- Importable-name candidate: `locallama_gui.app`
- Size: 1,480 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `os`
  - `sys`
  - `pathlib.Path`
  - `platformdirs.user_config_dir`
  - `PySide6.QtCore.Qt`
  - `PySide6.QtWidgets.QApplication`
  - `locallama_gui.core.config.APP_NAME`
  - `locallama_gui.core.config.AppConfig`
  - `locallama_gui.core.logging.configure_logging`
  - `locallama_gui.ui.main_window.MainWindow`
  - `locallama_gui.ui.production_fixes.apply_production_fixes`
- functions:
  - `main() -> int`
- classes:
- constants:
- dynamic:
  - `sys.path.insert(...) when __package__ in {None,''}`
- env:
  - `QT_ENABLE_HIGHDPI_SCALING`
  - `QT_AUTO_SCREEN_SCALE_FACTOR`
- side_effects:
  - `sets Qt env defaults`
  - `may replace MainWindow.refresh_backend with lambda`
  - `creates QApplication`
  - `calls apply_production_fixes`
  - `calls app.exec()`

### `locallama_gui/backends/__init__.py`
- Importable-name candidate: `locallama_gui.backends`
- Size: 0 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/backends/base.py`
- Importable-name candidate: `locallama_gui.backends.base`
- Size: 1,783 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `abc.ABC`
  - `abc.abstractmethod`
  - `collections.abc.AsyncIterator`
  - `dataclasses.dataclass`
  - `typing.Any`
  - `ChatMessage`
  - `ModelInfo`
- classes:
  - `BackendStatus`
  - `LLMBackend`
- functions:
  - `LLMBackend.__init__`
  - `LLMBackend.test_connection [abstract async]`
  - `LLMBackend.list_models [abstract async]`
  - `LLMBackend.chat [abstract async]`
  - `LLMBackend.pull_model`
  - `push_model`
  - `delete_model`
  - `copy_model`
  - `create_model`
  - `show_model`
- fields:
  - `BackendStatus`: ['state', 'latency_ms', 'detail']
- abc:
  - `LLMBackend`

### `locallama_gui/backends/manager.py`
- Importable-name candidate: `locallama_gui.backends.manager`
- Size: 620 bytes
- Source status: VERIFIED
- imports:
  - `LLMBackend`
  - `OllamaBackend`
  - `OpenAICompatibleBackend`
  - `ProviderProfile`
- functions:
  - `create_backend`
- factory:
  - `provider_type == 'openai' -> OpenAICompatibleBackend`
  - `provider_type == 'llama.cpp' -> OpenAICompatibleBackend`
  - `otherwise -> OllamaBackend`

### `locallama_gui/backends/ollama.py`
- Importable-name candidate: `locallama_gui.backends.ollama`
- Size: 6,740 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `json`
  - `time`
  - `AsyncIterator`
  - `Any`
  - `ClassVar`
  - `httpx`
  - `BackendStatus`
  - `LLMBackend`
  - `ChatMessage`
  - `ModelInfo`
- classes:
  - `OllamaBackend`
- functions:
  - `sanitize_options [classmethod]`
  - `sanitize_request_fields [staticmethod]`
  - `build_chat_payload [classmethod]`
  - `test_connection [async]`
  - `list_models [async]`
  - `chat [async generator]`
  - `pull_model [async generator]`
  - `push_model [async generator]`
  - `delete_model [async]`
  - `copy_model [async]`
  - `create_model [async generator]`
  - `show_model [async]`
  - `_stream_endpoint [async generator]`
- constants:
  - `name`: ollama
  - `SUPPORTED_OPTIONS`: ['temperature', 'top_k', 'top_p', 'min_p', 'repeat_penalty', 'repeat_last_n', 'num_predict', 'seed', 'stop', 'num_ctx', 'num_batch', 'num_gpu', 'num_keep', 'typical_p', 'presence_penalty', 'frequency_penalty', 'main_gpu', 'use_mmap', 'num_thread']
- endpoints:
  - `GET /api/tags`
  - `POST /api/chat`
  - `POST /api/pull`
  - `POST /api/push`
  - `DELETE /api/delete`
  - `POST /api/copy`
  - `POST /api/create`
  - `POST /api/show`
- timeouts:
  - `5`
  - `15`
  - `30`
  - `None`

### `locallama_gui/backends/openai.py`
- Importable-name candidate: `locallama_gui.backends.openai`
- Size: 3,129 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `json`
  - `time`
  - `AsyncIterator`
  - `Any`
  - `httpx`
  - `BackendStatus`
  - `LLMBackend`
  - `ChatMessage`
  - `ModelInfo`
- classes:
  - `OpenAICompatibleBackend`
- functions:
  - `_headers`
  - `test_connection [async]`
  - `list_models [async]`
  - `chat [async generator]`
- constants:
  - `name`: openai
  - `headers`: Content-Type: application/json; Authorization: Bearer <api_key> when configured
- endpoints:
  - `GET /models`
  - `POST /chat/completions`
- timeouts:
  - `5`
  - `15`
  - `None`

### `locallama_gui/core/__init__.py`
- Importable-name candidate: `locallama_gui.core`
- Size: 0 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/core/config.py`
- Importable-name candidate: `locallama_gui.core.config`
- Size: 10,323 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `json`
  - `dataclasses.asdict`
  - `dataclasses.dataclass`
  - `dataclasses.field`
  - `pathlib.Path`
  - `typing.Any`
  - `keyring`
  - `keyring.errors.KeyringError`
  - `keyring.errors.PasswordDeleteError`
  - `platformdirs.user_config_dir`
  - `platformdirs.user_data_dir`
  - `platformdirs.user_log_dir`
- classes:
  - `CredentialStore`
  - `AppPaths`
  - `ProviderProfile`
  - `GenerationParameters`
  - `UISettings`
  - `AppConfig`
- functions:
  - `AppPaths.create`
  - `CredentialStore._username`
  - `CredentialStore.get`
  - `CredentialStore.set`
  - `GenerationParameters.__post_init__`
  - `GenerationParameters.to_backend_options`
  - `AppConfig.file_path [property]`
  - `AppConfig._migrate_data`
  - `AppConfig.load`
  - `AppConfig.save`
  - `AppConfig.active_profile`
- fields:
  - `AppPaths`: ['config_dir', 'data_dir', 'logs_dir', 'sessions_dir', 'prompts_dir', 'agents_dir', 'modelfiles_dir', 'plugins_dir']
  - `ProviderProfile`: ['name', 'provider_type', 'base_url', 'api_key', 'default_model', 'enabled']
  - `GenerationParameters`: ['temperature', 'top_k', 'top_p', 'min_p', 'repeat_penalty', 'repeat_last_n', 'mirostat', 'mirostat_eta', 'mirostat_tau', 'tfs_z', 'num_predict', 'seed', 'stop', 'num_ctx', 'num_batch', 'num_gpu', 'reasoning_mode', 'thinking_mode', 'plan_mode', 'normal_mode']
  - `UISettings`: ['theme', 'geometry_hex', 'state_hex', 'active_session_id', 'font_size']
  - `AppConfig`: ['paths', 'schema_version', 'provider_profiles', 'active_provider', 'parameters', 'parameter_presets', 'enabled_plugins', 'trusted_plugins', 'developer_mode', 'ui', 'global_system_prompt']
- constants:
  - `APP_NAME`: locallama-gui
  - `CONFIG_SCHEMA_VERSION`: 2
  - `APP_SYSTEM_PROMPT`: multiline string
- paths:
  - `config.json`
  - `sessions`
  - `prompts`
  - `agents`
  - `modelfiles`
  - `plugins`
- persistence:
  - `JSON config read/write`
  - `OS keyring credential read/write/delete`
  - `chmod(0600)`

### `locallama_gui/core/domain.py`
- Importable-name candidate: `locallama_gui.core.domain`
- Size: 3,321 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `json`
  - `uuid`
  - `dataclasses.asdict`
  - `dataclasses.dataclass`
  - `dataclasses.field`
  - `datetime.UTC`
  - `datetime.datetime`
  - `pathlib.Path`
  - `typing.Any`
  - `typing.Literal`
- classes:
  - `ChatMessage`
  - `ChatSession`
  - `ModelInfo`
  - `PromptRecord`
  - `AgentProfile`
  - `ScrollRestorePlan is not here`
- functions:
  - `now_iso`
  - `ChatSession.touch`
  - `ChatSession.to_json`
  - `ChatSession.from_file [classmethod]`
  - `ChatSession.save`
  - `ChatSession.export_markdown`
  - `ChatSession.export_text`
  - `ModelInfo.size_display [property]`
- constants:
  - `Role`: Literal['system','user','assistant','tool']
- fields:
  - `ChatMessage`: ['role', 'content', 'id', 'created_at', 'name', 'metadata']
  - `ChatSession`: ['title', 'id', 'created_at', 'updated_at', 'provider', 'model', 'system_prompt', 'messages', 'parameters']
  - `ModelInfo`: ['name', 'size', 'parameter_size', 'quantization', 'context_size', 'backend', 'metadata']
  - `PromptRecord`: ['title', 'content', 'category', 'favorite', 'id', 'versions', 'updated_at']
  - `AgentProfile`: ['name', 'model', 'system_prompt_id', 'tools', 'plugins', 'memory_mode', 'reasoning_mode', 'behavior', 'execution_policy', 'id']

### `locallama_gui/core/logging.py`
- Importable-name candidate: `locallama_gui.core.logging`
- Size: 816 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/core/managers.py`
- Importable-name candidate: `locallama_gui.core.managers`
- Size: 11,465 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `ast`
  - `importlib.util`
  - `json`
  - `shutil`
  - `dataclasses.asdict`
  - `pathlib.Path`
  - `types.ModuleType`
  - `typing.Any`
  - `typing.Protocol`
  - `AppConfig`
  - `AgentProfile`
  - `ChatSession`
  - `PromptRecord`
  - `now_iso`
- classes:
  - `SessionManager`
  - `PromptManager`
  - `AgentManager`
  - `PluginAPI [Protocol]`
  - `PluginContext`
  - `LoadedPlugin`
  - `PluginManager`
- methods:
  - `SessionManager.__init__`
  - `list_sessions`
  - `load`
  - `save`
  - `import_session`
  - `PromptManager.__init__`
  - `list`
  - `save_all`
  - `upsert`
  - `delete`
  - `import_file`
  - `export`
  - `AgentManager.__init__`
  - `list`
  - `save_all`
  - `upsert`
  - `PluginAPI.activate`
  - `PluginAPI.deactivate`
  - `PluginContext.__init__`
  - `register_tool`
  - `register_command`
  - `register_chat_interceptor`
  - `add_panel`
  - `LoadedPlugin.__init__`
  - `PluginManager.__init__`
  - `_validate_manifest`
  - `_read_static_manifest`
  - `plugin_paths`
  - `discover`
  - `load_enabled`
  - `trust`
  - `untrust`
  - `enable`
  - `disable`
  - `reload`
  - `remove`
  - `_load_module`
- instance_state:
  - `SessionManager`: ['config']
  - `PromptManager`: ['config', 'path']
  - `AgentManager`: ['config', 'path']
  - `PluginContext`: ['main_window', 'config', 'tools', 'commands', 'chat_interceptors', 'memory_providers']
  - `LoadedPlugin`: ['path', 'module', 'instance', 'manifest']
  - `PluginManager`: ['config', 'context', 'loaded']
- plugin_hooks:
  - `register_tool`
  - `register_command`
  - `register_chat_interceptor`
  - `add_panel`
- dynamic_import:
  - `importlib.util.spec_from_file_location`
- security:
  - `static AST manifest parse before execution`
  - `trusted_plugins gate`
  - `runtime manifest validation`
  - `runtime ID match`

### `locallama_gui/plugins/__init__.py`
- Importable-name candidate: `locallama_gui.plugins`
- Size: 0 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/ui/__init__.py`
- Importable-name candidate: `locallama_gui.ui`
- Size: 0 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/ui/chat_view.py`
- Importable-name candidate: `locallama_gui.ui.chat_view`
- Size: 1,758 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `dataclasses.dataclass`
  - `ChatMessage`
- classes:
  - `ScrollRestorePlan [@dataclass(frozen=True)]`
- functions:
  - `compute_scroll_restore_plan`
  - `message_is_internal_system`
  - `visible_chat_messages`
  - `assistant_label`
  - `redacted_request_messages`
- constants:
  - `INTERNAL_PROMPT_REDACTION`: [redacted app system prompt]

### `locallama_gui/ui/controllers/__init__.py`
- Importable-name candidate: `locallama_gui.ui.controllers`
- Size: 207 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/ui/controllers/chat_controller.py`
- Importable-name candidate: `locallama_gui.ui.controllers.chat_controller`
- Size: 3,991 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `pathlib.Path`
  - `typing.Protocol`
  - `ChatMessage`
  - `ChatSession`
  - `message_is_internal_system`
- classes:
  - `ChatWindowPort [Protocol]`
  - `ChatController`
- methods:
  - `ChatWindowPort.current_tab`
  - `set_tab_title`
  - `render_tab`
  - `generate_for_tab`
  - `refresh_sessions`
  - `log`
  - `open_session`
  - `ChatController.__init__`
  - `save_current`
  - `open_chat_file`
  - `send_message`
  - `regenerate`
  - `retry`
  - `copy_last_message`
  - `edit_message`
  - `delete_message`
- dynamic_imports:
  - `PySide6.QtWidgets.QFileDialog`
  - `QApplication`
  - `QInputDialog`

### `locallama_gui/ui/controllers/model_controller.py`
- Importable-name candidate: `locallama_gui.ui.controllers.model_controller`
- Size: 5,025 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `typing.Protocol`
  - `create_backend`
  - `OperationStreamParser`
  - `StreamTask`
- classes:
  - `ModelWindowPort [Protocol]`
  - `ModelController`
- methods:
  - `ModelWindowPort.model_name`
  - `begin_operation`
  - `update_operation`
  - `complete_operation`
  - `fail_operation`
  - `refresh_backend`
  - `add_worker`
  - `run_async`
  - `open_modelfile_editor`
  - `ModelController.__init__`
  - `pull_model`
  - `push_model`
  - `create_model`
  - `clone_model`
  - `delete_model`
  - `_model_stream_op`
- dynamic_imports:
  - `PySide6.QtWidgets.QInputDialog`
  - `QMessageBox`
- closures:
  - `_model_stream_op.on_stream`
  - `_model_stream_op.on_completed`
  - `_model_stream_op.on_error`

### `locallama_gui/ui/controllers/plugin_controller.py`
- Importable-name candidate: `locallama_gui.ui.controllers.plugin_controller`
- Size: 897 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `pathlib.Path`
  - `typing.Protocol`
- classes:
  - `PluginWindowPort [Protocol]`
  - `PluginController`
- methods:
  - `PluginWindowPort.log`
  - `PluginController.__init__`
  - `reload_plugins`
  - `install_plugin`
- dynamic_imports:
  - `PySide6.QtWidgets.QFileDialog`

### `locallama_gui/ui/diagnostics.py`
- Importable-name candidate: `locallama_gui.ui.diagnostics`
- Size: 4,413 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `json`
  - `logging`
  - `dataclasses.dataclass`
  - `typing.TextIO`
  - `QObject`
  - `Signal`
  - `QTextCursor`
  - `QPlainTextEdit`
- classes:
  - `DiagnosticsSignals`
  - `QtLogHandler`
  - `LineBufferedStream`
  - `OperationUpdate [@dataclass(frozen=True)]`
  - `OperationStreamParser`
- functions:
  - `append_output`
  - `_integer_or_none`
- signals:
  - `DiagnosticsSignals.log_line: Signal(str)`
  - `DiagnosticsSignals.console_text: Signal(str)`

### `locallama_gui/ui/dialogs.py`
- Importable-name candidate: `locallama_gui.ui.dialogs`
- Size: 22,055 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/ui/main_window.py`
- Importable-name candidate: `locallama_gui.ui.main_window`
- Size: 41,757 bytes
- Source status: PARTIALLY_VERIFIED: source is 41,757 bytes; connector returned multiple excerpts rather than complete source text
- classes:
  - `ChatTab(QWidget)`
  - `ComposerTextEdit(QPlainTextEdit)`
  - `MainWindow(QMainWindow)`
- functions:
  - `_build_readonly_table_item`
- signals:
  - `ComposerTextEdit.send_requested`
  - `ComposerTextEdit.zoom_requested`
- verified_methods:
  - `ChatTab.__init__`
  - `ChatTab.render`
  - `ChatTab.set_generating`
  - `ComposerTextEdit.keyPressEvent`
  - `ComposerTextEdit.wheelEvent`
  - `MainWindow.__init__`
  - `_build_ui`
  - `_create_docks`
  - `_dock`
  - `add_plugin_panel`
  - `_menu_action`
  - `_build_menus`
  - `_build_file_menu`
  - `_build_models_menu`
  - `_build_agents_menu`
  - `_build_plugins_menu`
  - `_build_settings_menu`
  - `_build_view_menu`
  - `_build_developer_menu`
  - `_build_help_menu`
  - `current_tab`
  - `new_chat`
  - `_wire_chat_tab`
  - `close_tab`
  - `_generate`
  - `_append_token`
  - `_stream_error`
  - `_stream_done`
  - `stop_generation`
  - `model_changed`
  - `refresh_backend`
  - `_show_dock`
  - `show_diagnostics_dock`
  - `_show_diagnostics_tab`
  - `show_logs_dock`
  - `show_console_dock`
  - `show_operations_dock`
  - `show_request_dock`
  - `show_token_dock`
  - `_backend_refresh_error`
  - `_backend_refreshed`
  - `_update_backend_status`
  - `_refresh_model_combo`
  - `_refresh_model_table`
  - `_insert_model_table_row`
  - `switch_provider`
  - `refresh_sessions`
  - `refresh_prompts`
  - `apply_prompt_item`
  - `save_as`
  - `open_session`
  - `import_chat`
  - `export_current`
  - `_async`
  - `run_async`
  - `set_tab_title`
  - `render_tab`
  - `generate_for_tab`
  - `model_name`
  - `_install_diagnostics_sinks`
  - `append_log`
  - `append_console`
  - `append_operation_history`
  - `begin_operation`
  - `update_operation`
  - `complete_operation`
  - `fail_operation`
  - `add_worker`
  - `open_modelfile_editor`
  - `build_model_from_modelfile`
  - `open_template_viewer`
  - `_show_text_dialog`
  - `open_endpoints`
  - `open_parameters`
  - `edit_default_system_prompt`
  - `open_plugins`
  - `open_plugin_docs`
  - `open_agent_builder`
  - `import_agent`
  - `export_agent`
  - `toggle_theme`
  - `show_shortcuts`
  - `adjust_font_size`
  - `toggle_all_docks`
  - `reset_layout`
  - `inspect_api`
  - `_open_document`
  - `open_docs`
  - `about`
  - `diagnostics`
  - `log`
  - `_restore_state`
  - `closeEvent`
- verified_state:
  - `config`
  - `sessions`
  - `prompts`
  - `agents`
  - `plugin_context`
  - `plugins`
  - `models`
  - `chat_controller`
  - `model_controller`
  - `plugin_controller`
  - `worker_refs`
  - `current_stream`
  - `_stream_owner_seq`
  - `_active_stream_owner`
  - `_diagnostics_signals`
  - `_diagnostics_log_handler`
  - `_original_stdout`
  - `_original_stderr`
  - `tabs`
  - `status`
  - `provider_combo`
  - `model_combo`
  - `model_table`
  - `sessions_list`
  - `prompt_list`
  - `log_view`
  - `console_view`
  - `operation_status`
  - `operation_progress`
  - `operation_history`
  - `diagnostics_tabs`
  - `diagnostics_dock`
  - `request_view`
  - `request_copy`
  - `request_clear`
  - `request_dock`
  - `token_view`
  - `token_copy`
  - `token_clear`
  - `token_dock`
- verified_flow: `_generate builds APP_SYSTEM_PROMPT message, appends session messages, applies plugin chat_interceptors, translates generation options, builds/redacts request preview, creates assistant message, creates StreamTask, connects token/error/completed callbacks, starts task.`
- end_cleanup: `closeEvent restores stdout/stderr, removes Qt log handler, cancels active workers, saves geometry/state and config.`

### `locallama_gui/ui/model_browser.py`
- Importable-name candidate: `locallama_gui.ui.model_browser`
- Size: 4,805 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/ui/production_fixes.py`
- Importable-name candidate: `locallama_gui.ui.production_fixes`
- Size: 6,778 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/ui/setup_wizard.py`
- Importable-name candidate: `locallama_gui.ui.setup_wizard`
- Size: 7,831 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/ui/theme.py`
- Importable-name candidate: `locallama_gui.ui.theme`
- Size: 1,063 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `locallama_gui/ui/workers.py`
- Importable-name candidate: `locallama_gui.ui.workers`
- Size: 1,508 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `asyncio`
  - `AsyncIterator`
  - `Callable`
  - `Any`
  - `QObject`
  - `QThread`
  - `Signal`
- classes:
  - `AsyncTask(QThread)`
  - `StreamTask(QThread)`
- signals:
  - `AsyncTask.result(object)`
  - `AsyncTask.error(str)`
  - `AsyncTask.finished_ok()`
  - `StreamTask.token(str)`
  - `StreamTask.error(str)`
  - `StreamTask.completed(str)`
- methods:
  - `AsyncTask.__init__`
  - `AsyncTask.run`
  - `StreamTask.__init__`
  - `StreamTask.cancel`
  - `StreamTask.run`
- state:
  - `AsyncTask.coro_factory`
  - `StreamTask.iterator_factory`
  - `StreamTask._cancelled`
  - `StreamTask.full_text`

### `packaging/assets/generate_myloai_icon.py`
- Importable-name candidate: `packaging.assets.generate_myloai_icon`
- Size: 1,646 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `pathlib.Path`
  - `PIL.Image`
  - `PIL.ImageDraw`
- constants:
  - `ROOT`
  - `ICO`
  - `PNG`
  - `SIZE=1024`
- module_execution:
  - `creates image`
  - `writes PNG`
  - `writes ICO`
- unverified:
  - `exact source line locations not captured in this session`

### `packaging/check-release-payload.py`
- Importable-name candidate: `packaging.check-release-payload`
- Size: 1,394 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `argparse`
  - `pathlib.Path`
- constants:
  - `EXCLUDED_TOP_LEVEL={.github,archive,tests}`
  - `EXCLUDED_FILES={AGENTS.md,CONTRIBUTING.md,CODE_OF_CONDUCT.md}`
  - `EXCLUDED_NAME_PARTS={.pyc,.pyo}`
- functions:
  - `validate(root)`
  - `main()`
- cli: `python packaging/check-release-payload.py <staging_dir>`

### `plugins/sample_plugin.py`
- Importable-name candidate: `plugins.sample_plugin`
- Size: 1,220 bytes
- Source status: VERIFIED
- imports:
  - `__future__.annotations`
  - `typing.ClassVar`
  - `QLabel`
  - `QTextEdit`
  - `QVBoxLayout`
  - `QWidget`
- classes:
  - `Plugin`
- methods:
  - `__init__`
  - `activate`
  - `deactivate`
  - `add_metadata`
- constants:
  - `Plugin.manifest`: {'id': 'sample_plugin', 'name': 'Sample Productivity Plugin', 'version': '1.0.0', 'description': 'Adds a command, a chat interceptor, a tool, and a custom dock panel.'}
- state:
  - `_active`
- hooks:
  - `register_tool('uppercase', lambda text: str(text).upper())`
  - `register_command('insert_timestamp', lambda: context.main_window.terminal.appendPlainText(...))`
  - `register_chat_interceptor(add_metadata)`
  - `add_panel('Sample Plugin', panel)`

### `tests/test_backend_and_config.py`
- Importable-name candidate: `tests.test_backend_and_config`
- Size: 3,035 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_chat_view.py`
- Importable-name candidate: `tests.test_chat_view`
- Size: 1,842 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_config_roundtrip.py`
- Importable-name candidate: `tests.test_config_roundtrip`
- Size: 4,040 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_config_schema.py`
- Importable-name candidate: `tests.test_config_schema`
- Size: 1,831 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_controller_invalid_flows.py`
- Importable-name candidate: `tests.test_controller_invalid_flows`
- Size: 2,754 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_controllers.py`
- Importable-name candidate: `tests.test_controllers`
- Size: 4,765 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_diagnostics.py`
- Importable-name candidate: `tests.test_diagnostics`
- Size: 3,158 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_model_controller_delete.py`
- Importable-name candidate: `tests.test_model_controller_delete`
- Size: 2,901 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_model_metadata_table_flags.py`
- Importable-name candidate: `tests.test_model_metadata_table_flags`
- Size: 395 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_model_operations.py`
- Importable-name candidate: `tests.test_model_operations`
- Size: 10,905 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_ollama_backend.py`
- Importable-name candidate: `tests.test_ollama_backend`
- Size: 6,224 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_plugin_lifecycle.py`
- Importable-name candidate: `tests.test_plugin_lifecycle`
- Size: 2,730 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

### `tests/test_security_boundaries.py`
- Importable-name candidate: `tests.test_security_boundaries`
- Size: 3,086 bytes
- Source status: UNVERIFIED: complete blob text was not retrieved in this census session.
- AST symbols: UNVERIFIED.
- Exact source locations: UNVERIFIED.

## 3. Import census

### `locallama_gui/app.py`
- `__future__.annotations`
- `os`
- `sys`
- `pathlib.Path`
- `platformdirs.user_config_dir`
- `PySide6.QtCore.Qt`
- `PySide6.QtWidgets.QApplication`
- `locallama_gui.core.config.APP_NAME`
- `locallama_gui.core.config.AppConfig`
- `locallama_gui.core.logging.configure_logging`
- `locallama_gui.ui.main_window.MainWindow`
- `locallama_gui.ui.production_fixes.apply_production_fixes`

### `locallama_gui/core/config.py`
- `__future__.annotations`
- `json`
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `pathlib.Path`
- `typing.Any`
- `keyring`
- `keyring.errors.KeyringError`
- `keyring.errors.PasswordDeleteError`
- `platformdirs.user_config_dir`
- `platformdirs.user_data_dir`
- `platformdirs.user_log_dir`

### `locallama_gui/core/domain.py`
- `__future__.annotations`
- `json`
- `uuid`
- `dataclasses.asdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.UTC`
- `datetime.datetime`
- `pathlib.Path`
- `typing.Any`
- `typing.Literal`

### `locallama_gui/backends/base.py`
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `collections.abc.AsyncIterator`
- `dataclasses.dataclass`
- `typing.Any`
- `ChatMessage`
- `ModelInfo`

### `locallama_gui/backends/manager.py`
- `LLMBackend`
- `OllamaBackend`
- `OpenAICompatibleBackend`
- `ProviderProfile`

### `locallama_gui/backends/ollama.py`
- `__future__.annotations`
- `json`
- `time`
- `AsyncIterator`
- `Any`
- `ClassVar`
- `httpx`
- `BackendStatus`
- `LLMBackend`
- `ChatMessage`
- `ModelInfo`

### `locallama_gui/backends/openai.py`
- `__future__.annotations`
- `json`
- `time`
- `AsyncIterator`
- `Any`
- `httpx`
- `BackendStatus`
- `LLMBackend`
- `ChatMessage`
- `ModelInfo`

### `locallama_gui/ui/chat_view.py`
- `__future__.annotations`
- `dataclasses.dataclass`
- `ChatMessage`

### `locallama_gui/ui/controllers/chat_controller.py`
- `__future__.annotations`
- `pathlib.Path`
- `typing.Protocol`
- `ChatMessage`
- `ChatSession`
- `message_is_internal_system`
- Dynamic imports:
  - `PySide6.QtWidgets.QFileDialog`
  - `QApplication`
  - `QInputDialog`

### `locallama_gui/ui/controllers/model_controller.py`
- `__future__.annotations`
- `typing.Protocol`
- `create_backend`
- `OperationStreamParser`
- `StreamTask`
- Dynamic imports:
  - `PySide6.QtWidgets.QInputDialog`
  - `QMessageBox`

### `locallama_gui/ui/controllers/plugin_controller.py`
- `__future__.annotations`
- `pathlib.Path`
- `typing.Protocol`
- Dynamic imports:
  - `PySide6.QtWidgets.QFileDialog`

### `locallama_gui/ui/diagnostics.py`
- `__future__.annotations`
- `json`
- `logging`
- `dataclasses.dataclass`
- `typing.TextIO`
- `QObject`
- `Signal`
- `QTextCursor`
- `QPlainTextEdit`

### `locallama_gui/ui/workers.py`
- `__future__.annotations`
- `asyncio`
- `AsyncIterator`
- `Callable`
- `Any`
- `QObject`
- `QThread`
- `Signal`

### `plugins/sample_plugin.py`
- `__future__.annotations`
- `typing.ClassVar`
- `QLabel`
- `QTextEdit`
- `QVBoxLayout`
- `QWidget`

### `packaging/assets/generate_myloai_icon.py`
- `__future__.annotations`
- `pathlib.Path`
- `PIL.Image`
- `PIL.ImageDraw`

### `packaging/check-release-payload.py`
- `__future__.annotations`
- `argparse`
- `pathlib.Path`

### `locallama_gui/core/managers.py`
- `__future__.annotations`
- `ast`
- `importlib.util`
- `json`
- `shutil`
- `dataclasses.asdict`
- `pathlib.Path`
- `types.ModuleType`
- `typing.Any`
- `typing.Protocol`
- `AppConfig`
- `AgentProfile`
- `ChatSession`
- `PromptRecord`
- `now_iso`

## 4. Class / Protocol / ABC census

### `locallama_gui/core/config.py`
- `CredentialStore`
- `AppPaths`
- `ProviderProfile`
- `GenerationParameters`
- `UISettings`
- `AppConfig`

### `locallama_gui/core/domain.py`
- `ChatMessage`
- `ChatSession`
- `ModelInfo`
- `PromptRecord`
- `AgentProfile`
- `ScrollRestorePlan is not here`

### `locallama_gui/backends/base.py`
- `BackendStatus`
- `LLMBackend`
- ABC: `LLMBackend`

### `locallama_gui/backends/ollama.py`
- `OllamaBackend`

### `locallama_gui/backends/openai.py`
- `OpenAICompatibleBackend`

### `locallama_gui/ui/chat_view.py`
- `ScrollRestorePlan [@dataclass(frozen=True)]`

### `locallama_gui/ui/controllers/chat_controller.py`
- `ChatWindowPort [Protocol]`
- `ChatController`

### `locallama_gui/ui/controllers/model_controller.py`
- `ModelWindowPort [Protocol]`
- `ModelController`

### `locallama_gui/ui/controllers/plugin_controller.py`
- `PluginWindowPort [Protocol]`
- `PluginController`

### `locallama_gui/ui/diagnostics.py`
- `DiagnosticsSignals`
- `QtLogHandler`
- `LineBufferedStream`
- `OperationUpdate [@dataclass(frozen=True)]`
- `OperationStreamParser`

### `locallama_gui/ui/workers.py`
- `AsyncTask(QThread)`
- `StreamTask(QThread)`

### `plugins/sample_plugin.py`
- `Plugin`

### `locallama_gui/core/managers.py`
- `SessionManager`
- `PromptManager`
- `AgentManager`
- `PluginAPI [Protocol]`
- `PluginContext`
- `LoadedPlugin`
- `PluginManager`

### `locallama_gui/ui/main_window.py`
- `ChatTab(QWidget)`
- `ComposerTextEdit(QPlainTextEdit)`
- `MainWindow(QMainWindow)`

## 5. Function / method census

### `locallama_gui/app.py`
- `main() -> int`

### `locallama_gui/core/config.py`
- `AppPaths.create`
- `CredentialStore._username`
- `CredentialStore.get`
- `CredentialStore.set`
- `GenerationParameters.__post_init__`
- `GenerationParameters.to_backend_options`
- `AppConfig.file_path [property]`
- `AppConfig._migrate_data`
- `AppConfig.load`
- `AppConfig.save`
- `AppConfig.active_profile`

### `locallama_gui/core/domain.py`
- `now_iso`
- `ChatSession.touch`
- `ChatSession.to_json`
- `ChatSession.from_file [classmethod]`
- `ChatSession.save`
- `ChatSession.export_markdown`
- `ChatSession.export_text`
- `ModelInfo.size_display [property]`

### `locallama_gui/backends/base.py`
- `LLMBackend.__init__`
- `LLMBackend.test_connection [abstract async]`
- `LLMBackend.list_models [abstract async]`
- `LLMBackend.chat [abstract async]`
- `LLMBackend.pull_model`
- `push_model`
- `delete_model`
- `copy_model`
- `create_model`
- `show_model`

### `locallama_gui/backends/manager.py`
- `create_backend`

### `locallama_gui/backends/ollama.py`
- `sanitize_options [classmethod]`
- `sanitize_request_fields [staticmethod]`
- `build_chat_payload [classmethod]`
- `test_connection [async]`
- `list_models [async]`
- `chat [async generator]`
- `pull_model [async generator]`
- `push_model [async generator]`
- `delete_model [async]`
- `copy_model [async]`
- `create_model [async generator]`
- `show_model [async]`
- `_stream_endpoint [async generator]`

### `locallama_gui/backends/openai.py`
- `_headers`
- `test_connection [async]`
- `list_models [async]`
- `chat [async generator]`

### `locallama_gui/ui/chat_view.py`
- `compute_scroll_restore_plan`
- `message_is_internal_system`
- `visible_chat_messages`
- `assistant_label`
- `redacted_request_messages`

### `locallama_gui/ui/controllers/chat_controller.py`
- `ChatWindowPort.current_tab`
- `set_tab_title`
- `render_tab`
- `generate_for_tab`
- `refresh_sessions`
- `log`
- `open_session`
- `ChatController.__init__`
- `save_current`
- `open_chat_file`
- `send_message`
- `regenerate`
- `retry`
- `copy_last_message`
- `edit_message`
- `delete_message`

### `locallama_gui/ui/controllers/model_controller.py`
- `ModelWindowPort.model_name`
- `begin_operation`
- `update_operation`
- `complete_operation`
- `fail_operation`
- `refresh_backend`
- `add_worker`
- `run_async`
- `open_modelfile_editor`
- `ModelController.__init__`
- `pull_model`
- `push_model`
- `create_model`
- `clone_model`
- `delete_model`
- `_model_stream_op`

### `locallama_gui/ui/controllers/plugin_controller.py`
- `PluginWindowPort.log`
- `PluginController.__init__`
- `reload_plugins`
- `install_plugin`

### `locallama_gui/ui/diagnostics.py`
- `append_output`
- `_integer_or_none`

### `locallama_gui/ui/workers.py`
- `AsyncTask.__init__`
- `AsyncTask.run`
- `StreamTask.__init__`
- `StreamTask.cancel`
- `StreamTask.run`

### `plugins/sample_plugin.py`
- `__init__`
- `activate`
- `deactivate`
- `add_metadata`

### `packaging/check-release-payload.py`
- `validate(root)`
- `main()`

### `locallama_gui/core/managers.py`
- `SessionManager.__init__`
- `list_sessions`
- `load`
- `save`
- `import_session`
- `PromptManager.__init__`
- `list`
- `save_all`
- `upsert`
- `delete`
- `import_file`
- `export`
- `AgentManager.__init__`
- `list`
- `save_all`
- `upsert`
- `PluginAPI.activate`
- `PluginAPI.deactivate`
- `PluginContext.__init__`
- `register_tool`
- `register_command`
- `register_chat_interceptor`
- `add_panel`
- `LoadedPlugin.__init__`
- `PluginManager.__init__`
- `_validate_manifest`
- `_read_static_manifest`
- `plugin_paths`
- `discover`
- `load_enabled`
- `trust`
- `untrust`
- `enable`
- `disable`
- `reload`
- `remove`
- `_load_module`

### `locallama_gui/ui/main_window.py`
- `_build_readonly_table_item`

## 6. Dataclass / structured-data census

| Type | Module | Fields / structure |
|---|---|---|
| `ChatMessage` | `locallama_gui.core.domain` | role, content, id, created_at, name, metadata |
| `ChatSession` | `locallama_gui.core.domain` | title, id, created_at, updated_at, provider, model, system_prompt, messages, parameters |
| `ModelInfo` | `locallama_gui.core.domain` | name, size, parameter_size, quantization, context_size, backend, metadata |
| `PromptRecord` | `locallama_gui.core.domain` | title, content, category, favorite, id, versions, updated_at |
| `AgentProfile` | `locallama_gui.core.domain` | name, model, system_prompt_id, tools, plugins, memory_mode, reasoning_mode, behavior, execution_policy, id |
| `AppPaths` | `locallama_gui.core.config` | config_dir, data_dir, logs_dir, sessions_dir, prompts_dir, agents_dir, modelfiles_dir, plugins_dir |
| `ProviderProfile` | `locallama_gui.core.config` | name, provider_type, base_url, api_key, default_model, enabled |
| `GenerationParameters` | `locallama_gui.core.config` | temperature, top_k, top_p, min_p, repeat_penalty, repeat_last_n, mirostat, mirostat_eta, mirostat_tau, tfs_z, num_predict, seed, stop, num_ctx, num_batch, num_gpu, reasoning_mode, thinking_mode, plan_mode, normal_mode |
| `UISettings` | `locallama_gui.core.config` | theme, geometry_hex, state_hex, active_session_id, font_size |
| `AppConfig` | `locallama_gui.core.config` | paths, schema_version, provider_profiles, active_provider, parameters, parameter_presets, enabled_plugins, trusted_plugins, developer_mode, ui, global_system_prompt |
| `BackendStatus` | `locallama_gui.backends.base` | state, latency_ms, detail |
| `ScrollRestorePlan` | `locallama_gui.ui.chat_view` | should_pin_bottom, previous_value |
| `OperationUpdate` | `locallama_gui.ui.diagnostics` | status, history_text, completed, total |
| `ModelRecommendation` | `locallama_gui.ui.model_browser` | source module not fully retrieved; UNVERIFIED in this session |

## 7. Constants / literal contracts

| Constant/contract | Location | Value / form |
|---|---|---|
| `APP_NAME` | `core/config.py` | `locallama-gui` |
| `CONFIG_SCHEMA_VERSION` | `core/config.py` | `2` |
| `APP_SYSTEM_PROMPT` | `core/config.py` | LocalLama application system prompt |
| `Role` | `core/domain.py` | `Literal['system','user','assistant','tool']` |
| `INTERNAL_PROMPT_REDACTION` | `ui/chat_view.py` | `[redacted app system prompt]` |
| `OllamaBackend.name` | `backends/ollama.py` | `ollama` |
| `OllamaBackend.SUPPORTED_OPTIONS` | `backends/ollama.py` | 19 option names |
| `OpenAICompatibleBackend.name` | `backends/openai.py` | `openai` |
| `QT_ENABLE_HIGHDPI_SCALING` | `app.py` | default `1` |
| `QT_AUTO_SCREEN_SCALE_FACTOR` | `app.py` | default `1` |
| Ollama default URL | `core/config.py` | `http://localhost:11434` |
| Ollama tags | `backends/ollama.py` | `GET /api/tags` |
| Ollama chat | `backends/ollama.py` | `POST /api/chat` |
| Ollama pull | `backends/ollama.py` | `POST /api/pull` |
| Ollama push | `backends/ollama.py` | `POST /api/push` |
| Ollama delete | `backends/ollama.py` | `DELETE /api/delete` |
| Ollama copy | `backends/ollama.py` | `POST /api/copy` |
| Ollama create | `backends/ollama.py` | `POST /api/create` |
| Ollama show | `backends/ollama.py` | `POST /api/show` |
| OpenAI models | `backends/openai.py` | `GET /models` |
| OpenAI chat | `backends/openai.py` | `POST /chat/completions` |
| plugin ID | `plugins/sample_plugin.py` | `sample_plugin` |
| plugin command | `plugins/sample_plugin.py` | `insert_timestamp` |
| plugin tool | `plugins/sample_plugin.py` | `uppercase` |

## 8. Instance-state census
### `locallama_gui/ui/workers.py`
- `AsyncTask.coro_factory`
- `StreamTask.iterator_factory`
- `StreamTask._cancelled`
- `StreamTask.full_text`

### `plugins/sample_plugin.py`
- `_active`

### `locallama_gui/core/managers.py`
- `SessionManager`: `config`
- `PromptManager`: `config`, `path`
- `AgentManager`: `config`, `path`
- `PluginContext`: `main_window`, `config`, `tools`, `commands`, `chat_interceptors`, `memory_providers`
- `LoadedPlugin`: `path`, `module`, `instance`, `manifest`
- `PluginManager`: `config`, `context`, `loaded`

### `locallama_gui/ui/main_window.py`
- MainWindow `config`
- MainWindow `sessions`
- MainWindow `prompts`
- MainWindow `agents`
- MainWindow `plugin_context`
- MainWindow `plugins`
- MainWindow `models`
- MainWindow `chat_controller`
- MainWindow `model_controller`
- MainWindow `plugin_controller`
- MainWindow `worker_refs`
- MainWindow `current_stream`
- MainWindow `_stream_owner_seq`
- MainWindow `_active_stream_owner`
- MainWindow `_diagnostics_signals`
- MainWindow `_diagnostics_log_handler`
- MainWindow `_original_stdout`
- MainWindow `_original_stderr`
- MainWindow `tabs`
- MainWindow `status`
- MainWindow `provider_combo`
- MainWindow `model_combo`
- MainWindow `model_table`
- MainWindow `sessions_list`
- MainWindow `prompt_list`
- MainWindow `log_view`
- MainWindow `console_view`
- MainWindow `operation_status`
- MainWindow `operation_progress`
- MainWindow `operation_history`
- MainWindow `diagnostics_tabs`
- MainWindow `diagnostics_dock`
- MainWindow `request_view`
- MainWindow `request_copy`
- MainWindow `request_clear`
- MainWindow `request_dock`
- MainWindow `token_view`
- MainWindow `token_copy`
- MainWindow `token_clear`
- MainWindow `token_dock`

## 9. Environment-variable census
- `QT_ENABLE_HIGHDPI_SCALING`: read/write via `os.environ.setdefault` in `locallama_gui/app.py`.
- `QT_AUTO_SCREEN_SCALE_FACTOR`: read/write via `os.environ.setdefault` in `locallama_gui/app.py`.
- Shell launcher scripts use process `PATH` through `command -v`.
- Shell installation scripts use `HOME`.
- No other application environment-variable access was verified in the fully retrieved Python source.
- Additional references in partially/unretrieved files: UNVERIFIED.

## 10. Filesystem census
| Path / construction | Operation | Owner/source |
|---|---|---|
| `platformdirs.user_config_dir(APP_NAME, 'LocalLama')` | create/read config directory | `AppPaths.create`, `app.main` |
| `platformdirs.user_data_dir(APP_NAME, 'LocalLama')` | create data directory | `AppPaths.create` |
| `platformdirs.user_log_dir(APP_NAME, 'LocalLama')` | create log directory | `AppPaths.create` |
| `<data>/sessions/*.json` | enumerate/read/write | `SessionManager`, `ChatSession` |
| `<data>/prompts/prompts.json` | read/write/copy | `PromptManager` |
| `<data>/agents/agents.json` | read/write | `AgentManager` |
| `<data>/modelfiles` | read/write/versioning | dialogs/modelfile editor |
| `<data>/plugins/*.py` | discover/load/delete | `PluginManager` |
| `<config>/config.json` | read/write/chmod 0600 | `AppConfig` |
| `README.md` | read | `MainWindow.open_docs` |
| `docs/PLUGIN_SDK.md` | read | `MainWindow.open_plugin_docs` |
| `<HOME>/.local/bin/run-locallama` | install target | `scripts/install-launcher` |
| `<HOME>/.local/share/applications/com.github.gr00t-user-706.locallama-gui.desktop` | install target | `scripts/install-desktop-entry` |

## 11. HTTP/API census
### Ollama
- Base URL default: `http://localhost:11434`.
- `GET /api/tags`: connection test and model listing.
- `POST /api/chat`: streaming and non-streaming chat.
- `POST /api/pull`: streamed model pull.
- `POST /api/push`: streamed model push.
- `DELETE /api/delete`: model deletion.
- `POST /api/copy`: model clone.
- `POST /api/create`: model creation from modelfile.
- `POST /api/show`: model metadata/template.
- Streaming response parser: newline JSON via `aiter_lines()`.
- Request option filter: `SUPPORTED_OPTIONS`; `think` is separately copied to request fields.
### OpenAI-compatible
- Base URL is profile-controlled.
- `GET /models`: connection/model listing.
- `POST /chat/completions`: streaming/non-streaming chat.
- Optional `Authorization: Bearer <api_key>`.
- Streaming parser accepts `data: ` lines and `[DONE]`.

## 12. CLI / entry-point census
| Entry point | Target | Verified |
|---|---|---|
| `locallama-gui` | `locallama_gui.app:main` | VERIFIED from feature `pyproject.toml` |
| `myloai` | `locallama_gui.app:main` | VERIFIED from feature `pyproject.toml` |
| `python -m locallama_gui` | `locallama_gui.__main__` -> `app.main` | VERIFIED |
| `./run-locallama` | `locallama-gui` then `python3 -m locallama_gui` then `python -m locallama_gui` | VERIFIED |
| `packaging/check-release-payload.py <staging_dir>` | `main()` | VERIFIED |
| `scripts/install-launcher [--dry-run]` | launcher installation | VERIFIED |
| `scripts/install-desktop-entry [--dry-run]` | desktop entry installation | VERIFIED |

## 13. Qt architecture census
- Verified custom Qt classes: `ChatTab(QWidget)`, `ComposerTextEdit(QPlainTextEdit)`, `MainWindow(QMainWindow)`, `DiagnosticsSignals(QObject)`, `QtLogHandler(logging.Handler)`, `AsyncTask(QThread)`, `StreamTask(QThread)`.
- `ComposerTextEdit.send_requested: Signal()`.
- `ComposerTextEdit.zoom_requested: Signal(int)`.
- `DiagnosticsSignals.log_line: Signal(str)`.
- `DiagnosticsSignals.console_text: Signal(str)`.
- `AsyncTask.result: Signal(object)`.
- `AsyncTask.error: Signal(str)`.
- `AsyncTask.finished_ok: Signal()`.
- `StreamTask.token: Signal(str)`.
- `StreamTask.error: Signal(str)`.
- `StreamTask.completed: Signal(str)`.
- MainWindow chat-tab wiring connects send/input/zoom/stop/regenerate/retry/copy/edit/delete actions.
- Stream wiring connects token/error/completed to generation callbacks.
- Exact connection inventory in `main_window.py` beyond the retrieved excerpts is PARTIALLY VERIFIED.

## 14. Worker/concurrency census
- `AsyncTask(QThread)` owns a coroutine factory and executes it with `asyncio.run` inside `run()`.
- `AsyncTask` emits `result` and `finished_ok`, or `error`.
- `StreamTask(QThread)` owns an async iterator factory, `_cancelled`, and `full_text`.
- `StreamTask.cancel()` sets `_cancelled=True`.
- `StreamTask.run()` consumes the iterator and emits each token.
- `MainWindow.worker_refs` retains task objects.
- MainWindow tracks chat-stream ownership with `_stream_owner_seq` and `_active_stream_owner`.
- `closeEvent` cancels active workers that expose `isRunning()` and `cancel()`.
- No multiprocessing boundary was verified in the retrieved active source.

## 15. Plugin census
- Static discovery uses AST parsing of `Plugin.manifest` before execution.
- Required manifest keys: `id`, `name`, `version`.
- Trust state: `AppConfig.trusted_plugins`.
- Enable state: `AppConfig.enabled_plugins`.
- Load path: `importlib.util.spec_from_file_location` -> module creation -> `exec_module` -> `Plugin()`.
- Runtime manifest is revalidated and runtime ID must equal static discovery ID.
- Lifecycle: `activate(context)` and `deactivate()`.
- Context registries: `tools`, `commands`, `chat_interceptors`, `memory_providers`.
- Implemented registration methods: `register_tool`, `register_command`, `register_chat_interceptor`, `add_panel`.
- `memory_providers` exists as state but no `register_memory_provider` method was verified.
- Sample plugin registers one tool, one command, one interceptor, and one panel.
- Plugin installation copies selected Python source into the configured plugin directory.

## 16. Memory/context census
- Persisted conversation history is represented by `ChatSession.messages`.
- `ChatMessage` stores role/content/id/timestamp/name/metadata.
- Session persistence is JSON under the sessions directory.
- Generated model context is assembled in `MainWindow._generate` from an internal `APP_SYSTEM_PROMPT` message plus `tab.session.messages`.
- Plugin chat interceptors can replace the message list before backend submission.
- `AgentProfile.memory_mode` exists as a persisted data field.
- `PluginContext.memory_providers` exists as a dictionary.
- No retrieved active implementation performs retrieval, embeddings, vector-store lookup, memory summarization, or long-term-memory retrieval.
- No verified `register_memory_provider` API exists in `PluginContext`.
- Therefore: persisted session history and model context construction are VERIFIED; a functioning separate memory subsystem is NOT PRESENT in the inspected active implementation.

## 17. Persistence census
- Config: JSON `config.json`.
- Provider credentials: OS keyring through `keyring`.
- Sessions: one JSON file per session ID.
- Prompts: `prompts.json`.
- Agents: `agents.json`.
- Modelfiles: filesystem text/version files.
- Logs: `locallama-gui.log`.
- UI geometry/state: serialized into config as hex strings.
- Chat exports: JSON, Markdown, or text.
- Config schema migration: schema version 1 -> 2.
- Config file permission attempt: `chmod(0o600)`.
- No database/SQLite persistence was verified in the retrieved active source.

## 18. Packaging/release census
- `pyproject.toml` declares Python >=3.11 and dependencies PySide6, httpx, platformdirs, pydantic, psutil, markdown, keyring.
- Dev dependencies: pytest and ruff.
- Feature branch package version: 1.2.0.
- Console scripts: `myloai` and `locallama-gui`.
- Ruff excludes `archive`, `llm_studio`, `ollama_GUI`.
- Packaging includes Linux PKGBUILD, AppImage, Debian build, desktop entries, macOS DMG build, PyInstaller spec, Windows Inno Setup script, PowerShell build script.
- Release payload validator excludes `.github`, `archive`, `tests`, selected repository documents, and `.pyc`/`.pyo`.

## 19. Test census
| Test file | Verified test symbols |
|---|---|
| `tests/test_backend_and_config.py` | `test_ollama_list_models_parsing`, `test_config_save_load_roundtrip` |
| `tests/test_chat_view.py` | `test_scroll_restore_policy_near_bottom_pins`, `test_scroll_restore_policy_scrolled_up_preserves_position`, `test_visible_messages_exclude_internal_system`, `test_assistant_label_prefers_message_model_then_fallback_active_model`, `test_request_redaction_only_for_internal_system_prompt` |
| `tests/test_config_roundtrip.py` | source not fully retrieved in this session; test symbols UNVERIFIED |
| `tests/test_config_schema.py` | source not fully retrieved; UNVERIFIED |
| `tests/test_controller_invalid_flows.py` | source not fully retrieved; UNVERIFIED |
| `tests/test_controllers.py` | source not fully retrieved; UNVERIFIED |
| `tests/test_diagnostics.py` | source not fully retrieved; UNVERIFIED |
| `tests/test_model_controller_delete.py` | source not fully retrieved; UNVERIFIED |
| `tests/test_model_metadata_table_flags.py` | source not fully retrieved; UNVERIFIED |
| `tests/test_model_operations.py` | source not fully retrieved; UNVERIFIED |
| `tests/test_ollama_backend.py` | source not fully retrieved; UNVERIFIED |
| `tests/test_plugin_lifecycle.py` | source not fully retrieved; UNVERIFIED |
| `tests/test_security_boundaries.py` | source not fully retrieved; UNVERIFIED |

### Test-to-production links verified from retrieved tests
- `OllamaBackend.list_models` -> `test_ollama_list_models_parsing`.
- `AppConfig.save/load` -> `test_config_save_load_roundtrip`.
- `compute_scroll_restore_plan` -> two tests.
- `visible_chat_messages` -> one test.
- `assistant_label` -> one test.
- `redacted_request_messages` -> one test.

## 20. Dependency graph
```text
locallama_gui.app
  -> core.config.AppConfig
  -> core.logging.configure_logging
  -> ui.main_window.MainWindow
  -> ui.production_fixes.apply_production_fixes

MainWindow
  -> SessionManager / PromptManager / AgentManager / PluginManager
  -> ChatController / ModelController / PluginController
  -> create_backend
  -> AsyncTask / StreamTask

create_backend
  -> OllamaBackend
  -> OpenAICompatibleBackend

OllamaBackend / OpenAICompatibleBackend
  -> httpx
  -> HTTP provider

PluginManager
  -> AST static manifest parsing
  -> dynamic module loading
  -> PluginContext
```

## 21. Runtime call graph
### Startup
```text
locallama_gui.app.main
 -> AppConfig.load
 -> configure_logging
 -> QApplication
 -> MainWindow(config)
 -> apply_production_fixes
 -> win.show
 -> app.exec
```
### Chat
```text
ChatTab input/send
 -> ChatController.send_message
 -> window.generate_for_tab
 -> MainWindow._generate
 -> create_backend
 -> plugin_context.chat_interceptors
 -> backend.chat
 -> StreamTask
 -> token/error/completed signals
 -> MainWindow callbacks
 -> session save on completion
```
### Model streaming
```text
ModelController._model_stream_op
 -> create_backend
 -> getattr(backend, method)
 -> StreamTask
 -> OperationStreamParser.feed
 -> ModelWindowPort.update_operation
 -> refresh_backend on completion
```

## 22. State ownership graph
```text
AppConfig -> provider profiles, parameters, plugins, UI state
SessionManager -> persisted ChatSession files
ChatSession -> messages/session metadata
PromptManager -> prompts.json
AgentManager -> agents.json
PluginManager -> loaded plugins + plugin enable/trust state
PluginContext -> tools/commands/interceptors/memory_providers
MainWindow -> active UI state + worker references + active stream
StreamTask -> cancellation/full streamed text
Backend -> base_url/api_key transport state
```

## 23. Data flow
### ChatMessage
```text
ChatController.send_message
 -> ChatMessage('user', text)
 -> ChatSession.messages
 -> MainWindow._generate
 -> plugin interceptors
 -> backend payload
 -> provider
```
### Assistant output
```text
provider response
 -> StreamTask token
 -> MainWindow._append_token
 -> ChatMessage.content += token
 -> ChatTab.render
 -> ChatSession.save on completion
```

## 24. Trust-boundary graph
```text
user-selected plugin file
 -> PluginController.install_plugin
 -> filesystem copy
 -> PluginManager static manifest AST inspection
 -> trusted_plugins check
 -> dynamic import / execution
 -> PluginContext
 -> application UI / interceptors / commands / tools

provider API key
 -> AppConfig / CredentialStore
 -> OS keyring
 -> backend Authorization header for OpenAI-compatible provider

user/session message
 -> ChatSession
 -> MainWindow message assembly
 -> HTTP backend```

## 25. Branch-difference census
### Git comparison
- Base: `main` at `86e3ec01cc3e18e1c3d0ec41d22a95e2aa006154`.
- Head: `feat/myloai-production-packaging` at `5e2c520426386084d795779f3121a3a856d4459a`.
- Ahead/behind: 116 / 11.
- Merge base: `e2f0d56ab3c4cde2e8ec291f45e60f940fedf55a`.

### Added files
- `.github/workflows/release-packaging.yml`
- `docs/qa/WINDOWS-VM-2026-09-09.md`
- `locallama_gui/ui/model_browser.py`
- `locallama_gui/ui/production_fixes.py`
- `locallama_gui/ui/setup_wizard.py`
- `packaging/README.md`
- `packaging/RELEASE_BUILD_SPEC.md`
- `packaging/RELEASE_PAYLOAD.md`
- `packaging/USER_MANUAL.md`
- `packaging/assets/generate_myloai_icon.py`
- `packaging/check-release-payload.py`
- `packaging/linux/PKGBUILD`
- `packaging/linux/appimage/README.md`
- `packaging/linux/appimage/build-appimage.sh`
- `packaging/linux/appimage/myloai.svg`
- `packaging/linux/com.github.gr00t-user-706.locallama-gui.desktop`
- `packaging/linux/debian/README.Debian`
- `packaging/linux/debian/build-deb.sh`
- `packaging/linux/install-myloai.sh`
- `packaging/linux/myloai`
- `packaging/linux/myloai.1`
- `packaging/linux/myloai.desktop`
- `packaging/macos/README.md`
- `packaging/macos/build-dmg.sh`
- `packaging/pyinstaller/myloai.spec`
- `packaging/windows/MyLoAI.iss`
- `packaging/windows/README.md`
- `packaging/windows/build-installer.ps1`

### Modified files
- `CHANGELOG.md`
- `README.md`
- `docs/LAUNCHING.md`
- `docs/PLUGIN_SDK.md`
- `locallama_gui/__init__.py`
- `locallama_gui/__main__.py`
- `locallama_gui/app.py`
- `locallama_gui/core/logging.py`
- `pyproject.toml`

### Verified symbol/contract differences
- `__version__`: 1.1.10 -> 1.2.0.
- package description changed to MyLoAI Control Center wording.
- console entry `myloai` added.
- app window name changed to `MyLoAI Control Center`.
- first-run detection and production-fix invocation added to `app.main`.
- `MainWindow.refresh_backend` is temporarily replaced with a lambda during first-run construction.
- logging changed from file + stream handler on `main` to file-only on feature.
- `model_browser`, `production_fixes`, and `setup_wizard` added.

## 26. Documentation / implementation discrepancies
- `docs/PRODUCTION_CODE_MAP.md` states the active package is `locallama_gui/` and archived trees are historical-only; this matches the recursive-tree scope and active imports verified here.
- `PluginContext` contains `memory_providers`, but no `register_memory_provider` method was found in the fully retrieved `core/managers.py`.
- `AgentProfile.memory_mode` is a data field, but no separate active retrieval/vector memory implementation was verified.
- `MainWindow` and several large files could not be fully retrieved through the connector; therefore documentation-vs-implementation discrepancies inside those complete files are UNVERIFIED.
- Existing documentation may describe behavior not proven by the source; this census does not treat documentation as runtime proof.

## 27. Completeness verification
| Cross-check | Result |
|---|---|
| filesystem/Git tree vs file census | VERIFIED: 106 tracked blobs outside archive represented |
| module inventory vs Python tree | PARTIAL: all Python paths are listed; AST complete only for fully retrieved source |
| imports vs AST | PARTIAL |
| classes vs AST | PARTIAL |
| functions vs AST | PARTIAL |
| methods vs AST | PARTIAL |
| dataclasses vs source | VERIFIED for retrieved domain/config/backend/chat/diagnostics files |
| constants/literals | PARTIAL |
| environment references | VERIFIED for fully retrieved application source; partial globally |
| filesystem paths | PARTIAL globally; application persistence paths verified |
| HTTP endpoints | VERIFIED for retrieved Ollama/OpenAI backends |
| entry points | VERIFIED from feature `pyproject.toml`, `__main__.py`, launcher and validator |
| Qt signals | VERIFIED for retrieved custom signal declarations |
| Qt connections | PARTIAL because `main_window.py` was returned as excerpts |
| workers | VERIFIED for `AsyncTask`/`StreamTask` |
| plugin hooks | VERIFIED for manager/context/sample plugin |
| persistence | VERIFIED for config/session/prompt/agent/backend-visible persistence |
| tests | PARTIAL: 2 test files fully retrieved; 11 test files tree-verified but source symbols unverified |
| branch diff | VERIFIED at Git file-diff metadata level; source-level diff partial for large files |

### Machine-verifiable counts from this session
- Git-tree blobs outside archive: 106
- Python files in tree: 44
- Test files: 13
- Packaging files: 23
- GitHub metadata files: 9
- Total recorded bytes outside archive: 420,262
- Fully source-retrieved/verified Python modules represented in symbol inventory: 18

## 28. Known blind spots
1. `locallama_gui/ui/main_window.py` is 41,757 bytes. The connector returned source excerpts, not the entire blob. The method/state list above reflects verified excerpts plus prior retrieved source observations, but exact AST-level locations and any symbols outside the returned excerpts are UNVERIFIED.
2. `locallama_gui/ui/dialogs.py` is 22,055 bytes and its complete source was not retrieved in this session. Its exact full AST inventory is UNVERIFIED.
3. `locallama_gui/core/managers.py` is 11,465 bytes; the connector response was truncated after the plugin manager body. The listed manager symbols are present in the retrieved source, but exact final-file completeness is marked UNVERIFIED.
4. `locallama_gui/core/config.py` is 10,323 bytes; its source was returned with the complete visible content in the connector response used here, but exact line-number extraction was not available.
5. Several tests, documentation files, packaging scripts, and UI modules were verified by Git-tree presence and byte size but not fully source-parsed in this session.
6. No claim is made that an unverified file contains or lacks a symbol.
7. No runtime execution or dynamic import tracing was performed against the user's machine; runtime claims are static-source claims only.

## 29. Final verified architecture map
```text
ENTRYPOINTS
  locallama-gui ─┐
  myloai ────────┼──> locallama_gui.app.main
  python -m ─────┘
                     │
                     ├── AppConfig / CredentialStore
                     ├── logging
                     ├── QApplication
                     ├── MainWindow
                     │      ├── ChatController
                     │      ├── ModelController
                     │      ├── PluginController
                     │      ├── SessionManager
                     │      ├── PromptManager
                     │      ├── AgentManager
                     │      ├── PluginManager / PluginContext
                     │      ├── AsyncTask / StreamTask
                     │      └── backend factory
                     │               ├── OllamaBackend ──> Ollama HTTP
                     │               └── OpenAICompatibleBackend ──> OpenAI-compatible HTTP
                     │
                     └── production_fixes / first-run setup / model browser

DATA
  ChatMessage -> ChatSession.messages -> request construction -> backend -> streamed assistant content -> session JSON

PLUGIN
  plugin file -> static AST manifest -> trust check -> dynamic import -> Plugin.activate(context)
       -> tools / commands / chat interceptors / panels

PERSISTENCE
  config.json
  OS keyring
  sessions/*.json
  prompts/prompts.json
  agents/agents.json
  modelfiles
  log file
```

## 30. Source-of-truth rule
- This document does not redesign the repository.
- It does not treat intended architecture as implementation.
- It does not silently treat documentation as source proof.
- Unretrieved source is explicitly marked UNVERIFIED.
- `archive/` is excluded except where repository metadata identifies it in branch/package rules.
- No repository file was modified by this census.

# 31. GAP-COMPLETION / EXHAUSTIVENESS REPAIR PASS

**Repair date:** 2026-09-10  
**Repository:** `GR00T-User-706/locallama-gui`  
**Audited ref:** `feat/myloai-production-packaging` @ `5e2c520426386084d795779f3121a3a856d4459a`  
**Comparison ref:** `main` @ `86e3ec01cc3e18e1c3d0ec41d22a95e2aa006154`  
**Merge base:** `e2f0d56ab3c4cde2e8ec291f45e60f940fedf55a`  
**Mode:** READ-ONLY

This section is a repair of the preceding census, not a replacement architecture document.

## 31.1 What the previous census actually left incomplete

The previous document was correct about the repository tree and broad architecture, but its own evidence markers showed that the following were not yet individually enumerated:

1. Python imports were represented as module-level lists rather than one occurrence record per statement.
2. Symbols were represented as class/method lists without complete signatures, decorators, state effects, callers, or source spans.
3. `dialogs.py` and `main_window.py` were explicitly marked partial because the connector had returned truncated large-file excerpts.
4. `model_browser.py`, `production_fixes.py`, `setup_wizard.py`, `theme.py`, package initializers, and all 13 test modules were previously listed as unverified despite now being retrieved.
5. Qt `.connect()` relationships were summarized rather than individually mapped.
6. Worker creation sites were summarized rather than enumerated as execution boundaries.
7. Persistence was grouped by subsystem rather than by individual operation.
8. Tests were represented mostly as test-file/target summaries rather than a complete exact test-function inventory.
9. Branch differences were correct at Git file-diff level but did not yet include the complete changed-symbol contract for the feature-only production packaging changes.
10. The document stopped at section 30 and therefore did not contain the requested independent counts/reconciliation sections 31/32.

## 31.2 Source retrieval repair

The following previously incomplete active Python sources were retrieved from the feature ref during this pass:

| File | Result |
|---|---|
| `locallama_gui/__init__.py` | STATIC_VERIFIED |
| `locallama_gui/__main__.py` | STATIC_VERIFIED |
| `locallama_gui/core/logging.py` | STATIC_VERIFIED |
| `locallama_gui/ui/model_browser.py` | STATIC_VERIFIED |
| `locallama_gui/ui/production_fixes.py` | STATIC_VERIFIED |
| `locallama_gui/ui/setup_wizard.py` | STATIC_VERIFIED |
| `locallama_gui/ui/theme.py` | STATIC_VERIFIED |
| `locallama_gui/ui/main_window.py` | STATIC_VERIFIED; exact file length established as 1,050 source lines |
| `locallama_gui/ui/dialogs.py` | STATIC_VERIFIED; exact file length established as 600 source lines |
| `locallama_gui/backends/__init__.py` | STATIC_VERIFIED; empty |
| `locallama_gui/core/__init__.py` | STATIC_VERIFIED; empty |
| `locallama_gui/plugins/__init__.py` | STATIC_VERIFIED; empty |
| `locallama_gui/ui/__init__.py` | STATIC_VERIFIED; empty |
| `locallama_gui/ui/controllers/__init__.py` | STATIC_VERIFIED |
| all 13 files under `tests/` | STATIC_VERIFIED |

The two formerly largest blind spots are therefore no longer source-truncation blind spots.

The Git tree still does not expose line counts for arbitrary non-Python blobs. Those records retain their verified byte/mode/tree status, while line count remains `UNVERIFIED` unless source text was retrieved and counted.

## 31.3 Repaired module/symbol inventory

### Package/entry modules

`locallama_gui/__init__.py`
- module docstring
- `__version__ = "1.2.0"`

`locallama_gui/__main__.py`
- import: `from locallama_gui.app import main`
- module guard: `raise SystemExit(main())`

`locallama_gui/ui/controllers/__init__.py`
- relative imports:
  - `.chat_controller import ChatController`
  - `.model_controller import ModelController`
  - `.plugin_controller import PluginController`
- `__all__ = ["ChatController", "ModelController", "PluginController"]`

### `locallama_gui/ui/model_browser.py`

`ModelRecommendation` is a frozen dataclass:
- `name: str`
- `size: str`
- `purpose: str`
- `minimum_ram_gib: float`

`CATALOG` contains exactly five recommendation records:
- `gemma3:1b`, ~0.8 GB, starter, 4 GiB
- `qwen3.5:4b`, ~3.4 GB, general + vision, 8 GiB
- `mistral:7b`, ~4.1 GB, general, 12 GiB
- `deepseek-r1:7b`, ~4.7 GB, reasoning, 12 GiB
- `qwen2.5-coder:7b`, ~4.7 GB, coding, 12 GiB

`ModelBrowserDialog(QDialog)`:
- `__init__(window, recommended_name: str | None = None) -> None`
- `filter_models(text: str) -> None`
- `open_library() -> None`
- `pull_selected() -> None`

State created:
- `window`
- `list`
- `search`
- `pull_button`
- `library_button`
- `close_button`

Qt connections:
- `close_button.rejected -> reject`
- `pull_button.clicked -> pull_selected`
- `library_button.clicked -> open_library`
- `search.textChanged -> filter_models`
- `task.token -> on_stream`
- `task.completed -> on_completed`
- `task.error -> on_error`

External effect:
- opens `https://ollama.com/search`, optionally with `?q=<quote_plus(query)>`
- starts `StreamTask` for backend `pull_model`

### `locallama_gui/ui/setup_wizard.py`

`FirstRunWizard(QWizard)`:
- `__init__(config, parent=None) -> None`
- `_build_welcome_page() -> QWizardPage`
- `_build_hardware_page() -> QWizardPage`
- `_build_backend_page() -> QWizardPage`
- `_build_finish_page() -> QWizardPage`
- `_recommended_model() -> str`
- `_page_changed(index: int) -> None`
- `_check_backend() -> None`
- `accept() -> None`

Instance state:
- `config`
- `_connection_ok`
- `_pull_on_finish`
- `welcome_page`
- `hardware_page`
- `backend_page`
- `finish_page`
- `hardware_label`
- `provider_label`
- `status_label`
- `model_combo`
- `pull_check`
- `install_button`
- `finish_label`
- `_task`
- `_pull_task`

Qt connections:
- `currentIdChanged -> _page_changed`
- download button `clicked -> QDesktopServices.openUrl`
- `AsyncTask.result -> done`
- `AsyncTask.error -> failed`
- `StreamTask.token -> operation parser/update`
- `StreamTask.completed -> done`
- `StreamTask.error -> failed`

Hardware selection:
- `<6 GiB -> gemma3:1b`
- `<12 GiB -> qwen3.5:4b`
- `<24 GiB -> mistral:7b`
- otherwise `deepseek-r1:7b`

Worker boundaries:
- `_check_backend` creates `AsyncTask(work)` where `work` awaits `create_backend(...).test_connection()`.
- `accept` may create `StreamTask` for `create_backend(profile).pull_model(model)`.

### `locallama_gui/ui/production_fixes.py`

Module-level functions:
- `_menu(window, title: str)`
- `_remove_action(menu, text: str) -> None`
- `_replace_action(menu, text: str, callback) -> None`
- `_resource_path(name: str) -> Path`
- `_open_bundled_document(window, title: str, name: str) -> None`
- `_show_about(window) -> None`
- `_choose_theme(window) -> None`
- `_import_agent(window) -> None`
- `_export_agent(window) -> None`
- `_show_model_browser(window) -> None`
- `_build_diagnostics_submenu(window, developer) -> None`
- `_add_ai_model_settings(settings, window) -> None`
- `apply_production_fixes(window, first_run: bool = False) -> None`

Observed side effects:
- mutates existing menu actions
- inserts a model-browser action
- opens bundled documentation from `packaging/`
- imports/exports `AgentProfile` JSON
- changes theme and persists config
- schedules `FirstRunWizard` with `QTimer.singleShot(250, ...)` when `first_run=True`

### `locallama_gui/ui/theme.py`

- `dark_qss(font_size: int = 12) -> str`
- `DARK_QSS = dark_qss()`

No class, signal, worker, network, or filesystem operation.

### `locallama_gui/core/logging.py`

- `configure_logging(log_dir: Path) -> None`
- creates `log_dir`
- configures `logging.basicConfig`
- uses `FileHandler(log_dir / "locallama-gui.log")`
- feature branch intentionally has no `StreamHandler`

### `locallama_gui/ui/main_window.py`

The previously truncated method inventory is now source-complete at 1,050 lines.

Classes:
- `ChatTab(QWidget)`
- `ComposerTextEdit(QPlainTextEdit)`
- `MainWindow(QMainWindow)`

Module function:
- `_build_readonly_table_item(value: str) -> QTableWidgetItem`

`ChatTab` methods:
- `__init__(session: ChatSession) -> None`
- `render(active_model: str = "") -> None`
- `set_generating(generating: bool) -> None`

`ComposerTextEdit` signals:
- `send_requested = Signal()`
- `zoom_requested = Signal(int)`

`ComposerTextEdit` methods:
- `keyPressEvent(event) -> None`
- `wheelEvent(event) -> None`

`MainWindow` methods, in source order:
- `__init__(config: AppConfig) -> None`
- `_build_ui() -> None`
- `_create_docks() -> None`
- `_dock(title: str, widget: QWidget, area: Qt.DockWidgetArea) -> QDockWidget`
- `add_plugin_panel(title: str, widget: QWidget, area: Any = None) -> None`
- `_menu_action(menu, text, slot, shortcut: str | None = None)`
- `_build_menus() -> None`
- `_build_file_menu() -> None`
- `_build_models_menu() -> None`
- `_build_agents_menu() -> None`
- `_build_plugins_menu() -> None`
- `_build_settings_menu() -> None`
- `_build_view_menu() -> None`
- `_build_developer_menu() -> None`
- `_build_help_menu() -> None`
- `current_tab() -> ChatTab | None`
- `new_chat() -> None`
- `_wire_chat_tab(tab: ChatTab) -> None`
- `close_tab(idx: int) -> None`
- `_generate(tab: ChatTab) -> None`
- `_append_token(tab: ChatTab, msg: ChatMessage, token: str, owner_id: int) -> None`
- `_stream_error(error: str, owner_id: int) -> None`
- `_stream_done(tab: ChatTab, owner_id: int) -> None`
- `stop_generation() -> None`
- `model_changed(text: str) -> None`
- `refresh_backend() -> None`
- `_show_dock(dock: QDockWidget | None, name: str) -> None`
- `show_diagnostics_dock() -> None`
- `_show_diagnostics_tab(index: int) -> None`
- `show_logs_dock() -> None`
- `show_console_dock() -> None`
- `show_operations_dock() -> None`
- `show_request_dock() -> None`
- `show_token_dock() -> None`
- `_backend_refresh_error(error: str) -> None`
- `_backend_refreshed(result: Any) -> None`
- `_update_backend_status(state: str, latency_ms: float, detail: str) -> None`
- `_refresh_model_combo() -> None`
- `_refresh_model_table() -> None`
- `_insert_model_table_row(model: ModelInfo) -> None`
- `switch_provider(name: str) -> None`
- `refresh_sessions() -> None`
- `refresh_prompts() -> None`
- `apply_prompt_item(item) -> None`
- `save_as() -> None`
- `open_session(session_id: str) -> None`
- `import_chat() -> None`
- `export_current() -> None`
- `_async(coro_factory, done_msg: str) -> None`
- `run_async(coro_factory, done_msg: str, *, start_msg: str, error_title: str, parent: QWidget | None = None) -> None`
- `set_tab_title(title: str) -> None`
- `render_tab(tab: ChatTab) -> None`
- `generate_for_tab(tab: ChatTab) -> None`
- `model_name() -> str`
- `_install_diagnostics_sinks() -> None`
- `append_log(text: str) -> None`
- `append_console(text: str) -> None`
- `append_operation_history(text: str) -> None`
- `begin_operation(operation: str) -> None`
- `update_operation(update: OperationUpdate) -> None`
- `complete_operation(operation: str) -> None`
- `fail_operation(operation: str, error: str) -> None`
- `add_worker(worker: Any) -> None`
- `open_modelfile_editor() -> None`
- `build_model_from_modelfile(name: str, modelfile: str) -> None`
- `open_template_viewer() -> None`
- `_show_text_dialog(title: str, text: str) -> None`
- `open_endpoints() -> None`
- `open_parameters() -> None`
- `edit_default_system_prompt() -> None`
- `open_plugins() -> None`
- `open_plugin_docs() -> None`
- `open_agent_builder() -> None`
- `import_agent() -> None`
- `export_agent() -> None`
- `toggle_theme() -> None`
- `show_shortcuts() -> None`
- `adjust_font_size(delta: int) -> None`
- `toggle_all_docks() -> None`
- `reset_layout() -> None`
- `inspect_api() -> None`
- `_open_document(title: str, path: Path) -> None`
- `open_docs() -> None`
- `about() -> None`
- `diagnostics() -> None`
- `log(text: str) -> None`
- `_restore_state() -> None`
- `closeEvent(event) -> None`

Important direct state mutations:
- `MainWindow._generate` creates/assigns `current_stream`, `_active_stream_owner`, appends `worker_refs`, mutates session model/provider/messages.
- `_append_token` mutates `ChatMessage.content`.
- `_stream_done` persists the session.
- `stop_generation` cancels and clears active stream state.
- `refresh_backend` creates an `AsyncTask`.
- `closeEvent` restores stdio, removes the log handler, cancels workers, persists geometry/state/config.

### `locallama_gui/ui/dialogs.py`

Classes:
- `ModelfileHighlighter(QSyntaxHighlighter)`
- `EndpointDialog(QDialog)`
- `ModelfileEditor(QDialog)`
- `PromptManagerDialog(QDialog)`
- `AgentBuilderDialog(QDialog)`
- `PluginManagerDialog(QDialog)`
- `ParameterDialog(QDialog)`

Methods:
- `ModelfileHighlighter.highlightBlock(text: str) -> None`
- `EndpointDialog.__init__(config: AppConfig, parent: QWidget | None = None) -> None`
- `EndpointDialog.add_row(profile: ProviderProfile | None = None) -> None`
- `EndpointDialog.accept() -> None`
- `ModelfileEditor.__init__(config: AppConfig, parent: QWidget | None = None) -> None`
- `ModelfileEditor.new() -> None`
- `ModelfileEditor.open_file() -> None`
- `ModelfileEditor.save() -> None`
- `ModelfileEditor.duplicate() -> None`
- `ModelfileEditor.validate() -> None`
- `ModelfileEditor.build_model() -> None`
- `ModelfileEditor.update_preview() -> None`
- `PromptManagerDialog.__init__(manager: PromptManager, parent: QWidget | None = None) -> None`
- `PromptManagerDialog.refresh() -> None`
- `PromptManagerDialog.load_selected(row: int) -> None`
- `PromptManagerDialog.new() -> None`
- `PromptManagerDialog.save() -> None`
- `PromptManagerDialog.delete() -> None`
- `PromptManagerDialog.import_prompt() -> None`
- `PromptManagerDialog.export_prompts() -> None`
- `AgentBuilderDialog.__init__(manager: AgentManager, models: list[str], plugins: list[str], parent: QWidget | None = None) -> None`
- `AgentBuilderDialog.refresh() -> None`
- `AgentBuilderDialog.load_selected(row: int) -> None`
- `AgentBuilderDialog.new() -> None`
- `AgentBuilderDialog._agent() -> AgentProfile`
- `AgentBuilderDialog.save() -> None`
- `AgentBuilderDialog.import_agent() -> None`
- `AgentBuilderDialog.export_agent() -> None`
- `PluginManagerDialog.__init__(manager: PluginManager, parent: QWidget | None = None) -> None`
- `PluginManagerDialog.refresh() -> None`
- `PluginManagerDialog.apply() -> None`
- `PluginManagerDialog.reload_plugins() -> None`
- `ParameterDialog.__init__(config: AppConfig, parent: QWidget | None = None) -> None`
- nested `ParameterDialog.__init__.<locals>.spin(name: str, value: int, lo: int, hi: int) -> QSpinBox`
- nested `ParameterDialog.__init__.<locals>.dbl(name: str, value: float, lo: float, hi: float) -> QLineEdit`
- `ParameterDialog._collect() -> dict[str, object]`
- `ParameterDialog.save_preset() -> None`
- `ParameterDialog.load_preset() -> None`
- `ParameterDialog.accept() -> None`

Nested-function evidence is explicitly recorded here because the prior census did not.

## 31.4 Repaired import-occurrence inventory

The companion file `LocalLama_Forensic_Census_Dependencies.md` contains the normalized one-record-per-import-statement inventory.

Important repaired distinctions:
- `from .chat_controller ...` etc. are relative imports.
- `__import__("json")` in `AgentBuilderDialog.import_agent/export_agent` is a dynamic import occurrence, not a static top-level import.
- `PySide6.QtWidgets` imports inside controller methods are dynamic/conditional-at-call-time imports.
- `importlib.util.spec_from_file_location` in `PluginManager._load_module` is dynamic module loading and is not equivalent to a static import dependency.
- `ast.parse` in plugin discovery inspects plugin source without executing it.

## 31.5 Repaired dataclass-field inventory

The complete active dataclass set established from source is:

| Dataclass | Fields |
|---|---|
| `AppPaths` | config_dir, data_dir, logs_dir, sessions_dir, prompts_dir, agents_dir, modelfiles_dir, plugins_dir |
| `ProviderProfile` | name, provider_type, base_url, api_key, default_model, enabled |
| `GenerationParameters` | temperature, top_k, top_p, min_p, repeat_penalty, repeat_last_n, mirostat, mirostat_eta, mirostat_tau, tfs_z, num_predict, seed, stop, num_ctx, num_batch, num_gpu, reasoning_mode, thinking_mode, plan_mode, normal_mode |
| `UISettings` | theme, geometry_hex, state_hex, active_session_id, font_size |
| `AppConfig` | paths, schema_version, provider_profiles, active_provider, parameters, parameter_presets, enabled_plugins, trusted_plugins, developer_mode, ui, global_system_prompt |
| `ChatMessage` | role, content, id, created_at, name, metadata |
| `ChatSession` | title, id, created_at, updated_at, provider, model, system_prompt, messages, parameters |
| `ModelInfo` | name, size, parameter_size, quantization, context_size, backend, metadata |
| `PromptRecord` | title, content, category, favorite, id, versions, updated_at |
| `AgentProfile` | name, model, system_prompt_id, tools, plugins, memory_mode, reasoning_mode, behavior, execution_policy, id |
| `BackendStatus` | state, latency_ms, detail |
| `ScrollRestorePlan` | should_pin_bottom, previous_value |
| `OperationUpdate` | status, history_text, completed, total |
| `ModelRecommendation` | name, size, purpose, minimum_ram_gib |

All are `@dataclass`; the first ten core/config/domain records use `slots=True`. `ScrollRestorePlan`, `OperationUpdate`, and `ModelRecommendation` are frozen dataclasses.

## 31.6 Repaired instance-state inventory

### `MainWindow`
Primary mutable state:
- `config`
- `sessions`
- `prompts`
- `agents`
- `plugin_context`
- `plugins`
- `models`
- `chat_controller`
- `model_controller`
- `plugin_controller`
- `worker_refs`
- `current_stream`
- `_stream_owner_seq`
- `_active_stream_owner`
- `_diagnostics_signals`
- `_diagnostics_log_handler`
- `_original_stdout`
- `_original_stderr`
- `tabs`
- `status`
- `toolbar`
- `provider_combo`
- `model_combo`
- `model_table`
- `sessions_list`
- `prompt_list`
- `log_view`
- `console_view`
- `operation_status`
- `operation_progress`
- `operation_history`
- `diagnostics_tabs`
- `diagnostics_dock`
- `request_view`
- `request_copy`
- `request_clear`
- `request_dock`
- `token_view`
- `token_copy`
- `token_clear`
- `token_dock`

### `ChatTab`
- `session`
- `chat`
- `input`
- `streaming`
- `send`
- `stop`
- `regen`
- `retry`
- `copy_last`
- `edit_msg`
- `delete_msg`

### `ComposerTextEdit`
No explicit application-owned `self.*` state is created; behavior is held by Qt base class and custom signals.

### `FirstRunWizard`
- `config`
- `_connection_ok`
- `_pull_on_finish`
- page/widget references listed in 31.3
- `_task`
- `_pull_task`

### `ModelBrowserDialog`
- `window`
- `list`
- `search`
- `pull_button`
- `library_button`
- `close_button`

### `EndpointDialog`
- `config`
- `table`

### `ModelfileEditor`
- `config`
- `path`
- `editor`
- `preview`
- `name`
- dynamically-created button attributes: `new`, `open`, `save`, `duplicate`, `validate`, `preview_config`, `build_model`

### `PromptManagerDialog`
- `manager`
- `listw`
- `editor`
- `title`
- `category`
- `favorite`
- `current_id`
- `prompts`

### `AgentBuilderDialog`
- `manager`
- `current_id`
- `agents`
- `name`
- `model`
- `reasoning`
- `behavior`
- `memory`
- `policy`
- `tools`
- `plugins`
- `items`

### `PluginManagerDialog`
- `manager`
- `table`
- `plugins`

### `ParameterDialog`
- `config`
- `widgets`
- `stop`
- `preset_name`
- `reasoning_mode`

### Worker state
`AsyncTask`:
- `coro_factory`

`StreamTask`:
- `iterator_factory`
- `_cancelled`
- `full_text`

## 31.7 Repaired Qt signal / connection inventory

### Declared custom signals

| Owner | Signal | Signature |
|---|---|---|
| `ComposerTextEdit` | `send_requested` | `()` |
| `ComposerTextEdit` | `zoom_requested` | `(int)` |
| `DiagnosticsSignals` | `log_line` | `(str)` |
| `DiagnosticsSignals` | `console_text` | `(str)` |
| `AsyncTask` | `result` | `(object)` |
| `AsyncTask` | `error` | `(str)` |
| `AsyncTask` | `finished_ok` | `()` |
| `StreamTask` | `token` | `(str)` |
| `StreamTask` | `error` | `(str)` |
| `StreamTask` | `completed` | `(str)` |

### MainWindow connection records

`MainWindow._build_ui`:
- `tabs.tabCloseRequested -> close_tab`
- toolbar action `New Chat -> new_chat`
- toolbar action `Save -> ChatController.save_current`
- toolbar action `Refresh Models -> refresh_backend`
- toolbar action `Parameters -> open_parameters`
- toolbar action `Plugins -> open_plugins`
- `provider_combo.currentTextChanged -> switch_provider`
- `model_combo.currentTextChanged -> model_changed`

`MainWindow._create_docks`:
- `sessions_list.itemDoubleClicked -> lambda -> open_session`
- `prompt_list.itemDoubleClicked -> apply_prompt_item`
- `request_copy.clicked -> lambda -> QApplication.clipboard().setText(...)`
- `request_clear.clicked -> request_view.clear`
- `token_copy.clicked -> lambda -> QApplication.clipboard().setText(...)`
- `token_clear.clicked -> token_view.clear`

`MainWindow._wire_chat_tab`:
- `send.clicked -> ChatController.send_message`
- `input.send_requested -> ChatController.send_message`
- `input.zoom_requested -> MainWindow.adjust_font_size`
- `stop.clicked -> stop_generation`
- `regen.clicked -> ChatController.regenerate`
- `retry.clicked -> ChatController.retry`
- `copy_last.clicked -> ChatController.copy_last_message`
- `edit_msg.clicked -> lambda -> ChatController.edit_message`
- `delete_msg.clicked -> lambda -> ChatController.delete_message`

Generation:
- `StreamTask.token -> lambda -> _append_token`
- `StreamTask.error -> lambda -> _stream_error`
- `StreamTask.completed -> lambda -> _stream_done`

Backend refresh:
- `AsyncTask.result -> _backend_refreshed`
- `AsyncTask.error -> lambda -> _backend_refresh_error`

Generic async:
- `AsyncTask.finished_ok -> on_completed`
- `AsyncTask.error -> on_error`

Model creation:
- `StreamTask.token -> on_stream`
- `StreamTask.completed -> on_completed`
- `StreamTask.error -> on_error`

Template viewer:
- `AsyncTask.result -> on_result`
- `AsyncTask.error -> on_error`

Diagnostics:
- `DiagnosticsSignals.log_line -> append_log`
- `DiagnosticsSignals.console_text -> append_console`

### Other active Qt connection records

`EndpointDialog`
- Add clicked -> `add_row`
- Remove clicked -> lambda removing current row
- Save accepted -> `accept`
- Cancel rejected -> `reject`

`ModelfileEditor`
- each seven action button `clicked -> new/open_file/save/duplicate/validate/update_preview/build_model`

`PromptManagerDialog`
- `listw.currentRowChanged -> load_selected`
- five buttons -> `new/save/delete/import_prompt/export_prompts`

`AgentBuilderDialog`
- `agents.currentRowChanged -> load_selected`
- four buttons -> `new/save/import_agent/export_agent`

`PluginManagerDialog`
- Reload -> `reload_plugins`
- Apply -> `apply`

`ParameterDialog`
- Save Preset -> `save_preset`
- Load Preset -> `load_preset`
- dialog accepted/rejected -> `accept/reject`

`ModelBrowserDialog`
- close rejected -> `reject`
- pull -> `pull_selected`
- library -> `open_library`
- search textChanged -> `filter_models`
- worker token/completed/error -> nested callbacks

`FirstRunWizard`
- current page changed -> `_page_changed`
- install button -> `QDesktopServices.openUrl`
- backend `AsyncTask.result/error` -> callbacks
- pull `StreamTask.token/completed/error` -> callbacks

No `@Slot`/`@pyqtSlot` decorator was found in the active source retrieved in this pass.

## 31.8 Repaired worker/execution-boundary inventory

| Creator | Worker | Execution | Output | Consumer |
|---|---|---|---|---|
| `MainWindow._generate` | `StreamTask` | `backend.chat(...)` async iterator | token/error/completed | `_append_token`, `_stream_error`, `_stream_done` |
| `MainWindow.refresh_backend` | `AsyncTask` | backend connection + model listing coroutine | result/error | `_backend_refreshed`, `_backend_refresh_error` |
| `MainWindow._async` | `AsyncTask` | arbitrary coroutine factory | finished/error | logging/refresh or error dialog |
| `MainWindow.run_async` | `AsyncTask` | arbitrary coroutine factory | finished/error | operation lifecycle |
| `MainWindow.build_model_from_modelfile` | `StreamTask` | backend `create_model` | operation parser updates | operation UI |
| `MainWindow.open_template_viewer` | `AsyncTask` | backend `show_model` | result/error | text dialog / error |
| `ModelController._model_stream_op` | `StreamTask` | backend model operation | token/error/completed | operation UI |
| `ModelBrowserDialog.pull_selected` | `StreamTask` | backend `pull_model` | operation parser updates | dialog/main-window operation UI |
| `FirstRunWizard._check_backend` | `AsyncTask` | backend `test_connection` | status/error | wizard labels |
| `FirstRunWizard.accept` | `StreamTask` | backend `pull_model` | operation parser updates | wizard/main-window operation UI |

`AsyncTask.run()` executes its coroutine via `asyncio.run` inside the `QThread`.
`StreamTask.run()` consumes the async iterator and emits output from the worker thread through Qt signals.
`MainWindow.worker_refs` retains worker objects.
Chat generation additionally uses `_stream_owner_seq` / `_active_stream_owner` to reject stale token/error/completion callbacks.

## 31.9 Repaired HTTP/API request inventory

### Ollama backend

| Method | Endpoint | Source operation | Stream | Auth |
|---|---|---|---|---|
| GET | `/api/tags` | `test_connection`, `list_models` | no | none |
| POST | `/api/chat` | `chat` | optional | none |
| POST | `/api/pull` | `pull_model` | yes | none |
| POST | `/api/push` | `push_model` | yes | none |
| DELETE | `/api/delete` | `delete_model` | no | none |
| POST | `/api/copy` | `copy_model` | no | none |
| POST | `/api/create` | `create_model` | yes | none |
| POST | `/api/show` | `show_model` | no | none |

Transport is `httpx`.
Streaming is line-oriented JSON from `aiter_lines()`.
`SUPPORTED_OPTIONS` filters Ollama option fields.
Top-level `think` is handled separately from `options`.

### OpenAI-compatible backend

| Method | Endpoint | Source operation | Stream | Auth |
|---|---|---|---|---|
| GET | `/models` | `list_models` / connection test | no | optional Bearer |
| POST | `/chat/completions` | `chat` | optional | optional Bearer |

Streaming parser handles `data: ...` records and `[DONE]`.

No websocket or `requests`/`urllib` request boundary was verified in active application source.

## 31.10 Repaired filesystem/persistence operation inventory

Individual operations established from source:

- `AppPaths.create`: create config/data/log/session/prompt/agent/modelfile/plugin directories.
- `AppConfig.load`: read `<config_dir>/config.json`.
- `AppConfig.save`: write `<config_dir>/config.json`; chmod `0600`.
- `CredentialStore.get`: read OS keyring.
- `CredentialStore.set`: write/delete OS keyring credential.
- `SessionManager.list_sessions`: glob `sessions/*.json`; read each.
- `SessionManager.load`: read one session JSON.
- `SessionManager.save`: serialize and write one session JSON.
- `SessionManager.import_session`: read external session, save into session directory.
- `PromptManager.__init__`: create `prompts.json` if absent.
- `PromptManager.list`: read `prompts.json`.
- `PromptManager.save_all`: overwrite `prompts.json`.
- `PromptManager.upsert`: read then overwrite `prompts.json`.
- `PromptManager.delete`: read then overwrite `prompts.json`.
- `PromptManager.import_file`: read selected file then persist prompt.
- `PromptManager.export`: `shutil.copyfile(prompts.json, selected destination)`.
- `AgentManager.__init__`: create `agents.json` if absent.
- `AgentManager.list`: read `agents.json`.
- `AgentManager.save_all`: overwrite `agents.json`.
- `AgentManager.upsert`: read then overwrite `agents.json`.
- `ChatSession.from_file`: read JSON and deserialize messages.
- `ChatSession.save`: create directory and write `<id>.json`.
- `ChatSession.export_markdown`: in-memory serialization only.
- `ChatSession.export_text`: in-memory serialization only.
- `MainWindow.save_as`: write selected JSON export.
- `MainWindow.export_current`: write selected JSON/Markdown/Text export.
- `MainWindow._restore_state`: read serialized Qt geometry/state from config fields.
- `MainWindow.closeEvent`: write Qt geometry/state into config then persist config.
- `ModelfileEditor.open_file`: read selected Modelfile.
- `ModelfileEditor.save`: write Modelfile and write version copy under `.versions/<stem>/<n>.Modelfile`.
- `AgentBuilderDialog.import_agent`: read selected JSON and deserialize `AgentProfile`.
- `AgentBuilderDialog.export_agent`: serialize `AgentProfile` and write JSON.
- `production_fixes._open_bundled_document`: read bundled documentation.
- `production_fixes._export_agent`: serialize/write `AgentProfile`.
- `production_fixes._import_agent`: read/deserialize selected agent JSON.
- `MainWindow.open_docs`: read `README.md`.
- `MainWindow.open_plugin_docs`: read `docs/PLUGIN_SDK.md`.
- `MainWindow._open_document`: generic text-file read.
- `PluginManager.plugin_paths`: glob plugin directory.
- `PluginManager.remove`: unlink plugin file.

No SQLite/database persistence was found in the active tree.

## 31.11 Environment-variable inventory

Verified active application environment references:

| Variable | File | Operation | Default | Effect |
|---|---|---|---|---|
| `QT_ENABLE_HIGHDPI_SCALING` | `locallama_gui/app.py` | read/write via `os.environ.setdefault` | `"1"` | Qt high-DPI scaling |
| `QT_AUTO_SCREEN_SCALE_FACTOR` | `locallama_gui/app.py` | read/write via `os.environ.setdefault` | `"1"` | Qt automatic screen scaling |

Shell/packaging scripts also consume standard shell environment such as `HOME`/`PATH` through shell expansion and `command -v`; those are not application Python environment APIs.

## 31.12 Plugin hook repair

Actual hook lifecycle:

1. `PluginManager.plugin_paths()` discovers `*.py`.
2. `discover()` calls `_read_static_manifest()` using `ast.parse` and `ast.literal_eval`.
3. `trust()` verifies a valid manifest before adding the ID to `config.trusted_plugins`.
4. `enable()` requires trust.
5. `enable()` dynamically imports the file.
6. It instantiates `Plugin`.
7. Runtime `manifest` is revalidated.
8. Runtime manifest ID must match static ID.
9. `instance.activate(context)` is invoked.
10. `PluginContext` stores registrations.

Actual registration stores:
- `tools[name]`
- `commands[name]`
- `chat_interceptors.append(callable_)`
- `main_window.add_plugin_panel(...)`

Actual invocation:
- `chat_interceptors` are invoked by `MainWindow._generate`.
- tools and commands are registered and exposed in context, but no active invocation path for arbitrary tool/command execution was verified in this source set.
- panels are attached by `PluginContext.add_panel`.
- `deactivate()` is invoked by `PluginManager.disable`.
- `reload()` disables then reloads enabled plugins.

`memory_providers` is exposed as a dictionary but no `register_memory_provider` method or active invocation path was found.

## 31.13 Memory/context repair

### Conversation history
**VERIFIED**
- `ChatSession.messages`
- `ChatMessage`
- session JSON persistence

### System prompt
Two distinct sources exist:
1. user-editable `AppConfig.global_system_prompt`, inserted into a new chat as an ordinary `ChatMessage("system", ...)`;
2. internal `APP_SYSTEM_PROMPT`, injected at generation time with metadata `{"internal": True, "source": "app"}`.

### Model context
**VERIFIED**
`MainWindow._generate`:
1. creates internal app system message;
2. extends with `tab.session.messages`;
3. passes the list through every registered `chat_interceptor`;
4. passes resulting messages to backend;
5. for request preview only, redacts the internal app system prompt.

### Persistent/retrieved memory
**NOT PRESENT / NOT VERIFIED**
- no vector store
- no embeddings lookup
- no retrieval pipeline
- no summarization memory
- no separate long-term memory service

`AgentProfile.memory_mode` and `PluginContext.memory_providers` are data/API surfaces, not proof of an active memory implementation.

## 31.14 Test-function inventory repair

Exactly **49 test functions** were established across the 13 active test files.

See `LocalLama_Forensic_Census_Tests.md` for the complete one-record-per-test list and reverse production-symbol matrix.

High-value reverse coverage established:
- `OllamaBackend.list_models` -> `test_ollama_list_models_parsing`, `test_list_models_parses_missing_and_partial_fields`
- `OllamaBackend.test_connection` -> HTTP-error and timeout tests
- `OllamaBackend.chat`/payload sanitization -> reasoning-mode and option filtering tests
- `AppConfig.load/save` -> roundtrip and schema migration/rejection tests
- `GenerationParameters` -> reasoning mode and backend-option tests
- `chat_view` helpers -> five direct tests
- `ChatController` -> send/regenerate/save/edit/delete invalid-flow tests
- `ModelController` -> pull/push/delete/clone/create lifecycle tests
- `MainWindow.run_async`, `build_model_from_modelfile`, `open_template_viewer`, `_build_readonly_table_item`, `update_operation` -> direct tests
- `PluginManager` -> lifecycle/discovery/trust/security tests
- `CredentialStore`/config serialization -> API-key redaction test

## 31.15 Branch-symbol repair

Git compare remains the authoritative file-level delta:
- feature ahead 116
- feature behind 11
- 40 changed files in the comparison result

Verified changed active symbols/contracts:

| File | Main | Feature | Status |
|---|---|---|---|
| `locallama_gui/__init__.py` | `__version__ = 1.1.10` | `1.2.0` | CONTRACT_CHANGED |
| `locallama_gui/__main__.py` | relative `.app` import | absolute `locallama_gui.app` import | MODIFIED |
| `locallama_gui/app.py` | direct `MainWindow(config)` startup | first-run detection, temporary `refresh_backend` suppression, production-fix invocation, MyLoAI application name | IMPLEMENTATION_CHANGED |
| `locallama_gui/core/logging.py` | file + `StreamHandler` | file-only handler | IMPLEMENTATION_CHANGED |
| `pyproject.toml` | version 1.1.10 | version 1.2.0 | CONTRACT_CHANGED |
| `pyproject.toml` | one console script `locallama-gui` | adds `myloai` while retaining `locallama-gui` | CONTRACT_CHANGED |
| `pyproject.toml` | Ruff excludes `llm_studio`, `ollama_GUI` | additionally excludes `archive` | CONTRACT_CHANGED |
| `locallama_gui/ui/model_browser.py` | absent | `ModelRecommendation`, `CATALOG`, `ModelBrowserDialog` | ADDED |
| `locallama_gui/ui/setup_wizard.py` | absent | `FirstRunWizard` | ADDED |
| `locallama_gui/ui/production_fixes.py` | absent | production menu/document/theme/first-run functions | ADDED |

Packaging additions are listed individually in the preceding branch-difference section and are also indexed in the dependency companion.

No removed active application Python module was identified in the Git compare file list.

## 31.16 Documentation cross-check repair

Observed classifications:

| Claim area | Classification | Evidence |
|---|---|---|
| active package is `locallama_gui/` | IMPLEMENTED_AND_DOCUMENTED | README/docs + active imports |
| archive is excluded from Ruff on feature | IMPLEMENTED_AND_DOCUMENTED | `pyproject.toml` |
| `myloai` console entry exists | IMPLEMENTED_AND_DOCUMENTED | `pyproject.toml` |
| MyLoAI first-run setup exists | IMPLEMENTED_AND_DOCUMENTED | `app.py`, `setup_wizard.py` |
| plugin `memory_providers` registration | DOCUMENTATION_STALE / CONTRADICTORY where docs imply a registration method exists | context dictionary exists; no registration method |
| separate persistent retrieval memory | DOCUMENTED_NOT_IMPLEMENTED / NOT VERIFIED where described only as capability | no active retrieval implementation found |
| packaging payload excludes archive/tests | IMPLEMENTED_AND_DOCUMENTED | release validator + packaging docs |
| complete UI action behavior in all docs | UNKNOWN | source is authoritative; documentation claims require case-by-case verification |

## 31.17 Security/trust inventory repair

Actual security-relevant boundaries:
- provider API keys -> OS keyring
- config serialization -> API keys omitted
- config file -> attempted `0600`
- plugin discovery -> AST literal parsing before execution
- plugin enable -> trust check before dynamic import
- runtime plugin manifest -> revalidated after import
- plugin ID -> static/runtime equality check
- plugin removal -> filesystem unlink
- model/request content -> provider HTTP request
- user-selected files -> QFileDialog -> filesystem read/write
- dynamic JSON imports in agent import/export
- no active `subprocess` call was verified in application source
- no active shell execution was verified in application source

## 31.18 Call-path repair

### Startup
`locallama_gui.app.main`
-> environment defaults
-> first-run config path test
-> `AppConfig.load`
-> `configure_logging`
-> `QApplication`
-> temporarily suppress `MainWindow.refresh_backend` on first run
-> `MainWindow(config)`
-> restore original method
-> `apply_production_fixes`
-> `win.show`
-> `app.exec`

### First run
`apply_production_fixes(..., first_run=True)`
-> `QTimer.singleShot(250, ...)`
-> `FirstRunWizard.exec`
-> hardware recommendation
-> `AsyncTask` backend test
-> optional `StreamTask` model pull
-> config default-model persistence

### New chat
`MainWindow.new_chat`
-> `ChatSession`
-> optional user-editable system message
-> `ChatTab`
-> `_wire_chat_tab`
-> tab insertion

### Send
`ChatController.send_message`
-> read composer
-> append user `ChatMessage`
-> set title
-> render
-> `window.generate_for_tab`
-> `MainWindow._generate`

### Generation
`_generate`
-> active profile
-> backend factory
-> model selection
-> internal system message
-> session messages
-> plugin interceptors
-> generation options
-> request preview
-> `StreamTask`
-> backend async stream
-> token/error/completion callbacks

### Stop
`stop_generation`
-> `StreamTask.cancel`
-> clear owner/current stream
-> reset tab/status

### Completion
`_stream_done`
-> clear active stream state
-> `SessionManager.save`
-> `refresh_sessions`
-> render

### Model pull/delete/create/clone
UI/controller
-> backend factory
-> `StreamTask` for streamed operations or `run_async` for non-streaming
-> operation parser/UI
-> refresh backend

### Plugin load
`PluginManager.load_enabled`
-> static manifest
-> `enable`
-> trust check
-> dynamic import
-> instantiate
-> runtime manifest validation
-> `activate(context)`

### Shutdown
`MainWindow.closeEvent`
-> restore stdout/stderr
-> remove Qt logging handler
-> cancel current/active workers
-> save geometry/state
-> `AppConfig.save`
-> Qt superclass close

## 31.19 Exact test inventory index

The companion test artifact contains these 49 exact tests:

`tests/test_backend_and_config.py`
- `test_ollama_list_models_parsing`
- `test_config_save_load_roundtrip`

`tests/test_chat_view.py`
- `test_scroll_restore_policy_near_bottom_pins`
- `test_scroll_restore_policy_scrolled_up_preserves_position`
- `test_visible_messages_exclude_internal_system`
- `test_assistant_label_prefers_message_model_then_fallback_active_model`
- `test_request_redaction_only_for_internal_system_prompt`

`tests/test_config_roundtrip.py`
- `test_config_load_save_roundtrip`
- `test_reasoning_mode_persists_in_config`
- `test_reasoning_mode_is_exclusive_via_single_enum`
- `test_legacy_generation_parameters_load_but_do_not_emit_strict_backend_options`

`tests/test_config_schema.py`
- `test_legacy_unversioned_config_migrates_to_current_schema`
- `test_future_config_schema_is_rejected`

`tests/test_controller_invalid_flows.py`
- `test_chat_controller_invalid_prompt_no_crash`
- `test_model_controller_invalid_model_name_no_crash`

`tests/test_controllers.py`
- `test_send_and_regenerate_regression`
- `test_save_current_regression`
- `test_edit_message_uses_visible_index_and_skips_internal_system`
- `test_delete_message_uses_visible_index_and_skips_internal_system`
- `test_model_create_delegates_to_editor`
- `test_plugin_reload_regression`

`tests/test_diagnostics.py`
- `test_logging_record_uses_structured_diagnostics_format`
- `test_line_buffered_stream_emits_complete_lines_and_flushes_partial_text`
- `test_append_output_is_cursor_safe`
- `test_operation_stream_parser_assembles_partial_json_and_collapses_statuses`
- `test_operation_update_refreshes_live_status_and_progress_without_history_spam`

`tests/test_model_controller_delete.py`
- `test_delete_model_without_selection_shows_info`
- `test_delete_model_confirmed_runs_async`

`tests/test_model_metadata_table_flags.py`
- `test_model_metadata_table_items_are_non_editable_and_selectable`

`tests/test_model_operations.py`
- `test_run_async_routes_lifecycle_to_operations_before_dialog`
- `test_pull_stream_collapses_repeated_status_and_updates_progress`
- `test_pull_partial_chunks_do_not_create_corrupt_history`
- `test_stream_error_updates_operations_before_dialog`
- `test_clone_strips_names_and_delete_contract_remains_public`
- `test_create_stream_uses_operations_without_console_output`
- `test_templates_require_a_selected_model`
- `test_templates_route_lifecycle_to_operations_before_dialog`

`tests/test_ollama_backend.py`
- `test_list_models_parses_missing_and_partial_fields`
- `test_test_connection_returns_disconnected_on_http_error`
- `test_test_connection_returns_disconnected_on_timeout`
- `test_chat_payload_emits_only_selected_reasoning_mode`
- `test_sanitize_options_preserves_supported_and_filters_invalid_and_stop_fragments`
- `test_sanitize_request_fields_only_forwards_supported_top_level_fields`
- `test_stream_endpoint_raises_for_successful_http_response_with_error_payload`

`tests/test_plugin_lifecycle.py`
- `test_plugin_lifecycle_discover_validate_trust_enable_disable_reload_untrust_remove`
- `test_plugin_discovery_reports_manifest_validation_error`

`tests/test_security_boundaries.py`
- `test_api_key_is_not_serialized_to_config`
- `test_plugin_discovery_does_not_execute_module_code`
- `test_untrusted_plugin_is_rejected_before_import`

## 31.20 Repair conclusion

The previous census's two largest source gaps (`main_window.py`, `dialogs.py`) have now been retrieved to their end-of-file boundaries. The previous 13 test files are now individually inventoried. The feature branch's production additions are source-verified.

The remaining limitation is not application-source retrieval. It is the ability of the connected GitHub interface to expose machine-readable AST line offsets and line counts for every non-Python tracked blob without reconstructing a local Git checkout. Therefore the census distinguishes:
- source structure that is directly verified;
- tree metadata that is directly verified;
- exact line-offset data not exposed by the source connector.

No implementation is inferred to fill those missing offsets.

# 32. AUTOMATED RECONCILIATION / FINAL COMPLETENESS GATE

## 32.1 Independent repository reconciliation

Independent Git tree reconciliation:
- active tracked blobs outside `archive/`: **106**
- Python files: **44**
- test files: **13**
- packaging/release files: **23**
- GitHub metadata/workflow/template files: **9**
- recorded bytes: **420,262**
- archive excluded from active census.

The feature/main Git comparison independently reports **40 changed files**, matching the branch-difference inventory.

## 32.2 Reconciliation results

| Check | Result |
|---|---|
| active tracked-file set | VERIFIED |
| archive exclusion | VERIFIED |
| Python-file set | VERIFIED |
| test-file set | VERIFIED |
| package initializer set | VERIFIED |
| main_window end boundary | VERIFIED at line 1,050 |
| dialogs end boundary | VERIFIED at line 600 |
| exact 49 test functions | VERIFIED from retrieved source |
| plugin memory registration API absence | VERIFIED in retrieved `core/managers.py` |
| Ollama endpoint set | VERIFIED |
| OpenAI-compatible endpoint set | VERIFIED |
| console-script set | VERIFIED from feature `pyproject.toml` |
| feature/main file diff | VERIFIED by Git compare |
| complete per-symbol caller graph | PARTIAL for dynamically resolved/UI callback relationships |
| exact line offsets for every record | PARTIAL |
| dynamic runtime behavior | UNVERIFIED unless directly visible in source |
| generated code | NOT PRESENT in active tracked tree outside excluded archive |
| parser/runtime instrumentation | NOT PERFORMED |

## 32.3 Missing/unresolved records

The following remain explicitly unresolved rather than silently treated as complete:
- exact line offsets for every inventory record where the connector did not provide AST coordinates;
- exact line counts for arbitrary Markdown/YAML/SVG/shell/package blobs not individually retrieved and counted;
- runtime-only callback dispatch where static code cannot determine the receiver;
- dynamic plugin behavior beyond the sample plugin and source-visible hook contracts;
- behavior of external Ollama/OpenAI-compatible services outside the application's request/response handling;
- actual GUI thread affinity at runtime;
- exact exception propagation for code paths not statically represented by explicit handlers.

## 32.4 No duplicate-record finding

No duplicate tracked-file records were introduced. The repair pass is additive and keyed to repository-relative path/symbol identity. Existing file census rows were preserved.

## 32.5 Evidence standard

The final document does **not** use `COMPLETE` for categories where exact machine-level enumeration remains impossible from the connector interface.

Where source was retrieved, the evidence is `STATIC_VERIFIED`.

Where a relationship depends on runtime resolution, it remains `STATIC_INFERRED`, `UNKNOWN`, or `UNVERIFIED`.

# 33. FINAL VERIFICATION STATEMENT

| Category | Required | Enumerated | Verified | Missing | Status |
|---|---:|---:|---:|---:|---|
| tracked files outside archive | 106 | 106 | 106 | 0 | VERIFIED |
| Python modules/files | 44 | 44 | 44 | 0 | VERIFIED |
| individual imports | every active `.py` | source-retrieved set | source statements | dynamic/runtime resolution | PARTIAL |
| classes | every active `.py` | known active set | source-retrieved | AST offset metadata | PARTIAL |
| methods | every class | source-retrieved set | source | AST offset metadata | PARTIAL |
| functions/nested functions | every active `.py` | source-retrieved set | source | AST offset metadata | PARTIAL |
| properties | every active `.py` | known set | source | Qt/property runtime mechanisms | PARTIAL |
| dataclasses | every active `.py` | 14 | 14 | 0 | VERIFIED |
| dataclass fields | every dataclass | all listed fields | source | field-option metadata not emitted by connector | VERIFIED/PARTIAL |
| Protocols | every active `.py` | 6 known | source | structural runtime uses | PARTIAL |
| ABCs | every active `.py` | 1 known | source | 0 | VERIFIED |
| constants/contracts | all contract literals | major active contracts | source | every incidental magic literal | PARTIAL |
| instance attributes | every `self.*` mutation | major application classes | source | complete AST write-site indexing | PARTIAL |
| environment references | every active file | verified application vars + shell references | source | some packaging text not individually scanned | PARTIAL |
| filesystem references | every active file | major application operations | source | arbitrary docs/package literals | PARTIAL |
| HTTP requests | every network request | 10 endpoint operations | source | runtime server behavior | VERIFIED |
| CLI routes | every executable route | 7 primary routes | source | platform package manager dispatch | PARTIAL |
| plugin hooks | every hook | all source-visible hooks | source | arbitrary third-party plugin behavior | VERIFIED/PARTIAL |
| worker boundaries | every active worker | 10 execution boundaries | source | runtime thread scheduling | VERIFIED/PARTIAL |
| signals | every custom signal | 9 | source | external Qt signal inventory | PARTIAL |
| slots/decorators | every slot | no explicit `@Slot` found | source | inherited Qt slots | VERIFIED/PARTIAL |
| connections | every active `.connect()` | source-visible connections enumerated | source | generated/runtime Qt connections | PARTIAL |
| persistence operations | every active operation | major persistence set enumerated | source | incidental logging internals | PARTIAL |
| tests | every test function | 49 | source | 0 test functions | VERIFIED |
| reverse test coverage | production symbol -> tests | major tested symbols | source | untested-symbol proof requires full AST graph | PARTIAL |
| branch symbol differences | changed active source | changed source contracts enumerated | Git + source | exact symbol diff for all docs/package literals | PARTIAL |
| call graph | required workflows | startup/chat/model/plugin/shutdown | source | fully dynamic callback paths | PARTIAL |
| state ownership | important mutable state | source-visible state | source | dynamic Qt-owned state | PARTIAL |
| data flow | required domain objects | source-visible paths | source | external server internals | VERIFIED/PARTIAL |
| trust/security boundaries | actual code | source-visible boundaries | source | external OS internals | VERIFIED |
| packaging/release | every active packaging file | 23 packaging/release files indexed | tree + source subset | every non-Python literal line | PARTIAL |
| documentation cross-check | implementation claims | major documented contracts | source/docs | exhaustive prose comparison | PARTIAL |
| independent reconciliation | second pass | performed | tree + source | connector runtime limits | VERIFIED/PARTIAL |

### Explicit answers

**1. Which sections of the previous census were truncated?**  
`main_window.py`, `dialogs.py`, several test files, and several newly added production UI files were explicitly marked source-unretrieved or partially retrieved. Those sources have now been retrieved. The old sections 3, 5, 6, 13, 14, 19, and 25 were therefore materially under-granular.

**2. Which were merely summarized?**  
Imports, methods, Qt connections, workers, persistence, plugin hooks, tests, state, call paths, and branch changes were summarized at subsystem/file level rather than as individual records.

**3. Which were incorrectly marked complete?**  
The prior file-tree census was correctly complete at tree level. The prior claims for source-level imports, symbols, Qt connections, tests, and branch-symbol relationships were not sufficient for the requested forensic standard and are now classified PARTIAL unless individually source-verified.

**4. What was added during this repair?**  
- source verification of the previously incomplete Python files;
- complete 1,050-line `main_window.py` boundary;
- complete 600-line `dialogs.py` boundary;
- exact 49-test-function inventory;
- ModelBrowser/FirstRun/production-fix symbol and state records;
- nested function records in `ParameterDialog`;
- individual Qt connection records;
- worker creation boundary records;
- individual persistence operation records;
- plugin hook lifecycle records;
- branch source-contract comparison;
- independent reconciliation section and final completeness gate;
- companion symbol/dependency/test inventories.

**5. What remains impossible to determine statically?**  
Runtime thread affinity, runtime-generated Qt object relationships, arbitrary third-party plugin behavior, external provider behavior, and dynamically resolved callback consumers cannot be fully established by source inspection alone.

**6. Which repository files were not inspected, if any?**  
No active Python file outside `archive/` remains source-unretrieved in this pass. Non-Python tracked files were verified for tree identity/size/mode; not every non-Python blob was individually opened and line-parsed.

**7. What evidence supports the final completeness claim?**  
The Git recursive tree is non-truncated and contains 106 active tracked blobs. Git compare independently reports 40 changed files. Every active Python file has now been retrieved or source-verified, including the two formerly truncated large UI modules. All 13 test files were retrieved and yield exactly 49 test functions. The remaining PARTIAL classifications are explicitly tied to connector limitations or inherently dynamic behavior rather than hidden gaps.

**FINAL STATUS: PARTIAL FOR FULL MACHINE-LEVEL FORENSIC GRANULARITY; SOURCE-GROUNDED ACTIVE-PYTHON CENSUS REPAIRED.**

This is intentionally not labeled globally COMPLETE because exact line-offset extraction for every inventory record and exhaustive line parsing of every non-Python tracked blob were not independently established.
