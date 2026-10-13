---
name: guru-ensure-task-checkout
description: Resolve the current task's unique registered checkout from its TaskId, generation, branch binding, ownership, and live Git facts.
---

# Ensure Task Checkout

Use this deterministic owner for an active task. Read the immutable TaskId and
generation from the caller, then resolve its current task artifact, branch
binding, resource ownership, and registered Git checkout. A machine path is
returned only to the immediate workflow consumer; it is never persisted as
task or session identity. Missing binding or ownership routes to the establishment owner.
Missing or multiple registered checkouts route to checkout acquisition. An
identity or ownership contradiction fails closed. No task or Git mutation is
performed here.

Invoke `scripts/invoke.sh --root . --input -` with the structured input on
stdin. Return exactly one declared typed exit. Reinvoke after an acquisition
or establishment route; never infer a branch from a task name or checkout path.

Use `delivery_active_task`. Validate the public Task schema-2 identity and
its C4/C5 resource association without reading any Task development status.
The branch-binding input no longer carries `expected_status`; Delivery phase
belongs exclusively to the upstream model. Old profiles are rejected rather
than reinterpreted as Delivery calls.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
