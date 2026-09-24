# LocalLama Exhaustive Codebase Mapping
## Canonical Architecture + Symbol Inventory Specification

**Repository:** `GR00T-User-706/locallama-gui`  
**Primary branch under audit:** `feat/myloai-production-packaging`  
**Comparison branch:** `main`  
**Audit mode:** READ-ONLY  
**Purpose:** Define and capture an exhaustive, machine-verifiable map of the application before architectural changes are made.

---

## 1. Audit Contract

This document is the canonical specification for the first-pass codebase mapping.

The mapping is intentionally broader than a normal architecture diagram. It must expose not only modules and dependency relationships, but also the concrete implementation surfaces that determine ownership, coupling, runtime behavior, persistence, extensibility, and branch drift.

### Non-negotiable rules

1. Do not modify repository files during collection.
2. Do not rename, refactor, reorganize, or "clean up" code during the mapping pass.
3. Do not infer a symbol that cannot be verified from source.
4. Preserve exact module, class, function, method, property, field, constant, path, endpoint, signal, slot, and CLI names.
5. Record source location for every inventory item.
6. Distinguish static declarations from runtime-discovered behavior.
7. Distinguish `main` from `feat/myloai-production-packaging`.
8. Record missing/unknown information explicitly instead of inventing it.
9. Treat branch differences as first-class inventory records.
10. The mapping must be reproducible from a fresh checkout.

---

# 2. Scope

The exhaustive mapping covers:

- Python application source
- tests
- packaging/install code
- CLI scripts and entry points
- plugin SDK and plugin loading
- configuration
- persistence
- filesystem usage
- environment variables
- HTTP/provider integrations
- Qt UI
- Qt signals/slots
- asynchronous workers and execution boundaries
- domain/data models
- backend abstractions
- controllers/managers
- branch-specific additions, removals, modifications, and symbols
- documentation only where it defines executable contracts or public interfaces

The mapping is **not** limited to `locallama_gui/`.

---

# 3. Master Inventory Record

Every discovered object should be represented internally by a record with at least:

| Field | Meaning |
|---|---|
| `id` | Stable inventory identifier |
| `branch` | `main` or `feat/myloai-production-packaging` |
| `file` | Repository-relative source path |
| `line_start` | First source line |
| `line_end` | Last relevant source line |
| `kind` | Inventory category |
| `name` | Exact declared/reference name |
| `qualified_name` | Fully qualified symbol when applicable |
| `owner` | Containing module/class/component |
| `visibility` | Public/private/internal |
| `definition` | Declaration site |
| `references` | Known callers/users |
| `dependencies` | Direct dependencies |
| `side_effects` | I/O, persistence, process, network, UI, etc. |
| `branch_status` | Added/removed/changed/unchanged |
| `confidence` | Verified/static/dynamic/unknown |
| `notes` | Important architectural information |

---

# 4. Mandatory Inventory #1: Every Module

## Required capture

For every Python module/package:

- repository path
- importable module name
- package membership
- `__init__.py` status
- public/private classification
- classes
- functions
- constants
- imports
- environment references
- filesystem references
- network references
- Qt references
- worker references
- persistence references
- plugin references
- test coverage/targets

## Module record

| Module | File | Package | Imports | Classes | Functions | Constants | Side Effects | Tests |
|---|---|---|---|---|---|---|---|---|

---

# 5. Mandatory Inventory #2: Every Import

Every import must be recorded individually.

Capture:

- `import X`
- `import X as Y`
- `from X import Y`
- relative imports
- conditional imports
- optional imports
- dynamically constructed imports where detectable
- import-time side effects

## Import record

| Source Module | Imported Module | Symbol | Alias | Relative | Conditional | Optional | Used By |
|---|---|---|---|---|---|---|---|

Important distinction:

**Import dependency != runtime dependency.**

Both must be represented where they differ.

---

# 6. Mandatory Inventory #3: Every Class

Capture every class declaration.

Required fields:

- class name
- module
- base classes
- metaclass if explicit
- decorators
- constructor
- methods
- properties
- signals
- slots
- instance attributes
- class attributes
- constants
- protocols/ABCs
- callers/instantiators
- tests

## Class record

| Class | Module | Bases | Decorators | Constructor | Methods | Properties | Signals | Slots | State |
|---|---|---|---|---|---|---|---|---|---|

---

# 7. Mandatory Inventory #4: Every Method

Capture every method, including:

- `__init__`
- dunder methods
- synchronous methods
- async methods
- private methods
- class methods
- static methods
- Qt slots
- overridden methods
- abstract methods
- default implementations

Record:

- owner class
- method name
- parameters
- return annotation
- async/sync
- decorators
- exceptions
- state mutations
- external calls
- persistence
- UI mutations
- worker crossings

---

# 8. Mandatory Inventory #5: Every Function

Capture every module-level function.

For each:

| Function | Module | Parameters | Return | Async | Decorators | Calls | Side Effects | Tests |
|---|---|---|---|---|---|---|---|---|

Include helper functions that appear trivial. Small functions become architectural load-bearing walls with alarming regularity.

---

# 9. Mandatory Inventory #6: Every Property

Capture:

- `@property`
- property setters
- property deleters
- Qt property mechanisms
- dynamically exposed properties where detectable

Record:

| Property | Owner | Getter | Setter | Deleter | Reads State | Writes State | External Side Effect |
|---|---|---|---|---|---|---|---|

---

# 10. Mandatory Inventory #7: Every Dataclass Field

Every dataclass must be expanded field-by-field.

Capture:

- class
- field name
- annotation
- default
- default factory
- initialization behavior
- serialization behavior
- consumers

Known confirmed dataclasses include:

### `AppPaths`

- `config_dir`
- `data_dir`
- `logs_dir`
- `sessions_dir`
- `prompts_dir`
- `agents_dir`
- `modelfiles_dir`
- `plugins_dir`

### `ProviderProfile`

- `name`
- `provider_type`
- `base_url`
- `api_key`
- `default_model`
- `enabled`

### `GenerationParameters`

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
- `reasoning_mode`
- `thinking_mode`
- `plan_mode`
- `normal_mode`

### `UISettings`

- `theme`
- `geometry_hex`
- `state_hex`
- `active_session_id`
- `font_size`

### `AppConfig`

- `paths`
- `schema_version`
- `provider_profiles`
- `active_provider`
- `parameters`
- `parameter_presets`
- `enabled_plugins`
- `trusted_plugins`
- `developer_mode`
- `ui`
- `global_system_prompt`

### `BackendStatus`

- `state`
- `latency_ms`
- `detail`

All additional dataclasses discovered by the full scan must be added.

---

# 11. Mandatory Inventory #8: Every Protocol / ABC

Capture every:

- `Protocol`
- `ABC`
- `abstractmethod`
- interface-like class
- structural interface
- Qt interface pattern

For each interface:

| Interface | Type | Required Members | Implementations | Consumers | Branch Differences |
|---|---|---|---|---|---|

Known confirmed interfaces:

### `LLMBackend(ABC)`

Abstract operations:

- `test_connection`
- `list_models`
- `chat`

Default backend operations:

- `pull_model`
- `push_model`
- `delete_model`
- `copy_model`
- `create_model`
- `show_model`

### `PluginAPI(Protocol)`

Required:

- `manifest`
- `activate(context)`
- `deactivate()`

### `ChatWindowPort(Protocol)`

Required:

- `current_tab`
- `set_tab_title`
- `render_tab`
- `generate_for_tab`
- `refresh_sessions`
- `log`
- `open_session`

---

# 12. Mandatory Inventory #9: Every Constant

Capture:

- module constants
- class constants
- enum-like constants
- endpoint constants
- default values that function as contracts
- environment variable names
- application identifiers
- schema versions
- supported-option lists

Known confirmed examples:

`locallama_gui/core/config.py`

- `APP_NAME = "locallama-gui"`
- `CONFIG_SCHEMA_VERSION = 2`
- `APP_SYSTEM_PROMPT`

`locallama_gui/backends/ollama.py`

- `SUPPORTED_OPTIONS`

Every additional literal that functions as an application contract should be evaluated and recorded.

---

# 13. Mandatory Inventory #10: Every Instance Attribute

This is separate from dataclass fields.

Capture every attribute assigned to `self`, including assignments inside:

- `__init__`
- setup methods
- callbacks
- lazy initialization
- Qt construction
- worker startup
- plugin activation

Record:

| Class | Attribute | First Assignment | Type/Value | Mutated By | Read By | Lifecycle |
|---|---|---|---|---|---|---|

This inventory is critical for determining actual state ownership.

Known `MainWindow` state includes, among other items:

- `config`
- `sessions`
- `prompts`
- `agents`
- `plugin_context`
- `plugins`
- `models`
- `chat_controller`
- `model_controller`
- `plugin_controller`
- `worker_refs`
- `current_stream`
- `_stream_owner_seq`
- `_active_stream_owner`
- diagnostic state
- `_original_stdout`
- `_original_stderr`
- UI widget references

The complete scan must enumerate every additional `self.*` assignment.

---

# 14. Mandatory Inventory #11: Every Environment-Variable Reference

Capture every:

- `os.environ[...]`
- `os.getenv(...)`
- `os.environ.get(...)`
- environment lookup helper
- subprocess environment construction
- documented environment variable
- shell-script environment export
- packaging environment dependency

Record:

| Variable | File | Line | Read/Write | Default | Consumer | Purpose | Branch Difference |
|---|---|---:|---|---|---|---|---|

Do not assume undocumented variables are harmless. Environment variables are configuration APIs whether someone wrote documentation for them or not.

---

# 15. Mandatory Inventory #12: Every Filesystem Path

Capture literal and constructed paths.

Sources include:

- `Path(...)`
- `.resolve()`
- `.mkdir()`
- `.open()`
- `.read_text()`
- `.write_text()`
- `.exists()`
- `.glob()`
- `.rglob()`
- `shutil`
- `os.path`
- config directories
- XDG paths
- platformdirs
- package resource paths
- installer paths
- desktop-file paths
- log paths
- session paths
- plugin paths
- modelfile paths
- test fixtures

Record:

| Path | File | Construction | Read | Write | Create | Delete | Owner | Persistence Role |
|---|---|---|---|---|---|---|---|---|

Known application path groups:

- config
- data
- logs
- sessions
- prompts
- agents
- modelfiles
- plugins

---

# 16. Mandatory Inventory #13: Every HTTP Endpoint

Capture every network endpoint and request.

Required fields:

| Provider | Method | Endpoint | Caller | Payload | Response | Streaming | Auth | Error Handling | Tests |
|---|---|---|---|---|---|---|---|---|---|

Known Ollama endpoints:

- `GET /api/tags`
- `POST /api/chat`
- `POST /api/pull`
- `POST /api/push`
- `DELETE /api/delete`
- `POST /api/copy`
- `POST /api/create`
- `POST /api/show`

Also capture:

- base URL construction
- headers
- authentication
- timeouts
- streaming transport
- JSON encoding/decoding
- retry behavior
- provider-specific request sanitization

OpenAI-compatible endpoints must be enumerated from source rather than inferred from the provider name.

---

# 17. Mandatory Inventory #14: Every CLI Entry Point

Capture:

- console scripts
- `if __name__ == "__main__"`
- executable scripts
- shell entry points
- installer commands
- launcher commands
- package entry points
- command dispatchers
- argparse/click/typer/etc.
- desktop-launch command paths

Record:

| Entry Point | File | Command | Arguments | Calls | Environment | Privileges | Packaging |
|---|---|---|---|---|---|---|---|

Scripts under `scripts/` must be included.

---

# 18. Mandatory Inventory #15: Every Plugin Hook

Capture every extension point.

Known plugin surfaces:

### `PluginAPI`

- `manifest`
- `activate(context)`
- `deactivate()`

### `PluginContext`

State exposed:

- `main_window`
- `config`
- `tools`
- `commands`
- `chat_interceptors`
- `memory_providers`

Registration methods:

- `register_tool`
- `register_command`
- `register_chat_interceptor`
- `add_panel`

Plugin lifecycle operations:

- discover
- validate manifest
- trust
- untrust
- enable
- disable
- load
- reload
- remove
- activate
- deactivate

The mapping must also capture plugin filesystem discovery and manifest parsing.

Important implementation fact to preserve:

`PluginContext` exposes `memory_providers`, but the confirmed API surface does not currently include a corresponding `register_memory_provider` method. This is an API consistency observation, not a reason to redesign the system during the audit.

---

# 19. Mandatory Inventory #16: Every Worker Boundary

Capture every transition between:

- GUI thread
- worker thread
- async task
- coroutine
- executor
- subprocess
- external process
- network stream

For each boundary:

| Caller | Worker | Direction | Mechanism | Input | Output | Cancellation | Error | UI Callback |
|---|---|---|---|---|---|---|---|---|

Known worker surfaces include:

- `AsyncTask`
- `StreamTask`

Known live chat path:

`MainWindow._generate`
→ backend construction
→ `backend.chat(...)`
→ `StreamTask`
→ token/error/completion callbacks
→ UI/session state

Cancellation and stale-stream ownership must be mapped explicitly.

---

# 20. Mandatory Inventory #17: Every Qt Signal / Slot

Capture every:

- `Signal(...)`
- `@Slot`
- connected signal
- callback passed to `.connect(...)`
- custom event mechanism
- overridden Qt event handler

Record:

| Signal | Owner | Signature | Emitted By | Connected To | Thread Context |
|---|---|---|---|---|---|

Known confirmed signals:

### `ComposerTextEdit`

- `send_requested`
- `zoom_requested`

### `MainWindow`

Uses imported PySide6 `Signal` and must be fully enumerated by source scan.

Worker signals and dialog signals must also be included.

---

# 21. Mandatory Inventory #18: Every Persistence Operation

Capture every operation that creates, reads, updates, deletes, imports, exports, serializes, or migrates persistent state.

Categories:

- JSON
- text
- configuration
- sessions
- prompts
- agents
- model files
- plugin state
- keyring
- application settings
- Qt geometry/state
- caches
- logs
- generated files

Record:

| Operation | Owner | Storage | Format | Path | Read/Write | Serialization | Migration | Failure Mode |
|---|---|---|---|---|---|---|---|---|

Known persistence components:

### `SessionManager`

- `list_sessions`
- `load`
- `save`
- `import_session`

### `PromptManager`

- `list`
- `save_all`
- `upsert`
- `delete`
- `import_file`
- `export`

### `AgentManager`

- `list`
- `save_all`
- `upsert`

### `AppConfig`

- `load`
- `save`
- `_migrate_data`

### Credential storage

`CredentialStore` uses OS keyring storage for provider API keys.

Configuration JSON deliberately excludes stored API keys.

---

# 22. Mandatory Inventory #19: Every Test Target

Tests must be mapped to implementation targets.

Capture:

- test files
- test classes
- test functions
- fixtures
- mocks
- monkeypatches
- parametrization
- integration tests
- UI tests
- backend tests
- packaging tests
- installer tests
- plugin tests
- persistence tests
- branch-specific tests

Record:

| Test | File | Target | Type | Fixture | External Dependency | Branch |
|---|---|---|---|---|---|---|

Also produce a reverse matrix:

`implementation symbol → tests`

This reveals important code that has no direct test target.

---

# 23. Mandatory Inventory #20: Every Branch-Specific Symbol Difference

This is not merely a Git diff.

Compare the two branches at symbol level.

For every changed source file determine:

- added module
- removed module
- added class
- removed class
- changed class inheritance
- added method
- removed method
- changed method signature
- added function
- removed function
- added property
- removed property
- added dataclass field
- removed dataclass field
- changed constant
- added instance attribute
- removed instance attribute
- added import
- removed import
- changed endpoint
- changed path
- changed environment variable
- changed signal
- changed slot
- changed worker boundary
- changed persistence operation
- changed plugin hook
- changed CLI entry point
- changed test target

## Branch-difference record

| Symbol | Kind | File | Main | Feature Branch | Status | Behavioral Impact |
|---|---|---|---|---|---|---|

Allowed statuses:

- `UNCHANGED`
- `ADDED`
- `REMOVED`
- `MODIFIED`
- `RENAMED`
- `MOVED`
- `SIGNATURE_CHANGED`
- `IMPLEMENTATION_CHANGED`
- `CONTRACT_CHANGED`
- `UNKNOWN`

A textual diff alone is insufficient.

---

# 24. Known Architecture Anchors

These are confirmed implementation anchors and should seed the full inventory.

## Configuration

`locallama_gui/core/config.py`

Confirmed components:

- `CredentialStore`
- `AppPaths`
- `ProviderProfile`
- `GenerationParameters`
- `UISettings`
- `AppConfig`

## Managers

`locallama_gui/core/managers.py`

Confirmed components:

- `SessionManager`
- `PromptManager`
- `AgentManager`
- `PluginAPI`
- `PluginContext`
- `LoadedPlugin`
- `PluginManager`

## Backend abstraction

`locallama_gui/backends/base.py`

- `BackendStatus`
- `LLMBackend`

## Backend factory

`locallama_gui/backends/manager.py`

`create_backend(profile)`

Provider mapping confirmed:

- `openai` → `OpenAICompatibleBackend`
- `llama.cpp` → `OpenAICompatibleBackend`
- other/default → `OllamaBackend`

## Ollama backend

`locallama_gui/backends/ollama.py`

Confirmed class:

- `OllamaBackend`

## Chat controller

`locallama_gui/ui/controllers/chat_controller.py`

Confirmed:

- `ChatWindowPort`
- `ChatController`

## Main window

`locallama_gui/ui/main_window.py`

Confirmed:

- `ChatTab`
- `ComposerTextEdit`
- `MainWindow`

## Controller layer

Known controller modules:

- `chat_controller.py`
- `model_controller.py`
- `plugin_controller.py`

## Worker layer

Known worker module:

- `workers.py`

Confirmed worker classes:

- `AsyncTask`
- `StreamTask`

## Diagnostics

Known diagnostic components:

- `DiagnosticsSignals`
- `LineBufferedStream`
- `OperationStreamParser`
- `OperationUpdate`
- `QtLogHandler`
- `append_output`

## Dialog layer

Known dialogs include:

- `AgentBuilderDialog`
- `EndpointDialog`
- `ModelfileEditor`
- `ParameterDialog`
- `PluginManagerDialog`
- `PromptManagerDialog`

## UI support

Known modules include:

- `chat_view.py`
- `model_browser.py`
- `production_fixes.py`
- `setup_wizard.py`
- `theme.py`

---

# 25. Confirmed Chat Execution Pipeline

The currently confirmed live-branch generation path is:

```text
Chat UI
  ↓
ChatController
  ↓
MainWindow._generate()
  ↓
AppConfig.active_profile()
  ↓
create_backend(profile)
  ↓
LLMBackend implementation
  ↓
provider HTTP API
```

Within `MainWindow._generate()` the confirmed sequence includes:

1. obtain active provider profile
2. create backend
3. select model
4. update session model/provider
5. create application system message
6. append session messages
7. apply `plugin_context.chat_interceptors`
8. convert generation parameters to backend options
9. construct request preview
10. construct Ollama payload when applicable
11. redact/display request information
12. update UI status
13. append empty assistant message
14. create `StreamTask`
15. assign stream ownership
16. connect token/error/completion callbacks
17. start worker

This sequence must be represented in the final dependency/sequence map.

---

# 26. State Ownership Mapping

The audit must explicitly answer:

> Which component owns each piece of mutable state?

For every mutable object, produce:

| State | Owner | Readers | Writers | Persistence | Thread | UI Exposure |
|---|---|---|---|---|---|---|

Particular attention must be paid to:

- current chat session
- message list
- active model
- active provider
- generation parameters
- plugin state
- worker references
- active stream
- stream ownership
- diagnostics state
- UI geometry/state
- configuration
- credentials

---

# 27. Dependency Direction Mapping

For every dependency, classify direction:

```text
UI
 ↓
Controller
 ↓
Manager / Service
 ↓
Domain / Backend abstraction
 ↓
Backend implementation
 ↓
External system
```

The actual codebase may violate this idealized direction. Those violations must be recorded rather than "fixed" during mapping.

Example:

`MainWindow._generate()` currently performs orchestration involving configuration, plugin interceptors, backend construction, request preparation, streaming, and UI state.

The audit should document this as an observed dependency relationship.

---

# 28. Cross-Reference Requirements

The completed inventory must support these queries:

### Symbol → dependencies

"Show everything this class depends on."

### Symbol → consumers

"Show everything that calls or uses this symbol."

### State → writers

"Who can mutate this state?"

### Path → operations

"Who reads/writes this file?"

### Endpoint → callers

"Who invokes this API?"

### Signal → slots

"What receives this signal?"

### Worker → UI

"How does worker output reach the UI?"

### Plugin hook → implementations

"Which plugins can attach here?"

### Test → production target

"What code does this test protect?"

### Branch → architectural change

"What changed between `main` and the feature branch?"

---

# 29. Static Extraction Rules

The first collection pass should use AST-based extraction wherever possible.

Minimum Python AST targets:

- `Module`
- `Import`
- `ImportFrom`
- `ClassDef`
- `FunctionDef`
- `AsyncFunctionDef`
- `AnnAssign`
- `Assign`
- `NamedExpr`
- decorators
- `Call`
- `Attribute`
- `Name`
- `Constant`
- `With`
- `AsyncWith`
- exception handlers
- class bases
- function arguments

AST extraction should identify declarations.

Text/search analysis should supplement AST for:

- shell commands
- endpoint strings
- filesystem patterns
- environment variables
- Qt `.connect(...)`
- dynamic imports
- subprocess invocation
- plugin discovery
- packaging metadata

Dynamic runtime discovery should be a separate evidence layer.

---

# 30. Evidence Levels

Every inventory record must identify its evidence level.

### `STATIC_VERIFIED`

Directly established from source.

### `STATIC_INFERRED`

Strongly implied by static code structure but not directly declared.

### `DYNAMIC_VERIFIED`

Confirmed by execution/instrumentation.

### `DOCUMENTED`

Defined by project documentation but not confirmed in implementation.

### `UNKNOWN`

Could not be established.

Never silently convert one category into another.

---

# 31. Completeness Gates

The mapping is not considered complete until all of these are satisfied:

- [ ] Every Python module inventoried
- [ ] Every import inventoried
- [ ] Every class inventoried
- [ ] Every method inventoried
- [ ] Every function inventoried
- [ ] Every property inventoried
- [ ] Every dataclass field inventoried
- [ ] Every Protocol inventoried
- [ ] Every ABC inventoried
- [ ] Every constant inventoried
- [ ] Every instance attribute inventoried
- [ ] Every environment variable inventoried
- [ ] Every filesystem path inventoried
- [ ] Every HTTP endpoint inventoried
- [ ] Every CLI entry point inventoried
- [ ] Every plugin hook inventoried
- [ ] Every worker boundary inventoried
- [ ] Every Qt signal inventoried
- [ ] Every Qt slot inventoried
- [ ] Every persistence operation inventoried
- [ ] Every test target inventoried
- [ ] Every branch-specific symbol difference inventoried

---

# 32. Required Final Outputs From the Mapping Pass

The mapping process should ultimately produce these artifacts:

```text
architecture/
├── LocalLama_Exhaustive_Codebase_Mapping.md
├── modules.md
├── imports.md
├── classes.md
├── methods.md
├── functions.md
├── properties.md
├── dataclass_fields.md
├── interfaces.md
├── constants.md
├── instance_attributes.md
├── environment_variables.md
├── filesystem_paths.md
├── http_endpoints.md
├── cli_entrypoints.md
├── plugin_hooks.md
├── worker_boundaries.md
├── qt_signals_slots.md
├── persistence.md
├── tests.md
├── branch_symbol_diff.md
├── dependency_graph.md
├── state_ownership.md
└── completeness_report.md
```

The individual files are optional implementation outputs. The canonical mapping itself must contain enough information to reconstruct them.

---

# 33. Machine-Readable Companion Format

A machine-readable representation should use records resembling:

```json
{
  "id": "symbol:locallama_gui.core.config:AppConfig",
  "branch": "feat/myloai-production-packaging",
  "kind": "class",
  "file": "locallama_gui/core/config.py",
  "name": "AppConfig",
  "qualified_name": "locallama_gui.core.config.AppConfig",
  "line_start": null,
  "line_end": null,
  "bases": [],
  "members": [],
  "references": [],
  "branch_status": "UNCHANGED",
  "confidence": "STATIC_VERIFIED"
}
```

Line numbers are deliberately left as placeholders here because this specification is not a substitute for executing the repository scan.

---

# 34. Branch Baseline

Previously established repository references:

- `main`: `86e3ec01cc3e18e1c3d0ec41d22a95e2aa006154`
- `feat/myloai-production-packaging`: `5e2c520426386084d795779f3121a3a856d4459a`

Previously identified merge base:

- `e2f0d56...`

These references should be revalidated at scan time before being used as the final audit baseline.

---

# 35. What This Mapping Is For

The purpose is to make the architecture visible **before changing it**.

The desired end state is not merely:

```text
MainWindow
ChatController
Backend
PluginManager
```

That level of abstraction hides exactly the information needed to safely modularize the application.

The useful map must instead answer questions such as:

- Which module imports which module?
- Which class owns which state?
- Which method mutates that state?
- Which UI object invokes that method?
- Which worker executes the operation?
- Which signal carries the result?
- Which backend receives it?
- Which HTTP endpoint is called?
- Which file or keyring entry persists the result?
- Which plugin hook can intercept it?
- Which environment variable changes its behavior?
- Which tests protect the behavior?
- Which of those relationships exist on one branch but not the other?

That is the level of mapping required before architectural separation can be evaluated safely.

---

# 36. Architectural Principle Captured by This Audit

The mapping must preserve the distinction between:

### UI responsibility

Rendering, user interaction, Qt state, visual feedback.

### Controller responsibility

User-intent orchestration and coordination.

### Manager/service responsibility

Persistence, configuration, plugin lifecycle, domain operations.

### Backend responsibility

Provider-specific communication.

### Worker responsibility

Asynchronous execution and thread boundaries.

### Domain responsibility

Application data and behavior independent of Qt where possible.

### External system responsibility

Ollama, OpenAI-compatible servers, llama.cpp, filesystem, keyring, OS services.

The audit does **not** assume the current code perfectly follows these boundaries.

It records where the current implementation does and does not follow them.

---

# 37. Read-Only Audit Checklist

Before collection:

- [ ] Checkout/inspect only
- [ ] No working-tree modifications
- [ ] No generated files inside repository unless explicitly requested
- [ ] Record branch commit IDs
- [ ] Record merge base
- [ ] Record Python version used for AST parsing
- [ ] Record scanner version

During collection:

- [ ] Parse every `.py`
- [ ] Scan shell scripts
- [ ] Scan packaging metadata
- [ ] Scan tests
- [ ] Scan desktop launchers
- [ ] Scan workflow scripts where they affect application behavior
- [ ] Scan documentation for declared interfaces
- [ ] Compare both branches

After collection:

- [ ] Deduplicate symbols
- [ ] Resolve qualified names
- [ ] Attach source locations
- [ ] Build reverse references
- [ ] Build branch comparison
- [ ] Flag unresolved/dynamic behavior
- [ ] Run completeness gates

---

# 38. Final Rule

This document defines the **minimum acceptable granularity** for the first codebase map.

A report that only lists:

- files
- major classes
- broad architecture
- obvious dependencies

is **not exhaustive**.

A report becomes exhaustive only when it can account for all 20 mandatory categories and establish relationships among them.

The goal is not to make the codebase look clean.

The goal is to make the codebase **knowable**.
