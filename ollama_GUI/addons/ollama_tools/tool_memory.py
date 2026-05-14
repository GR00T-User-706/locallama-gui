#!/usr/bin/env python3
"""
tool_memory.py  (v3)
--------------------
Persistent memory tool for Ollama LLMs.

v3 changes (surgical, backward-compatible):
  FIX 1     — Memory poisoning mitigation: entries carry 'source' and
               'trusted' metadata; all_as_context() labels untrusted entries.
  UPGRADE 2 — Structured state memory: remember_struct / recall_struct /
               forget_struct store JSON objects under a reserved key,
               leaving the existing k/v system completely intact.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_MEMORY_DIR  = Path.home() / ".ollama_tools"
DEFAULT_MEMORY_FILE = DEFAULT_MEMORY_DIR / "memory.json"

# Reserved key used to store structured entries inside the namespace dict.
_STRUCT_KEY = "__structured__"


class MemoryStore:
    """
    Persistent key/value store backed by a JSON file.
    All existing public methods are unchanged in signature and behaviour.
    """

    def __init__(self, path: Path = DEFAULT_MEMORY_FILE, namespace: str = "default"):
        self.path      = Path(path)
        self.namespace = namespace
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, Any] = self._load()

    # ------------------------------------------------------------------ internal

    def _load(self) -> Dict[str, Any]:
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)
        tmp.replace(self.path)

    def _ns(self) -> Dict[str, Any]:
        if self.namespace not in self._data:
            self._data[self.namespace] = {}
        return self._data[self.namespace]

    # ------------------------------------------------------------------ public k/v API (UNCHANGED signatures)

    def remember(self, key: str, value: str,
                 source: str = "user", trusted: bool = False) -> str:
        """
        Store a key/value pair.
        v3: entries now include 'source' and 'trusted' fields (FIX 1).
        Old callers that omit these get safe defaults (source=user, trusted=False).
        """
        key = key.strip()
        if not key:
            return "Error: key cannot be empty."
        self._ns()[key] = {
            "value":   value,
            "updated": datetime.now().isoformat(timespec="seconds"),
            "source":  source,    # --- NEW (FIX 1)
            "trusted": trusted,   # --- NEW (FIX 1)
        }
        self._save()
        return f"Remembered: '{key}' = '{value}'"

    def recall(self, key: Optional[str] = None) -> str:
        """Retrieve a value by key, or list all keys."""
        ns = self._ns()
        if not key or key.strip() == "":
            if not ns:
                return "Memory is empty — nothing has been stored yet."
            lines = ["Stored memory keys:"]
            for k, entry in ns.items():
                if k == _STRUCT_KEY:
                    continue
                trust = "trusted" if entry.get("trusted") else "unverified"
                lines.append(f"  • {k}  [{trust}]  (last updated: {entry.get('updated','?')})")
            return "\n".join(lines)
        key = key.strip()
        if key not in ns:
            return f"Nothing stored for key '{key}'."
        entry = ns[key]
        trust = "trusted" if entry.get("trusted") else "unverified"
        return f"{key}: {entry['value']}  [{trust}]  (stored: {entry.get('updated','?')})"

    def forget(self, key: str) -> str:
        """Delete a key from memory."""
        key = key.strip()
        ns  = self._ns()
        if key not in ns:
            return f"Key '{key}' was not found in memory — nothing to forget."
        del ns[key]
        self._save()
        return f"Forgot '{key}'."

    def all_as_context(self) -> str:
        """
        Return all stored memory as a string for the system prompt.
        v3 (FIX 1): untrusted entries carry a '[User-provided, not verified]' label.
        """
        ns    = self._ns()
        plain = {k: v for k, v in ns.items() if k != _STRUCT_KEY}
        if not plain:
            return ""
        lines = ["[Persistent Memory]"]
        for k, entry in plain.items():
            label = "" if entry.get("trusted") else "  [User-provided, not verified]"
            lines.append(f"  {k}: {entry['value']}{label}")
        return "\n".join(lines)

    # ------------------------------------------------------------------ NEW (UPGRADE 2): structured state

    def _struct_ns(self) -> Dict[str, Any]:
        ns = self._ns()
        if _STRUCT_KEY not in ns:
            ns[_STRUCT_KEY] = {}
        return ns[_STRUCT_KEY]

    def remember_struct(self, name: str, obj: dict) -> str:
        """Store a named JSON object (e.g. project state)."""
        name = name.strip()
        if not name:
            return "Error: structured entry name cannot be empty."
        if not isinstance(obj, dict):
            return "Error: structured entry must be a JSON object (dict)."
        self._struct_ns()[name] = {
            "data":    obj,
            "updated": datetime.now().isoformat(timespec="seconds"),
        }
        self._save()
        return f"Stored structured entry '{name}'."

    def recall_struct(self, name: Optional[str] = None) -> str:
        """Retrieve a named structured entry, or list all names."""
        sn = self._struct_ns()
        if not name or name.strip() == "":
            if not sn:
                return "No structured entries stored yet."
            lines = ["Structured memory entries:"]
            for k, entry in sn.items():
                lines.append(f"  • {k}  (updated: {entry.get('updated','?')})")
            return "\n".join(lines)
        name = name.strip()
        if name not in sn:
            return f"No structured entry named '{name}'."
        return json.dumps(sn[name]["data"], indent=2, ensure_ascii=False)

    def forget_struct(self, name: str) -> str:
        """Delete a named structured entry."""
        name = name.strip()
        sn   = self._struct_ns()
        if name not in sn:
            return f"No structured entry named '{name}' — nothing to forget."
        del sn[name]
        self._save()
        return f"Forgot structured entry '{name}'."

    def struct_as_context(self) -> str:
        """Return structured entries as a compact string for the system prompt."""
        sn = self._struct_ns()
        if not sn:
            return ""
        lines = ["[Structured State Memory]"]
        for name, entry in sn.items():
            lines.append(f"  {name}: {json.dumps(entry['data'], ensure_ascii=False)}")
        return "\n".join(lines)


# ------------------------------------------------------------------ Ollama schema

MEMORY_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "memory",
        "description": (
            "Manage your persistent memory across conversations. "
            "Simple key/value: use 'remember', 'recall', 'forget'. "
            "Structured JSON state: use 'remember_struct', 'recall_struct', 'forget_struct'. "
            "Use memory proactively when the user tells you to remember something, "
            "or when you need to track project state across turns."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["remember", "recall", "forget",
                             "remember_struct", "recall_struct", "forget_struct"],
                    "description": (
                        "remember/recall/forget — simple key/value pairs.\n"
                        "remember_struct/recall_struct/forget_struct — named JSON objects."
                    ),
                },
                "key":   {"type": "string", "description": "Key name for k/v operations."},
                "value": {"type": "string", "description": "Value to store (k/v only)."},
                "name":  {"type": "string", "description": "Entry name for structured operations."},
                "data":  {"type": "object", "description": "JSON object to store (structured only)."},
            },
            "required": ["operation"],
        },
    },
}


def dispatch_memory_tool(args: dict, store: MemoryStore) -> str:
    op    = args.get("operation", "").strip().lower()
    key   = args.get("key",   "")
    value = args.get("value", "")
    name  = args.get("name",  "")
    data  = args.get("data",  {})

    if op == "remember":
        if not key:   return "Error: 'remember' requires a 'key'."
        if not value: return "Error: 'remember' requires a 'value'."
        return store.remember(key, value)
    elif op == "recall":
        return store.recall(key or None)
    elif op == "forget":
        if not key: return "Error: 'forget' requires a 'key'."
        return store.forget(key)
    elif op == "remember_struct":
        if not name:              return "Error: 'remember_struct' requires a 'name'."
        if not isinstance(data, dict): return "Error: 'remember_struct' requires a 'data' object."
        return store.remember_struct(name, data)
    elif op == "recall_struct":
        return store.recall_struct(name or None)
    elif op == "forget_struct":
        if not name: return "Error: 'forget_struct' requires a 'name'."
        return store.forget_struct(name)
    else:
        return f"Error: Unknown memory operation '{op}'."
