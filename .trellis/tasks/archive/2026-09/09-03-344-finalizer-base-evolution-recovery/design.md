# Design

## Current behavior

The current Finalizer checks an unbound
`ordinary_publication/push_content` transaction against
`classify_provenance_tail_transaction_rebind()`. That classifier raises when
the current descendant is not the exact one-commit manifest-only tail required
by #342. The caller then does not get a chance to classify the same live PR
through the already-supported strict-ancestor recovery engine.

## Proposed behavior

Keep the #342 classifier narrow and fail-closed for its own candidate shape,
but distinguish “this transaction is not a provenance-tail candidate” from a
real identity or remote/PR conflict. When the provenance-tail topology is not
applicable, route the unchanged predecessor transaction and current plan to
the existing-PR strict-ancestor classifier. The fallback must require:

- exact task, repository, base/head branch, Publication title/body, and close
  scope identity;
- one unique same-repository Open PR with matching branch/base;
- remote branch HEAD equal to PR HEAD and equal to the predecessor Publication
  HEAD before the recovery push;
- current Publication HEAD a strict descendant of that predecessor HEAD;
- unchanged metadata comparison and initial Draft/Ready state;
- transaction persistence before the single content push.

The fallback must not widen equal-HEAD adoption, bypass #342, rewrite owner
state on failure, create another PR, or convert business-content/scope/PR
drift into a recoverable case.

## Files and projections

Primary implementation and focused tests live in the canonical
`guru-finalize-task` package. Update its contract/spec evidence only where the
new routing contract is not already represented, then regenerate or apply the
existing preset projections so `.agents`, `.codex`, `.cursor`, `.claude`, and
`.trellis/guru-team` remain byte/semantic consistent.

## Alternatives rejected

- Treating every provenance-tail error as recoverable would weaken
  fail-closed behavior for identity and business-content drift.
- Removing provenance-tail recovery would regress #342.
- Reusing generic base-evolution supersession would lose the existing PR's
  strict-ancestor identity and duplicate-mutation guarantees.
