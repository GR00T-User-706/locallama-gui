#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
BUILD_DIR="$ROOT_DIR/build/debian"
STAGE_DIR="$BUILD_DIR/root"

cd "$ROOT_DIR"
VERSION="$(python -c 'import pathlib,tomllib; print(tomllib.loads(pathlib.Path("pyproject.toml").read_text())["project"]["version"])')"
ARCH="amd64"
APP_NAME="MyLoAI Control Center"

python packaging/assets/generate_myloai_icon.py
rm -rf "$BUILD_DIR"
mkdir -p "$STAGE_DIR/DEBIAN" \
    "$STAGE_DIR/opt/myloai" \
    "$STAGE_DIR/usr/bin" \
    "$STAGE_DIR/usr/share/applications" \
    "$STAGE_DIR/usr/share/icons/hicolor/scalable/apps" \
    "$STAGE_DIR/usr/share/doc/myloai" \
    "$STAGE_DIR/usr/share/man/man1"

python -m PyInstaller --noconfirm --clean --distpath "$DIST_DIR" --workpath "$ROOT_DIR/build/pyinstaller" packaging/pyinstaller/myloai.spec

cp -a "$DIST_DIR/$APP_NAME/." "$STAGE_DIR/opt/myloai/"

cat > "$STAGE_DIR/usr/bin/myloai" <<'EOF'
#!/bin/sh
exec "/opt/myloai/MyLoAI Control Center" "$@"
EOF
chmod 0755 "$STAGE_DIR/usr/bin/myloai"

install -Dm644 packaging/linux/myloai.desktop "$STAGE_DIR/usr/share/applications/myloai.desktop"
install -Dm644 packaging/linux/appimage/myloai.svg "$STAGE_DIR/usr/share/icons/hicolor/scalable/apps/myloai.svg"
install -Dm644 packaging/USER_MANUAL.md "$STAGE_DIR/usr/share/doc/myloai/USER_MANUAL.md"
install -Dm644 LICENSE "$STAGE_DIR/usr/share/doc/myloai/LICENSE"
install -Dm644 packaging/linux/myloai.1 "$STAGE_DIR/usr/share/man/man1/myloai.1"

cat > "$STAGE_DIR/DEBIAN/control" <<EOF
Package: myloai
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: MyLoAI contributors
Depends: libgl1, libegl1, libglib2.0-0t64 | libglib2.0-0, libdbus-1-3, libfontconfig1, libx11-6, libxext6, libxrender1, libxkbcommon0, libxkbcommon-x11-0, libxcb1, libxcb-cursor0
Homepage: https://github.com/GR00T-User-706/locallama-gui
Description: MyLoAI Control Center
 Native desktop control center for local and remote large language model backends.
 Provides chat, model operations, agents, plugins, diagnostics, and backend management.
EOF

mkdir -p "$DIST_DIR/deb"
DEB_PATH="$DIST_DIR/deb/myloai_${VERSION}_${ARCH}.deb"
rm -f "$DEB_PATH"
dpkg-deb --build --root-owner-group "$STAGE_DIR" "$DEB_PATH"

echo "Created $DEB_PATH"
