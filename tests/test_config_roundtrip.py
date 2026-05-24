from pathlib import Path

from locallama_gui.core.config import AppConfig, AppPaths, GenerationParameters, ProviderProfile, UISettings


def test_config_load_save_roundtrip(monkeypatch, tmp_path):
    def _fake_create():
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

    monkeypatch.setattr("locallama_gui.core.config.AppPaths.create", _fake_create)

    paths = _fake_create()
    for p in [
        paths.config_dir,
        paths.data_dir,
        paths.logs_dir,
        paths.sessions_dir,
        paths.prompts_dir,
        paths.agents_dir,
        paths.modelfiles_dir,
        paths.plugins_dir,
    ]:
        Path(p).mkdir(parents=True, exist_ok=True)

    original = AppConfig(
        paths=paths,
        provider_profiles=[ProviderProfile(name="Custom", base_url="http://example:11434", default_model="llama3")],
        active_provider="Custom",
        parameters=GenerationParameters(temperature=0.2, top_k=12, num_ctx=2048),
        parameter_presets={"fast": {"temperature": 0.1}},
        enabled_plugins={"plug": True},
        trusted_plugins=["plug"],
        developer_mode=True,
        ui=UISettings(theme="light", geometry_hex="aa", state_hex="bb", active_session_id="sess-1"),
        global_system_prompt="system",
    )
    original.save()

    loaded = AppConfig.load()

    assert loaded.active_provider == "Custom"
    assert loaded.provider_profiles[0].base_url == "http://example:11434"
    assert loaded.provider_profiles[0].default_model == "llama3"
    assert loaded.parameters.temperature == 0.2
    assert loaded.parameters.top_k == 12
    assert loaded.parameters.num_ctx == 2048
    assert loaded.parameter_presets == {"fast": {"temperature": 0.1}}
    assert loaded.enabled_plugins == {"plug": True}
    assert loaded.trusted_plugins == ["plug"]
    assert loaded.developer_mode is True
    assert loaded.ui.theme == "light"
    assert loaded.ui.active_session_id == "sess-1"
    assert loaded.global_system_prompt == "system"
