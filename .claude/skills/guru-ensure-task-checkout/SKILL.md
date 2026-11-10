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

Use this deterministic owner for an explicit active task or the caller's own
current context. Resolve its current task artifact, branch
binding, resource ownership, and registered Git checkout. A machine path is
returned only to the immediate workflow consumer; it is never persisted as
task or session identity. Missing binding or ownership routes to the establishment owner.
Missing or multiple registered checkouts route to checkout acquisition. An
identity or ownership contradiction fails closed. No task or Git mutation is
performed here.

Invoke `scripts/invoke.sh --root . --input -` with the structured input on
stdin. Return exactly one declared typed exit. Reinvoke after an acquisition
or establishment route; never infer a branch from a task name or checkout path.

Use `delivery_active_task` for an explicitly supplied TaskId/generation. Its
input, outputs and consumers remain compatible. Use `delivery_current_task`
with only `profile` and `mode` to query this caller's current context. Resolve
context availability with the installed public context resolver, then read
`task.py current --json` and apply the same C4/C5 and unique-checkout checks.
Never borrow another session, edit context environment variables, select from
inventory, or infer identity from a directory.

`current_context_ready` returns TaskId/generation/TaskRef/checkout_path. When a
Delivery is selected, `current_delivery` contains only delivery_key, phase and
planning_root from public current. The workflow router uses these fields to
locate the original lifecycle owner and its planning files; phase does not
prove a semantic pass. Read that owner's complete applicable contract and
necessary dependencies before invoking it. No Delivery omits current_delivery.
Results, candidate paths and history never cross this query boundary.

`no_current_task` means an actual context has no Task binding.
`context_unavailable` with reason_code=context_key_unavailable means the carrier
has no context key. Both enter the original current-checkout router to report
the fact and stop; neither starts Intake or repairs binding/selection.
Binding/checkout/identity failures retain the original exits and recovery
owners. Public current errors retain their available code, field_path and
remediation as nonzero invocation errors. Terminal selections return to their
original lifecycle owner. Requery after original-owner recovery.

The query changes no Task, Delivery, session, Git or business state. The managed
launcher can refresh its ignored Python selection cache; this infrastructure
write is separate from the query. `--help` lists both profile schema/example
locators through the original public command help.

Validate the public Task schema-2 identity and
its C4/C5 resource association without reading any Task development status.
The branch-binding input no longer carries `expected_status`; Delivery phase
belongs exclusively to the upstream model. Old profiles are rejected rather
than reinterpreted as Delivery calls.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
