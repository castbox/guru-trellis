# #376 降低基线分支更新对并行任务的干扰

## Goal

当其他任务合并提交导致基线分支前进时，正在进行中的任务只因集成时钟变化而被强制退回 Planning；只有 live Issue、已批准规划假设或任务内容真正发生变化时，才判定规划过期。

## Background

- Issue #376 描述：并行任务在其他 PR 合并后被强行更新 base，任务计划变为 Stale，导致并行开发退回 Stage1 或更早阶段。
- 当前 workflow 已区分 base reconciliation 与 task lifecycle，但规划有效性仍需要明确绑定 authority/task-content clock，而非把每次 base delta 都当作 planning 变化。
- 任务只处理 Guru Trellis workflow、reconcile contract、canonical package 与其已声明投影；不扩展到业务仓库或完整 Release/升级矩阵。

## Requirements

### R1 独立时钟

将 integration clock 与 authority/task-content clock 明确建模为独立判断维度。基线提交变化本身只能证明需要重新评估集成，不得单独证明规划过期。

### R2 无关基线变化保持规划

当 base delta 不改变 live Issue、已批准规划假设、accepted scope 或任务内容时，reconcile 结果保持 `reconciled`，保留原 `resume_target`，不得路由回 Planning。

### R3 真实权威变化仍然失效

当 live Issue 或已批准 planning assumption 实际变化时，必须返回 `planning_stale` 或其现有明确 owner route，并携带可验证的变化原因；不能因 R2 而弱化真实 stale 检测。

### R4 post-plan 行为

`post_plan` 场景不得仅因 base 更新回到 Planning；只有 authority/task-content clock 变化才允许进入 planning-stale 路由。

### R5 兼容与投影

保持 canonical workflow/spec、dogfood workflow/spec、preset 与声明平台投影的一致性；不新增未经批准的兼容路径、状态机、锁或持久化授权信息。

## Acceptance Criteria

- A1：无关 base delta 的 canonical reconciliation fixture/runtime 测试通过，并断言 `reconciled` 与原 `resume_target` 保留。
- A2：真实 Issue 或已批准 planning assumption 变化的 fixture/runtime 测试通过，并断言仍进入 `planning_stale`。
- A3：`post_plan` 仅发生 base 更新时保持原阶段，不回 Planning。
- A4：canonical workflow/spec、dogfood projection、preset projection 与相关 package 字节/结构校验通过。
- A5：相关 JSON、Python、shell、`git diff --check` 与 task artifact 校验通过。

## Out Of Scope

- 不修改业务仓库、Issue 状态、PR、发布、merge 或 remote branch。
- 不执行完整多平台 throwaway installer 矩阵；该矩阵由专门兼容性/Release Issue 负责。
- 不处理恶意伪造、并发压力、TOCTOU、分布式锁或非常规 crash consistency。

## Docs SSOT Plan

- 需求与验收：本 `prd.md`。
- 技术边界、状态与迁移：`design.md`。
- 实施顺序、验证命令和风险：`implement.md`。
- durable workflow contract：`.trellis/spec/workflow/quality-guidelines.md` 与 `.trellis/spec/workflow/subtraction-first-compatibility.md`；仅在本 Issue 语义需要时同步 canonical/preset/dogfood 投影。

## Open Questions

无阻塞规划问题。当前实现选择沿用现有 `reconciled`、`planning_stale`、`resume_target` 合同，不引入新 public exit。
