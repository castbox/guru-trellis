# Workflow Contract

## Canonical Sources

`trellis/workflows/guru-team/workflow.md` is the reusable marketplace workflow
contract. `.trellis/workflow.md` is the dogfood installation copy and must be
byte-identical after every canonical workflow change.

The workflow marketplace installs only `.trellis/workflow.md`. The complete
Guru Team extension, public Skill projections, package runtimes, minimal shared kernel, schemas, platform
discovery copies, and Guru-owned explicit entries are installed by the preset.

Guru task workspace terminology means the isolated task checkout/worktree and
its ignored Guru runtime mappings. It never refers to the retired
`.trellis/workspace/<developer>/journal-*` namespace. Current task resolution
uses task metadata, current checkout/branch, live Git worktree facts, and those
mappings; no normal workflow path initializes or reads developer identity,
workspace journal/index, session recording, or legacy agent traces.

## SSOT Boundary

The global workflow owns only:

- phase order and the current-task status router;
- one mandatory invocation marker per active stable `guru-*` Skill id;
- every declared typed exit and its single consumer;
- workflow targets, fail-closed stops, and automatic mapped re-entry;
- tool-free initial request classification;
- workspace/task boundary selection and task activation;
- Docs SSOT and Publication-owned external-work-item disposition points;
- human-readable artifact presentation;
- the user interaction and external side-effect boundaries.

Each active package under `trellis/skills/guru-team/packages/` owns its own
entry preconditions, `judgment_mode`, forward behavior, semantic review when
applicable, conditional confirmation, recorder/validator sequence, private
checkpoint, freshness, recovery, and public DTO. Workflow, README, prompts,
commands, launchers, breadcrumbs, hooks, and agents must not restate those
step-local contracts.

The active registry, package `interface.json`, independent per-exit output
schemas, consumer input contracts, and `public_contracts.projections[]` are the
only public I/O graph authority. Workflow prose must never infer a route from a
private checkpoint, digest, recorder result, example, or runtime implementation.

## GitHub Platform I/O

All Guru Team GitHub platform reads, semantic evidence reads, mutations, and
recovery verification use authenticated GitHub CLI only. Prefer a repo-bound
high-level command (`gh issue`, `gh pr`, or `gh run`); otherwise use `gh api`
with a complete `repos/<owner>/<repository>/...` endpoint. GitHub App, MCP,
connector, browser UI, implicit repository context, and cross-channel fallback
are forbidden.

Every high-level operation supplies `--repo owner/repository`. Mutations bind
the exact number and, where applicable, base, head and expected head SHA or an
equivalent precondition. Required response fields fail closed. Preflight and
runtime distinguish `github_cli_missing`, `github_auth_failed`,
`github_repo_access_denied`, `github_permission_denied`,
`github_api_unavailable`, and `github_response_incomplete`; recovery retries
the same repo-bound owner. These facts never decide scope, readiness, findings,
close semantics, or routes, which remain owned by the semantic Skill.

`git` remains the sole owner of local Git and Git transport (`fetch`, `push`,
`ls-remote`, revisions and worktrees). CLI credentials stay in the credential
store and never enter argv, logs, artifacts or DTOs. Authorization remains
dialogue-local and is never persisted.

## Integrated Public Graph

The current package registry contains exactly 32 active Skill ids, 142 external
exits, and 102 commands. Twenty-two mandatory Skill invocations participate in
the business-task workflow, whose global graph contains 98 mapped exits, 35
workflow targets, and 24 stop targets. Nine additional active packages remain
deferred capability owners, and `guru-verify-extension-installation` remains the
standalone-only source-repository Skill; none of those ten packages activates a
new business-workflow edge before the owning lifecycle change.

| Skill | Typed exit -> unique consumer |
| --- | --- |
| `guru-maintain-architecture-baseline` | `baseline_current -> guru-architecture-baseline-current-router`; `sync_required -> guru-maintain-architecture-baseline`; `baseline_incomplete -> guru-architecture-baseline-bootstrap-router`; `architecture_conflict -> guru-architecture-baseline-planning-router`; `contract_incomplete -> guru-architecture-baseline-planning-router`; `fitness_regression -> guru-architecture-baseline-check-router`; `blocked -> architecture-baseline-blocked` |
| `guru-qualify-normal-scenario` | `classified -> guru-normal-scenario-classified-router`; `scope_confirmation_required -> guru-clarify-requirements`; `mechanism_revision_required -> guru-normal-scenario-mechanism-router`; `blocked -> normal-scenario-qualification-blocked` |
| `guru-qualify-solution-mechanism` | `classified -> guru-solution-mechanism-classified-router`; `scope_confirmation_required -> guru-clarify-requirements`; `mechanism_revision_required -> guru-solution-mechanism-mechanism-router`; `blocked -> solution-mechanism-qualification-blocked` |
| `guru-execute-task-free-change` | `completed -> guru-task-free-completed`; `resume_active_task -> guru-task-free-resume-active-task-router`; `scope_change -> guru-task-free-scope-change-router`; `location_required -> guru-execute-task-free-change`; `reselect_mode -> guru-select-workflow-mode`; `explicit_choice_required -> guru-execute-task-free-change`; `blocked -> task-free-change-blocked` |
| `guru-sync-base` | `synced -> guru-discover-change-context`; `skipped -> original-request-route`; `blocked -> base-sync-blocked` |
| `guru-discover-change-context` | `context_ready -> guru-clarify-requirements`; `refresh_base -> guru-sync-base`; `blocked -> change-context-blocked` |
| `guru-clarify-requirements` | `clear -> guru-requirements-clear-router`; `needs_context -> guru-discover-change-context`; `refresh_context -> guru-sync-base`; `retarget_context -> guru-sync-base`; `new_task -> guru-full-task-intake-chain`; `blocked -> requirements-clarification-blocked` |
| `guru-review-contract-wording` | `pass -> guru-contract-wording-pass-router`; `content_changed -> guru-contract-wording-change-router`; `blocked -> contract-wording-blocked` |
| `guru-review-change-request` | `ready -> guru-create-task-workspace`; `clarify_requirements -> guru-clarify-requirements`; `review_wording -> guru-review-contract-wording`; `refresh_context -> guru-sync-base`; `blocked -> change-request-review-blocked` |
| `guru-create-task-workspace` | `created -> guru-task-workspace-created`; `refresh_review -> guru-sync-base`; `blocked -> task-workspace-blocked`; `invalid_task_state -> invalid-task-state` |
| `guru-approve-task-plan` | `approved -> phase-1-task-activation`; `revision_required -> guru-approve-task-plan`; `clarify_scope -> guru-task-plan-clarify-scope-router`; `blocked -> task-plan-approval-blocked` |
| `guru-check-task` | `passed -> guru-create-task-commit`; `implementation_required -> guru-resume-implementation`; `planning_stale -> guru-task-check-planning-router`; `blocked -> task-check-blocked` |
| `guru-create-task-commit` | `committed -> guru-review-branch`; `revision-required -> guru-create-task-commit`; `blocked -> task-commit-blocked` |
| `guru-review-branch` | `passed -> guru-review-task-publication`; `continuity_passed -> guru-base-continuity-passed-router`; `implementation_required -> guru-branch-review-implementation-router`; `scope_confirmation_required -> guru-branch-review-scope-router`; `blocked -> branch-review-blocked`; `archived_review_passed -> guru-review-task-publication` |
| `guru-review-task-publication` | `ready -> guru-finalize-task`; `return_to_task_work -> guru-task-publication-work-router`; `blocked -> task-publication-review-blocked`; `archived_ready -> guru-finalize-task` |
| `guru-verify-extension-installation` (standalone only) | `verified -> extension-installation-verification-verified`; `blocked -> extension-installation-verification-blocked` |
| `guru-finalize-task` | `publication_review_stale -> guru-review-task-publication`; `resume_finalization -> guru-finalize-task`; `reprepare_required -> guru-finalize-task`; `ready_for_merge -> guru-merge-task-pr`; `blocked -> task-finalization-blocked` |
| `guru-merge-task-pr` | `merged -> guru-finalization-finish-response`; `merge_blocked -> task-pr-merge-blocked`; `phase2_reentry_required -> guru-restore-archived-task`; `closure_mismatch -> task-pr-closure-mismatch`; `review_refresh_required -> guru-review-branch` |
| `guru-restore-archived-task` | `restored_to_phase2 -> guru-resume-implementation`; `restore_blocked -> task-pr-phase2-reentry-blocked` |

Missing Skill packages, missing or duplicate markers, unknown/multiple/unmapped
exits, a consumer mismatch, a dangling target, a kind mismatch, or an invalid
projection always fails closed. Frontmatter discovery is only a convenience and
never substitutes for a mandatory workflow invocation marker.

### Normal-scenario qualification invocation

`guru-qualify-normal-scenario` is the only semantic owner for candidate
qualification. The global workflow names the stable Skill id, the ten mandatory
profiles, their exact pre-judgment trigger points, the four exits above, and the
unique consumer of each exit. It does not restate scope-first reasoning,
security-candidate evidence, severity quarantine, decision criteria, or
mechanism revision semantics.

The ten profiles are `task_free_pre_write`, `task_free_evolution`,
`requirements_scope_set`, `change_request_candidate_set`,
`planning_scenario_set`, `implementation_discovery`,
`base_impact_candidate_set`, `phase2_candidate_set`,
`branch_review_candidate_set`, and `publication_candidate_set`. Their
classified and mechanism-revision returns go only to the original profile
owner. Scope confirmation goes only to
`guru-clarify-requirements:normal_scenario_scope_confirmation`; blocked stops at
`normal-scenario-qualification-blocked`. Unknown, empty, multiple, stale, or
mismatched profile/result routing fails closed.

For Phase 2, `guru-phase2-implementation-coordinator` invokes
`implementation_discovery` before any planning-external candidate can cause an
edit or test. Its existing deterministic resume target remains
`guru-resume-implementation`. Rejected candidates never enter clarification,
acceptance, negative tests, implementation, P0-P3 findings, follow-up work, or
publication blocking.

### Solution-mechanism qualification invocation

`guru-qualify-solution-mechanism` is the only semantic owner for proposed
solution-mechanism qualification. It is independent from
`guru-qualify-normal-scenario`: the former judges whether a mechanism can carry
business authority, while the latter judges whether a problem scenario is
qualified. The global workflow names the same ten closed profiles and consumes
the four exits declared by the solution-mechanism interface.

The ten profiles are `task_free_pre_write`, `task_free_evolution`,
`requirements_scope_set`, `change_request_candidate_set`,
`planning_scenario_set`, `implementation_discovery`,
`base_impact_candidate_set`, `phase2_candidate_set`,
`branch_review_candidate_set`, and `publication_candidate_set`. Each caller
provides only its profile-specific candidate set and live locators; the Skill
reads current requirement, planning, architecture/spec, dependency/caller
graph, diff, tests, and repository contract before making its semantic judgment.

The exits route as follows: `classified` returns through
`guru-solution-mechanism-classified-router` to the original profile owner;
`scope_confirmation_required` invokes
`guru-clarify-requirements:solution_mechanism_scope_confirmation`;
`mechanism_revision_required` returns through
`guru-solution-mechanism-mechanism-router` for remove/replace and fresh
qualification; and `blocked` stops at
`solution-mechanism-qualification-blocked`. A forbidden
OS/kernel/process/descriptor mechanism cannot enter scope confirmation.

The package's `record-solution-mechanism-qualification` and
`check-solution-mechanism-qualification` commands are deterministic
recorder/validator components only. They validate shape, identity, freshness,
candidate coverage, and consumer binding; they do not judge mechanism,
architecture, sufficiency, severity, decision, or route. The public invocation
emits one call-local typed exit and creates no qualification artifact,
checkpoint, persistent state store, handoff, or result locator.

## Phase Route

### Architecture stage consumption

Every standard task mandatory invokes
`guru-maintain-architecture-baseline:task_impact_sync` with one fresh stage at
Planning, qualified `implementation_discovery` boundary expansion, Phase 2,
committed full-diff Branch Review, Publication, and Acceptance/Finish. The one
global mandatory marker identifies the stable Skill; a prior stage result never
substitutes for the next invocation.

Planning cannot approve without current baseline, design-constitution, and
project change-contract evidence. Expansion of scope, risk, owner, state
authority, persistence, SDK lifecycle, external integration, or another
architecture boundary invalidates the Planning result before the expanded edit
or test. Phase 2 performs the first project-check and semantic before/after
judgment. Branch Review independently recomputes those concerns over the
complete committed diff and never reuses Phase 2 as review proof.

Every fresh `baseline_current` binds `constitution_status=current`, an existing
regular project-owned constitution locator, and its exact source profile. Only
`source_profile=task_impact_sync` may resume the matching stage.
`source_profile=bootstrap_foundation|repair` reruns
`task_impact_sync(stage=<affected-stage>)` before that stage can resume.
`source_profile=promotion` always re-enters fresh Phase 2, Task Commit, and
independent committed full-diff Branch Review before Publication or
Acceptance/Finish reruns. Missing or stale Architecture evidence,
`architecture_conflict`, `contract_incomplete`, or `fitness_regression` cannot
reach Publication. Stale baseline, constitution, contribution,
expected-current, or stage identity returns `sync_required` to the Architecture
owner. Acceptance/Finish requires `reviewed_promoted` for a long-term
Architecture change or a current `no_change` proof. This is
routing-only integration; Publication and Finalizer keep their existing
package-owned business semantics.

### Workflow mode selection and Phase 0 — Issue-backed intake

Classify the user request before repository/network semantic reads. Only a
file-changing request that has not already entered an active-task route invokes
`guru-select-workflow-mode`. An Issue-backed or task-like request that only asks
for information, such as checking an Issue's current status, remains a
non-file-changing direct answer. The selector's `standard_intake` exit enters
`guru-sync-base`, then automatically follows the public graph through current
context discovery, requirements clarification, wording review, change-request
review, and `guru-create-task-workspace`. Its `task_free` exit enters only the
bounded current-checkout edit target.

`guru-sync-base` public invocation is the only authoritative synchronization
entry. The workflow, platform launchers, prompts, and Skill Markdown do not
pre-run low-level resolve/execute/check commands. Those commands remain
deterministic components inside the public Skill and focused diagnostics/tests.
Each refresh edge starts one new complete public sync invocation and discards
the stale transition; it does not maintain a parallel evidence track.

The standard Intake route carries a workflow-owned closed transition through
the five current stages:

```text
base_current -> guru-discover-change-context
context_current -> guru-clarify-requirements
clarity_current -> guru-review-contract-wording
wording_current -> guru-review-change-request
readiness_current -> guru-create-task-workspace
```

The producer's actual checked stdout is projected into the next stage and then
combined only with that consumer's current semantic authoring input. Normal
pre-task routing writes no owner-result, prerequisite, or transition file under
`.trellis/tasks/**`, `.trellis/workspace/**`, or `.trellis/.runtime/**`.
Missing/stale stage identity, unknown or multiple exits, or an unmapped consumer
stops fail closed. `prepare-task` is never a Phase 0 hop; its explicit legacy
use is a compatibility-only local diagnostic governed by the source-preserving
provenance contract.

Only `guru-create-task-workspace:created` enters planning. An incomplete or
conflicting active-task identity is terminal at the unique `invalid-task-state`
consumer and never re-enters Intake or automatic recovery. The workflow does not
create an issue, branch, worktree, or task directly and does not copy the
workspace owner's target selection, recovery, confirmation, executor, or
checker behavior.

The pre-selection identity check is scoped to the current workspace and the
requested Issue, not the repository-wide active-task inventory. Unrelated
`in_progress` tasks, including tasks owned by the same user, do not prevent
`guru-select-workflow-mode` and do not justify asking the user to select an
unrelated task or use task-free. A mapping's `source_checkout` is provenance,
not a binding of its task to that checkout. Validate a task bound to the current
workspace and resolve an unfinished task for the same Issue before selecting
new work; incomplete or conflicting relevant identity remains fail closed.
An archived task's incomplete Finalizer/closeout blocks only when live workspace,
branch, task, PR and Finalizer facts bind it to the current identity. None of
these relevance checks permits task mutation, mapping repair, or cleanup.

Every file-changing request not already routed through an active task invokes
the selector, including requests without an Issue or task-free wording.
Explicit task-free intent selects that route without another confirmation.
Without explicit intent, high-confidence bounded, reversible, low-risk work
automatically selects task-free; likely suitability with insufficient scope or
risk evidence asks once; clearly complex or high-risk work selects standard
Intake. Issue presence, file count, path, or keywords do not independently
decide the mode. Mapped exits, ordinary recovery, and same-scope retries reuse
the current selection. A failure to bootstrap the normal workflow is not
permission to switch to task-free.

Selector `task_free` invokes semantic `guru-execute-task-free-change` through a
target-owned authoring seed without expanding the selector DTO. The execution
Skill owns checkout suitability, bounded edit, targeted checks, post-write
scope/risk review, interaction re-entry, and its seven typed exits. Post-write
expansion routes bind real partial-edit and stopped-remaining-write evidence.
The `completed` workflow handoff reports only actual edited paths, concise
validation results, and unverified boundaries. The global workflow owns only
their unique consumers and fail-closed routing.

### Phase 1 — Planning

Planning produces non-empty `prd.md`, `design.md`, and `implement.md`, including
one explicit Docs SSOT Plan. Before presenting those files, mandatory invoke
`guru-review-contract-wording` with the planning profile. Then mandatory invoke
`guru-approve-task-plan` and automatically consume its typed exit. Only
`approved` reaches `phase-1-task-activation`. That target first presents the
three planning links, semantic conclusion, key choices, alternatives,
trade-offs, and unverified boundaries, then owns the dialogue-local review
pause before the official task-start state transition. Questions, revision
requests, partial choices, and ambiguous replies remain paused. Material plan
changes rerun wording and semantic review before a new presentation; an older
reply and any Phase 0 confirmation are not reusable. Explicit autonomous
execution may omit only the ordinary unchanged-plan pause; scope, authority,
material design, or risk changes still pause.

Planning owner private checkpoints are not workflow authority. The approved DTO
is sufficient for the activation consumer; later phases must not reopen or
delete an upstream owner's private state.

### Phase 2 — Implementation and check

Validate the task worktree boundary, read the approved planning artifacts and
relevant specs, implement the current scope, and use the configured Trellis
implement/check agents. Their terminal results and live repository facts are
ephemeral evidence for the mandatory `guru-check-task` semantic owner. Do not
create an implementation handoff artifact.

Every Guru-owned worker invocation prompt authorizes approved-plan work only.
For any planning-external observation it requires only a candidate ref,
observed behavior, locators, and a minimal reproduction hint; the worker must
not edit, add a test, self-fix, assign severity or classification, or select a
route for that observation. The main coordinator rereads those facts and runs
`implementation_discovery` before any follow-up dispatch or change. Official
`trellis-*` agent definitions remain upstream-owned and are not patched by the
Guru preset.

Only `guru-check-task:passed` reaches `guru-create-task-commit`. Finding and
planning-stale exits return to their declared consumers automatically. The
workflow does not reproduce Phase 2 adequacy dimensions, severity rules,
recorder/checker commands, or private evidence shape.

### Phase 3 — Commit, independent review, publication, finalization, merge

Mandatory invoke `guru-create-task-commit`, then `guru-review-branch` over the
complete committed base-to-HEAD range. After `passed`, mandatory invoke
`guru-review-task-publication`; its AI owner authors and reviews the exact
Chinese PR title/body directly from live authority without a task-local
publication handoff file.

Only publication `ready` enters `guru-finalize-task`. Stale publication,
resume, and reprepare exits are automatically consumed by their declared
Skills. The Finalizer never routes a business task to extension installation
verification. Only the finalizer may display and execute the bounded
commit/push/PR/archive/ready side-effect plan. The global workflow never calls
deterministic closeout scripts directly.

Finalizer `ready_for_merge` is not completion. It proves that the unique PR is
Ready, still points at the reviewed expected head, and still carries the exact
Publication-reviewed reference or closing-keyword semantics. The workflow immediately and mandatorily
invokes `guru-merge-task-pr`; only `merged` reaches the finish response.
`phase2_reentry_required` invokes `guru-restore-archived-task` without merge
confirmation or remote mutation. Exact restoration resumes Phase 2 through
`guru-resume-implementation`; restore conflicts stop at
`task-pr-phase2-reentry-blocked`. External blockers remain `merge_blocked`, and
`closure_mismatch` remains the post-merge closure stop.

`guru-merge-task-pr` is a semantic, remote-only post-publication route. It
compares live PR base/head branches with Finalizer's minimal reviewed identity,
then derives the GitHub closing effect from the live PR body for semantic review
and post-merge verification. The Merge owner
authors and reviews the exact Chinese
`chore(merge)` subject/body on top of that seed, then rebuilds check, review, mergeability, repository-policy
and Issue facts using repo-bound `gh`; it never enters Phase 0, invokes `guru-sync-base`, updates
the PR branch, synchronizes local `main`, or cleans resources. After one exact
merge confirmation, its deterministic executor uses the merge-commit method,
expected-head precondition and reviewed subject/body. Post-merge verification is read-only:
the PR must be `MERGED`, the merge commit must have the reviewed message and
parents `[pre-merge base head, expected head]`, the remote base must point at
that merge SHA, every close Issue must be `CLOSED`/`COMPLETED`, and
each Issue close timestamp must be no earlier than the PR merge timestamp.
Missing GitHub close-keyword effects return `closure_mismatch`; no Guru command
manually closes an Issue.

Finalizer stale handback preserves exactly `task_ref`,
`branch_review_commit`, and `stale_reason` for Publication's unique consumer
profile. Inputs outside that current profile fail closed. Proven descendant
content drift may leave Publication only through `return_to_task_work` and the
existing Phase 2 router; `ready` continues to require current content
continuity.

`guru-finalize-task` owns the single resumable transaction loop entered by the
canonical thin `guru-finish-work` router. Formal closeout accepts exactly one
reviewed payload source: Publication `ready` schema 4.0 projects
`task_ref/branch_review_commit/pr_title/pr_body`, and Finalizer target authoring
adds only `profile/mode`. Finalizer binds that exact payload in an owner-private
ignored `finalization-transaction.json` before its
first remote mutation, including the exact accepted pre-push remote head, and
retires it only after terminal public consumption. The minimal state binds
task/repository/base/branch, reviewed and publication heads, immutable
publication input, current transition and an optional PR identity. It contains no live scan, review
history, authorization, command transcript or archive projection.
`ready_for_merge` retires transaction, gate, request and superseded owner state.

GitHub PR discovery must bind the exact repository identity as well as the
branch and HEAD: `headRepository.nameWithOwner` must match the selected repo,
`headRepositoryOwner.login` must agree, and `isCrossRepository` must be false.
Missing or inconsistent repository identity fails closed before a PR candidate
can be reused or published.

### Active-task continuation authority

For an exact current task, the active workflow's single non-empty
`[trellis-continuation]` block is the only detailed continuation authority.
`task.json.status`, Phase Index text, `[workflow-state:*]` breadcrumbs, platform
entries, hooks, prior conversation text, and private checkpoint names provide
facts or broad lifecycle guidance only. They must not maintain another route
table or infer a semantic pass. `planning` and `planning-inline` share one Phase
1 matrix; `in_progress` and `in_progress-inline` share one Phase 2-to-Finalizer
matrix; `completed` enters canonical `guru-finish-work`; invalid identity or an
unsupported task state stops at `invalid-task-state`. Without an exact current
task, continuation never selects a replacement from project inventory.

Continuation first distinguishes a current adjacent public DTO from lost
output. A still-current adjacent DTO goes directly through its Interface-
declared projection to the unique consumer. A lost DTO returns to the original
producer: deterministic mutation/output loss uses only that producer's formal
recovery or rematerialization, while a semantic result is rerun fresh by its
semantic owner. Missing checkpoints, clean Git state, commit messages, task
status, old summaries, and earlier confirmation are never substitutes.

The Phase 1 matrix preserves the current owner for task-created attachment,
partial planning, planning wording, Planning Architecture, plan approval,
dialogue-local plan acceptance, and activation. Activation has one
workflow-owned `initial|recovery` contract: `initial` performs the official
status transition once after current approval and confirmation; `recovery`
requires the same exact task/worktree/branch/mapping pair already to be
`in_progress` and rematerializes the same success without invoking activation
again. Neither path persists confirmation.

When the task/workspace mutation succeeded but its `created` output was lost,
the original `guru-create-task-workspace:recover_created_result` profile invokes
its read-only `recover-task-workspace-result` checker for the exact planning
task. It may rematerialize only the normal `created` exit after current task,
branch, worktree, boundary, and both runtime mappings agree; it never creates or
repairs another Issue, branch, worktree, task, or mapping.

For Phase 2, a current retained `passed` checkpoint may be checked again and
projected through the existing checker-to-`invoke-guru-check-task` path. This is
rematerialization through the existing public invocation, not a new public
recovery profile, exit, schema, or semantic judgment. If that checkpoint is
missing or stale, fresh Phase 2 Architecture and `guru-check-task` are required.
Task Commit output loss uses the existing `guru-create-task-commit` same-
candidate `recovery_resume` contract and may not create a second candidate,
empty commit, amend, or duplicate commit. Lost Branch Review or Publication
DTOs require fresh Architecture at the matching stage and a fresh semantic
owner run because their successful checkpoints retire after output validation.
This continuation stops at the existing `guru-finalize-task` entry; Finalizer,
archive, Merge, and archived-task recovery retain their existing owners.

`确认继续` authorizes only one unique, fully displayed, still-current side-effect
plan in the current dialogue. A verified successful executor result returns the
formal typed exit, and mapped transitions continue automatically until a new
side effect, real choice, or fail-closed stop appears. If no plan is pending and
an exact active task exists, the phrase expresses continuation intent and loads
the same workflow block. Authorization is never written to task, runtime,
checkpoint, gate, DTO, schema, or archive state.

## Consumer Projection

- Producer output is the selected exit's independent public schema.
- Consumer input is owned by the consumer package, workflow target, or stop.
- Projection is the single Interface-declared `direct`, `select`, `rename`, or
  deterministic `normalize` operation.
- When the consumer needs fresh semantic fields, only the target package's
  `skill_input_authoring_seed` may partition producer seed fields from
  caller-authored fields. The partitions must be disjoint, complete, and merge
  without overwrite.
- Private artifacts, digests, live scans, review history, authorization state,
  recorder implementation, and runtime source are never consumer input.

An exit field with no direct consumer use is invalid public output. Digest or
artifact convenience never creates workflow authority.

## Interaction Budget

Ask the user only for missing intent, a material scope/plan choice, new external
authority, or one fully displayed side-effect set. Use `确认继续` for one current,
unique, unambiguous plan and accept any clear affirmative reply. Never require
the user to repeat a SHA, digest, ref, or prescribed sentence.

Automatically consume mapped typed exits, stale/re-entry/reprepare routes, and
recorder/validator steps. Do not simulate a human approval chain and do not
persist authorization state, text, refs, digests, or process.

For an existing Open Issue, the happy-path budget is exactly four
`确认继续` boundaries: workspace/task creation, Phase 1 plan review, the complete
Finalizer side-effect set, and expected-head merge. Creating a new Issue adds
one independent Issue creation confirmation for a total of five. Task
activation after the Phase 1 acceptance, implementation, Phase 2 check, Branch
Review, an exactly requested task commit, mapped exits and read-only recovery
add no routine confirmation. Branch
classification, protection, sharing, ownership and publication state are not
operation authority; without a current exact commit request, Task Commit asks
once for the fully displayed action.
Finalizer and merge confirmation remain separate because merge readiness exists
only after Finalizer reaches `ready_for_merge`.

The canonical workflow declares those five possible boundaries with one
`guru-confirmation-boundary` marker each. The controlled #174 replay derives
open/new-Issue budgets from those markers and its single chained event log; it
must not hard-code totals or sum isolated eval cases.

## Docs SSOT And External Work Items

Every planning cycle chooses one Docs SSOT strategy:
`ssot_first`, `delta_first`, `bootstrap_or_repair_docs`, or
`no_docs_update_needed`. Phase 2 executes that decision; Branch Review verifies
the final reconciliation but must not perform the first merge.

Publication is the sole semantic owner of external-work-item disposition. It
rereads current requirement authority and live GitHub state, then decides one
of three effects: a fully delivered Issue-backed task normally requests closure;
a concrete post-merge validation, observation, release, or incomplete-delivery
requirement keeps the Issue reference-only; and a task with no external work
item produces no Issue reference or closing effect. A PR targeting the default
branch carries the reviewed closing keyword when closure is requested. A PR
targeting a non-default branch remains reference-only; the later Publication
onto the default branch rereads authority and decides closure afresh.

Finalizer binds the exact Publication-reviewed PR payload. Merge verifies that
payload and GitHub's resulting state but does not re-decide disposition or call
an Issue-close API.

Before a planning, Phase 2, Branch Review, or publication stop, resolve the
human-authored artifacts and show only files that exist. JSON gates, private
checkpoints, assignment/liveness records, raw agent reports, and digests are not
standard user-facing handoff artifacts.

## Platform And Ownership Boundary

Official Trellis owns `trellis-start`, `trellis-continue`,
`trellis-finish-work`, official hooks, sub-agents, runtime agents, bundled
skills, and meta references. The Guru preset neither installs nor
managed-upgrades those paths.

The continuation extraction/loading protocol and all official platform entry
bytes are likewise upstream-owned. Guru Team owns only the semantic body in its
canonical marketplace workflow and the Guru packages that body names. Preset
apply or reapply must not create, patch, replace, delete, or claim upstream
entries, and must not modify the selected `.trellis/workflow.md` continuation
body. A target with the Guru workflow but without the required Guru preset is
an incomplete contract and stops instead of falling back to native routes.

Mandatory Guru routing is guaranteed by the active workflow markers and
installed `guru-*` packages. Platform discovery copies are generated only under
Guru namespaces. The canonical overlay inventory contains one descriptor-bound
`guru-finish-work` entry for each of the 22 pinned upstream platforms. A target
installs only its exact manifest-selected entries; the guru-trellis dogfood set
is Claude, Codex, and Cursor, while OpenCode remains explicitly selectable.
Every installed entry loads live context, reads this workflow, invokes the
active owners, and contains no step-local logic.

## Validation

At minimum validate:

```bash
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

Combined acceptance also covers clean marketplace init, existing-project
preview/switch, preset initial apply/reapply, official `trellis update`, version
upgrade, the complete descriptor inventory and canonical projections, exact
manifest-selected discovery roots, three-platform dogfood drift, managed hashes,
`.new`/`.bak`, current ownership/installed-manifest validation, executable
modes, README commands, and a recursive zero-sidecar scan.

## Active-Task Base Evolution Boundaries

Every stable active-task boundary observes the selected base through the single
`guru-reconcile-task-base` pair guard before continuing. The guarded
boundaries are planning approval before activation, Phase 2 pass before Task
Commit, Task Commit before Branch Review, Branch Review before Publication,
Publication readiness before the first Finalizer publication side effect, and
Finalizer base-only mismatch before resuming the same finalization plan.

The workflow owns one closed `resume_target` table, mandatory invocation of the
semantic owner for a new pair, and one `guru-base-reconciliation-router`.
An unchanged pair resumes the original target without semantic invocation.
The six semantic exits route uniquely: `reconciled` resumes the guarded target,
`review_continuity_required` first completes its confirmed expected-head local
reconciliation commit and then invokes the bounded Branch Review profile,
`implementation_required` returns to implementation and a fresh Phase 2
check, `planning_stale` returns to Planning,
`scope_confirmation_required` invokes requirement clarification, and
`blocked` stops fail closed. Mapped routes do not create a generic
confirmation boundary.

Base identity is integration evidence, not authority or task-content
freshness. A base-only change cannot by itself invalidate Planning, Phase 2,
Branch Review, or Publication. For post-Branch Review, post-Publication, and
Finalizer mismatch profiles, a compatible candidate that changes the shared
reviewed-content identity uses `review_continuity_required`: after semantic
judgment and an exact current-dialogue Git confirmation, the reconcile owner
creates one persistent local reconciliation commit bound to expected task/base
HEADs and the reviewed candidate tree. Bounded continuity separately binds the
prior complete review commit and that current commit, then projects the current
commit as Publication's reviewed-content anchor. Publication stale remains
limited to its own PR payload, issue scope, validation statement, deployment,
security metadata, or genuine task-content drift. Finalizer exposes
`base_reconciliation_required` separately and never relabels a base-only
mismatch as Publication stale.

## Closeout Original-Entry Routing

Commit, Publication, Finalizer, and Merge remain four independent semantic
Skills. Each package keeps its existing Interface-declared public wrapper and
stable command id as the only normal entry. Happy Path consolidation happens
inside that command; an older argument shape selects a mutually exclusive
compatibility branch, while record/check/execute helpers remain package-private
testing, diagnosis, or bounded-recovery entries. The normal sequence is:

- Commit: one `prepare-task-commit`, one dialogue-local action confirmation,
  then one `invoke-guru-create-task-commit` through `scripts/invoke.sh` with the
  prepared candidate locator.
- Publication: after the AI semantic review, one
  `invoke-guru-review-task-publication` through `scripts/invoke.sh` with the
  public input and semantic result.
- Finalizer: one read-only preview, one dialogue-local Finalizer confirmation,
  then one `invoke-guru-finalize-task` through `scripts/invoke.sh` with the
  confirmed preview identity.
- Merge: at most one expected-head-bound `watch-task-pr-checks` while checks are
  pending, then one dialogue-local merge confirmation and one
  `invoke-task-pr-merge` through `scripts/invoke.sh`.

The original command may reuse facts only within one invocation, for one exact
authority identity, and only until a mutation boundary. It may automatically
consume a mapped deterministic recovery/reprepare only when the package proves
the semantic plan and side-effect set are unchanged. Material scope, authority,
payload, head, plan, or action changes return to the owning semantic step and
invalidate the previous confirmation. The Happy Path must not execute the
compatibility branch first or publish a second wrapper/command authority. Every
Merge exit is terminal for that Skill; its consumer or stop target runs next,
with no post-exit polling or work.

## Post-Delivery Task Lifecycle

The additive Post-Delivery lifecycle consists of five independent semantic
owners. Their packages may be installed before activation, but the production
workflow does not route into them until the lifecycle graph owner performs one
atomic cutover. A Delivery merge, PR readiness, deployment, passing test, closed
Issue, or archived directory never implies Task Completion.

`guru-review-task-completion` is the only Completion owner. It rereads accepted
scope, every applicable Delivery fact, current requirement authority, validation
and external evidence. Any remaining work, evidence gap, requirement revision,
implementation revision, or additional Delivery keeps the same task active and
returns the earliest affected owner. Only `completed` enters Closure.

`guru-complete-task-closure` owns the source Issue disposition after Completion.
No-Issue, reference-only, follow-up and parent-only relationships produce
`no_mutation`. Closing one exact source Issue is a separate confirmed provider
mutation with same-transaction recovery and post-read verification. Delivery
and bookkeeping PRs contain no Issue-closing keyword.

`guru-finish-task` owns terminal archive persistence after Closure. It reviews a
lifecycle-only allowlist, then uses three separate mutation boundaries: local
archive projection, bookkeeping commit/push/PR publication, and expected-head
merge. The bookkeeping PR is administrative: it creates no task or Delivery
result and never re-enters Completion. Finish returns `success` only after the
remote target baseline contains the unique final archive, the active task is
absent, and terminal metadata is readable there. Local movement, commit, push,
or PR creation alone returns `resume_finish`.

`guru-cleanup-task-resources` consumes only the current Finish success. It
freshly reviews the exact owned branch, worktree and ignored runtime resources,
requires an independent confirmation, and preserves every previous lifecycle
result when cleanup is partial. A Reactivate invalidates the prior Finish
receipt, so old success cannot delete current resources.

`guru-reactivate-task` handles only a normally finished original task and is
distinct from merge-time `guru-restore-archived-task`. It preserves task and
Issue identity, verifies current archive/scope/base facts, and either reuses one
exact clean branch/worktree or creates a new branch/worktree from the reviewed
target baseline. It moves the single archive copy back to active, refreshes task
metadata and ignored mappings, and routes explicitly to requirements, planning,
implementation, or evidence refresh. It never creates a replacement task,
reopens an Issue, or treats prior Completion/Closure/Finish as current approval.
