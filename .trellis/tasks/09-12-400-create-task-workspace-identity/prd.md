# Issue #400: 修复任务 Workspace Identity 闭环

## 背景

`guru-create-task-workspace` 当前可能在缺少完整前置证据或任务身份未闭合时暴露一个看似可用的 task workspace。典型表现包括 `task.json` 缺少 `worktree_path`、session current-task 与 task artifact 不一致，以及 workspace/task mapping 与 live worktree 无法组成同一身份。

## 目标

- 创建 owner 只接受同一条 fresh Intake 链的直接消费结果，并在缺失、过期或 mismatch 时 fail closed。
- 创建成功后，task、session locator、workspace/task mapping 与 live worktree 共享可验证 identity。
- identity 缺失或冲突返回唯一 `invalid_task_state` stop，不自动修复、迁移、清理或重入 Intake。
- canonical、dogfood、安装投影和定向测试保持一致。

## 范围

修改 Guru/Trellis workspace 创建、identity binding、前置证据消费、诊断、恢复边界及其合同和回归测试。

## 非目标

- 不修改 Issue #393、#398、#396 的业务范围。
- 不支持旧 task 格式迁移，不新增 restore/migration Skill。
- 不处理恶意伪造、TOCTOU、并发压力或跨 OS crash consistency。

## 验收

1. 任一 required fresh predecessor 缺失或 mismatch 时，创建前 zero-write 并返回明确 blocker。
2. `task.json.worktree_path == task mapping.workspace_path == workspace mapping.workspace_path == live worktree path`。
3. session current-task 与 task artifact locator 一致；缺失或冲突为 `invalid_task_state`。
4. 手工创建对象不能被识别为 owner `created`。
5. 合法同范围恢复幂等，不重复创建 Git 资源。
6. canonical、dogfood、installed 和正常恢复测试通过。
