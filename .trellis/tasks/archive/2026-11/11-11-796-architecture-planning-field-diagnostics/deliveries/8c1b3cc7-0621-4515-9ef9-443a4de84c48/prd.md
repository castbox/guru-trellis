
# #796 D1 规划字段诊断需求

## 1. 整体来源与术语

Direct Source：https://github.com/castbox/guru-trellis/issues/796 的目标与行为要求、最小验收及范围边界。
整体需求：[Task PRD](../../prd.md)；公共 accepted_scope 为 Task 记录中的该 PRD 内容引用。
本批 scope_ref 选取整体 AC1、AC2；planning_root 为本目录。identity 和 typed exit 定义沿用整体 PRD 第1节。

## 2. 整体与本批目标、非目标

当前 planning baseline_current 的两个 identity 遗漏通过 Schema，运行时直接读取后变成 internal_error。
D1 完整交付整体 R1—R4：明确字段诊断、Schema 与实际消费一致、复用原纠正路径和受影响投影同步。
不处理 Reconcile/Wording 未定位故障、全局异常框架、遥测、业务 Task 状态、独立恢复机制或新审核链。

## 3. 本批起点、前序结果、依赖与剩余责任

D1 尚无前序 Delivery。development baseline 为 main@e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e；当前只有 Task accepted_scope 与本批 planning 身份，未实施、未通过 Check。
已有证据是现场 payload、Schema 校验和正常 fixture 的 wrapper 复现。它们证明缺陷，不证明本批实现已完成或业务 #813 已恢复。
本批无延期责任；整体完成仍需实际修复验证、独立 Review、Delivery 合并、Task Completion/Closure/Finish。

## 4. 本批调用方、场景与流程

- D1-S1：Architecture owner 在 candidate_assessment 或 final_plan 提交 baseline_current，遗漏 baseline_identity 或 constitution_identity；原入口应定位缺失的 owner_result 字段并拒绝成功出口。
- D1-S2：同一 owner 按当前 authority、评估与合同补全输入，再经原 wrapper 得到原合法 typed exit；保留原失败记录。
- D1-S3：其它合法出口遵守各自分支合同，不新增无关 identity 负担。

## 5. 完整行为、条件与约束

- D1-R1：在读取两个 identity 前检查实际分支结构；缺字段使用既有错误合同给字段路径与纠正指引，不静默补值，不归为 internal_error。
- D1-R2：candidate_assessment/final_plan 共用的规划合同对齐运行时消费，保留其它 typed exit、身份、freshness 及 AI 语义门禁。
- D1-R3：复用原 Skill fresh re-entry，不增加恢复协议；公开合同或示例有实际缺漏时修正。来源设计承诺由本批 design 第3节唯一承接。
- D1-R4：沿原安装 owner 同步实际受影响的 canonical/dogfood/声明平台投影，不手工绕过受管更新。

## 6. 本批验收、验证方式与未决项

- AC1：从正式 invoke wrapper 分别观察两个 identity 缺失的明确字段诊断及非成功结果。用例按真实分支选取，共享逻辑不要求完整 purpose×字段矩阵。
- AC2：完整合法输入保持原 typed exit。复用适用正常路径与受影响回归，只补实际缺口。
代码、合同、投影验证不等同业务 Task 恢复或完整安装升级证明。本批需求无未决项。

## 7. Canonical 引用与本轮差额

- trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/runtime/invoke.py：_check_owner_result 的实际字段消费。
- 同 package schemas/semantic-result-delivery-1.0.schema.json：规划结果分支的结构合同；本轮缺口落点。
- 同 package references/contract.md：原 owner 评估、结果 authoring 和 fresh re-entry；实际缺漏才更新。
- 同 package tests/test_contract.py：正式 wrapper 正常路径和本次字段诊断覆盖。
- .trellis/spec/workflow/quality-guidelines.md 的 Test And Validation Value：选择最小可靠验证集。
Architecture authority/constitution/change-contract 由独立原 owner 按实际候选评估；本 PRD 不预填其通过或晋升结论。
