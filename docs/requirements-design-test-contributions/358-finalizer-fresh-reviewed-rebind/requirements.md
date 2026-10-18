# #358 Requirements Contribution

- `R358-01`: an unbound predecessor `ordinary_publication/push_content`
  transaction may recover when the current Branch Review and Publication bind
  the same fresh task-content commit after legal selected-base evolution,
  without requiring an additional provenance metadata tail.
- `R358-02`: the predecessor Publication and selected base must both be
  ancestors of the current reviewed commit, while the selected base must not be
  an ancestor of the predecessor Publication. Fresh Phase 2, Task Commit,
  Branch Review and Publication identity distinguish this route from unreviewed
  drift without requiring the commit to modify the task directory again.
- `R358-03`: the unique same-repository Open PR and remote branch must agree on
  a commit descended from predecessor Publication and strictly ancestral to the
  current Publication. Recovery retains that exact pre-push remote HEAD and
  delegates metadata and Draft/Ready handling to the existing strict-ancestor
  classifier.
- `R358-04`: execute writes the current-plan
  `existing_pr_recovery/push_content` transaction before mutation, pushes the
  current Publication once, creates no PR, and repeats no completed mutation on
  same-plan retry.
- `R358-05`: direct-tail, pure-base-evolution, base-evolution-plus-tail,
  equal-HEAD, post-bind and terminal recovery remain compatible. Invalid tails,
  unreviewed drift, identity/scope/PR/remote/transaction drift and stale review
  or Publication identity remain fail-closed.
- `R358-06`: no public DTO, typed exit, transaction mode/stage, schema identity,
  persistence owner or Architecture boundary is added.
