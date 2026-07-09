# #65 Docs SSOT implementation/check gate：把同步纳入 Phase 2

## 目标

在 #64 已建立 Phase 1 `Docs SSOT Plan` 合同之后，把这份计划纳入 Phase 2 implementation 与 `trellis-check` 的 AI 判断流程。实现代理必须按计划执行 durable docs 同步责任，阶段二检查代理必须按计划验证 durable docs、task artifacts、代码、测试与 overlay/spec 是否一致。

## 背景与证据

- GitHub issue: https://github.com/castbox/guru-trellis/issues/65
- 依赖 issue #64；当前 `origin/main` 已合并 #64，并包含 Phase 1 `Docs SSOT Plan` 合同。
- 当前 main 已有通用 `phase2-check.json` `docs_ssot` coverage、pre-commit `dirty_paths` 记录与 post-commit audit。本任务不重复实现这些 objective gate。
- 官方 Trellis 自定义 workflow 文档已核对：workflow 行为通过 `.trellis/workflow.md` 的 Markdown 阶段、skill routing、workflow-state block 控制，hook/script 不应承载 AI 语义判断。
- 官方 custom spec template marketplace 文档已核对：spec template marketplace 用于可复用规范、测试规则、review checklist，不能放 active task/runtime 状态。本任务如更新 `.trellis/spec/`，只沉淀通用 workflow/preset/docs 规范。

## 已确认范围

本任务修改 Guru Team workflow / preset / overlay / docs / spec 的长期源头与 dogfood 安装副本，使 Phase 2 明确消费 `Docs SSOT Plan`：

- canonical workflow: `trellis/workflows/guru-team/workflow.md`
- dogfood workflow: `.trellis/workflow.md`
- implementation/check agent definitions:
  - `trellis/presets/guru-team/overlays/.trellis/agents/implement.md`
  - `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
  - platform overlay copies under `.codex/agents/`, `.cursor/agents/`, `.claude/agents/`
  - dogfood installed copies under `.trellis/agents/`, `.codex/agents/`, `.cursor/agents/`, `.claude/agents/`
- continue overlays that describe in-progress flow:
  - shared `.agents/skills/trellis-continue/SKILL.md`
  - `.codex/skills/trellis-continue/SKILL.md`
  - `.codex/prompts/trellis-continue.md`
  - `.cursor/commands/trellis-continue.md`
  - `.claude/commands/trellis/continue.md`
- durable requirements docs: `docs/requirements/guru-team-trellis-flow.md` and `docs/requirements/requirement-main.md`
- project specs: `.trellis/spec/workflow/**` and `.trellis/spec/preset/overlay-guidelines.md`
- workflow/preset README when user-facing install or daily-operation text must mention the new Phase 2 responsibility.

## 功能需求

1. Phase 2 implementation 入口必须要求读取 Phase 1 `Docs SSOT Plan`，识别 `ssot_first` / `delta_first` / `bootstrap_or_repair_docs` / `no_docs_update_needed` 策略，并按策略执行 docs 同步责任。
2. 实现代理 completion handoff 必须包含：
   - 当前策略；
   - durable docs 已更新结果；
   - task artifact delta 已 merge 回 durable docs 的内容；
   - 只保留为 task history 的内容；
   - `no_docs_update_needed` 的理由；
   - `bootstrap_or_repair_docs` 的最小修复、follow-up 和当前 PR 声明限制；
   - 哪些实现输入来自 durable docs，哪些来自已确认的 task delta。
3. Phase 2 check 必须按 `Docs SSOT Plan` 验证：
   - durable docs 是否按策略更新；
   - `prd.md` / `design.md` / `implement.md` 与 durable docs 是否冲突；
   - code/API/schema/config/deploy/test 是否与 durable docs 或已确认 task delta 一致；
   - 测试计划或测试用例是否覆盖本次 docs/代码变化；
   - `delta_first` 是否在 final Phase 2 check 前完成 durable docs merge；
   - `ssot_first` 是否以修订后的 durable docs 为主要实现输入；
   - `bootstrap_or_repair_docs` 是否完成最小 docs 修复，或明确 follow-up / PR 声明限制；
   - `no_docs_update_needed` 的理由是否仍成立。
4. 若实现中发现长期需求、设计、测试或 workflow 合同变化，必须先更新 planning artifacts 和 `Docs SSOT Plan`，必要时回到 Phase 1 重新做 planning approval；不能把判断推迟到 Branch Review Gate 或 finish-work。
5. 继续保留 #64 / #8 已有 `phase2-check.json` `docs_ssot` coverage 与 post-commit dirty-path audit，不新增脚本来判断 docs 语义充分性。
6. canonical workflow、canonical overlays、dogfood installed copies 必须一致；改动 overlay 后必须 apply preset 并跑 dogfood drift check。

## 非目标

- 不实现 #66 的 Branch Review Gate / finish-work / PR body 最终阻断语义。
- 不重复实现 `phase2-check.json` coverage key 或 dirty-path audit。
- 不新增脚本语义判断来替代 AI implementation/check/review 判断。
- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不关闭 #64、#66 或 #1；本任务只关闭 #65。

## Docs SSOT 状态

本仓库存在 durable docs，当前状态判定为 `complete_docs`：

- `docs/requirements/guru-team-trellis-flow.md` 已描述全流程和 Phase 1 `Docs SSOT Plan`，但 Phase 2 部分尚未展开四种策略的实现/check 消费规则。
- `docs/requirements/requirement-main.md` 已记录 #64 的 planning 合同和 Phase 2 execute/check 基线，但尚未记录 #65 的策略执行/check 细化。
- `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**` 是 workflow/preset 长期维护说明。

本任务采用 `ssot_first`：先同步 durable docs/spec/canonical workflow/overlay，再让 task artifacts 保留本次执行证据。

## 验收标准

- [ ] Phase 2 implementation 入口要求读取并执行 #64 `Docs SSOT Plan`。
- [ ] 实现代理 handoff 必须包含 plan 策略、docs 同步职责、已完成同步结果或明确 no-docs / follow-up 理由。
- [ ] Phase 2 check 明确按 plan 策略检查 durable docs / task artifacts / code / test 一致性。
- [ ] `delta_first` 策略要求在 final Phase 2 check 前完成 durable docs merge。
- [ ] `ssot_first` 策略要求实现以修订后的 durable docs 为主输入。
- [ ] `bootstrap_or_repair_docs` 策略要求当前 task 创建/修复最小 durable docs，或明确 follow-up 和当前 PR 声明限制。
- [ ] `no_docs_update_needed` 策略要求 Phase 2 check 复核该理由仍成立。
- [ ] 实现中发现长期合同变化时，必须更新 `Docs SSOT Plan` / planning artifacts，必要时重新 planning approval，再重新 Phase 2 check。
- [ ] 保留并对齐现有 `phase2-check.json` `docs_ssot` coverage 与 post-commit dirty-path audit，不新增脚本语义判断来替代 AI check。
- [ ] 相关 platform overlays、canonical workflow、dogfood installed copy 保持一致。

## 当前无阻塞问题

Issue 范围、依赖关系和非目标已经足够清晰；无需追加产品意图问题。进入实现前仍需用户在看到 `prd.md`、`design.md`、`implement.md` 三个链接后明确确认。
