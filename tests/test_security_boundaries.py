import json
from pathlib import Path

import pytest

from locallama_gui.core.config import AppConfig, AppPaths, CredentialStore, ProviderProfile
from locallama_gui.core.managers import PluginContext, PluginManager


def _paths(tmp_path: Path) -> AppPaths:
    paths = AppPaths(
        config_dir=tmp_path / "config",
        data_dir=tmp_path / "data",
        logs_dir=tmp_path / "logs",
        sessions_dir=tmp_path / "data" / "sessions",
        prompts_dir=tmp_path / "data" / "prompts",
        agents_dir=tmp_path / "data" / "agents",
        modelfiles_dir=tmp_path / "data" / "modelfiles",
        plugins_dir=tmp_path / "data" / "plugins",
    )
    for path in vars(paths).values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def test_api_key_is_not_serialized_to_config(monkeypatch, tmp_path):
    stored = {}
    monkeypatch.setattr(
        CredentialStore,
        "set",
        classmethod(lambda cls, profile, api_key: stored.__setitem__(profile.name, api_key)),
    )
    paths = _paths(tmp_path)
    cfg = AppConfig(paths=paths, provider_profiles=[ProviderProfile(name="Remote", api_key="secret")])

    cfg.save()

    raw = json.loads(cfg.file_path.read_text(encoding="utf-8"))
    assert raw["provider_profiles"][0]["name"] == "Remote"
    assert "api_key" not in raw["provider_profiles"][0]
    assert stored["Remote"] == "secret"


def test_plugin_discovery_does_not_execute_module_code(tmp_path):
    plugin_path = tmp_path / "plugins" / "evil.py"
    paths = _paths(tmp_path)
    plugin_path = paths.plugins_dir / "evil.py"
    marker = paths.data_dir / "executed.txt"
    plugin_path.write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('executed')\n"
        "class Plugin:\n"
        "    manifest = {'id': 'evil', 'name': 'Evil', 'version': '1.0.0'}\n"
        "    def activate(self, context): pass\n"
        "    def deactivate(self): pass\n",
        encoding="utf-8",
    )
    manager = PluginManager(AppConfig(paths=paths), PluginContext(None, AppConfig(paths=paths)))

    discovered = manager.discover()

    assert discovered[0]["id"] == "evil"
    assert not marker.exists()


def test_untrusted_plugin_is_rejected_before_import(tmp_path):
    paths = _paths(tmp_path)
    plugin_path = paths.plugins_dir / "evil.py"
    marker = paths.data_dir / "executed.txt"
    plugin_path.write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('executed')\n"
        "class Plugin:\n"
        "    manifest = {'id': 'evil', 'name': 'Evil', 'version': '1.0.0'}\n"
        "    def activate(self, context): pass\n"
        "    def deactivate(self): pass\n",
        encoding="utf-8",
    )
    cfg = AppConfig(paths=paths, trusted_plugins=[])
    manager = PluginManager(cfg, PluginContext(None, cfg))

    with pytest.raises(PermissionError):
        manager.enable(plugin_path)

    assert not marker.exists()
