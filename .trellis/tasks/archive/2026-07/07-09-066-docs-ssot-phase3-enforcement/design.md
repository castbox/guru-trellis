# #66 技术设计

## 设计原则

- Markdown workflow / skill / prompt / docs 承载 AI 判断流程；Python / shell 只做确定性 validator / recorder / executor。
- Phase 3 只验证 Docs SSOT 链条已完成，不把首次 reconciliation 延后到 final review 或 finish-work。
- Canonical source 先改，再同步 dogfood installed copies；避免只 patch 当前仓库运行副本。
- 脚本如需增强，只检查 PR body 结构是否出现 Docs SSOT section / key，不判断内容真实充分。

## Docs SSOT Plan

### docs state

`complete_docs`

证据路径：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

仓库已经有 durable workflow/docs/spec SSOT，且 #64/#65 已建立 Phase 1/2 Docs SSOT 合同。本任务是在现有完整文档体系上新增 Phase 3 enforcement 语义。

### strategy

`ssot_first`

原因：本任务修改的是长期 Guru Team workflow / release contract。必须先把 durable docs、workflow 和 overlay 合同更新为权威输入，再让实现、测试和 PR body validator 与其一致。任务 artifact 不得成为长期规则来源。

### affected durable docs / source surfaces

- Workflow 合同：`trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`
- Continue closeout overlay：`.agents/skills/trellis-continue/SKILL.md`、`.codex/skills/trellis-continue/SKILL.md`、`.codex/prompts/trellis-continue.md`、`.claude/commands/trellis/continue.md`、`.cursor/commands/trellis-continue.md` 及 canonical overlay copies
- Finish-work overlay：`.agents/skills/trellis-finish-work/SKILL.md`、`.codex/skills/trellis-finish-work/SKILL.md`、`.codex/prompts/trellis-finish-work.md`、`.claude/commands/trellis/finish-work.md`、`.cursor/commands/trellis-finish-work.md` 及 canonical overlay copies
- Review/check agent definitions：`.trellis/agents/check.md`、platform `trellis-check` agent copies，如 Branch Review mode 需要更明确的 Docs SSOT 判断
- Durable docs/spec：`docs/requirements/**`、`.trellis/spec/workflow/**`、`.trellis/spec/preset/**`、workflow/preset README
- Objective validator/tests：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、`test_guru_team_trellis.py`，仅限 PR body Docs SSOT section/key presence

### task artifact deltas to merge

- `prd.md` 中的 scope、非目标、验收标准需要映射到 workflow/docs/spec/overlay。
- 本 `design.md` 的 Phase 3 Docs SSOT enforcement 设计需要合入 durable workflow/spec/docs。
- `implement.md` 中的验证策略需要体现在 quality guideline 和脚本测试中。

### merge checkpoint

使用 `ssot_first`，无 `delta_first` merge checkpoint。实现阶段必须先完成 durable docs/workflow/overlay 更新，再进行脚本/测试更新和 dogfood overlay sync。

### follow-up / limit

当前计划不创建 follow-up。若实现时发现 throwaway install 或 `trellis update` 兼容性无法验证，PR body 和最终报告必须将该验证缺口列为限制，而不是扩大 #66 scope。

## 行为设计

### Branch Review Gate

Workflow 和 overlays 需要明确 final reviewer 的职责：

- 读取 approved `Docs SSOT Plan`、Phase 2 implementation handoff、`phase2-check.json` 和当前 full diff。
- 验证 plan strategy 是否已在 Phase 2 完成。
- 验证 durable docs、task artifacts、code/schema/config/deploy/test 是否与当前 HEAD 一致。
- 对 `ssot_first`、`delta_first`、`bootstrap_or_repair_docs`、`no_docs_update_needed` 分别检查对应完成条件。
- 如果发现当前 scope docs inconsistency 或 Phase 2 缺失 docs merge，记录 blocking finding，让任务回 Phase 2/3。
- 不修改 durable docs，不补写 missing Phase 2 work，不把 current-scope defect 降级为 observation/follow-up。

### Review 后与 finish-work

已有 metadata-tail fail-closed 规则保留。本任务需要把 Docs SSOT 语义写得更明确：

- Gate 后只允许 `review.md`、`reviews/*.md`、`review-gate.json`、`agent-assignment.json`、`pr-body.md`、`pr-readiness.json`、archive/journal metadata。
- Gate 后新增或修改 durable docs、`.trellis/spec/`、source、tests、schema、config、scripts、preset、overlay、CI/CD、deployment、migration、Makefile 都必须回 Phase 2 check 和 Branch Review Gate。
- finish-work dry-run 和 formal finish 都不得首次修改 durable docs 或 `.trellis/spec/`。

### PR body

AI readiness review 必须生成或确认 `pr-body.md` 中包含 Docs SSOT 处理结果。推荐独立 `## Docs SSOT` 或 `## 文档同步` section，至少包含：

- plan strategy
- durable docs 更新清单或 no-update 理由
- task artifact delta merge 结果
- task-history-only 内容
- follow-up / current PR limitation

如脚本增强，新增 required structure 只能检查 section 或关键词存在，不能判断“理由充分”或“语义真实”。

## 兼容性与发布影响

- Workflow / overlay 改动会影响新安装和已安装项目，需要 canonical + dogfood copy 同步，并运行 preset apply 和 dogfood drift check。
- PR body validator 如新增 section required，会影响非 draft publish；需测试现有 valid body helper 和 publish tests，避免误伤 reviewed readable body。
- 不新增配置项，不改变 task/ledger schema，不改变 GitHub issue close/ref 语义。
- 不涉及 runtime secrets、数据库、部署资产或外部 API。

## 风险与缓解

- 风险：多平台 overlay 文字漂移。缓解：修改 canonical overlays 后运行 `apply.sh --repo . --all-platforms` 和 drift check。
- 风险：脚本越界成为 reviewer。缓解：只加入固定 section/key presence tests，语义判断留在 workflow/AI readiness review。
- 风险：遗漏 durable docs。缓解：用 `rg` 检查 `Docs SSOT`、`finish-work`、`Branch Review Gate`、`PR body` 相关 surface。
- 风险：开箱即用验证不足。缓解：尽量执行 throwaway install / preview；无法执行时在 PR body 和最终回复中明确限制。
