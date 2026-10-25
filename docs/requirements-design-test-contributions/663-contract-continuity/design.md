# 流程合同连续性：设计差额

完整拟写定义在 `proposed/docs/design/current/task-delivery-lifecycle.md`。新增 D663-01..05 / CON663-REPAIR/ARCHIVE/BEFORE/MAINTENANCE/DISTRIBUTION，与对应 R663 一一关联。精确公共字段、schema、wrapper和typed exits仍由三个canonical packages单写；本层拥有职责和协作条件。

Architecture 原 owner判断 target_native，真实 before缺失的决定由 ADR-CONTRACT-CONTINUITY候选承接。原 RDT/Architecture owners在候选Check后串行 final_integration，写完整单元并读回；implementation重绑实际after，再最终质量链。无根identity或导航变化，不强制更新总README。
