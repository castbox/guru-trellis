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
   recorder envelope carries `readiness_current` plus the authoring described
   below, or a compatible complete plan. Executor/checker envelopes carry that
   returned plan and, for check, the executor result. The recorder prepares
   consumer-local projections; complete predecessor payloads stay private. No
   prerequisite payload or locator crosses the Skill boundary, and the calls
   create no repository evidence files.
10. Return exactly one declared typed exit.

## Recorder Input Preparation

The additive `record-task-workspace-plan --invocation -` input is:

```json
{
  "schema_version": "1.0",
  "transition": "the actual ready output's transition object, not this string",
  "authoring": {
    "scope": {"primary": {}, "close": [], "related": [], "followup": []},
    "naming": {},
    "assignee": {},
    "side_effects": {},
    "ai_review_gate": {}
  }
}
```

This diagram is not executable input. Use
`schemas/record-authoring-input.schema.json` and the complete authoring example
`examples/workspace-authoring.json`, combined with the actual checked public
Readiness `ready.transition`. A recorder's `typed_exit=ready` is not that public
handoff. Never use example transition digests as live evidence.

- `scope` contains the existing plan's primary/close/related/followup issue rows
  (`number`, `url`, `title`, `reason`), without `scope_sha256`. The primary must
  match the transition target; each other issue set must match Readiness.
- `naming`, `assignee`, and `side_effects` retain their existing complete plan
  shapes. The caller supplies exact paths, object dispositions and operations;
  runtime does not generate names, choose an assignee, or decide side effects.
- `ai_review_gate` contains `status`, `reviewer`, `summary`, `evidence`, without
  `reviewed_plan_sha256`. The AI supplies the actual semantic conclusion, even
  when blocked/reroute; no runtime default or inferred pass exists.
- No timestamps or hashes are caller-authored. Authorization is dialogue-only,
  never a field. The AI reviews the transition and authoring and obtains any
  required current confirmation before invoking the recorder.

The new form supports only ordinary `existing_issue` targets without prior
created-issue provenance. A reviewed draft or an issue created by this owner
must use the existing complete-plan compatibility path, including its required
draft/provenance fields. The compact transition cannot establish that history;
the caller selects the applicable documented input, not a runtime inference.

Preparation validates the transition against the consumer schema distributed
beside the installed packages at
`consumers/workflow/stage0/transitions/readiness-current.schema.json`, then checks
the repeated same-source content/facts/linkage identities for consistency.
Clarity's content-identity disposition hash and the target disposition digest
are distinct producer fields and are preserved independently, not compared.
It projects target fields by name, so `target.content_sha256` is not copied into
the differently shaped plan target. Base and continuation come from transition.

For this additive form, prerequisite `payload_sha256` binds the consumer-local
compact projection: `clarity`, `wording`, or `readiness` exactly as provided by
the transition. The base projection is `{schema_version:"1.0", transition_id:
"base_current:" + base.post_sync_resolution_sha256[:24], stage:"base_current",
mode, repo_locator, base}`. These are not reconstructed predecessor payloads.
Facts/content/linkage fields copy their corresponding transition values; base
facts and `base.sync_facts_sha256` hash that base projection. Clarity linkage
retains the content-identity projection; wording content/linkage use scope/scan.
All derived hashes use canonical UTF-8 JSON with sorted keys, compact separators,
and unescaped Unicode. Scope excludes its own digest; reviewable fields are
exactly `common.reviewable`; final plan hashing excludes only
`freshness.plan_sha256`. The recorder supplies capture/generation time and both
reviewable bindings, then validates and returns the existing plan schema.
Hash construction records no approval and does not replace the AI gate.

Use the exact returned object for the remaining calls:

```text
record  {schema_version:"1.0", transition, authoring} -> plan
execute {schema_version:"1.0", transition, plan} -> result
check   {schema_version:"1.0", transition, plan, result} -> checked_result
invoke  {schema_version:"1.0", public_input:{profile:"execute_reviewed_plan",mode},
         transition, owner_plan:plan, owner_result:checked_result} -> typed exit
```

`authoring` is accepted only by record. Supplying both `plan` and `authoring`
is an error. Full-plan record envelopes and existing `--input`/`--plan-input`
locator calls remain compatible; no existing plan schema or digest meaning is
rewritten. Package-local diagnostics identify missing envelope objects and
missing/extra/incorrect fields before executor mutation. Readiness schema and
projection checks apply to the new form; the compatibility form retains its
existing checks. Neither preparation nor recording fetches, creates resources,
or persists evidence.

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
issue, builds a created-issue binding, and stops. GitHub read/list operations
declare JSON output and accept only a JSON object or array. `gh issue create`
has a separate output contract: exactly one canonical plain-text
`https://github.com/<owner>/<repo>/issues/<positive-number>` line for the
reviewed repository, with at most its terminal line ending. The adapter never
tries to decode that mutation response as JSON and preserves the reviewed title
and body bytes without trimming, newline injection, or content rewriting.

Before create, runtime executes the exact repo-bound lookup:

```text
gh issue list --state open --search created:>=YYYY-MM-DD --limit 1000 \
  --json number,url,state,title,body,createdAt,updatedAt,labels
```

The date is the reviewed capture instant's UTC calendar date. Every returned
row must carry complete typed fields, a canonical URL for the reviewed
repository, valid UTC timestamps, and a valid label-name set. A response with
1000 rows cannot prove query exhaustion and blocks before create. For fewer
rows, runtime exact-filters `state=open`, title/body bytes, label-name set, and
`createdAt >= captured_at`. Zero matches creates once, one match is recovered,
and multiple matches block before create. Create and recovery both enter the
same immediate live reread/binding helper and emit the same `created_issue`
result. A retry after remote create but before successful response, reread, or
result delivery therefore recovers the unique live Issue and performs no
second create.

GitHub resolves label names case-insensitively and returns repository-canonical
casing. Runtime therefore preserves every reviewed label string unchanged for
the draft digest and `gh issue create`, but compares the plan and live label
sets through one case-folded, deduplicated identity in lookup, immediate
binding, and checker reread. A genuinely different label set still fails
closed.

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
subprocess, its adapter invokes the official task store with explicit
`--creator <reviewed-login>` and `--assignee <reviewed-login>`. The official
store therefore writes task ownership without a developer accessor. The
executor then sets branch, worktree, base and issue scope.
It writes exactly one tracked task-local Intake artifact:

- `issue-scope-ledger.json`

All other prerequisite evidence stays call-local and owner-private. The new
recorder input validates the readiness consumer schema and prepares
`call-local:<stage>` tokens from compact projections. Execution/check validate
the complete plan schema, reviewable/final digest and decision HEAD; they do not
reconstruct predecessor payloads or independently revalidate the transition.
Execution additionally checks live base/target at its mutation boundary, and
check validates the result binding and the applicable live created objects.
These calls do not create or reread prerequisite files.
Compatibility-only locator calls remain available until the next
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
`scripts/invoke.sh --invocation -` validates the result schema and embedded
checker status and serializes the result's typed exit. It does not rerun the
checker, validate the entire envelope, or revalidate transition/plan identity;
the preceding explicit checker call remains required. Its current refresh route
uses a top-level `base_branch` when supplied and otherwise `main`; this change
does not alter that pre-existing behavior. Normal plan/result transport is
in-memory; only compatibility locators and genuine interrupted same-owner
recovery may use ignored owner-private artifacts.
