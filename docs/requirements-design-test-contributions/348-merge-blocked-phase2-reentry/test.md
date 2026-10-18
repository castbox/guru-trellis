# #348 Test Contribution

- `T348-01`: Merge contract/runtime test proves the new route is selected only
  for an AI-reviewed current-scope content finding and performs no GitHub write.
- `T348-02`: Recovery success test proves archive-to-active restoration, status
  repair, mapping repair, current-task update, and stale authority cleanup.
- `T348-03`: Idempotent retry test proves exact already-restored state creates
  no duplicate task, branch, worktree, or PR and repeats no archive move.
- `T348-04`: Negative tests cover external blocker, head drift, scope drift,
  dirty worktree, different active task, merged PR, and unsafe/ambiguous paths
  with zero business writes.
- `T348-05`: Package/interface/registry/workflow tests prove unique consumers,
  declared exits, command ownership, schema closure, and source/installed graph
  consistency.
- `T348-06`: Preset reapply, dogfood drift, sidecar/residue, Python compile,
  shell syntax, task validation, and `git diff --check` cover the current
  repository projection.

Inherited strategy: `TST-004`, `TST-011`, `TST-012`, `TST-018`, `SCN-002`,
`SCN-003`, `SCN-004`, `SCN-008`, and `SCN-009`.

The complete multi-platform throwaway, upgrade/update, release, and production
matrices remain unverified and outside this ordinary Issue's validation scope.
