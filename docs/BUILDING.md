# Building MyLoAI Control Center

This is the canonical local production-build guide.

## What you build

On Linux, the production build produces:

- `dist/deb/myloai_VERSION_amd64.deb`
- `dist/MyLoAI-Control-Center-VERSION-x86_64.AppImage`

Both contain the PyInstaller-bundled application runtime. End users do **not** need Python, pip, PyInstaller, or the repository.

## Recommended Linux build path

For the current Manjaro/Arch development machine:

### 1. Enter the repository

Use a path without spaces.

```bash
cd ~/src/locallama-gui
```

### 2. Create or activate the build environment

If the project virtual environment already exists:

```bash
source .venv/bin/activate
```

Otherwise:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the build requirements

The build environment needs the project runtime dependencies plus PyInstaller and Pillow.

```bash
python -m pip install -e .
python -m pip install pyinstaller pillow
```

If the machine is offline, those packages must already be available in the local pip cache or supplied as wheel files. The production build itself does not download anything.

### 4. Install the Linux package-build tool

The Debian artifact requires `dpkg-deb`. On Manjaro/Arch:

```bash
sudo pacman -S dpkg
```

### 5. Supply appimagetool

The AppImage build requires the official `appimagetool` executable. The build script looks for it here first:

```text
build/appimagetool
```

You can also point to another copy:

```bash
APPIMAGETOOL=/path/to/appimagetool ./packaging/build-linux.sh
```

If the machine is offline, copy the appimagetool AppImage/executable to the build machine before starting. Current appimagetool builds can also require a local AppImage runtime. Put that runtime on the build machine and set `APPIMAGERUNTIME=/path/to/runtime-x86_64` when running the build command. The official appimagetool documentation explicitly supports `--runtime-file` for builds without Internet access.

### 6. Build everything

From the repository root:

```bash
./packaging/build-linux.sh
```

That is the **one canonical Linux production build command**.

### 7. Find the artifacts

```bash
find dist -maxdepth 2 -type f \\( -name '*.deb' -o -name '*.AppImage' \\) -print
```

The AppImage can be tested directly:

```bash
chmod +x dist/*.AppImage
./dist/MyLoAI-Control-Center-*.AppImage
```

The Debian package can be inspected on Manjaro without installing it:

```bash
dpkg-deb --info dist/deb/*.deb
dpkg-deb --contents dist/deb/*.deb
```

For actual Debian installation testing, use a Debian/Ubuntu environment. Building a Debian package on Manjaro is supported by the packaging script, but installing Debian packages into an Arch-based host is not the normal package-management path.

## Build prerequisites

| Tool | Purpose | Required |
|---|---|---|
| Python 3.11+ | Build/runtime environment | Yes |
| PySide6 | Application dependency | Yes |
| httpx | Application dependency | Yes |
| platformdirs | Application dependency | Yes |
| pydantic | Application dependency | Yes |
| psutil | Application dependency | Yes |
| markdown | Application dependency | Yes |
| keyring | Application dependency | Yes |
| PyInstaller | Creates bundled application | Yes |
| Pillow | Icon generation | Yes |
| dpkg-deb | Creates `.deb` | Debian artifact |
| appimagetool | Creates AppImage | AppImage artifact |

## Other platforms

### Windows

Build on Windows. PyInstaller is not a cross-compiler, so a Linux machine does not build the Windows executable.

Requirements:

- Python 3.13
- project dependencies
- PyInstaller
- Pillow
- Inno Setup 6

Command:

```powershell
python -m pip install -e .
python -m pip install pyinstaller pillow
powershell -ExecutionPolicy Bypass -File packaging\\windows\\build-installer.ps1
```

Output:

```text
dist\\installer\\MyLoAI-Control-Center-VERSION-Windows-x64.exe
```

### macOS

Build on macOS. Build separately on Apple Silicon and Intel when both architectures are required.

Requirements:

- Python 3.13
- project dependencies
- PyInstaller
- Xcode command-line tools
- `hdiutil`

Command:

```bash
python3 -m pip install -e .
python3 -m pip install pyinstaller
bash packaging/macos/build-dmg.sh
```

## What not to do

Do not ask end users to:

- install Python
- install PyInstaller
- clone the repository
- run `pip install`
- run `python -m locallama_gui`
- use `run-locallama`

Those are development/build paths, not production installation paths.
