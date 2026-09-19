---
name: guru-bind-task-session
description: Bind one current session to an exact task identity, rebind after loss, switch between independent tasks, and resume with lifecycle freshness.
---

# Guru Bind Task Session

This package owns the short-lived session binding contract for Issue #443. It
never creates tasks, branches, worktrees, Issues, or lifecycle records. It
reads official `task.json`, ignored task/workspace mappings, live Git facts and
the official Trellis session resolver, then writes only its own ignored
session-binding record after the caller's semantic result has selected a route.

The current task identity remains authoritative; session, branch and worktree
are replaceable carriers. Missing or mismatched identity fails closed.
