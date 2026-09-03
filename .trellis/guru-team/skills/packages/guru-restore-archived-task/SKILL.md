---
name: guru-restore-archived-task
description: Restore one archived Trellis task to Phase 2 after a scoped merge blocker through fresh identity checks and an idempotent local transaction.
---

# Guru Restore Archived Task

Use only after an AI semantic owner has classified the exact current-scope
finding as task work and obtained any required dialogue-local confirmation.
Pass the current public re-entry input, semantic result, and fresh live-facts
snapshot to `restore-archived-task`.

The AI owner rereads the PR, Issue, remote branch, archive, task,
finish-summary, runtime mapping, worktree and active-task facts immediately
before invocation. The runtime validates that closed snapshot, rereads the
local task artifacts and Git worktree, then owns only deterministic local
recovery. External blockers, identity drift, dirty
worktrees, duplicate active tasks, merged PRs, or ambiguous archive state return
`restore_blocked` with zero business writes.

An exact already-restored identity is read-only and returns
`restored_to_phase2`. A normal interrupted or lost-result retry may finish the
same identity, but it never creates a second task, branch, worktree, or PR.

The workflow routes `phase2_reentry_required` here and routes
`restored_to_phase2` through `guru-resume-implementation`; registry, preset and
platform copies are managed projections of this canonical package.
