<!-- guru-team-overlay: v1 -->
# Guru Finish Work

Load current task, repository, and phase facts with the live context helpers,
then read `.trellis/workflow.md`. Use its Phase 3.6/3.7 route and mandatory load
these active owners by stable Skill id:

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
Finalizer side effects and expected-head merge each keep their own exact
dialogue-local confirmation; new external authority or a material scope decision
may also pause the route.

Do not call deterministic closeout scripts directly, reproduce package
internals or artifact schemas, or create a handoff artifact. Return only the
terminal `merged` result or the concrete declared blocker.
