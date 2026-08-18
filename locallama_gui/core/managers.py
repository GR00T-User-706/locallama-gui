from __future__ import annotations

import ast
import importlib.util
import json
import shutil
from dataclasses import asdict
from pathlib import Path
from types import ModuleType
from typing import Any, Protocol

from locallama_gui.core.config import AppConfig
from locallama_gui.core.domain import AgentProfile, ChatSession, PromptRecord, now_iso


class SessionManager:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def list_sessions(self) -> list[ChatSession]:
        sessions = []
        for path in sorted(self.config.paths.sessions_dir.glob("*.json"), reverse=True):
            try:
                sessions.append(ChatSession.from_file(path))
            except (json.JSONDecodeError, TypeError, OSError):
                continue
        return sessions

    def load(self, session_id: str) -> ChatSession:
        return ChatSession.from_file(self.config.paths.sessions_dir / f"{session_id}.json")

    def save(self, session: ChatSession) -> Path:
        return session.save(self.config.paths.sessions_dir)

    def import_session(self, path: Path) -> ChatSession:
        session = ChatSession.from_file(path)
        session.save(self.config.paths.sessions_dir)
        return session


class PromptManager:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.path = config.paths.prompts_dir / "prompts.json"
        if not self.path.exists():
            self.save_all([])

    def list(self) -> list[PromptRecord]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [PromptRecord(**item) for item in data]

    def save_all(self, prompts: list[PromptRecord]) -> None:
        self.path.write_text(json.dumps([asdict(p) for p in prompts], indent=2), encoding="utf-8")

    def upsert(self, prompt: PromptRecord) -> None:
        prompts = self.list()
        for idx, existing in enumerate(prompts):
            if existing.id == prompt.id:
                prompt.versions = existing.versions + [{"at": existing.updated_at, "content": existing.content}]
                prompt.updated_at = now_iso()
                prompts[idx] = prompt
                self.save_all(prompts)
                return
        prompts.append(prompt)
        self.save_all(prompts)

    def delete(self, prompt_id: str) -> None:
        self.save_all([p for p in self.list() if p.id != prompt_id])

    def import_file(self, path: Path, category: str = "Imported") -> PromptRecord:
        prompt = PromptRecord(title=path.stem, content=path.read_text(encoding="utf-8"), category=category)
        self.upsert(prompt)
        return prompt

    def export(self, path: Path) -> None:
        shutil.copyfile(self.path, path)


class AgentManager:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.path = config.paths.agents_dir / "agents.json"
        if not self.path.exists():
            self.save_all([])

    def list(self) -> list[AgentProfile]:
        return [AgentProfile(**item) for item in json.loads(self.path.read_text(encoding="utf-8"))]

    def save_all(self, agents: list[AgentProfile]) -> None:
        self.path.write_text(json.dumps([asdict(a) for a in agents], indent=2), encoding="utf-8")

    def upsert(self, agent: AgentProfile) -> None:
        agents = self.list()
        for idx, existing in enumerate(agents):
            if existing.id == agent.id:
                agents[idx] = agent
                self.save_all(agents)
                return
        agents.append(agent)
        self.save_all(agents)


class PluginAPI(Protocol):
    manifest: dict[str, Any]

    def activate(self, context: PluginContext) -> None: ...

    def deactivate(self) -> None: ...


class PluginContext:
    def __init__(self, main_window: Any, config: AppConfig) -> None:
        self.main_window = main_window
        self.config = config
        self.tools: dict[str, Any] = {}
        self.commands: dict[str, Any] = {}
        self.chat_interceptors: list[Any] = []
        self.memory_providers: dict[str, Any] = {}

    def register_tool(self, name: str, callable_: Any) -> None:
        self.tools[name] = callable_

    def register_command(self, name: str, callable_: Any) -> None:
        self.commands[name] = callable_

    def register_chat_interceptor(self, callable_: Any) -> None:
        self.chat_interceptors.append(callable_)

    def add_panel(self, title: str, widget: Any, area: Any = None) -> None:
        self.main_window.add_plugin_panel(title, widget, area)


class LoadedPlugin:
    def __init__(self, path: Path, module: ModuleType, instance: Any) -> None:
        self.path = path
        self.module = module
        self.instance = instance
        self.manifest = getattr(instance, "manifest", {"id": path.stem, "name": path.stem})


class PluginManager:
    def __init__(self, config: AppConfig, context: PluginContext) -> None:
        self.config = config
        self.context = context
        self.loaded: dict[str, LoadedPlugin] = {}

    def _validate_manifest(self, manifest: dict[str, Any], path: Path) -> dict[str, Any]:
        required = ("id", "name", "version")
        missing = [key for key in required if not manifest.get(key)]
        if missing:
            raise ValueError(f"Plugin {path.name} manifest missing required keys: {', '.join(missing)}")
        return manifest

    def _read_static_manifest(self, path: Path) -> dict[str, Any]:
        """Read a Plugin.manifest literal without importing or executing plugin code."""
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef) or node.name != "Plugin":
                continue
            for statement in node.body:
                value_node: ast.expr | None = None
                if isinstance(statement, ast.Assign):
                    if any(isinstance(target, ast.Name) and target.id == "manifest" for target in statement.targets):
                        value_node = statement.value
                elif (
                    isinstance(statement, ast.AnnAssign)
                    and isinstance(statement.target, ast.Name)
                    and statement.target.id == "manifest"
                ):
                    value_node = statement.value
                if value_node is not None:
                    try:
                        manifest = ast.literal_eval(value_node)
                    except (ValueError, SyntaxError) as exc:
                        raise ValueError(
                            f"Plugin {path.name} manifest must be a static literal dictionary"
                        ) from exc
                    if not isinstance(manifest, dict):
                        raise ValueError(f"Plugin {path.name} manifest must be a dictionary")
                    return self._validate_manifest(manifest, path)
        raise ValueError(f"Plugin {path.name} must define a static Plugin.manifest dictionary")

    def plugin_paths(self) -> list[Path]:
        paths = list(self.config.paths.plugins_dir.glob("*.py"))
        if self.config.developer_mode:
            repo_plugins = Path.cwd() / "plugins"
            if repo_plugins.exists():
                paths.extend(repo_plugins.glob("*.py"))
        return sorted(set(paths))

    def discover(self) -> list[dict[str, Any]]:
        discovered = []
        for path in self.plugin_paths():
            manifest = {"id": path.stem, "name": path.stem, "path": str(path)}
            try:
                manifest.update(self._read_static_manifest(path))
            except Exception as exc:  # noqa: BLE001 - discovery must isolate invalid plugins
                manifest["error"] = str(exc)
            discovered.append(manifest)
        return discovered

    def load_enabled(self) -> None:
        for path in self.plugin_paths():
            try:
                manifest = self._read_static_manifest(path)
            except Exception:  # noqa: BLE001, S112 - one invalid plugin must not block startup
                continue
            if self.config.enabled_plugins.get(manifest["id"], False):
                try:
                    self.enable(path)
                except (PermissionError, ImportError, RuntimeError, ValueError):
                    continue

    def trust(self, plugin_id: str) -> None:
        if not any(p.get("id") == plugin_id and not p.get("error") for p in self.discover()):
            raise ValueError(f"Plugin '{plugin_id}' is not a valid discovered plugin")
        if plugin_id not in self.config.trusted_plugins:
            self.config.trusted_plugins.append(plugin_id)
            self.config.save()

    def untrust(self, plugin_id: str) -> None:
        self.disable(plugin_id)
        if plugin_id in self.config.trusted_plugins:
            self.config.trusted_plugins.remove(plugin_id)
        self.config.save()

    def enable(self, path: Path) -> None:
        manifest = self._read_static_manifest(path)
        plugin_id = manifest["id"]
        if plugin_id not in self.config.trusted_plugins:
            raise PermissionError(f"Plugin '{plugin_id}' is not trusted. Add it to trusted_plugins before enabling.")

        module = self._load_module(path)
        cls = getattr(module, "Plugin", None)
        if cls is None:
            raise ValueError(f"Plugin {path.name} does not define a Plugin class")
        instance = cls()
        runtime_manifest = self._validate_manifest(getattr(instance, "manifest", {}), path)
        if runtime_manifest.get("id") != plugin_id:
            raise ValueError(f"Plugin {path.name} manifest ID changed between discovery and load")
        instance.activate(self.context)
        self.loaded[plugin_id] = LoadedPlugin(path, module, instance)
        self.config.enabled_plugins[plugin_id] = True
        self.config.save()

    def disable(self, plugin_id: str) -> None:
        loaded = self.loaded.pop(plugin_id, None)
        if loaded:
            loaded.instance.deactivate()
        self.config.enabled_plugins[plugin_id] = False
        self.config.save()

    def reload(self) -> None:
        enabled_plugin_ids = [
            plugin_id
            for plugin_id in self.loaded
            if self.config.enabled_plugins.get(plugin_id, False)
        ]
        for plugin_id in list(self.loaded):
            self.disable(plugin_id)
        for plugin_id in enabled_plugin_ids:
            self.config.enabled_plugins[plugin_id] = True
        self.config.save()
        self.load_enabled()

    def remove(self, plugin_id: str) -> None:
        loaded = self.loaded.get(plugin_id)
        path = loaded.path if loaded else None
        if path is None:
            for item in self.discover():
                if item.get("id") == plugin_id:
                    path = Path(item["path"])
                    break
        self.untrust(plugin_id)
        self.config.enabled_plugins.pop(plugin_id, None)
        self.config.save()
        if path is not None and path.exists():
            path.unlink()

    def _load_module(self, path: Path) -> ModuleType:
        spec = importlib.util.spec_from_file_location(f"locallama_user_plugin_{path.stem}", path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load plugin at {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
