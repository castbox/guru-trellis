# #348 Design Contribution

- `D348-01`: `guru-merge-task-pr` retains semantic ownership of task-work
  classification and adds `phase2_reentry_required` beside the unchanged
  external `merge_blocked` stop route.
- `D348-02`: The re-entry DTO carries only exact repository, PR/head/branch,
  Issue, task/archive, finding, and `resume_target=phase-2` identity.
- `D348-03`: `guru-restore-archived-task` is the sole recovery owner. Its AI
  boundary rereads live facts; its command validates closed identity and owns
  only deterministic local restoration.
- `D348-04`: The transaction restores archive to the canonical active locator,
  changes task status to `in_progress`, repairs owner-private mapping/current
  task state, and removes stale Phase 2/review/publication/finalization files.
- `D348-05`: Exact already-restored state is read-only success; ambiguous,
  dirty, duplicate, stale, merged, or external-blocked state is zero-write
  failure.
- `D348-06`: Workflow routes restoration success only to
  `guru-resume-implementation`; all downstream owners rerun from fresh evidence.

Inherited design authority: `DES-004`, `DES-005`, `DES-011`, `DES-012`,
`DES-027`, `CON-004`, and the cross-domain typed-projection boundary.
