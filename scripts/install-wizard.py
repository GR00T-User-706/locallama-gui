#!/usr/bin/env python3
"""Install LocalLama GUI into an isolated Python environment."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

MIN_PYTHON = (3, 11)
MAX_PYTHON = (3, 13)
DEFAULT_VENV = ".venv"
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/tags"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install LocalLama GUI into a repository-local virtual environment.")
    parser.add_argument("--venv", default=DEFAULT_VENV, help="Virtual-environment directory (default: .venv).")
    parser.add_argument("--python", dest="python_executable", help="Python executable for the new virtual environment.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned actions without changing the system.")
    parser.add_argument("--no-launcher", action="store_true", help="Skip Unix launcher/desktop integration.")
    parser.add_argument("--desktop-entry", action="store_true", help="On Linux, also install the desktop entry.")
    parser.add_argument("--windows-desktop", action="store_true", help="Also create a Windows desktop shortcut.")
    parser.add_argument("--check-backend", nargs="?", const=DEFAULT_OLLAMA_URL, metavar="URL", help="Check a backend after installation. Defaults to Ollama's local API.")
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run(command: list[str], *, cwd: Path, dry_run: bool = False) -> None:
    print("$", " ".join(str(part) for part in command))
    if dry_run:
        return
    subprocess.run(command, cwd=cwd, check=True)


def check_python() -> None:
    version = sys.version_info[:2]
    if version < MIN_PYTHON or version > MAX_PYTHON:
        raise SystemExit("Unsupported Python version: " f"{version[0]}.{version[1]}. LocalLama GUI supports Python 3.11 through 3.13.")
    print(f"✓ Python {version[0]}.{version[1]} detected")


def resolve_python(requested: str | None) -> str:
    candidate = (shutil.which(requested) or requested) if requested else sys.executable
    result = subprocess.run([candidate, "-c", "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"], capture_output=True, text=True, check=True)
    major, minor = (int(part) for part in result.stdout.strip().split("."))
    if (major, minor) < MIN_PYTHON or (major, minor) > MAX_PYTHON:
        raise SystemExit(f"Unsupported Python executable {candidate}: {major}.{minor}. Use Python 3.11, 3.12, or 3.13.")
    return candidate


def venv_python(venv: Path) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ensure_venv(venv: Path, python_executable: str, dry_run: bool) -> None:
    if venv.exists():
        interpreter = venv_python(venv)
        if not interpreter.exists() and not dry_run:
            raise SystemExit(f"Existing virtual environment is incomplete: {venv}")
        print(f"✓ Using existing virtual environment: {venv}")
        return
    print(f"Creating virtual environment: {venv}")
    run([python_executable, "-m", "venv", str(venv)], cwd=repo_root(), dry_run=dry_run)
    if not dry_run:
        print("✓ Virtual environment created")


def install_package(venv: Path, dry_run: bool) -> None:
    python = venv_python(venv)
    if not dry_run and not python.exists():
        raise SystemExit(f"Virtual-environment Python was not created: {python}")
    run([str(python), "-m", "pip", "install", "--upgrade", "pip"], cwd=repo_root(), dry_run=dry_run)
    run([str(python), "-m", "pip", "install", "-e", "."], cwd=repo_root(), dry_run=dry_run)
    if not dry_run:
        print("✓ LocalLama GUI installed")


def install_unix_launchers(root: Path, args: argparse.Namespace) -> None:
    if args.no_launcher:
        print("• Unix launcher installation skipped")
        return
    launcher = root / "scripts" / "install-launcher"
    desktop = root / "scripts" / "install-desktop-entry"
    if not launcher.is_file():
        raise SystemExit(f"Missing canonical launcher installer: {launcher}")
    run([str(launcher)], cwd=root, dry_run=args.dry_run)
    if platform.system() == "Linux" and args.desktop_entry:
        if not desktop.is_file():
            raise SystemExit(f"Missing canonical desktop installer: {desktop}")
        run([str(desktop)], cwd=root, dry_run=args.dry_run)


def windows_start_menu_dir() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise SystemExit("APPDATA is not available; cannot determine the Windows Start Menu path.")
    return Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs"


def create_windows_shortcut(target_python: Path, root: Path, destination: Path, dry_run: bool) -> None:
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
    powershell = shutil.which("powershell.exe") or shutil.which("powershell")
    if not powershell:
        raise SystemExit("PowerShell is required to create Windows shortcuts.")
    script = "$ws = New-Object -ComObject WScript.Shell; " f"$s = $ws.CreateShortcut('{destination}'); " f"$s.TargetPath = '{target_python}'; " "$s.Arguments = '-m locallama_gui'; " f"$s.WorkingDirectory = '{root}'; " "$s.Description = 'LocalLama Control Center'; " "$s.Save()"
    run([powershell, "-NoProfile", "-NonInteractive", "-Command", script], cwd=root, dry_run=dry_run)


def install_windows_shortcuts(root: Path, venv: Path, args: argparse.Namespace) -> None:
    python = venv_python(venv)
    start_menu = windows_start_menu_dir() / "LocalLama Control Center.lnk"
    create_windows_shortcut(python, root, start_menu, args.dry_run)
    print(f"✓ Start Menu shortcut: {start_menu}")
    if args.windows_desktop:
        desktop = Path.home() / "Desktop" / "LocalLama Control Center.lnk"
        create_windows_shortcut(python, root, desktop, args.dry_run)
        print(f"✓ Desktop shortcut: {desktop}")


def check_backend(url: str) -> bool:
    print(f"Checking backend: {url}")
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            print(f"✓ Backend reachable (HTTP {response.status})")
            return True
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"⚠ Backend not reachable: {exc}")
        return False


def verify_installation(root: Path, venv: Path, dry_run: bool) -> None:
    python = venv_python(venv)
    if dry_run:
        print("• Verification skipped in dry-run mode")
        return
    run([str(python), "-c", "import locallama_gui; import PySide6; import httpx; import platformdirs; import pydantic; import psutil; import markdown; print('imports ok')"], cwd=root)
    result = subprocess.run([str(python), "-c", "import importlib.metadata as m; print(m.version('locallama-gui'))"], cwd=root, capture_output=True, text=True, check=True)
    print(f"✓ Installed package version: {result.stdout.strip()}")
    print("✓ Installation verification passed")


def main() -> int:
    args = parse_args()
    root = repo_root()
    if not (root / "pyproject.toml").is_file():
        raise SystemExit(f"This script must be run from the repository checkout: {root}")
    print("LocalLama Control Center installer")
    print("=" * 38)
    print(f"Repository: {root}")
    print(f"Platform:   {platform.system()} ({platform.machine()})")
    print()
    check_python()
    python_executable = resolve_python(args.python_executable)
    venv = (root / args.venv).resolve()
    ensure_venv(venv, python_executable, args.dry_run)
    install_package(venv, args.dry_run)
    if os.name == "nt":
        install_windows_shortcuts(root, venv, args)
    else:
        install_unix_launchers(root, args)
    verify_installation(root, venv, args.dry_run)
    if args.check_backend:
        if args.dry_run:
            print(f"• Would check backend: {args.check_backend}")
        else:
            check_backend(args.check_backend)
    print()
    if args.dry_run:
        print("Dry run complete. No installation changes were made by this wizard.")
    else:
        print("Installation complete.")
        print(f"Launch with: {venv_python(venv)} -m locallama_gui")
        if os.name == "nt":
            print("A Start Menu shortcut was created for LocalLama Control Center.")
        else:
            print("Use the installed run-locallama launcher from your user-local bin directory.")
        print("Configure an AI backend from Settings → API Endpoints.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
