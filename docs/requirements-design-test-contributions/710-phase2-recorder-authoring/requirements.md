# #710：正常 Check authoring 需求差额

状态：proposed。适用 authority 为 `guru-trellis-rdt`，固定 before 为 Git `2fc49bda6552d1a8bf95dff243ab2de9a9ea8e30`。整体要求由 [Task PRD](../../../.trellis/tasks/10-31-710-phase2-recorder-authoring/prd.md) 拥有；本批是 Delivery `63d55014-9fec-48da-a106-2a7403305977`，覆盖全部 R710-01..07 和 AC710-01..09。

完整拟写见 [Requirements 目标正文](proposed/docs/requirements/current/knowledge-maintenance.md)。本差额新增 R710/BEH710，承接正常 authoring 与结果消费分工、显式输入退出、真实 stale、候选及最终 native、finding 和 matching 安装证据。R331/R578/R638/R648/R649/R-MECH/R693 及前驱完整条件、稳定身份与历史引用保持。

本目录是完整隔离提案。目标正文中的相对引用按 manifest 所列最终 target locator 解析，保持实际晋升字节的关系；不以 proposed 内的目录名或目标正文中的 current 身份宣称已晋升。精确字段、argv、schema 和 profile 出口仅由 [原 Check 合同](../../../trellis/skills/guru-team/packages/guru-check-task/references/contract.md) 与其 interface/schema 单写。

原 RDT owner 在实现与行为证据齐备后执行 task_impact_sync；原 Architecture 和候选 Check 审完整提案，随后原 owners final_integration、写入读回，再由 implementation 重绑全部 actual after。这里没有提前写 shared current 或导航，也不以文档存在宣称实现、native 或安装通过。关系与来源见 [traceability](traceability.md)，实际观察见 [Test](test.md)。
