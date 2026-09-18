---
name: guru-cleanup-task-resources
description: Remove only the current Finish-owned branch, worktree and runtime resources after terminal success.
---

# Guru Cleanup Task Resources

Cleanup consumes one current Finish `success`. It shows the exact owned
resources, requires an independent confirmation, and preserves user checkouts,
other task resources, archives and shared runtime state. The executor accepts
only a complete terminal Finish transaction, an exact clean registered
worktree for that transaction's head branch, the merged head branch itself,
and task-bound runtime files. It never force-removes a worktree or removes the
checkout executing Cleanup.
