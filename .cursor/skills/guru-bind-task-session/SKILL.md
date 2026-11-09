---
name: guru-bind-task-session
description: Bind one current session to a TaskLifecycleDTO, rebind after loss, switch, reactivate, and resume with lifecycle freshness.
---

# Guru Bind Task Session

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

`judgment_mode=semantic`. Read the explicit TaskId and generation (including
generation 0), current session, and the official Fixed Fork TaskId resolver.
Review the requested profile and target lifecycle before invoking the recorder.
The shared C4 branch/ownership readers and C3 checkout validator must agree on
one live execution checkout for every selected lifecycle. Ordinary dirty work
does not disqualify a session resume; identity or artifact conflicts do.
Select that current checkout before calling the Fixed Fork TaskId resolver:
an old branch may legitimately retain the same task artifact after rebind,
but it is not another current checkout. Scope official resolution to the
selected registered checkout and compare its TaskRef/artifact to the C3 result.
Only the current session pointer is mutable here; branch association, checkout,
resource ownership, task artifact locator, and lifecycle transitions have
separate owners. A missing context key yields `explicit_task_mode` with the
TaskLifecycleDTO and no session write.

- `delivery_resume_current_task` requires the existing session pointer to resolve to
  the exact current lifecycle; it performs no write.
- `delivery_rebind_missing_session` restores a missing pointer for the selected lifecycle.
- `delivery_switch_task` validates both the bound source and the selected target before
  replacing only this session's pointer. A -> B -> A is supported.
- `delivery_reactivate_rebind` accepts a pointer for the same TaskId at an older
  generation or a missing pointer in a new session; the target generation must
  fresh-resolve.
- `delivery_manual_recovery` repairs only a missing/stale public schema-3 pointer for the
  explicitly selected task, never task/workspace mappings.

Bind/resume validates the installed public Task schema-2 record. Task binding
never clears an existing same-Task Delivery selection. A new binding has no
selected Delivery; only `guru-create-delivery` or the explicit Delivery selection
owner selects execution. Old profiles and schema-2 session records require
upstream migration and are rejected by this candidate.

All five success exits carry `TaskLifecycleDTO + resume_target` to their retained
workflow routers. `explicit_task_mode` carries TaskLifecycleDTO to
`guru-current-phase-router`; `binding_blocked` carries ReasonDTO to
`task-session-binding-blocked`. Each consumer derives TaskRef afresh if needed.
Unknown, stale, ambiguous or mismatched official identity stops without writing.

After same-identity carrier recovery, follow the original Branch
[recovery contract](../guru-establish-task-branch-binding/references/task-carrier-recovery.md)
only at this owner's receiving-session boundary. Require the actual Identity
and Ensure results for the restored original lifecycle. Inspect this receiving
chat's own official pointer; do not borrow the source chat's environment,
pointer or hidden runtime. Reuse a matching pointer with resume, restore a
missing pointer with rebind, and retain the original switch/manual-recovery
preconditions for a different or stale pointer. A truly absent context key
keeps `explicit_task_mode` and writes no session.

After the actual success exit, read native `task.py current --json`,
`delivery.py current --json` and `get_context.py --mode continuation` from the
resolved checkout. Consume the real current phase and remaining obligations.
`no_current_delivery` is not a request to allocate an empty Delivery. Retain
the original TaskId/generation/Delivery and missing historical Publication,
Delivery, full_review and readiness; restored binding does not supply a gate,
business delivery or Task Completion result.

Read [JSON inputs and complete invocations](references/json-inputs.md) before
choosing the two input carriers. Both parameters accept inline JSON, a regular
UTF-8 JSON file, or `-` for stdin. Only one parameter may use `-`; the runtime
rejects two stdin selections before either read. Process substitution and other
nonregular file carriers are unsupported. Carrier selection does not replace
the semantic review or identity checks above.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
