#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
BUILD_DIR="$ROOT_DIR/build/pyinstaller"
APP_NAME="MyLoAI Control Center"
VERSION="$(python -c 'import pathlib,tomllib; print(tomllib.loads(pathlib.Path("pyproject.toml").read_text())["project"]["version"])')"
APP_PATH="$DIST_DIR/$APP_NAME.app"
DMG_PATH="$DIST_DIR/MyLoAI-Control-Center-${VERSION}-macOS.dmg"

cd "$ROOT_DIR"
rm -rf "$APP_PATH"
python -m PyInstaller --noconfirm --clean --distpath "$DIST_DIR" --workpath "$BUILD_DIR" packaging/pyinstaller/myloai.spec

test -d "$APP_PATH"
mkdir -p "$APP_PATH/Contents/Resources/MyLoAI"
cp packaging/USER_MANUAL.md "$APP_PATH/Contents/Resources/MyLoAI/USER_MANUAL.md"
cp LICENSE "$APP_PATH/Contents/Resources/MyLoAI/LICENSE"

rm -f "$DMG_PATH"
hdiutil create -volname "$APP_NAME" -srcfolder "$APP_PATH" -ov -format UDZO "$DMG_PATH"

echo "Created $DMG_PATH"
