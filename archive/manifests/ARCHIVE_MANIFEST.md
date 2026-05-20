# ARCHIVE_MANIFEST

## Purpose
Track archived or archive-candidate subsystems and document reactivation prerequisites.

## Archive candidates
- `ollama_GUI/` — legacy/parallel GUI tree.
- `ollama_GUI/addons/ollama_tools/` — tool execution framework and tests.
- Any duplicate GUI/backend implementations outside the primary maintained runtime path.

## Reactivation requirements
1. Assign explicit code ownership.
2. Run full security review (plugin execution, subprocess, filesystem writes).
3. Confirm dependency freshness and CI compatibility.
4. Add/refresh integration tests proving parity with the primary app behavior.
