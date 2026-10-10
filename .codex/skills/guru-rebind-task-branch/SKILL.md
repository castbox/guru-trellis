---
name: guru-rebind-task-branch
description: Rebind one active task branch at a reviewed clean and base-contained boundary, with exact read-only recovery.
---

# Rebind Task Branch

Review the exact active task, current branch and ownership, target branch,
clean checkout and selected base. Record one call-local plan. Rebind only if
the current HEAD is contained in the reviewed target base; no uncommitted or
undelivered content moves through this owner. Show the branch/worktree effects
before execution. Existing caller-owned resources remain caller-owned.

Use `scripts/record-plan.sh` to capture the exact pre-state and
`scripts/invoke.sh --root <repository> --input -` to execute or recover.
After lost output, recover from the same plan without executing again. Never
persist checkout paths in task identity, branch binding or session state.

Read `.trellis/spec/workflow/companion-scripts.md#intermediate-command-stdout-10` for receipts and `result` projection.
Only the declared public invocation emits a formal exit; follow its consumer and positive-exit conditions.
