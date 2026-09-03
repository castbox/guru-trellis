# #347 Test contribution

- `T347-01`: a real Git fixture creates predecessor Publication, multiple base
  commits, a legal merge, and one final valid manifest-only provenance tail.
- `T347-02`: the fixture proves the tail validator accepts the final commit,
  the pre-fix current-endpoint comparison fails, and the validated-parent
  composition returns strict-ancestor recovery.
- `T347-03`: execution coverage proves the current Publication push count is
  one, PR creation is zero, transaction write precedes mutation, metadata and
  Ready actions retain their existing counts, and terminal retry repeats none.
- `T347-04`: negative cases cover extra paths, invalid manifest changes, wrong
  parent, merge/chained tails, post-base business drift, and existing task/repo/
  base/head/scope/PR/transaction conflicts.
- `T347-05`: existing #342, #344 and #338 tests remain passing together with
  source/installed Finalizer tests, finish-family integration, preset reapply,
  ownership, drift, package/task, diff and sidecar checks.
- `T347-06`: release-wide Throwaway, tag/Release, deployment and production
  proof are not part of this Issue-level verification.
