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

To read an existing binding reference, use the original read-only
`discover-task-branch-binding-candidates` command with `action=establish`.
Only an `already_established` receipt provides `result.binding_ref`, containing
`task_id`, `lifecycle_generation`, and `binding_revision`. Closure copies that
reference unchanged into its `binding_ref` input. Other discovery statuses
return to this owner for establishment or selection. The formal
`binding_established` output remains a TaskKey and does not supply a revision.

Use `delivery_active_task` for normal candidate establishment and exact
read-only result recovery. Validate the public Task schema-2 identity and
its C4/C5 resource association without reading any Task development status.
The branch-binding input no longer carries `expected_status`; Delivery phase
belongs exclusively to the upstream model. Old profiles are rejected rather
than reinterpreted as Delivery calls.

For a missing Task carrier, or a restored workspace whose unbound HEAD does
not contain that Task, read the complete
[same-identity recovery contract](references/task-carrier-recovery.md).
Normal unbound candidates are checked in the HEAD Git tree; restoring an
untracked directory alone does not qualify one. Repeated discovery is not
carrier restoration, and recovery does not implicitly require a commit.

Use `delivery_restored_checkout` only after this owner has reviewed the fixed
carrier, same TaskId/generation, full Delivery plans and real historical gaps,
and the explicitly selected target branch/checkout and write set. Complete
the semantic Gate and the applicable dialogue boundary before invoke. Its
input contains only profile/mode, TaskId/TaskRef/generation, `branch_name` and
`expected_head`; `--root` is the current registered checkout. The executor
validates workspace schema-2 active identity, registration, branch/HEAD and
existing C4/C5 associations. It reuses matching controls and establishes only
missing controls through the original transaction; mismatches stop. New
ownership is caller-owned, with primary-worktree ownership `not_applicable`.
Existing ownership remains unchanged. Primary and linked checkouts are
supported; Creation's non-primary/non-base restrictions do not apply.

The restored-checkout profile preserves the existing typed exits and consumers.
`binding_established` enters the original Ensure owner, then the receiving
chat's own Bind and current continuation. It writes no Task/Delivery content,
Planning/Check/Review result, session pointer or recovery ledger. Historical
Publication/Delivery/full_review/readiness gaps remain gaps. On lost stdout,
use the existing discovery binding reference and read-only recover action;
do not infer failure and repeat the write. The normal discovery/recorder
commands still accept only `delivery_active_task` with `action=establish`.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
