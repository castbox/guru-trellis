# Workflow Contract

## Canonical Sources

`trellis/workflows/guru-team/workflow.md` is the reusable marketplace workflow
contract. `.trellis/workflow.md` is the dogfood installation copy and must be
byte-identical after every canonical workflow change.

The workflow marketplace installs only `.trellis/workflow.md`. The complete
Guru Team extension, public Skill projections, package runtimes, minimal shared kernel, schemas, platform
discovery copies, and Guru-owned explicit entries are installed by the preset.

## SSOT Boundary

The global workflow owns only:

- phase order and the current-task status router;
- one mandatory invocation marker per active stable `guru-*` Skill id;
- every declared typed exit and its single consumer;
- workflow targets, fail-closed stops, and automatic mapped re-entry;
- tool-free initial request classification;
- workspace/task boundary selection and task activation;
- Docs SSOT and Issue Scope Ledger integration points;
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

The current package registry contains exactly 23 active Skill ids and 97
external exits. Twenty-two Skills participate in the business-task workflow,
whose global graph contains 22 mandatory invokes, 95 mapped exits, 35 workflow
targets, and 24 stop targets. `guru-verify-extension-installation` is the remaining
standalone-only source-repository Skill; its two exits return directly to its
caller-owned stop targets and never appear in the business workflow.

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
| `guru-review-branch` | `passed -> guru-review-task-publication`; `continuity_passed -> guru-base-continuity-passed-router`; `implementation_required -> guru-branch-review-implementation-router`; `scope_confirmation_required -> guru-branch-review-scope-router`; `blocked -> branch-review-blocked` |
| `guru-review-task-publication` | `ready -> guru-finalize-task`; `return_to_task_work -> guru-task-publication-work-router`; `blocked -> task-publication-review-blocked` |
| `guru-verify-extension-installation` (standalone only) | `verified -> extension-installation-verification-verified`; `blocked -> extension-installation-verification-blocked` |
| `guru-finalize-task` | `publication_review_stale -> guru-review-task-publication`; `resume_finalization -> guru-finalize-task`; `reprepare_required -> guru-finalize-task`; `ready_for_merge -> guru-merge-task-pr`; `blocked -> task-finalization-blocked` |
| `guru-merge-task-pr` | `merged -> guru-finalization-finish-response`; `merge_blocked -> task-pr-merge-blocked`; `phase2_reentry_required -> guru-restore-archived-task`; `closure_mismatch -> task-pr-closure-mismatch` |
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
checkpoint, ledger, handoff, or result locator.

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
Ready, still points at the reviewed expected head, and every `close_issues`
entry remains Open before merge. The workflow immediately and mandatorily
invokes `guru-merge-task-pr`; only `merged` reaches the finish response.
`phase2_reentry_required` invokes `guru-restore-archived-task` without merge
confirmation or remote mutation. Exact restoration resumes Phase 2 through
`guru-resume-implementation`; restore conflicts stop at
`task-pr-phase2-reentry-blocked`. External blockers remain `merge_blocked`, and
`closure_mismatch` remains the post-merge closure stop.

`guru-merge-task-pr` is a semantic, remote-only post-publication route. It
compares live PR base/head branches and close keywords with Finalizer's minimal
reviewed authority. The Merge owner authors and reviews the exact Chinese
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
adds only `profile/mode`. The schema 3.0 closeout plan binds that exact payload;
no body file, summary-index file, alternate locator, or generated source
participates in closeout. Legacy 3.0 Publication/Finalizer DTO shapes fail
closed and require a fresh Publication run.

The paragraph above describes only legacy compatibility. Current Finalizer
persists an owner-private ignored `finalization-transaction.json` before its
first remote mutation, including the exact accepted pre-push remote head, and
retires it only after terminal public consumption. The minimal state binds
task/repository/base/branch, reviewed and publication heads, immutable
publication input, current transition and an optional PR identity. It contains no live scan, review
history, authorization, command transcript or archive projection.
`ready_for_merge` retires transaction, gate, request and superseded owner state.
Legacy `closeout-plan.json` schema/example bytes remain immutable assets and
never enter a current route.

GitHub PR discovery must bind the exact repository identity as well as the
branch and HEAD: `headRepository.nameWithOwner` must match the selected repo,
`headRepositoryOwner.login` must agree, and `isCrossRepository` must be false.
Missing or inconsistent repository identity fails closed before a PR candidate
can be reused or published.

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

## Docs SSOT And Issue Scope

Every planning cycle chooses one Docs SSOT strategy:
`ssot_first`, `delta_first`, `bootstrap_or_repair_docs`, or
`no_docs_update_needed`. Phase 2 executes that decision; Branch Review verifies
the final reconciliation but must not perform the first merge.

`issue-scope-ledger.json` is the task-local scope classification source.
`close_issues` alone may appear in PR close keywords. `related_issues` and
`followup_issues` remain open unless a later independently accepted task closes
them.

Before a planning, Phase 2, Branch Review, or publication stop, resolve the
human-authored artifacts and show only files that exist. JSON gates, private
checkpoints, assignment/liveness records, raw agent reports, and digests are not
standard user-facing handoff artifacts.

## Platform And Ownership Boundary

Official Trellis owns `trellis-start`, `trellis-continue`,
`trellis-finish-work`, official hooks, sub-agents, runtime agents, bundled
skills, and meta references. The Guru preset neither installs nor
managed-upgrades those paths.

Mandatory Guru routing is guaranteed by the active workflow markers and
installed `guru-*` packages. Platform discovery copies are generated only under
Guru namespaces. The only explicit platform overlays are the three Guru-owned
`guru-finish-work` entries for Codex, Claude, and Cursor; they load live context,
read this workflow, invoke the active owners, and contain no step-local logic.

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
upgrade, Shared/Codex/Claude/Cursor discovery, managed hashes, `.new`/`.bak`,
current ownership/installed-manifest validation, executable modes, README
commands, and a recursive zero-sidecar scan.

## Active-Task Base Evolution Boundaries

Every stable active-task boundary observes the selected base through the single
`guru-reconcile-task-base` pair guard before continuing. The guarded
boundaries are planning approval before activation, Phase 2 pass before Task
Commit, Task Commit before Branch Review, Branch Review before Publication,
Publication readiness before the first Finalizer publication side effect, and
Finalizer base-only mismatch before resuming the same closeout plan.

The workflow owns one closed `resume_target` table, mandatory invocation of the
semantic owner for a new pair, and one `guru-base-reconciliation-router`.
An unchanged pair resumes the original target without semantic invocation.
The six semantic exits route uniquely: `reconciled` resumes the guarded target,
`review_continuity_required` invokes the bounded Branch Review profile,
`implementation_required` returns to implementation and a fresh Phase 2
check, `planning_stale` returns to Planning,
`scope_confirmation_required` invokes requirement clarification, and
`blocked` stops fail closed. Mapped routes do not create a generic
confirmation boundary.

Base identity is integration evidence, not authority or task-content
freshness. A base-only change cannot by itself invalidate Planning, Phase 2,
Branch Review, or Publication. Publication stale remains limited to its own PR
payload, issue scope, validation statement, deployment, and security metadata.
Finalizer exposes `base_reconciliation_required` separately and never
relabels a base-only mismatch as Publication stale.

## Closeout Happy Path Routing

Commit, Publication, Finalizer, and Merge remain four independent semantic
Skills. Each package declares exactly one recommended normal-path facade while
retaining older record/check/execute/invoke commands as compatibility, testing,
or bounded recovery entries. The normal sequence is:

- Commit: one `prepare-task-commit`, one dialogue-local action confirmation,
  then one `invoke-guru-create-task-commit-happy-path-v1`.
- Publication: after the AI semantic review, one `review-task-publication`.
- Finalizer: one read-only preview, one dialogue-local Finalizer confirmation,
  then one `finalize-task-happy-path`.
- Merge: at most one expected-head-bound `watch-task-pr-checks` while checks are
  pending, then one dialogue-local merge confirmation and one
  `complete-task-pr-merge`.

A facade may reuse facts only within one invocation, for one exact authority
identity, and only until a mutation boundary. It may automatically consume a
mapped deterministic recovery/reprepare only when the package proves the
semantic plan and side-effect set are unchanged. Material scope, authority,
payload, head, plan, or action changes return to the owning semantic step and
invalidate the previous confirmation. Every Merge exit is terminal for that
Skill; its consumer or stop target runs next, with no post-exit polling or work.
