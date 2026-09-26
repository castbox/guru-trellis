---
name: guru-reactivate-task
description: Reactivate one normally finished archived task while preserving its identity and routing the fresh work.
---

# Guru Reactivate Task

Reactivate owns one normally finished archived TaskLifecycleKey, never Finish
recovery or implementation activation. The AI reviews the fresh archive,
source relation, target base and shared checkout acquisition disposition. Entry
requires the archived generation's sealed Finish result, or the exact completed
manual Cleanup receipt after Finish returned `manual_cleanup_required`, and no
unfinished visible Finish transaction, not merely `status=completed`. A reviewed
SourceCorrectionReadyDTO is applied to the archived task with a private
recoverable receipt before routing to the source owner; it never advances the
generation. A ready correction accompanying acquisition is also applied in
the Reactivate transaction and bound to its recovery receipt, including when
the selected checkout predates the separate archive correction. Confirm source correction or acquisition side effects in the
current dialogue.
For a normally committed old schema-2 archive, absent generation or explicit
generation zero with a matching retired `task.json.archive_dir` uses the
unique Git archive and old Finalizer-residue check when no C5 ledger exists.
Other explicit-generation archives require the current Finish seal or exact
manual Cleanup receipt. An empty old finish-summary Issue index does not
exclude a candidate whose committed task source identifies the Issue.

The executor keeps TaskId, moves the archived artifact into the active locator,
increments the generation and enters planning. It composes the shared checkout,
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
is part of this package. Production router activation belongs to #434.
