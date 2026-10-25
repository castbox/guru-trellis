# 〈Delivery 标题〉实施与验证计划

写作前实际加载 [共享正文合同](../references/planning-body.md)。以下六节按序填写；仅有执行步骤不能代替 design。`plan_ready` 前完成适用内容，保留原 Policy 与 Docs Plan 语义。

## 1. 输入与引用

定位整体范围、本批 PRD、design 第3节唯一来源设计处置、真实候选依赖及必要规格。每个必要引用写具体章节和用途，实施前实际加载完整相关条件。说明本批起点和前序输入，不把历史结果当本批要求。

## 2. 有依赖顺序的步骤与文件责任

按步骤 ID 写前置依赖、原责任模块/owner、实际文件、改动行为、可审核产物及完成观察。步骤应可执行；不能只写“按设计实现”。明确适用的前后 Delivery 接口与未完成责任。

存在真实临时限制时，按共享正文合同安排解除条件核对、当前行为／说明／断言更新及原后继 owner。没有变化时不制造维护步骤。

## 3. 验证入口、输入与预期观察

按验证 ID 写实际命令或受支持入口、环境/输入、预期结果、对应设计与AC，以及未验证边界。按依赖排序。规划时不预填 pass；确定性、实际 Agent、安装和外部证据不得混用。

## 4. 停止条件与适用回退点

写必要依赖缺失、来源/范围/机制变化及验证失败时的具体停点和原 owner。说明适用的本地回退、数据/发布恢复；无迁移/发布副作用时写明理由，不造回滚协议。保留并行改动；Git/GitHub 副作用仍按原边界处理。

## 5. Delivery Policy（唯一）

按 [原 Policy 合同](../references/authoring.md#solution-writing-and-complete-positive-capability) 选择 full/partial/staged，不发明新字段协议。full 写本批整体覆盖与完成条件；partial 写独立切片、剩余责任及整体 Completion 条件；staged 写有序阶段、当前阶段、进入/退出、剩余阶段及最终条件。没有延期责任不等于已完成验收，Delivery 合并不等于 Task Completion。

本批存在真实临时限制时，在 Policy 中写明对象、原因、解除条件、当前阶段边界和后继责任；限定到实际能力和适用环境。

## 6. Docs SSOT Plan（唯一）

定位解除后真正需要维护的当前规范、指南和派生说明，历史正文保持原观察。

按 [原 Docs Plan 合同](../references/authoring.md#solution-writing-and-complete-positive-capability) 选择一种 strategy，写真实差额、命中的 requirement/behavior、design、test、Architecture canonical 引用、原 writer、直接 consumer 和晋升时点。delta 在最终 Phase 2 前由原 owners reconciliation/promotion；no_docs_update_needed 说明依据。模板填充不写共享导航、不预建空贡献；真实 Architecture contribution/ADR 候选仍归原职责。
