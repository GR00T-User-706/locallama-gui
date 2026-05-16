from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from platformdirs import user_config_dir, user_data_dir, user_log_dir

APP_NAME = "locallama-gui"


@dataclass(slots=True)
class AppPaths:
    config_dir: Path
    data_dir: Path
    logs_dir: Path
    sessions_dir: Path
    prompts_dir: Path
    agents_dir: Path
    modelfiles_dir: Path
    plugins_dir: Path

    @classmethod
    def create(cls) -> "AppPaths":
        config_dir = Path(user_config_dir(APP_NAME, "LocalLama"))
        data_dir = Path(user_data_dir(APP_NAME, "LocalLama"))
        logs_dir = Path(user_log_dir(APP_NAME, "LocalLama"))
        paths = cls(
            config_dir=config_dir,
            data_dir=data_dir,
            logs_dir=logs_dir,
            sessions_dir=data_dir / "sessions",
            prompts_dir=data_dir / "prompts",
            agents_dir=data_dir / "agents",
            modelfiles_dir=data_dir / "modelfiles",
            plugins_dir=data_dir / "plugins",
        )
        for path in asdict(paths).values():
            Path(path).mkdir(parents=True, exist_ok=True)
        return paths


@dataclass(slots=True)
class ProviderProfile:
    name: str = "Local Ollama"
    provider_type: str = "ollama"
    base_url: str = "http://localhost:11434"
    api_key: str = ""
    default_model: str = ""
    enabled: bool = True


@dataclass(slots=True)
class GenerationParameters:
    temperature: float = 0.7
    top_k: int = 40
    top_p: float = 0.9
    min_p: float = 0.0
    repeat_penalty: float = 1.1
    repeat_last_n: int = 64
    mirostat: int = 0
    mirostat_eta: float = 0.1
    mirostat_tau: float = 5.0
    tfs_z: float = 1.0
    num_predict: int = 512
    seed: int = -1
    stop: list[str] = field(default_factory=list)
    num_ctx: int = 4096
    num_batch: int = 512
    num_gpu: int = -1
    thinking_mode: bool = False
    plan_mode: bool = False
    normal_mode: bool = True

    def to_backend_options(self) -> dict[str, Any]:
        return {
            "temperature": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "min_p": self.min_p,
            "repeat_penalty": self.repeat_penalty,
            "repeat_last_n": self.repeat_last_n,
            "mirostat": self.mirostat,
            "mirostat_eta": self.mirostat_eta,
            "mirostat_tau": self.mirostat_tau,
            "tfs_z": self.tfs_z,
            "num_predict": self.num_predict,
            "seed": self.seed,
            "stop": self.stop,
            "num_ctx": self.num_ctx,
            "num_batch": self.num_batch,
            "num_gpu": self.num_gpu,
        }


@dataclass(slots=True)
class UISettings:
    theme: str = "dark"
    geometry_hex: str = ""
    state_hex: str = ""
    active_session_id: str = ""


@dataclass(slots=True)
class AppConfig:
    paths: AppPaths = field(default_factory=AppPaths.create)
    provider_profiles: list[ProviderProfile] = field(default_factory=lambda: [ProviderProfile()])
    active_provider: str = "Local Ollama"
    parameters: GenerationParameters = field(default_factory=GenerationParameters)
    parameter_presets: dict[str, dict[str, Any]] = field(default_factory=dict)
    enabled_plugins: dict[str, bool] = field(default_factory=dict)
    ui: UISettings = field(default_factory=UISettings)
    global_system_prompt: str = "You are a helpful, precise assistant."

    @property
    def file_path(self) -> Path:
        return self.paths.config_dir / "config.json"

    @classmethod
    def load(cls) -> "AppConfig":
        paths = AppPaths.create()
        path = paths.config_dir / "config.json"
        if not path.exists():
            cfg = cls(paths=paths)
            cfg.save()
            return cfg
        data = json.loads(path.read_text(encoding="utf-8"))
        profiles = [ProviderProfile(**item) for item in data.get("provider_profiles", [])]
        cfg = cls(
            paths=paths,
            provider_profiles=profiles or [ProviderProfile()],
            active_provider=data.get("active_provider", "Local Ollama"),
            parameters=GenerationParameters(**data.get("parameters", {})),
            parameter_presets=data.get("parameter_presets", {}),
            enabled_plugins=data.get("enabled_plugins", {}),
            ui=UISettings(**data.get("ui", {})),
            global_system_prompt=data.get("global_system_prompt", "You are a helpful, precise assistant."),
        )
        return cfg

    def save(self) -> None:
        data = {
            "provider_profiles": [asdict(profile) for profile in self.provider_profiles],
            "active_provider": self.active_provider,
            "parameters": asdict(self.parameters),
            "parameter_presets": self.parameter_presets,
            "enabled_plugins": self.enabled_plugins,
            "ui": asdict(self.ui),
            "global_system_prompt": self.global_system_prompt,
        }
        self.file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def active_profile(self) -> ProviderProfile:
        for profile in self.provider_profiles:
            if profile.name == self.active_provider:
                return profile
        return self.provider_profiles[0]
