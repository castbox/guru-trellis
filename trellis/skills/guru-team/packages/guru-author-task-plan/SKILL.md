---
name: guru-author-task-plan
description: Author current task planning through source-design convergence, whole-Task requirements and eight independent Delivery planning profiles.
---

# Author Task Plan

Before substantive output, read `.trellis/spec/workflow/clear-technical-writing.md`
in full and apply it within this entry's existing scope. Until that read succeeds,
use only short progress messages or concrete missing-dependency diagnostics.
State the current action or missing item; make no unverified claim. If the file
cannot be read, pause substantive output, then read it and resume the same
request when available. No additional approval is needed for that recovery.

Read `.trellis/spec/workflow/workflow-contract.md#interaction-budget` before
any confirmation, choice or clarification. This Skill retains its own action
plan, confirmation boundary and execution/recovery contract.

`judgment_mode=semantic`. Read [the authoring contract](references/authoring.md)
and [the shared planning-body contract](references/planning-body.md) before
any planning write. Actually load the applicable templates through the
[profile load table](references/authoring.md#profile-specific-body-loading);
do not treat their links or seed files as completed writing. Workflow and
standalone modes use the same current
TaskId/generation, source, checkout, upstream output and dependency checks.

This is the sole business writer: task_scope_requirements writes only the
root overall PRD; eight delivery_<original_profile> entries write that
Delivery planning_root PRD/design/implement and official JSONL. Wording owns only its controlled rewrite; Architecture
owns independent assessment; Approval owns semantic approval. Loading upstream
`trellis-brainstorm` may supply a method, but never another planning writer.

Select one closed profile from the actual original producer route. Complete
forward behavior, current AI review, any real choice/side-effect confirmation,
then invoke `scripts/invoke.sh --root <checkout> --input <json|->
--owner-result <json>`. The call-local owner result binds the exact input and
chosen output. The validator checks objective facts and emits one exit; it
does not write docs, review source commitments or choose the next route.
No persistent Author checkpoint or authorization record is created.

- `scope_requirements_ready`: `guru-task-scope-requirements-ready-router`
  passes only the actual root requirements locator to original Clarify scope
  acceptance, with fresh original source selection. It is not Task Planning.
- `requirements_ready`: `guru-task-plan-requirements-ready-router` projects the
  real candidate into original Architecture `candidate_assessment`.
- `plan_ready`: `guru-task-plan-ready-router` invokes Wording on current docs.
- `clarify_scope`: original `guru-task-plan-clarify-scope-router` invokes Clarify
  for the precise unresolved choice.
- `blocked`: stop at `task-plan-author-blocked` with the actual missing refs.

Missing/stale upstream output returns to its original owner. Unknown, multiple
or unmapped exits stop. Files alone never establish approval or activation.
