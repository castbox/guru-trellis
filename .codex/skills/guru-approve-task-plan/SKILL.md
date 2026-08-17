---
name: guru-approve-task-plan
description: Approve current task planning through one AI-owned semantic review, compact private evidence, and four minimal typed exits.
---

# Guru Approve Task Plan

Use this Skill after the current planning wording review has passed and before
task activation. Load [references/contract.md](references/contract.md) before
acting.

Read the live requirement authority, `prd.md`, `design.md`, `implement.md`, the
Docs SSOT plan, and the issue scope ledger directly. Review requirement
authority, scope, design, implementation planning, acceptance verifiability,
Docs SSOT, provenance, and supported unusual scenarios. The AI owns findings,
revision actions, scope proposals, the final route, and delta classification.

Before an acceptance scenario, negative test, behavior constraint, or planning
finding participates in that review, form only the profile-specific candidate
set and invoke `guru-qualify-normal-scenario` with `planning_scenario_set`.
Assign no severity or revision action before `classified` returns. Rejected
candidates cannot become scope clarification, acceptance, tests, or
implementation work. Mechanism revision removes/replaces the task-introduced
mechanism and reruns qualification; blocked stops. No qualification state is
written to planning runtime or task files.

The checked `approved` exit establishes semantic adequacy only. Its stable
consumer is the workflow target `phase-1-task-activation`, which separately
presents the current plan and owns the dialogue-local review pause before task
activation. This Skill neither satisfies, evaluates, records, nor persists that
workflow-owned acceptance. Within this Skill, interact only when unresolved
scope or a material plan choice requires current dialogue input. Never write
authorization, its wording, time, source, reference, or digest into an input,
checkpoint, gate, handoff, archive, schema, or public DTO. Mapped exits and
same-scope re-entry continue automatically.

After the semantic result exists, record and validate only the compact 3.0
owner-private projection. Its one composite planning-content token serves only
the adjacent freshness checker; it is not semantic or workflow authority.
Return exactly one of `approved`,
`revision_required`, `clarify_scope`, or `blocked`. The public input only routes
the owner entry; it never supplies findings, approval status, or a preselected
exit. Missing, stale, multiple, unknown, or consumer-mismatched results fail
closed. This package requires the complete compatible Guru Team preset runtime
and is not self-contained or portable.
