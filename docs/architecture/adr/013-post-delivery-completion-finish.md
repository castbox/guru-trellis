# ADR-013: Post-Delivery Completion And Finish Ownership

状态：`accepted`。来源：Issue #436 reviewed contribution；提升：`.55 -> .56`。

## Context

Active Task Delivery deliberately leaves a task active after each delivered slice. The
repository therefore needs a terminal lifecycle without moving production graph activation
into the capability contribution. Completion, Issue disposition, archive publication,
resource cleanup, and normal reactivation have different authorities and recovery facts.

## Decision

Five semantic owners remain separate:

- `guru-review-task-completion` decides whether the accepted task scope is complete.
- `guru-complete-task-closure` owns no-mutation disposition or one exact confirmed Issue-close transaction.
- `guru-finish-task` owns archive projection, lifecycle-only bookkeeping publication, and expected-head merge.
- `guru-cleanup-task-resources` owns deletion of the exact current-cycle resources after Finish success.
- `guru-reactivate-task` owns normal archive-to-active recovery while preserving task and Issue identity.

Each owner exposes only its minimal typed projection. Recovery state stays owner-private and
transaction-scoped; authorization remains dialogue-local. A Delivery success is not completion,
closure, archive, Finish, cleanup, or reactivation success.

The five packages are additive and remain workflow-deferred until #434 performs the only
production graph activation and retires the old edges. No adapter, Delivery ledger, dual graph,
old-output reader, or second lifecycle writer is introduced. Reactivation invalidates prior
Finish receipts and requires fresh completion evidence.

## Consequences

The `.56` current authority contains the five lifecycle packages and their RDT/Architecture
traceability, while the production workflow remains `22 mandatory invokes / 98 exits`.
Promotion does not authorize Publication, push, PR, merge, Release, Issue closure, or cleanup.
The promotion-created documentation diff must pass fresh Phase 2, Task Commit, and independent
complete Branch Review before Publication can consume it.
