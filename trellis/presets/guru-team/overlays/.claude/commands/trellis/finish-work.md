<!-- guru-team-overlay: v1 -->
# Guru Team Finish Work

Read live state before choosing a closeout step:

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

Use `.trellis/workflow.md` as the global route and load each mandatory semantic
owner by stable Skill id. This entry does not copy package schemas, evidence
recipes, confirmation algorithms, transaction commands, or recovery internals.

## Route

- If current Branch Review evidence is not `passed`, return to the workflow step
  that owns the missing review or task work. Do not manufacture publication
  readiness here.
- After Branch Review `passed`, follow Phase 3.6: prepare only the current
  publication candidates required by the workflow, then invoke
  `guru-review-task-publication`. Automatically consume its metadata revision
  route; real task findings return to the complete downstream review sequence.
- Only `guru-review-task-publication:ready` enters Phase 3.7 and invokes
  `guru-finalize-task`. That Skill owns plan review, exact side-effect
  confirmation, the deterministic transaction boundary, and recovery intent.
- Automatically consume finalizer `verification_required` through
  `guru-verify-extension-installation`, `publication_review_stale` through
  `guru-review-task-publication`, and same-plan `resume_finalization` or
  `reprepare_required` through `guru-finalize-task`. Do not render these internal
  exits as user choices.
- Return only the final `published` result. A declared `blocked` result, missing
  external authority, or a materially changed side-effect plan stops with its
  concrete reason.

Ask the user only for the exact bounded finalization side-effect plan when the
semantic owner requires confirmation, for new external authority, or for a
material scope decision. Never ask for a generic `确认继续` between mapped Skill
exits or ask the user to select an internal recovery command.

Deterministic closeout scripts are private implementation details of
`guru-finalize-task`; this entry never invokes them directly. It does not create
a handoff artifact or duplicate live Git, GitHub, task, review, publication, or
finalizer evidence.
