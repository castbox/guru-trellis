# Workflow Contract

## Canonical Sources

`trellis/workflows/guru-team/workflow.md` is the reusable marketplace workflow
contract. `.trellis/workflow.md` is the dogfood installation copy and must be
byte-identical after every canonical workflow change.

The workflow marketplace installs only `.trellis/workflow.md`. The complete
Guru Team extension, public Skill projections, package runtimes, minimal shared kernel, schemas, platform
discovery copies, and Guru-owned explicit entries are installed by the preset.

Guru task workspace terminology means the isolated task checkout/worktree and
current task/branch/session binding. It never refers to the retired
`.trellis/workspace/<developer>/journal-*` namespace. Current task resolution
uses TaskId/generation, task metadata, branch binding, and live Git checkout
facts; old task/workspace mappings and checkout paths are not identity authority.
No normal workflow path initializes or reads developer identity, workspace
journal/index, session recording, or legacy agent traces.

## SSOT Boundary

The global workflow owns only:

- phase order and the current-task status router;
- one mandatory invocation marker per active stable `guru-*` Skill id;
- every declared typed exit and its single consumer;
- workflow targets, fail-closed stops, and automatic mapped re-entry;
- tool-free initial request classification;
- workspace/task boundary selection and task activation;
- Docs SSOT and post-Completion external-work-item Closure integration points;
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

The current source registry has 36 active packages, 164 package exits, and 109
commands. The business-task workflow declares 34 mandatory invocations and 158
external exits; `guru-verify-extension-installation` and
`guru-upgrade-installation` are standalone-only. These
counts are checks against the live registry and workflow markers, not an
alternative routing authority.

The production spine is `guru-sync-base` -> context/clarification/wording/
change-request review -> `guru-create-issue` for a proposed draft (then fresh
Intake) or `guru-create-task` for an existing Issue/standalone request ->
identity/binding/checkout/session resolution -> Planning and `guru-activate-task`
-> Phase 2 check -> Task Commit -> independent Branch Review -> Delivery Review
-> Delivery Publish -> Delivery Merge -> whole-task Completion -> source Issue
Closure -> Finish -> Cleanup. Incomplete Completion retains the same active
TaskId and routes to the earliest affected owner or next Delivery slice.
Normally finished archives can enter Reactivate under a new generation.

The workflow's `guru-skill-invoke` and `guru-skill-exit` markers, registry and
package interfaces declare every exact exit/consumer pair. No summary in this
contract supersedes that graph. The old `guru-create-task-workspace`,
`guru-review-task-publication`, `guru-finalize-task`, `guru-merge-task-pr`, and
`guru-restore-archived-task` packages have no current production edge. Historical
IDs and old DTOs cannot be projected into the new lifecycle.

Missing Skill packages, missing or duplicate markers, unknown/multiple/unmapped
exits, a consumer mismatch, a dangling target, a kind mismatch, or an invalid
projection always fails closed. The installed graph validator checks every
parsed invocation and exit against the current registry/interface declarations;
an extra retired marker fails even when all required markers remain present.
Frontmatter discovery is only a convenience and
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

Explicit old-installation upgrades enter standalone `guru-upgrade-installation`
from the reviewed target source, outside business-task Intake/current target
preflight. Its current Interface owns all local behavior and typed exits;
the global workflow declares only terminal consumers. Successful installation
does not imply task re-entry, Planning approval or Release qualification.

### Architecture stage consumption

Every standard task mandatory invokes
`guru-maintain-architecture-baseline:task_impact_sync` with one fresh stage at
Planning, qualified `implementation_discovery` boundary expansion, Phase 2,
committed full-diff Branch Review, Delivery Review, and Completion/Finish. The one
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
independent committed full-diff Branch Review before Delivery Review or
Completion/Finish reruns. Missing or stale Architecture evidence,
`architecture_conflict`, `contract_incomplete`, or `fitness_regression` cannot
reach Delivery Review. Stale baseline, constitution, contribution,
expected-current, or stage identity returns `sync_required` to the Architecture
owner. Completion/Finish requires `reviewed_promoted` for a long-term
Architecture change or a current `no_change` proof. This is routing-only
integration; Delivery, Completion, Closure and Finish retain their package-owned
judgments.

### Workflow mode selection and Phase 0 — Issue-backed intake

Classify the user request before repository/network semantic reads. Only a
file-changing request that has not already entered an active-task route invokes
`guru-select-workflow-mode`. An Issue-backed or task-like request that only asks
for information, such as checking an Issue's current status, remains a
non-file-changing direct answer. The selector's `standard_intake` exit enters
`guru-sync-base`, then automatically follows the public graph through current
context discovery, requirements clarification, wording review, change-request
review, and the `guru-task-intake-router`. Its `task_free` exit enters only the
bounded current-checkout edit target.

`guru-sync-base` public invocation is the only authoritative synchronization
entry. The workflow, platform launchers, prompts, and Skill Markdown do not
pre-run low-level resolve/execute/check commands. Those commands remain
deterministic components inside the public Skill and focused diagnostics/tests.
Each refresh edge starts one new complete public sync invocation and discards
the stale transition; it does not maintain a parallel evidence track.

The standard Intake route carries a workflow-owned closed transition:

```text
base_current -> guru-discover-change-context
context_current -> guru-clarify-requirements
clarity_current -> guru-review-contract-wording
wording_current -> guru-review-change-request
readiness_current -> guru-task-intake-router
```

The router uses `ready.transition.target.kind`: `proposed_draft` invokes
`guru-create-issue` with its own confirmation and then restarts fresh Sync and
Intake for the new Issue; `existing_issue` and `standalone_request` invoke
`guru-create-task`. Only the latter's checked `created` exit enters Planning.
Issue creation is not task creation. Identity, branch binding, checkout and
session owners resolve the exact TaskId/generation for subsequent phases.

The producer's actual checked stdout is projected into the next stage and then
combined only with that consumer's current semantic authoring input. Normal
pre-task routing writes no owner-result, prerequisite, or transition file under
`.trellis/tasks/**`, `.trellis/workspace/**`, or `.trellis/.runtime/**`.
Missing/stale stage identity, unknown or multiple exits, or an unmapped consumer
stops fail closed. Retired `prepare-task` is never a Phase 0 hop.

Only `guru-create-task:created` enters planning. An incomplete or
conflicting active-task identity is terminal at the unique `invalid-task-state`
consumer and never re-enters Intake or automatic recovery. The workflow does not
create an issue, branch, worktree, or task directly and does not copy their
owners' selection, recovery, confirmation, executor, or checker behavior.

The pre-selection identity check is scoped to the current workspace and the
requested Issue, not the repository-wide active-task inventory. Unrelated
`in_progress` tasks, including tasks owned by the same user, do not prevent
`guru-select-workflow-mode` and do not justify asking the user to select an
unrelated task or use task-free. A checkout path or old mapping is not a task
binding. Validate the exact TaskId/generation and resolve an unfinished task
for the same Issue before selecting new work; incomplete or conflicting
relevant identity remains fail closed. An archived incomplete closeout blocks
only when live task, branch, PR and lifecycle facts bind it to the current
identity. Old in-flight Finalizer residue is a legacy stop, not a current task
route. None of these relevance checks permits mutation or cleanup.

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
pause before `guru-activate-task` activates a planning task or resumes an
in-progress replan. The same approved consumer selects `activate` or
`resume_execution` from live lifecycle after the current pair guard. Only first
activation changes status; active resumption preserves identity, branch,
checkout and `in_progress`. Questions, revision
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

### Phase 3 — Delivery cycles and task completion

Mandatory invoke `guru-create-task-commit`, then independently review the
complete committed base-to-HEAD diff with `guru-review-branch`. A checked
`passed` enters the active-task pair guard and Delivery Review. The Delivery
Review owner checks one independently deliverable slice and authors the exact
Chinese PR title/body with `Refs` only, including when the target is the
default branch. It discloses remaining task work and unverified boundaries;
task-content findings return to Phase 2 and affected downstream gates.

Only `guru-review-task-delivery:ready` enters `guru-publish-task-delivery`.
That owner controls the reviewed HEAD push, current Draft/Ready PR, bounded
side-effect confirmation, and same-plan recovery. Only its checked
`ready_for_merge` enters `guru-merge-task-delivery`, which requires a separate
expected-head merge confirmation. Its `delivered` result is one Delivery, not
whole-task completion, Issue closure, archive authority, or cleanup permission.
Lost outputs return to the original producer against current exact identity;
they do not create duplicate PRs or merges. No retired Finalizer or Restore
path is a current consumer.

Mandatory invoke `guru-review-task-completion` after a checked Delivery result.
It rereads the entire accepted scope, all applicable Deliveries, current
requirements and evidence. Incomplete results keep the same task active and
route to the earliest affected owner, evidence refresh, or next Delivery
planning; only `completed` enters `guru-complete-task-closure`. Closure alone
decides and, where applicable, separately confirms the exact source Issue
mutation. No-Issue, reference-only, follow-up and parent dispositions use
`no_mutation`; neither Delivery nor bookkeeping PR closes an Issue by keyword.

After Closure, fresh `task_impact_sync(stage=acceptance_finish)` gates
`guru-finish-task`. Finish alone persists the terminal archive through its
reviewed local archive and bookkeeping Git/GitHub boundaries. Only verified
success on the target baseline enters `guru-cleanup-task-resources`, which
reviews exact owned resources and requests its own confirmation. Partial
cleanup does not undo Completion, Closure or Finish. The global workflow
never invokes package-private closeout scripts directly.

### Active-task continuation authority

For an exact current task, the active workflow's single non-empty
`[trellis-continuation]` block is the only detailed continuation authority.
`task.json.status`, Phase Index text, `[workflow-state:*]` breadcrumbs, platform
entries, hooks, prior conversation text, and private checkpoint names provide
facts or broad lifecycle guidance only. They must not maintain another route
table or infer a semantic pass. `planning` and `planning-inline` share one Phase
1 matrix; `in_progress` and `in_progress-inline` share one Phase 2-to-Completion
matrix; `completed` resumes the current Finish or Cleanup consumer; invalid identity or an
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
dialogue-local plan acceptance, and activation. `guru-activate-task` performs
the status-only transition once after current approval and confirmation; lost
output is recovered through `recover_activation` for that same first operation.
An active replan uses `resume_execution`, and only its completed lost result
uses `recover_execution`. The single continuation block handles pending replan
approval/presentation before ordinary Phase 2 continuation. Semantic output
loss returns to the original producer; unavailable dialogue acceptance is
obtained again, never stored. The execution owner's short-lived completed
result is retired after a current Check passed projection. Existing later-stage
continuation never restarts activation merely because that result is absent.
None of these paths persists confirmation or writes legacy branch metadata.

When task creation succeeded but its `created` output was lost, return to
`guru-create-task` read-only result recovery for the exact TaskId/generation.
It may rematerialize only the checked `created` result, never create a second
Issue, branch, worktree or task. Issue creation output loss belongs to the
separate `guru-create-issue` owner and returns through fresh Intake.

For Phase 2, a current retained `passed` checkpoint may be checked again and
projected through the existing checker-to-`invoke-guru-check-task` path. This is
rematerialization through the existing public invocation, not a new public
recovery profile, exit, schema, or semantic judgment. If that checkpoint is
missing or stale, fresh Phase 2 Architecture and `guru-check-task` are required.
Task Commit output loss uses the existing `guru-create-task-commit` same-
candidate `recovery_resume` contract and may not create a second candidate,
empty commit, amend, or duplicate commit. Lost Branch Review or Delivery Review
DTOs require fresh Architecture at the matching stage and a fresh semantic
owner run. Delivery Review's original owner determines whether its still-held
checked Branch Review anchor remains applicable; normal checkpoint retirement
alone does not invalidate that DTO. Loss of Delivery Review output does not
mechanically rerun unaffected upstream owners. New committed content still
requires a complete current exact-range Branch Review.
Delivery Publish/Merge recovery belongs to the original owner and
current PR/HEAD transaction. A current checked Delivery result enters
Completion; evidence-only changes use Completion's evidence-refresh entry,
not a fabricated Delivery. Closure, Finish and Cleanup retain their own
generation-bound recovery and consumers.

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

Current side-effect boundaries are distinct: new Issue creation when needed,
task creation/checkout, Phase 1 plan acceptance and activation, Task Commit
when not already exactly requested, Delivery push/PR, Delivery merge,
post-Completion source Issue closure when applicable, Finish archive and
bookkeeping, and Cleanup. Each owner displays its current exact action and
obtains confirmation where required by its contract; an earlier confirmation
does not authorize a later action. Task activation after accepted Planning,
implementation, Phase 2 check, Branch Review, mapped exits and read-only
recovery add no second routine confirmation. Branch classification, protection,
sharing, ownership and PR state are facts, not operation authority.

The canonical workflow retains five `guru-confirmation-boundary` marker IDs
for historical #174 replay compatibility. In particular
`finalizer_side_effect_set` names a retired profile; it does not route to a
Finalizer or define the current lifecycle's confirmation count. Use the
current owners' plans and exits for production authorization.

## Docs SSOT And External Work Items

Every planning cycle chooses one Docs SSOT strategy:
`ssot_first`, `delta_first`, `bootstrap_or_repair_docs`, or
`no_docs_update_needed`. Phase 2 executes that decision; Branch Review verifies
the final reconciliation but must not perform the first merge.

Delivery Review owns each slice's Refs-only PR payload, even for an Issue-backed
Delivery to the default branch. Publish and Merge do not close the source
Issue. Completion owns the whole accepted-scope judgment; only its `completed`
result enters Closure, which reviews the exact source Issue disposition and
performs a separate confirmed close when applicable. No-Issue, reference-only,
follow-up and parent relationships produce `no_mutation`. Finish's bookkeeping
PR is likewise Refs-only. PR merge, Issue state and archive presence never
substitute for Completion or Closure.

Before a planning, Phase 2, Branch Review, Delivery, Completion, Closure, or Finish stop, resolve the
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
boundaries are plan approval before activation, Phase 2 pass before Task
Commit, Task Commit before Branch Review, Branch Review before Delivery Review,
and Delivery Review readiness before Delivery Publish.

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
Branch Review, or Delivery Review. For post-Branch Review and post-Delivery
Review profiles, a compatible candidate that changes the shared
reviewed-content identity uses `review_continuity_required`: after semantic
judgment and an exact current-dialogue Git confirmation, the reconcile owner
creates one persistent local reconciliation commit bound to expected task/base
HEADs and the reviewed candidate tree. Bounded continuity separately binds the
prior complete review commit and that current commit, then projects the current
commit as Delivery Review's reviewed-content anchor. The retained
`post_publication` and `finalizer_base_mismatch` profile IDs are historical
compatibility identifiers: the former serves the current post-Delivery Review
boundary, while the latter creates no Finalizer production route. A base-only
change is not a Delivery Review content-staleness finding.

## Public Entry And Recovery Routing

Each current package's Interface-declared public invocation is the normal
entry; component record/check/execute commands remain diagnostics or bounded
recovery, not an alternate workflow. Task Commit keeps its reviewed
`prepare-task-commit` and `invoke-guru-create-task-commit` entry. Delivery
Review, Publish and Merge, then Completion, Closure, Finish and Cleanup use
their own current public contracts and mapped exits. A command may reuse
facts only for one current authority identity and mutation boundary. Recovery
may consume a mapped same-plan result only after the original owner proves
the side-effect set unchanged; material scope, payload, HEAD, authority or
action changes invalidate prior confirmation and return to semantic review.
The workflow does not invoke retired Publication/Finalizer/PR Merge wrappers.

## Post-Delivery Task Lifecycle

The five post-Delivery owners are active production consumers, not deferred
packages awaiting cutover. A Delivery merge, PR readiness, deployment, passing
test, closed Issue, or archived directory never implies Task Completion.

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

`guru-cleanup-task-resources` consumes current Finish `success` or its declared
`manual_cleanup_required` handoff. It
freshly reviews the exact owned branch, worktree and ignored runtime resources,
requires an independent confirmation, and preserves every previous lifecycle
result when cleanup is partial. A Reactivate invalidates the prior Finish
receipt, so old success cannot delete current resources.
If the terminal resource ledger is missing, manual selection also requires the
exact same-generation manual Finish result from the common-dir store; archived
status alone does not authorize resource deletion.
For a noncanonical legacy active task, Closure may freeze a freshly reviewed
non-exact source without a metadata-only write. Finish consumes that frozen
source and materializes it in the required archive metadata mutation.

`guru-reactivate-task` handles only a normally finished original task. It
preserves TaskId, source and accepted scope, verifies archive/base identity,
increments the lifecycle generation and establishes a current branch/checkout
binding. Its normal exit returns to Planning; session recovery, same-transaction
resume and legacy source correction use their declared consumers. It never
creates a replacement task, reopens an Issue, or treats prior
Completion/Closure/Finish as current approval. An old in-flight Finalizer
residue is not a normally finished archive: inspect exact task/PR/local/remote/
base facts, then use a pinned compatible old version or explicit per-case
manual disposition. Never adapt old Publication/Finalizer/Merge/Restore DTOs
into new Delivery or Completion results. `archived_review_passed` stops at
`legacy-archived-review-disposition-required` in the current graph.

## Root-Cause Global Routing

Global workflow explicitly invokes guru-qualify-root-cause after normal/solution outcomes for the ten current candidate profiles. Three root routers return to original owners; root stop consumes a concrete reason. Step-local semantic admission and reuse remain package-owned. #383 retains common completion ownership.
