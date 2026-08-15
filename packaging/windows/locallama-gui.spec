# PyInstaller build specification for the LocalLama Control Center desktop app.
# The application remains a normal Python package; this file only defines the
# native Windows distribution bundle.

from PyInstaller.utils.hooks import collect_data_files, collect_submodules


hiddenimports = collect_submodules("locallama_gui")
datas = collect_data_files("locallama_gui")


app = Analysis(
    ["locallama_gui/app.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "pytest",
        "ruff",
    ],
    noarchive=False,
)

pyz = PYZ(app.pure)

exe = EXE(
    pyz,
    app.scripts,
    app.binaries,
    app.datas,
    [],
    name="LocalLamaControlCenter",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
)
