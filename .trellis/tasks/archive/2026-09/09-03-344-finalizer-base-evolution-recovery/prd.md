# #344 Finalizer base-evolution PR recovery

## Problem

`guru-finalize-task` currently treats failure of the narrow provenance-tail
transaction rebind as a terminal recovery failure. When an existing task PR's
old Publication HEAD is still the unique same-repository remote/PR HEAD, but
the current task HEAD is a valid strict descendant created through one or more
base-evolution commits or a merge, the Finalizer can incorrectly stop with
`provenance_tail_changed_paths_invalid` or `provenance_tail_parent_mismatch`.

## Goal

Allow the Finalizer to continue through the existing-PR strict-ancestor
recovery route whenever the provenance-tail route does not apply, while
preserving all existing identity, scope, metadata, transaction, and
fail-closed checks.

## Acceptance criteria

- Existing PR plus a legal base merge recovers successfully.
- Existing PR plus multiple legal base commits recovers successfully.
- The #342 single direct-child provenance-tail route remains unchanged.
- Provenance-tail inapplicability does not block a valid existing-PR
  strict-ancestor recovery.
- Recovery pushes the current Publication HEAD once, creates zero PRs, and a
  same-plan retry performs no duplicate push.
- Business-content changes, scope/PR drift, multiple or fork PRs, and
  conflicting transactions remain fail closed.
- Canonical, dogfood, installed, and declared platform projections remain
  consistent.

## Boundaries

This task does not reimplement #333, modify PR #337, close #249, or expand to
release-wide, tag, deployment, or production-proof work.
