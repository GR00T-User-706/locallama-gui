# FUNCTIONALITY_STATUS

## WORKING
- Core chat UI wiring, session management, and backend dispatch paths are present and connected in `locallama_gui/ui/main_window.py`.
- Backend abstraction and concrete providers (Ollama/OpenAI-compatible) are implemented in `locallama_gui/backends/`.
- Plugin discovery/loading scaffolding exists in `locallama_gui/core/managers.py`.

## PARTIAL
- Plugin management UX exists, but safety/validation boundaries for third-party plugins rely on local trust assumptions.
- Agent/profile import-export flows work but include compact one-line logic that is difficult to audit and maintain.
- Archive tool frameworks under `ollama_GUI/addons/ollama_tools/` appear usable but are not clearly integrated with the primary app path.

## BROKEN
- No confirmed automated end-to-end test evidence in this change set; runtime status is unknown for many legacy and archive modules.
- Duplicate/parallel code trees (`llm_studio`, `locallama_gui`, `ollama_GUI`) indicate potential drift and stale functionality.

## UNKNOWN
- Actual runtime health of archived/legacy tool engines and test scripts in `ollama_GUI/addons/ollama_tools/`.
- Whether all plugin hooks remain API-compatible across duplicated UI/backend implementations.

## MOVED_TO_ARCHIVE
- `ollama_GUI/addons/ollama_tools/` should be treated as archive-oriented tool framework material unless explicitly re-adopted and tested.
- Historical/parallel GUI code under `ollama_GUI/` appears separate from the current primary `locallama_gui/` app path.

## NEEDS_HUMAN_REVIEW
- Mixed UI/backend orchestration in main window chat and model operations.
- Dynamic plugin/module loading and enablement defaults.
- Stream parsing and token-handling correctness across providers.
- Filesystem write paths for configs, chats, and plugin install operations.
