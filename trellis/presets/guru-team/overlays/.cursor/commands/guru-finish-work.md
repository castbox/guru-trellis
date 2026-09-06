<!-- guru-team-overlay: v1 -->
# Guru Finish Work

Load current task, repository, and phase facts with the live context helpers,
then read `.trellis/workflow.md`. Use its Phase 3.6/3.7 route and mandatory load
these active owners by stable Skill id:

This is the exclusive finish entry for a Guru task. The upstream-owned
`trellis-finish-work` Skill is not applicable to Guru tasks and must not be
loaded or invoked. Before Finalizer, do not call `task.py archive`,
`add_session.py`, or any archive/journal executor.

All GitHub platform operations use authenticated, explicitly repo-bound
`gh`/`gh api` only. Do not use or fall back to App, MCP, connector, or browser
UI; keep Git transport on `git`.

- `guru-review-task-publication`
- `guru-finalize-task`
- `guru-merge-task-pr`

Consume only their current public typed exits and mapped workflow consumers:

- Publication `ready` enters finalization; `return_to_task_work` resumes the
  complete Phase 2 route; `blocked` stops with its concrete reason.
- Finalization `publication_review_stale` re-enters publication review, and
  `resume_finalization` or `reprepare_required` re-enters finalization.
  `ready_for_merge` enters `guru-merge-task-pr`; `blocked` stops with its
  concrete reason.
- Merge `merged` is terminal; `merge_blocked` and `closure_mismatch` stop with
  their concrete reason.

Missing, stale, unknown, multiple, or unmapped exits fail closed. Mapped
stale, resume, and reprepare transitions are internal workflow
routes, not user choices. Do not add a routine confirmation between them.
When the user gives a clear affirmative such as `确认继续` for the exact action
just displayed, consume it for that action without asking them to repeat its
SHA, digest, PR, or plan identity. Continue mapped internal exits automatically.
Finalizer side effects and expected-head merge each keep their own exact
dialogue-local confirmation; new external authority or a material scope decision
may also pause the route.

Do not call deterministic closeout scripts directly, reproduce package
internals or artifact schemas, or create a handoff artifact. Return only the
terminal `merged` result or the concrete declared blocker.
