# Parameters Reference (Baseline)

Date: 2026-05-25
Scope: Baseline explanation of generation/config parameters from observed config/backend mapping.

## Reasoning Mode

### CONFIRMED
`locallama_gui/core/config.py` defines `reasoning_mode` with allowed values:
- `normal`
- `thinking`
- `plan`

Backward compatibility logic maps older booleans into `reasoning_mode`.

Backend option mapping:
- `thinking` => sends `think: true`
- `plan` => sends `plan: true`
- `normal` => sends neither flag

### LIKELY
- UI currently exposes this as a single exclusive control (per changelog notes).

### UNKNOWN
- Whether all dialogs/tooltips clearly communicate this behavior to end users.

## Core Generation Parameters (Observed)

From `GenerationParameters` in `core/config.py`:
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

## Operational Notes

### CONFIRMED
- Parameters are persisted via `AppConfig` serialization.
- Backend options are built through `to_backend_options()`.

### LIKELY
- Parameter presets are user-editable through parameter dialogs/workflows.

### UNKNOWN
- Final UI copy quality, guardrails, and validation behavior for edge values.

## TODO
- Add user-facing recommended ranges and backend compatibility notes.
- Add examples for common profiles (balanced, deterministic, long-context).
