<!-- guru-team-overlay: v1 -->
# Guru Finish Work

Load current task, repository, and phase facts with the live context helpers,
then read `.trellis/workflow.md`. Use its Phase 3.6/3.7 route and mandatory load
these active owners by stable Skill id:

- `guru-review-task-publication`
- `guru-verify-extension-installation`
- `guru-finalize-task`

Consume only their current public typed exits and mapped workflow consumers:

- Publication `ready` enters finalization; `return_to_task_work` resumes the
  complete Phase 2 route; `blocked` stops with its concrete reason.
- Finalization `verification_required` enters extension verification,
  `publication_review_stale` re-enters publication review, and
  `resume_finalization` or `reprepare_required` re-enters finalization.
  `published` is terminal; `blocked` stops with its concrete reason.
- Verification `verified` or `not_required` returns to finalization,
  `return_to_task_work` resumes the complete Phase 2 route, and `blocked` stops.

Missing, stale, unknown, multiple, or unmapped exits fail closed. Mapped
verification, stale, resume, and reprepare transitions are internal workflow
routes, not user choices. Do not add a routine confirmation between them; only
the exact side-effect plan confirmation owned by `guru-finalize-task`, new
external authority, or a material scope decision may pause the route.

Do not call deterministic closeout scripts directly, reproduce package
internals or artifact schemas, or create a handoff artifact. Return only the
terminal `published` result or the concrete declared blocker.
