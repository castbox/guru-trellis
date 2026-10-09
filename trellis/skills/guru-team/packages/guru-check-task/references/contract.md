# Guru Check Task Contract

## Ownership

`guru-check-task` is the sole semantic owner of the complete Phase 2 check. It
uses `judgment_mode=semantic`. Official Trellis workers and repository commands
provide ephemeral evidence; they do not own the Guru result and do not create a
handoff, assignment, liveness record, or raw review artifact.

Workflow and standalone mode use the same owner loop. Any real side-effect
authorization remains only in the current conversation and is never recorded.

Every official implement, check, research, channel-runtime, or review worker is
invoked with a prompt that authorizes approved-plan work only. A
planning-external observation stops that worker before any edit, added test,
self-fix, severity, classification, or route. Its complete invocation-local
candidate shape is `candidate_ref`, `observed_behavior`, `locators`, and
`minimal_reproduction_hint`; it is ephemeral input, not a worker-owned finding
or handoff. This owner rereads the live evidence and completes fresh
`phase2_candidate_set` qualification before continuing or redispatching work
for that candidate. Official `trellis-*` agent files remain unchanged and
upstream-owned.

## Public Entry

### Execution Order

The current AI executing this package is the contract-selected semantic owner.
Do not wait for another owner, worker, subagent, agent ID, or pre-existing result.
Workers may supply evidence but their absence does not remove your ownership.

1. Load the complete package contract and the selected public input schema.
2. Read the current task, approved `prd.md`, `design.md`, `implement.md`,
   live Issue authority, complete diff and dirty paths, implementation, tests,
   Docs SSOT, fresh Phase 2 Architecture result, and actual validation evidence.
3. Execute the Semantic Loop below yourself, including qualification and all
   nine adequacy dimensions. Judge the outcome from the evidence, not from a
   desired exit.
4. Author the minimal semantic content described under Recorder Authoring.
5. Call the original recorder, checker, and public wrapper in that order.
   These commands record and validate your completed judgment; they cannot
   perform it or authorize it.
6. Consume exactly the wrapper's declared typed exit. Only `passed` can enter
   Task Commit; follow each other exit's existing unique consumer.

The internal state `owner_not_yet_executed` means continue steps 2-4 here. It
is not an external exit. A genuinely missing authority, Architecture result,
or mandatory validation is a concrete evidence gap, not a missing AI owner;
use the existing Architecture route or `blocked`, never invent a pass.
Schema, identity, freshness, or path errors end that invocation with their
original diagnostic. Reread current facts and perform a fresh semantic round
before invoking again; do not relabel the error as missing external ownership.
Only an observed failure of the platform's required read or formal execution
capability can justify an execution blocker. Worker dispatch failure alone
does not prove such a platform failure.

Public input schema 2.0 is a minimal route DTO:

- `initial_check` identifies the current implementation-complete entry;
- `finding_fix_rerun` carries only the finding references whose fixes require a
  complete current-scope rerun;
- `planning_reentry` identifies a refreshed planning route.
- `resolved_reconciliation` identifies a conflict-resolved merge tree that has
  returned from implementation and must pass fresh Phase 2 before Reconcile may
  create the local merge commit.

The caller does not submit semantic conclusions, findings, raw evidence, an AI
gate, or an exit. Eval cases likewise choose a staged semantic case outside the
public input and assert the actual exit only after the owner result returns.

## Architecture Stage Consumption

The global workflow mandatory invokes
`guru-maintain-architecture-baseline:task_impact_sync(stage=phase2)` before this
owner can select `passed`. The Architecture owner rereads the current baseline,
design constitution, project change-contract identity, task-local Architecture
change contract, and applicable project Architecture check results. This Skill
consumes only the checked current route and the live authorities; it does not
read Architecture private state or repeat applicability, contribution, ADR,
promotion, or typed-route judgment.

The Architecture contract selects a fresh independent reviewer over the
complete tracked/untracked candidate before task narratives. The same fresh
worker may execute this Skill only after completing Architecture and then
reading the whole task; its two actual results remain separate. A worker
already exposed to narratives or implementation cannot backfill that review.

Phase 2 uses that stage result to perform the first semantic before/after review
of the complete worktree candidate. Applicable project checks must be current;
mandatory `fail` or `unverified` evidence remains blocking. New or worsened
deviation, owner expansion, dual writer, compatibility without an exit, or a
closed-GAP recurrence routes as `fitness_regression` to implementation/check.
Missing applicable facts route as `contract_incomplete`, authority conflict
returns to Planning, and stale baseline/constitution/contribution identity
returns `sync_required` to the Architecture owner. None can be converted into a
Phase 2 pass by this consumer.

After `implementation_discovery` qualification, any expansion of scope, risk,
owner, state authority, persistence, SDK lifecycle, external integration, or
another architecture boundary makes the Planning Architecture result stale.
The coordinator stops before the expanded edit or test and mandatory invokes
`task_impact_sync(stage=implementation_discovery)`. Rejected candidates remain
out of scope; a qualified expansion resumes only from a fresh Architecture
result.

## Current constitution consumption

Apply `minimum-necessary-complexity` from the unique current project authority
to every added capability in the complete worktree, including public contracts
and abstractions, using its applicable conclusion and current evidence. The
task-local consumer check is part of this review, not its complete coverage.
Judge necessity against all applicable current contracts and responsibilities;
passing functional tests alone is insufficient. This package consumes the
authority and does not restate its principle prose.

Form concrete candidate observations and qualify them through the existing
Phase 2 profiles before severity or findings. An unnecessary mechanism returns
through `mechanism_revision_required` for remove/replace and fresh complete
check while preserving accepted scope. A conflict in the requirement itself
re-enters the Architecture owner: `architecture_conflict` returns to Planning
and existing clarification for a revised current authority. A resulting scope
or authority change uses this Skill's existing `planning_stale` consumer.
Missing applicable evidence uses the existing Architecture
`contract_incomplete` route or a concrete blocked dependency. No keyword,
approval assertion, or automatic deletion of accepted scope supplies a pass.

Only a qualified current-scope defect may enter existing finding fields.
Existing evidence and adequacy dimensions carry the applicable conclusion;
no new score, per-capability checkpoint, public DTO field or exit is required.

## Semantic Loop

Before repository, Docs, test, fixture, consumer, or history retrieval, read
`.trellis/spec/workflow/semantic-retrieval.md`. Apply its concept-family and
negative-conclusion requirements while judging the existing nine dimensions.
Do not persist raw searches, query lists, or search-process fields in the
private result or public DTO.

Apply `.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value`
to the actual tests, checks and reported outcomes in the current worktree.
Trace their entry and observations to the tested logic and accepted behavior;
a command pass does not settle necessity or effectiveness. Worker checklists
and coverage recommendations are evidence to judge under this policy, not
automatic requirements to add tests or repeat a full chain. Qualified
current-scope defects use the existing finding/fix/full-rerun loop; genuine
evidence gaps use existing blocked handling. Carry conclusions in the existing
adequacy dimensions and validation summaries.

Before proposing a fix, test, validation obligation, severity or route,
separately establish problem validity, current-task necessity and mechanism
suitability through the existing qualification profiles. Identify the concrete
current goal or affected contract that would fail without the work. Preserve
necessary refactoring, consumer adaptation and obsolete-path exit; do not leave
duplicated logic or a second authority for minimum diff. Unrelated historical
debt does not automatically enter current findings, gates or required follow-up.
Architecture facts and work coordination remain separate; scope cannot dismiss
a responsibility violation, and its discovery does not authorize a product-goal
or authority change.

For a red validation, collect only enough evidence to attribute it to a task
regression, inseparable prerequisite, unrelated historical failure, environment,
or unresolved cause. Handle the first two in scope; stop investigation and
repair after unrelatedness is established. Unresolved does not mean historical.
A real required release gate can block release without authorizing unrelated
repairs. Do not pursue full green by weakening assertions, fixtures or samples,
or adjusting timeouts. Review defaults, recommendations, legal explicit
configuration and real protection invariants against their authority; missing
diagnostic attribution alone must not add a business rejection.

1. Reread the current task, approved plan, live authority, diff,
   dirty paths, code, tests, docs, the current Phase 2 Architecture result, and
   current toolchain and environment. Determine the complete applicable check
   set and apply Dependency-Scoped Validation below; do not inherit the old set
   without checking new or changed validation obligations.
2. Perform early candidate hygiene over the committed task-base diff, staged,
   unstaged, untracked, and new files before expensive or external validation.
   Git-diff and untracked-text whitespace or blank-EOF findings are suppressed
   only when the bytes in the projection being checked (`HEAD`, index, or
   worktree) exactly match the same repo-relative path's valid schema-v2
   Trellis `.trellis/.template-hashes.json` entry. This covers tracked
   upstream-template migration deltas without letting exact worktree bytes
   exempt a different staged or committed candidate, and without treating the
   digest as semantic authority. Missing, invalid, unknown, or mismatched
   provenance does not exempt the file, and path, UTF-8, and JSON validation
   always remains active.
3. Form a candidate-only set, then invoke
   `guru-qualify-normal-scenario:phase2_candidate_set`. Only candidates returned
   eligible through `classified` may receive P0-P3 findings.
   `scope_confirmation_required` enters requirements clarification,
   `mechanism_revision_required` returns to implementation for remove/replace
   and full rerun, and `blocked` stops. Rejected candidates never become a
   finding, negative test, implementation route, planning-stale route, or user
   question.
4. Review requirements, design, implementation, tests, Docs SSOT, cross-layer
   behavior, Architecture before/after satisfaction, compatibility,
   deployment/operations, and verification completeness.
   For delete, replace, and merge work, independently review the
   `code_subtraction` and `docs_ssot_subtraction` dimensions. Apply the
   subtraction-first policy: direct evolution first, affected deprecated assets
   exit unless a real supported consumer remains, and non-server compatibility
   added, widened, or extended without concrete current-dialogue approval is a
   finding. Explain growth by asset category instead of a numeric ratio.
   Independently bind the approved Delivery slice, remaining work, observable
   independent-delivery conditions, and validation boundary. Remaining work is
   not a current omission, while any defect or false claim inside the current
   slice remains a finding.
5. After a finding fix, perform one current complete semantic round. Do not
   persist each worker round or require historical HEAD equality. This complete
   round covers current scope and adequacy; it does not require executing every
   unaffected deterministic command again.

AI-owned delta classification decides which conclusions actually changed.
Equivalent formatting, links, derived text, OS noise, and stale downstream
workflow projections refresh direct dependencies without an unrelated full
replay. Real content changes, unknown dirty content, missing checks, or
reproduced findings require the affected review and validation. A changed
shared authority identity first returns to its authority owner for fresh
applicability judgment: an unchanged applicable contract refreshes that direct
dependency; a material contract or scope change returns to the earliest
affected owner through the existing routes. A changed path or identity alone
cannot prove semantic equivalence or require an unrelated full-chain replay.

### Dependency-Scoped Validation

For each check in the current applicable set, the AI owner performs these
steps before recording the current result:

1. Read the check's actual definition/version, checked object, real dependency
   set, runtime/toolchain, and environment profile from their existing sources.
   Compare those dependencies with any prior execution fact this same owner
   still legally retains and can inspect. These are applicability questions,
   not a new schema, stored checklist, or dependency registry.
2. Reuse an execution fact only when the check definition/version, toolchain
   and environment profile are unchanged, its real dependencies remain
   semantically equivalent, and the actual result is still available.
   Candidate revision alone does not invalidate an independent
   check: changing A must not rerun B when B's real dependencies remain
   unchanged. Unknown dependencies or an unavailable result require executing
   that check; do not reconstruct facts from a remembered pass or require
   already-retired checkpoints to be retained.
3. Bind each reused fact to the current candidate in this owner's new
   validation result. In the existing validation summary, identify what
   actually ran and explain why its execution fact applies to the current
   checked object. Do not rewrite the old candidate's record or directly
   present its result as the current candidate's result. The original recorder
   derives the current content identity; no old token or new receipt supplies
   this binding. Reuse supplies validation evidence, never semantic pass.
4. Run each new applicable check and each check whose definition/version,
   dependency, toolchain, or environment changed or whose equivalence cannot
   be established. Keep unaffected facts; do not rerun unrelated checks merely
   because one result is missing. A legal configuration change is a reason to
   rerun its affected check, not an error for differing from an old value.
   Judge configuration usability from appropriate actual integration/E2E
   execution under the current profile, without adding fixed-value allowlists.
5. Account for every currently applicable check with a current bound result or
   an explicit unverified boundary in the existing validation fields. Newly
   applicable checks cannot disappear because a previous set lacked them.
   Complete all current semantic dimensions and handle findings and blocking
   evidence normally before the original recorder/checker/public invocation.

Execution-result updates or added external evidence alone do not redefine the
candidate or trigger identity recomputation loops. If they reveal a real
behavior, applicable-contract, scope, or validation-obligation change, return
to the earliest affected existing owner. Normal task-metadata, documentation,
generated/projection, promotion, or finding-fix changes receive the same impact
judgment and automatic re-entry. Record the current worktree candidate through
the original recorder even when business conclusions remain applicable; do
not exclude task metadata from exact-candidate checking. Once committed
content changes, the current exact base-to-HEAD still receives a complete
independent Branch Review.

Only this owner interprets its available validation facts. No new cache,
checkpoint field, public DTO, cross-Skill receipt chain, or long-lived result
history is introduced. Existing Phase 2-to-Task Commit checkpoint consumption,
capture ancestry, content identity and retirement remain unchanged; Branch
Review does not consume Phase 2 private evidence as its own semantic result.

## Private Result

New evidence uses schema `guru-phase2-check-5.0` in ignored runtime. It retains
only task and checked content identity, one composite
`reviewed_content_sha256` freshness token computed with the private
`guru-phase2-worktree-content-1.0` algorithm over live tracked and untracked
worktree paths, reviewed path locators, validation
summaries and unverified items, Docs SSOT conclusion, nine-dimension semantic
result, scope decisions, findings, route, reason, and consumer.

For each current candidate it directly retains the final classification and
the six-part witness required by the existing Task Commit consumer:
`requirement_refs`, `supported_entry_refs`, `existing_caller_refs`,
`honest_action_sequence`, `defect_observation`, and `excluded_assumptions`.
These fields are authored by the Phase 2 semantic owner from current live
evidence; they do not import or reference qualification stdout, a result/report,
temporary locator, or checkpoint.

It does not retain implementation handoffs, worker identity, raw output,
assignments, liveness, repository snapshots, per-file digests, artifact-digest
bundles, or authorization. The one composite token has a direct local consumer:
the checker invoked inside this Skill's public wrapper before typed-output
projection. A mismatch returns to this owner for AI delta classification; it is
not authorization, semantic approval, a public DTO field, cross-Skill authority,
or a digest chain. After the checked typed output passes its output schema, the
producer retains the checkpoint only for `passed` and deletes it for the other
three exits. Task Commit rereads the retained checkpoint, current content
identity, and commit parent before its candidate and executor proceed, then
deletes the checkpoint after successful publication or successful same-plan
recovery. Failed attempts retain it. Only schema 5.0 is valid; any older artifact
shape is rejected and the owner must run again from the current public profile.

## Recorder And Validator

### Recorder Authoring

Author exactly these existing recorder-input fields in a temporary JSON file
under the task's ignored owner-private runtime, with no authorization or worker
metadata:

- `mode` and `reviewed_paths`: the invocation mode and reviewed repository
  locators covering all current dirty paths.
- `validation`: actual command outcomes, summaries, and explicitly blocking
  or nonblocking unverified items.
- `docs_ssot`: strategy, durable paths, status, and evidence-based conclusion.
- `candidate_classifications`: this owner's final decisions and six-part
  normal-scenario witness for the Task Commit consumer.
- `semantic_review`: status, summary, all nine named adequacy dimensions,
  scope decisions, and findings linked to current candidates.
- `typed_exit`, `route`, `reason`, and `consumer`: your justified result
  and its existing unique consumer, as constrained by schema 5.0.

Read `schemas/phase2-check.schema.json` for the exact nested field shapes.
Do not copy example conclusions. Omit the schema/version, skill/task, captured
commit, and content-token fields from this authoring form: the original
recorder derives them from the real task worktree, not from a model projection.
The public input 2.0 remains a separate routing DTO.

From the task worktree, use the installed package's
`scripts/record-phase2-check.sh --root . --task <task-ref> --input <authoring-file>`,
then `scripts/check-phase2-check.sh --root . --task <task-ref>`, then
`scripts/invoke.sh --input <public-input-file> --owner-result <artifact-path>`.
The artifact path is returned by the recorder; its file is the schema-5.0
result, not the recorder's stdout metadata. Recorder input is a file locator,
not stdin. Keep all public schemas, wrapper arguments, and checkpoint
lifecycle unchanged. Delete the temporary authoring file after consumption.
Normal owner-private recording needs no additional user confirmation; separate
Git/GitHub side effects still require their existing dialogue-local gate.

Native `semantic_authoring` evals must supply facts without an owner result,
let the current AI complete this same review, and forward its authoring unchanged
to these original commands. `post_owner` evals prove deterministic routing
only; neither their staged results nor fake-native traces prove semantic review.

The recorder writes the completed semantic result and derives the one composite
worktree-content token. The validator recomputes that token before public output
projection and checks closed schema shape, task/planning linkage, reviewed dirty-path
coverage, the current content identity and commit-anchor ancestry, finding/scope linkage,
and exit/consumer invariants. It never decides scope, severity, sufficiency,
Docs SSOT, semantic pass, or route.

The ignored runtime result is distinct from the public DTO. `passed` projects
only `task_ref` and `phase2_commit_anchor` to `guru-create-task-commit`; finding and
planning routes project only their direct consumer references.

## Exits

- `passed`: all nine dimensions pass with no open finding or blocking
  unverified item, and the Phase 2 Architecture result and mandatory project
  checks are current and passing.
- An exact conflict-resolved tree records the private
  `resolved_reconciliation_passed` result after the same semantic bar passes.
  It is not an external exit. The package-local deterministic
  `project-resolved-reconciliation` command checks that private result and
  emits the target-owned `resolved_candidate` input directly; it never enters
  ordinary Task Commit or adds a workflow marker.
- `implementation_required`: A current-scope finding returns to implementation.
- `planning_stale`: a current scope or authority change returns to planning.
- `blocked`: a concrete evidence or dependency gap prevents a reliable result.

Mapped re-entry is automatic. Unknown, multiple, stale, ambiguous, or
consumer-mismatched exits fail closed without a routine user prompt.
