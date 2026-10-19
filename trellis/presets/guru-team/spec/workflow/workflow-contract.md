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

- phase order and the public Task/Delivery availability router;
- one mandatory invocation marker per active stable `guru-*` Skill id;
- every declared typed exit and its single consumer;
- workflow targets, fail-closed stops, and automatic mapped re-entry;
- tool-free initial request classification;
- workspace/task boundary selection and Delivery activation;
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

## Candidate Applicability And Coverage

This section is the single shared rule for Architecture, Check, TaskCommit,
Branch Review, Delivery Review, Publication, Merge and their continuation.
Each original owner applies it within its own responsibility and produces its
own current formal result. It adds no Skill, phase, public field or evidence store.

Keep three kinds of evidence distinct:

- Engineering execution facts are actual command results for specific checked
  inputs, dependencies, toolchain, environment, parameters, check definition
  and expectations. They may remain applicable after a candidate changes.
- Semantic judgments are an owner's actual conclusions about its current
  responsibility and exact candidate. An old pass never supplies a new pass.
- Git/PR facts identify commits, trees, ranges, payloads and remote outcomes.
  Read current facts for the action; they do not prove semantic coverage or
  engineering execution.

### Original coverage and current judgment

The first candidate requires a complete independent review. Planning and
implementation self-checks do not replace it. For a later candidate, the
original review owner reads verifiable original coverage, the entire actual
delta and affected dependencies, including unchanged consumers. It states
what remains applicable, what no longer applies and what it supplemented.
Original coverage plus that reviewed delta and affected dependencies must
cover the complete current fixed-base-to-HEAD range. The owner then judges
the current candidate and uses its original recorder/validator/public entry.
This applies to normal integration, finding fixes and other content changes;
the narrow promotion-reference-alignment profile retains its own input limits.

Use only actual retained public Task/Delivery results or public invocation
objects, exact Git objects and ranges, current bodies, and verifiable original
command results. A passed public full_review can locate its formal coverage
through candidate, scope, plan, outcome and predecessor. A planning AuthorityRef
does not establish command execution. If rework cleared a result slot, use a
still-held actual public output or its original producer's supported recovery.
Never read another owner's private checkpoint, reconstruct retired private
state, or add a permanent review/test ledger, transcript or digest chain.

An initial implementation_required has no passed full_review. Its commit and
finding refs locate facts and defects; they do not prove passed coverage.
Any original complete review work used for the next judgment must remain
verifiable through actual public results/invocation objects, Git and current
bodies. Retained reviewer understanding can reduce repeated reading but does
not create authority. Supplement missing coverage; perform a complete review
when the combined effect cannot be bounded. Neither a missing checkpoint nor
a new reviewer/session alone invalidates otherwise verifiable coverage.

Independence means that the reviewer has not authored or implemented the
candidate under review. Keep the Architecture contract's first independent
read order. A compliant independent reviewer may perform Architecture and
then Branch Review, or continue a later candidate. When no new Architecture
fact requires reassessment, do not dispatch another reviewer merely to rebuild
the same understanding. Each stage still personally judges applicability and
produces its own required formal result. An author cannot approve their work.

After a finding fix, verify closure, the fix delta and affected coverage.
The original compliant reviewer may complete the current final judgment;
there is no unconditional distinct-reviewer or identical full-review rerun.
Closure alone is not passed. Existing finding anchors, ancestry and current
result binding remain required. The retained `fresh_final_review` wire value
has the explicit successor meaning and matching-install boundary in
MIGRATION-637; it is not permission to silently reinterpret an old installation.

### Engineering fact applicability

Before inspecting prior results, determine the current complete scope, risks,
affected consumers and applicable check set. Adopt an original engineering
result only when accessible and verifiable and its inputs, actual dependencies,
toolchain, environment, invocation parameters, check definition/version and
expectations remain applicable. Reviewer, stage, commit or promotion changes
alone do not require command repetition. A matching path or tree is insufficient.

Run each new or affected check when any input changed, applicability is unknown
or the original result is unavailable. Preserve unaffected verifiable facts.
In existing summary/evidence fields distinguish current execution from adoption,
with the original source, checked object and applicability reason. Never claim
to have executed an adopted command. Complete every current semantic dimension
and report required evidence gaps through the original owner routes. A legal
configuration change is an affected-check input, not an old-value correctness
whitelist; judge usability through appropriate actual integration/E2E execution
under the current profile. Execution-result updates or added external evidence
alone do not redefine the candidate or start identity recomputation loops.
Keep the existing exact-candidate checks, including Task metadata, intact.

### Candidate and action boundaries

A same-tree commit only refreshes necessary commit/candidate binding. It does
not establish unchanged tools, environment or required checks. Review navigation,
version and reference changes for their actual behavior; document suffixes do
not grant exemptions. For conflict resolution, read both sides, the combined
semantics and affected unchanged consumers, rather than only conflict lines.
An unrelated target advance does not replace the fixed review object or require
integration. Real scope, design assumptions, authority or dependency changes
return to the earliest affected original owner.

Delivery Review, Publication and Merge consume applicable content review and
judge their own current payload, Issue semantics, candidate and live facts.
They do not repeat unchanged business-design review. Required checks, expected
HEAD, remote transaction readback and each side-effect boundary remain intact.
Same-Delivery recovery uses the original producer and actual public identity;
it requires no new Delivery, empty commit or proof ledger. See
[MIGRATION-637](https://github.com/castbox/guru-trellis/blob/main/trellis/presets/guru-team/MIGRATION-637.md) for matching installation
and in-flight recovery; source edits never hot-migrate an active installation.

## Native Reference And Guru Route Ownership

Upstream bundled `trellis-meta` references are provider-owned and are not
preset overlay targets. They describe generic Trellis facilities; older
candidate references can still name retired Guru Task activation. For a Guru
Team operation, load the installed `.trellis/workflow.md`, current package
registry and this contract before selecting a route. Generic Task start or a
historical bundled reference cannot supply Planning approval or activation.
The current workflow selects `guru-create-delivery` and
`guru-activate-delivery`; public model and transition details remain solely in
upstream `.trellis/delivery-contract.md`. Do not patch bundled references or
introduce a substitute model to reconcile an old route. Report provider
reference drift separately from verified Guru platform-entry behavior.

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

The current source registry has 38 active packages, 187 package exits, and 114
commands. The business-task workflow declares 36 mandatory invocations and 180
external exits; `guru-verify-extension-installation` and
`guru-upgrade-installation` are standalone-only. These
counts are checks against the live registry and workflow markers, not an
alternative routing authority.

The production spine is `guru-sync-base` -> context/clarification/wording/
change-request review -> `guru-create-issue` for a proposed draft (then fresh
Intake) or `guru-create-task` for an existing Issue/standalone request ->
identity/binding/checkout/session resolution -> Task scope -> `guru-create-delivery`
-> per-Delivery Planning and `guru-activate-delivery` -> Phase 2 check -> Task Commit -> independent Branch Review -> Delivery Review
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
or test. Phase 2 assesses the complete candidate and proposed Architecture delta
after Docs reconciliation. The original Architecture owner promotes the
reviewed delta and verifies actual-write applicability before final Check.
Branch Review forms its own current conclusion over the complete committed
range, including promoted files and pre-promotion authority. Apply Candidate
Applicability And Coverage to original coverage and actual delta; a Phase 2
result cannot replace the Branch Review-stage result.

Every fresh `baseline_current` binds `constitution_status=current`, an existing
regular project-owned constitution locator, and its exact source profile. Only
`source_profile=delivery_task_impact_sync` may resume a Delivery stage with its
same DeliveryKey and planning root; Task-only acceptance/finish uses
`source_profile=task_impact_sync`. `delivery_bootstrap_foundation|delivery_repair`
reruns `delivery_task_impact_sync(stage=<affected-stage>)` with that same key and
root. Task-only `bootstrap_foundation|repair` reruns the matching
`task_impact_sync` call. `source_profile=delivery_promotion|promotion` returns to
the original Architecture owner for actual-write applicability and its matching
final Phase 2 result. A consistent write does not dispatch the same independent
assessment again. The resulting complete candidate enters final Check, Task
Commit and independent committed Review. Missing or stale Architecture evidence,
`architecture_conflict`, `contract_incomplete`, or `fitness_regression` cannot
reach Delivery Review. Stale baseline, constitution, contribution,
expected-current, or stage identity returns `sync_required` to the Architecture
owner. Completion/Finish requires `reviewed_promoted` for a long-term
Architecture change or a current `no_change` proof. This is routing-only
integration; Delivery, Completion, Closure and Finish retain their package-owned
judgments.

The matching nonplanning 4.0 / Delivery 2.0 Architecture current result carries
`before_authority` and `candidate` to this existing current router. The router
preserves them for the original stage owner to read the actual comparison origin
and final candidate; it does not interpret private project checks or decide
applicability. Planning 3.0 and bootstrap/repair keep their declared contracts.

After a full Review, the original Branch Review owner alone handles
`delivery_promotion_reference_alignment`. Its formal `passed` covers the final
candidate by reviewing all source/status alignment delta and dependencies while
retaining a recoverable original complete Review. This narrow profile is not
Git continuity. Missing proof or changed obligations return through the
affected original owner. Completion/Finish never repeats an accepted promotion
or adds baseline prose solely to record final Review/HEAD.

### Workflow mode selection and Phase 0 — Issue-backed intake

Classify the user request before repository/network semantic reads. A
change-intent request that has not already entered an active-task route invokes
`guru-select-workflow-mode`, including proposed-change requirements discussion,
feature design and planning with deferred writes/resources. Method loading
does not replace the actual selection or Clarify entry from current Discovery. An Issue-backed or task-like request that only asks
for information, such as checking an Issue's current status, remains a
information-only direct answer. The selector's `standard_intake` exit enters
`guru-sync-base`, then automatically follows the public graph through current
context discovery, requirements clarification, wording review, change-request
review, and the `guru-task-intake-router`. Its `task_free` exit enters only the
bounded task-free edit owner, which determines linked non-base execution before the first write.

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
active Tasks, including Tasks owned by the same user, do not prevent
`guru-select-workflow-mode` and do not justify asking the user to select an
unrelated task or use task-free. A checkout path or old mapping is not a task
binding. Validate the exact TaskId/generation and resolve an unfinished task
for the same Issue before selecting new work; incomplete or conflicting
relevant identity remains fail closed. An archived incomplete closeout blocks
only when live task, branch, PR and lifecycle facts bind it to the current
identity. Old in-flight Finalizer residue is a legacy stop, not a current task
route. None of these relevance checks permits mutation or cleanup.

Every change-intent request not already routed through an active task invokes
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

Task-free mode never establishes a Task identity. Its existing execution owner
handles linked non-base location acquisition and suitability; isolation alone
does not select standard Intake. The Guru workflow caller consumes actual
upstream no_current_task into fresh no-Task routing without modifying upstream
entries. Native caller delivery remains distinct from serializer evidence.
New formal Task primary rejection belongs only to create preparation; existing
primary recovery, clean acquisition, Sync and Cleanup retain their owners.

### Phase 1 — Planning

The #531 source candidate directly evolves the delivered #292 Author contract:
one scope-only profile writes Task root requirements, while eight Delivery
profiles write the public planning_root. Matching package Interfaces and thin
projections must be reviewed and installed together. Existing development Tasks
keep their complete installed runtime; source import is not runtime cutover.


The canonical workflow delegates planning business writing to mandatory
`guru-author-task-plan`. Its scope_requirements_ready enters original Clarify
task_scope_requirements_acceptance for actual scope publication; pre-publication
scope_ready returns to scope-only Author writing. Accepted scope then routes to
explicit Delivery Creation, affected rework/exit, or Completion by current
obligations. No Task solution-planning state or automatic empty Delivery exists.
The same Author's Delivery profiles own their three planning documents and
official planning JSONL. Their `requirements_ready` enters the original Architecture
owner's planning `candidate_assessment`; that current result returns to Author
for solution writing. Author `plan_ready` enters Wording, whose planning pass
enters Architecture `final_plan`; only that current result enters adjacent
Approval. The packages own their local contracts, including source-design
disposition, Delivery Policy and Docs SSOT Plan. Automatically consume each
declared typed exit. Task scope is distinct from the per-Delivery plan. The first and subsequent
Delivery are created/selected through `guru-create-delivery` before the existing
unique Author writes their public planning_root. D2 never replaces D1 artifacts.
Wording, Architecture and Approval retain separate judgments over that exact plan.
Only current approved output enters `phase-1-delivery-activation`, which presents
the complete plan and invokes `guru-activate-delivery` after the current dialogue
boundary. No base-pair observation is required. No Task planning/in_progress writer remains.
Same-Delivery rework uses the same owner rather than first/subsequent activation.
The exact profiles and output-loss recovery are step-local package contracts.
Questions, revision requests, partial choices and ambiguous replies remain
paused. Material plan changes re-enter the earliest affected Author/dependency
and repeat current Wording, final Architecture and Approval before presentation.
Explicit autonomous execution omits only the ordinary unchanged-plan pause;
scope, authority, material design or risk changes retain their existing boundary.

Read the canonical [#531 migration boundary](task-delivery-migration.md)
for old schema/DTO retirement and cutover; current phase or files never prove
semantic approval. No recorder stores dialogue acceptance. No earlier creation
or old plan confirmation accepts materially changed planning.

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

The final Check-bound path reaches `guru-create-task-commit` only through
`guru-check-task:passed`. The early Draft path explicitly invokes the same
TaskCommit and Publication owners through their independent profiles and five
workflow-owned Draft routers. Finding and
planning-stale exits return to their declared consumers automatically. The
workflow does not reproduce Phase 2 adequacy dimensions, severity rules,
recorder/checker commands, or private evidence shape.

### Phase 3 — Delivery cycles and task completion

Mandatory invoke `guru-create-task-commit`, then independently review the
complete committed base-to-HEAD diff with `guru-review-branch`. A checked
`passed` enters Delivery Review directly. The Delivery
Review owner checks one independently deliverable slice and authors the exact
Chinese PR title/body with `Refs` only, including when the target is the
default branch. It discloses remaining task work and unverified boundaries;
task-content findings return to Phase 2 and affected downstream gates.

Only `guru-review-task-delivery:ready` enters the final Ready Publication
profile. Early task/key/B/H enters the independent Draft profile; return-to-Draft
uses the original publishing revision owner and lawful rework.
That owner controls the selected HEAD push, current Draft/Ready PR, bounded
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

For an exact current Task, the active workflow's sole non-empty
`[trellis-continuation]` owns routing. Resolve current public Delivery selection,
phase and evidence through the installed upstream contract, independently of
Task identity/resource bindings. No inventory guessing, Task-status route,
private checkpoint route table or competing native gate is allowed.

Continuation first distinguishes a current adjacent public DTO from lost
output. A still-current adjacent DTO goes directly through its Interface-
declared projection to the unique consumer. A lost DTO returns to the original
producer: deterministic mutation/output loss uses only that producer's formal
recovery or rematerialization, while a semantic result is rerun fresh by its
semantic owner. Missing checkpoints, clean Git state, commit messages, task
status, old summaries, and earlier confirmation are never substitutes.

Planning preserves the original Author, source selection and both
purpose-bound Architecture producers. Incomplete plans and lost source selection
return to their original producer; a legitimate branch rebind never replays
initial creation. Wording and final_plan precede fresh Approval.
Adjacent current public DTOs use their Interface projection. Missing outputs
return to their original semantic or transaction producer. Commit/publication/
merge facts survive affected gate rework; their existence does not prove pass.
No-current Delivery legitimately supports scope revision, an explicit first/next
slice, Completion evidence/validation or closeout. It never uniformly creates
an empty slice. D1 and D2 follow the same owners. Ordinary method checks do not
write formal phases. The public runtime declaration supplies unique writers;
platform entries and breadcrumbs only load the sole continuation.

When task creation succeeded but its `created` output was lost, return to
`guru-create-task` read-only result recovery for the exact TaskId/generation.
It may rematerialize only the checked `created` result, never create a second
Issue, branch, worktree or task. Issue creation output loss belongs to the
separate `guru-create-issue` owner and returns through fresh Intake.

For Phase 2, a current retained `passed` checkpoint may be checked again and
projected through the existing checker-to-`invoke-guru-check-task` path. This is
rematerialization through the existing public invocation, not a new public
recovery profile, exit, schema, or semantic judgment. If that checkpoint is
missing or stale, the original Phase 2 Architecture and Check owners perform
their current invocations under Candidate Applicability And Coverage.
Task Commit output loss uses the existing `guru-create-task-commit` same-
candidate `recovery_resume` contract and may not create a second candidate,
empty commit, amend, or duplicate commit. Lost Branch Review or Delivery Review
DTOs require fresh Architecture at the matching stage and a fresh semantic
owner run. Delivery Review's original owner determines whether its still-held
checked Branch Review anchor remains applicable; normal checkpoint retirement
alone does not invalidate that DTO. Loss of Delivery Review output does not
mechanically rerun unaffected upstream owners. New committed content still
requires a current exact-range Branch Review under Candidate Applicability
And Coverage; it does not unconditionally repeat original covered work.
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

Ordinary chat is the default channel for confirmations, real choices and
necessary clarification. Honor an expressed preference for prompt interaction.
The availability of a structured question tool is not a requirement to use it.
Use a structured question only when the user requests that channel or a higher
platform constraint requires it, and only for uses allowed by that tool. An
unanswered question, a preselected option or elapsed waiting time is not an
answer or authorization.

Interpret clear natural-language replies against the current question and its
fully displayed plan. When the current conversation already requests or
confirms the exact action under its owner's contract, consume it through that
owner's execution and validation path; do not switch channels to require a
button, identity restatement or another confirmation of the same action.

Text and button answers belong to the question and plan they answer. A late or
repeated answer to an action already confirmed or completed does not execute it
again and does not authorize a subsequent independent action. Resolve that
relationship in the current dialogue, using the original question and current
execution facts; do not rebind an old answer to a newer pending question. Avoid
leaving both a chat question and an optional structured question pending for the
same choice. Do not create an authorization record or question-state store.

Agent-authored questions are distinct from mandatory platform permission,
sandbox or external-action approvals. When the platform requires approval,
explain its source and corresponding action and follow that requirement. This
contract does not remove or bypass platform approvals; their appearance alone
is not evidence of an extra Agent-authored confirmation question.

Automatically consume mapped typed exits, stale/re-entry/reprepare routes, and
recorder/validator steps. Do not simulate a human approval chain and do not
persist authorization state, text, refs, digests, or process.

Current side-effect boundaries are distinct: new Issue creation when needed,
task creation/checkout, Phase 1 plan acceptance and activation, Task Commit
when not already exactly requested, Delivery push/PR, Delivery merge,
post-Completion source Issue closure when applicable, Finish archive and
bookkeeping, and Cleanup. Each owner displays its current exact action and
obtains confirmation where required by its contract; an earlier confirmation
does not authorize a later action. Delivery activation after accepted Planning,
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

## Fixed Development Baseline And Actual Integration

Development baseline, Delivery content range and PR target are separate facts.
The implementation owner retains the selected Delivery content base B, binds
actual implementation HEAD H and full B..H paths through begin_check. D2 derives
B from actual preceding delivery_result heads; same-Delivery recovery uses its
own candidate. No fetch, integration candidate or synchronization is required
to obtain a range. The Task's complete accepted scope remains Completion's duty.

Planning, Activation, Check, TaskCommit, BranchReview, DeliveryReview/Publish,
Completion and Finish have no default pair guard/Reconcile edge. The current
owner invokes guru-reconcile-task-base only for an actual conflict, a concrete
required-check integration failure, an existing server-required update already
observed by Merge, an explicit dependency/requirement or user-requested sync.
Behind/latest target SHA alone does not qualify. No Ruleset query gate is added.

An actual operation pins its integration target OID separately from content B.
Its six declared exits retain their unique consumers. The phase2 resume target
means bounded reentry through implementation and Check for the actual delta
and affected dependencies. A real prior Check/full_review remains historical;
new candidate applicability rejects it until the original owners actually judge
coverage and record new results. Prior complete Review plus independently
reviewed resolution delta may cover B..Hi; missing complete Review still
requires the first full Review. Do not relabel continuity, manufacture gates,
repeat unrelated tests, or create another empty/same-content TaskCommit.

In-flight stages retain explicit applicable authority and fixed candidates.
Unrelated CURRENT/navigation/archive/remote-ref advancement cannot replace
these objects. Actual task-applicable authority, scope, dependency or solution
changes return to their original semantic owner. Shared-current promotion
still validates its own expected-current write boundary.

Merge observes actual GitHub eligibility/checks and uses expected task HEAD;
terminal verification uses actual parents/message/merge identity and current
target reachability. Finish preserves the same exact bookkeeping transaction
across unrelated target advances. Completion consumes bounded historical facts
only for their stated coverage, supplements missing task Delivery facts, and
rejudges affected conclusions. #569 alone owns history-query preparation.

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
`no_mutation`. An exact-source relation may also produce reviewed `retain_open`
with a no-mutation result; the step-owned disposition and matching consumer
contract live in `guru-complete-task-closure` and `guru-finish-task`.
Closing one exact source Issue is a separate confirmed provider
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

## #250 Intake profile routing

The current global route retains Sync → Discovery → Clarify. Clarify owns six
profiles and source authority; Discovery's context_ready returns the original
four context-capable profiles using Interface 1.8 handoff_profile projection.
Current Planning consumes adjacent minimal source_selection after task identity
resolution, rereads selected sources, and owns final design dispositions. Lost
selection returns to original Clarify/context. Upstream brainstorm remains a
discoverable method constrained by the Guru owner, never a second workflow.

The global initial classifier distinguishes information-only questions about
existing facts from proposed-change requirements/design/planning intent. Deferred
file writes or resource creation preserve that intent and its current Guru route.
See the marketplace workflow Guru Team Gate for the single routing definition.

## #292 active-scope boundary

Clarify owns accepted scope before the original Author writes planning.
Current active private result is 4.0; scope_ready public output and the original
clear-router's independent consumer input are 1.0. The output is exactly
exit_id/mode/task_ref/source_selection/revision_refs. The thin router drops
exit_id, adds fixed profile=active_task_scope_change and passes the remaining
fields unchanged to Author's existing input 1.0. AI chooses revision_refs from
actual revisions; scripts do not infer them. Updated planning, planning hashes,
reentry owners and active_task_scope_update are not Clarify prerequisites.
Original Sync/Discovery still handles source mutation or missing context.
Original activation/resume_execution retains TaskId/generation and in_progress.
Historical private3.0/public-clear3.0/clear-consumer2.0 bytes remain unchanged;
old successful active results require fresh original Clarify, while other
profiles keep their contracts. This migration does not imply native semantic,
fixture resume, full installer-matrix or release qualification.

## Independent maintenance routing

Explicit tools-only and selected legacy Task maintenance load their standalone source packages before old target preflight; they do not enter standard Intake or infer a task from inventory. The original history/control owner exits return through their unique thin selected-maintenance consumers. Only verified target-native current continuation resumes the original lifecycle owner. History-retention stops without Completion/Closure/Finish. Full Plan2 and ordinary current-only remain separate contracts.


## Manual archive resume (#577)

Manual historical archive resume enters the existing standalone maintenance owner archive_resume profile. Formal Finish archives still enter Reactivate; unfinished Closure/Finish/Finalizer work returns to its original owner. Only actual installed identity/checkout/binding/session, target-native continuation and next semantic-owner validation may resume current execution.

## Early Draft routing (#636)

The canonical workflow uniquely consumes draft_committed, draft_published,
draft_revision_ready, draft_content_reviewed and draft_revision_required. It
explicitly invokes original TaskCommit, Publication and early Branch Review;
profiles and internal behavior remain package-owned. Draft feedback dispatches
independent fixed B/H content analysis and implementation/Check-owned HEAD
validation in parallel. Final Check, formal full_review, readiness and Merge
remain mandatory. Target advancement, conflicts and absent merge refs do not
block the supported HEAD entry; target/integration evidence stays separate.
Current continuation uses public phase plus original-owner transaction readback,
never Draft as gate authority. See task-delivery-early-draft-migration.md.
