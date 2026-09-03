# Restore Archived Task Contract

## Ownership

`guru-restore-archived-task` is the recovery owner for one already-created task
whose archive, branch, worktree, remote branch and open PR must be reused. The
semantic caller decides whether a finding is in the current task scope. The
runtime never infers that decision from file names, issue text, or a diff.

## Public input

The `restore_archived_task` profile is authored from the Merge
`phase2_reentry_required` seed and contains stable caller-owned identity:
`repo_ref`, PR and Issue numbers/URL, expected immutable PR head and branch
names, task id, archive/active task locators, archive commit, exact finding
references, and `resume_target=phase-2`. It contains no local worktree path,
authorization, merge permission, private checkpoint, or full remote payload.

The semantic result separately binds the same profile, mode, and finding refs
to `classification=task_work` and `requires_task_content_change=true`.

## Fresh validation

Before any write, the runtime validates:

- PR is open and exactly matches repository, number, URL, base, head, and head SHA;
- Issue is open and its close intent is unchanged;
- local and remote branch identity matches the expected branch and head;
- the archived task, `task.json`, `finish-summary.json`, and archive commit
  match the public identity;
- the runtime mapping is unique and points to the archived identity;
- the mapped path is the exact top level of a real Git worktree, is on the
  expected branch and HEAD, is clean, contains the archive commit in current
  HEAD ancestry, and is not occupied by another active task;
- no different active task owns the same task identity;
- no provider, permission, ruleset, external-service, scope, identity, or
  merge blocker is present.

The AI owner builds the facts file only after rereading the live authorities.
It is a package-local invocation boundary, not public output or durable gate
state. The runtime validates the closed snapshot and independently rereads the
local task artifacts and Git worktree before mutation.

## Recovery transaction

The first valid invocation moves the archive directory to the canonical active
locator, changes `task.json.status` to `in_progress`, removes `completedAt`,
writes the existing owner-private mapping as active, writes the active task
pointer, removes the archived `finish-summary.json`, and retires stale
check/review/publication/finalization authority from both legacy task-local
paths and current owner-private checkpoint paths. No new object is created.

If the archive is already absent and the exact active task is present, the
runtime accepts a complete restored state without writing. If a normal
interruption left the exact active task in a pending state, the same invocation
finishes the status/mapping/authority repair. Active plus archive, mismatched
mapping, a different active task, or any other ambiguous state is blocked before
mutation.

## Typed exits

`restored_to_phase2` returns only `exit_id`, `task_ref`, and `resume_target`;
the downstream workflow rereads all PR, archive, and finding identity. `restore_blocked`
returns only a stable reason, remediation, and the zero-write claim. Downstream
full Phase 2 checks, task commit, branch review, publication, finalization, and
merge are outside this package.
