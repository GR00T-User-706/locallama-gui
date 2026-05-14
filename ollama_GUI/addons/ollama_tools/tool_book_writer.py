#!/usr/bin/env python3
"""
tool_book_writer.py  (v4 — NEW FILE)
-------------------------------------
Book Writer Tool for Ollama LLMs.

Provides structured long-form writing with persistent state.
ALL files are stored inside the sandbox directory only.

Operations:
  create_project    — initialise a new book project
  update_outline    — set or update the chapter outline
  write_section     — write or overwrite a chapter/section
  revise_section    — append a revision note to a section
  summarize_section — return a trimmed summary of a section
  track_character   — add or update a character entry

File layout inside sandbox/<project_name>/:
  outline.json      — chapter outline
  characters.json   — character registry
  chapters/<name>.md — individual chapter/section files

Security:
  - All paths resolved and verified inside sandbox
  - Max section size enforced (MAX_SECTION_BYTES)
  - No direct arbitrary file writes
  - No shell calls
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# ------------------------------------------------------------------
MAX_SECTION_BYTES   = 64 * 1024   # 64 KB per section
MAX_SUMMARY_CHARS   = 1_000       # chars returned by summarize_section
MAX_PROJECT_NAME    = 64
MAX_SECTION_NAME    = 64
MAX_CHARACTER_NAME  = 64
_BAD_NAME_RE        = re.compile(r'[^\w\s\-]')   # allow word chars, spaces, hyphens


def _validate_name(name: str, label: str, max_len: int = 64) -> str:
    name = name.strip()
    if not name:
        raise ValueError(f"{label} cannot be empty.")
    if len(name) > max_len:
        raise ValueError(f"{label} is too long (max {max_len} chars).")
    if _BAD_NAME_RE.search(name):
        raise ValueError(f"{label} contains invalid characters. Use letters, numbers, spaces, hyphens.")
    return name


def _safe_project_path(sandbox: Path, project: str) -> Path:
    """Resolve and verify a project directory is inside the sandbox."""
    candidate = (sandbox / project).resolve()
    try:
        candidate.relative_to(sandbox.resolve())
    except ValueError:
        raise ValueError(f"Project path escapes sandbox: '{project}'")
    return candidate


def _safe_chapter_path(project_dir: Path, section: str) -> Path:
    """Resolve and verify a chapter file is inside the project's chapters/ dir."""
    chapters_dir = project_dir / "chapters"
    filename     = section.strip().replace(" ", "_") + ".md"
    candidate    = (chapters_dir / filename).resolve()
    try:
        candidate.relative_to(chapters_dir.resolve())
    except ValueError:
        raise ValueError(f"Section path escapes chapters directory: '{section}'")
    return candidate


# ------------------------------------------------------------------

class BookWriterStore:
    """
    Manages book projects stored inside a sandbox directory.
    Each project lives in sandbox/<project_name>/.
    """

    def __init__(self, sandbox: Path):
        self.sandbox = Path(sandbox).resolve()
        self.sandbox.mkdir(parents=True, exist_ok=True)

    # ---- helpers ----

    def _project_dir(self, project: str) -> Path:
        name = _validate_name(project, "Project name", MAX_PROJECT_NAME)
        return _safe_project_path(self.sandbox, name)

    def _load_json(self, path: Path, default: Any) -> Any:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return default
        return default

    def _save_json(self, path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp.replace(path)

    # ---- operations ----

    def create_project(self, project: str, title: str = "", description: str = "") -> str:
        pd = self._project_dir(project)
        if pd.exists():
            return f"Error: Project '{project}' already exists."
        pd.mkdir(parents=True)
        (pd / "chapters").mkdir()
        meta = {
            "title":       title or project,
            "description": description,
            "created":     datetime.now().isoformat(timespec="seconds"),
        }
        self._save_json(pd / "outline.json",    {"meta": meta, "chapters": []})
        self._save_json(pd / "characters.json", {"characters": {}})
        return f"Created book project '{project}' at {pd}."

    def update_outline(self, project: str, chapters: list) -> str:
        pd      = self._project_dir(project)
        if not pd.exists():
            return f"Error: Project '{project}' does not exist."
        outline = self._load_json(pd / "outline.json", {"meta": {}, "chapters": []})
        if not isinstance(chapters, list):
            return "Error: 'chapters' must be a list of strings."
        outline["chapters"] = [str(c)[:MAX_SECTION_NAME] for c in chapters]
        outline["updated"]  = datetime.now().isoformat(timespec="seconds")
        self._save_json(pd / "outline.json", outline)
        return f"Outline updated for '{project}' ({len(chapters)} chapters)."

    def write_section(self, project: str, section: str, content: str) -> str:
        pd = self._project_dir(project)
        if not pd.exists():
            return f"Error: Project '{project}' does not exist."
        try:
            _validate_name(section, "Section name", MAX_SECTION_NAME)
            path = _safe_chapter_path(pd, section)
        except ValueError as e:
            return f"Error: {e}"
        if len(content.encode("utf-8")) > MAX_SECTION_BYTES:
            return f"Error: Content exceeds max section size ({MAX_SECTION_BYTES//1024} KB)."
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Wrote section '{section}' ({len(content)} chars) in project '{project}'."

    def revise_section(self, project: str, section: str, revision_note: str) -> str:
        pd = self._project_dir(project)
        if not pd.exists():
            return f"Error: Project '{project}' does not exist."
        try:
            path = _safe_chapter_path(pd, section)
        except ValueError as e:
            return f"Error: {e}"
        if not path.exists():
            return f"Error: Section '{section}' does not exist. Use write_section first."
        existing = path.read_text(encoding="utf-8")
        appended = (
            existing + f"\n\n---\n**Revision ({datetime.now().isoformat(timespec='seconds')}):**\n"
            + revision_note
        )
        if len(appended.encode("utf-8")) > MAX_SECTION_BYTES:
            return f"Error: Revised content would exceed max section size ({MAX_SECTION_BYTES//1024} KB)."
        path.write_text(appended, encoding="utf-8")
        return f"Revision appended to section '{section}' in project '{project}'."

    def summarize_section(self, project: str, section: str) -> str:
        pd = self._project_dir(project)
        if not pd.exists():
            return f"Error: Project '{project}' does not exist."
        try:
            path = _safe_chapter_path(pd, section)
        except ValueError as e:
            return f"Error: {e}"
        if not path.exists():
            return f"Error: Section '{section}' does not exist."
        content = path.read_text(encoding="utf-8")
        if len(content) <= MAX_SUMMARY_CHARS:
            return content
        return content[:MAX_SUMMARY_CHARS] + f"\n\n[...truncated — {len(content)} total chars]"

    def track_character(self, project: str, name: str, attributes: dict) -> str:
        pd = self._project_dir(project)
        if not pd.exists():
            return f"Error: Project '{project}' does not exist."
        try:
            _validate_name(name, "Character name", MAX_CHARACTER_NAME)
        except ValueError as e:
            return f"Error: {e}"
        if not isinstance(attributes, dict):
            return "Error: 'attributes' must be a JSON object."
        chars_path = pd / "characters.json"
        chars      = self._load_json(chars_path, {"characters": {}})
        chars["characters"][name] = {
            "attributes": attributes,
            "updated":    datetime.now().isoformat(timespec="seconds"),
        }
        self._save_json(chars_path, chars)
        return f"Character '{name}' tracked in project '{project}'."

    def list_projects(self) -> str:
        projects = [d.name for d in sorted(self.sandbox.iterdir()) if d.is_dir()]
        if not projects:
            return "No book projects found."
        return "Book projects:\n" + "\n".join(f"  • {p}" for p in projects)


# ------------------------------------------------------------------
# Ollama tool schema
# ------------------------------------------------------------------

BOOK_WRITER_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "book_writer",
        "description": (
            "Manage structured long-form writing projects. "
            "Create book projects, maintain outlines, write and revise chapters/sections, "
            "and track characters. All files are stored in a secure sandbox."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": [
                        "create_project", "update_outline", "write_section",
                        "revise_section", "summarize_section", "track_character",
                        "list_projects",
                    ],
                    "description": "The book writing operation to perform.",
                },
                "project":       {"type": "string",  "description": "Project name (slug)."},
                "title":         {"type": "string",  "description": "Book title (create_project only)."},
                "description":   {"type": "string",  "description": "Book description (create_project only)."},
                "chapters":      {"type": "array",   "items": {"type": "string"}, "description": "Chapter list (update_outline only)."},
                "section":       {"type": "string",  "description": "Section/chapter name."},
                "content":       {"type": "string",  "description": "Text content (write_section only)."},
                "revision_note": {"type": "string",  "description": "Revision text (revise_section only)."},
                "name":          {"type": "string",  "description": "Character name (track_character only)."},
                "attributes":    {"type": "object",  "description": "Character attributes dict (track_character only)."},
            },
            "required": ["operation"],
        },
    },
}


def dispatch_book_writer_tool(args: dict, store: BookWriterStore) -> str:
    op      = args.get("operation", "").strip().lower()
    project = args.get("project", "")
    try:
        if op == "create_project":
            if not project: return "Error: 'create_project' requires 'project'."
            return store.create_project(project, args.get("title",""), args.get("description",""))
        elif op == "update_outline":
            if not project: return "Error: 'update_outline' requires 'project'."
            return store.update_outline(project, args.get("chapters", []))
        elif op == "write_section":
            if not project:             return "Error: 'write_section' requires 'project'."
            if not args.get("section"): return "Error: 'write_section' requires 'section'."
            if not args.get("content"): return "Error: 'write_section' requires 'content'."
            return store.write_section(project, args["section"], args["content"])
        elif op == "revise_section":
            if not project:                  return "Error: 'revise_section' requires 'project'."
            if not args.get("section"):      return "Error: 'revise_section' requires 'section'."
            if not args.get("revision_note"):return "Error: 'revise_section' requires 'revision_note'."
            return store.revise_section(project, args["section"], args["revision_note"])
        elif op == "summarize_section":
            if not project:             return "Error: 'summarize_section' requires 'project'."
            if not args.get("section"): return "Error: 'summarize_section' requires 'section'."
            return store.summarize_section(project, args["section"])
        elif op == "track_character":
            if not project:           return "Error: 'track_character' requires 'project'."
            if not args.get("name"):  return "Error: 'track_character' requires 'name'."
            return store.track_character(project, args["name"], args.get("attributes", {}))
        elif op == "list_projects":
            return store.list_projects()
        else:
            return f"Error: Unknown book_writer operation '{op}'."
    except Exception as e:
        return f"Error: {e}"
