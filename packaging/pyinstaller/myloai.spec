# MyLoAI Control Center production PyInstaller specification.
# The spec intentionally starts from the active application entry point and
# collects only the locallama_gui package plus its runtime imports.

import sys

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

APP_NAME = "MyLoAI Control Center"
PACKAGE = "locallama_gui"

hiddenimports = collect_submodules(PACKAGE)
datas = collect_data_files(PACKAGE, include_py_files=False)

analysis = Analysis(
    ["../../locallama_gui/__main__.py"],
    pathex=["../.."],
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

exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

if sys.platform == "darwin":
    app = BUNDLE(
        exe,
        name=f"{APP_NAME}.app",
        icon=None,
        bundle_identifier="com.myloai.controlcenter",
    )
else:
    app = COLLECT(
        exe,
        analysis.binaries,
        analysis.datas,
        strip=False,
        upx=False,
        name=APP_NAME,
    )
