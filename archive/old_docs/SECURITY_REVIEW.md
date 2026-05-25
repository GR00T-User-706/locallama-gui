# SECURITY_REVIEW

Security-focused review checklist and hotspot index.

## Dynamic imports / module loading
- `locallama_gui/core/managers.py` uses `importlib.util` plugin loading from filesystem paths.
- Risk: untrusted plugin execution if path controls are weak or plugin sources are not vetted.

## Plugin execution
- Plugin discovery and load/enable paths are centralized in `locallama_gui/core/managers.py` and invoked from UI controls in `locallama_gui/ui/main_window.py`.
- Risk: runtime code execution through plugin hooks and UI panel injection.

## Filesystem writes / deletes
- Multiple write points in UI and manager layers:
  - `locallama_gui/ui/main_window.py` (chat save, plugin install copy, export-like flows)
  - `locallama_gui/ui/dialogs.py` (modelfiles, versions, agent/profile export)
  - `locallama_gui/core/managers.py` (prompt/agent persistence)
- Archived tools also perform writes/deletes, including temporary workspace cleanup in `ollama_GUI/addons/ollama_tools/` tests.

## Subprocess / command execution
- `ollama_GUI/addons/ollama_tools/ollama_tools.py` imports and uses `subprocess.run(...)`.
- Risk: command construction mistakes, unexpected tool invocation surface, and output handling trust.

## Credential handling
- `locallama_gui/backends/openai.py` constructs `Authorization: Bearer ...` headers from configured API keys.
- `locallama_gui/ui/dialogs.py` displays/edits provider API keys in table forms.
- Risk: accidental exposure in UI logs, exports, or screenshots.

## Archived tool frameworks
- `ollama_GUI/addons/ollama_tools/` contains advanced tool orchestration patterns (model-guided actions, workspace managers, evaluator-style tests).
- Treat as high-risk archive material until re-reviewed, threat-modeled, and gated behind explicit opt-in.
