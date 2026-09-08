#!/usr/bin/env python3
"""Validate that a staged production release contains no repository-only material."""
from __future__ import annotations

import argparse
from pathlib import Path

EXCLUDED_TOP_LEVEL = {".github", "archive", "tests"}
EXCLUDED_FILES = {"AGENTS.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def validate(root: Path) -> list[str]:
    problems: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if rel.parts and rel.parts[0] in EXCLUDED_TOP_LEVEL:
            problems.append(rel.as_posix())
            continue
        if path.name in EXCLUDED_FILES or path.suffix in EXCLUDED_SUFFIXES:
            problems.append(rel.as_posix())
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("staging_dir", type=Path)
    args = parser.parse_args()
    problems = validate(args.staging_dir)
    if problems:
        print("Release payload validation failed:")
        for item in problems:
            print(f"  {item}")
        return 1
    print(f"Release payload OK: {args.staging_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
