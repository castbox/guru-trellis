---
name: guru-review-task-publication
description: Review task publication readiness through ten semantic dimensions, metadata-only revision, one private gate, and three typed exits.
---

# Guru Review Task Publication

Use after `guru-review-branch:passed`, or for a checker-declared stale
finalization handback. Read `references/contract.md`, author the selected public
input profile, complete the semantic review, then call the package recorder and
checker through the shared dispatcher.

The stale profile requires the Finalizer-projected `reviewed_content_head`.
Bind the checked owner result to that same HEAD. Normal content continuity drift
may produce a semantic `task_work` finding and `return_to_task_work`; it can
never produce `ready`. This exception applies only after the runtime proves the
reviewed HEAD is an ancestor of current HEAD and successfully inspects the
descendant diff; an invalid or non-ancestor HEAD, or an uninspectable diff,
fails closed. A legacy stale input without the reviewed HEAD fails
closed and returns to current Finalizer discovery instead of synthesizing one.

Never treat scanner success, empty findings, changed-file classification, a
legacy `ready=true` snapshot, or script success as semantic pass. Metadata-only
revision remains inside this Skill. Reread every objective precondition, then
re-review only dimensions whose direct evidence changed. A prior passed
dimension may be carried forward only when its evidence references remain
current and byte-identical; source, test, durable-doc, spec, workflow, schema,
config, or deployment drift returns to task work.

Emit exactly one declared typed exit. Missing, stale, ambiguous, multiple,
unmapped, or checker-failed evidence fails closed.

Existing v1 `publication_review` inputs are read-only migration signals only.
If an input still contains `reviewed_head` or `review_ref`, fail closed and
return to the Branch Review owner. That owner completes any required fresh
review and emits the current minimal `passed` DTO. Publication never reads,
projects, rewrites, or republishes another Skill's private checkpoint.
