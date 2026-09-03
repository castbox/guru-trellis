# #342 Requirements contribution

- `R342-01`: only an unbound predecessor `ordinary_publication/push_content`
  transaction may rebind across one valid direct-child provenance metadata tail.
- `R342-02`: predecessor task/repository/base/head, Publication payload and close
  scope remain exact; predecessor Publication HEAD equals live remote/PR HEAD.
- `R342-03`: preview reports existing-PR strict ancestry, `push_required=true`,
  exact old/new HEADs, metadata decision and Ready action without mutation.
- `R342-04`: execute writes one current-plan bound
  `existing_pr_recovery/push_content` transaction before pushing the new
  Publication HEAD exactly once; PR creation remains zero.
- `R342-05`: metadata convergence, archive, archive push, Ready preservation or
  Draft-to-Ready and same-plan retry reuse the existing transaction engine.
- `R342-06`: business/invalid tails and identity, scope, PR, HEAD, metadata,
  gate, archive or transaction drift fail before mutation.
- `R342-07`: #338 exact equal-HEAD `push_required=false` behavior remains
  unchanged; public Interface, typed exits, owner boundary and schema 3.0 remain
  unchanged.
