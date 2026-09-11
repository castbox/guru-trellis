# #356 根治 active task workspace 身份断裂与错误重入 Intake

## Goal

修复 Guru Team 在 task 创建、激活和后续路由之间的身份闭合缺陷，使一个
`in_progress` task 只有在 task、branch/worktree、Issue Scope Ledger、task
runtime mapping 与 session/runtime 定位关系均可验证时，才会被识别为 active
task；身份不完整时稳定 fail closed，而不是错误重入 Intake、重复确认或继续
写入半成品。

## Background And Confirmed Facts

- Issue #356 是支持的正常流程可触发的 correctness bug，不依赖恶意输入、故意
  篡改或非常规并发。
- `guru-create-task-workspace` 当前在 `runtime/execute.py` 中创建 branch、
  worktree、task artifact 和两类 ignored runtime mapping，但成功结果在最终
  boundary 完成前没有把 session/runtime 定位闭合纳入同一可消费状态合同。
- `.trellis/scripts/common/active_task.py` 当前可从 session pointer 返回 task
  ref；pointer 本身不证明 task.json、当前 branch/worktree、ledger 和 Guru
  task/workspace mappings 仍然一致。
- `guru-reconcile-task-base`、Finalizer 和 Publication 已有严格 task/runtime
  identity 校验；本次要把同等 fail-closed 语义前移到 active-task 识别和创建边界。
- 当前 canonical workflow 是
  `trellis/workflows/guru-team/workflow.md`，`.trellis/workflow.md` 是 dogfood
  projection；Guru skill canonical source 是
  `trellis/skills/guru-team/`，安装副本必须由 preset 同步。

## Requirements

### R1 创建状态闭合

1. 创建阶段按确定性顺序准备并校验 branch、worktree、planning 状态的
   `task.json`、Issue Scope Ledger、task identity mapping 和 workspace boundary；
   后续 activation 阶段再闭合 session/runtime 定位 mapping。
2. 在 session/runtime 定位和最终 activation boundary 通过前，不暴露可被
   active-task 路由消费的 `in_progress` 状态；`created` 只表示可安全进入规划的
   `planning` task。
3. 任一步骤失败只回滚本次调用新建的对象和 mapping；既有任务、branch、
   worktree、session/runtime 状态不得被删除、覆盖、迁移或归档。
4. 任一失败返回稳定的 `invalid_task_state` 或语义等价的明确终止出口，并由唯一
   workflow stop consumer 承接。

### R2 身份语义

1. task identity 由 `task.json`、对应 branch/worktree、Issue Scope Ledger、
   task mapping、workspace mapping 和 session/runtime pointer 的一致关系共同
   闭合。
2. session pointer 仅用于定位或恢复索引，不单独决定 task 状态、归属或 Phase
   2/Phase 3 可进入性。
3. 缺失、冲突、过期、无法闭合的 identity 统一 fail closed；不自动 restore、
   migration、rebuild mapping、绕过 boundary、清理或重入 Intake。

### R3 全局路由

1. 全局 workflow 在处理新的 Intake/create-workspace 意图前，先解析并验证当前
   active task。
2. 完整的已有 `in_progress` task 优先进入其当前 Phase 2/Phase 3 路由；不得
   再进入初始 Intake。
3. `guru-create-task-workspace` 对已有 `in_progress` task 不执行
   `reuse_exact`；完整 identity 返回 active-task route，identity 不完整返回
   `invalid_task_state`。
4. `invalid_task_state` 只有一个 consumer；不能被重新映射为 Intake、自动
   restore 或无界确认循环。

## Acceptance Criteria

- AC1 成功创建后，branch、worktree、task、ledger、两类 Guru mapping、session
  pointer 与 boundary 可相互验证；只有完成验证后 active-task 路由才能消费。
- AC2 在每个受支持失败点及最终 boundary 失败时，不留下本次创建的 active 半
  成品；既有资源保持字节和 Git 状态不变。
- AC3 已有完整 `in_progress` task 时，新的 Intake/create-workspace 请求不调用
  `reuse_exact`，而是进入当前状态路由。
- AC4 identity 缺失、冲突或过期时稳定产生 `invalid_task_state`/等价终止出口，
  不自动恢复、迁移、重建 mapping 或清理。
- AC5 `invalid_task_state` 唯一消费，重复的无具体动作确认不会触发无限重试。
- AC6 canonical workflow、README、skill contract/interface/schema/runtime、
  preset projection、dogfood projection 和定向测试保持一致且无 drift。

## Out Of Scope

- 不支持旧任务格式迁移，不新增 restore、migration 或 compatibility Skill。
- 不修改 Finalizer #355 业务实现，不自动清理或归档既有无效任务。
- 不处理恶意伪造、故意篡改、TOCTOU、非常规并发或跨 OS crash consistency。
- 不执行完整多平台安装矩阵、Trellis upgrade/update 专项验证或 Release Gate。

## Open Questions

无阻塞性问题。官方 Trellis 生命周期文件保持 upstream-owned；本次只通过 Guru
workflow、package runtime/contract 与 preset projection 承接扩展行为。
