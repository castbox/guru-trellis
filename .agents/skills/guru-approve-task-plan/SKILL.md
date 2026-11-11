---
name: guru-approve-task-plan
description: Review whether current formal Delivery planning is sufficient to implement, including 审核规划是否可实施, through the existing semantic approval loop and four typed exits. Standalone product or system-design document review uses its applicable specialist; retain Approval prerequisites.
---

# Guru Approve Task Plan

## Common review sufficiency

Before reviewing this owner's object, read `review-sufficiency.md` in full from
the complete Guru provider that supplies this Skill. Its workflow-spec root is
`trellis/presets/guru-team/spec/workflow` in source, or `.trellis/spec/workflow`
after installation. Resolve target-project authority separately; the target
need not install Trellis to receive review from another provider. Apply the
common rules within this owner's original scope, order and stage conditions.

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

## Qualification Applicability

At this Skill's candidate boundary, first read the original owners' short
[normal](../guru-qualify-normal-scenario/references/applicability.md),
[solution](../guru-qualify-solution-mechanism/references/applicability.md), and
[root](../guru-qualify-root-cause/references/applicability.md) conditions before
loading any qualifier in full. This owner judges each condition independently
from current authority, actual candidates and material changes; it does not
copy a qualifier's complete verdict. Adopt a still-applicable conclusion. Only
when an owner's conditions require a current invocation, explicitly load that
stable Skill and invoke it with its real applicable nonempty set and the
profile below. If it does not trigger, load no qualifier body, assemble no
input and emit no empty, classified or skipped result for it. The complete
current-stage judgment and all applicable non-passing routes remain required.

Apply `.trellis/spec/workflow/quality-guidelines.md#specialist-review-standards`
within this Skill's existing entry and planning review. Load applicable
specialist methods and same-source standards for the actual planned artifacts,
then judge their evidence against this Delivery's requirements, solution and
validation plan. Do not require unrelated full product or system-design
packages, or accept a specialist pass as this owner's planning approval.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

Read `.trellis/spec/workflow/causal-completion-semantics.md` alongside this
package contract before the stage judgment; the contract owns its local routes.

Use this Skill after the current planning wording review has passed and before
Activation. No official context key means this profile's explicit DeliveryKey
is validated by the original projection against current generation, C4 and
public record; an available context still requires its exact official current
selection. Missing/stale/conflicting session facts never use explicit fallback.
Before reading this Delivery's planning bodies or recording Approval, check the
receiving session's own public current facts. Missing Task invokes original
Identity/Ensure/Bind; missing selection invokes original
`guru-create-delivery:delivery_selection` on the explicit applicable key.
Execute the installed workflow's `Explicit receiving-session continuation`,
then reread key/generation, phase, scope and planning_root. Reuse matching facts;
terminal, conflicting selection and real errors remain with their original
owners. Workflow and standalone use this same entry. Preserve the actual
unfinished Approval and applicable adjacent final_plan output; restored
binding is not approval and does not restart Author.
Use the resulting Delivery planning_root for this approval.
Load [references/contract.md](references/contract.md) before
acting.

Before judging planned validation, read and apply
`.trellis/spec/workflow/quality-guidelines.md#test-and-validation-value`.

Read the live requirement authority, `prd.md`, `design.md`, `implement.md`, and
the Docs SSOT plan directly. Review requirement
authority, scope, design, implementation planning, acceptance verifiability,
Docs SSOT, provenance, and supported unusual scenarios. The AI owns findings,
revision actions, scope proposals, the final route, and delta classification.
For an Issue-backed task, its single `source.repo_ref + number` is the Direct
Source even when that repository differs from the execution repository. A legal
`no_issue` source needs no invented Issue. Coordination, Related Work and
Follow-up links supply only the uses explicitly required by accepted scope;
they do not add source identity, project topology or Closure authority. Reread
revised Direct Source content and necessary external facts. Material changes
return to the earliest affected existing owner; informational changes alone
do not invalidate planning. Keep the existing dependency-scoped delta judgment.
For delete, replace, merge, or compatibility-impacting work, also apply
`.trellis/spec/workflow/subtraction-first-compatibility.md`: review direct
deletion/modification/reuse first, identify affected deprecated assets and
consumers, and require the concrete compatibility dialogue before coding,
compatibility tests, or self-fixing. Do not treat `public` or `stable` naming as
an exemption, and do not persist authorization.
Reject incidental task-local fields, persistence, retries, locks, fallbacks, or
other complexity without a named direct consumer. Treat the 3000-line limit for
every touched non-generated code file as a mandatory mechanical-split or small-
decoupling review trigger.

Before that review may return `approved`, consume a fresh
`guru-maintain-architecture-baseline:delivery_task_impact_sync(stage=planning, planning_purpose=final_plan)`
`baseline_current` result from the adjacent upstream invocation and reread its project-owned Architecture Baseline,
design-constitution authority, and Architecture change-contract authority.
That current result proves the contract-selected Architecture AI owner already
completed its semantic authoring and formal invocation. Do not search for a
second external owner, reconstruct the Architecture private result, or repeat
its impact/path/contribution/ADR judgment inside Planning approval.
Planning cannot approve a missing or stale Architecture result, a missing
constitution or change contract, or an unresolved conflict, incomplete
contract, regression, or sync route. Bind the current impact/change-path result
inside the existing design-adequacy and provenance judgments; do not copy the
Architecture owner's reasoning or turn constitution principles into a second
checklist. A current `no_architecture_impact` result creates no contribution or
ADR burden.

Before an acceptance scenario, negative test, behavior constraint, or planning
finding participates in that review, apply Qualification Applicability.
When normal requires a current invocation, form only its applicable nonempty
set and invoke `guru-qualify-normal-scenario` with `planning_scenario_set`.
That candidate receives no severity or revision action before the actual
`classified` outcome establishes eligibility. Rejected
candidates cannot become scope clarification, acceptance, tests, or
implementation work. Mechanism revision removes/replaces the task-introduced
mechanism and reruns qualification; blocked stops. No qualification state is
written to planning runtime or task files.

Before a proposed mechanism participates in planning acceptance, tests,
findings, or revision actions, apply solution's conditions. When they require
a current invocation, invoke `guru-qualify-solution-mechanism` with
`planning_scenario_set`. A `mechanism_revision_required` result removes or
replaces only the task-introduced mechanism and returns here for fresh
qualification; it never becomes scope clarification.

The checked `approved` exit establishes semantic adequacy only. Its stable
consumer is the workflow target `phase-1-delivery-activation`, which separately
presents the current plan and owns the dialogue-local review pause before Delivery
activation. This Skill neither satisfies, evaluates, records, nor persists that
workflow-owned acceptance. Within this Skill, interact only when unresolved
scope or a material plan choice requires current dialogue input. Never write
authorization, its wording, time, source, reference, or digest into an input,
checkpoint, gate, handoff, archive, schema, or public DTO. Mapped exits and
same-scope re-entry continue automatically.

After the semantic result exists, record and validate only the compact delivery-1.0
owner-private projection. Its composite planning-content token serves the
adjacent freshness checker; the checked `approved` exit projects it as the
minimal `planning_result_id` consumed by Activation. The token is not semantic
or workflow authority, and Activation must not treat a recomputed token as semantic approval.
Return exactly one of `approved`,
`revision_required`, `clarify_scope`, or `blocked`. The public input only routes
the owner entry; it never supplies findings, approval status, or a preselected
exit. Missing, stale, multiple, unknown, or consumer-mismatched results fail
closed. This package requires the complete compatible Guru Team preset runtime
and is not self-contained or portable.


At this candidate boundary, apply the original
[root conditions](../guru-qualify-root-cause/references/applicability.md).
When they require a current invocation, explicitly load `guru-qualify-root-cause`
with `planning_scenario_set` and supply only actual eligible refs. This caller uses its
current scenario and authority-placement judgments and consumes actual normal
or solution outcomes when those owners triggered. It never requires an outcome
from an owner that correctly did not trigger. Adopt a still-applicable
same-mechanism conclusion and independently review this stage's current
work/evidence; stage or caller change alone does not repeat qualification.
Material changes refresh only affected judgments; a lost necessary conclusion
returns to its original owner for recovery or fresh judgment. Root `classified`
continues this stage, retaining diagnosis or mitigation disposition without
claiming repair. `mechanism_revision_required` removes/replaces that mechanism
and reenters; `diagnosis_required` pauses only the unsupported repair and
continues bounded investigation of the returned gaps through this owner, then
resubmits. A concrete `blocked` stops. Do not turn symptom suppression into
unrelated scope confirmation, cache qualifications, or use qualification as
completion. Actual scope changes use existing routes.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

## Source design and Author revision boundary

Before the semantic review, actually load
`.trellis/guru-team/skills/packages/guru-author-task-plan/references/planning-body.md`
and that package's `templates/delivery-prd.md`,
`templates/delivery-design.md`, and `templates/delivery-implement.md`.
Read the selected Delivery's three complete bodies, whole accepted scope,
and necessary source/canonical references with their associated conditions.
A listed reference, complete heading set, or matrix does not prove sufficient
content. Apply the shared depth and trimming rules to the actual task.

Within the existing eight dimensions, trace actual scenarios to requirements,
design landing points, executable implementation steps, planned validation and
observable acceptance. Check this batch's context, actual predecessor facts,
remaining responsibility and whole-task Completion relationship for full D1
as well as partial/later Deliveries. When accepted scope requires actual Agent
writing/review behavior, assess that evidence separately from deterministic
checks and installation projections. Neither template presence nor
package/schema success proves that behavior.
Return ordinary omissions as concrete `revision_actions` through
`revision_required` to the earliest affected original owner. Real requirement
choices use `clarify_scope`; technical design elaboration stays with
Author/Architecture without changing product scope. Approval never writes the
missing bodies or repeats Architecture's independent assessment/read order.

Freshly read the actual normative source commitments and the sole disposition
matrix in design.md, one commitment at a time. Check concrete source locators,
original promises, retain landing points, change/reject rationale/impact and
applicable completed upstream handling. A provenance flag or a complete-looking
matrix cannot replace this review. Missing normal source commitments return
revision_required; an unresolved requirement/authority choice returns
clarify_scope. Do not silently reinterpret normative design as advisory or
upgrade advice into a constraint. PRD/implement must not duplicate the matrix.
Explicitly verify the unique Delivery Policy and Docs SSOT Plan in implement,
including remaining work/stages and whole-task Completion conditions where
applicable, original RDT writer and precommit integration/readback followed by independent
committed Review.

Only adjacent current final_plan Architecture output is eligible for approval;
candidate_assessment cannot establish final currentness. Final task design and
real contribution/necessary ADR must remain current at this boundary. Preserve
original eight dimensions and qualification owners. Approval never writes
business planning. revision_required 2.0 projects actual revision_actions to
its workflow router, which invokes Author approval_revision; afterwards refresh
the earliest affected gates and re-enter Approval with its current input.
The Delivery checkpoint preserves the 4.0 semantic constraints, and the old revision self-writer edge is
retired by MIGRATION-292. Approved/Activation identity semantics stay unchanged.

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

Current Delivery input 2.0 consumes only the actual adjacent final_plan output
through architecture_assessment. Its purpose must be final_plan and its design
freshness current. Reread the identified baseline and constitution and judge
impact/promotion eligibility yourself; do not synthesize an assessment from
phase or files. The deterministic wrapper checks identity/freshness, while
Approval remains the original semantic gate and never writes public Planning.

For selected legacy control inspection/retirement, load `references/legacy-maintenance.md` and use its separate `scripts/legacy-maintenance.sh` entry. Normal current profiles are unchanged.
