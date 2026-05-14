#!/usr/bin/env python3
"""
tool_sandbox_files.py  (v3)
---------------------------
Sandboxed file read/write tool for Ollama LLMs.

v3 changes (surgical, backward-compatible):
  FIX 4 — Filename sanitization: strip whitespace, reject control chars,
           null bytes, reserved names, and overly long filenames.
  FIX 5 — Firejail fallback transparency: firejail failures now log clearly
           and require explicit opt-in (allow_firejail_fallback=True) before
           downgrading to a direct write. Default is to fail loudly.
"""

import logging
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
DEFAULT_SANDBOX_DIR = Path.home() / ".ollama_tools" / "sandbox"
MAX_WRITE_BYTES     = 512 * 1024
MAX_READ_BYTES      = 128 * 1024

BLOCKED_EXTENSIONS = {
    ".sh", ".bash", ".zsh", ".fish",
    ".py", ".pl", ".rb", ".php",
    ".elf", ".so", ".out",
    ".desktop",
}

# --- NEW (FIX 4): tighter filename validation ---
_MAX_FILENAME_LEN = 128
_BAD_FILENAME_RE  = re.compile(r'[/\x00-\x1f\x7f]')   # slash + all control chars
_RESERVED_NAMES   = {".", "..", "~"}


def _validate_filename(raw: str) -> str:
    """
    Sanitize and validate a filename string.
    Returns the cleaned filename, or raises ValueError with a clear reason.
    Replaces the old inline strip().lstrip() logic in _safe_path.
    """
    name = raw.strip()                              # FIX 4: strip whitespace
    if not name:
        raise ValueError("Filename cannot be empty.")
    if name in _RESERVED_NAMES:
        raise ValueError(f"'{name}' is a reserved name.")
    if len(name) > _MAX_FILENAME_LEN:
        raise ValueError(f"Filename too long ({len(name)} chars, max {_MAX_FILENAME_LEN}).")
    if _BAD_FILENAME_RE.search(name):              # FIX 4: reject control chars
        raise ValueError(f"Filename '{name}' contains illegal characters.")
    clean = name.lstrip("/").lstrip(".")
    if not clean:
        raise ValueError(f"Filename '{name}' reduces to empty after stripping.")
    return clean


class SandboxedFileStore:
    """
    Provides read/write/list/delete access to a single sandboxed directory.

    v3 new parameter:
      allow_firejail_fallback (bool, default False):
        False — firejail failure returns an error (secure default).
        True  — firejail failure falls back to direct write (v2 behaviour, opt-in).
    """

    def __init__(
        self,
        sandbox_dir:             Path          = DEFAULT_SANDBOX_DIR,
        use_firejail:            Optional[bool] = None,
        allow_firejail_fallback: bool           = False,   # --- NEW (FIX 5)
    ):
        self.sandbox                 = Path(sandbox_dir).resolve()
        self.allow_firejail_fallback = allow_firejail_fallback
        self.sandbox.mkdir(parents=True, exist_ok=True)

        if use_firejail is None:
            self.use_firejail = shutil.which("firejail") is not None
        else:
            self.use_firejail = use_firejail

        backend  = "firejail" if self.use_firejail else "pure-Python"
        fallback = "allowed" if allow_firejail_fallback else "disabled (secure)"
        print(f"  [Sandbox] Directory : {self.sandbox}")
        print(f"  [Sandbox] Backend   : {backend}  (fallback: {fallback})")

    # ------------------------------------------------------------------ path validation

    def _safe_path(self, filename: str) -> Path:
        """
        Validate filename and resolve to an absolute path inside the sandbox.
        v3: delegates to _validate_filename() for FIX 4 checks.
        """
        clean     = _validate_filename(filename)
        candidate = (self.sandbox / clean).resolve()
        try:
            candidate.relative_to(self.sandbox)
        except ValueError:
            raise ValueError(
                f"Path traversal detected: '{filename}' resolves outside the sandbox."
            )
        return candidate

    def _check_extension(self, path: Path) -> None:
        if path.suffix.lower() in BLOCKED_EXTENSIONS:
            raise ValueError(
                f"Extension '{path.suffix}' is not allowed. "
                f"Blocked: {', '.join(sorted(BLOCKED_EXTENSIONS))}"
            )

    # ------------------------------------------------------------------ public operations (UNCHANGED signatures)

    def list_files(self) -> str:
        files = sorted(self.sandbox.iterdir())
        if not files:
            return "The sandbox directory is empty."
        lines = [f"Files in sandbox ({self.sandbox}):"]
        for f in files:
            size     = f.stat().st_size
            size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
            lines.append(f"  {f.name:<40} {size_str}")
        return "\n".join(lines)

    def read_file(self, filename: str) -> str:
        try:
            path = self._safe_path(filename)
        except ValueError as e:
            return f"Error: {e}"
        if not path.exists():
            return f"Error: File '{filename}' does not exist in the sandbox."
        if not path.is_file():
            return f"Error: '{filename}' is not a regular file."
        size = path.stat().st_size
        if size > MAX_READ_BYTES:
            return (
                f"Error: File '{filename}' is {size/1024:.1f} KB, "
                f"exceeds read limit of {MAX_READ_BYTES//1024} KB."
            )
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return f"Error: File '{filename}' does not appear to be a text file."
        except OSError as e:
            return f"Error reading '{filename}': {e}"

    def write_file(self, filename: str, content: str, append: bool = False) -> str:
        try:
            path = self._safe_path(filename)
            self._check_extension(path)
        except ValueError as e:
            return f"Error: {e}"
        if len(content.encode("utf-8")) > MAX_WRITE_BYTES:
            return f"Error: Content exceeds write limit of {MAX_WRITE_BYTES//1024} KB."
        path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if append else "w"
        if self.use_firejail:
            return self._write_with_firejail(path, content, mode)
        return self._write_direct(path, content, mode)

    def delete_file(self, filename: str) -> str:
        try:
            path = self._safe_path(filename)
        except ValueError as e:
            return f"Error: {e}"
        if not path.exists():
            return f"Error: File '{filename}' does not exist in the sandbox."
        if not path.is_file():
            return f"Error: '{filename}' is not a regular file."
        try:
            path.unlink()
            return f"Deleted '{filename}' from the sandbox."
        except OSError as e:
            return f"Error deleting '{filename}': {e}"

    # ------------------------------------------------------------------ write backends

    def _write_direct(self, path: Path, content: str, mode: str) -> str:
        try:
            with open(path, mode, encoding="utf-8") as f:
                f.write(content)
            verb = "Appended to" if mode == "a" else "Wrote"
            return f"{verb} '{path.name}' in sandbox ({len(content)} chars)."
        except OSError as e:
            return f"Error writing '{path.name}': {e}"

    def _write_with_firejail(self, path: Path, content: str, mode: str) -> str:
        """
        Write via firejail-sandboxed Python.
        v3 (FIX 5): failure is logged clearly; fallback requires explicit opt-in.
        """
        import base64
        encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
        helper  = (
            f"import base64; "
            f"content = base64.b64decode('{encoded}').decode('utf-8'); "
            f"open('{path}', '{mode}', encoding='utf-8').write(content); "
            f"print('OK')"
        )
        cmd = [
            "firejail", "--quiet", "--private-tmp", "--noroot",
            "--nosound", "--nodvd", "--no3d",
            f"--whitelist={self.sandbox}", "--read-only=/",
            "python3", "-c", helper,
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, shell=False)
            if result.returncode != 0:
                return self._handle_firejail_failure(
                    path, content, mode,
                    reason=f"exited with code {result.returncode}: {result.stderr.strip()[:200]}"
                )
            verb = "Appended to" if mode == "a" else "Wrote"
            return f"{verb} '{path.name}' in sandbox via firejail ({len(content)} chars)."
        except subprocess.TimeoutExpired:
            logger.warning("[Sandbox] firejail write timed out for %s", path.name)
            return "Error: firejail write timed out."
        except FileNotFoundError:
            return self._handle_firejail_failure(
                path, content, mode, reason="firejail binary not found"
            )
        except Exception as e:
            logger.error("[Sandbox] firejail unexpected error: %s", e)
            return f"Error during firejail write: {e}"

    def _handle_firejail_failure(self, path: Path, content: str, mode: str, reason: str) -> str:
        """
        Central handler for all firejail failure cases (FIX 5).
        Logs clearly, then either falls back or returns an error.
        """
        logger.warning("[Sandbox] firejail failed: %s", reason)
        print(f"  [Sandbox] WARNING: firejail failed — {reason}")
        if self.allow_firejail_fallback:
            print("  [Sandbox] Falling back to direct write (allow_firejail_fallback=True).")
            return self._write_direct(path, content, mode)
        return (
            "Error: firejail write failed and fallback is disabled. "
            f"Reason: {reason}. "
            "Set allow_firejail_fallback=True in SandboxedFileStore to permit "
            "unconfined writes, or fix the firejail configuration."
        )


# ------------------------------------------------------------------ Ollama schema + dispatcher (UNCHANGED)

SANDBOX_FILE_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "sandbox_file",
        "description": (
            "Read, write, list, or delete files inside a secure sandboxed directory. "
            "You can ONLY access files within this sandbox."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["read", "write", "append", "list", "delete"],
                    "description": "list/read/write/append/delete",
                },
                "filename": {
                    "type": "string",
                    "description": "Filename only (no paths). e.g. 'notes.txt'",
                },
                "content": {
                    "type": "string",
                    "description": "Text content for write/append operations.",
                },
            },
            "required": ["operation"],
        },
    },
}


def dispatch_sandbox_file_tool(args: dict, store: SandboxedFileStore) -> str:
    op       = args.get("operation", "").strip().lower()
    filename = args.get("filename",  "")
    content  = args.get("content",   "")

    if op == "list":
        return store.list_files()
    elif op == "read":
        if not filename: return "Error: 'read' requires a 'filename'."
        return store.read_file(filename)
    elif op == "write":
        if not filename: return "Error: 'write' requires a 'filename'."
        if content == "": return "Error: 'write' requires 'content'."
        return store.write_file(filename, content, append=False)
    elif op == "append":
        if not filename: return "Error: 'append' requires a 'filename'."
        if content == "": return "Error: 'append' requires 'content'."
        return store.write_file(filename, content, append=True)
    elif op == "delete":
        if not filename: return "Error: 'delete' requires a 'filename'."
        return store.delete_file(filename)
    else:
        return f"Error: Unknown file operation '{op}'. Use list, read, write, append, or delete."
