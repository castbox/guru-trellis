# 智能选择 task-free 或标准 Guru Team Intake

## Goal

让所有尚未进入活动任务路径的文件修改请求先由 AI 选择 `task_free` 或
`standard_intake`。边界清楚、局部、可逆、低风险的修改不承担完整 Intake 成本；
复杂或高风险修改仍进入完整 Guru Team 生命周期。

## Background

- Live authority 为 `castbox/guru-trellis#164` 顶部“现行需求 SSOT（2026-08-13）”。
  下方旧四档风险分级正文仅是历史记录，不构成本任务合同。
- 当前 `main@5c70adc5320dae8af2e45ea3807fbd42461128c0` 已包含
  `guru-select-workflow-mode`、`task_free` / `standard_intake` typed exits、
  global workflow 路由、平台投影和基础 eval。
- 当前合同仍把无明确 task-free 意图的请求统一引向一次确认，并把不确定性统一引向
  `standard_intake`；这与现行 SSOT 的三分判断不一致。
- 当前 task-free workflow target 仅声明“当前 checkout 限定编辑”，尚未完整定义
  checkout suitability、活动 task scope、dirty overlap、错误 worktree 和执行中风险扩大行为。

## Requirements

### R1 请求入口

- 不修改仓库文件的请求直接回答，不进入 mode selector。
- 所有尚未进入活动任务路径的文件修改请求必须进入
  `guru-select-workflow-mode`，无论是否已有 Issue、是否出现 task-free 表达、当前 branch
  是什么。
- 活动 task scope 内的请求不得建立 task-free 旁路，必须返回当前 task 流程。

### R2 Mode selection

- Selector 仅选择 `task_free`、`standard_intake` 或 fail-closed `blocked`，不得选择
  checkout、branch、worktree、Issue 或发布动作。
- 用户明确表达 task-free 语义时直接选择 `task_free`，不再询问 mode。
- 用户未明确表达 task-free 时，AI 必须按有限 live repository facts 与 Issue 内容执行：
  - 高置信局部、可逆、低风险修改：自动 `task_free`；
  - 倾向 task-free 但范围或风险证据不足：仅询问一次；
  - 明显需要隔离、规划、完整评审或高风险验证：自动 `standard_intake`。
- Issue 存在与否不得替代上述语义判断。
- 文件数量、路径或关键词不得单独决定 mode。

### R3 Checkout suitability

- `task_free` consumer 写文件前必须本地只读检查 branch/worktree 身份、活动 task、
  当前 task 与请求 scope、dirty/untracked 与目标文件重叠。
- `default` / `non-default` branch 身份本身不构成阻塞。
- 当前活动 task 同 scope 请求返回该 task；潜在 scope expansion 进入既有 scope-change；
  明显无关请求询问目标 checkout；dirty overlap 或位置证据不足时仅询问执行位置。
- Checkout suitability 不读取远端 branch protection，不扩大 selector public DTO。

### R4 Task-free execution

- task-free 仅授权读取限定上下文、修改明确文件、保留无关 dirty/untracked、运行风险匹配的
  targeted checks、报告结果与未验证边界。
- task-free 不授权创建 Issue/task/worktree/branch，不授权 commit、push、PR、merge、tag、
  release、installation、cleanup 或关闭 Issue。

### R5 Scope/risk evolution

- 自动选择 task-free 后发现 scope 或风险扩大时，停止后续写入并重新选择 mode。
- 用户明确选择 task-free 后发现 scope 或风险扩大时，停止后续写入，向用户说明新事实，
  由用户选择缩小范围或进入 `standard_intake`。
- Checkout 冲突继续由 checkout suitability 处理，不引入 tier、升降档或审计 ledger。

### R6 Canonical 与投影一致性

- 语义 SSOT 位于 canonical workflow 与
  `trellis/skills/guru-team/packages/guru-select-workflow-mode/`。
- 同步 dogfood workflow、installed package、Shared/Codex/Claude/Cursor discovery projection、
  三份公共 README 和平台入口提示。
- 所有入口公开最简表达 `这次走 task-free`。
- 不新增第二个风险 owner，不把语义判断写入 Python/shell，不恢复旧单体或旧 tier 机制。

## Acceptance Criteria

- [ ] AC1：无 Issue、无 task-free 表达的文件修改 prompt 仍进入 selector。
- [ ] AC2：明确 task-free 语义直接输出 `task_free`，且入口文案统一包含
      `这次走 task-free`。
- [ ] AC3：高置信小改自动 `task_free`；证据不足仅询问一次；复杂或高风险请求自动
      `standard_intake`。
- [ ] AC4：简单 Issue、信息不足 Issue、复杂 Issue 分别覆盖自动、询问、标准 Intake。
- [ ] AC5：同一文件数量构造不同风险结果，证明文件数、路径和关键词均非独立分类器。
- [ ] AC6：checkout suitability 覆盖普通 checkout、非 primary branch、活动 task 同 scope、
      scope expansion、无关 worktree、dirty overlap 和位置证据不足。
- [ ] AC7：task-free 选择与执行链路不调用 branch-protection 查询。
- [ ] AC8：task-free 不产生生命周期资源或 Git/GitHub 发布副作用。
- [ ] AC9：自动 task-free 与显式 task-free 均覆盖 scope/risk 扩大后的暂停和重新选择。
- [ ] AC10：canonical、dogfood、Shared/Codex/Claude/Cursor 与 README 语义一致，overlay drift
      检查无差异。
- [ ] AC11：package tests/evals、preset 测试、fresh throwaway install、`trellis update` 后
      preset reapply 全部通过，且不存在 `.new` / `.bak` sidecar。

## Out of Scope

- 不修改 `guru-check-task` Phase 2 九维合同。
- 不修改 planning artifact 数量或 workspace 池机制。
- 不实现固定风险档位、风险分数、关键词分类器、文件数分类器、tier ledger 或双向升降档。
- 不把 branch protection 引入本地 task-free 编辑判断。
- 不为恶意伪造、对抗性绕过、锁、竞态、fault injection 或跨 OS 原子性增加机制。
- 不在本任务中执行 release 或清理历史 worktree。

## Technical Notes

- Selector owner result 与 public DTO 保持现行 1.0 双 mode 结构；三分判断属于 semantic owner
  行为与 eval，不新增无人消费字段。
- Checkout suitability、bounded edit 与 scope/risk evolution 由独立 semantic Skill
  `guru-execute-task-free-change` 承接；selector 仍只投影现有最小 `task_free` DTO，
  checkout facts 不进入 selector。
- Close scope 仅 #164。Issue #157、#156、#108、#154、#152 保持 scope ledger 中的
  Related 集合，不由本任务关闭。

## Open Questions

无阻塞问题。现行 Issue SSOT 与仓库证据已经决定 mode、consumer、投影和验证边界。
