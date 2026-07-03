# Contributing to TORTUGA

First, thank you for considering contributing to TORTUGA. Our goal is to provide safe, reversible, and understandable OS hardening for home users.

## Safety Principles
When proposing a new action, ensure you adhere to the **Safety Principles**:
1. **Reversibility**: Provide both an `apply()` and a guaranteed `rollback()`.
2. **Pre-flight Impact Analysis**: You must dynamically check if a targeted port/service/feature is in active use.
3. **Non-Destruction**: Never uninstall system components, disable networking entirely, or delete user data. Prefer `disable` over `uninstall`.

## Branch Protection and Review Process
The `main` branch is protected. All contributions must:
- Be submitted via a Pull Request.
- Pass the CI pipeline (Ruff, Bandit, ShellCheck, PSScriptAnalyzer, Pytest).
- Receive approval from at least one core maintainer.
- Adhere strictly to the action contract defined in `docs/CONFIG_MATRIX.md`.

## Adding a New Action
1. Open an Issue discussing the action and proposing its level/impact.
2. Update `docs/CONFIG_MATRIX.md`.
3. Create the action script in the respective module folder (`tortuga/modules/`).
4. Ensure the action complies with `tortuga.action.Action` interface.

## Supply Chain Hygiene
- Do not introduce arbitrary Python dependencies. The core engine aims for ≤5 dependencies.
- Any external data downloads must be fully validated.
