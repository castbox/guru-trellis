# Workflow Contract

## Canonical Sources

`trellis/workflows/guru-team/workflow.md` is the reusable marketplace workflow
contract. `.trellis/workflow.md` is the dogfood installation copy and must be
byte-identical after every canonical workflow change.

The workflow marketplace installs only `.trellis/workflow.md`. The complete
Guru Team extension, public Skill packages, shared runtime, schemas, platform
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

## Integrated Public Graph

The current graph contains exactly 14 active mandatory Skill ids, 54 external
exits, and 31 workflow/stop targets. Each exit below has one consumer; the
package Interface owns the exact projection and any target-owned authoring
partition.

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
| `guru-verify-extension-installation` | `verified -> guru-finalize-task`; `not_required -> guru-finalize-task`; `return_to_task_work -> guru-extension-verification-work-router`; `blocked -> extension-installation-verification-blocked` |
| `guru-finalize-task` | `verification_required -> guru-verify-extension-installation`; `publication_review_stale -> guru-review-task-publication`; `resume_finalization -> guru-finalize-task`; `reprepare_required -> guru-finalize-task`; `published -> guru-finalization-finish-response`; `blocked -> task-finalization-blocked` |

Missing Skill packages, missing or duplicate markers, unknown/multiple/unmapped
exits, a consumer mismatch, a dangling target, a kind mismatch, or an invalid
projection always fails closed. Frontmatter discovery is only a convenience and
never substitutes for a mandatory workflow invocation marker.

## Phase Route

### Phase 0 — Issue-backed intake

Classify the user request before repository/network semantic reads. A
repo-changing, issue-backed, task-like, or file-changing route begins with
`guru-sync-base`, then automatically follows the public graph through current
context discovery, requirements clarification, wording review, change-request
review, and `guru-create-task-workspace`.

Only `guru-create-task-workspace:created` enters planning. The workflow does not
create an issue, branch, worktree, or task directly and does not copy the
workspace owner's target selection, recovery, confirmation, executor, or
checker behavior.

The normal route is Issue + Trellis task + task worktree. A task-free/direct
edit path exists only when the user explicitly authorizes that exact bounded
exception for the current turn. A failure to bootstrap the normal workflow is
not permission to switch to task-free.

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

### Phase 3 — Commit, independent review, publication, finalization

Mandatory invoke `guru-create-task-commit`, then `guru-review-branch` over the
complete committed base-to-HEAD range. After `passed`, the caller authors the
current task-local `pr-body.md` and `finish-summary-index.json` candidates and
mandatory invokes `guru-review-task-publication`.

Only publication `ready` enters `guru-finalize-task`. Finalizer verification,
stale publication, resume, and reprepare exits are automatically consumed by
their declared Skills. Only the finalizer may display and execute the bounded
commit/push/PR/archive/ready side-effect plan. The global workflow never calls
deterministic closeout scripts directly.

Finalizer stale handback preserves exactly `task_ref`,
`branch_review_commit`, and `stale_reason` for Publication's unique consumer
profile. Inputs outside that current profile fail closed. Proven descendant
content drift may leave Publication only through `return_to_task_work` and the
existing Phase 2 router; `ready` continues to require current content
continuity.

`guru-finalize-task` owns the single resumable transaction loop entered by the
canonical thin `guru-finish-work` router. Formal closeout accepts exactly one
reviewed body source: `--body-file` must point directly to the current
task-local `pr-body.md` and bind its exact raw UTF-8 bytes. No alternate body
locator or generated source participates in closeout.

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
