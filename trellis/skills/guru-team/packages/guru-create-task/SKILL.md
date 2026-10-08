---
name: guru-create-task
description: Create an independently reviewed Trellis task in the exact acquired checkout, or recover its result without repeating mutation.
---

# Create Task

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
`adopt_invocation_checkout` for the unique clean branch-bound invocation
checkout at the reviewed decision HEAD, or `provision_linked_worktree` with
an explicit `new_branch | existing_branch | existing_checkout` disposition.
Review the actual branch and absolute call-local checkout path, plus the five
cleanup ownership projections. Show the exact task and Git side effects in
the current dialogue before invoking the executor.
The reviewed TaskRef must use the current Asia/Shanghai task date. If the date
changes before or during official creation, return `refresh_review` and review
a new TaskRef; do not create a task under a different date. Read-only result
recovery retains the original TaskRef across dates.

Public input schema `guru-create-task-input-2.0` removes the retired task
`creator` and `assignee` fields. Rereview a 1.0 request and omit those fields;
the closed 2.0 schema rejects them before acquisition. The reviewed delivery
target remains call-local and is never added to official `task.json`. The
official creator receives the slug body without its date prefix.

Use `record-task-plan` for objective preconditions, `create-task` for the
official Fixed Fork `task.py create --no-start` followed by TaskId/source
materialization and C4/C5 control-state establishment, then
`check-task-creation-result`. The task remains `planning` until
`guru-activate-task`. A context key binds via the official schema-2 session
port; without one continue in explicit-task mode. Session failure after
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
