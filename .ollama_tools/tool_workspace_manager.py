#!/usr/bin/env python3
"""
tool_workspace_manager.py  (v4 — NEW FILE)
--------------------------------------------
Project Workspace Manager Tool for Ollama LLMs.

Organises multi-file projects safely inside the sandbox directory.
Each project is a subdirectory of sandbox/workspaces/<project_name>/.

Operations:
  create_project    — create a new project workspace
  list_projects     — list all project workspaces
  read_project_file — read a file inside a project
  write_project_file— write a file inside a project
  snapshot_project  — return a manifest of all files in a project

Constraints:
  - ALL operations inside sandbox/workspaces/
  - Strict project directory boundary enforcement
  - Path traversal prevention (realpath + relative_to check)
  - File size limits enforced
  - No shell calls, no arbitrary subprocess
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

MAX_FILE_BYTES    = 128 * 1024   # 128 KB per file
MAX_PROJECT_NAME  = 64
MAX_FILENAME_LEN  = 128
_BAD_NAME_RE      = re.compile(r'[/\x00-\x1f\x7f]')

BLOCKED_EXTENSIONS = {
    ".sh", ".bash", ".zsh", ".fish",
    ".py", ".pl", ".rb", ".php",
    ".elf", ".so", ".out", ".desktop",
}


def _validate_project_name(name: str) -> str:
    name = name.strip()
    if not name:
        raise ValueError("Project name cannot be empty.")
    if len(name) > MAX_PROJECT_NAME:
        raise ValueError(f"Project name too long (max {MAX_PROJECT_NAME} chars).")
    if _BAD_NAME_RE.search(name):
        raise ValueError("Project name contains illegal characters.")
    return name


def _validate_filename(name: str) -> str:
    name = name.strip()
    if not name:
        raise ValueError("Filename cannot be empty.")
    if len(name) > MAX_FILENAME_LEN:
        raise ValueError(f"Filename too long (max {MAX_FILENAME_LEN} chars).")
    if _BAD_NAME_RE.search(name):
        raise ValueError("Filename contains illegal characters (control chars or slash).")
    if name in {".", "..", "~"}:
        raise ValueError(f"'{name}' is a reserved name.")
    ext = Path(name).suffix.lower()
    if ext in BLOCKED_EXTENSIONS:
        raise ValueError(f"Extension '{ext}' is not allowed.")
    return name


class WorkspaceManagerStore:
    """
    Manages multi-file project workspaces inside sandbox/workspaces/.
    """

    def __init__(self, sandbox: Path):
        self.sandbox    = Path(sandbox).resolve()
        self.workspaces = self.sandbox / "workspaces"
        self.workspaces.mkdir(parents=True, exist_ok=True)

    # ---- helpers ----

    def _project_dir(self, project: str) -> Path:
        name      = _validate_project_name(project)
        candidate = (self.workspaces / name).resolve()
        try:
            candidate.relative_to(self.workspaces.resolve())
        except ValueError:
            raise ValueError(f"Project path escapes workspace root: '{project}'")
        return candidate

    def _file_path(self, project_dir: Path, filename: str) -> Path:
        clean     = _validate_filename(filename)
        candidate = (project_dir / clean).resolve()
        try:
            candidate.relative_to(project_dir.resolve())
        except ValueError:
            raise ValueError(f"File path escapes project directory: '{filename}'")
        return candidate

    # ---- operations ----

    def create_project(self, project: str, description: str = "") -> str:
        pd = self._project_dir(project)
        if pd.exists():
            return f"Error: Project '{project}' already exists."
        pd.mkdir(parents=True)
        meta = {
            "project":     project,
            "description": description,
            "created":     datetime.now().isoformat(timespec="seconds"),
            "files":       [],
        }
        (pd / ".meta.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return f"Created workspace project '{project}'."

    def list_projects(self) -> str:
        projects = [d.name for d in sorted(self.workspaces.iterdir()) if d.is_dir()]
        if not projects:
            return "No workspace projects found."
        return "Workspace projects:\n" + "\n".join(f"  • {p}" for p in projects)

    def read_project_file(self, project: str, filename: str) -> str:
        try:
            pd   = self._project_dir(project)
            path = self._file_path(pd, filename)
        except ValueError as e:
            return f"Error: {e}"
        if not pd.exists():
            return f"Error: Project '{project}' does not exist."
        if not path.exists():
            return f"Error: File '{filename}' not found in project '{project}'."
        if not path.is_file():
            return f"Error: '{filename}' is not a regular file."
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            return f"Error: File '{filename}' is {size//1024} KB, exceeds read limit of {MAX_FILE_BYTES//1024} KB."
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return f"Error: '{filename}' does not appear to be a text file."

    def write_project_file(self, project: str, filename: str, content: str) -> str:
        try:
            pd   = self._project_dir(project)
            path = self._file_path(pd, filename)
        except ValueError as e:
            return f"Error: {e}"
        if not pd.exists():
            return f"Error: Project '{project}' does not exist. Use create_project first."
        if len(content.encode("utf-8")) > MAX_FILE_BYTES:
            return f"Error: Content exceeds max file size ({MAX_FILE_BYTES//1024} KB)."
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Wrote '{filename}' in project '{project}' ({len(content)} chars)."

    def snapshot_project(self, project: str) -> str:
        try:
            pd = self._project_dir(project)
        except ValueError as e:
            return f"Error: {e}"
        if not pd.exists():
            return f"Error: Project '{project}' does not exist."
        files = sorted(f for f in pd.rglob("*") if f.is_file() and f.name != ".meta.json")
        if not files:
            return f"Project '{project}' has no files yet."
        lines = [f"Snapshot of project '{project}':"]
        total = 0
        for f in files:
            rel  = f.relative_to(pd)
            size = f.stat().st_size
            total += size
            lines.append(f"  {str(rel):<48} {size:>8,} bytes")
        lines.append(f"\n  Total: {len(files)} file(s), {total:,} bytes")
        return "\n".join(lines)


# ------------------------------------------------------------------
# Ollama tool schema
# ------------------------------------------------------------------

WORKSPACE_MANAGER_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "workspace_manager",
        "description": (
            "Manage multi-file project workspaces inside the secure sandbox. "
            "Create projects, read and write files, and get project snapshots. "
            "All files are strictly contained within the sandbox."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": [
                        "create_project", "list_projects",
                        "read_project_file", "write_project_file",
                        "snapshot_project",
                    ],
                    "description": "The workspace operation to perform.",
                },
                "project":     {"type": "string", "description": "Project name."},
                "description": {"type": "string", "description": "Project description (create_project only)."},
                "filename":    {"type": "string", "description": "File name within the project."},
                "content":     {"type": "string", "description": "File content (write_project_file only)."},
            },
            "required": ["operation"],
        },
    },
}


def dispatch_workspace_manager_tool(args: dict, store: WorkspaceManagerStore) -> str:
    op      = args.get("operation", "").strip().lower()
    project = args.get("project",  "")
    try:
        if op == "create_project":
            if not project: return "Error: 'create_project' requires 'project'."
            return store.create_project(project, args.get("description", ""))
        elif op == "list_projects":
            return store.list_projects()
        elif op == "read_project_file":
            if not project:              return "Error: 'read_project_file' requires 'project'."
            if not args.get("filename"): return "Error: 'read_project_file' requires 'filename'."
            return store.read_project_file(project, args["filename"])
        elif op == "write_project_file":
            if not project:              return "Error: 'write_project_file' requires 'project'."
            if not args.get("filename"): return "Error: 'write_project_file' requires 'filename'."
            if args.get("content") is None: return "Error: 'write_project_file' requires 'content'."
            return store.write_project_file(project, args["filename"], args["content"])
        elif op == "snapshot_project":
            if not project: return "Error: 'snapshot_project' requires 'project'."
            return store.snapshot_project(project)
        else:
            return f"Error: Unknown workspace_manager operation '{op}'."
    except Exception as e:
        return f"Error: {e}"
