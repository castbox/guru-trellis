# #342 Design contribution

- `D342-01`: place a narrow predecessor rebind classifier before generic
  current-transaction base-evolution supersession.
- `D342-02`: validate fixed transaction/plan fields and delegate both historical
  and current tail continuity to `provenance_tail_commit_errors()`.
- `D342-03`: require the predecessor Publication HEAD at the unique live remote
  and PR, then reuse `classify_existing_pr_recovery()` for strict ancestry,
  scope and metadata comparison.
- `D342-04`: execute rereads the preview facts and directly persists the final
  current-plan `existing_pr_recovery/push_content` transaction; there is no
  rebound ordinary intermediate state.
- `D342-05`: retain original metadata comparison and Draft/Ready state in the
  existing additive `adopted_pr` shape, then reuse push, bind, archive,
  push-archive, Ready and terminal recovery transitions.
- `D342-06`: canonical Finalizer is the only source; preset apply generates
  installed and platform copies. No schema, public graph or architecture owner
  changes.
