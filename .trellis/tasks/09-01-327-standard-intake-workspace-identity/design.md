# 技术设计

## 边界

实现边界由一个确定性的 `check-workspace-boundary.sh`/对应 runtime helper 负责提供客观事实；AI/实现协调器只负责决定是否继续。校验失败统一返回 `stale_identity` 或既有 declared blocked exit，不新增公共 Skill ID、typed exit 或自动 recovery 副作用。

## 身份合同

在每次写入前，从当前 checkout 重新建立 composite identity：

- repository root 与实际 cwd；
- 当前 branch/HEAD 与 task.json 中的 branch、base branch、task id/status；
- task-local artifact 目录和 task branch；
- ignored `workspaces/<slug>.json` 与 `tasks/<slug>.json` mapping；
- `git worktree list --porcelain` 中的实际 root、branch 和重复可写 root；
- 当前请求、active task、workspace slug 与 mapping 的一致性。

worktree 模式要求当前 root 精确等于 mapping 的 workspace path，且不能等于 source/main checkout。任何缺失或 mismatch 都是阻断。检查只读，不执行 stash、迁移、清理或自动切换。

## 调用位置

1. workflow Phase 2.1 在 dispatch implement/check 前调用 boundary helper。
2. 实现协调器在每个 target write 前调用同一 helper，避免仅依赖启动时检查。
3. task artifact writer、Phase 2/check 入口复用同一身份校验，确保测试或 artifact 写入不会绕过源码写入边界。
4. `guru-create-task-workspace` 的 created checker 继续验证创建结果；它不代替实现阶段的 live recheck。

## 回归策略

使用临时 Git 仓库和真实 linked worktree fixture，分别覆盖缺少 created、main/worktree mismatch、branch/task/runtime mismatch、新增 worktree/dirty drift、重复 root 绑定、正常 task worktree，以及 dirty main 不变。测试断言阻断结果和写入前后字节不变。
