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

Use `record-task-plan` for objective preconditions, `create-task` for the
official Fixed Fork `task.py create --no-start` followed by TaskId/source
materialization and C4/C5 control-state establishment, then
`check-task-creation-result`. The task remains `planning` until
`guru-activate-task`. A context key binds via the official schema-2 session
port; without one continue in explicit-task mode. Session failure after
creation does not erase a durable task. If output was lost, use only
`recover-created-task-result`; it rereads the task, branch binding and
resource ownership without creating a second task or checkout, then retries
the official session binding. Recovery returns `created` only after that bind
is complete or explicit-task mode is current.

Return exactly one exit: `created -> guru-task-created`, `refresh_review ->
guru-sync-base` for changed base authority or a stale creation date, `blocked ->
task-creation-blocked`, or `invalid_task_state -> invalid-task-state`.
An unchanged base with invocation branch HEAD mismatch is blocked; a changed
acquisition route requires a new semantic review. Never use task/workspace
mappings, `task.json.branch` or checkout paths as durable identity.
