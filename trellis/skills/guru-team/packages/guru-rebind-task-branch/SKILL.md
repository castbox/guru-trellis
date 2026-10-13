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

## Delivery API 迁移

公共 profile 为 `delivery_task_branch_rebind`；旧 profile 只保留历史 schema，不能执行。分支绑定属于 Task 的资源事实，公共输入不再携带 Task stage/status。executor 从已安装公共 Task schema 2 校验身份和 generation，并保留 clean/base-contained、原 plan 与输出丢失只读恢复条件；不会创建或修改 Delivery Planning/gate。
