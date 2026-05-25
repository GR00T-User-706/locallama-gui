"""
PluginManager — discovers, loads, enables/disables plugins.

Plugins live in the `plugins/` directory.  Each subdirectory that contains
an `__init__.py` (or a single `.py` file) is scanned for BasePlugin subclasses.

Hot reload is supported: call reload_plugin(plugin_id).
"""

import importlib
import importlib.util
import inspect
import logging
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional

from app.plugin_sdk.base_plugin import BasePlugin, ToolDefinition, CommandDefinition

log = logging.getLogger(__name__)


class PluginRecord:
    def __init__(self, plugin: BasePlugin, source_path: Path, module_name: str):
        self.plugin = plugin
        self.source_path = source_path
        self.module_name = module_name
        self.enabled = True
        self.error: Optional[str] = None


class PluginManager:
    def __init__(self, plugins_dir: Path, disabled_ids: List[str] = None):
        self._dir = plugins_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._records: Dict[str, PluginRecord] = {}
        self._disabled_ids = set(disabled_ids or [])
        self._change_listeners: List[Callable] = []
        self._discover_all()

    # ── Discovery ─────────────────────────────────────────────────────────

    def _discover_all(self):
        """Scan plugins directory and load all discovered plugins."""
        # Ensure plugins dir is in sys.path so imports work
        plugins_parent = str(self._dir.parent)
        if plugins_parent not in sys.path:
            sys.path.insert(0, plugins_parent)

        for entry in sorted(self._dir.iterdir()):
            if entry.name.startswith("_") or entry.name.startswith("."):
                continue
            try:
                if entry.is_dir() and (entry / "__init__.py").exists():
                    self._load_package(entry)
                elif entry.is_file() and entry.suffix == ".py":
                    self._load_module_file(entry)
            except Exception as e:
                log.error("Plugin discovery error for %s: %s", entry.name, e)

    def _load_package(self, package_dir: Path):
        mod_name = f"plugins.{package_dir.name}"
        self._load_module_name(mod_name, package_dir / "__init__.py")

    def _load_module_file(self, file_path: Path):
        mod_name = f"plugins._file_{file_path.stem}"
        self._load_module_name(mod_name, file_path)

    def _load_module_name(self, mod_name: str, source_path: Path):
        """Import a module and register any BasePlugin subclasses found."""
        try:
            spec = importlib.util.spec_from_file_location(mod_name, source_path)
            if spec is None or spec.loader is None:
                return
            module = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = module
            spec.loader.exec_module(module)

            for _name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BasePlugin)
                        and obj is not BasePlugin
                        and obj.PLUGIN_ID):
                    self._register_plugin_class(obj, source_path, mod_name)
        except Exception as e:
            log.error("Failed to load plugin module %s: %s", mod_name, e, exc_info=True)

    def _register_plugin_class(self, cls: type, source: Path, mod_name: str):
        plugin_id = cls.PLUGIN_ID
        if plugin_id in self._records:
            log.debug("Plugin %s already registered, skipping.", plugin_id)
            return
        try:
            instance = cls()
            record = PluginRecord(instance, source, mod_name)
            record.enabled = plugin_id not in self._disabled_ids
            self._records[plugin_id] = record

            if record.enabled:
                instance.on_load()
                log.info("Plugin loaded: %s v%s", cls.PLUGIN_NAME, cls.PLUGIN_VERSION)
            else:
                log.debug("Plugin disabled: %s", plugin_id)
        except Exception as e:
            log.error("Error instantiating plugin %s: %s", plugin_id, e, exc_info=True)
            record = PluginRecord.__new__(PluginRecord)
            record.source_path = source
            record.module_name = mod_name
            record.enabled = False
            record.error = str(e)
            # Create a dummy instance to display in UI
            record.plugin = _DummyPlugin(plugin_id, str(e))
            self._records[plugin_id] = record

    # ── Queries ───────────────────────────────────────────────────────────

    def list_all(self) -> List[PluginRecord]:
        return list(self._records.values())

    def get(self, plugin_id: str) -> Optional[PluginRecord]:
        return self._records.get(plugin_id)

    def get_enabled_plugins(self) -> List[BasePlugin]:
        return [r.plugin for r in self._records.values() if r.enabled]

    def all_tools(self) -> List[ToolDefinition]:
        tools = []
        for r in self._records.values():
            if r.enabled:
                try:
                    tools.extend(r.plugin.get_tools())
                except Exception as e:
                    log.warning("Error getting tools from %s: %s",
                                r.plugin.PLUGIN_ID, e)
        return tools

    def all_commands(self) -> List[CommandDefinition]:
        cmds = []
        for r in self._records.values():
            if r.enabled:
                try:
                    cmds.extend(r.plugin.get_commands())
                except Exception as e:
                    log.warning("Error getting commands from %s: %s",
                                r.plugin.PLUGIN_ID, e)
        return cmds

    # ── Enable / Disable ──────────────────────────────────────────────────

    def enable(self, plugin_id: str) -> bool:
        r = self._records.get(plugin_id)
        if r and not r.enabled:
            r.enabled = True
            self._disabled_ids.discard(plugin_id)
            try:
                r.plugin.on_load()
            except Exception as e:
                log.error("Error on enable for %s: %s", plugin_id, e)
            self._notify_change()
            return True
        return False

    def disable(self, plugin_id: str) -> bool:
        r = self._records.get(plugin_id)
        if r and r.enabled:
            r.enabled = False
            self._disabled_ids.add(plugin_id)
            try:
                r.plugin.on_unload()
            except Exception as e:
                log.error("Error on disable for %s: %s", plugin_id, e)
            self._notify_change()
            return True
        return False

    def reload_plugin(self, plugin_id: str) -> bool:
        r = self._records.get(plugin_id)
        if not r:
            return False
        mod_name = r.module_name
        was_enabled = r.enabled
        try:
            r.plugin.on_unload()
        except Exception:
            pass
        # Remove from sys.modules so it reloads fresh
        to_remove = [k for k in sys.modules if k == mod_name or k.startswith(mod_name + ".")]
        for k in to_remove:
            del sys.modules[k]
        del self._records[plugin_id]

        self._load_module_name(mod_name, r.source_path)
        new_r = self._records.get(plugin_id)
        if new_r:
            new_r.enabled = was_enabled
            if was_enabled:
                try:
                    new_r.plugin.on_load()
                except Exception as e:
                    log.error("Error on reload for %s: %s", plugin_id, e)
            self._notify_change()
            log.info("Plugin reloaded: %s", plugin_id)
            return True
        return False

    def reload_all(self):
        for pid in list(self._records.keys()):
            self.reload_plugin(pid)

    def install_from_file(self, source_path: Path) -> bool:
        """Copy a .py file or directory into the plugins folder and load it."""
        import shutil
        try:
            dest = self._dir / source_path.name
            if source_path.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(source_path, dest)
                self._load_package(dest)
            else:
                shutil.copy2(source_path, dest)
                self._load_module_file(dest)
            self._notify_change()
            return True
        except Exception as e:
            log.error("Install from file failed: %s", e)
            return False

    def get_disabled_ids(self) -> List[str]:
        return list(self._disabled_ids)

    # ── Chat interceptors ─────────────────────────────────────────────────

    def intercept_message(self, message: dict) -> dict:
        for r in self._records.values():
            if r.enabled:
                try:
                    result = r.plugin.on_chat_message(message)
                    if result is not None:
                        message = result
                except Exception as e:
                    log.warning("Plugin intercept_message error %s: %s",
                                r.plugin.PLUGIN_ID, e)
        return message

    def intercept_response(self, response: str) -> str:
        for r in self._records.values():
            if r.enabled:
                try:
                    result = r.plugin.on_chat_response(response)
                    if result is not None:
                        response = result
                except Exception as e:
                    log.warning("Plugin intercept_response error %s: %s",
                                r.plugin.PLUGIN_ID, e)
        return response

    # ── Observer ──────────────────────────────────────────────────────────

    def add_change_listener(self, fn: Callable):
        self._change_listeners.append(fn)

    def remove_change_listener(self, fn: Callable):
        self._change_listeners = [l for l in self._change_listeners if l is not fn]

    def _notify_change(self):
        for fn in self._change_listeners:
            try:
                fn()
            except Exception as e:
                log.warning("Plugin change listener error: %s", e)

    def shutdown(self):
        for r in self._records.values():
            if r.enabled:
                try:
                    r.plugin.on_unload()
                except Exception as e:
                    log.warning("Plugin on_unload error %s: %s",
                                r.plugin.PLUGIN_ID, e)


class _DummyPlugin(BasePlugin):
    """Placeholder for plugins that failed to load."""
    def __init__(self, plugin_id: str, error: str):
        super().__init__()
        self.PLUGIN_ID = plugin_id
        self.PLUGIN_NAME = f"[ERROR] {plugin_id}"
        self.PLUGIN_DESC = f"Failed to load: {error}"
        self.PLUGIN_VERSION = "?"
        self.PLUGIN_AUTHOR = ""
