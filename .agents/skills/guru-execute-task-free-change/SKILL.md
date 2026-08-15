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
