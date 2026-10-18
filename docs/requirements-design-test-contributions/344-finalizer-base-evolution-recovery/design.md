# #344 Design contribution

- `D344-01`: keep the #342 provenance-tail classifier narrow and classify its
  two topology-inapplicable errors separately from identity and drift errors.
- `D344-02`: recognize legal base evolution from Git topology: the selected
  base HEAD is an ancestor of the current Publication HEAD, not the
  predecessor Publication HEAD, and the predecessor-to-current tree delta
  exactly equals the common-ancestor-to-base delta.
- `D344-03`: after that topology check, delegate to
  `classify_existing_pr_recovery()` so existing unique-PR, remote/HEAD, scope,
  metadata and Draft/Ready checks remain the single implementation.
- `D344-04`: do not create a second transaction route or alter the existing
  execute engine; its transaction-before-push and retry behavior remain the
  source of truth.
- `D344-05`: canonical Finalizer and companion spec are authoritative; preset
  apply produces dogfood, installed and declared platform projections without
  schema or architecture changes.
