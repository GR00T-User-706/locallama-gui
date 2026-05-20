# MODULE_INTAKE_POLICY

## Goal
Standardize how new modules, plugins, and tool frameworks are accepted into this repository.

## Intake gates (required)
1. **Ownership**: Named maintainer and backup reviewer.
2. **Security**: Review for dynamic imports, plugin execution, subprocess use, filesystem write/delete behavior, and secrets handling.
3. **Functionality**: Minimal smoke tests plus one integration test on intended runtime path.
4. **Scope clarity**: Declare whether module is primary, experimental, or archive.
5. **Duplication check**: Confirm feature is not already implemented in another code tree.

## Plugin/module-specific requirements
- Plugins must document trust assumptions and execution boundaries.
- Any dynamic loading must include explicit allowlist/enablement policy.
- Modules that execute commands or external tools must enforce strict argument validation and safe defaults.

## Archive handling
- Legacy modules must be placed under archive paths with manifest entries.
- Archived modules cannot be reactivated without passing all intake gates.
