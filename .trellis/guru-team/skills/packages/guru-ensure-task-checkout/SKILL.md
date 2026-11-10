---
name: guru-ensure-task-checkout
description: Resolve the current task's unique registered checkout from its TaskId, generation, branch binding, ownership, and live Git facts.
---

# Ensure Task Checkout

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Use this deterministic owner for an active task. Read the immutable TaskId and
generation from the caller, then resolve its current task artifact, branch
binding, resource ownership, and registered Git checkout. A machine path is
returned only to the immediate workflow consumer; it is never persisted as
task or session identity. Missing binding or ownership routes to the establishment owner.
Missing or multiple registered checkouts route to checkout acquisition. An
identity or ownership contradiction fails closed. No task or Git mutation is
performed here.

For same-identity carrier recovery, read this owner's boundary in the original
Branch [recovery contract](../guru-establish-task-branch-binding/references/task-carrier-recovery.md).
First obtain the actual restored workspace Identity result. A normal missing
C4 binding or C5 ownership returns to Branch; where unbound HEAD lacks the
restored Task, that owner alone reviews and invokes `delivery_restored_checkout`.
This Ensure owner does not relax candidate checks, restore files, set a base,
create controls or require a commit. Reuse an already valid binding directly.
After establishment, invoke this public entry again and require one current
registered checkout with matching TaskId/generation, branch and ownership.
An association contradiction or ambiguous checkout retains its original stop.
Only `checkout_resolved` supplies the execution path to the receiving Bind
consumer; it is not a session binding, Delivery selection or stage result.

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
