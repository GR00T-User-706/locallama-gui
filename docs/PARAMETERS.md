# Parameters Reference

## Generation parameters

The active parameter dialog exposes sampling, context, GPU, and stop-sequence settings. Reasoning, thinking, and planning controls are temporarily disabled for beta compatibility while backend request behavior is reviewed.

Legacy configuration fields (`reasoning_mode`, `thinking_mode`, and `plan_mode`) remain readable so existing user configuration files continue to load. On load, these fields are normalized to normal mode. They are not exposed in the UI and are never serialized into chat request payloads.

## Core generation parameters

- `temperature`
- `top_k`
- `top_p`
- `min_p`
- `repeat_penalty`
- `repeat_last_n`
- `mirostat`
- `mirostat_eta`
- `mirostat_tau`
- `tfs_z`
- `num_predict`
- `seed`
- `stop`
- `num_ctx`
- `num_batch`
- `num_gpu`

Parameter values are persisted through `AppConfig`. Parameter presets remain supported; legacy reasoning keys in older presets are ignored.
