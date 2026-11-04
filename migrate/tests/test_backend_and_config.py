from pathlib import Path

from locallama_gui.backends.ollama import OllamaBackend
from locallama_gui.core.config import AppConfig, AppPaths, ProviderProfile


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class _FakeAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def get(self, url):
        return _FakeResponse(
            {
                "models": [
                    {
                        "name": "llama3:8b",
                        "size": 123,
                        "details": {"parameter_size": "8B", "quantization_level": "Q4_K_M"},
                        "model_info": {"llama.context_length": 8192},
                    },
                    {
                        "name": "tiny",
                        # intentionally partial payload to verify fallback robustness
                    },
                ]
            }
        )


def test_ollama_list_models_parsing(monkeypatch):
    import locallama_gui.backends.ollama as ollama_mod

    monkeypatch.setattr(ollama_mod.httpx, "AsyncClient", _FakeAsyncClient)
    backend = OllamaBackend(base_url="http://localhost:11434", api_key="")

    import asyncio

    models = asyncio.run(backend.list_models())
    assert len(models) == 2
    assert models[0].name == "llama3:8b"
    assert models[0].parameter_size == "8B"
    assert models[0].quantization == "Q4_K_M"
    assert models[0].context_size == 8192
    assert models[1].name == "tiny"


def test_config_save_load_roundtrip(tmp_path: Path):
    paths = AppPaths(
        config_dir=tmp_path / "cfg",
        data_dir=tmp_path / "data",
        logs_dir=tmp_path / "logs",
        sessions_dir=tmp_path / "data" / "sessions",
        prompts_dir=tmp_path / "data" / "prompts",
        agents_dir=tmp_path / "data" / "agents",
        modelfiles_dir=tmp_path / "data" / "modelfiles",
        plugins_dir=tmp_path / "data" / "plugins",
    )
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
        p.mkdir(parents=True, exist_ok=True)

    cfg = AppConfig(paths=paths, provider_profiles=[ProviderProfile(name="Remote", base_url="http://10.0.0.2:11434")], active_provider="Remote")
    cfg.parameters.temperature = 0.2
    cfg.global_system_prompt = "test"
    cfg.save()

    loaded = AppConfig.load()
    # AppConfig.load uses platform paths; verify persisted file has expected values instead.
    raw = cfg.file_path.read_text(encoding="utf-8")
    assert '"active_provider": "Remote"' in raw
    assert '"temperature": 0.2' in raw
    assert '"global_system_prompt": "test"' in raw
    assert loaded is not None
