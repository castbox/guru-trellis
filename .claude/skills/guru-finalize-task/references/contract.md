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

## Provenance Source And Target Binding

Pre-PR provenance reprepare owns two independent temporary checkouts. The
detached `target_reviewed_checkout` belongs to the task repository at
`reviewed_content_head`; it is the only preset `--repo` target, manifest
mutation owner, metadata-tail parent, and publication-lineage owner. The
detached `extension_source_checkout` supplies only canonical Guru Trellis
preset implementation bytes and must remain clean. The two paths remain
separate in every mode.

Finalizer resolves one private closed binding from the target reviewed
manifest and the plan's canonical target repository identity:

- `self_hosted` applies when source and target repository identities match. It
  preserves #191 reprepare by accepting stale dirty/mutable manifest preimage,
  but binds the new source checkout and postimage ref/commit to
  `reviewed_content_head`.
- `installed` applies when the identities differ. It requires the manifest's
  canonical GitHub repo, equal full-OID ref/commit, `tree_state=clean`, and
  `is_mutable_ref=false`; then it initializes an independent repository,
  configures canonical `origin`, fetches that exact OID, checks out detached,
  and validates repository identity, HEAD, and clean state.

There is no fallback to the target tree, a mutable ref, hidden checkout, PATH
package, global installation, or verifier runtime. The apply executable comes
from `extension_source_checkout` and receives `target_reviewed_checkout`
through `--repo`. Apply must leave source identity and clean state unchanged and
may dirty only `.trellis/guru-team/extension.json` in the target. The existing
field allowlist remains closed. The committed tail has exactly one parent equal
to target `reviewed_content_head`; self-hosted postimage source ref/commit equal
that head, while installed postimage repo/ref/commit preserve the selected
immutable extension identity. Any failure stops before push, PR, archive,
Ready, or Issue mutation and does not add a public profile, exit, transaction
state, checkpoint, or verifier result.

Initial `publication_ready` preview classifies the unique existing PR before
fresh provenance inference. If no PR and no remote branch exist, the ordinary
plan remains `prepared`; when it has no metadata tail and its installed binding
requires one, preview returns `reprepare_required` with reason
`provenance_metadata_tail`. This preview is side-effect-free and does not push,
create a PR, archive, mark Ready, or mutate the Issue. A matching existing-PR
recovery, including its exact post-bind transaction, retains precedence.

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

Once that exact transaction owns `archive`, `push_archive`, or `mark_ready`, its
bound PR, payload, close scope, plan digest, and HEAD identities are validated
before any pre-PR provenance inference. A matching post-bind recovery continues
from its recorded transition; any mismatch fails closed instead of falling back
to fresh PR adoption or provenance reprepare.

If archive move, commit, and push complete before Draft-to-Ready succeeds, the
archived task retains the exact `archive`/`push_archive` transaction stage. A
same-plan retry validates the archived task, the bound PR's recorded initial
Draft/Ready state, and three-way archive
HEAD, performs only the remaining Ready transition, then persists `mark_ready`
and retires owner state. It never reruns archive or creates a second PR.

Current preparation retires a historically tracked but already deleted
`closeout-plan.json` through the private archive projection. The path is absent
from move, retained, required, and reviewed-binding sets, but remains an exact
active-side deletion in the archive transaction with parent-blob continuity.
It is never materialized or copied into the current archive.
If a post-bind transaction still carries the predecessor projection digest,
preview accepts the current digest only when that predecessor digest equals the
deterministic reverse projection with `closeout-plan.json` restored to the
tracked move set, every other transaction field is byte-for-byte identical,
and this single retired path is present. Executor then persists that same
minimal digest projection before continuing; any unrelated digest fails closed.

Once the transaction has reached `ready`, execute performs only terminal live
revalidation and materializes the current `ready_for_merge` DTO. It does not
call the Draft-only finish path or repeat push, PR, archive, commit, or Ready
mutations. The public invocation retires owner-private state only after
consuming that validated terminal DTO.

After that terminal cleanup, public invoke may receive the exact retired gate
locator emitted by the completed checker. Its authority is then the committed
archive terminal state, not the obsolete in-progress Publication state: the
wrapper reconstructs only the private executor marker and requires current
local/remote/Ready PR HEAD to remain the exact reviewed archive metadata commit.
It rechecks that commit's active-task deletion, six-file archive tree,
reviewed-content continuity, PR/head/branch/close-Issue facts and output schema before
projecting `ready_for_merge`. A different locator, a surviving transaction
without its gate, an unsafe gate path, or any terminal fact drift remains
fail-closed and never falls back to reprepare.

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

`publication_review_stale` is valid before a closeout plan or transaction
exists. Its `task_ref`, `branch_review_commit`, and `stale_reason` bind the
current public input and the Publication owner facts exactly; in particular,
the commit is `publication_branch_review_commit`, not a value inferred from a
missing plan or the current HEAD. The route is accepted only while Publication
is `stale` and the current transaction state is `publication_review_stale`.
Every plan-backed exit continues to bind the immutable plan commit,
publication HEAD, plan ref, and its existing recovery-state contract.
