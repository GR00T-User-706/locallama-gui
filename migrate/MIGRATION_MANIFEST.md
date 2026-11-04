# MyLoAI Control Center Migration Manifest

## Purpose

This manifest inventories the files staged for migration from the historical `GR00T-User-706/locallama-gui` repository into a clean MyLoAI repository.

- **Source repository:** `GR00T-User-706/locallama-gui`
- **Source branch:** `main`
- **Application version at inspection:** `1.2.12`
- **Application package:** `myloai`
- **Python import namespace:** `locallama_gui` (retained for compatibility)
- **Product display name:** MyLoAI Control Center
- **Staging root:** `migrate/`

The source repository is preserved. Nothing in the original application tree was moved, renamed, deleted, or rewritten for this migration.

## Migration status

**105 files copied and verified.**

- 105 source files were copied to the same relative paths under `migrate/`.
- All 105 copied files have Git blob identifiers identical to their source files. This verifies byte-for-byte equality at the Git blob level.
- `migrate/README.md` is a new staging-area explanation, not a source-file copy.
- Two active binary image assets could not be copied by the text-only repository file operation. Their exact source paths, blob identifiers, and sizes are listed below.
- The icon generator source was copied. It can regenerate both missing assets when run in an environment with Pillow installed.
- No application tests or platform builds were run. This staging copy is not yet a verified standalone repository or release.

## Required files copied

Each row identifies the original source path, the destination path, and the original Git blob SHA. The destination has been checked against the source and has the same blob SHA.

| Source path | Staged path | Status | Source blob SHA |
|---|---|---|---|
| `.github/ISSUE_TEMPLATE/bug_report.yml` | `migrate/.github/ISSUE_TEMPLATE/bug_report.yml` | Copied; exact Git blob match | `8994fc426e0ca71118f4937b0c7d73b05708f4de` |
| `.github/ISSUE_TEMPLATE/config.yml` | `migrate/.github/ISSUE_TEMPLATE/config.yml` | Copied; exact Git blob match | `0d7dd1276c49c4c94a5e7d0f4ed4ff6781266b88` |
| `.github/ISSUE_TEMPLATE/feature_request.yml` | `migrate/.github/ISSUE_TEMPLATE/feature_request.yml` | Copied; exact Git blob match | `5ec87b7a687069402e153bf23dd21996e381f562` |
| `.github/agents/repo-code-risk-reviewer.agent.md` | `migrate/.github/agents/repo-code-risk-reviewer.agent.md` | Copied; exact Git blob match | `92f117275e80cd1740a42448165ab71b110d20ef` |
| `.github/prompts/repo-code-risk-reviewer.prompt.md` | `migrate/.github/prompts/repo-code-risk-reviewer.prompt.md` | Copied; exact Git blob match | `6a46292a80dce4bdca1395c316e048d0a4c2805f` |
| `.github/workflows/active-ci.yml` | `migrate/.github/workflows/active-ci.yml` | Copied; exact Git blob match | `d23fac0fc968bf6d661a10a4cafffe98fa0f8ff0` |
| `.github/workflows/ci.yml` | `migrate/.github/workflows/ci.yml` | Copied; exact Git blob match | `a4f2a6b3d0286801324d351497f70877f7b29bd7` |
| `.github/workflows/release-packaging.yml` | `migrate/.github/workflows/release-packaging.yml` | Copied; exact Git blob match | `bbe5c63ea56eabe137007c8d8e2216b4db279b87` |
| `.gitignore` | `migrate/.gitignore` | Copied; exact Git blob match | `ee1ce40cdfd49bc1707571c3a75896ad7ff5ec46` |
| `.semver-forge.toml` | `migrate/.semver-forge.toml` | Copied; exact Git blob match | `7ed35cc345468cd8f3523fa3ac7ca57b0903f9c1` |
| `AGENTS.md` | `migrate/AGENTS.md` | Copied; exact Git blob match | `f22ec3f789456891c2d3c8cd1938896215c6d76e` |
| `CHANGELOG.md` | `migrate/CHANGELOG.md` | Copied; exact Git blob match | `804506f7e0def1395ec9600d964141bd70da91a1` |
| `CODE_OF_CONDUCT.md` | `migrate/CODE_OF_CONDUCT.md` | Copied; exact Git blob match | `d682a8eb7cd2823ff8f023417cff6e42bc879267` |
| `CONTRIBUTING.md` | `migrate/CONTRIBUTING.md` | Copied; exact Git blob match | `461ba5a0d5a25ee99232d07e07fa85b919aeab8f` |
| `LICENSE` | `migrate/LICENSE` | Copied; exact Git blob match | `b9d29b16ba83a97fe7c191fdf7f79693c77cf82a` |
| `SECURITY.md` | `migrate/SECURITY.md` | Copied; exact Git blob match | `6fc3fb1dfe60681bafb1391219d2446260d77195` |
| `VERSION` | `migrate/VERSION` | Copied; exact Git blob match | `f2ae0b4a2ced5b12ea5298962a7684a799e2e264` |
| `docs/ARCHITECTURE.md` | `migrate/docs/ARCHITECTURE.md` | Copied; exact Git blob match | `b903700b50c32258119c845cd28df2e5297c0d48` |
| `docs/BUGS/KNOWN_BUGS.md` | `migrate/docs/BUGS/KNOWN_BUGS.md` | Copied; exact Git blob match | `4dd2574db1555bd148b337984f40dc39d2b0ded1` |
| `docs/BUILDING.md` | `migrate/docs/BUILDING.md` | Copied; exact Git blob match | `af42f4fe6788643b3a916710c42ad500bb7431f3` |
| `docs/CONFIG_SCHEMA.md` | `migrate/docs/CONFIG_SCHEMA.md` | Copied; exact Git blob match | `f2fd348d7dcb0dc6c745430f4221bd732fd3f2a2` |
| `docs/FEATURE_MATRIX.md` | `migrate/docs/FEATURE_MATRIX.md` | Copied; exact Git blob match | `37cabb00a4e5ac1dce44cda441fbef61560406ae` |
| `docs/LAUNCHING.md` | `migrate/docs/LAUNCHING.md` | Copied; exact Git blob match | `69bb7cc5734c50eb46d0931e28a952bb01a14e37` |
| `docs/MENU_MAP.md` | `migrate/docs/MENU_MAP.md` | Copied; exact Git blob match | `e4a2bef067f92f194764f6c9fe37da909e03d8ee` |
| `docs/MODULE_INTAKE_POLICY.md` | `migrate/docs/MODULE_INTAKE_POLICY.md` | Copied; exact Git blob match | `4278249352d43d01f9ee360e37e964cc88e72d93` |
| `docs/PARAMETERS.md` | `migrate/docs/PARAMETERS.md` | Copied; exact Git blob match | `1204a48bcb923346abfd982635ef09f306354201` |
| `docs/PLUGIN_SDK.md` | `migrate/docs/PLUGIN_SDK.md` | Copied; exact Git blob match | `997c572df85989448728372c8dc7d8d9b494b563` |
| `docs/PRODUCTION_CODE_MAP.md` | `migrate/docs/PRODUCTION_CODE_MAP.md` | Copied; exact Git blob match | `81019763d5641501af808b46b95548701bfb7f20` |
| `docs/PROJECT_STANDARDS.md` | `migrate/docs/PROJECT_STANDARDS.md` | Copied; exact Git blob match | `09a8bd208665df97f39c9df5a5ba967ac2d56bf7` |
| `docs/QA_CHECKLIST.md` | `migrate/docs/QA_CHECKLIST.md` | Copied; exact Git blob match | `d2acc965520de6a42e60cac84e6dcd0205680d43` |
| `docs/REPO_ANALYSIS.md` | `migrate/docs/REPO_ANALYSIS.md` | Copied; exact Git blob match | `52ed5ef8b46a8d913d796a8ef0c76557cd20f425` |
| `docs/VERSIONING.md` | `migrate/docs/VERSIONING.md` | Copied; exact Git blob match | `88c8ead46d7efd72c5709a4a8ef4bb74e93be6fd` |
| `locallama_gui/__init__.py` | `migrate/locallama_gui/__init__.py` | Copied; exact Git blob match | `edfbe323110c60f04cf3e055b7a1e3f2ddd6e73e` |
| `locallama_gui/__main__.py` | `migrate/locallama_gui/__main__.py` | Copied; exact Git blob match | `57f6dc90aec186ce220d37a2590d5385e64d8a56` |
| `locallama_gui/app.py` | `migrate/locallama_gui/app.py` | Copied; exact Git blob match | `ee95be84c9f461fdf11e3ab0fd23df8b6261c6ac` |
| `locallama_gui/backends/__init__.py` | `migrate/locallama_gui/backends/__init__.py` | Copied; exact Git blob match | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `locallama_gui/backends/base.py` | `migrate/locallama_gui/backends/base.py` | Copied; exact Git blob match | `aeffc1b15c6f0e3423b8f19cf5d482707ed22c24` |
| `locallama_gui/backends/manager.py` | `migrate/locallama_gui/backends/manager.py` | Copied; exact Git blob match | `0705d1d2ef742968512dd4ad486f1de19c107e0b` |
| `locallama_gui/backends/ollama.py` | `migrate/locallama_gui/backends/ollama.py` | Copied; exact Git blob match | `38cb88b73d7b681a42acba1af4df1d25b6212cd9` |
| `locallama_gui/backends/openai.py` | `migrate/locallama_gui/backends/openai.py` | Copied; exact Git blob match | `5b16668da9c66c2fa9ff7af5a78170054ebf3b72` |
| `locallama_gui/core/__init__.py` | `migrate/locallama_gui/core/__init__.py` | Copied; exact Git blob match | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `locallama_gui/core/config.py` | `migrate/locallama_gui/core/config.py` | Copied; exact Git blob match | `2d6283ec89786f509fa5089c706c422cafb365dd` |
| `locallama_gui/core/domain.py` | `migrate/locallama_gui/core/domain.py` | Copied; exact Git blob match | `7ffc1d0455fbfb85d3b56e1668b4838d9f08235e` |
| `locallama_gui/core/logging.py` | `migrate/locallama_gui/core/logging.py` | Copied; exact Git blob match | `c8a6481c0de5cb7d5dc93c19f5cb02dce7aef123` |
| `locallama_gui/core/managers.py` | `migrate/locallama_gui/core/managers.py` | Copied; exact Git blob match | `25d7cbe852cfc3d45fec84a72b1383216e5fc29f` |
| `locallama_gui/plugins/__init__.py` | `migrate/locallama_gui/plugins/__init__.py` | Copied; exact Git blob match | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `locallama_gui/ui/__init__.py` | `migrate/locallama_gui/ui/__init__.py` | Copied; exact Git blob match | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `locallama_gui/ui/chat_view.py` | `migrate/locallama_gui/ui/chat_view.py` | Copied; exact Git blob match | `2c1e2ca6d82e77f06ae4b8cd9b61e261630dca55` |
| `locallama_gui/ui/controllers/__init__.py` | `migrate/locallama_gui/ui/controllers/__init__.py` | Copied; exact Git blob match | `9edfe16013ed5933e063923e497dd081e9f6bad3` |
| `locallama_gui/ui/controllers/chat_controller.py` | `migrate/locallama_gui/ui/controllers/chat_controller.py` | Copied; exact Git blob match | `7e1a65f991e56d2b2be8e5c0f8ef1a9037842375` |
| `locallama_gui/ui/controllers/model_controller.py` | `migrate/locallama_gui/ui/controllers/model_controller.py` | Copied; exact Git blob match | `450118239144107578bf661df589d8fd4f6ac777` |
| `locallama_gui/ui/controllers/plugin_controller.py` | `migrate/locallama_gui/ui/controllers/plugin_controller.py` | Copied; exact Git blob match | `83a35392322f4ceb60f59cd0f62b91f3330104b3` |
| `locallama_gui/ui/diagnostics.py` | `migrate/locallama_gui/ui/diagnostics.py` | Copied; exact Git blob match | `89eaf383fc4eca32e32dbedbf5a0006170c0a521` |
| `locallama_gui/ui/dialogs.py` | `migrate/locallama_gui/ui/dialogs.py` | Copied; exact Git blob match | `b33fc7733ea817f051046b6122dceff3dc83ecf8` |
| `locallama_gui/ui/main_window.py` | `migrate/locallama_gui/ui/main_window.py` | Copied; exact Git blob match | `bfbb135264879c51a87cfd5d318296cfa6ca9f65` |
| `locallama_gui/ui/model_browser.py` | `migrate/locallama_gui/ui/model_browser.py` | Copied; exact Git blob match | `3ec2b13683d49d7a95fed5e8ae5ac606d478a473` |
| `locallama_gui/ui/production_fixes.py` | `migrate/locallama_gui/ui/production_fixes.py` | Copied; exact Git blob match | `cfe4ff1fad49b2d85b26124aec8f83277766bf18` |
| `locallama_gui/ui/setup_wizard.py` | `migrate/locallama_gui/ui/setup_wizard.py` | Copied; exact Git blob match | `e072ff7fe99261a83438e47822351a837ee6b6b2` |
| `locallama_gui/ui/theme.py` | `migrate/locallama_gui/ui/theme.py` | Copied; exact Git blob match | `a867a720242616fb37693221d973afb3985220e8` |
| `locallama_gui/ui/workers.py` | `migrate/locallama_gui/ui/workers.py` | Copied; exact Git blob match | `55cec059d90a19fe878284b18c2a5c29f473bc19` |
| `packaging/README.md` | `migrate/packaging/README.md` | Copied; exact Git blob match | `045731a5f703adb451f2a9dfb49d783022742d45` |
| `packaging/RELEASE_BUILD_SPEC.md` | `migrate/packaging/RELEASE_BUILD_SPEC.md` | Copied; exact Git blob match | `fb5b024f38d46e9e8a038e1a34079a63837be93e` |
| `packaging/RELEASE_PAYLOAD.md` | `migrate/packaging/RELEASE_PAYLOAD.md` | Copied; exact Git blob match | `4ff84de72996c021d2b47d716c96273de32afd04` |
| `packaging/USER_MANUAL.md` | `migrate/packaging/USER_MANUAL.md` | Copied; exact Git blob match | `4350896181b23b32f4fbec84a736709c3fe2c61a` |
| `packaging/assets/generate_myloai_icon.py` | `migrate/packaging/assets/generate_myloai_icon.py` | Copied; exact Git blob match | `50ab8d05cdda05c3a54b7e8b59227c74725c6784` |
| `packaging/build-linux.sh` | `migrate/packaging/build-linux.sh` | Copied; exact Git blob match | `cb88a7baa88338b6d379426c304969e61acc267c` |
| `packaging/check-release-payload.py` | `migrate/packaging/check-release-payload.py` | Copied; exact Git blob match | `c566982edb948a2921b0a647fff99a3639a2593d` |
| `packaging/linux/PKGBUILD` | `migrate/packaging/linux/PKGBUILD` | Copied; exact Git blob match | `f084866be8ce7c1f7e2d857eb01cf11b1a6aedc0` |
| `packaging/linux/appimage/README.md` | `migrate/packaging/linux/appimage/README.md` | Copied; exact Git blob match | `7849f3fa88b49ae88ef93dd6c14731b8b904c0e3` |
| `packaging/linux/appimage/build-appimage.sh` | `migrate/packaging/linux/appimage/build-appimage.sh` | Copied; exact Git blob match | `0cfc934753bb9cb4c8cfb40e1efa65c00ef36883` |
| `packaging/linux/appimage/myloai.svg` | `migrate/packaging/linux/appimage/myloai.svg` | Copied; exact Git blob match | `574d3465b2cdd6e610df4a46af40557e742e5f8c` |
| `packaging/linux/com.github.gr00t-user-706.locallama-gui.desktop` | `migrate/packaging/linux/com.github.gr00t-user-706.locallama-gui.desktop` | Copied; exact Git blob match | `e59f966dd6252a466007b8247464339a3be45a33` |
| `packaging/linux/debian/README.Debian` | `migrate/packaging/linux/debian/README.Debian` | Copied; exact Git blob match | `ff9d733b73f2422355606f36dc17666c115540ae` |
| `packaging/linux/debian/build-deb.sh` | `migrate/packaging/linux/debian/build-deb.sh` | Copied; exact Git blob match | `64fe1b45c6be6ae09385689989c0e29671e97cfe` |
| `packaging/linux/icons/com.github.gr00t-user-706.locallama-gui.svg` | `migrate/packaging/linux/icons/com.github.gr00t-user-706.locallama-gui.svg` | Copied; exact Git blob match | `b53a0fd2c026559e21d80e76fdf8667c52cb5ff9` |
| `packaging/linux/install-myloai.sh` | `migrate/packaging/linux/install-myloai.sh` | Copied; exact Git blob match | `4249888148abc8b49cb048000d6478047d587dbe` |
| `packaging/linux/myloai` | `migrate/packaging/linux/myloai` | Copied; exact Git blob match | `66d555fc3322726fa1e706c1d575ddb21805f6aa` |
| `packaging/linux/myloai.1` | `migrate/packaging/linux/myloai.1` | Copied; exact Git blob match | `324ccfdb5a496311a091c692589c80a4b56d407a` |
| `packaging/linux/myloai.desktop` | `migrate/packaging/linux/myloai.desktop` | Copied; exact Git blob match | `0c6cac560c6453184048fc310823ccb105b1c31f` |
| `packaging/macos/README.md` | `migrate/packaging/macos/README.md` | Copied; exact Git blob match | `39dfe743d39970e23fdc06bd93589ec912d782e0` |
| `packaging/macos/build-dmg.sh` | `migrate/packaging/macos/build-dmg.sh` | Copied; exact Git blob match | `ad51545d765b70392ed94f40554f22f3c1e5edf6` |
| `packaging/myloai-package.yaml` | `migrate/packaging/myloai-package.yaml` | Copied; exact Git blob match | `c70208d0b68e4d79385376abd78309dd4b07f6ab` |
| `packaging/pyinstaller/myloai.spec` | `migrate/packaging/pyinstaller/myloai.spec` | Copied; exact Git blob match | `8b655183018d34287082ec1b2f39df8219962153` |
| `packaging/windows/MyLoAI.iss` | `migrate/packaging/windows/MyLoAI.iss` | Copied; exact Git blob match | `795f1ff1f82d88d7fa2048d9ee730f901669a9ec` |
| `packaging/windows/README.md` | `migrate/packaging/windows/README.md` | Copied; exact Git blob match | `d64d428e09af8a0bb00f5751787b07a8bcdfe514` |
| `packaging/windows/build-installer.ps1` | `migrate/packaging/windows/build-installer.ps1` | Copied; exact Git blob match | `dca3319b7740d937c3fcedc239e4d903aa924bd0` |
| `plugins/sample_plugin.py` | `migrate/plugins/sample_plugin.py` | Copied; exact Git blob match | `6b2c5f905974eef8bb304b3dbe2f0ff437a48219` |
| `pyproject.toml` | `migrate/pyproject.toml` | Copied; exact Git blob match | `6606ccf96961d7320bec08ac50a80c7dc5c3db79` |
| `requirements.txt` | `migrate/requirements.txt` | Copied; exact Git blob match | `1518db404940cc7de5ff5a8df83adbca70a3f5c3` |
| `scripts/install-desktop-entry` | `migrate/scripts/install-desktop-entry` | Copied; exact Git blob match | `a52503241ff539b95c1f8710d2905040f4332a5b` |
| `scripts/install-launcher` | `migrate/scripts/install-launcher` | Copied; exact Git blob match | `1beaa0f0594bf866c2c46ccaf41ba69e0ffe1e01` |
| `tests/test_backend_and_config.py` | `migrate/tests/test_backend_and_config.py` | Copied; exact Git blob match | `d02b918ddaa0a6e60dca6179bffe4ae93408f6f5` |
| `tests/test_chat_payloads.py` | `migrate/tests/test_chat_payloads.py` | Copied; exact Git blob match | `4de8b58586775f98c7827e4f03c279e51b1bf1a0` |
| `tests/test_chat_view.py` | `migrate/tests/test_chat_view.py` | Copied; exact Git blob match | `e63cc45600ebdb1259f87c5aad8a809b952276b7` |
| `tests/test_config_roundtrip.py` | `migrate/tests/test_config_roundtrip.py` | Copied; exact Git blob match | `4a36944471c53e6c007641c1240514bc5c744b37` |
| `tests/test_config_schema.py` | `migrate/tests/test_config_schema.py` | Copied; exact Git blob match | `ed8545caac2276c56c33a324e84a52093ec0e74d` |
| `tests/test_controller_invalid_flows.py` | `migrate/tests/test_controller_invalid_flows.py` | Copied; exact Git blob match | `719bcb76790b2b7839c4fc2f7d3a0986761329cc` |
| `tests/test_controllers.py` | `migrate/tests/test_controllers.py` | Copied; exact Git blob match | `1e817b7ba837208fed5beaa5f0d2071f6d7d4f40` |
| `tests/test_diagnostics.py` | `migrate/tests/test_diagnostics.py` | Copied; exact Git blob match | `1fe952f4758384ee3cbf5cddf8f6dfe0fb07b88e` |
| `tests/test_model_controller_delete.py` | `migrate/tests/test_model_controller_delete.py` | Copied; exact Git blob match | `6791b6579b3213dce5c380ad10b3bb8a31cf6982` |
| `tests/test_model_metadata_table_flags.py` | `migrate/tests/test_model_metadata_table_flags.py` | Copied; exact Git blob match | `4f077f6e2e04c07c54e9a6eb4ac95489142619c6` |
| `tests/test_model_operations.py` | `migrate/tests/test_model_operations.py` | Copied; exact Git blob match | `d1ce102720fd7b0725e6690ff6b1a57832bc41c0` |
| `tests/test_ollama_backend.py` | `migrate/tests/test_ollama_backend.py` | Copied; exact Git blob match | `3ea3895275eb95d9363080a37dc639964a090528` |
| `tests/test_plugin_lifecycle.py` | `migrate/tests/test_plugin_lifecycle.py` | Copied; exact Git blob match | `0e63ba1f3c04c69c3459c2cb30e0143e93e563fb` |
| `tests/test_security_boundaries.py` | `migrate/tests/test_security_boundaries.py` | Copied; exact Git blob match | `8799c72efae846e7835c0a9ddf3a8380f3f6d278` |

## Required binary assets not copied

The GitHub file-writing interface used for this staging operation accepts UTF-8 text, not binary file content. These assets therefore remain only in the original source tree.

| Source path | Size | Source blob SHA | Required recovery |
|---|---:|---|---|
| `packaging/assets/MyLoAI.ico` | 36991 bytes | `21dd21a9d35a91dad9a17a556c31842081a6f1b2` | Retrieve the original binary or regenerate with `migrate/packaging/assets/generate_myloai_icon.py` (requires Pillow). |
| `packaging/assets/MyLoAI.png` | 15944 bytes | `1380766773d945e723a1f12995322b673547f822` | Retrieve the original binary or regenerate with `migrate/packaging/assets/generate_myloai_icon.py` (requires Pillow). |

These assets are referenced by the packaging/icon workflow. The Windows PyInstaller build expects `packaging/assets/MyLoAI.ico`; the PNG is the source/preview output generated by the icon script. Until the assets are restored or regenerated, the staging tree is not complete for all platform packaging workflows.

### Regenerating the assets

From the future repository root, after installing Pillow:

```bash
python packaging/assets/generate_myloai_icon.py
```

The script writes `packaging/assets/MyLoAI.png` and `packaging/assets/MyLoAI.ico`. This recreates the artwork from the checked-in generator, not necessarily the exact original binary bytes.

## Deliberately excluded material

These items were not copied because they are not required to build, install, test, or operate the current application. They remain preserved in the historical source repository.

| Source path/pattern | Reason |
|---|---|
| `archive/**` | Historical/legacy implementations and retired experiments. Not part of the active `locallama_gui` runtime or current production payload. |
| `docs/API_Docs/**` | Historical forensic censuses, duplicate codebase mappings, and audit reports rather than current application requirements. |
| `docs/deep-research-report*.md` | Research notes, not current runtime, build, or user documentation. |
| `docs/STATE_OF_REPO.md` | Repository-state snapshot; not a build or runtime dependency. |
| `docs/FUNCTIONALITY_AUDIT.md` | Historical audit snapshot. Current feature contract is carried by `docs/FEATURE_MATRIX.md`. |
| `docs/UI_ACTION_AUDIT.md` | Audit snapshot; current UI contract is carried by the feature matrix and menu map. |
| `docs/qa/WINDOWS-VM-2026-09-09.md` | Dated test record, not a current build/runtime dependency. |
| `diagrams/**` | Supplementary planning diagrams; current architecture and plugin contracts are documented in the migrated docs. |
| `CODE_AUDIT.md` | Repository audit record, not required application source or release metadata. |
| `.github/workflows/archive-lint.yml` | Workflow specifically for the excluded historical archive tree. |

No files were excluded because they were inconvenient to copy. The exclusions are based on current application scope, not a cleanup or deletion decision.

## Important migration dependencies and observations

1. **Application source:** all files under `locallama_gui/` were copied, including backend implementations, UI, controllers, configuration, persistence, plugin manager, and launch entry points.
2. **Python metadata:** `pyproject.toml`, `requirements.txt`, and `VERSION` were copied unchanged. The project metadata currently declares version `1.2.12`.
3. **Launch paths:** `myloai`, compatibility entry point `locallama-gui`, and `python -m locallama_gui` are represented in the copied package metadata and launcher sources.
4. **Configuration/data compatibility:** current `platformdirs` paths and the `locallama-gui` application identifier are preserved. Do not rename these paths during migration without an explicit data-migration plan.
5. **Credential storage:** provider credentials use the operating-system keyring; the config JSON excludes API keys. Preserve this behavior.
6. **Plugin trust:** discovery uses static manifest parsing; plugin execution requires trust and enablement. Preserve this boundary.
7. **Packaging:** current Linux, Windows, macOS, Arch, Debian, AppImage, and PyInstaller definitions were copied as text. Their build status has not been revalidated in this staging operation.
8. **Release payload:** the packaging contract excludes archive, tests, CI, contributor-only, and internal audit material from production installer payloads. That is separate from the broader source repository migration.
9. **Tests:** all 14 current test files were copied. No tests were executed here.
10. **GitHub Actions:** active CI, full CI, and release-packaging workflows were copied. The archive-only lint workflow was excluded.
11. **Historical source:** old Tkinter/Qt/QML applications and archived legacy Python code were not copied into the new application tree.

## Not yet done

- Restore or regenerate the two binary icon assets.
- Create the new standalone MyLoAI Git repository.
- Decide the new repository's final name/owner/visibility.
- Review whether the existing issue templates, license terms, security contact, and governance files should be retained unchanged in the new public repository.
- Run tests in the staged tree.
- Build and validate each supported packaging target.
- Verify the staged release payload and ensure `migrate/` itself is not accidentally included in the future production artifacts.
- Review documentation links and any references to the old repository name.
- Confirm that the migration's current version and changelog baseline are the desired starting point.

## Preservation rule

Treat this manifest as an inventory, not permission to clean up the source repository. The historical repository remains the source of record until a separate migration decision is made.
