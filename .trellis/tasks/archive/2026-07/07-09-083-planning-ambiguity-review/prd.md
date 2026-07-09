# #83 禁止 Trellis task planning artifacts 使用无约束模糊表达

## 目标

Guru Team workflow 在进入实现前必须完成 planning artifact ambiguity review，并把审查结论写入可审计证据。`prd.md`、`design.md`、`implement.md` 中承载需求、设计、事件合同、状态机、gate、验收标准、非目标、实现步骤和测试步骤的内容，必须使用确定性约束语言。

## 背景与证据

- Source issue: https://github.com/castbox/guru-trellis/issues/83
- Issue #83 指出近期 planning 审查中出现弱约束表达，导致实现、检查和 Branch Review Gate 对同一需求产生不同解释。
- 官方 Trellis 文档 `https://docs.trytrellis.app/advanced/custom-workflow.md` 明确 `/.trellis/workflow.md` 定义 Trellis 开发流程，phase、skill routing、per-turn reminder 都由 Markdown workflow 控制。
- 官方 Trellis 文档 `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md` 明确 spec template marketplace 承载复用工程约定，不承载 active task state 或 project-private runtime state。
- 当前仓库规格要求 workflow 行为改动同时覆盖 canonical workflow、dogfood `.trellis/workflow.md`、preset overlay、README / durable requirement docs、companion scripts 与测试。

## 范围

### In Scope

- 更新 `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md`，把 ambiguity review 纳入 Phase 1 planning start gate。
- 更新 Guru Team continue / brainstorm / before-dev / sub-agent overlay 文案，使安装后的 Codex、Cursor、Claude、共享 `.agents` 入口读取同一 planning ambiguity review 规则。
- 更新 `record-planning-approval` / `check-planning-approval`，要求 `planning-approval.json` 记录结构化 ambiguity review evidence。
- 更新 durable docs / specs，说明 planning artifact 语言约束和脚本边界。
- 更新测试，覆盖缺失 ambiguity review evidence 时 fail closed，以及记录后通过的路径。
- 同步 dogfood overlay，并验证无 drift。

### Out of Scope

- 不实现自然语言语义理解器。
- 不把词表扫描结果当作 AI planning review 结论。
- 不要求清除仓库内所有中文弱约束词。
- 不改写 GitHub issue 原文。
- 不把本 issue 变成修补某个历史 task artifact 的一次性任务。

## 术语

- **Ambiguity review**: 主会话在展示三份 planning artifacts 给用户前执行的 AI 语义审查，必须确认需求无遗漏、无矛盾、无误导、无无约束模糊表达。
- **受控弱约束词表**: `可以`、`允许`、`建议`、`尽量`、`视情况`、`类似`、`相关`、`等`。该词表是检查对象数据，不是执行合同措辞。
- **规范性条款**: task artifact 中用于约束实现、检查、验收、gate、状态机、事件合同、配置和验证步骤的文本。

## 功能需求

1. Guru Team Phase 1 planning workflow 必须要求主会话在展示 `prd.md`、`design.md`、`implement.md` 前执行 ambiguity review。
2. Ambiguity review 必须覆盖以下风险：
   - 需求弱化；
   - issue 原始语义丢失；
   - 可选执行路径缺少触发条件；
   - 同一目的存在两套并行实现；
   - gate 条款只有自然语言兜底，缺少机器可验证条件；
   - acceptance criteria 的 pass/fail 语义不确定。
3. 规范性条款不得无条件使用受控弱约束词表中的词。若外部引用或历史记录包含这些词，task artifact 必须标明来源，并且不得把引用文本直接作为执行合同。
4. Workflow、skills、prompts、agent overlay 必须要求把弱约束表达改写成确定性语义，例如 `必须`、`不得`、`只能`、`当且仅当`、`失败并阻塞`、`记录结构化字段`。
5. `planning-approval.json` 必须包含结构化 `ambiguity_review` evidence。该 evidence 至少记录 review 状态、审查维度、受控词表、规范性条款结论、引用豁免结论、AI reviewer、summary。
6. Companion script 只能记录和校验客观字段、词表、必填状态和 artifact digest；脚本不得声明自然语言语义审查充分。
7. 缺失 `ambiguity_review`、状态不是通过、缺少必填维度、缺少受控词表、缺少 reviewer/summary 时，`check-planning-approval.sh` 必须 fail closed。
8. Branch Review Gate 必须覆盖 workflow、overlay、docs、script、test、preset sync 与 dogfood drift。

## Docs SSOT 状态

- Docs state: `complete_docs`
- Requirement impact: 本任务改变长期 Guru Team workflow / planning gate / companion script data contract，必须更新 durable docs。
- Evidence paths:
  - `docs/requirements/guru-team-trellis-flow.md`
  - `docs/requirements/requirement-main.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/overlay-guidelines.md`

## 验收标准

- [ ] Canonical workflow 和 dogfood `.trellis/workflow.md` 明确要求 planning artifact ambiguity review，并说明审查发生在展示三份 planning docs 给用户前。
- [ ] `trellis-continue` / `trellis-brainstorm` / `trellis-before-dev` / implementation 与 check agent overlay 均指向同一 ambiguity review gate，且没有把语义判断下沉到 hook 或脚本。
- [ ] `record-planning-approval.sh` 生成的 `planning-approval.json` 包含结构化 `ambiguity_review` evidence。
- [ ] `check-planning-approval.sh` 对缺失或不通过的 `ambiguity_review` fail closed。
- [ ] durable docs / specs 记录 planning ambiguity review 规则、受控词表、引用豁免、脚本边界和测试要求。
- [ ] Unit tests 覆盖通过路径和缺失 / 不通过 ambiguity review evidence 的阻断路径。
- [ ] 运行 preset apply 同步 dogfood 安装副本，并运行 dogfood overlay drift check。
- [ ] 运行必要验证命令：JSON、Bash syntax、Python compile、targeted unit tests、task validate、phase context read、git diff check。

## 非目标

- 不自动改写自然语言。
- 不把机器词表扫描提升为语义 review。
- 不把受控词表扩展为仓库全局禁词清理。
- 不把 spec template marketplace 用作 active task artifact 存储。

## Open Questions

无。Issue #83、官方文档、当前 workflow specs 和代码足以进入实现规划。
