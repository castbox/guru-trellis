<!-- guru-team-overlay: v1 -->
# Guru Team Continue Current Task

Read current state instead of replaying remembered steps:

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode phase
```

Use `.trellis/workflow.md` as the global route and load each mandatory owner by
stable Skill id. This entry never copies a package schema, evidence recipe,
review loop, confirmation algorithm, or typed-exit payload.

## Route

- `planning`: complete proportionate planning and invoke
  `guru-approve-task-plan`. Only `approved` may enter implementation.
- `in_progress`: validate the workspace and current planning approval,
  implement, then invoke `guru-check-task`. Use terminal output and the live
  diff directly; do not create `implementation-handoff.md` or routine liveness
  prose. Batch qualified findings before another check and commit cycle.
- after Phase 2: invoke `guru-create-task-commit`, then
  `guru-review-branch`. Automatically consume declared revision routes; stop
  only for missing authority, unresolved scope, or a real blocker.
- after Branch Review `passed`: prepare current publication candidates and
  invoke `guru-review-task-publication`. Automatically consume internal
  metadata-revision routes. `ready` enters the explicit finalization entry.

Do not expose internal digests, recorder steps, `verification_required`,
`resume_finalization`, or other machine routes as user decisions. Ask only for
missing intent, a material scope/plan choice, new external authority, or the
bounded publication/finalization side effects. A generic `确认继续` must never be
required between automatically mapped Skill exits.

Before a planning, review, or publication stop, run:

```bash
.trellis/guru-team/scripts/bash/resolve-human-artifacts.sh --json --task <task-path>
```

Show only existing human-authored artifacts. JSON gates remain internal. All
task paths must resolve inside the task worktree. This entry never stages,
commits, pushes, creates a PR, archives a task, or invokes finalization itself.
