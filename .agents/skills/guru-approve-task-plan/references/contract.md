# Guru Approve Task Plan Contract

## Ownership

`guru-approve-task-plan` is the sole semantic owner of Phase 1 planning
approval. It uses `judgment_mode=semantic` and the exact semantic profile:

```text
forward behavior -> AI review gate -> conditional current-conversation
authorization -> recorder/validator -> typed exit
```

The checked `approved` exit proves semantic adequacy; it does not accept the
current solution direction or activate the Delivery. Its stable consumer remains
the workflow target `phase-1-delivery-activation`. That target separately owns the
human-readable plan presentation, dialogue-local review pause, and subsequent
Delivery activation transition. The workflow boundary is outside this Skill's Gate,
recorder, validator, private result, and public DTO.

The conditional authorization step inside this Skill exists only when
unresolved scope or a material plan choice requires it during semantic review.
Authorization is never an artifact or public field. Workflow and standalone
mode apply the same semantic review and objective checks; standalone invocation
returns the same minimal exit to its caller without pretending to satisfy the
workflow-owned plan pause.

For delete, replace, merge, or compatibility-impacting plans, apply the
repository policy in `.trellis/spec/workflow/subtraction-first-compatibility.md`.
The planning judgment must select direct deletion, modification, replacement,
reuse, or synchronized consumer migration before proposing a second path. It
must identify affected deprecated assets and real consumers, and it must reject
unsupported compatibility that has not been specifically approved in the
current conversation before coding, compatibility tests, or self-fixing.

## Public Entry

Public input schema delivery-1.0 is a route DTO. Each profile carries only the owner
entry identity needed for direct consumption:

- `delivery_initial_review`: mode, TaskRef, DeliveryKey, and source route;
- `delivery_revision_reentry`: the same identity plus a task-local revision reason;
- `delivery_clarification_reentry`: the same identity plus an authority-refresh reason.

The caller does not author adequacy, provenance conclusions, findings,
authorization, an AI gate, or an exit. Re-entry reasons select the owner entry;
they do not decide the owner result.

Before planning scenarios can influence acceptance, negative tests, findings,
revision actions, scope proposals, or approval, the owner forms only candidate
refs plus current authority/planning/caller/test locators and invokes
`guru-qualify-normal-scenario:planning_scenario_set`. `classified` returns to
this owner; `scope_confirmation_required` enters requirements clarification;
`mechanism_revision_required` returns here to remove or replace a mechanism and
then rerun the complete current plan review; `blocked` stops. Rejected
candidates never become questions, acceptance, tests, implementation, or
follow-up. The planning checkpoint stores only the Planning owner's final
direct-consumer conclusions and never contains or references qualification
stdout, a result/report, locator, or checkpoint.

## Architecture Stage Consumption

The global workflow mandatory invokes
`guru-maintain-architecture-baseline:delivery_task_impact_sync(stage=planning, planning_purpose=final_plan)` before
this owner can approve Planning. Its fresh `baseline_current` is the adjacent
upstream result and proves that the contract-selected Architecture AI owner has
already completed semantic authoring and the formal deterministic invocation.
For a new Planning assessment, that owner is the fresh independent subagent
selected by the Architecture contract's Independent assessment entry. An
approval caller's self-authored result or a checker pass is insufficient.
This Skill consumes only that checked route and rereads the live project-owned Architecture
Baseline, design-constitution locator/identity, and Architecture change-contract
locator/identity. It never reads Architecture private state or repeats that
owner's impact, applicability, path, contribution, ADR, or route judgment, and
it never searches for or delegates to a second external Architecture owner.

The current Planning result must cover the current task scope and bind both the
Guru public contract and project Architecture contract. Missing or stale
Architecture evidence, a missing constitution/change contract, or an unresolved
`sync_required`, `baseline_incomplete`, `architecture_conflict`,
`contract_incomplete`, or `fitness_regression` route cannot become `approved`.
Those exits return through the global Architecture router to their unique owner.
A current `no_architecture_impact` result is sufficient without a contribution,
ADR, principle score, or new planning artifact.

## Semantic Review

The owner rereads live authority and current files, then reviews these eight
dimensions:

1. requirement authority;
2. scope boundary;
3. design adequacy, including consistency with the current Architecture impact
   result and design constitution;
4. implementation plan;
5. acceptance verifiability;
6. Docs SSOT;
7. provenance;
8. supported unusual scenarios.

Before a proposed change, validation obligation or revision action enters the
plan, distinguish the evidenced problem, its necessity for this task, and the
suitability of its mechanism through the existing qualification owners. Ask
where the current goal or an affected current contract fails without the work.
Retain necessary refactoring, consumer adaptation and old-path retirement;
neither minimum diff nor unrelated historical debt defines the task. Approved
plans, green tests and reviewer suggestions do not establish necessity. A true
responsibility violation need not await functional failure to be considered.
Keep legal non-default configuration distinct from defaults/recommendations
and authority-defined hard invariants; diagnostic gaps do not invent business
rejection. Out-of-plan scope or authority changes use the existing routes.

For implementation planning and acceptance verifiability, apply
`.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value` to the
proposed tests and gates. Judge whether the planned entry, observed behavior
and defect detection prove the accepted scope at the stated layer. Revise
ineffective validation through the existing task-local revision loop before
approval; use existing clarification or blocked routes for actual authority
choices or evidence gaps. Keep the judgment in the existing dimensions.

The planning result also records one closed Delivery policy as semantic
evidence: the complete task scope, current Delivery slice, explicit remaining
work, observable conditions that make the slice independently deliverable,
the slice validation boundary, and the owner that retains the remaining work.
An empty or ambiguous slice, hidden remaining work, or a condition that depends
on the remaining work already being complete cannot produce `approved`.

Formatting, spelling, link, derived-text, and workflow-metadata deltas are
classified by the AI against their actual semantic effect. A proven equivalent
delta refreshes only the directly dependent owner identity. A requirement,
scope, authority, design, acceptance, behavior, or verification change routes
through the affected semantic owner.

An actual task-applicable semantic change to Architecture, constitution,
project change-contract, task scope or impact conclusions requires the affected
owner's fresh Architecture Planning result before reconsidering approval.
Unrelated CURRENT/version/navigation advancement does not replace the stage's
explicit applicable authority and is not such a semantic change. The Architecture result remains live stage evidence;
it is not added to this Skill's public DTO or compact checkpoint.

## Causal planning dependency

Read `.trellis/spec/workflow/causal-completion-semantics.md` when reviewing
the current accepted goals, proposed mechanisms, evidence requirements and
validation plan. Bind each diagnosis, mitigation or repair slice to its own
observable acceptance; whole-task completion retains all accepted obligations.
Use the existing qualification owners and plan revision/scope/blocked routes.
Do not require an unknown root cause to be solved before bounded diagnosis or
qualified mitigation can start or satisfy their own scope. Plan production
proof only when accepted requirements need it and keep pre-delivery slice
validation distinct from evidence obtainable after merge/deploy.

## Private Result

New owner evidence uses schema `guru-planning-approval-delivery-1.0` in ignored runtime.
It retains only:

- mode and task locator;
- the three planning locators and current authority references;
- one composite `reviewed_content_sha256` freshness token over those three
  planning files;
- the compact Docs SSOT decision;
- the closed Delivery policy used by later Check and Branch Review owners;
- the final eight-dimension semantic result;
- typed exit, reason, and consumer.

The composite token first serves the planning checker inside this Skill's
public wrapper. On `approved`, the wrapper projects the checked token as the
minimal `planning_result_id` handed to Activation. Activation compares that
reviewed identity with the current planning files; its caller must not replace
it with a freshly computed digest. The token detects same-path content drift,
then returns control to this owner for AI delta classification. It is not
authorization, semantic approval, or a digest chain. After the checked typed output passes
its output schema, the same producer wrapper deletes the checkpoint. Delivery
activation and Phase 2 consume only the minimal DTO plus current planning/live
facts; they never read or delete this private state. The checkpoint does not
retain per-file hashes, sizes, mtimes, repository snapshots, full scan history,
reviewer metadata, raw reports, handoffs, assignments, authorization, or
authorization digests.

Only schema delivery-1.0 is a valid current owner result. Any other schema version or
unknown CLI option is rejected by the current validator; callers rerun this
owner with the current public profile instead of projecting prior fields.

## Recorder And Validator

The recorder writes the already completed semantic result and derives the one
composite planning-content token. The validator recomputes that token and checks
schema closure, task and required-file locators, current approved route,
consumer mapping, and objective union invariants. Neither component decides
scope, sufficiency, findings, revisions, authorization, semantic pass, or route.

Keep cwd at the task repository root. The installed package is
`.trellis/guru-team/skills/packages/guru-approve-task-plan`; its
`examples/planning-approval-delivery.json` describes the complete recorded result, not
the normal recorder input. Normal authoring contains exactly these eight
top-level fields: `mode`, `authority_refs`, `delivery_policy`, `docs_ssot_plan`,
`semantic_review`, `typed_exit`, `consumer`, and `reason`. Populate their semantic content using
the corresponding definitions in `schemas/planning-approval-delivery.schema.json`.
Omit `schema_version`, `skill_id`, `task_ref`, `planning_paths`, and
`reviewed_content_sha256`: the recorder supplies those from the exact task and
current planning files. An object with `schema_version=delivery-1.0` is already a
complete recorded result and must not be used as partial authoring.

Use the existing commands in this order. Record and invoke each receive one
JSON object on stdin; the checker does not read stdin:

```bash
GURU_SKILL_PACKAGE=.trellis/guru-team/skills/packages/guru-approve-task-plan
"$GURU_SKILL_PACKAGE/scripts/record-planning-approval.sh" --root . --task "$TASK_REF" --delivery-key "$DELIVERY_KEY_JSON" --input -
"$GURU_SKILL_PACKAGE/scripts/check-planning-approval.sh" --root . --task "$TASK_REF" --delivery-key "$DELIVERY_KEY_JSON"
"$GURU_SKILL_PACKAGE/scripts/invoke.sh" --root . --input - --owner-result "$CHECKPOINT"
```

The recorder receives the eight-field semantic input. Retain its returned
`artifact_path` as `CHECKPOINT`; the checker reads that task-owned checkpoint.
Invoke receives the minimal public route DTO on stdin and the checked owner
result from that path. Do not pass recorder response metadata (`artifact_path`,
`dry_run`) as owner-result fields. The wrapper retires the checkpoint after a
valid public projection; the next owner consumes only the typed stdout.

The ignored runtime result is not a tracked task artifact and is not the public
DTO. A failed checker or invalid output retains it for same-owner repair; a
valid public projection retires it before control reaches the next owner.

## Exits

- `approved`: every dimension passed and the activation workflow receives only
  `exit_id`, `task_ref`, `delivery_key`, and `planning_result_id`, and the current Planning-stage Architecture result
  is still fresh; the consumer must still satisfy its own
  presentation and dialogue-local review boundary.
- `revision_required`: actual task-local revision actions go through
  `guru-task-plan-approval-revision-router` to Author `approval_revision`;
  after the affected gates refresh, this owner reviews `revision_reentry`.
- `clarify_scope`: exact scope proposal references route to requirements
  clarification.
- `blocked`: a concrete authority or evidence gap stops the workflow.

Mapped re-entry is automatic. Unknown, multiple, stale, ambiguous, or unmapped
exits fail closed without creating a routine user prompt.


## #292 author boundary

Author owns business writing and original-source design dispositions. This
owner reviews the sole design.md matrix commitment by commitment, actual
retain landing points, change/reject rationale/impact and required upstream
handling; no provenance flag substitutes. Check implement's unique Delivery
Policy and Docs SSOT Plan with their actual remaining-work/Completion and RDT
reconciliation consumers. Only Wording-current final_plan Architecture output
is eligible; candidate_assessment never substitutes. Revision returns actual
revision_actions through the workflow router to Author approval_revision, then
fresh dependent gates and this owner's revision_reentry. The old Approval
self-writing edge and private 3.0 checkpoint are retired; the Delivery checkpoint and
revision_actions handoff are the current selectors. Approved output and #468 semantics remain.

## Delivery Planning boundary (schema 2.0 installation)

The public input carries an explicit opaque DeliveryKey, including D1. Resolve
all three documents through the installed public planning_root; Task-root
prd.md remains whole-task accepted scope and is not this Delivery's plan.
The same key covers active replanning and partial scope revision. Full withdrawal
returns through Clarify and the original current stage's legal stop owner.
Author responsibilities remain with the existing unique Author; #292's delivered
unique Author remains the sole business writer; Delivery identity is a thin projection.
Approval never calls public record_gate. Only adjacent Activation consumes the
Guru planning_result_id; the independent public planning_accepted_result_id is
written by guru-activate-delivery. The checkpoint is keyed by Delivery and
retired by this same owner on output, never read by another owner.
The prior Task planning/activation inputs require the pinned complete old
installation. No activity fallback or Task status mutation exists in this graph.

## Adjacent final-plan input 2.0

Each current Delivery profile uses its independent 2.0 input. The actual
Architecture final_plan stdout supplies architecture_assessment via one thin
projection: planning_purpose routes only final_plan; freshness_identity binds
current selected design; baseline_identity and constitution_identity/status
are the authorities this semantic owner rereads; impact_kind selects the
applicable contribution judgment; promotion_state is this owner's current
eligibility prerequisite. Do not hand-author this assessment from files or use
candidate_assessment as final proof. No Architecture private result crosses.
The invocation objectively checks design freshness, and semantic Approval
still checks adequate current authority/contribution and full planning scope.
The older Delivery1.0 input without that actual final producer is retained as
a validation asset and fails closed at current invocation. Lost output refreshes
final Architecture after Wording, not an inferred approval from public phase.

## Applicable authority and fixed candidate

Review the versions actually applicable to this Task/Delivery and current plan.
An unrelated CURRENT, navigation, archive, non-dependency code or tool-version
advance is not a Planning dependency change. Explicitly applicable rules, user
requirements, invalidated assumptions and actual scope/dependency/solution
changes still refresh their original owners. Consume the actual adjacent
final_plan for this design; no latest-base or pair qualification precedes
Approval or Activation. Check the complete range mechanism, actual head
evolution and same-Delivery recovery; no historical pass supplies approval.
