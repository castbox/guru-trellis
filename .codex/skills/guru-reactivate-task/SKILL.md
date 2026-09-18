---
name: guru-reactivate-task
description: Reactivate one normally finished archived task while preserving its identity and routing the fresh work.
---

# Guru Reactivate Task

Reactivate is the normal archived-task continuation owner. It is distinct from
`guru-restore-archived-task`: it preserves the original task identity, moves a
single archive copy back to active, and routes either requirements, planning,
implementation or evidence refresh. It never reopens an Issue implicitly.

Before mutation, the AI reviews one exact target baseline and either an exact
reusable clean branch/worktree or a new branch/worktree plan. The deterministic
executor prepares that workspace, moves the original archive to the single
active locator, refreshes task metadata and ignored runtime mappings, and
invalidates prior Finish receipts. It never creates a replacement task.
