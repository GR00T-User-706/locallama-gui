#!/bin/sh
set -eu

# Development/source-tree helper. Native release packages should use their
# package manager and the packaged `myloai` entry point instead.

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd)

if [ ! -f "$REPO_ROOT/pyproject.toml" ]; then
    echo "Error: repository root could not be determined." >&2
    exit 1
fi

echo "MyLoAI Control Center source-tree installation helper"
echo "For production distribution, use a generated .deb, .rpm, Arch package, or AppImage."
echo "For a source installation, run:"
echo "  python3 -m pip install ."
