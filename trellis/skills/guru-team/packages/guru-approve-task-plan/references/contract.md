# Guru Approve Task Plan Contract

## Ownership

`guru-approve-task-plan` is the sole semantic owner of Phase 1 planning
approval. It uses `judgment_mode=semantic` and the exact semantic profile:

```text
forward behavior -> AI review gate -> conditional current-conversation
authorization -> recorder/validator -> typed exit
```

The checked `approved` exit and `task.py start` status write do not create a
routine authorization stop. The conditional authorization step exists only
when unresolved scope, a material plan choice, or the next real external side
effect requires it. Authorization is never an artifact or public field.
Workflow and standalone mode apply the same semantic review and objective
checks.

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

## Semantic Review

The owner rereads live authority and current files, then reviews these eight
dimensions:

1. requirement authority;
2. scope boundary;
3. design adequacy;
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
  `exit_id` and `task_ref`.
- `revision_required`: task-local revision actions return to this owner.
- `clarify_scope`: exact scope proposal references route to requirements
  clarification.
- `blocked`: a concrete authority or evidence gap stops the workflow.

Mapped re-entry is automatic. Unknown, multiple, stale, ambiguous, or unmapped
exits fail closed without creating a routine user prompt.
