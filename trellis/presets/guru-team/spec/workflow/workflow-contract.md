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

The current package registry contains exactly 16 active Skill ids and 62
external exits. Fifteen Skills participate in the business-task workflow,
whose global graph contains 15 mandatory invokes, 60 mapped exits, and 36
workflow/stop targets. `guru-verify-extension-installation` is the remaining
standalone-only source-repository Skill; its two exits return directly to its
caller-owned stop targets and never appear in the business workflow.

| Skill | Typed exit -> unique consumer |
| --- | --- |
| `guru-sync-base` | `synced -> guru-discover-change-context`; `skipped -> original-request-route`; `blocked -> base-sync-blocked` |
| `guru-discover-change-context` | `context_ready -> guru-clarify-requirements`; `refresh_base -> guru-sync-base`; `blocked -> change-context-blocked` |
| `guru-clarify-requirements` | `clear -> guru-requirements-clear-router`; `needs_context -> guru-discover-change-context`; `refresh_context -> guru-sync-base`; `retarget_context -> guru-sync-base`; `new_task -> guru-full-task-intake-chain`; `blocked -> requirements-clarification-blocked` |
| `guru-review-contract-wording` | `pass -> guru-contract-wording-pass-router`; `content_changed -> guru-contract-wording-change-router`; `blocked -> contract-wording-blocked` |
| `guru-review-change-request` | `ready -> guru-create-task-workspace`; `clarify_requirements -> guru-clarify-requirements`; `review_wording -> guru-review-contract-wording`; `refresh_context -> guru-sync-base`; `blocked -> change-request-review-blocked` |
| `guru-create-task-workspace` | `created -> guru-task-workspace-created`; `refresh_review -> guru-sync-base`; `blocked -> task-workspace-blocked` |
| `guru-approve-task-plan` | `approved -> phase-1-task-activation`; `revision_required -> guru-approve-task-plan`; `clarify_scope -> guru-task-plan-clarify-scope-router`; `blocked -> task-plan-approval-blocked` |
| `guru-check-task` | `passed -> guru-create-task-commit`; `implementation_required -> guru-resume-implementation`; `planning_stale -> guru-task-check-planning-router`; `blocked -> task-check-blocked` |
| `guru-create-task-commit` | `committed -> guru-review-branch`; `revision-required -> guru-create-task-commit`; `blocked -> task-commit-blocked` |
| `guru-review-branch` | `passed -> guru-review-task-publication`; `implementation_required -> guru-branch-review-implementation-router`; `scope_confirmation_required -> guru-branch-review-scope-router`; `blocked -> branch-review-blocked` |
| `guru-review-task-publication` | `ready -> guru-finalize-task`; `return_to_task_work -> guru-task-publication-work-router`; `blocked -> task-publication-review-blocked` |
| `guru-verify-extension-installation` (standalone only) | `verified -> extension-installation-verification-verified`; `blocked -> extension-installation-verification-blocked` |
| `guru-finalize-task` | `publication_review_stale -> guru-review-task-publication`; `resume_finalization -> guru-finalize-task`; `reprepare_required -> guru-finalize-task`; `ready_for_merge -> guru-merge-task-pr`; `blocked -> task-finalization-blocked` |
| `guru-merge-task-pr` | `merged -> guru-finalization-finish-response`; `merge_blocked -> task-pr-merge-blocked`; `closure_mismatch -> task-pr-closure-mismatch` |

Missing Skill packages, missing or duplicate markers, unknown/multiple/unmapped
exits, a consumer mismatch, a dangling target, a kind mismatch, or an invalid
projection always fails closed. Frontmatter discovery is only a convenience and
never substitutes for a mandatory workflow invocation marker.

## Phase Route

### Workflow mode selection and Phase 0 — Issue-backed intake

Classify the user request before repository/network semantic reads. A
repo-changing, issue-backed, task-like, or file-changing route first invokes
`guru-select-workflow-mode`. Its `standard_intake` exit enters `guru-sync-base`,
then automatically follows the public graph through current context discovery,
requirements clarification, wording review, change-request review, and
`guru-create-task-workspace`. Its `task_free` exit enters only the bounded
current-checkout edit target.

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

Only `guru-create-task-workspace:created` enters planning. The workflow does not
create an issue, branch, worktree, or task directly and does not copy the
workspace owner's target selection, recovery, confirmation, executor, or
checker behavior.

Explicit task-free intent selects that route without another confirmation.
Implicit intent may trigger one confirmation; refusal selects standard Intake.
Uncertainty selects standard Intake, and mapped exits, ordinary recovery, and
same-scope retries reuse the current selection. A failure to bootstrap the
normal workflow is not permission to switch to task-free.

### Phase 1 — Planning

Planning produces non-empty `prd.md`, `design.md`, and `implement.md`, including
one explicit Docs SSOT Plan. Before presenting those files, mandatory invoke
`guru-review-contract-wording` with the planning profile. Then mandatory invoke
`guru-approve-task-plan` and automatically consume its typed exit. Only
`approved` reaches `phase-1-task-activation` and the official task-start state
transition.

Planning owner private checkpoints are not workflow authority. The approved DTO
is sufficient for the activation consumer; later phases must not reopen or
delete an upstream owner's private state.

### Phase 2 — Implementation and check

Validate the task worktree boundary, read the approved planning artifacts and
relevant specs, implement the current scope, and use the configured Trellis
implement/check agents. Their terminal results and live repository facts are
ephemeral evidence for the mandatory `guru-check-task` semantic owner. Do not
create an implementation handoff artifact.

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
`merge_blocked` and `closure_mismatch` stop at their distinct consumers.

`guru-merge-task-pr` is a semantic, remote-only post-publication route. It
compares live PR base/head branches and close keywords with Finalizer's minimal
reviewed authority, then rebuilds check, review, mergeability, repository-policy
and Issue facts using repo-bound `gh`; it never enters Phase 0, invokes `guru-sync-base`, updates
the PR branch, synchronizes local `main`, or cleans resources. After one exact
merge confirmation, its deterministic executor uses the selected repository
method and expected-head precondition. Post-merge verification is read-only:
the PR must be `MERGED`, every close Issue must be `CLOSED`/`COMPLETED`, and
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

For an existing Open Issue, the happy-path budget is exactly three
`确认继续` boundaries: workspace/task creation, the complete Finalizer side-effect
set, and expected-head merge. Creating a new Issue adds one independent Issue
creation confirmation for a total of four. Planning, task activation,
implementation, Phase 2 check, Branch Review, an exactly requested task commit,
mapped exits and read-only recovery add no routine confirmation. Branch
classification, protection, sharing, ownership and publication state are not
operation authority; without a current exact commit request, Task Commit asks
once for the fully displayed action.
Finalizer and merge confirmation remain separate because merge readiness exists
only after Finalizer reaches `ready_for_merge`.

The canonical workflow declares those four possible boundaries with one
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
