---
name: guru-review-task-publication
description: Review task publication readiness through ten semantic dimensions, metadata-only revision, one private gate, and three typed exits.
---

# Guru Review Task Publication

Use after `guru-review-branch:passed`, or for a checker-declared stale
finalization handback. Read `references/contract.md`, author the selected public
input profile, and complete the semantic review. The single recommended Happy
Path is `review-task-publication`: pass the public input and the AI-completed
semantic result, and let that facade record, objectively check, project, and
retire the private checkpoint in one invocation.

Do not read package runtime, schemas, examples, evals, or tests for the normal
path. `record-task-publication-review`, `check-task-publication-review`, and
`invoke-guru-review-task-publication` remain compatibility, testing, and bounded
recovery commands only.

The stale profile requires the Finalizer-projected `branch_review_commit`.
Bind the checked owner result to that same commit. Normal content continuity drift
may produce a semantic `task_work` finding and `return_to_task_work`; it can
never produce `ready`. This exception applies only after the runtime proves the
reviewed commit is an ancestor of current HEAD and successfully inspects the
descendant diff; an invalid or non-ancestor commit, or an uninspectable diff,
fails closed.

Never treat scanner success, empty findings, changed-file classification, a
deterministic readiness flag, or script success as semantic pass. Metadata-only
revision remains inside this Skill. Reread every objective precondition, then
re-review only dimensions whose direct evidence changed. A prior passed
dimension may be carried forward only when its evidence references remain
current and byte-identical; source, test, durable-doc, spec, workflow, schema,
config, or deployment drift returns to task work.

Before a publication observation can become a finding, task-work return, or
publication blocker, form only candidate refs and live publication/diff/test
locators and invoke `guru-qualify-normal-scenario` with
`publication_candidate_set`. Do not assign severity or route before
`classified`. Rejected candidates cannot become clarification, task work, or a
blocker. Mechanism revision returns to task work for remove/replace and a fresh
publication review; blocked stops. The Publication gate records only this
owner's final direct-consumer classification/witness and never references
qualification stdout, a result/report, locator, or checkpoint.

Emit exactly one declared typed exit. Missing, stale, ambiguous, multiple,
unmapped, or checker-failed evidence fails closed.

`ready` has exactly one consumer: `guru-finalize-task`. The caller must not
push the reviewed/publication HEAD or create a PR between this Skill and that
consumer; Finalizer owns the complete remote transaction.
