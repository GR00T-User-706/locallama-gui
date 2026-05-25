# Menu Map (Baseline)

Date: 2026-05-25
Scope: Baseline documentation map for menu/action ownership and audit follow-up.

## Purpose

Provide a single place to track menu items, their intended behavior, and owning module/function.

## Menu Ownership Baseline

| Menu | Intended Scope | Primary Owner File | Status |
|---|---|---|---|
| File | session/file operations | `locallama_gui/ui/main_window.py` + controllers | LIKELY_DEFINED |
| Models | model lifecycle operations | `locallama_gui/ui/main_window.py` + `ui/controllers/model_controller.py` | LIKELY_DEFINED |
| Agents | agent profile flows | `locallama_gui/ui/main_window.py` + dialogs/managers | UNKNOWN_DETAILS |
| Plugins | plugin management flows | `locallama_gui/ui/main_window.py` + `ui/controllers/plugin_controller.py` | LIKELY_DEFINED |
| Settings | endpoints/parameters/theme/config | `locallama_gui/ui/main_window.py` + dialogs + `core/config.py` | LIKELY_DEFINED |
| View | panel visibility/layout | `locallama_gui/ui/main_window.py` | UNKNOWN_DETAILS |
| Developer | diagnostics/request/token/log tools | `locallama_gui/ui/main_window.py` | UNKNOWN_DETAILS |
| Help | app/help/about diagnostics | `locallama_gui/ui/main_window.py` | UNKNOWN_DETAILS |

## CONFIRMED
- Menu construction is centralized in `locallama_gui/ui/main_window.py`.

## LIKELY
- Some actions delegate to controller/dialog layers instead of inline logic.

## UNKNOWN
- Exact item-level duplication or ambiguous action naming between View and Developer menus.

## TODO
- Add per-item rows (Action label, handler, expected behavior, current status).
- Mark every action as CONFIRMED_WORKING / UNKNOWN / NEEDS_FIX once manually verified.
