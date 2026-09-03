# #344 Requirements contribution

- `R344-01`: an unbound predecessor `ordinary_publication/push_content`
  transaction may recover through existing-PR strict ancestry after a legal
  base evolution or merge.
- `R344-02`: fallback is allowed only for the two inapplicable provenance-tail
  topology errors and only when the selected base HEAD is present in the
  current Publication history but absent from the predecessor Publication
  history.
- `R344-03`: task/repository/base/head, Publication payload, close scope,
  transaction identity, unique PR, remote HEAD and PR HEAD checks remain exact;
  business-content, scope, PR and conflicting-transaction drift fail closed.
- `R344-04`: fallback reuses existing strict-ancestor recovery, preserving one
  current Publication push, zero PR creation, metadata convergence, archive,
  Ready handling and same-plan retry idempotence.
- `R344-05`: #342 direct-child provenance metadata-tail and #338 equal-HEAD
  recovery remain unchanged; public Interface, typed exits and schema remain
  unchanged.
