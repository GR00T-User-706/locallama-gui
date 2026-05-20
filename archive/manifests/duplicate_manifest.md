# duplicate_manifest

## Suspected duplicate/overlapping implementations
- `locallama_gui/` vs `llm_studio/` vs `ollama_GUI/` (UI/backends/tooling overlap likely).
- Plugin and model-management patterns appear in multiple trees with differing maturity.

## Human decisions required
1. Define canonical production path.
2. Mark non-canonical trees as archived/deprecated/read-only.
3. Create migration notes for any retained features in non-canonical trees.
4. Add guardrails to prevent new feature drift across duplicate trees.
