# Active Task Delivery Publication Contract

## Ownership

`guru-publish-task-delivery` is the only owner of the remote publication
transaction for one reviewed Delivery cycle. It consumes the exact ready DTO
from Delivery Review and produces only the minimal Merge seed or a typed
same-owner/stale/blocking result. Git and GitHub remain the live fact sources;
the ignored transaction is recovery state, not a Delivery ledger.

The exact stages are:

```text
push_content -> bind_pr -> converge_metadata -> mark_ready -> ready
```

The transaction binds the active task, delivery cycle, repository, base/head
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

`ready_for_merge` contains only `task_ref`, `delivery_cycle_ref`, `repo_ref`,
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
