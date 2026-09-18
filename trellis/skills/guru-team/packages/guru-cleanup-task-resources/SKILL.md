---
name: guru-cleanup-task-resources
description: Remove only the current Finish-owned branch, worktree and runtime resources after terminal success.
---

# Guru Cleanup Task Resources

Cleanup consumes one current Finish `success`. It shows the exact owned
resources, requires an independent confirmation when a deletion remains, and
preserves user checkouts, other task resources, archives and shared runtime
state. A fresh empty set or a reviewed set whose resources are already absent
is a normal `cleaned` terminal state.

The executor accepts only a complete terminal Finish transaction, an exact
clean registered worktree for that transaction's head branch, the merged local
head branch, `origin/<head_branch>`, its exact remote-tracking ref, and
task-bound runtime files. Existing Git refs must still point to the Finish
commit. It never force-removes a worktree or removes the checkout executing
Cleanup.

After successful deletion, Cleanup records one ignored-runtime terminal
receipt before retiring the Finish receipt. An exact same-input retry can
therefore recover `cleaned` after stdout loss. A pending `remaining_resources`
route emits only task/archive/Finish continuation identity and does not require
the Finish receipt to remain readable.
