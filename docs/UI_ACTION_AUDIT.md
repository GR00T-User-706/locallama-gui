# UI Action Audit (Baseline Template)

Date: 2026-05-25
Scope: Baseline structure for auditing visible UI actions; no UI code changes.

## Purpose

Track each visible UI control/action and classify whether it is fully functional, explicitly disabled, intentionally hidden, or unknown.

## Status Legend

- CONFIRMED_WORKING
- LIKELY_WORKING
- UNKNOWN
- NEEDS_FIX
- SHOULD_DISABLE

## Audit Matrix (Initial Baseline)

| Area | Action/Control | Current Status | Evidence Type | Notes | Next Check |
|---|---|---|---|---|---|
| Chat | Send / Stop / Retry / Regenerate | LIKELY_WORKING | code+changelog | Behavior appears actively maintained. | manual UI smoke |
| Models | Refresh Models | LIKELY_WORKING | toolbar wiring | Present in main toolbar actions. | backend-connected smoke |
| Models | Delete Model | UNKNOWN | mission concerns | Requires explicit destructive-flow validation. | targeted manual test |
| Models | Create Model dialog/action | UNKNOWN | mission concerns | Ambiguity risk noted in repo audit. | dialog copy/flow review |
| Parameters | Reasoning mode selector | LIKELY_WORKING | config+changelog | Exclusive mode logic appears present. | UI/serialization regression check |
| Developer | Request Viewer copy/clear | LIKELY_WORKING | code+changelog | Explicit button wiring exists. | manual interaction check |
| Developer | Token Viewer copy/clear | LIKELY_WORKING | code+changelog | Explicit button wiring exists. | manual interaction check |
| View/Developer Menus | duplication/ambiguity | UNKNOWN | mission concerns | Needs menu-by-menu map. | `docs/MENU_MAP.md` completion |
| Agent Builder | Create/manage workflows | UNKNOWN | large surface area | No current dedicated functional audit doc. | workflow checklist |

## CONFIRMED
- Baseline intentionally marks uncertain controls as UNKNOWN rather than assuming health.

## LIKELY
- Many core controls are wired, but actual reliability needs runtime validation.

## UNKNOWN
- Exact broken/duplicated actions by menu and dialog until full UI walk-through.

## TODO
- Expand this matrix to include every menu action and dock control.
- Attach reproducible steps and expected/actual outcomes for each NEEDS_FIX row.
