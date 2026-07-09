# #64 Docs SSOT planning contract：Phase 1 必须选择同步策略

## 目标

在 Guru Team workflow 的 Phase 1 planning 阶段建立显式 `Docs SSOT Plan` 合同。后续 #65 的 implementation/check 消费和 #66 的 Branch Review / finish-work / PR body enforcement 都应以同一个 planning 合同为输入，避免到实现后或 final review 后才临时补 durable docs。

## 背景与证据

- GitHub issue: https://github.com/castbox/guru-trellis/issues/64
- 本 issue 是 #1 / PR #4 的 Docs SSOT hardening 后续，属于 1 / 3；#65 和 #66 应在本合同存在后再继续。
- 当前 `main` 已有通用 Repo Docs SSOT discovery / reconciliation 文案、Phase 2 `docs_ssot` coverage、Branch Review Gate durable docs 判断和 finish-work metadata-tail drift 阻断；本任务不重复实现新的 Phase 2 / Branch Review / finish gate。
- 官方 Trellis 自定义 workflow 文档说明 workflow 行为应通过 `.trellis/workflow.md` 的 Markdown 阶段、skill routing、workflow-state block 来控制，hook 只做运行时读取；本任务应修改 Guru Team Markdown workflow / overlay / docs，而不是把 AI 判断写进脚本。
- 官方 spec template marketplace 文档说明 spec template 用于可复用工程约定、测试规则、review checklist 等，不应放 active task state 或项目私有运行状态；本任务如更新 `.trellis/spec/`，只记录通用 workflow / preset / docs 规范。

## 已确认范围

本任务必须修改可复用 Guru Team extension 的长期源头和 dogfood 安装副本，使 Phase 1 计划阶段明确要求创建或更新 `Docs SSOT Plan`：

- canonical workflow: `trellis/workflows/guru-team/workflow.md`
- dogfood active workflow: `.trellis/workflow.md`
- durable requirements docs: `docs/requirements/guru-team-trellis-flow.md`，必要时同步 `docs/requirements/requirement-main.md`
- workflow specs: `.trellis/spec/workflow/**`
- preset specs / README: `.trellis/spec/preset/**`、`trellis/presets/guru-team/README.md`
- marketplace workflow README: `trellis/workflows/guru-team/README.md`
- platform overlays that carry planning reminders:
  - `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
  - `trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md`
  - `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md`
  - `.agents/skills/trellis-continue/SKILL.md`
  - `.codex/skills/trellis-continue/SKILL.md`
  - `.codex/prompts/trellis-continue.md`
  - Claude / Cursor continue overlays when they repeat planning reminders

## 功能需求

1. Phase 1 必须要求 planning 产物创建或更新同一个 `Docs SSOT Plan`，推荐由 `design.md` 承载权威计划，`prd.md` 记录 docs 状态与需求影响，`implement.md` 记录执行 checklist 与 checkpoint。
2. `Docs SSOT Plan` 必须记录目标 repo docs 状态枚举之一：
   - `complete_docs`
   - `partial_docs`
   - `stale_docs`
   - `no_docs`
3. `Docs SSOT Plan` 必须记录当前 task docs 同步策略之一：
   - `ssot_first`
   - `delta_first`
   - `bootstrap_or_repair_docs`
   - `no_docs_update_needed`
4. `Docs SSOT Plan` 至少必须包含：
   - docs 状态枚举与证据路径；
   - 策略选择及理由；
   - 当前 task 影响或需要更新的 durable docs 文件；
   - task artifact delta 需要 merge 回 durable docs 的内容；
   - `delta_first` 的 merge checkpoint；
   - `bootstrap_or_repair_docs` 的最小 docs 修复范围或 follow-up 限制声明；
   - `no_docs_update_needed` 的具体理由。
5. 大范围、边界清楚的需求 / 设计 / workflow 合同变更应推荐 `ssot_first`；小范围或早期探索可用 `delta_first`，但必须记录 merge checkpoint。
6. `no_docs`、`partial_docs`、`stale_docs` 必须有处理规则，不能让 task artifacts 长期冒充 durable docs。
7. 规则必须保持 repo-neutral，不能绑定 `chengtuo-resume` 或任何单一业务仓库私有 docs 结构。
8. overlay 与 dogfood 安装副本必须保持一致；改动 canonical overlay 后要重新 apply preset 并跑 dogfood overlay drift check。

## 非目标

- 不实现 #65 的 Phase 2 implementation/check plan consumption 细节。
- 不实现 #66 的 Branch Review Gate / finish-work / PR body 最终阻断语义。
- 不新增脚本来判断 docs 内容是否充分；这是 AI planning/check/review 判断，脚本只能 recorder / validator 客观事实。
- 不把 task artifacts 定义成 durable docs 的长期替代品。
- 不在 archive / finish-work 阶段首次执行 docs merge。

## Docs SSOT 状态

本仓库存在 durable docs，状态判定为 `complete_docs`：

- `docs/requirements/guru-team-trellis-flow.md`：Guru Team 全流程 durable requirements / flow SSOT，已描述 Phase 1 docs SSOT discovery，但未包含 issue #64 要求的 `Docs SSOT Plan` 枚举和策略合同。
- `docs/requirements/requirement-main.md`：扩展能力总览，包含 Docs / spec / knowledge 协同类别。
- `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`：marketplace / preset 的 public docs surface。
- `.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、`.trellis/spec/docs/**`：本仓库开发规范。

本任务采用 `ssot_first`：先更新 durable docs / spec / canonical workflow，再同步 overlay 与 dogfood 安装副本。Task artifacts 只记录本次计划、证据和执行 checklist。

## 验收标准

- [ ] Phase 1 文档明确要求创建或更新 `Docs SSOT Plan`。
- [ ] `Docs SSOT Plan` 包含 docs 状态：`complete_docs` / `partial_docs` / `stale_docs` / `no_docs`。
- [ ] `Docs SSOT Plan` 包含策略选择：`ssot_first` / `delta_first` / `bootstrap_or_repair_docs` / `no_docs_update_needed`。
- [ ] `prd.md` / `design.md` / `implement.md` 的 planning 完成条件能定位到同一个 `Docs SSOT Plan`。
- [ ] planning artifact 必须列出本 task 影响的 durable docs 文件，或解释为什么不需要更新。
- [ ] 大范围变更明确推荐 `ssot_first`；小范围变更可用 `delta_first`，但必须记录 merge checkpoint。
- [ ] 无 docs / partial docs / stale docs 都有明确处理规则，不把 task artifacts 长期冒充 durable docs。
- [ ] 该规则不绑定任何单一业务 repo 的私有文档结构。
- [ ] 相关 platform overlays、canonical workflow、dogfood installed copy 保持一致。

## 当前无阻塞问题

Issue 范围、非目标和实现顺序已经足够清晰；无需向用户追加产品意图问题。进入实现前仍需用户在看到 `prd.md`、`design.md`、`implement.md` 三个链接后明确确认。
