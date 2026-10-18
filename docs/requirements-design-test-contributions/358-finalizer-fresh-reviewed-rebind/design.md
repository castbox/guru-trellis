# #358 Design Contribution

- `D358-01`: preserve direct-tail, pure-base-evolution,
  base-evolution-plus-tail and reprepare classification order, then try one
  direct reviewed-descendant predicate only for provenance-shape
  inapplicability.
- `D358-02`: the package-private predicate requires the comparison commit to be
  the current Branch Review identity, satisfy current Publication ancestry,
  and descend from predecessor and selected base after real base evolution.
  Fresh review/publication identity remains the authority; no changed-path
  heuristic is added.
- `D358-03`: after direct qualification, resolve the unique Open PR and exact
  remote HEAD, require that HEAD to descend from predecessor Publication, then
  reuse `classify_existing_pr_recovery()` for strict ancestry, metadata
  comparison, close scope and Draft/Ready state. Only this direct classification
  may use a remote HEAD newer than the predecessor Publication.
- `D358-04`: transaction conversion copies the classifier's exact
  `pre_push_remote_head` into the existing schema 3.0 recovery binding before
  the first push; all later metadata, archive, Ready and retry behavior remains
  owned by the current transaction engine.
- `D358-05`: canonical Finalizer runtime/tests/contracts remain the source;
  preset apply creates installed and platform projections without adding a new
  public interface or workflow state.
