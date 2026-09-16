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

## Semantic Loop

Before repository, Docs, test, fixture, consumer, or history retrieval, read
`.trellis/spec/workflow/semantic-retrieval.md`. Apply its concept-family and
negative-conclusion requirements while judging the existing nine dimensions.
Do not persist raw searches, query lists, or search-process fields in the
private result or public DTO.

1. Reread the current task, approved plan, live authority, diff,
   dirty paths, code, tests, docs, the current Phase 2 Architecture result, and
   applicable validation commands.
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
5. After a finding fix, perform one current complete semantic round. Do not
   persist each worker round or require historical HEAD equality.

AI-owned delta classification decides which conclusions actually changed.
Equivalent formatting, links, derived text, OS noise, and stale downstream
workflow projections do not trigger an unrelated full replay. Real semantic
changes, unknown dirty content, missing checks, or reproduced findings do.

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
- `implementation_required`: A current-scope finding returns to implementation.
- `planning_stale`: a current scope or authority change returns to planning.
- `blocked`: a concrete evidence or dependency gap prevents a reliable result.

Mapped re-entry is automatic. Unknown, multiple, stale, ambiguous, or
consumer-mismatched exits fail closed without a routine user prompt.
