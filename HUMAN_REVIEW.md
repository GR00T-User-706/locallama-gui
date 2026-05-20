# HUMAN_REVIEW

This file tracks code areas requiring manual review due to mixed responsibilities, risky execution paths, or unclear duplicate ownership.

## Priority review entries

1. `locallama_gui/ui/main_window.py`
   - Mixes UI concerns with backend orchestration, model operations, plugin interception, request logging, and file writes.
   - Contains streaming lifecycle control that can hide race/cancellation edge cases.

2. `locallama_gui/ui/dialogs.py`
   - Includes filesystem writes, inline JSON import/export, API key handling in UI table flows, and parent-callback model build triggers.
   - Contains compact one-line conditionals that reduce readability and auditability.

3. `locallama_gui/core/managers.py`
   - Dynamically loads plugin modules and mounts plugin UI panes into the main window.
   - Handles plugin discovery from multiple directories with potentially unclear trust boundaries.

4. `locallama_gui/ui/workers.py`
   - Streaming token loop and thread signaling should be manually validated for cancellation behavior and UI thread safety.

5. `locallama_gui/backends/ollama.py` and `locallama_gui/backends/openai.py`
   - Streaming parsing and model responses should be reviewed for malformed payload handling and partial-frame behavior.

6. `ollama_GUI/addons/ollama_tools/ollama_tools.py`
   - Archived tool framework executes subprocess commands and orchestrates model-guided tool actions; requires explicit human approval before reuse.

7. Duplicate implementation families
   - `llm_studio/`, `locallama_gui/`, and `ollama_GUI/` appear to overlap in responsibility.
   - Human decision needed on canonical runtime path and deprecation/archive policy.
