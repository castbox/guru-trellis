---
name: guru-approve-task-plan
description: Approve current Delivery planning through one AI-owned semantic review, compact private evidence, and four minimal typed exits.
---

# Guru Approve Task Plan

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
finding participates in that review, form only the profile-specific candidate
set and invoke `guru-qualify-normal-scenario` with `planning_scenario_set`.
Assign no severity or revision action before `classified` returns. Rejected
candidates cannot become scope clarification, acceptance, tests, or
implementation work. Mechanism revision removes/replaces the task-introduced
mechanism and reruns qualification; blocked stops. No qualification state is
written to planning runtime or task files.

Before a proposed mechanism participates in planning acceptance, tests,
findings, or revision actions, invoke `guru-qualify-solution-mechanism` with
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


At this candidate boundary, consume actual normal-scenario and solution-mechanism
outcomes before loading `guru-qualify-root-cause` with `planning_scenario_set`. Supply only eligible
refs. New or materially changed incident/protection mechanisms enter that owner;
ordinary features receive its stable applicability disposition. Consume a
still-applicable same-mechanism conclusion on later stages and independently
review this stage's current work/evidence; caller change alone does not repeat
qualification. Root `classified` continues this stage, retaining diagnosis or
mitigation disposition without claiming repair. `mechanism_revision_required`
removes/replaces that mechanism and reenters; `diagnosis_required` pauses only
the unsupported repair and continues bounded investigation of the returned
gaps through this owner, then resubmits. A concrete `blocked` stops. Do not turn
symptom suppression into unrelated scope confirmation, cache qualifications,
or use qualification as completion. Actual scope changes use existing routes.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.

## Source design and Author revision boundary

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
applicable, original RDT writer and final-Phase2 reconciliation order.

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
