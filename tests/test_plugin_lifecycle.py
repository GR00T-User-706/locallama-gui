from pathlib import Path
from types import SimpleNamespace

import pytest

from locallama_gui.core.managers import PluginContext, PluginManager


class FakeConfig:
    def __init__(self, plugins_dir: Path) -> None:
        self.paths = SimpleNamespace(plugins_dir=plugins_dir)
        self.developer_mode = False
        self.enabled_plugins = {}
        self.trusted_plugins = []
        self.saves = 0

    def save(self) -> None:
        self.saves += 1


def make_plugin(path: Path) -> None:
    path.write_text(
        """
ACTIVATED = []
DEACTIVATED = []

class Plugin:
    manifest = {"id": "demo", "name": "Demo Plugin", "version": "1.0.0"}

    def activate(self, context):
        ACTIVATED.append("activate")

    def deactivate(self):
        DEACTIVATED.append("deactivate")
""",
        encoding="utf-8",
    )


def test_plugin_lifecycle_discover_validate_trust_enable_disable_reload_untrust_remove(tmp_path):
    plugin_path = tmp_path / "demo.py"
    make_plugin(plugin_path)
    config = FakeConfig(tmp_path)
    manager = PluginManager(config, PluginContext(SimpleNamespace(), config))

    discovered = manager.discover()
    assert discovered[0]["id"] == "demo"
    assert discovered[0]["version"] == "1.0.0"
    assert "error" not in discovered[0]

    with pytest.raises(PermissionError):
        manager.enable(plugin_path)

    manager.trust("demo")
    assert "demo" in config.trusted_plugins

    manager.enable(plugin_path)
    assert "demo" in manager.loaded
    assert config.enabled_plugins["demo"] is True

    manager.disable("demo")
    assert "demo" not in manager.loaded
    assert config.enabled_plugins["demo"] is False

    manager.enable(plugin_path)
    manager.reload()
    assert "demo" in manager.loaded
    assert config.enabled_plugins["demo"] is True

    manager.untrust("demo")
    assert "demo" not in manager.loaded
    assert "demo" not in config.trusted_plugins
    assert config.enabled_plugins["demo"] is False

    manager.trust("demo")
    manager.enable(plugin_path)
    manager.remove("demo")
    assert not plugin_path.exists()
    assert "demo" not in manager.loaded
    assert "demo" not in config.trusted_plugins
    assert "demo" not in config.enabled_plugins


def test_plugin_discovery_reports_manifest_validation_error(tmp_path):
    path = tmp_path / "invalid.py"
    path.write_text(
        "class Plugin:\n    manifest = {'id': 'invalid'}\n",
        encoding="utf-8",
    )
    config = FakeConfig(tmp_path)
    manager = PluginManager(config, PluginContext(SimpleNamespace(), config))

    result = manager.discover()[0]
    assert result["id"] == "invalid"
    assert "error" in result

    with pytest.raises(ValueError):
        manager.trust("invalid")
