#!/usr/bin/env bash
set -euo pipefail

echo "==> Creating archive directories"

mkdir -p \
  archive/old_apps \
  archive/legacy_code \
  archive/experimental \
  archive/old_docs \
  archive/notes \
  archive/manifests

echo "==> Moving legacy app trees"

if [ -d "ollama_GUI" ]; then
  if [ -e "archive/old_apps/ollama_GUI" ]; then
    echo "ERROR: archive/old_apps/ollama_GUI already exists. Refusing to overwrite."
    exit 1
  fi
  git mv ollama_GUI archive/old_apps/ollama_GUI
else
  echo "SKIP: ollama_GUI not found"
fi

if [ -d "llm_studio" ]; then
  if [ -e "archive/legacy_code/llm_studio" ]; then
    echo "ERROR: archive/legacy_code/llm_studio already exists. Refusing to overwrite."
    exit 1
  fi
  git mv llm_studio archive/legacy_code/llm_studio
else
  echo "SKIP: llm_studio not found"
fi

echo "==> Moving old docs"

if [ -f "FUNCTIONALITY_STATUS.md" ]; then
  git mv FUNCTIONALITY_STATUS.md archive/old_docs/FUNCTIONALITY_STATUS.md
else
  echo "SKIP: FUNCTIONALITY_STATUS.md not found"
fi

if [ -f "SECURITY_REVIEW.md" ]; then
  git mv SECURITY_REVIEW.md archive/old_docs/SECURITY_REVIEW.md
else
  echo "SKIP: SECURITY_REVIEW.md not found"
fi

if [ -f "HUMAN_REVIEW.md" ]; then
  git mv HUMAN_REVIEW.md archive/notes/HUMAN_REVIEW.md
else
  echo "SKIP: HUMAN_REVIEW.md not found"
fi

echo "==> Ensuring archive governance files exist"

touch archive/ARCHIVE_INDEX.md
touch archive/README.md
touch archive/manifests/ARCHIVE_MANIFEST.md
touch archive/manifests/duplicate_manifest.md

echo "==> Removing Python cache files from tracked/untracked working tree"

find . -type d -name "__pycache__" -prune -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "==> Archive move complete"
echo
echo "Review with:"
echo "  git status"
echo "  git diff --stat"
