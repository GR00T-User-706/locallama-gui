#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "\${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="\${PYTHON:-python3}"
APPIMAGETOOL="\${APPIMAGETOOL:-$ROOT_DIR/build/appimagetool}"

cd "$ROOT_DIR"

fail() {
    echo "ERROR: $*" >&2
    exit 1
}

command -v "$PYTHON" >/dev/null 2>&1 || fail "Python 3 is required. Set PYTHON=/path/to/python or install Python 3."
command -v dpkg-deb >/dev/null 2>&1 || fail "dpkg-deb is required for the Debian artifact. On Manjaro/Arch: sudo pacman -S dpkg."
"$PYTHON" -c 'import PyInstaller, PIL, PySide6, httpx, platformdirs, pydantic, psutil, markdown, keyring' >/dev/null 2>&1 || fail "Build Python dependencies are missing. Activate the project venv and install the project plus PyInstaller and Pillow."

if [ ! -x "$APPIMAGETOOL" ] && ! command -v appimagetool >/dev/null 2>&1; then
    fail "appimagetool is required for the AppImage. Put the executable at build/appimagetool or set APPIMAGETOOL=/path/to/appimagetool."
fi

echo "Building MyLoAI Linux production artifacts..."
echo "  Version: $("$PYTHON" -c 'import pathlib,tomllib; print(tomllib.loads(pathlib.Path("pyproject.toml").read_text())["project"]["version"])')"
echo "  Debian:  dist/deb/"
echo "  AppImage: dist/"

"$ROOT_DIR/packaging/linux/debian/build-deb.sh"

if [ -x "$APPIMAGETOOL" ]; then
    APPIMAGETOOL="$APPIMAGETOOL" "$ROOT_DIR/packaging/linux/appimage/build-appimage.sh"
else
    APPIMAGETOOL="$(command -v appimagetool)" "$ROOT_DIR/packaging/linux/appimage/build-appimage.sh"
fi

echo
echo "Production artifacts:"
find "$ROOT_DIR/dist" -maxdepth 2 -type f \( -name '*.deb' -o -name '*.AppImage' \) -print
