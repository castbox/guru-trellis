Read and apply `.trellis/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage`
for shared candidate coverage, engineering facts and recovery. This package
retains its own current judgment, formal result and action boundary.

## Public Delivery integration 1.0

### Bounded private transaction migration

The original Publish owner reads its exact old cycle/Task/generation, actual
PR/head/payload and retry stage before invoking owner-private
`scripts/migrate-delivery-transaction.sh --input <migration> --owner-result <actual-review>`.
`historical_publication_migration` is separate from
`inflight_publication_migration` in the private 1.0 input schema. Historical
Ready recovery rereads actual PR postconditions and binds the owner-selected
original candidate; private `readiness_result_id=null` denotes no current gate,
and is never a public input/pass. Incomplete transactions require a fresh real
Readiness output covering the unchanged action before binding the new key.
The exact transaction reference, stage, decisions and performed side effects
remain; no remote mutation or gate is produced. Public same-plan resume then
recovers the original publication fact and independently routes current
readiness. Upgrade only consumes the intermediate transaction ref for backup,
same-plan recovery and exact rollback; it cannot choose cycle attribution.

This current Skill consumes the target installation's reviewed Delivery API
1.0 and Task schema 2.0 through a thin projection. `task_ref` is a locator;
`delivery_key` is the opaque public identity. Read the current `interface.json`
profile schema and its exact exit consumer before invoking. Do not derive an
identity from branch, worktree, legacy cycle, PR, or Task status. D1 and later
Deliveries use the same entry and lifecycle. The public phase never proves a
semantic pass. Historical facts never prove a currently applicable gate.

Read the Delivery's public `planning_root` for its three planning documents and
context JSONL; Task-root PRD remains overall scope. Rework keeps the Delivery
identity and returns through the real current stage owner's public operation to
the earliest affected role. Invalidate only the affected results. Unchanged,
still-applicable execution facts need not be rerun. A successful recorder is
objective evidence only; the AI must actually perform this Skill's full review.
Missing public API or an unmigrated old record stops with precise migration
remediation. Do not install a private alternative, select a source fallback,
convert a legacy checkpoint into pass, or switch an old installation before
upstream migration/default-cutover qualification.

### Private publication transaction and public fact

Apply the shared candidate contract to the current readiness and content
review. This owner judges exact payload/Issue semantics, selected candidate,
publication action and live PR facts; it does not repeat unchanged business
design. Preserve preview, expected HEAD, transaction recovery and readback.

Current profiles are `delivery_review_ready`, `delivery_same_plan_resume`, and
`delivery_reprepare_publication`. A fresh transaction consumes the exact
`readiness_result_id`; recovery is keyed by selected public Delivery and the
private transaction reference. Keep publication substeps private and
preserve same-PR adoption and metadata convergence. Bind provider queries and
mutations to the actual repository; no implicit target guessing.

Only after actual PR/HEAD/payload/Ready facts are read back does this owner
project a public PublicationFact. Its candidate is the transaction's original
reviewed candidate; publication URL and actual body revision bind that fact.
If the remote result succeeded but public projection or stdout was lost, resume
this transaction, read the same result and retry projection without repeating
push/create/Ready. Recover historical success even if current scope, HEAD or
readiness changed, then separately return `review_stale`; history does not
supply a new readiness pass. `stale_reason` has the direct
`delivery_readiness_refresh.reentry_reason` consumer. If the slice remains publishing and earlier full Review is applicable, this
Publication owner legally reworks to Readiness before returning. Earlier
missing/stale gates retain their real owner obligation. No Issue closure occurs.

### Scope withdrawal in the current stage

`delivery_scope_withdrawal` is an independent semantic entry with mode,
`task_ref` and `delivery_key`. Before authoring its separate review input,
read the current whole-scope decision and selected undelivered slice; judge
that its full scope was withdrawn/replaced, with no remaining obligations in
that slice. Partial changes use ordinary same-Delivery rework. This package
uses only its fixed public role and expected phase; it never accepts a role
parameter or selects an owner from phase. Record the actual reason,
`scope_decision` and minimum evidence through public `stop`, then release the
selection. `delivery_stopped` hands Task identity to whole-task Completion.
Stop preserves commits/PR/resources; PR close and cleanup require their actual
owners and any necessary current side-effect confirmation. Lost output retries
the identical stored stop result and releases selection without another stop.

## Early Draft and Ready revision

`delivery_draft_publish` consumes task/key/B/H and exact Chinese pr_title/pr_body.
It requires accepted Planning in implementing, a nonempty fixed complete range
and actual HEAD H. It does not consume readiness. Review scope, target,
sensitive content and evidence claims. The body separates HEAD checks from
target/integration checks and truthfully lists executed, failed, SKIP and pending
work. Every Delivery body remains Refs-only.

Preview the exact same repo/base/head/PR, title/body and maximum remote writes.
Obtain current-dialogue confirmation only for actual remote mutation. Invoke
the original public wrapper with the completed semantic review. This profile's
route.typed_exit is draft_published. The current 2.0 transaction records its
action/terminal and necessary mutation preimage/postimage. ensure_draft precedes
push. An existing Ready PR is first returned to Draft; binding and exact
metadata convergence reuse that PR. draft_published reads actual PR/HEAD/payload
and enters the feedback router. It never records final PublicationFact.

Before a publishing Delivery receives unreviewed changes, use independent
`delivery_return_to_draft` with concrete revision_reason. Read the original
same PR/HEAD/state and review the exact revision boundary. This owner confirms
Draft and lawfully reworks publication to implementation, invalidating
check/full_review/readiness while retaining Planning, identity and history.
The review route is draft_revision_ready. Its output returns task/key/repo/PR
to implementation. A new HEAD cannot use old readiness.

Same-plan resume keeps the original action/exit and reads actual state after
lost push/create/edit/Draft/Ready output. It accepts the original preimage or
completed postimage. No second PR, repeated push or empty commit restores
stdout. Recover an old action before previewing a new one. The next action
verifies and retires the prior completed transaction; no action journal or
second Delivery store remains.

Final delivery_review_ready still requires current candidate-bound readiness.
Only actual Ready records PublicationFact, and only current gates permit
ready_for_merge. Early feedback/analysis cannot supply a gate. One-time matching
1.0 transaction conversion is defined by MIGRATION-636.

## Preserved semantic and transaction duties

The duties below apply to the current Delivery input and output contracts.
Historical data is read only by its named history or migration owner.

# Active Task Delivery Publication Contract

## Ownership

`guru-publish-task-delivery` is the only owner of the remote publication
transaction for one reviewed public Delivery. It consumes the exact ready DTO
from Delivery Review and produces only the minimal Merge seed or a typed
same-owner/stale/blocking result. Git and GitHub remain the live fact sources;
the ignored transaction is recovery state, not a Delivery ledger.

The current 2.0 transaction owns one action and terminal:

```text
draft_publish: ensure_draft -> push_content -> bind_pr -> converge_metadata -> draft
return_to_draft: ensure_draft -> draft_revision
ready: push_content -> bind_pr -> converge_metadata -> mark_ready -> ready
```

The transaction binds the Task identity, public Delivery key, repository, base/head
branches, reviewed head, title/body bytes, initial remote/PR facts, and every
mutation decision. Before each mutation the owner writes the decision and the
live preimage it expects. A retry accepts only that preimage or the exact
postimage of the already successful mutation.

## PR Classification And Recovery

At most one same-repository Open PR may represent the current head branch.
Fresh adoption accepts an equal reviewed head or one strict ancestor that can
be fast-forwarded to the reviewed head. A fork-owned PR, different base/head,
terminal PR, unrelated remote head, or multiple candidate is blocked before
mutation.

The #405 recovery is deliberately narrow. When the same transaction is at
`bind_pr`, has no bound PR, and the remote branch plus one same-repository Open
PR already equal the reviewed head, the owner treats that PR as the result of
the transaction's prior create attempt. It records the PR identity, original
Draft state, title/body comparison, convergence decision, and Ready decision
before any remaining edit or Ready mutation. It performs no second push or PR
create.

Metadata convergence is byte-exact. If an edit returns without usable stdout,
the owner rereads the bound PR and accepts only the exact reviewed title/body
postimage. Draft-to-Ready recovery follows the same rule. Once `ready` is
persisted, every invocation is read-only and rematerializes the same
`ready_for_merge` DTO after live revalidation.

## Public Boundary

`ready_for_merge` contains only `task_ref`, `delivery_key`, `publication_result_id`, `repo_ref`,
`pr_number`, `expected_head_sha`, and the SHA-256 of the exact reviewed PR body.
Merge rereads the PR by repository and number and uses the body digest as its
minimal freshness token.

`review_stale` returns the task plus a stale reason to Delivery Review.
`resume_publication` returns the task plus private transaction reference to this
same owner. `reprepare_required` returns a task plus reason code when the
current call no longer matches the recoverable private plan. `blocked` is a
terminal stop payload.

The PR body must not contain `Close`, `Closes`, `Closed`, `Fix`, `Fixes`,
`Fixed`, `Resolve`, `Resolves`, or `Resolved` followed by an Issue reference.
The package does not infer Issue completion from `Refs` and never calls an
Issue mutation API.

## Current-stage scope revision

`delivery_scope_revision` is this existing owner's semantic re-entry after original
Clarify has published the changed whole-Task scope. Read actual accepted scope,
selected Delivery and obligations; review the retained slice anchors and original
source_selection/revision_refs. Complete the AI gate before invoking this profile.
Do not require stale Planning/Check/Review/Readiness evidence to revise scope.
Project only the reviewed current scope_ref through upstream rework to planning;
invalidate planning/check/full_review/readiness and retain identity, candidate and
historical publication/delivery facts. No new acceptance or approval is inferred.
`delivery_scope_revised` goes only to guru-delivery-scope-revised-router and the
same Delivery Author active_task_scope_change. A retry after lost output reads
matching public scope, planning phase and cleared results; it returns the same
minimal handoff, without replaying rework or installing an approval token.
A new change receives fresh original Clarify and this owner judgment.

## Fixed content publication

Publish the actual current readiness candidate and exact reviewed PR payload.
Target-branch advancement alone is not stale readiness and adds no pair guard,
Task synchronization or semantic-impact gate. Preserve expected Task/remote
HEAD, payload and same-PR transaction/recovery checks. Real content/authority
changes return to their original owners.
