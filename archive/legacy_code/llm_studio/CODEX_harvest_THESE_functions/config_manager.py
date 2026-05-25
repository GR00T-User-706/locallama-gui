"""
ConfigManager — persistent JSON-backed settings store.

All application settings live under ~/.llm_studio/config.json.
The manager exposes typed get/set helpers and emits change signals
through a lightweight observer pattern so UI panels can react.
"""

import json
import logging
import copy
from pathlib import Path
from typing import Any, Callable, Dict, List

log = logging.getLogger(__name__)

DEFAULT_CONFIG: Dict[str, Any] = {
    # ── Backend / API ─────────────────────────────────────────────────────
    "backends": {
        "ollama": {
            "base_url": "http://localhost:11434",
            "api_key": "",
            "enabled": True,
        },
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "api_key": "",
            "enabled": False,
        },
    },
    "active_backend": "ollama",
    "active_model": "",

    # ── Generation parameters ─────────────────────────────────────────────
    "parameters": {
        "temperature": 0.7,
        "top_k": 40,
        "top_p": 0.9,
        "min_p": 0.0,
        "repeat_penalty": 1.1,
        "repeat_last_n": 64,
        "mirostat": 0,
        "mirostat_eta": 0.1,
        "mirostat_tau": 5.0,
        "tfs_z": 1.0,
        "num_predict": -1,
        "seed": -1,
        "stop": [],
        "num_ctx": 4096,
        "num_batch": 512,
        "num_gpu": -1,
    },

    # ── Reasoning/mode ────────────────────────────────────────────────────
    "reasoning_mode": "normal",   # normal | thinking | plan
    "streaming_enabled": True,

    # ── UI ────────────────────────────────────────────────────────────────
    "theme": "dark",
    "font_size": 13,
    "window_geometry": None,
    "dock_state": None,
    "active_tab_index": 0,

    # ── Paths ─────────────────────────────────────────────────────────────
    "sessions_dir": "",           # resolved at runtime
    "plugins_dir": "",            # resolved at runtime
    "prompts_dir": "",

    # ── Plugins ───────────────────────────────────────────────────────────
    "disabled_plugins": [],
    "developer_mode": False,

    # ── Keyboard shortcuts ────────────────────────────────────────────────
    "shortcuts": {
        "new_chat": "Ctrl+N",
        "send_message": "Ctrl+Return",
        "stop_generation": "Escape",
        "toggle_sidebar": "Ctrl+B",
        "open_settings": "Ctrl+,",
    },

    # ── Parameter presets ─────────────────────────────────────────────────
    "parameter_presets": {
        "Default": {
            "temperature": 0.7, "top_k": 40, "top_p": 0.9,
            "repeat_penalty": 1.1, "num_predict": -1,
        },
        "Creative": {
            "temperature": 1.2, "top_k": 80, "top_p": 0.95,
            "repeat_penalty": 1.05, "num_predict": -1,
        },
        "Precise": {
            "temperature": 0.2, "top_k": 10, "top_p": 0.7,
            "repeat_penalty": 1.15, "num_predict": -1,
        },
        "Coding": {
            "temperature": 0.1, "top_k": 20, "top_p": 0.8,
            "repeat_penalty": 1.1, "num_predict": 2048,
        },
    },
}


class ConfigManager:
    """Thread-safe (read-write in Qt main thread only) settings manager."""

    def __init__(self):
        self._base_dir = Path.home() / ".llm_studio"
        self._config_path = self._base_dir / "config.json"
        self._listeners: Dict[str, List[Callable]] = {}
        self._data: Dict[str, Any] = {}
        self._load()

    # ── Internal ──────────────────────────────────────────────────────────

    def _resolve_paths(self):
        if not self._data["sessions_dir"]:
            self._data["sessions_dir"] = str(self._base_dir / "sessions")
        if not self._data["plugins_dir"]:
            self._data["plugins_dir"] = str(
                Path(__file__).parent.parent.parent / "plugins"
            )
        if not self._data["prompts_dir"]:
            self._data["prompts_dir"] = str(self._base_dir / "prompts")
        # Ensure dirs exist
        for key in ("sessions_dir", "plugins_dir", "prompts_dir"):
            Path(self._data[key]).mkdir(parents=True, exist_ok=True)

    def _load(self):
        self._data = copy.deepcopy(DEFAULT_CONFIG)
        if self._config_path.exists():
            try:
                with open(self._config_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                self._deep_merge(self._data, saved)
                log.debug("Config loaded from %s", self._config_path)
            except Exception as e:
                log.warning("Could not load config (%s); using defaults.", e)
        self._resolve_paths()

    def _deep_merge(self, base: dict, override: dict):
        for k, v in override.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                self._deep_merge(base[k], v)
            else:
                base[k] = v

    # ── Public API ────────────────────────────────────────────────────────

    def save(self):
        self._base_dir.mkdir(parents=True, exist_ok=True)
        try:
            with open(self._config_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2)
            log.debug("Config saved.")
        except Exception as e:
            log.error("Failed to save config: %s", e)

    def get(self, key: str, default: Any = None) -> Any:
        """Dot-notation key access: get('backends.ollama.base_url')."""
        parts = key.split(".")
        node = self._data
        for p in parts:
            if isinstance(node, dict) and p in node:
                node = node[p]
            else:
                return default
        return node

    def set(self, key: str, value: Any, save: bool = True):
        """Set by dot-notation key and optionally persist."""
        parts = key.split(".")
        node = self._data
        for p in parts[:-1]:
            node = node.setdefault(p, {})
        node[parts[-1]] = value
        if save:
            self.save()
        self._notify(key, value)

    def get_all(self) -> Dict[str, Any]:
        return copy.deepcopy(self._data)

    # ── Convenience shortcuts ─────────────────────────────────────────────

    @property
    def active_backend(self) -> str:
        return self._data.get("active_backend", "ollama")

    @active_backend.setter
    def active_backend(self, value: str):
        self.set("active_backend", value)

    @property
    def active_model(self) -> str:
        return self._data.get("active_model", "")

    @active_model.setter
    def active_model(self, value: str):
        self.set("active_model", value)

    @property
    def parameters(self) -> Dict[str, Any]:
        return copy.deepcopy(self._data["parameters"])

    def update_parameters(self, params: Dict[str, Any]):
        self._data["parameters"].update(params)
        self.save()
        self._notify("parameters", self._data["parameters"])

    @property
    def sessions_dir(self) -> Path:
        return Path(self._data["sessions_dir"])

    @property
    def plugins_dir(self) -> Path:
        return Path(self._data["plugins_dir"])

    @property
    def prompts_dir(self) -> Path:
        return Path(self._data["prompts_dir"])

    @property
    def streaming_enabled(self) -> bool:
        return bool(self._data.get("streaming_enabled", True))

    @streaming_enabled.setter
    def streaming_enabled(self, value: bool):
        self.set("streaming_enabled", value)

    def get_backend_config(self, name: str = None) -> Dict[str, Any]:
        name = name or self.active_backend
        return copy.deepcopy(self._data["backends"].get(name, {}))

    def set_backend_config(self, name: str, config: Dict[str, Any]):
        self._data["backends"][name] = config
        self.save()
        self._notify(f"backends.{name}", config)

    # ── Observer ──────────────────────────────────────────────────────────

    def on_change(self, key: str, callback: Callable):
        """Register a callback for when a config key changes."""
        self._listeners.setdefault(key, []).append(callback)

    def off_change(self, key: str, callback: Callable):
        if key in self._listeners:
            self._listeners[key] = [c for c in self._listeners[key] if c is not callback]

    def _notify(self, key: str, value: Any):
        for cb in self._listeners.get(key, []):
            try:
                cb(value)
            except Exception as e:
                log.warning("Config listener error for key %s: %s", key, e)
        # Also notify wildcard listeners
        for cb in self._listeners.get("*", []):
            try:
                cb(key, value)
            except Exception as e:
                log.warning("Wildcard config listener error: %s", e)
