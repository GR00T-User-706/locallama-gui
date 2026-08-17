# Configuration Schema

Date: 2026-08-17
Current schema version: `2`

## Purpose

`config.json` stores non-secret application configuration. Provider API keys are deliberately excluded from this file and are stored in the operating-system credential store.

The configuration schema version is independent from the application/package version in `pyproject.toml`.

## Current top-level schema

```json
{
  "schema_version": 2,
  "provider_profiles": [
    {
      "name": "Local Ollama",
      "provider_type": "ollama",
      "base_url": "http://localhost:11434",
      "default_model": "",
      "enabled": true
    }
  ],
  "active_provider": "Local Ollama",
  "parameters": {},
  "parameter_presets": {},
  "enabled_plugins": {},
  "trusted_plugins": [],
  "developer_mode": false,
  "ui": {},
  "global_system_prompt": "You are a helpful, concise assistant."
}
```

The `parameters` and `ui` objects are represented by `GenerationParameters` and `UISettings` in `locallama_gui/core/config.py`.

## Schema version 2

Version 2 establishes an explicit top-level `schema_version` and uses the OS credential store for provider secrets.

Provider profile JSON must not contain:

```text
api_key
```

The runtime `ProviderProfile.api_key` field may contain the secret after loading because backend calls need it, but `AppConfig.save()` strips it from the serialized JSON representation.

## Migration policy

`AppConfig.load()` owns configuration migration.

Current rules:

- Missing `schema_version` is treated as schema version `1`.
- Version `1` is migrated to version `2`.
- Legacy plaintext `api_key` fields are moved to the OS credential store during load.
- Migrated configuration is rewritten in the current schema.
- A schema version newer than the application-supported version is rejected with an explicit error.

Do not silently reinterpret an unknown future schema.

## Adding schema versions

When persisted configuration changes incompatibly:

1. increment `CONFIG_SCHEMA_VERSION`;
2. add an explicit migration step in `AppConfig._migrate_data()`;
3. preserve existing user settings where their meaning is known;
4. reject versions newer than the supported version;
5. add migration and round-trip regression tests;
6. update this document;
7. update `docs/VERSIONING.md` when the release version changes.

## Compatibility expectations

A normal application update should preserve supported user configuration. Schema migration is part of startup and must complete before the main window is constructed.

A configuration migration must not require users to manually edit JSON unless the migration is impossible to perform safely. Secret migration must never copy the API key back into `config.json`.

## Testing requirements

Configuration changes require tests for:

- current-schema round trip;
- legacy-schema migration;
- future-schema rejection;
- secret exclusion from serialized JSON;
- runtime access to credentials through the credential store.
