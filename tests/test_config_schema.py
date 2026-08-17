import json
from pathlib import Path

import pytest

from locallama_gui.core.config import CONFIG_SCHEMA_VERSION, AppConfig, AppPaths


def make_paths(tmp_path: Path) -> AppPaths:
    base = tmp_path / "app"
    return AppPaths(
        config_dir=base / "config",
        data_dir=base / "data",
        logs_dir=base / "logs",
        sessions_dir=base / "data" / "sessions",
        prompts_dir=base / "data" / "prompts",
        agents_dir=base / "data" / "agents",
        modelfiles_dir=base / "data" / "modelfiles",
        plugins_dir=base / "data" / "plugins",
    )


def test_legacy_unversioned_config_migrates_to_current_schema(monkeypatch, tmp_path):
    paths = make_paths(tmp_path)
    paths.config_dir.mkdir(parents=True)
    legacy = {
        "provider_profiles": [{"name": "Local Ollama", "provider_type": "ollama", "base_url": "http://localhost:11434", "enabled": True}],
        "active_provider": "Local Ollama",
    }
    (paths.config_dir / "config.json").write_text(json.dumps(legacy), encoding="utf-8")
    monkeypatch.setattr("locallama_gui.core.config.AppPaths.create", lambda: paths)

    loaded = AppConfig.load()

    assert loaded.schema_version == CONFIG_SCHEMA_VERSION
    saved = json.loads((paths.config_dir / "config.json").read_text(encoding="utf-8"))
    assert saved["schema_version"] == CONFIG_SCHEMA_VERSION


def test_future_config_schema_is_rejected(monkeypatch, tmp_path):
    paths = make_paths(tmp_path)
    paths.config_dir.mkdir(parents=True)
    (paths.config_dir / "config.json").write_text(
        json.dumps({"schema_version": CONFIG_SCHEMA_VERSION + 1}),
        encoding="utf-8",
    )
    monkeypatch.setattr("locallama_gui.core.config.AppPaths.create", lambda: paths)

    with pytest.raises(ValueError, match="Unsupported config schema version"):
        AppConfig.load()
