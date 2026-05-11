#!/usr/bin/env python3
"""
tool_context_builder.py  (v4 — NEW FILE)
------------------------------------------
Context Builder Tool for Ollama LLMs.

Provides read-only context aggregation from memory and sandbox files.
The LLM can use this to pull relevant information into its working context
without directly accessing the filesystem or memory store internals.

Operations:
  fetch_memory_context  — return all memory entries as formatted context
  fetch_file_context    — return contents of a sandbox file (read-only)
  summarize_context     — return a trimmed combined context snapshot

Constraints:
  - Read-only: no writes, no deletes
  - Output size limited (MAX_OUTPUT_CHARS)
  - No raw filesystem traversal outside sandbox
  - No shell calls
"""

from pathlib import Path
from typing import Optional

MAX_OUTPUT_CHARS   = 4_000    # max chars returned in any single context fetch
MAX_FILE_READ_BYTES = 32 * 1024  # 32 KB


class ContextBuilderStore:
    """
    Aggregates context from MemoryStore and SandboxedFileStore.
    Holds references to the existing stores — does NOT duplicate data.
    """

    def __init__(self, memory_store, sandbox_store):
        """
        memory_store  : MemoryStore instance (from tool_memory.py)
        sandbox_store : SandboxedFileStore instance (from tool_sandbox_files.py)
        """
        self.memory  = memory_store
        self.sandbox = sandbox_store

    # ------------------------------------------------------------------ operations

    def fetch_memory_context(self) -> str:
        """Return all memory (k/v + structured) as formatted context."""
        parts = []
        kv_ctx     = self.memory.all_as_context()
        struct_ctx = self.memory.struct_as_context()
        if kv_ctx:     parts.append(kv_ctx)
        if struct_ctx: parts.append(struct_ctx)
        if not parts:
            return "Memory is empty — nothing has been stored yet."
        result = "\n\n".join(parts)
        return _trim(result, MAX_OUTPUT_CHARS)

    def fetch_file_context(self, filename: str) -> str:
        """Return the contents of a sandbox file (read-only)."""
        filename = (filename or "").strip()
        if not filename:
            return "Error: 'fetch_file_context' requires a filename."
        # Delegate to the existing sandbox store's read_file which already
        # enforces path validation and size limits.
        result = self.sandbox.read_file(filename)
        return _trim(result, MAX_OUTPUT_CHARS)

    def summarize_context(self, max_chars: int = MAX_OUTPUT_CHARS) -> str:
        """
        Return a combined snapshot of memory + sandbox file listing,
        trimmed to max_chars.
        """
        max_chars = min(max(100, max_chars), MAX_OUTPUT_CHARS)
        parts = []

        kv_ctx     = self.memory.all_as_context()
        struct_ctx = self.memory.struct_as_context()
        file_list  = self.sandbox.list_files()

        if kv_ctx:     parts.append(kv_ctx)
        if struct_ctx: parts.append(struct_ctx)
        if file_list:  parts.append(f"[Sandbox Files]\n{file_list}")

        if not parts:
            return "No context available — memory is empty and sandbox has no files."

        combined = "\n\n".join(parts)
        return _trim(combined, max_chars)


def _trim(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n\n[...output trimmed at {max_chars} chars]"


# ------------------------------------------------------------------
# Ollama tool schema
# ------------------------------------------------------------------

CONTEXT_BUILDER_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "context_builder",
        "description": (
            "Retrieve relevant context from memory and sandbox files. "
            "Use this to pull in what you know before answering complex questions. "
            "All access is read-only."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["fetch_memory_context", "fetch_file_context", "summarize_context"],
                    "description": (
                        "fetch_memory_context — return all stored memory.\n"
                        "fetch_file_context   — return contents of a sandbox file.\n"
                        "summarize_context    — return a combined memory + file listing snapshot."
                    ),
                },
                "filename": {
                    "type": "string",
                    "description": "Filename to read (fetch_file_context only).",
                },
                "max_chars": {
                    "type": "integer",
                    "description": f"Max output characters (summarize_context only, max {MAX_OUTPUT_CHARS}).",
                },
            },
            "required": ["operation"],
        },
    },
}


def dispatch_context_builder_tool(args: dict, store: ContextBuilderStore) -> str:
    op = args.get("operation", "").strip().lower()
    try:
        if op == "fetch_memory_context":
            return store.fetch_memory_context()
        elif op == "fetch_file_context":
            return store.fetch_file_context(args.get("filename", ""))
        elif op == "summarize_context":
            return store.summarize_context(args.get("max_chars", MAX_OUTPUT_CHARS))
        else:
            return f"Error: Unknown context_builder operation '{op}'."
    except Exception as e:
        return f"Error: {e}"
