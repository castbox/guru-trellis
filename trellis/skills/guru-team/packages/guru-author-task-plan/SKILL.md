---
name: guru-author-task-plan
description: Author current task planning through source-design convergence, candidate Architecture assessment, and eight closed revision profiles.
---

# Author Task Plan

`judgment_mode=semantic`. Read [the authoring contract](references/authoring.md)
before any planning write. Workflow and standalone modes use the same current
TaskId/generation, source, checkout, upstream output and dependency checks.

This is the sole business writer of `prd.md`, `design.md`, `implement.md` and
official planning JSONL. Wording owns only its controlled rewrite; Architecture
owns independent assessment; Approval owns semantic approval. Loading upstream
`trellis-brainstorm` may supply a method, but never another planning writer.

Select one closed profile from the actual original producer route. Complete
forward behavior, current AI review, any real choice/side-effect confirmation,
then invoke `scripts/invoke.sh --root <checkout> --input <json|->
--owner-result <json>`. The call-local owner result binds the exact input and
chosen output. The validator checks objective facts and emits one exit; it
does not write docs, review source commitments or choose the next route.
No persistent Author checkpoint or authorization record is created.

- `requirements_ready`: `guru-task-plan-requirements-ready-router` projects the
  real candidate into original Architecture `candidate_assessment`.
- `plan_ready`: `guru-task-plan-ready-router` invokes Wording on current docs.
- `clarify_scope`: original `guru-task-plan-clarify-scope-router` invokes Clarify
  for the precise unresolved choice.
- `blocked`: stop at `task-plan-author-blocked` with the actual missing refs.

Missing/stale upstream output returns to its original owner. Unknown, multiple
or unmapped exits stop. Files alone never establish approval or activation.
