# Guru Create Task Workspace Contract

## Ownership and modes

`guru-create-task-workspace` is the only Guru Team owner allowed to create a
reviewed GitHub issue, branch, worktree, Trellis task, or Intake task artifact.
Workflow and standalone mode validate the same entry preconditions. Standalone
changes caller routing only; it does not skip the complete Intake evidence,
freshness, AI Gate, confirmation, recorder, executor, or checker.

The global workflow owns only the mandatory invocation and typed-exit routing.
This contract owns the step-local semantic behavior. Companion scripts record,
execute, and check deterministic facts; they do not select a target, decide
scope, author names, choose an assignee, grant confirmation, or choose an exit.

## Forward behavior

1. Validate the complete installed runtime and current checker-passed results
   from `guru-sync-base`, `guru-discover-change-context`,
   `guru-clarify-requirements`, `guru-review-contract-wording`, and
   `guru-review-change-request`.
2. Project the final target, duplicate and disposition decisions, authority
   impact, and readiness close/related/follow-up conclusion without changing
   them.
3. Read current Git, GitHub, configured worktree-root, branch, worktree and task
   facts without mutation.
4. Author semantic branch/workspace/task names and classify each object as
   `create_new`, `reuse_exact`, or `conflict_blocked`.
5. Resolve one non-empty assignee in this order: explicit input; the issue's
   single assignee; current `gh api user` login when the issue has none; one
   user question when the issue has multiple assignees or the actor is
   unresolved.
6. Display the exact repository, target, GitHub operation, base, branch,
   worktree, task, assignee, four task-local artifacts, ignored runtime writes,
   command argv, and invocation stop condition.
7. Complete the AI Review Gate below.
8. Obtain exactly the confirmation required for this invocation.
9. Run `record-task-workspace-plan`, `create-task-workspace`, and
   `check-task-workspace-result` in order.
10. Return exactly one declared typed exit.

## AI Review Gate

The AI must verify that prerequisite bytes still own target and disposition;
no duplicate, closed-state, reopen, retarget, or follow-up decision was remade;
names contain issue identity and semantic action; assignee evidence follows the
fixed order; issue and workspace mutations are not mixed; the plan enumerates
every exact side effect; readiness scope projection is unchanged; artifacts,
runtime, no-developer and no-shared-write boundaries are complete; recovery
cannot overwrite a conflict; and the scenario remains inside normal supported
operation. Only a passed Gate can authorize mutation.

## Mutually exclusive confirmations

`github_issue_mutation` applies only to an exact reviewed draft. Its paired
`workspace_and_task_mutation` status must be `not_in_current_invocation`.
Creation is followed by an immediate live reread and a `refresh_review` exit;
the invocation stops without creating a branch, worktree, task, or runtime
mapping.

`workspace_and_task_mutation` applies only to a checker-passed final open
issue. Its paired `github_issue_mutation` status is
`not_in_current_invocation`. A confirmation from the draft invocation is not
reusable after Intake refresh.

Changing target or disposition returns `refresh_review` with zero side effects.
Explicit cancellation returns `cancelled` with zero side effects.

The plan preserves the AI-authored non-mutation route. A passed Gate plus a
digest-bound `refused` active confirmation returns `cancelled`; `reroute` plus
no active confirmation returns `refresh_review`; `blocked` plus no active
confirmation returns `blocked`. Only passed plus `confirmed` may mutate.

## Exact execution and recovery

The executor revalidates runtime, plan digest, base, final target, prerequisite
bytes, confirmation and live object facts at every mutation boundary. The plan
binds the initial checker-passed `post_sync_resolution_sha256`. Before the
first confirmed issue or workspace/task mutation, runtime calls the shared base
resolver/sync core once. A changed fresh post-sync identity returns
`refresh_review` before business mutation; an unchanged identity continues.

A draft transaction creates the exact reviewed title/body/labels, rereads the
issue, builds a created-issue binding, and stops. The GitHub adapter preserves
the reviewed title and body bytes; it does not trim them or append a newline.
Before create, it searches live open issues for exact title/body/labels with
`createdAt` not earlier than the reviewed plan capture. Zero matches creates
once, one match is recovered and reread, and multiple matches block. This
recovery emits the same `created_issue` result and prevents a second remote
create after an immediate reread failure.

After complete Intake re-entry, an existing issue produced by this path embeds
the complete prior checker-passed created-issue result. Runtime recomputes the
result and binding facts digests and matches the current issue, reviewed draft
id/digest, and creation confirmation digest. The fresh context is the canonical
live existing issue (`kind=issue`, canonical identity, open state, update time,
body and facts digests, null `issue_binding`) rather than the pre-create draft.
Ordinary existing issues use null result/binding provenance; partial or mixed
provenance fails closed.

An open-issue transaction creates or exactly reuses the reviewed branch and
worktree and reruns the guards in the target worktree. In an isolated
subprocess, its adapter invokes official `common.task_store.cmd_create` with the
reviewed assignee and replaces the module's developer accessor with a null
result only for that handler invocation. Official fallback therefore writes
`task.json.creator=task.json.assignee=<reviewed-login>` without consuming
developer identity. The executor then sets branch, base and issue scope.
It then writes exactly these tracked task-local Intake artifacts:

- `task-start-context.json`
- `issue-scope-ledger.json`
- `context-discovery.json`
- `issue-review.json`

The final two preserve checker-passed canonical bytes. Local path mappings are
written only under ignored `.trellis/.runtime/guru-team/workspaces/` and
`.trellis/.runtime/guru-team/tasks/`. Guru runtime never reads, copies,
initializes, restores, or requires `.trellis/.developer` or
`.trellis/workspace/**`; existing official identity bytes remain exact.

Public plan/result stdout and examples contain no machine-local absolute path.
The checker derives the expected worktree from current repo config, the
reviewed workspace slug, and live Git facts. Absolute mappings remain only in
ignored runtime files.

Ordinary re-entry may reuse only an identity-exact branch/worktree/task and
byte-identical artifacts. Any repo, base, issue, branch, task locator, status or
artifact mismatch returns `blocked` without overwrite. No transaction log,
lock, concurrency protocol, cross-OS mechanism, or hostile-input boundary is
part of this contract.

## Typed exits

- `created` enters `guru-task-workspace-created` and then Phase 1.
- `refresh_review` re-enters `guru-sync-base` and the complete Intake chain.
- `cancelled` stops at `task-workspace-cancelled`.
- `blocked` stops at `task-workspace-blocked`.

Unknown, multiple, unmapped, or consumer-mismatched exits fail closed.
`prepare-task` is query-only; its legacy mutation flags fail before writes and
direct callers must enter this Skill.
