# Parameters Reference

## Generation parameters

The active parameter dialog exposes sampling, context, GPU, and stop-sequence settings. Reasoning, thinking, and planning controls are temporarily disabled for beta compatibility while backend request behavior is reviewed.

Legacy configuration fields (\x60reasoning_mode\x60, \x60thinking_mode\x60, and \x60plan_mode\x60) remain readable so existing user configuration files continue to load. On load, these fields are normalized to normal mode. They are not exposed in the UI and are never serialized into chat request payloads.

## Core generation parameters

- \x60temperature\x60
- \x60top_k\x60
- \x60top_p\x60
- \x60min_p\x60
- \x60repeat_penalty\x60
- \x60repeat_last_n\x60
- \x60mirostat\x60
- \x60mirostat_eta\x60
- \x60mirostat_tau\x60
- \x60tfs_z\x60
- \x60num_predict\x60
- \x60seed\x60
- \x60stop\x60
- \x60num_ctx\x60
- \x60num_batch\x60
- \x60num_gpu\x60

Parameter values are persisted through \x60AppConfig\x60. Parameter presets remain supported; legacy reasoning keys in older presets are ignored.
