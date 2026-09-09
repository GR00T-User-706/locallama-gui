#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
APPDIR="$ROOT_DIR/build/AppDir"
APP_NAME="MyLoAI Control Center"
VERSION="$(python -c 'import pathlib,tomllib; print(tomllib.loads(pathlib.Path("pyproject.toml").read_text())["project"]["version"])')"
APPIMAGE="$DIST_DIR/MyLoAI-Control-Center-${VERSION}-x86_64.AppImage"
APPIMAGETOOL="${APPIMAGETOOL:-$ROOT_DIR/build/appimagetool}"

cd "$ROOT_DIR"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin" "$APPDIR/usr/share/applications" "$APPDIR/usr/share/doc/myloai"

python -m PyInstaller --noconfirm --clean --distpath "$DIST_DIR" --workpath "$ROOT_DIR/build/pyinstaller" packaging/pyinstaller/myloai.spec

cp -a "$DIST_DIR/$APP_NAME/." "$APPDIR/usr/bin/"
cp packaging/linux/myloai.desktop "$APPDIR/myloai.desktop"
cp packaging/linux/myloai.desktop "$APPDIR/usr/share/applications/myloai.desktop"
sed -i 's/^Exec=myloai$/Exec=AppRun/' "$APPDIR/myloai.desktop"
sed -i 's/^Exec=myloai$/Exec=AppRun/' "$APPDIR/usr/share/applications/myloai.desktop"
sed -i '/^Keywords=/a Icon=myloai' "$APPDIR/myloai.desktop"
sed -i '/^Keywords=/a Icon=myloai' "$APPDIR/usr/share/applications/myloai.desktop"
cp packaging/linux/appimage/myloai.svg "$APPDIR/myloai.svg"
cp packaging/USER_MANUAL.md "$APPDIR/usr/share/doc/myloai/USER_MANUAL.md"
cp LICENSE "$APPDIR/usr/share/doc/myloai/LICENSE"

cat > "$APPDIR/AppRun" <<'EOF'
#!/bin/sh
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec "$HERE/usr/bin/MyLoAI Control Center/MyLoAI Control Center" "$@"
EOF
chmod +x "$APPDIR/AppRun"

if [ ! -x "$APPIMAGETOOL" ]; then
    echo "appimagetool not found: set APPIMAGETOOL or install it in build/appimagetool" >&2
    exit 1
fi

rm -f "$APPIMAGE"
ARCH=x86_64 "$APPIMAGETOOL" --appimage-extract-and-run "$APPDIR" "$APPIMAGE"
echo "Created $APPIMAGE"
