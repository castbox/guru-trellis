---
name: guru-create-task
description: Create an independently reviewed Trellis task in the exact acquired checkout, or recover its result without repeating mutation.
---

# Create Task

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

`judgment_mode=semantic`. Consume only `guru-review-change-request:ready`
with `target.kind=existing_issue | standalone_request`, after the current
Intake and Sync decision. Never create or select a GitHub Issue here. For an
existing Issue, reread its live identity and accepted scope; for a standalone
request preserve `source.kind=no_issue` without invented closure semantics.
Issue creation input accepts `exact_source | reference_only` and preserves the
reviewed disposition through official creation and result recovery.
`reference_only` does not grant source-Issue closure; `follow_up | parent` remain
unsupported creation inputs.

Review the exact TaskId, date-prefixed TaskRef, title, ordinary scope, selected
base and delivery target. Choose one checkout acquisition route:
`adopt_invocation_checkout` for the unique clean registered linked invocation
checkout on a non-base, non-delivery branch at the reviewed decision HEAD,
or `provision_linked_worktree` with
an explicit `new_branch | existing_branch | existing_checkout` disposition.
New Task creation never adopts the primary checkout, including when it already
has a non-base branch. Read live topology, HEAD/ref, dirty/untracked contents
and the current conversation binding before choosing the location. Preserve
existing content and other worktrees; never switch or detach the primary HEAD
to prepare this Task. With no suitable linked location, review the exact path,
branch, source ref/HEAD and creation side effects before acquiring it.
`record-task-plan` and `create-task` reject primary adoption before mutation.
This create-only precondition does not govern read-only recovery of an already
created primary Task; old-Task migration, base Sync and Cleanup retain their
existing owners and clean-checkout requirements.

Review the actual branch and absolute call-local checkout path, plus the five
cleanup ownership projections. Show the exact task and Git side effects in
the current dialogue before invoking the executor.
The reviewed TaskRef must use the current Asia/Shanghai task date. If the date
changes before or during official creation, return `refresh_review` and review
a new TaskRef; do not create a task under a different date. Read-only result
recovery retains the original TaskRef across dates.

Use the `delivery_task_creation` profile. Public input schema `guru-create-task-input-delivery-1.0` removes the retired task
`creator` and `assignee` fields. Rereview an old request and omit those fields;
the closed Delivery schema rejects them before acquisition. The reviewed delivery
target remains call-local and is never added to official `task.json`. The
official creator receives the slug body without its date prefix.

Use `record-task-plan` for objective preconditions, `create-task` for the
official Fixed Fork `task.py create --schema-version 2.0 --no-start` followed by TaskId/source
materialization and C4/C5 control-state establishment, then
`check-task-creation-result`. Task retains overall scope and completion responsibility without a development
status. `created` enters the current workflow and `guru-create-delivery` before
any D1 Planning. A context key binds through the public schema-3 Task session
with no selected Delivery; without one continue in explicit-task mode. Session failure after
creation does not erase a durable task. If output was lost, use only
`recover-created-task-result`; it rereads the task, branch binding and
resource ownership without creating a second task or checkout. It reads the
current session route first: the same task remains unchanged, a missing record
may retry the official attach, and a different or invalid current route blocks
without overwriting it. Return to `guru-bind-task-session` for an explicit
task switch or rebind. Recovery returns `created` only after the same binding,
a completed missing-record attach, or explicit-task mode is current.

Return exactly one exit: `created -> guru-task-created`, `refresh_review ->
guru-sync-base` for changed base authority or a stale creation date, `blocked ->
task-creation-blocked`, or `invalid_task_state -> invalid-task-state`.
An unchanged base with invocation branch HEAD mismatch is blocked; a changed
acquisition route requires a new semantic review. Never use task/workspace
mappings, `task.json.branch` or checkout paths as durable identity.

Metadata and occupied-identity failures may carry one optional `diagnostic`
with `field_path` and `remediation`. The declared stop consumer uses these
call-local facts to explain the exact failing record and its disposition; they
are not task identity or a persisted inventory. Preserve the reason code and
stop. For unsupported old/mixed records, use `guru-upgrade-installation` for
reviewed per-record migration or manual disposition; never silently skip,
convert, or delete the record. Old minimal blocked/invalid outputs remain valid.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
