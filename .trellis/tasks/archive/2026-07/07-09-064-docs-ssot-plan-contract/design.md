# #64 技术设计：Phase 1 Docs SSOT Plan 合同

## 设计原则

- AI 判断留在 Markdown workflow / skill / prompt / docs 中；脚本只执行 deterministic recorder / validator / executor。
- canonical source 优先：先改 `trellis/workflows/guru-team/workflow.md`、`trellis/presets/guru-team/overlays/`、durable docs 和 specs，再同步 dogfood 安装副本。
- 不引入新数据 schema 或 companion script。`Docs SSOT Plan` 是 planning artifact 中的 Markdown 合同，由 AI 生成、check/review 消费。
- 保持 repo-neutral：只列通用 docs 类型和策略，不固化某个业务仓库目录。

## Docs SSOT Plan

### docs 状态

本任务判定当前仓库为 `complete_docs`。

证据路径：

- `docs/requirements/guru-team-trellis-flow.md`
- `docs/requirements/requirement-main.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/workflow/index.md`
- `.trellis/spec/preset/index.md`
- `.trellis/spec/docs/index.md`

### 策略

本任务选择 `ssot_first`。

理由：issue #64 修改 Guru Team workflow 的长期过程合同，影响所有新装 / 已安装业务仓库的 planning 行为。只在本 task 的 `prd.md` / `design.md` / `implement.md` 写增量说明会造成 durable workflow docs 与实际 AI 入口不一致。

### 需要更新的 durable docs / workflow surfaces

- `docs/requirements/guru-team-trellis-flow.md`：在 Phase 1 flow 中加入 `Docs SSOT Plan` 明确步骤、状态枚举、策略枚举和 artifact 责任。
- `docs/requirements/requirement-main.md`：在 Docs / spec / knowledge 协同能力总览中补充 Phase 1 plan contract。
- `.trellis/spec/workflow/workflow-contract.md`：记录 `Docs SSOT Plan` 是 Phase 1 planning 合同，不能由脚本判断充分性。
- `.trellis/spec/workflow/quality-guidelines.md`：把检查点加入 workflow / overlay review focus。
- `.trellis/spec/preset/overlay-guidelines.md`：要求 continue overlays 在 planning reminder 中提及 `Docs SSOT Plan`。
- `trellis/workflows/guru-team/README.md`：public marketplace workflow docs 中描述 planning 阶段的计划合同。
- `trellis/presets/guru-team/README.md`：preset docs 中描述 overlay 安装后的 planning 入口会提醒 `Docs SSOT Plan`。

### 需要更新的 workflow / overlay surfaces

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md`
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md`
- Dogfood installed copies under `.agents/skills/`, `.codex/skills/`, `.codex/prompts/` after preset apply.

### task artifact delta merge

本 task artifact 中的以下内容需要 merge 回 durable docs / workflow：

- `Docs SSOT Plan` 的四个 docs 状态枚举。
- 四个策略枚举及适用场景。
- `prd.md` / `design.md` / `implement.md` 与同一个 `Docs SSOT Plan` 的定位关系。
- `delta_first` 的 merge checkpoint 要求。
- `bootstrap_or_repair_docs` 对 no/partial/stale docs 的处理规则。
- `no_docs_update_needed` 必须写具体理由。

### merge checkpoint

因为本任务使用 `ssot_first`，不使用 `delta_first`。仍需在 `implement.md` 中设置检查点：完成 source edits 后，必须确认 task artifact 中的合同内容已经落入 durable docs / specs / workflow，不能只停留在 task artifact。

### no_docs / partial_docs / stale_docs 处理

Workflow 应规定：

- `no_docs`：task 必须创建最小 durable docs，或明确说明 repo 暂不设 durable docs SSOT 且 task artifact 仅为 archived evidence。
- `partial_docs`：必须列出可复用的现有 docs、缺口、当前 task 更新范围或 follow-up 限制。
- `stale_docs`：必须列出 stale 证据，并选择当前 task 修复最小范围或降级为 follow-up；不能声称 durable docs 已一致。
- `bootstrap_or_repair_docs`：适用于 no/partial/stale docs 的修复或 follow-up 声明。

### no_docs_update_needed 规则

仅限纯局部 bugfix、内部重构，且没有长期产品 / API / 架构 / 数据 / 部署 / 运营 / 测试合同变化。必须写具体理由和受影响 docs 检查结果。

## 实现边界

### 会改

- Markdown workflow / skill / prompt / README / spec / requirements docs。
- `implement.jsonl`、`check.jsonl` 只作为 task-local sub-agent context manifest。

### 不会改

- `trellis/workflows/guru-team/scripts/**`
- `trellis/presets/guru-team/scripts/**`
- `trellis/workflows/guru-team/schemas/**`
- `trellis/index.json`
- Trellis upstream package、全局 npm、`node_modules`

若实现中发现脚本或 schema 必须变更，应回到 Phase 1 更新本设计并重新请求 planning approval。

## 兼容性与 upgrade/update

- 长期合同放在 marketplace workflow 和 preset overlay canonical source 中。
- `.trellis/workflow.md` 和平台目录 dogfood copies 通过 apply preset / 手动同步保持一致，不作为唯一源头。
- 改动 overlay 后必须运行：
  - `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`
  - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- 若 apply 产生 `.new` / `.bak`，必须逐个检查并处理。
- 最终验证应至少覆盖 `get_context.py --mode phase` 的 Phase 1 文案和 dogfood drift；完整 throwaway install / upgrade 验证若本轮未跑，最终报告必须明确未覆盖。

## 验证设计

计划执行以下验证：

- `python3 -m json.tool trellis/index.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-064-docs-ssot-plan-contract`
- `python3 ./.trellis/scripts/get_context.py --mode phase`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `git diff --check`

## 风险

- 文案分散在 canonical workflow、dogfood copy、shared skills、Codex prompts、Cursor/Claude overlays 和 public docs，漏改会造成平台行为漂移。应使用 `rg` 和 drift check 补漏。
- `Docs SSOT Plan` 是 AI 合同，不应被表达成脚本自动判定；review 需重点检查是否误把语义判断放进 companion script。
- 本 issue 不实现 #65 / #66，文案需要清楚说明后续消费与阻断由后续 issue 完成，避免验收范围扩张。
