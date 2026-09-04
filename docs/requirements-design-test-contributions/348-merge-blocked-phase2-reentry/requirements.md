# #348 Requirements Contribution

Candidate identity: `rdt-contribution-348-merge-blocked-phase2-reentry-v1`.
Source baseline `current-main-0.6.5-guru.43` is superseded. PR #351's reviewed
contract was serialized into shared `current-main-0.6.5-guru.44`; this file
remains the historical task-owned source and authorizes no further shared write.

- `R348-01`: When Merge identifies an in-scope task-content finding for an
  archived task and an open same-head PR, the workflow must expose one typed
  Phase 2 re-entry route without merge confirmation or remote mutation.
- `R348-02`: Provider, permission, ruleset, external-service, scope, head,
  branch, PR, closure, task, archive, or workspace drift must remain blocked
  before recovery writes.
- `R348-03`: Recovery must reuse the original Issue, task, branch, worktree,
  remote branch, and PR, restore `in_progress` status, and remove stale
  downstream authority.
- `R348-04`: The same identity must support interrupted or lost-output retry
  without duplicate objects or repeated archive movement.
- `R348-05`: A successful restore must rerun Phase 2, Task Commit, full-diff
  Branch Review, Publication, Finalizer/Delivery, and expected-head Merge.
- `R348-06`: Canonical, installed, workflow, schema, example, eval, docs, and
  Shared/Codex/Claude/Cursor projections must remain consistent.

Inherited current authority: `REQ-001`, `REQ-005`, `REQ-011`, `REQ-012`,
`REQ-014`, `BEH-003`, `BEH-005`, `BEH-006`, `BEH-008`, and `BEH-010`.
