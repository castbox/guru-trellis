# #93 将 planning artifact 弱约束词改为受控词表并阻塞未分类命中

## 目标

Guru Team workflow 在 planning approval 前必须对当前 task 的 `prd.md`、`design.md`、`implement.md` 执行正文扫描。扫描命中必须进入 `planning-approval.json` 的 `ambiguity_review.normative_language.hits[]`，未分类命中和 `contract_violation` 命中必须进入 `unchecked_normative_hits[]` 并阻塞 `record-planning-approval` 与 `check-planning-approval`。

## 背景与证据

- Source issue: https://github.com/castbox/guru-trellis/issues/93
- Issue #93 是 #83 的 follow-up hardening。#83 已建立 planning artifact ambiguity review gate，但当前实现只记录结构化 AI review evidence，不扫描 planning artifact 正文。
- 现状代码证据：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 中 `PLANNING_AMBIGUITY_CONTROLLED_TERMS` 只有 8 个词。
  - `build_planning_ambiguity_review_payload()` 只写入 `controlled_terms` 与空的 `unchecked_normative_hits`。
  - `validate_planning_approval()` 校验结构和 planning artifact digest，不重新扫描 `prd.md`、`design.md`、`implement.md`。
- 官方 Trellis 文档依据：
  - `https://docs.trytrellis.app/advanced/custom-workflow.md` 明确 workflow 行为由 `.trellis/workflow.md` Markdown 控制。
  - `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md` 明确 spec marketplace 承载复用工程约定，不承载 active task state。
- 本仓库边界：Markdown / skill / prompt / workflow 定义判断流程；Python / shell 只做 executor、validator、recorder。

## 受控词表定义

本节是词表定义，不作为当前 task 执行合同正文。

```text
可以
允许
建议
推荐
可选
尽量
尽可能
最好
应该
应当
原则上
一般
通常
视情况
根据情况
根据需要
按需
必要时
如有需要
需要时
适当
适当时
合理
合理时
类似
相关
相应
等
等等
之类
一些
若干
部分
至少
默认
```

## 范围

### In Scope

- 扩展 canonical 与 dogfood `PLANNING_AMBIGUITY_CONTROLLED_TERMS` 常量。
- 扩展 `planning-approval.json` data contract：`controlled_terms`、`scan_scope`、`hits`、`unchecked_normative_hits`。
- `record-planning-approval` 在写入 artifact 前扫描三份 planning artifacts。
- `check-planning-approval` 重新扫描三份 planning artifacts，并验证 artifact 中记录的 `controlled_terms`、`scan_scope`、`hits`、`unchecked_normative_hits` 与当前扫描结果一致。
- 增加分类白名单与结构校验。分类白名单定义为词表数据，不作为当前 task 执行合同正文：
  - `contract_violation`
  - `quoted_source_non_contract`
  - `term_definition`
  - `literal_identifier`
  - `historical_record_non_contract`
  - `deterministic_threshold`
  - `deterministic_default`
  - `deterministic_option`
  - `deterministic_reference`
- 同步 canonical workflow、dogfood workflow、preset overlays、README、durable docs、`.trellis/spec/workflow/**` 和测试。
- 运行 preset apply 与 dogfood overlay drift check。

### Out of Scope

- 不构建自然语言语义 reviewer。
- 不自动决定每个命中的分类。
- 不扫描整个仓库。
- 不改写历史归档 task artifacts。
- 不改写 GitHub issue 原文、官方文档原文或历史引用原文。

## 功能需求

1. `record-planning-approval` 必须固定扫描 `{TASK_DIR}/prd.md`、`{TASK_DIR}/design.md`、`{TASK_DIR}/implement.md`，调用方不得缩小扫描范围。
2. `check-planning-approval` 必须重新扫描同三份文件，并验证 artifact 中记录的 `controlled_terms`、`scan_scope`、`hits`、`unchecked_normative_hits` 与当前扫描结果一致。
3. 每条命中必须记录 `path`、`line`、`term`、`text`、`classification`、`reason`。
4. 所有命中必须进入 `hits[]`。
5. 未分类命中必须进入 `unchecked_normative_hits[]`。
6. `classification=contract_violation` 的命中必须进入 `unchecked_normative_hits[]`。
7. `unchecked_normative_hits[]` 非空时，`record-planning-approval` 与 `check-planning-approval` 必须退出 2。
8. 允许分类命中不得进入 `unchecked_normative_hits[]`，且必须包含非空 `classification` 与 `reason`。
9. 未知分类、空分类、空理由、缺少必填字段、artifact 记录与重新扫描不一致时，validator 必须 fail closed。
10. Scanner 只提供客观命中事实和分类结构校验，不替代 AI ambiguity review。`ambiguity_review.status=passed`、七个 `checked_dimensions` 与 reviewer/summary 仍必须存在。

## Docs SSOT 状态

- Docs state: `complete_docs`
- Requirement impact: 本任务改变长期 Guru Team workflow / planning approval gate / companion script data contract，必须更新 durable docs 与 specs。
- Strategy: `ssot_first`
- Affected durable docs:
  - `docs/requirements/guru-team-trellis-flow.md`
  - `docs/requirements/requirement-main.md`
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `trellis/workflows/guru-team/README.md`
  - `trellis/presets/guru-team/README.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
- Task artifact delta: 仅保留 #93 的执行计划、证据与自检结果；长期合同写回 durable docs / specs。

## 验收标准

- [ ] canonical 与 dogfood `PLANNING_AMBIGUITY_CONTROLLED_TERMS` 包含 issue #93 定义的完整 v2 词表。
- [ ] canonical workflow、dogfood workflow、platform overlays、spec、durable docs 中展示的词表与脚本常量一致。
- [ ] `record-planning-approval` 扫描 `prd.md`、`design.md`、`implement.md` 正文，并在写入 artifact 前阻塞未分类或 `contract_violation` 命中。
- [ ] `check-planning-approval` 重新扫描三份 planning artifacts，并在扫描结果与 artifact 不一致时阻塞。
- [ ] `planning-approval.json` 中所有命中写入 `hits[]`；未分类命中和 `contract_violation` 命中写入 `unchecked_normative_hits[]`。
- [ ] 允许分类命中不写入 `unchecked_normative_hits[]`，且包含非空分类和理由。
- [ ] 单测覆盖 v2 词表中每个词。
- [ ] 单测覆盖 `推荐`、`可选`、`至少`、`默认` 的阻塞路径。
- [ ] 单测覆盖八类允许分类。
- [ ] 单测覆盖 `至少`、`默认`、`可选`、`相关` 缺少 issue #93 要求的确定性信息时的阻塞路径。
- [ ] Phase 2 check 与 Branch Review Gate 将 planning ambiguity scanner 结果纳入 review scope。
- [ ] #83 的语义边界保留：脚本扫描不得替代 AI ambiguity review。
- [ ] preset apply 与 dogfood overlay drift check 通过或在最终报告中明确阻塞证据。
- [ ] 至少执行 targeted Python unit tests、Python compile、Bash syntax、JSON validation、task validate、diff check。

## Open Questions

无。Issue #93、#83 artifact、当前代码和官方 Trellis 文档足以进入实现规划。
