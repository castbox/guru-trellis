# Task Finalization Contract

## Current Boundary

`guru-finalize-task` is the semantic owner of business-task closeout. Its
current aggregate input is 6.0, gate is 5.0, and ignored transaction is 3.0.
The four inputs are `publication_ready`, `same_plan_resume`,
`reprepare_preview`, and `standalone_finalization`. The six exits are
`base_reconciliation_required`, `publication_review_stale`, `resume_finalization`, `reprepare_required`,
`ready_for_merge`, and `blocked`.

Extension installation verification is unreachable from this package. Changed
paths, installed extension manifests, documentation, configuration, `.trellis`
files, and platform copies never create verifier applicability. Finalizer does
not read or write `marketplace-verification.json`, verifier owner state,
verification refs, or verifier recovery state.

## Transaction

The deterministic transaction states are `push_content`, `bind_pr`, `archive`,
`push_archive`, and `mark_ready`. There is no `verify` state. Transaction mode
is exactly `ordinary_publication` or `existing_pr_recovery`. Ordinary mode still
requires no Open PR before its first mutation. Recovery mode binds the unique
same-repository PR, its initial Draft/Ready state, exact pre-push remote HEAD,
publication HEAD and reviewed scope before mutation. Fresh adoption requires a
strict-ancestor HEAD; equality is accepted only by the same bound recovery
transaction after its exact push. It pushes only the exact publication commit by fast-forward,
converges title/body from current Publication, preserves Ready, or applies the
existing Draft-to-Ready transition.

Once the transaction has reached `ready`, execute performs only terminal live
revalidation and materializes the current `ready_for_merge` DTO. It does not
call the Draft-only finish path or repeat push, PR, archive, commit, or Ready
mutations. The public invocation retires owner-private state only after
consuming that validated terminal DTO.

## Migration

The 5.0 aggregate, verification re-entry schemas, verification-required output,
3.0 and 4.0 gates, 2.0 semantic-review input, and 1.0/2.0 transactions are immutable
legacy assets with explicit versioned filenames. Unversioned gate and semantic
review schemas/examples are current 5.0/3.0 assets and route to Merge. They are not
current profiles, outputs, projections, or private artifacts. A retired
task-bearing verification input or `next_transition=verify` fails closed with
remediation to rerun current Publication and rebuild Finalizer state. No
automatic projection or dual route is supported.

Recovery never treats an arbitrary prior push as authority. PR/remote identity,
pre-push HEAD, Publication payload, Issue close scope, original Draft/Ready
state, archive transaction, or three-way HEAD drift fails closed. The final
public output remains only `ready_for_merge`; recovery facts stay owner-private.

## Typed Exits

Every current exit has exactly one Interface-declared consumer. Unknown,
multiple, retired, or unmapped exits stop fail closed. Only
`ready_for_merge` enters `guru-merge-task-pr`; it is not completion.
Before the first publication side effect, a selected-base HEAD that differs
from the task's base anchor returns `base_reconciliation_required` with the
exact pair and `finalization_resume`. This route is distinct from
`publication_review_stale`, which is reserved for Publication content or
metadata evidence. Finalizer does not interpret the base delta.
