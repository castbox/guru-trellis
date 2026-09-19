# #438 修复 task workspace 创建后的 Codex session binding attach

## Goal

修复 `guru-create-task-workspace` 创建 branch、worktree 和 Trellis task 后遗漏当前 Codex session attach 的问题，使成功创建的 planning task 能立即被同一会话解析，并使后续 recovery 不再依赖一次人工补绑定。

## Confirmed Facts

- `trellis/skills/guru-team/packages/guru-create-task-workspace/runtime/execute.py` 的 `create_official_task()` 使用官方 `.trellis/scripts/task.py create`，并固定传入 `--no-start`。
- `--no-start` 会明确跳过 `set_active_task`；workspace/task executor 在其后没有任何 attach 操作。
- recovery 的 `runtime/recover.py` 先要求 `task.py current --json` 返回精确的 `current_task`、workspace root 和 resolved task path，再校验 task、branch、boundary 与 runtime mappings。
- 因此正常创建可留下完整 workspace/task/runtime identity，却没有当前 session binding；此时 recovery 以 `stale_identity/current_task` 停止，形成“缺 binding 只能 recovery，recovery 又要求 binding”的反向依赖。
- `task.py start` 不适合作为创建事务的补救：它会把 task 状态从 `planning` 写成 `in_progress`，越过 Phase 1 planning boundary。

## Requirements

1. 在官方 task 创建成功且 task identity 已写入后，使用当前运行时 context 调用现有的 session binding 逻辑，将精确 task path、workspace root 和 session context 写入当前 session record。
2. Attach 必须保持 task 状态为 `planning`，不执行 `task.py start`，不运行 hooks，不改变 branch、worktree、runtime mapping 或 task artifact 的业务字段。
3. 当前 session context 缺失时，创建流程必须返回明确的可诊断失败，并按既有事务回滚/失败语义处理，不能声称 `created`；不能绑定到其他 session。
4. attach 成功后，`task.py current --json` 必须在 source checkout 与目标 worktree 中解析到同一个精确 task identity；同一 task 的 recovery 必须能够通过 current-task 前置校验。
5. 保持其他 session 隔离：未匹配的 context 不得看到该 task；已有 task/workspace/runtime identity 不得被覆盖或重建。

## Out Of Scope

- 不改变 `task.py start` 的 planning-to-in-progress 生命周期。
- 不重写 recovery 合同，不放宽 `current_task`、workspace boundary 或 runtime mapping 校验。
- 不处理恶意篡改、并发锁、TOCTOU、跨平台 crash consistency 或非正常故障注入。
- 不创建新的 Issue、branch、worktree、task，不提交、推送、创建 PR、合并或发布。

## Acceptance Criteria

- [ ] 正常 workspace creation 在 task 创建后产生当前 session binding，且最终 public exit 仍为 `created`、task 状态仍为 `planning`。
- [ ] 缺失 session context 的创建路径以明确错误终止，并不留下声称成功的半成品 workspace/task identity。
- [ ] recovery fixture 覆盖：同一 context 可解析并恢复、不同 context 仍为 no-task、缺 binding 的旧行为被回归测试固定为创建期失败而非 recovery 死循环。
- [ ] package contract/runtime/integration tests 通过，并完成 canonical package 与已安装 dogfood projection 的一致性检查。
- [ ] `git diff --check`、相关 Python 编译和 task validation 通过；未执行提交、推送或发布。
