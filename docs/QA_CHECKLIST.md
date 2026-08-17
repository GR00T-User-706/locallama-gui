# QA Checklist

Date: 2026-08-17
Scope: Regression and release checklist for the active LocalLama Control Center application.

This document is a test contract, not a claim that every manual item is currently passing. Mark each item only after executing it against the target build.

## Result convention

- `[ ]` not tested
- `[x]` passed
- `[!]` failed
- `[~]` partial / known limitation
- `N/A` not applicable to the selected backend/environment

Record the build/version, OS, Python version, Qt/PySide6 version, backend type, backend URL, and model used for every release-oriented manual pass.

## 1. Automated preflight

Run from repository root:

```bash
ruff check .
python -m compileall -q locallama_gui
pytest tests
```

Also verify:

- [ ] No test depends on a real remote credential.
- [ ] Security-boundary tests pass.
- [ ] Plugin lifecycle tests pass.
- [ ] Configuration schema migration tests pass.
- [ ] Package metadata and runtime version agree.

## 2. Launch and startup

- [ ] `locallama-gui` launches successfully.
- [ ] `python -m locallama_gui` launches successfully.
- [ ] A normal configured installation reaches the main window.
- [ ] A missing/unavailable Ollama endpoint does not crash startup.
- [ ] Startup reports backend availability clearly.
- [ ] Existing window geometry/state is restored.
- [ ] The initial chat tab is created.
- [ ] The model list refresh is initiated after startup.

## 3. Backend states

### Missing Ollama

- [ ] Stop/unavailable Ollama.
- [ ] Launch LocalLama.
- [ ] Application remains usable for UI/configuration workflows.
- [ ] Connection failure is visible through status/diagnostics.
- [ ] No traceback is dumped as an unexplained UI failure.

### Connected Ollama

- [ ] Start Ollama at the configured endpoint.
- [ ] Refresh models.
- [ ] Connection status changes to the connected/available state.
- [ ] Model list populates without freezing the UI.

## 4. Model lifecycle

### Refresh

- [ ] Refresh Models updates the model combo/table.
- [ ] Refresh remains responsive while the backend responds.
- [ ] Backend errors are surfaced without destroying the current UI state.

### Pull

- [ ] Pull prompts for/uses a valid model name.
- [ ] Pull progress is represented in Diagnostics > Operations.
- [ ] Successful pull refreshes the model list.
- [ ] Pull failure is visible and non-crashing.

### Push

- [ ] Push prompts for/uses a valid model name.
- [ ] Push progress is represented in Diagnostics > Operations.
- [ ] Push success/failure is reported clearly.

### Clone

- [ ] Clone requires a selected source model.
- [ ] Clone requires a destination name.
- [ ] Successful clone refreshes models.
- [ ] Clone failure is reported clearly.

### Delete

- [ ] Delete requires a selected model.
- [ ] Delete requires explicit confirmation.
- [ ] Successful deletion refreshes models.
- [ ] Cancellation leaves the model untouched.

### Create

- [ ] Create opens the Modelfile editor.
- [ ] New/Open/Save/Duplicate work as applicable.
- [ ] Validate reports malformed directives.
- [ ] Preview Config reflects the current Modelfile.
- [ ] Build Model invokes the backend operation.
- [ ] Build failure is visible and non-crashing.

## 5. Chat

- [ ] New Chat creates a new tab/session.
- [ ] User message can be sent with the Send action.
- [ ] Ctrl+Enter sends a message.
- [ ] Streaming responses render incrementally when enabled.
- [ ] Stop terminates active generation.
- [ ] Retry reuses the expected conversation state.
- [ ] Regenerate reuses the expected conversation state.
- [ ] Edit Message updates the selected visible message.
- [ ] Delete Message removes the selected visible message.
- [ ] Copy Last copies the latest visible response.
- [ ] Request Viewer shows the redacted request representation.
- [ ] Token/Response Viewer updates during streaming.

## 6. Session save/load

- [ ] Save persists the current session.
- [ ] Save As writes the selected destination.
- [ ] Open Chat restores a saved session.
- [ ] Session list refreshes after saving.
- [ ] Double-clicking a session opens it.
- [ ] Import loads a valid session file.
- [ ] Export writes the current session.
- [ ] Corrupt/unreadable session files do not crash session listing.

## 7. Themes and UI state

- [ ] Themes action changes the active theme.
- [ ] Selected theme persists across restart.
- [ ] Font size setting persists when changed.
- [ ] Main-window geometry/state persists and restores.
- [ ] Docks remain usable after theme/state restoration.

## 8. Plugins

### Discovery and trust boundary

- [ ] Plugin Manager opens.
- [ ] Discovery lists valid plugin manifests.
- [ ] Invalid manifests show an actionable error.
- [ ] Discovery does not execute plugin top-level code.
- [ ] An untrusted plugin cannot be enabled.
- [ ] Trusting a valid plugin records its trust state.

### Lifecycle

- [ ] Discover
- [ ] Validate
- [ ] Trust
- [ ] Enable
- [ ] Disable
- [ ] Reload
- [ ] Untrust
- [ ] Remove

### Runtime

- [ ] Enabled/trusted plugin activates successfully.
- [ ] Plugin deactivation runs on disable/reload.
- [ ] Reload does not duplicate plugin state.
- [ ] Plugin load failure does not prevent unrelated plugins/application startup.
- [ ] Plugin installation copies the selected Python file into the configured plugin directory.

## 9. Agents

- [ ] Agent Builder opens.
- [ ] Create a new agent.
- [ ] Save an agent.
- [ ] Reopen/manage an existing agent.
- [ ] Import an agent JSON file.
- [ ] Export an agent JSON file.
- [ ] Model, reasoning, behavior, memory, execution policy, tools and plugins fields round-trip correctly.
- [ ] Confirm the current limitation that agent profiles do not yet alter chat generation/tool execution unless the active application path explicitly wires them in.

## 10. Prompts

- [ ] System prompt dock displays saved prompts.
- [ ] Double-click applies a prompt to the current chat as designed.
- [ ] Prompt Manager can create a prompt.
- [ ] Prompt Manager can save/update a prompt.
- [ ] Prompt Manager can delete a prompt.
- [ ] Prompt Manager can import a prompt.
- [ ] Prompt Manager can export prompts.
- [ ] Prompt version history survives an update.

## 11. Diagnostics and developer surfaces

- [ ] Logs panel receives Python logging records.
- [ ] Console captures stdout/stderr output.
- [ ] Operations view records model-operation lifecycle.
- [ ] Request Viewer Copy works.
- [ ] Request Viewer Clear works.
- [ ] Token Viewer Copy works.
- [ ] Token Viewer Clear works.
- [ ] Developer documentation/help paths report missing files without crashing.

## 12. API endpoints and parameters

- [ ] API Endpoints dialog opens.
- [ ] Add/remove endpoint rows work.
- [ ] Provider metadata persists.
- [ ] API keys are not written to `config.json`.
- [ ] API keys are retrieved from the OS credential store.
- [ ] Generation parameters save/load.
- [ ] Parameter presets save/load.
- [ ] Reasoning mode persists and maps to the expected backend request behavior.

## 13. Desktop integration

- [ ] `run-locallama` launches the application from the repository/install context where supported.
- [ ] Linux desktop entry is present under `packaging/linux/`.
- [ ] Desktop launcher installation script completes successfully.
- [ ] Installed launcher starts the same application entry point.

## 14. Release sign-off

- [ ] Automated preflight passes.
- [ ] Required backend scenarios have been exercised.
- [ ] Model lifecycle scenarios have been exercised.
- [ ] Chat and session lifecycle has been exercised.
- [ ] Theme/UI state has been exercised.
- [ ] Plugin lifecycle has been exercised.
- [ ] Agents/prompts have been exercised.
- [ ] Desktop launcher has been exercised.
- [ ] Known failures are recorded in `docs/BUGS/KNOWN_BUGS.md`.
- [ ] Documentation changes are included in the same release change set.
