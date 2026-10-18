# #347 Design contribution

- `D347-01`: retain the current direct-tail classifier and pure-base-evolution
  classifier, then compose them only for provenance-shape inapplicability.
- `D347-02`: derive the current Publication parent from Git facts and validate
  the complete child commit with `provenance_tail_commit_errors()` before using
  that parent as a base-evolution endpoint.
- `D347-03`: reuse the #344 ancestry, merge-base and binary-delta comparison;
  do not filter the manifest path or introduce another business-drift owner.
- `D347-04`: delegate successful composition to
  `classify_existing_pr_recovery()` and the existing transaction-before-push,
  metadata, archive, Ready and terminal replay engine.
- `D347-05`: canonical Finalizer runtime/tests/contracts are the source and
  preset apply creates installed/platform copies; no public graph, schema,
  persistence owner or Architecture boundary changes.
