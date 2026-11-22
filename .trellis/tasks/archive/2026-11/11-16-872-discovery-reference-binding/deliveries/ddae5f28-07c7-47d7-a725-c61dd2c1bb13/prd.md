# D1 Discovery 关联检索与草稿绑定需求

## 1. 整体来源与术语

整体 authority 为 .trellis/tasks/11-16-872-discovery-reference-binding/prd.md（accepted_scope，AC872-01）；Direct Source 为 [#872](https://github.com/castbox/guru-trellis/issues/872) 全文。当前 scope_ref 选择 AC872-01，planning_root 为 deliveries/ddae5f28-07c7-47d7-a725-c61dd2c1bb13。关联引用是背景/检索线索；真实绑定是同内容已有 Issue 的来源关联。原字段/一致性约束为兼容承诺，不能混用。

## 2. 整体与本批目标、非目标

本批全量修复正常新草稿的调用指引：有真实关联线索却没有外部绑定时，调用方能构造正确输入并继续原 Discovery。覆盖整体 R1—R4、S1—S3 和 AC872-01。保留整体 PRD §3 的非目标；不交付下游业务或重写检索/校验架构。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 D1，无前序 Delivery。起点 main@e33ecf82d：draft+非空 issue_refs 要求对象，空 issue_refs 要求 null；现有合同缺少就地解释，普通字段错误可由原 owner 纠正。整体需求已接受；尚未实施或验证。D1 无延期范围；整体 Completion 需实施、原检查与独立 Review、合并、来源关闭及正式收尾，不能只凭 PR 合并。

## 4. 本批调用方、场景与流程

S1：Discovery owner 阅读修改后的原指引，为关联已有 Issue 的未绑定新草稿组装输入，保留线索，经公开 record/check/invoke 得 context_ready。
S2：同一正常装配将关联编号误放入触发绑定的字段时，保留首次失败，按准确条件纠正并重跑；不伪造对象、不宣称未知内部错误。
S3：确有同内容绑定时，保持原来源/内容一致性校验，不推广 null。

## 5. 完整行为、条件与约束

R1 在原 Skill/contract/example 清晰解释字段、适用条件和关联线索表达，不删除线索。R2 保留 AI语义、public I/O及真实绑定校验。R3 复用已有普通纠正续接，必要诊断改动须基于真实缺口。R4 canonical修改经原 installer同步投影。terms 与 issue_refs 计分不同；局部通过不能当作完全等价或完整修复。具体方案由 candidate_assessment 与后续 design 明确，不预填通过。

## 6. 本批验收、验证方式与未决项

AC872-01：实际调用方从修订指引构造含关联线索的未绑定草稿，保留检索用途并实际调用公开三阶段到 context_ready；普通装配错误可纠正重跑，真实绑定一致性仍保持。既有字段/绑定回归可复用，只补实际缺口；固定文本或局部schema 不独立证明 Agent行为。不要求下游 Clarify/Readiness/真实创建或业务采用。无用户未决选择；未来实现/验证结果尚未建立。

## 7. Canonical 引用与本轮差额

- trellis/skills/guru-team/packages/guru-discover-change-context/{SKILL.md,references/contract.md,examples/history-preview.md}：字段、当前 authoring 与恢复指引，拟定向补齐。
- 同 package schemas/change-context-owner-result-4.0.schema.json、runtime/common.py、tests/test_contract.py/test_runtime.py：现行组合约束、检索语义和回归承接，优先复用。
- docs/requirements/README.md、docs/design/README.md、docs/test/README.md：沿原 RDT 评估是否有真实共享知识差额，不制造新资产。
- docs/architecture/README.md、00-foundation/design-constitution.md、06-governance/change-contract.md：独立 Architecture owner 依真实候选评估，未预设无影响。
