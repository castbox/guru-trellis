# #438 技术设计

## Architecture Boundary

修复归属 `guru-create-task-workspace` owner runtime 的 workspace creation transaction。创建事务仍由 `execute.py` 负责确定性副作用，session attach 复用 `.trellis/scripts/common/active_task.py` 的 `set_active_task`，不新增第二套 session store 或 recovery 旁路。

## Data Flow

1. executor 在 mutation boundary 通过后创建精确 branch/worktree。
2. `create_official_task()` 创建 `planning` task，继续禁止调用 `task.py start`。
3. task identity reread 且与 reviewed plan 一致后，调用一个 package-local attach helper：传入目标 worktree、repository-relative task ref 和继承的当前 context identity。
4. helper 必须要求 `resolve_context_key()` 成功，并调用 `set_active_task()`；返回 active record 后再写/确认 runtime mappings并完成 boundary verification。
5. attach 失败走现有异常/rollback 路径；只有 attach、mapping 和 final boundary 全部成功才返回 `created`。

## Compatibility

- `planning` task 的 current resolver、recovery 和 `start-task.sh` 合同保持不变。
- 不把 session binding 写入 tracked task artifact、public DTO、plan/result 或用户授权字段。
- source checkout 与 target worktree 继续使用同一 Git common-dir session store；session record 的 workspace 必须是目标 worktree。
- canonical `trellis/skills/guru-team/...` 与 dogfood `.trellis/guru-team/...` 通过既有 preset projection 同步，不把安装副本作为唯一源头。

## Failure and Rollback

- 无 context key：在任何声称成功的结果前返回稳定的 identity/runtime 错误，并清理本次新建的 branch/worktree/task/mappings。
- `set_active_task` 返回空或抛出绑定错误：视为创建事务失败；不得降级为“创建成功但稍后恢复”。
- attach 写入后后续 mapping/boundary 失败：清理本次 session record，再沿用现有创建 rollback，避免留下指向已回滚 task 的 binding。

## Trade-off

把 attach 放在 task 创建事务内部会让 session identity 成为 workspace creation 的正常前置条件，但这是当前 workflow 的必要 ownership：没有精确 current task，后续 planning/recovery 无法安全路由。继续允许无 identity 创建会保留已证实的半成功状态，代价更高。
