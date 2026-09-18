---
name: guru-review-task-delivery
description: Review one approved active-task Delivery slice through a fresh semantic gate and five minimal typed exits.
---

# Guru Review Task Delivery

Use after a fresh complete Branch Review for the exact current committed HEAD.
When Publish returns `review_stale`, its `task_ref` is only a seed: the caller
authors the ordinary `delivery_review` profile with a fresh
`branch_review_commit`, and this owner performs a new review rather than
reusing the prior result or Publish's stale reason.
Read `references/contract.md`, the current requirement authority, approved
Delivery policy, current slice and remaining work, validation evidence, RDT and
Architecture authorities, full Branch Review, base, and live Git/GitHub facts.

This Skill is the sole semantic owner of Delivery readiness. The normal public
path is `scripts/invoke.sh` with one public input and one AI-completed semantic
result. The invocation records, objectively checks, projects, validates, and
retires its owner-private checkpoint in one process. Recorder and checker
commands are diagnostic and test entrypoints only.

Require a truthful Chinese PR title/body, `Refs` only, explicit remaining work,
and no completion, closure, archive, finish, cleanup, push, PR mutation, or
merge claim. Missing or ambiguous Delivery policy returns
`planning_revision_required`; current-slice findings return
`implementation_required`; real scope authority changes return
`scope_confirmation_required`; concrete unavailable evidence returns
`blocked`; only a current complete slice returns `ready`.

Do not read another Skill's private checkpoint. Do not use a prior Delivery,
Completion, Finish, PR body, current branch name, or historical output as this
round's semantic authority. Emit exactly one declared typed exit. Missing,
stale, ambiguous, multiple, unmapped, or checker-failed evidence fails closed.
