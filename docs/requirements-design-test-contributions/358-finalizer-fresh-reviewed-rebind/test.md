# #358 Test Contribution

- `T358-01`: a real Git fixture creates predecessor Publication, an existing PR
  head, selected-base evolution and a fresh active-task commit used directly as
  current Branch Review and Publication HEAD, with no final provenance tail or
  requirement to modify the task directory in that commit.
- `T358-02`: classifier coverage proves strict-ancestor recovery preserves the
  exact PR, current Publication, pre-push remote HEAD, metadata comparison and
  push decision.
- `T358-03`: Ready/Draft and metadata-equal/convergence execution fixtures prove
  transaction write precedes mutation, current Publication push is one, PR
  creation is zero, metadata/Ready actions remain at most one, and retry repeats
  no completed mutation.
- `T358-04`: negative cases cover reviewed/Publication mismatch, missing base
  evolution, predecessor, selected-base or predecessor-to-remote ancestry
  failure, unreviewed HEAD drift,
  malformed/extra-path/chained/merged tails and post-base business-plus-tail
  drift before PR resolution or mutation.
- `T358-05`: existing direct-tail, pure-base-evolution,
  base-evolution-plus-tail, reprepare, equal-HEAD, post-bind and terminal tests
  remain passing in canonical and installed suites with projection, ownership,
  drift, task, diff and sidecar checks.
- `T358-06`: release-wide Throwaway, tag/Release, deployment, production proof,
  PR #337 mutation and Issue closure are outside this Issue-level verification.
