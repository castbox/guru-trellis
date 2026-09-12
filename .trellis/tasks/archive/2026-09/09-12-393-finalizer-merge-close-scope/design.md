# Design

## Boundary And Ownership

`guru-review-task-publication` owns interpretation of the reviewed PR body and the distinction between issue-scope evidence and close-keyword evidence. `guru-finalize-task` owns the closeout plan and produces the minimal `ready_for_merge` consumer input. `guru-merge-task-pr` owns execution and exact validation of the merge close set. The workflow only routes typed exits.

## Data Flow

1. Publication keeps the ledger-derived delivery scope for review, while retaining the parsed PR close-keyword set as the merge intent.
2. Finalizer derives `expected_close_issues` from that reviewed merge-intent set, not from the complete ledger `close_issues` collection.
3. Normal ready output, existing-PR recovery, and terminal recovery use the same projection rule.
4. Merge receives an ordered unique set, compares it byte-for-byte with the PR body parser result, and uses the existing empty-set branch for refs-only.

The implementation should prefer an existing parser/helper and a direct projection change. If current Publication evidence does not retain the parsed set across all recovery paths, extend the smallest existing owner-private field or derive it from the already-reviewed PR body at the Finalizer boundary; do not add a parallel ledger or compatibility alias.

## Compatibility

This is direct evolution of internal DTOs and owner-private recovery state. Existing non-empty `Closes` behavior remains unchanged. Existing persisted archives/results are historical evidence and are not rewritten. Old terminal outputs that contain the old incorrect non-empty set must fail freshness/recovery validation or route through the existing reprepare path rather than being silently reinterpreted.

## Recovery And Failure Behavior

- Fresh refs-only path: `expected_close_issues=[]`; Merge skips Issue reads/effects after its normal preflight.
- Fresh non-empty path: exact parsed keyword set remains required.
- Existing PR/terminal recovery: recompute the same set from current reviewed PR body and compare against the current transaction/review identity.
- Any body drift, unsupported keyword, stale predecessor, or inconsistent set remains fail closed through existing mismatch/reprepare exits.

## Architecture And Maintainability

No new public Skill, route, authorization field, persistent ledger, retry, lock, or fallback is needed. The change remains within the existing three package owners and their public projections. Any touched non-generated Python file over 3000 lines requires a separate reviewed mechanical split before implementation; otherwise this task does not expand into a refactor.

## Rollback

Rollback is a source-level revert of the bounded projection and tests before publication. No database, external configuration, or business repository migration is involved.
