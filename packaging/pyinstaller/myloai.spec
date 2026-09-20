# MyLoAI Control Center production PyInstaller specification.
# The spec intentionally starts from the active application entry point and
# collects only the locallama_gui package plus its runtime imports.

import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata, copy_metadata

APP_NAME = "MyLoAI Control Center"
APP_EXECUTABLE = "MyLoAI_Control_Center"
PACKAGE = "locallama_gui"
ROOT_DIR = Path(SPECPATH).resolve().parents[1]
ICON_PATH = ROOT_DIR / "packaging" / "assets" / "MyLoAI.ico"

hiddenimports = collect_submodules(PACKAGE) + collect_submodules("keyring.backends") + collect_submodules("keyring.backends")
datas = collect_data_files(PACKAGE, include_py_files=False) + copy_metadata("keyring") + copy_metadata("keyring")
datas += [
    (str(ROOT_DIR / "packaging" / "USER_MANUAL.md"), "docs"),
    (str(ROOT_DIR / "docs" / "PLUGIN_SDK.md"), "docs"),
]

analysis = Analysis(
    [str(ROOT_DIR / PACKAGE / "__main__.py")],
    pathex=[str(ROOT_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "ruff"],
    noarchive=False,
)

pyz = PYZ(analysis.pure)

if sys.platform == "darwin":
    exe = EXE(
        pyz,
        analysis.scripts,
        analysis.binaries,
        analysis.datas,
        [],
        name=APP_EXECUTABLE,
        icon=None,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=False,
    )
    app = BUNDLE(
        exe,
        name=f"{APP_EXECUTABLE}.app",
        icon=None,
        bundle_identifier="com.myloai.controlcenter",
    )
else:
    exe = EXE(
        pyz,
        analysis.scripts,
        exclude_binaries=True,
        name=APP_EXECUTABLE,
        icon=str(ICON_PATH),
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=False,
    )
    app = COLLECT(
        exe,
        analysis.binaries,
        analysis.datas,
        strip=False,
        upx=False,
        name=APP_EXECUTABLE,
    )
