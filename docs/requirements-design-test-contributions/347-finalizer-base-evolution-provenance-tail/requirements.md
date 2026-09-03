# #347 Requirements contribution

- `R347-01`: an unbound predecessor `ordinary_publication/push_content`
  transaction may recover when legal base evolution is followed by one valid
  direct-child provenance metadata tail.
- `R347-02`: the complete tail must pass the existing provenance validator;
  the existing base-evolution ancestry and exact binary-delta comparison then
  uses the validated tail parent as its current endpoint.
- `R347-03`: task/repository/base/head, Publication payload, close scope,
  transaction, remote/PR HEAD, unique same-repository Open PR, metadata and
  Draft/Ready checks remain exact.
- `R347-04`: recovery reuses the existing strict-ancestor transaction engine,
  writes current owner state before mutation, pushes the current Publication
  once, creates no PR, and repeats no completed mutation on same-plan retry.
- `R347-05`: #342 direct-tail, #344 pure-base-evolution and #338 equal-HEAD
  paths remain unchanged; invalid tails, business drift and identity/scope/PR/
  transaction drift remain fail-closed.
- `R347-06`: the current validator supports one direct-child tail; arbitrary
  multi-tail recovery, public Interface changes, new transaction stages and
  new schema identities remain outside this contribution.
