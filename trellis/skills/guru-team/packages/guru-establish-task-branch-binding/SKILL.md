---
name: guru-establish-task-branch-binding
description: Establish or recover one current task branch binding from live validated candidates and ownership state.
---

# Establish Task Branch Binding

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

Load for an active task with missing branch binding or ownership. Review the
TaskId, generation, current task artifact and live candidate set. A unique
registered candidate is established automatically; zero or multiple valid
candidates return `selection_required` for a fresh explicit choice or checkout
acquisition. Existing resources recovered without ownership facts remain
caller-owned. Do not derive binding authority from legacy task metadata.

Use `scripts/invoke.sh --root <repository> --input -`. The `recover` action
only rereads the exact binding, ownership and candidate facts after lost output.
Return exactly one declared exit; do not retry a mutation from a lost result.

Use `delivery_active_task`. Validate the public Task schema-2 identity and
its C4/C5 resource association without reading any Task development status.
The branch-binding input no longer carries `expected_status`; Delivery phase
belongs exclusively to the upstream model. Old profiles are rejected rather
than reinterpreted as Delivery calls.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
