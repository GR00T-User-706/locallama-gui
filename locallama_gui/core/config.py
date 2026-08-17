from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import keyring
from keyring.errors import KeyringError, PasswordDeleteError
from platformdirs import user_config_dir, user_data_dir, user_log_dir

APP_NAME = "locallama-gui"
APP_SYSTEM_PROMPT = """You are running inside LocalLama Control Center, a PySide6 desktop frontend for Ollama.

You are the active local assistant selected by the user through LocalLama.

Answer the user directly.
Do not explain what Ollama is unless asked.
Do not ask what frontend the user means when the user is clearly using LocalLama.
Do not provide generic setup instructions unless the user requests setup help.
Use the selected model and current conversation context.
Be concise, useful, and technically accurate.
When the user asks about LocalLama, treat it as this application.
When the user asks about models, prompts, parameters, requests, tokens, or logs, assume they are referring to the current LocalLama session unless stated otherwise."""


class CredentialStore:
    """Store provider credentials in the operating system credential store."""

    service_name = APP_NAME

    @classmethod
    def _username(cls, profile: "ProviderProfile") -> str:
        return f"{profile.provider_type}:{profile.name}"

    @classmethod
    def get(cls, profile: "ProviderProfile") -> str:
        try:
            return keyring.get_password(cls.service_name, cls._username(profile)) or ""
        except KeyringError as exc:
            raise RuntimeError(
                "The operating system credential store is unavailable. "
                "API keys will not be read from config.json."
            ) from exc

    @classmethod
    def set(cls, profile: "ProviderProfile", api_key: str) -> None:
        try:
            if api_key:
                keyring.set_password(cls.service_name, cls._username(profile), api_key)
            else:
                try:
                    keyring.delete_password(cls.service_name, cls._username(profile))
                except PasswordDeleteError:
                    pass
        except KeyringError as exc:
            raise RuntimeError(
                f"Cannot store the API key for provider '{profile.name}' in the operating system credential store."
            ) from exc


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
    # Retained only so older configs and presets continue to load safely.
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
    reasoning_mode: str = "normal"
    thinking_mode: bool = False
    plan_mode: bool = False
    normal_mode: bool = True

    def __post_init__(self) -> None:
        # Backward compatibility for older configs/presets that used booleans.
        if self.reasoning_mode not in {"normal", "thinking", "plan"}:
            self.reasoning_mode = "normal"
        if self.reasoning_mode == "normal":
            if self.thinking_mode:
                self.reasoning_mode = "thinking"
            elif self.plan_mode:
                self.reasoning_mode = "plan"
        self.thinking_mode = self.reasoning_mode == "thinking"
        self.plan_mode = self.reasoning_mode == "plan"
        self.normal_mode = self.reasoning_mode == "normal"

    def to_backend_options(self) -> dict[str, Any]:
        options = {
            "temperature": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "min_p": self.min_p,
            "repeat_penalty": self.repeat_penalty,
            "repeat_last_n": self.repeat_last_n,
            "num_predict": self.num_predict,
            "seed": self.seed,
            "stop": self.stop,
            "num_ctx": self.num_ctx,
            "num_batch": self.num_batch,
            "num_gpu": self.num_gpu,
        }
        if self.reasoning_mode == "thinking":
            options["think"] = True
        return options


@dataclass(slots=True)
class UISettings:
    theme: str = "dark"
    geometry_hex: str = ""
    state_hex: str = ""
    active_session_id: str = ""
    font_size: int = 12


@dataclass(slots=True)
class AppConfig:
    paths: AppPaths = field(default_factory=AppPaths.create)
    provider_profiles: list[ProviderProfile] = field(default_factory=lambda: [ProviderProfile()])
    active_provider: str = "Local Ollama"
    parameters: GenerationParameters = field(default_factory=GenerationParameters)
    parameter_presets: dict[str, dict[str, Any]] = field(default_factory=dict)
    enabled_plugins: dict[str, bool] = field(default_factory=dict)
    trusted_plugins: list[str] = field(default_factory=list)
    developer_mode: bool = False
    ui: UISettings = field(default_factory=UISettings)
    global_system_prompt: str = "You are a helpful, concise assistant."

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
        profiles: list[ProviderProfile] = []
        migrated_credentials = False
        for raw_profile in data.get("provider_profiles", []):
            item = dict(raw_profile)
            legacy_api_key = str(item.pop("api_key", "") or "")
            profile = ProviderProfile(**item)
            if legacy_api_key:
                profile.api_key = legacy_api_key
                CredentialStore.set(profile, legacy_api_key)
                migrated_credentials = True
            else:
                profile.api_key = CredentialStore.get(profile)
            profiles.append(profile)

        cfg = cls(
            paths=paths,
            provider_profiles=profiles or [ProviderProfile()],
            active_provider=data.get("active_provider", "Local Ollama"),
            parameters=GenerationParameters(**data.get("parameters", {})),
            parameter_presets=data.get("parameter_presets", {}),
            enabled_plugins=data.get("enabled_plugins", {}),
            trusted_plugins=data.get("trusted_plugins", []),
            developer_mode=data.get("developer_mode", False),
            ui=UISettings(**data.get("ui", {})),
            global_system_prompt=data.get(
                "global_system_prompt", "You are a helpful, concise assistant."
            ),
        )
        if migrated_credentials:
            cfg.save()
        return cfg

    def save(self) -> None:
        for profile in self.provider_profiles:
            CredentialStore.set(profile, profile.api_key)

        data = {
            "provider_profiles": [
                {
                    "name": profile.name,
                    "provider_type": profile.provider_type,
                    "base_url": profile.base_url,
                    "default_model": profile.default_model,
                    "enabled": profile.enabled,
                }
                for profile in self.provider_profiles
            ],
            "active_provider": self.active_provider,
            "parameters": asdict(self.parameters),
            "parameter_presets": self.parameter_presets,
            "enabled_plugins": self.enabled_plugins,
            "trusted_plugins": self.trusted_plugins,
            "developer_mode": self.developer_mode,
            "ui": asdict(self.ui),
            "global_system_prompt": self.global_system_prompt,
        }
        self.paths.config_dir.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        try:
            self.file_path.chmod(0o600)
        except OSError:
            pass

    def active_profile(self) -> ProviderProfile:
        for profile in self.provider_profiles:
            if profile.name == self.active_provider:
                return profile
        return self.provider_profiles[0]
