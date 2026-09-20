---
name: guru-execute-task-free-change
description: Execute one bounded task-free change through AI-owned checkout suitability, editing, targeted validation, and risk-evolution review.
---

# Guru Execute Task-Free Change

Invoke this Skill only after `guru-select-workflow-mode:task_free`. The caller
authors the current request summary, bounded target paths, continuation identity,
and whether selection was automatic or explicit. The selector contributes only
its existing `exit_id`; checkout facts never enter the selector DTO.

The AI owns the complete semantic loop: read local checkout/task/dirty facts,
judge write suitability, perform only the bounded edit, run risk-matched targeted
checks, and review scope/risk again after writing. Scripts only validate the
AI-authored result and serialize one typed exit. Never query branch protection.

Before the pre-write suitability decision, form only current candidate refs and
live locators, then invoke `guru-qualify-normal-scenario` with
`task_free_pre_write`. If execution discovers a new behavior, scope, test, or
risk candidate, stop further target writes and invoke it with
`task_free_evolution` before deciding expansion significance or route. Consume
only the current typed result: classified candidates return to this owner,
scope-confirmation candidates go to requirements clarification, mechanism
revision returns here for remove/replace and fresh qualification, and blocked
stops. Rejected candidates never become a user question, test, implementation,
or risk-expansion route. Qualification decisions remain invocation-local.

At each of those candidate boundaries, invoke
`guru-qualify-solution-mechanism` with the same profile before accepting a
proposed mechanism as part of the task-free edit or evolution decision. Its
`mechanism_revision_required` exit removes or replaces only the proposed
mechanism and returns here for fresh qualification; it never enters scope
confirmation.

`completed` requires current evidence for both the pre-write suitability review
and the post-write scope/risk review, plus the actual edited paths and targeted
checks. Its workflow output reports edited paths, concise validation results,
and unverified boundaries.

`reselect_mode` and `explicit_choice_required` require evidence of the actual
partial edit, the discovered scope/risk expansion, immediate write stop,
remaining target writes not performed, and applicable targeted checks. No exit
authorizes commit, push, PR, merge, release, installation, cleanup, Issue
closure, or any lifecycle resource.

Return exactly one of `completed`, `resume_active_task`, `scope_change`,
`location_required`, `reselect_mode`, `explicit_choice_required`, or `blocked`.
`location_required` and `explicit_choice_required` re-enter this Skill after the
dialogue-local choice. Preserve unrelated dirty and untracked work.
