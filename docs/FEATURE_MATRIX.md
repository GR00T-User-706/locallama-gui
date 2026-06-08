# Feature Matrix

This matrix classifies visible application actions by their current operational state. It is a stabilization reference, not a feature roadmap.

Status meanings:

- **working** — the visible action completes its documented loop.
- **partial** — useful behavior exists, but part of the visible workflow remains incomplete.
- **blocked** — an intentional requirement prevents completion and the UI does not yet provide the required path.
- **hidden** — implementation exists but has no clear visible entry point.

| Area | Action | Status | Current behavior | Remaining work |
|---|---|---|---|---|
| Models | Pull | working | Validates the model name, streams backend output, and records start/success/error in the diagnostics terminal. | Backend support and registry access still determine whether a pull succeeds. |
| Models | Push | working | Validates the model name, streams backend output, and records start/success/error in the diagnostics terminal. | Backend support, authentication, and registry access still determine whether a push succeeds. |
| Models | Clone | working | Validates source/destination names and runs the copy operation asynchronously with terminal status and error reporting. | Backend copy support is required. |
| Models | Create | working | Opens the Modelfile editor and builds asynchronously with streamed output and terminal status/error reporting. | Modelfile validation remains user-invoked before build. |
| Models | Delete | working | Requires a selected model, preserves destructive confirmation, and reports asynchronous status/errors in the terminal. | Backend delete support is required. |
| Models | Modelfiles | working | Opens the editor for creating, opening, saving, validating, previewing, and building Modelfiles. | No Phase 1 changes planned. |
| Models | Templates | working | Requires a selected model, loads metadata asynchronously, and reports terminal status/errors. | Display remains a general model metadata view. |
| Agents | Create/manage | partial | Agent profiles can be created, saved, imported, and exported. | Profiles do not yet affect chat generation, tools, memory, or execution policy. |
| Plugins | Install | partial | Copies a selected Python plugin into the configured plugin directory. | Installation does not yet guide the user through trust and enablement. |
| Plugins | Enable | blocked | The manager correctly refuses to execute plugins absent from `trusted_plugins`. | A clear Trust/Untrust UI workflow is required. |
| Prompts | Prompt dock | working | Lists saved prompts and applies a selected prompt to the current chat. | No Phase 1 changes planned. |
| Prompts | Full manager | hidden | A prompt manager dialog supports create, save, delete, import, and export. | Add a clear menu entry in a later approved phase. |
| Help | Documentation | working | Opens repository documentation when available and reports missing/unreadable files without crashing. | Installed packaging may need to bundle documentation explicitly. |
| Plugins | Developer documentation | working | Opens the Plugin SDK when available and reports missing/unreadable files without crashing. | Installed packaging may need to bundle documentation explicitly. |
