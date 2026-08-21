# Guru Approve Task Plan Contract

## Ownership

`guru-approve-task-plan` is the sole semantic owner of Phase 1 planning
approval. It uses `judgment_mode=semantic` and the exact semantic profile:

```text
forward behavior -> AI review gate -> conditional current-conversation
authorization -> recorder/validator -> typed exit
```

The checked `approved` exit proves semantic adequacy; it does not accept the
current solution direction or activate the task. Its stable consumer remains
the workflow target `phase-1-task-activation`. That target separately owns the
human-readable plan presentation, dialogue-local review pause, and subsequent
activation transition. The workflow boundary is outside this Skill's Gate,
recorder, validator, private result, and public DTO.

The conditional authorization step inside this Skill exists only when
unresolved scope or a material plan choice requires it during semantic review.
Authorization is never an artifact or public field. Workflow and standalone
mode apply the same semantic review and objective checks; standalone invocation
returns the same minimal exit to its caller without pretending to satisfy the
workflow-owned plan pause.

## Public Entry

Public input schema 2.0 is a route DTO. Each profile carries only the owner
entry identity needed for direct consumption:

- `initial_review`: mode, task, and source route;
- `revision_reentry`: the same identity plus a task-local revision reason;
- `clarification_reentry`: the same identity plus an authority-refresh reason.

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
`guru-maintain-architecture-baseline:task_impact_sync(stage=planning)` before
this owner can approve Planning. This Skill consumes only the checked
`baseline_current` route and rereads the live project-owned Architecture
Baseline, design-constitution locator/identity, and Architecture change-contract
locator/identity. It never reads Architecture private state or repeats that
owner's impact, applicability, path, contribution, ADR, or route judgment.

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

Formatting, spelling, link, derived-text, and workflow-metadata deltas are
classified by the AI against their actual semantic effect. A proven equivalent
delta refreshes only the directly dependent owner identity. A requirement,
scope, authority, design, acceptance, behavior, or verification change routes
through the affected semantic owner.

Architecture baseline, constitution, project change-contract, task scope, or
impact-result drift is a semantic dependency change rather than equivalent
formatting. It requires a fresh Architecture Planning result before this owner
can reconsider approval. The Architecture result remains live stage evidence;
it is not added to this Skill's public DTO or compact checkpoint.

## Private Result

New owner evidence uses schema `guru-planning-approval-3.0` in ignored runtime.
It retains only:

- mode and task locator;
- the three planning locators and current authority references;
- one composite `reviewed_content_sha256` freshness token over those three
  planning files;
- the compact Docs SSOT decision;
- the final eight-dimension semantic result;
- typed exit, reason, and consumer.

The composite token has one local deterministic consumer: the planning checker
invoked inside this Skill's public wrapper before typed-output projection. It
detects same-path content drift, then returns control to this owner for AI delta
classification. It is not authorization, semantic approval, a public DTO field,
cross-Skill authority, or a digest chain. After the checked typed output passes
its output schema, the same producer wrapper deletes the checkpoint. Task
activation and Phase 2 consume only the minimal DTO plus current planning/live
facts; they never read or delete this private state. The checkpoint does not
retain per-file hashes, sizes, mtimes, repository snapshots, full scan history,
reviewer metadata, raw reports, handoffs, assignments, authorization, or
authorization digests.

Only schema 3.0 is a valid current owner result. Any other schema version or
unknown CLI option is rejected by the current validator; callers rerun this
owner with the current public profile instead of projecting prior fields.

## Recorder And Validator

The recorder writes the already completed semantic result and derives the one
composite planning-content token. The validator recomputes that token and checks
schema closure, task and required-file locators, current approved route,
consumer mapping, and objective union invariants. Neither component decides
scope, sufficiency, findings, revisions, authorization, semantic pass, or route.

The ignored runtime result is not a tracked task artifact and is not the public
DTO. A failed checker or invalid output retains it for same-owner repair; a
valid public projection retires it before control reaches the next owner.

## Exits

- `approved`: every dimension passed and the activation workflow receives only
  `exit_id` and `task_ref`, and the current Planning-stage Architecture result
  is still fresh; the consumer must still satisfy its own
  presentation and dialogue-local review boundary.
- `revision_required`: task-local revision actions return to this owner.
- `clarify_scope`: exact scope proposal references route to requirements
  clarification.
- `blocked`: a concrete authority or evidence gap stops the workflow.

Mapped re-entry is automatic. Unknown, multiple, stale, ambiguous, or unmapped
exits fail closed without creating a routine user prompt.
