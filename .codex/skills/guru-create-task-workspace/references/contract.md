# Guru Create Task Workspace Contract

All GitHub facts and confirmed mutations use the shared authenticated,
repo-bound `gh` adapter in `.trellis/spec/workflow/workflow-contract.md`.

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

1. Validate the complete installed runtime, current reviewed DTOs from
   `guru-sync-base`, `guru-clarify-requirements`,
   `guru-review-contract-wording`, and `guru-review-change-request`, plus the
   live issue/task authority. Discovery private evidence is not an input.
2. Project the final target, duplicate and disposition decisions, authority
   impact, and readiness close/related/follow-up conclusion without changing
   them.
3. Read current Git, GitHub, package-local workspace configuration, branch,
   worktree and task facts without mutation. `workspace_mode` must be exactly
   `worktree` or `current`; missing or unsupported modes fail closed.
4. Author semantic branch/workspace/task names and classify each object as
   `create_new`, `reuse_exact`, or `conflict_blocked`.
5. Resolve one non-empty assignee in this order: explicit input; the issue's
   single assignee; current authenticated
   `gh auth status --active --hostname github.com --json hosts` identity after
   target-repository access preflight when the issue has none; one
   user question when the issue has multiple assignees or the actor is
   unresolved.
6. Display the exact repository, target, GitHub operation, base, branch,
   worktree, task, assignee, task-local issue ledger, ignored runtime writes,
   command argv, and invocation stop condition.
7. Complete the AI Review Gate below.
8. Obtain exactly the confirmation required for this invocation without
   writing the authorization or authorization process anywhere. Refusal stops
   here before any owner recorder/executor call and produces no result or DTO.
9. After confirmation, run `record-task-workspace-plan --invocation -`,
   `create-task-workspace --invocation -`, and
   `check-task-workspace-result --invocation -` in order. Their closed stdin
   envelopes carry the current `readiness_current` transition, owner plan, and,
   when applicable, the checked executor result. Runtime deterministically
   reconstructs the minimal checker projections from the transition; complete
   predecessor owner payloads stay private to their owning Skills. No
   prerequisite payload or locator crosses the Skill boundary, and the calls
   create no repository evidence files.
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

`github_issue_mutation` applies only to an exact reviewed draft.
Creation is followed by an immediate live reread and a `refresh_review` exit;
the invocation stops without creating a branch, worktree, task, or runtime
mapping.

`workspace_and_task_mutation` applies only to a checker-passed final open
issue. A confirmation from the draft invocation is not reusable after Intake
refresh.

Changing target or disposition returns `refresh_review` with zero side effects.
The plan preserves the AI-authored non-mutation route: `reroute` returns
`refresh_review` and `blocked` returns `blocked`. Only a passed Gate followed
by the user's current confirmation may cross into the recorder/executor. The
confirmation itself is ephemeral and is never a plan/result/schema/DTO field.

## Exact execution and recovery

The executor revalidates runtime, plan digest, base, final target, prerequisite
bytes and live object facts at every mutation boundary. The plan
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
result and binding facts digests and matches the current issue and reviewed
draft id/digest. The fresh Readiness target is the canonical live existing
issue identity and content reread after creation rather than the pre-create
draft. Workspace never reopens Discovery private evidence.
Ordinary existing issues use null result/binding provenance; partial or mixed
provenance fails closed.

The package-local resolver is the single configuration/path authority for
planner diagnostics, executor, checker and recovery. In `worktree` mode an
empty `worktree_root` resolves to
`<repository-parent>/<repository-name>-worktrees`; an absolute value is used as
the normalized root, and a relative value is normalized from repository root.
In `current` mode `worktree_root` must be empty, the current repository checkout
is the workspace, and runtime never invokes `git worktree add`. Paths that put
the worktree root inside the repository, non-scalar paths, and mode/root
conflicts fail before branch, worktree, task, artifact or mapping writes.

An open-issue transaction creates or exactly reuses the reviewed branch and
workspace and reruns the guards in the resolved workspace. In an isolated
subprocess, its adapter invokes official `common.task_store.cmd_create` with the
reviewed assignee and replaces the module's developer accessor with a null
result only for that handler invocation. Official fallback therefore writes
`task.json.creator=task.json.assignee=<reviewed-login>` without consuming
developer identity. The executor then sets branch, base and issue scope.
It writes exactly one tracked task-local Intake artifact:

- `issue-scope-ledger.json`

All other prerequisite evidence stays call-local and owner-private. Normal
record/execution/check transport validates `call-local:<stage>` plan tokens
against the exact in-memory payloads; it does not create or reread prerequisite
files. Compatibility-only locator calls remain available until the next
breaking Interface migration and are excluded from workflow, production eval,
and installed transcript paths. Local path mappings are
written only under ignored `.trellis/.runtime/guru-team/workspaces/` and
`.trellis/.runtime/guru-team/tasks/`. Guru runtime never reads, copies,
initializes, restores, or requires `.trellis/.developer` or
`.trellis/workspace/**`; existing official identity bytes remain exact.

Public plan/result stdout, tracked task artifacts, examples and public DTOs
contain no machine-local absolute path. The checker uses the same package-local
resolver as the executor and verifies the resolved workspace against live Git,
task and mapping facts. The exact normalized `workspace_path` remains only in
ignored runtime mappings.

Ordinary re-entry may reuse only an identity-exact branch/worktree/task and
byte-identical artifacts. Any repo, base, issue, branch, task locator, status or
artifact mismatch returns `blocked` without overwrite. No transaction log,
lock, concurrency protocol, cross-OS mechanism, or hostile-input boundary is
part of this contract.

If the task, branch/worktree, ledger, or Guru runtime mappings cannot be closed
into one identity, the state is invalid. The package makes no repair,
migration, restore, cleanup, or Intake decision and returns
`invalid_task_state` to the single `invalid-task-state` stop consumer.

## Typed exits

- `created` enters `guru-task-workspace-created` and then Phase 1.
- `refresh_review` re-enters `guru-sync-base` and the complete Intake chain.
- `blocked` stops at `task-workspace-blocked`.
- `invalid_task_state` stops at `invalid-task-state`; it cannot be projected to
  Intake or restore.

Unknown, multiple, unmapped, or consumer-mismatched exits fail closed.
`prepare-task` is query-only and exposes no mutation path; direct callers must
enter this Skill.

## Interface 1.4 Public Handoff

The single `execute_reviewed_plan` public profile carries only `profile` and
`mode`; target, naming, and recovery remain owner-private, while authorization
exists only in the current dialogue. Any input outside that current profile is
rejected by the declared schema. After the owner mutation/check loop,
`scripts/invoke.sh --invocation -` reruns the existing result checker from the
closed call-local envelope and serializes one minimal result derived from its
checked executor outcome. Normal plan, result, and prerequisite transport is
in-memory; only compatibility locators and genuine interrupted same-owner
recovery may use ignored owner-private artifacts.
