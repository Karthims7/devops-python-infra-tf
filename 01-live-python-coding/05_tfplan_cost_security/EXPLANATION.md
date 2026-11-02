# Live Coding Topic: Terraform Plan Parser & Security Gate

## Why This Problem Is a Direct Match for the Woven by Toyota Role
The job description explicitly mentions:
- *"build Python automation and integrations"*
- *"improve infrastructure delivery through Terraform"*

Building custom pre-apply policy engines (similar to OPA / Conftest or tfsec) in Python proves you can bridge the gap between infrastructure state and software tooling.

## Key Technical Points to Articulate
1. **Understanding Terraform JSON Schema:**
   - Terraform plans serialized to JSON with `terraform show -json` have a standardized structure:
     - `resource_changes`: List of modified resources.
     - `change.actions`: List of actions (`["create"]`, `["update"]`, `["delete"]`, `["delete", "create"]` for replacement).
     - `change.before` / `change.after`: State before and proposed state after.
2. **Shift-Left Security & Guardrails:**
   - Preventing catastrophic production blunders (e.g., replacement or deletion of stateful RDS instances) before `terraform apply` runs in a CI pipeline.
3. **Extensibility & Clean Architecture:**
   - Using dataclasses (`PolicyViolation`, `AuditReport`) and separating rule checks into modular methods.

