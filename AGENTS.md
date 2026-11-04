# AGENTS.md

This file defines the operating rules for any AI agent, coding assistant, automation, or human contributor working in this repository.

The short version: **do the requested work, preserve the project, update the version, update the docs, and do not rewrite the universe because someone asked for one button.**

---

## 1. Prime Directive

Make the smallest responsible change that fully satisfies the task.

Agents must avoid unnecessary rewrites, broad refactors, file renames, architecture swaps, framework changes, or style churn unless the requested task clearly requires it.

If the user asks for:

> Add a button for creating a model.

That means:

> Add the button and the supporting logic needed for model creation.

It does **not** mean:

> Replace the GUI framework, invent a new plugin system, move every file, rewrite the state layer, rename half the repo, and call it "cleanup."

Do not do that.

---

## 2. Project Identity

This repository is for a production-grade desktop frontend for Ollama built with Python and PySide6.

The application should behave like a serious local LLM control center, not a disposable demo wrapper.

Core goals:

- Provide a polished graphical frontend for Ollama.
- Preserve and improve existing working functionality.
- Keep the app stable, responsive, and maintainable.
- Prefer practical production quality over theoretical architectural purity.
- Treat existing user work as valuable unless clearly proven obsolete or broken.

---

## 3. Scope Control

Before changing files, identify the actual requested scope.

### Good behavior

- Read the relevant files first.
- Determine the smallest safe implementation path.
- Modify only files related to the task.
- Preserve existing public behavior unless the task requires changing it.
- Keep unrelated formatting changes out of the patch.
- Explain any necessary larger change before making it.

### Bad behavior

- Rewriting entire modules for a small feature.
- Renaming files without need.
- Reorganizing directories without need.
- Changing UI layout globally when only one panel needs work.
- Replacing working code because it is not your favorite style.
- Introducing new dependencies without strong justification.
- Breaking existing behavior while chasing elegance.

---

## 4. No Rewrite-the-Universe Rule

A full rewrite is forbidden unless at least one of these is true:

1. The existing implementation is nonfunctional and cannot reasonably be repaired.
2. The existing implementation contains serious security or data-loss risks.
3. The requested task explicitly asks for a rewrite.
4. The maintainer approves the rewrite after the agent documents why it is necessary.

If a rewrite seems necessary, first document:

- What is broken.
- Why a minimal patch is not enough.
- What files would be replaced.
- What behavior must be preserved.
- What migration or rollback path exists.

Do not silently rewrite core systems.

---

## 5. Preservation Rule

Do not delete old code casually.

If code is obsolete, duplicate, experimental, or broken but may contain useful logic, move it to `archive/` instead of deleting it.

Use this structure when practical:

```text
archive/
  old/
  experimental/
  broken/
  duplicate/
  notes/
```

When archiving files, update:

```text
archive/ARCHIVE_INDEX.md
```

Each entry must include:

- Original path.
- New archive path.
- Date archived.
- Reason archived.
- Whether useful logic remains.
- Related version or changelog entry.

Do not archive files just because they are ugly. Ugly working code may be improved. Broken or superseded code may be archived.

---


## 5.1 Archive Validation Scope

Archived code under `archive/**` is historical storage, not active runtime.

- Production CI, lint, and test workflows must target active code paths only.
- Archived trees must be excluded from routine CI validation scope.
- If archived code is revived for use, it must be moved to an active path under current naming/conventions and validated there.

---

## 6. Versioning Is Mandatory

Every meaningful change must bump the version.

No completed task is valid unless the version has been inspected and updated correctly.

### Before changing the version

Inspect the repository for the existing version source:

- `VERSION`
- `pyproject.toml`
- `setup.py`
- `setup.cfg`
- package `__init__.py`
- app metadata/constants
- About dialog
- README references
- docs references

Update all version locations that are meant to stay in sync.

### Versioning scheme

Use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

Guidelines:

- PATCH: bug fixes, lint fixes, small UI fixes, documentation corrections.
- MINOR: new features, meaningful UX improvements, new panels, new workflows.
- MAJOR: breaking changes, major architecture migrations, incompatible config changes.

When unsure, use PATCH for fixes and MINOR for user-visible features.

---

## 7. Changelog Is Mandatory

Every version bump must append an entry to:

```text
CHANGELOG.md
```

Use this format:

```markdown
## [x.y.z] - YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Archived
- ...

### Documentation
- ...
```

Only include sections that apply.

Do not rewrite the whole changelog unless explicitly asked.
Append the new entry at the top unless the repo uses a different clear convention.

---

## 8. Documentation Must Stay Current

If a change affects behavior, usage, configuration, architecture, packaging, or developer workflow, update the relevant documentation.

Possible documentation files:

- `README.md`
- `CHANGELOG.md`
- `docs/REPO_ANALYSIS.md`
- `docs/VERSIONING.md`
- `docs/QA_CHECKLIST.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `archive/ARCHIVE_INDEX.md`

### Required doc updates by change type

| Change type | Required documentation |
|---|---|
| New user-facing feature | `README.md`, `CHANGELOG.md` |
| Version bump | `CHANGELOG.md`, version source files |
| New setting/config option | `README.md` or config docs |
| New dependency | `README.md`, package/dependency files |
| New architecture/module layout | architecture/development docs |
| Archived files | `archive/ARCHIVE_INDEX.md`, `CHANGELOG.md` |
| Packaging/build change | `README.md`, packaging docs |
| Test workflow change | `README.md` or development docs |

---

## 9. UI Work Rules

This is a PySide6 GUI application. UI changes must be careful.

### Required behavior

- Do not block the GUI thread.
- Long operations must use workers, threads, signals, async-safe patterns, or existing project conventions.
- Buttons must work, be disabled, or be hidden.
- No dead controls.
- No fake menu items.
- No placeholder actions pretending to be complete features.
- Preserve the existing visual identity unless the task asks for redesign.
- Avoid cramped or unreadable UI.
- Keep panels and controls understandable.

### For Ollama operations

The GUI must not freeze during:

- model pulls
- model deletes
- model creation
- chat generation
- streaming responses
- model refresh
- server checks
- file imports/exports that may take noticeable time

---

## 9.1 UI Action Integrity

Every visible UI action must have clear and honest operational status.

### Integrity requirements

- Every visible control must be one of the following: fully working, explicitly disabled, intentionally hidden, or documented as not implemented.
- Active dead placeholders are prohibited.
- Ambiguous dialogs are prohibited; prompts and confirmations must clearly state what action is happening and what outcome to expect.

### New UI action delivery checklist

When introducing a new user-triggered UI action, wire all required implementation responsibilities:

- Action logic and signal/handler wiring.
- User-facing error handling and recovery messaging.
- Logging and status/progress updates where applicable.
- Documentation updates for user/developer visibility.
- Relevant tests or validation coverage updates where practical.
- Required version bump updates.
- Required `CHANGELOG.md` entry updates.

### Scope guardrail

For small UI requests, implement the smallest responsible change that completes the requested action without rewrite-the-universe refactors.

---

## 10. Ollama Integration Rules

Prefer a clean integration layer.

Avoid burying Ollama logic directly inside button callbacks.

Good structure:

- GUI calls service/client.
- Service/client handles Ollama API or CLI.
- Workers handle long-running operations.
- UI receives signals/events and updates safely.

Prefer the Ollama HTTP API when practical.
Use CLI fallback only when needed or already established by the project.

Handle failures clearly:

- Ollama not installed.
- Ollama service not running.
- Host unreachable.
- Model missing.
- Pull failed.
- Generation canceled.
- Invalid parameters.
- Malformed response.

Errors should be visible to the user in plain English and logged for debugging.

---

## 11. Testing and Validation

Before finishing a task, run the most relevant checks available.

Start with:

```bash
ruff check .
```

If formatting is configured:

```bash
ruff format .
```

If tests exist:

```bash
pytest
```

Also consider:

```bash
python -m compileall .
```

For GUI smoke testing, verify at minimum:

- App imports.
- Main window launches.
- Missing Ollama does not crash the app.
- Connected Ollama status works if available.
- Model refresh does not freeze the UI.
- Send/stop generation behavior is safe.

If a check cannot be run in the current environment, document that clearly in the final response.

Do not claim tests passed unless they were actually run.

---

## 12. Lint and Style Rules

Follow the repository's configured style.

If Ruff is used, satisfy Ruff.

Common required fixes:

### Do not use one-line conditional returns

Bad:

```python
if not project: return "Error: missing project."
```

Good:

```python
if not project:
    return "Error: missing project."
```

### Do not capture exception variables unsafely in lambdas

Bad:

```python
except Exception as e:
    self.root.after(0, lambda: self.update_output(f"Error: {e}\n"))
```

Good:

```python
except Exception as e:
    error_msg = str(e)
    self.root.after(0, lambda: self.update_output(f"Error: {error_msg}\n"))
```

Preserve existing behavior while fixing lint issues.

---

## 13. Dependency Rules

Do not add dependencies casually.

Before adding a dependency, verify:

- It is necessary.
- The functionality cannot be reasonably implemented with existing dependencies.
- It is maintained.
- It works cross-platform.
- It does not bloat the app without value.
- It is added to the correct dependency file.
- Documentation is updated.

Do not replace PySide6.
Do not introduce a second GUI framework.

---

## 14. File and Naming Rules

Do not rename files unless necessary.

Acceptable reasons to rename:

- The current name is objectively wrong and causing confusion or import issues.
- The task explicitly asks for it.
- A packaging/import bug requires it.
- The rename is part of an approved cleanup plan.

When renaming:

- Update imports.
- Update docs.
- Update tests.
- Update packaging.
- Mention it in `CHANGELOG.md`.

---

## 15. Security and Safety Rules

Do not introduce unsafe behavior.

Be careful with:

- shell commands
- subprocess calls
- file deletion
- user-selected paths
- model deletion
- arbitrary command execution
- plugin execution
- environment variables
- logs that may expose sensitive local paths or tokens

Use safe subprocess invocation.
Avoid `shell=True` unless absolutely necessary and justified.
Validate paths before writing or deleting files.
Ask for confirmation in the GUI before destructive actions.

---

## 16. Git and Commit Hygiene

Keep changes focused.

A good change should be reviewable.

Avoid mixing unrelated work:

- Do not combine lint fixes with major UI redesign.
- Do not combine model creation with packaging overhaul unless required.
- Do not combine archive cleanup with chat streaming changes unless part of the task.

If multiple areas must change, document why.

---

## 17. Final Response Requirements

At the end of any task, provide a concise summary with:

- What changed.
- Files changed.
- Version before and after.
- Changelog entry added.
- Documentation updated.
- Tests/checks run.
- Whether checks passed.
- Known remaining issues.
- Any files archived and why.

Do not hide failures.
Do not claim validation that was not performed.

---

## 18. Task Execution Template

For every task, follow this workflow:

1. Read the request.
2. Identify the smallest safe scope.
3. Inspect relevant files.
4. Check versioning locations.
5. Implement the requested change.
6. Update or add tests when practical.
7. Update documentation.
8. Bump version.
9. Append `CHANGELOG.md`.
10. Run checks.
11. Report results honestly.

---

## 19. Special Rule for Small Feature Requests

For small requests, do small work.

Examples:

### Request

> Add a create model button.

Expected:

- Add the button in the right existing UI location.
- Wire it to existing or new create-model logic.
- Validate inputs.
- Run creation in a worker.
- Show success/failure.
- Update docs.
- Bump version.
- Update changelog.

Not expected:

- Rebuild the entire GUI.
- Replace the layout system.
- Rename the app.
- Redesign settings.
- Move all services.
- Rewrite the Ollama client from scratch unless it is broken.

### Request

> Fix Ruff lint.

Expected:

- Fix the lint errors.
- Preserve behavior.
- Run Ruff.
- Bump PATCH.
- Update changelog.

Not expected:

- Format the entire repo unless configured and requested.
- Refactor unrelated modules.
- Change app behavior.

---

## 20. Maintainer Preference

The maintainer values:

- directness
- minimal responsible changes
- working software
- preserved history
- clear versioning
- clear changelogs
- documentation that matches reality
- production-grade UX
- no theatrical overengineering

Treat the project like it matters.

Because it does.


## 5.2 Canonical Launcher/Desktop Names

Production native packaging uses these canonical identities:

- human-facing product: `MyLoAI Control Center`
- filesystem-safe application executable: `MyLoAI_Control_Center`
- Linux command: `myloai`
- Debian executable: `/opt/myloai/MyLoAI_Control_Center`
- Debian launcher: `/usr/bin/myloai`
- AppImage entry point: `AppRun`

The repository launcher and installer helpers remain development-only:

- `run-locallama`
- `scripts/install-launcher`
- `scripts/install-desktop-entry`

Native production desktop entries must not depend on those source-tree launchers.

The canonical Linux production build command is `./packaging/build-linux.sh`; build prerequisites and platform-specific packaging commands are documented in `docs/BUILDING.md`.

Routine CI/lint/test validation must stay scoped to active production paths and active tests. Do not include archive/legacy trees in routine validation; use manual archive-specific workflows only when intentionally auditing archives.


---

# Additional Agent Safety and Evidence Rules

The rules below supplement the existing repository rules. They are additive and do not replace or weaken any existing rule.

## A. Read-Only Audit Before Modification

Before modifying files, perform a read-only audit of the relevant project area.

The initial pass must not modify files, install dependencies, alter configuration, create replacement files, commit changes, or otherwise mutate repository state.

Establish the relevant:

- repository structure;
- existing implementation;
- project instructions;
- configuration;
- version sources;
- tests and validation commands;
- Git state when relevant;
- dependencies and interfaces involved in the task.

Do not begin implementation until the existing state is sufficiently understood.

If a material ambiguity is discovered, stop and identify it before proceeding.

## B. Evidence Over Assumption

**Do not invent facts.**

If information is not confirmed by the repository, current task, tool output, documentation, test results, or explicit user input, treat it as unknown.

Do not invent:

- file contents;
- APIs or capabilities;
- dependency behavior or versions;
- configuration values;
- architecture;
- requirements;
- test results;
- command output;
- Git state;
- successful execution;
- security guarantees.

Use these distinctions when reporting:

- **Confirmed:** directly observed.
- **Verified:** tested or independently checked.
- **Inferred:** logically derived but not directly confirmed.
- **Unknown:** insufficient evidence.
- **Blocked:** required information is unavailable.

Never present an inference as a confirmed fact.

## C. Ambiguity and Intent

Do not silently reinterpret an ambiguous request.

If multiple interpretations would materially change the implementation, stop and ask for clarification.

A request to complete a task authorizes the work required for that task, not unrelated refactoring, redesign, deletion, dependency replacement, or architecture changes.

## D. No Fabricated Completion

Never claim an action occurred unless it actually occurred and the result was observed.

Do not claim that tests passed, a build succeeded, documentation was updated, a version was changed, a commit was created, or a deployment succeeded unless that result was actually verified.

If validation could not be performed, state that explicitly.

## E. Post-Change Verification

After editing:

1. Inspect the resulting diff.
2. Check for unintended changes.
3. Run the most relevant available validation.
4. Verify the requested behavior when practical.
5. Report failures and unverified areas honestly.

## F. Consequential Decisions

Do not independently make materially consequential decisions that were not established by the user or repository instructions, including major architecture changes, public API changes, persistent data migrations, removal of functionality, security-boundary changes, or destructive operations.

If such a decision is necessary, explain the specific blocker and obtain direction before proceeding.

## G. Git Safety

Do not reset user work, discard uncommitted changes, rewrite history, force-push, rebase, amend commits, delete branches, or delete files unless the user explicitly requests the specific operation.

Never claim a Git operation succeeded without observing its result.

## H. Completion Report

When the task is complete, report:

- what changed;
- files changed;
- what was verified;
- what was not verified;
- known remaining issues;
- relevant Git state when inspected.

Task completion means the requested work was implemented and the available evidence supports the result. Editing files alone is not proof of completion.


## Additional AI Agent Requirements: Packaging, Help, and User Documentation

Apply the Cross-Platform Packaging and User Documentation Contract below to this repository. For software products, this contract governs every supported distribution method. For templates and packaging-tool repositories, preserve the same requirements in generated project guidance and template output.



---

# Cross-Platform Packaging and User Documentation Contract

These requirements are additive. They supplement existing project-specific instructions and do not replace, weaken, or silently reinterpret them.

## 1. One product, one installation contract

Every supported distribution format for the same software MUST deliver an equivalent, complete product installation.

This requirement applies to every format the project supports, including as applicable:

- Python source distributions, wheels, and supported Python installers;
- Termux packages and Termux YAML manifests;
- Debian packages and APT repositories;
- Arch Linux packages and PKGBUILD-based builds;
- RPM packages;
- Alpine packages;
- AppImage and other portable Linux bundles;
- Windows installers and portable distributions;
- macOS application bundles, disk images, and installers;
- source builds and other project-supported installation paths.

A project is not required to support every format. The project MUST clearly identify which formats are supported, experimental, planned, or unsupported. However, once a format is declared supported, it MUST satisfy this contract.

The installation format is a delivery mechanism, not a separate product definition. Users MUST NOT receive materially different application capabilities, command interfaces, configuration behavior, or required resources merely because they selected a different package format.

## 2. Canonical release payload

Each product MUST define one canonical release payload or an equivalent machine-verifiable payload specification. Every supported packaging backend MUST derive its installed file set from that specification or from a demonstrably equivalent source of truth.

The specification MUST identify, as applicable:

- executable binaries and application entry points;
- Python modules, libraries, plugins, and runtime resources;
- GUI assets, icons, desktop entries, MIME definitions, and application metadata;
- default configuration files and configuration schema;
- templates, migrations, schemas, certificates, and other required data files;
- shell completion files and command aliases;
- man pages and other user manuals;
- usage examples and reference documentation;
- license, copyright, and third-party notices;
- changelog and release information;
- service definitions, integration files, and platform-specific support resources;
- uninstall metadata or other information required for safe removal.

Every packaging backend MUST install all files required for the software to function as documented. It MUST NOT omit a required resource merely because a packaging format or build script has a separate implementation.

Documentation may be installed in platform-appropriate locations, and platform-specific executable artifacts may differ. The logical documentation set and user-visible product capabilities MUST remain equivalent. A format-specific omission MUST be explicitly justified and documented.

## 3. Installation behavior parity

Every supported installer MUST implement the same product-level lifecycle contract:

- install the product and its required runtime resources;
- expose the documented commands, launchers, APIs, and interfaces;
- install or generate the same documented default configuration;
- preserve user configuration and user data during upgrades unless a documented migration explicitly requires otherwise;
- perform required configuration or data migrations safely and transparently;
- establish required permissions and platform integrations;
- report actionable errors when prerequisites or permissions are missing;
- support the documented upgrade and repair behavior;
- remove product-owned files during uninstall without deleting user data or unrelated files;
- provide an accurate installed-version and installation-location result where the platform supports it.

Package managers may own their native transaction, dependency, and uninstall mechanics. Product-specific scripts MUST NOT fight those mechanisms or perform surprising side effects.

Installing through a Python installer, Termux, APT/DEB, Arch, RPM, AppImage, Windows, macOS, or source installation MUST NOT result in different required application files, documentation, default behavior, command capabilities, or configuration semantics.

## 4. Platform-specific differences

Platform differences are allowed only when required by the operating system, runtime, package ecosystem, filesystem layout, security model, or user interaction conventions.

Examples include executable formats, filesystem destinations, service managers, desktop integration, permissions, signing, application bundle layout, dependency declarations, and platform-native launchers.

Every such difference MUST be:

1. identified in the packaging documentation;
2. limited to the platform-specific implementation detail;
3. tested or validated on the relevant platform when practical; and
4. prevented from changing the product-level contract without an explicit product decision.

Do not claim that two package formats are equivalent merely because both build successfully.

## 5. Packaging metadata, build scripts, and installers

All package metadata, manifests, build scripts, installer scripts, release workflows, and backend adapters MUST describe or produce the same canonical product payload.

Contributors and agents MUST inspect every supported packaging path when changing:

- application entry points or command names;
- modules, resources, plugins, assets, or runtime dependencies;
- default or user configuration;
- documentation or man pages;
- permissions, services, desktop integration, or filesystem paths;
- version metadata or release contents;
- installation, upgrade, repair, or uninstall behavior.

Do not independently add a file to one package format while omitting it from another supported format. Do not maintain conflicting versions of product metadata when a canonical source or generated manifest can be used.

Build scripts MUST distinguish building from installing. Building a package MUST NOT silently install it on the host, modify active system prefixes, publish a release, or perform unrelated destructive operations.

Generated metadata and package artifacts MUST be reproducible to the extent supported by the toolchain. Validation MUST distinguish metadata validation, mocked backend tests, native package builds, payload inspection, and actual installation tests. Passing one category MUST NOT be reported as proof of another.

## 6. Required packaging parity validation

For each supported format, maintain an auditable mapping between the canonical release payload and the package's installed filesystem contents.

Where practical, automate checks that compare:

- required paths and file presence;
- executable names and entry points;
- application version metadata;
- configuration defaults and schema;
- man pages and user documentation;
- icons, desktop entries, plugins, templates, and runtime data;
- dependency declarations and runtime requirements;
- uninstall ownership and preservation of user data.

A parity check MUST fail when a required payload item is missing from a supported package. Differences that are intentionally platform-specific MUST be enumerated as explicit exceptions rather than hidden through broad exclusions.

At least one clean installation test SHOULD be maintained for each supported package family and platform. Tests MUST verify actual installed behavior where feasible, not only inspect package metadata.

## 7. User manuals and man pages are required deliverables

Every user-facing software product MUST provide useful operating documentation appropriate to its interfaces. Documentation is part of the product, not an optional development extra.

For command-line applications, provide:

- a man page for the primary command;
- man pages for additional major commands when their interfaces warrant separate references;
- complete command and option reference documentation;
- examples of common and advanced workflows;
- help for applicable subcommands;
- installation, configuration, troubleshooting, and uninstall instructions.

For GUI applications, provide a user manual covering the interface, workflows, settings, dialogs, menus, shortcuts, supported file formats, error recovery, and relevant integration behavior.

For APIs, libraries, services, and automation tools, provide API or function references, configuration documentation, request/response or function examples, lifecycle information, and operational guidance appropriate to the actual public interface.

The manuals MUST be written for users and operators who did not develop the software. Use professional, neutral product documentation language. Do not address an individual maintainer, refer to private conversations, narrate how an AI agent wrote the code, or assume that the reader already knows the implementation.

Documentation MUST describe observed, implemented behavior. Clearly identify unsupported, experimental, optional, or platform-limited behavior.

## 8. Configuration documentation requirements

Every user-editable configuration file, environment variable, command-line setting, or remotely configurable option MUST be documented.

For each setting, document:

- exact key or option name;
- purpose and effect;
- data type;
- default value, or explicitly state that no default exists;
- accepted values, ranges, and format;
- whether the setting is required or optional;
- where the setting is read and how it is applied;
- precedence when multiple configuration sources exist;
- interactions or dependencies with other settings;
- validation rules and behavior for invalid values;
- a working example;
- whether a restart, reload, regeneration, or migration is required.

For structured configuration systems such as TOML, YAML, JSON, INI, or project-specific manifests, include a complete annotated example and explain every section and field. Do not document only the obvious settings while leaving nested or less common sections unexplained.

When configuration behavior is non-obvious, document the exact syntax and operational sequence. For example, a synchronization section must explain its supported targets, source and destination semantics, mapping rules, direction, conflict behavior, validation, and how a user can verify that synchronization occurred, but only to the extent those behaviors are confirmed by the implementation.

## 9. CLI and command help requirements

Every CLI MUST expose a discoverable general help interface, conventionally through `--help` and, where appropriate, `-h` or a `help` command.

Every command MUST communicate its purpose, syntax, arguments, options, defaults, accepted values, and relevant examples. Nested command systems MUST provide help for applicable subcommands, including a way to discover available subcommands without executing them.

Help output MUST:

- be accurate and generated from, or validated against, the actual command parser and implementation;
- include common usage examples;
- identify required and optional arguments;
- explain defaults and environment/configuration interactions;
- avoid exposing secrets or private implementation details;
- return useful output without performing the requested operation;
- use clear, user-facing language and actionable error messages.

If a command genuinely has no meaningful subcommands or no applicable secondary help surface, document why. Do not omit help merely for implementation convenience.

GUI applications and APIs MUST provide equivalent discoverability through their user manual, built-in help/about surfaces, API reference, or other appropriate interface documentation.

## 10. Documentation validation and release inclusion

Documentation must be checked as part of release validation.

For each supported package, verify that the applicable manuals, man pages, configuration references, examples, licenses, and notices are present in the installed payload and accessible at documented locations.

Man pages MUST use the correct section and platform installation conventions. Their source files MUST remain maintained alongside the implementation. Package build scripts MUST include them in the resulting artifact.

When a command, option, configuration key, API, UI action, installer, package format, or lifecycle behavior changes, update every affected user-facing reference in the same change set.

Do not leave examples, help output, or manuals describing removed or nonexistent behavior.

## 11. Contribution requirements for packaging changes

Any contribution that changes packaging, build metadata, release payloads, installers, installation paths, runtime dependencies, or uninstall behavior MUST:

1. inspect the canonical release payload specification;
2. inspect all supported package formats and their build/install scripts;
3. explain the intended behavior and any platform exceptions;
4. update all affected metadata and package definitions;
5. update user and maintainer documentation;
6. update or add payload parity and lifecycle tests where practical;
7. validate each affected package backend;
8. report which package formats were actually built and which were actually installed and tested.

A pull request MUST NOT be marked complete based solely on one successful package build when other supported formats may be affected.

## 12. AI agent enforcement

AI agents MUST treat this contract as a release requirement.

Before changing packaging, they MUST perform a read-only audit of all relevant package formats, metadata, build scripts, installer/uninstaller scripts, documentation payloads, and tests.

Agents MUST preserve existing files and behavior outside the explicit task scope. They MUST NOT delete, rewrite, reorganize, rename, or replace unrelated files or sections.

When a requested change cannot be applied consistently across supported formats, agents MUST identify the exact mismatch and either complete the consistent change or report the specific blocker. They MUST NOT silently update only the easiest backend.

Agents MUST NOT invent supported package formats, installation behavior, configuration semantics, commands, manual content, or validation results.

## Project-specific documentation standards

Before changing project behavior, packaging, interfaces, configuration, or release documentation, read [docs/PROJECT_STANDARDS.md](docs/PROJECT_STANDARDS.md) and keep it aligned with the actual implementation. These standards supplement this file and do not authorize unrelated changes.
