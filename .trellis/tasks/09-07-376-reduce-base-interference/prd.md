# #376 降低基线分支更新对并行任务的干扰

## Goal

当其他任务合并提交导致基线分支前进时，正在进行中的任务不再只因集成时钟变化而被强制退回 Planning；只有 live Issue、已批准规划假设或任务内容真正发生变化时，才判定规划过期。

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

### R6 Review 后的 bounded continuity

当任务已经完成完整 Branch Review，随后在 post-Branch Review、post-Publication 或 Finalizer 阶段集成无关且兼容的新 base 时，不得仅因整树 reviewed-content identity 随 base 前进而要求重新实施或重跑完整 Branch Review。

`guru-reconcile-task-base` 必须在先前完整 review identity 仍有效、task content 未变但 Publication 需要绑定当前 reconciled HEAD 时，返回既有 `review_continuity_required`。该 Skill 在语义判断和当次 Git 副作用确认后，以 expected-head 绑定的确定性 executor 形成唯一的持久化 reconciliation commit；不得把临时 candidate、未提交工作树或 caller 自报 SHA 当作当前 task HEAD。`guru-review-branch:base_continuity` 分别绑定先前完整 Branch Review commit 和当前 reconciled task HEAD，只审查 exact base delta、冲突解决、candidate tree 与受影响验证；通过后由当前 reconciled HEAD 承载 continuity-reviewed Publication identity，不得将其表述为新的完整 Branch Review。

live authority、accepted scope、approved planning assumptions、task content 或实现真实变化时，仍必须执行原有 Phase 2、Task Commit 与完整 Branch Review。

## Acceptance Criteria

- A1：无关 base delta 的 canonical reconciliation fixture/runtime 测试通过，并断言 `reconciled` 与原 `resume_target` 保留。
- A2：真实 Issue 或已批准 planning assumption 变化的 fixture/runtime 测试通过，并断言仍进入 `planning_stale`。
- A3：`post_plan` 仅发生 base 更新时保持原阶段，不回 Planning。
- A4：canonical workflow/spec、dogfood projection、preset projection 与相关 package 字节/结构校验通过。
- A5：相关 JSON、Python、shell、`git diff --check` 与 task artifact 校验通过。
- A6：真实跨 Skill 回归覆盖 Finalizer base mismatch → reconciliation → bounded continuity → Publication ready，并证明不进入重新实施或完整 Branch Review。
- A7：base-continuity 输入同时绑定 prior full-review commit 与 current reconciled task HEAD；输出只把经过 bounded continuity 审查的 current HEAD 交给 Publication，不伪造完整 Branch Review identity。
- A8：真实 task-content、authority 或 scope 变化仍不能走 continuity fast path。
- A9：post-review reconciliation 的持久化 merge/commit 仅由 `guru-reconcile-task-base` 在精确副作用计划获当次确认后执行，并校验 expected task/base HEAD、candidate tree、clean worktree 与结果 ancestry；stale 或不匹配时零写入失败。

## Out Of Scope

- 不修改业务仓库、Issue 状态、PR、发布、merge 或 remote branch。
- 不执行完整多平台 throwaway installer 矩阵；该矩阵由专门兼容性/Release Issue 负责。
- 不处理恶意伪造、并发压力、TOCTOU、分布式锁或非常规 crash consistency。
- 不增加 legacy 双读、兼容 wrapper、第二套 continuity 状态机或长期兼容分支；现有内部 continuity 合同直接演进，旧 owner-private checkpoint 按 stale 处理。

## Docs SSOT Plan

- 需求与验收：本 `prd.md`。
- 技术边界、状态与迁移：`design.md`。
- 实施顺序、验证命令和风险：`implement.md`。
- durable workflow contract：`trellis/presets/guru-team/spec/workflow/{workflow-contract.md,skill-package-contract.md,data-contracts.md,quality-guidelines.md}` 及其 dogfood projection；`subtraction-first-compatibility.md` 继续作为直接演进约束，不复制正文。
- Architecture：当前 baseline 已定义 semantic owner、deterministic executor、确认边界与 versioned typed projection；本修复不新增 owner、domain、GAP、shared-current decision 或 ADR，按 `no_architecture_impact` 处理。

## Open Questions

无阻塞规划问题。当前实现沿用现有 exit id、consumer 与 `resume_target`，但对语义已变化的 continuity public DTO、aggregate input 和 owner-private gate 使用新的 current-only schema version；旧版本不双读、不迁移。
