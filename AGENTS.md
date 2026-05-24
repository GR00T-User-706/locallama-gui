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
