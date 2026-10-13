---
name: guru-reactivate-task
description: Reactivate one normally finished archived task while preserving its identity and routing the fresh work.
---

# Guru Reactivate Task

Reactivate owns one normally finished archived TaskLifecycleKey, never Finish
recovery or implementation activation. The AI reviews the fresh archive,
source relation, target base and shared checkout acquisition disposition. Entry
selection starts from the original TaskId and live lifecycle when Direct Source
is reopened. An active task continues through its earliest affected owner;
an unfinished Closure/Finish returns to that original closeout transaction.
Issue reopening alone neither increments generation nor creates a replacement
task. Only a normally finished archive may enter this Reactivate owner.
Entry
requires the archived generation's sealed Finish result, or the exact completed
manual Cleanup receipt after Finish returned `manual_cleanup_required`, and no
unfinished visible Finish transaction, not merely `status=completed`. A reviewed
SourceCorrectionReadyDTO is applied to the archived task with a private
recoverable receipt before routing to the source owner; it never advances the
generation. A ready correction accompanying acquisition is also applied in
the Reactivate transaction and bound to its recovery receipt, including when
the selected checkout predates the separate archive correction. Confirm source correction or acquisition side effects in the
current dialogue.
Archives with retired personnel fields are never Reactivate candidates. They
may be located only by an exact TaskId or strictly matched Issue clue to return
the `unsupported_legacy_task` read-only diagnostic; no generation, source
correction, Finish residue, or summary index can restore them. Only an archive
that already satisfies the current task schema and current Finish/Cleanup
contract may enter Reactivate.

The executor keeps TaskId, moves the archived artifact into the active locator,
uses the common `guru-task-scope-projection` to call public `reopen_task`.
Only that operation increments generation; historical Delivery, Completion and
Closure facts remain intact. No current Delivery is required: evidence-only
or closeout work follows its original owner, while new implementation first
enters `guru-create-delivery`. It composes the shared checkout,
branch binding and common-dir resource ledger; it never creates task/workspace
mappings or turns historical Finish/Cleanup results into new authority. A
resolved old-generation binding may be released for branch reuse, but any
unresolved prior local resource responsibility blocks that reuse. A
session needing repair routes to Bind; session binding failure never rolls back
an established incarnation.

The package-local transaction identifies the exact acquisition and branch
successor without a persisted checkout path. Same-transaction recovery reads
live Git, task and ledger facts without repeating mutations. Partial or stale
states block; no direct requirements, implementation or evidence-refresh route
is part of this package. The active #434 workflow router consumes its typed
result without transferring Reactivate's package-local recovery ownership.

Use `delivery_reactivate_completed_task` and its independent input schema.
The semantic owner supplies `authority` as the exact current overall scope
reference in the owner result. It validates the completed/closed public Task
facts plus the existing Finish seal before any acquisition. Resume compares
the same public new generation and authority; it never resets Task status,
reuses an old gate pass or creates an empty Delivery. Old profiles are rejected.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
