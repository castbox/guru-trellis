---
name: guru-establish-task-branch-binding
description: Establish or recover one current task branch binding from live validated candidates and ownership state.
---

# Establish Task Branch Binding

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
