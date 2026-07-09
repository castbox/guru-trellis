# #65 技术设计：Docs SSOT Plan 的 Phase 2 消费合同

## 设计原则

- AI 语义判断留在 Markdown workflow、skill、prompt、agent definitions、docs 和 specs 中；脚本只做 executor / validator / recorder。
- 复用 #64 `Docs SSOT Plan`。本任务不定义新的 plan enum，不新增 schema，不修改 `record-phase2-check` coverage 结构。
- canonical source 优先：先改 `trellis/workflows/guru-team/workflow.md`、`trellis/presets/guru-team/overlays/`、durable docs/spec，再通过 preset apply 同步 dogfood installed copies。
- Phase 2 check 只能消费 plan 并判断一致性，不能把 docs 语义充分性推给 Branch Review Gate 或 finish-work 首次判断。

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

理由：issue #65 修改 Guru Team Phase 2 implementation/check 的长期过程合同，影响所有新装和已安装业务仓库。若只在 task artifact 里描述增量，会造成 durable workflow docs、agent overlays 与实际 AI 执行入口不一致。

### 需要更新的 durable docs / workflow surfaces

- `docs/requirements/guru-team-trellis-flow.md`：在 Phase 2 execute/check 段落补充 `Docs SSOT Plan` 四种策略的实现与检查消费规则。
- `docs/requirements/requirement-main.md`：在已实现能力总览中补充 #65 对 Phase 2 implementation/check 的职责。
- `.trellis/spec/workflow/workflow-contract.md`：记录 Phase 2 必须消费 `Docs SSOT Plan`，scope drift 必须回到 planning artifact / planning approval。
- `.trellis/spec/workflow/quality-guidelines.md`：把 Phase 2 plan consumption 加入 review focus。
- `.trellis/spec/preset/overlay-guidelines.md`：要求 continue overlays 和 implement/check agent files 表达 Phase 2 docs 策略消费。
- `trellis/workflows/guru-team/README.md`：marketplace workflow docs 描述 implementation/check 如何消费 plan。
- `trellis/presets/guru-team/README.md`：preset docs 描述安装后的 implement/check agents 会要求 docs 策略 handoff 和 check evidence。

### 需要更新的 workflow / overlay surfaces

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md`
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/implement.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
- `trellis/presets/guru-team/overlays/.codex/agents/trellis-implement.toml`
- `trellis/presets/guru-team/overlays/.codex/agents/trellis-check.toml`
- `trellis/presets/guru-team/overlays/.cursor/agents/trellis-implement.md`
- `trellis/presets/guru-team/overlays/.cursor/agents/trellis-check.md`
- `trellis/presets/guru-team/overlays/.claude/agents/trellis-implement.md`
- `trellis/presets/guru-team/overlays/.claude/agents/trellis-check.md`
- dogfood installed copies under `.agents/`, `.codex/`, `.cursor/`, `.claude/`, `.trellis/agents/` after preset apply.

### task artifact delta merge

本 task artifact 中以下长期合同必须 merge 回 durable docs / workflow / overlays：

- 实现代理必须读取 `Docs SSOT Plan` 并按策略执行。
- 实现 handoff 必须明确 plan 策略、docs 同步结果、未同步限制或 follow-up。
- `trellis-check` 必须按 plan 策略验证 durable docs、task artifacts、code/schema/config/deploy/test 和测试覆盖一致性。
- `delta_first` final Phase 2 check 前必须完成 durable docs merge。
- `ssot_first` 实现必须以修订后的 durable docs 为主要输入。
- `bootstrap_or_repair_docs` 必须完成最小 docs 修复，或明确 follow-up 与当前 PR 声明限制。
- `no_docs_update_needed` 必须在 Phase 2 check 中复核理由仍成立。
- scope drift 必须更新 planning artifacts / `Docs SSOT Plan`，必要时重新 planning approval，再重新 Phase 2 check。

### merge checkpoint

因为本任务使用 `ssot_first`，进入 Phase 2 check 前必须确认：

- canonical workflow 与 dogfood `.trellis/workflow.md` 均包含 Phase 2 plan consumption。
- implement/check agent definitions 的 canonical overlay 与 dogfood installed copies 已同步。
- durable docs/spec 已记录本任务的长期合同。
- task artifact 中没有未 merge 回 durable docs 的长期合同。

## 实现边界

### 会改

- Markdown workflow、agent definitions、continue skill/prompt/command overlays、README、durable requirements docs、`.trellis/spec/**`。
- task-local `implement.jsonl` / `check.jsonl` context manifests。

### 不会改

- `trellis/workflows/guru-team/scripts/**`
- `trellis/presets/guru-team/scripts/**`
- `trellis/workflows/guru-team/schemas/**`
- `trellis/index.json`
- Trellis upstream package、全局 npm、`node_modules`

如果实现中发现 objective validator 必须新增字段或脚本校验，应先回到 Phase 1 更新本设计并重新请求 planning approval。

## Scope Drift 处理

若实现中发现 #64 的 `Docs SSOT Plan` 字段不足、durable docs 状态不再是 `complete_docs`，或需要新增 Branch Review / finish-work / PR body 阻断语义：

- 暂停实现；
- 更新 `prd.md`、`design.md`、`implement.md` 和 `issue-scope-ledger.json`；
- 必要时在 GitHub issue 留下 scope 说明；
- 重新展示三份 planning artifact 并等待用户确认；
- 重新执行 Phase 2 check。

## 兼容性与 upgrade/update

- 长期合同放在 marketplace workflow 和 preset overlay canonical source 中，避免依赖已安装副本的一次性 patch。
- 改动 `trellis/presets/guru-team/overlays/` 后必须运行：
  - `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`
  - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- 若 apply 产生 `.new` / `.bak`，必须逐个检查并处理。
- 最终报告必须明确 throwaway install / upgrade-update 门禁覆盖情况。若未跑完整 throwaway 安装或 `trellis update` replay，不能声称开箱即用或升级恢复链路已完整验证。

## 验证设计

计划执行以下验证：

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-065-docs-ssot-phase2-sync-gate
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 1.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

如修改 agent/overlay 文案，还要执行 grep 复核：

```bash
rg "Docs SSOT Plan|ssot_first|delta_first|bootstrap_or_repair_docs|no_docs_update_needed|durable docs" trellis/presets/guru-team/overlays .trellis/agents .codex/agents .cursor/agents .claude/agents .agents/skills .codex/skills .codex/prompts .cursor/commands .claude/commands
```

## 风险

- 文案分散在 canonical workflow、dogfood copy、shared skills、Codex prompts/skills、Cursor/Claude commands、channel runtime agents 和 platform agents，漏改会造成平台行为漂移。
- `Docs SSOT Plan` 是 AI 合同，不应被表达成脚本自动判定；review 需重点检查是否误把语义判断放进 Python / shell。
- 本 issue 不实现 #66；文案需要清楚说明 Branch Review / finish-work / PR body 的最终阻断仍由 #66 完成。
