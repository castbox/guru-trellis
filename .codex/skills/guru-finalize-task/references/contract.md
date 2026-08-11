# Task Finalization Contract

## Current Boundary

`guru-finalize-task` is the semantic owner of business-task closeout. Its
current aggregate input is 6.0, gate is 4.0, and ignored transaction is 2.0.
The four inputs are `publication_ready`, `same_plan_resume`,
`reprepare_preview`, and `standalone_finalization`. The five exits are
`publication_review_stale`, `resume_finalization`, `reprepare_required`,
`ready_for_merge`, and `blocked`.

Extension installation verification is unreachable from this package. Changed
paths, installed extension manifests, documentation, configuration, `.trellis`
files, and platform copies never create verifier applicability. Finalizer does
not read or write `marketplace-verification.json`, verifier owner state,
verification refs, or verifier recovery state.

## Transaction

The deterministic transaction states are `push_content`, `bind_draft`,
`archive`, `push_archive`, and `mark_ready`. There is no `verify` state. After
content push, the transaction continues directly to the unique Draft PR and
the existing archive/Ready sequence. Publication freshness, repository/ref/HEAD
identity, PR uniqueness, Issue scope, archive projection, confirmation, and
recovery checks retain their existing ownership.

## Migration

The 5.0 aggregate, verification re-entry schemas, verification-required output,
3.0 gate, and 1.0 transaction are immutable legacy assets. They are not current
profiles, outputs, projections, or private artifacts. A retired task-bearing
verification input or `next_transition=verify` fails closed with remediation to
rerun current Publication and rebuild Finalizer state. No automatic projection
or dual route is supported.

## Typed Exits

Every current exit has exactly one Interface-declared consumer. Unknown,
multiple, retired, or unmapped exits stop fail closed. Only
`ready_for_merge` enters `guru-merge-task-pr`; it is not completion.
