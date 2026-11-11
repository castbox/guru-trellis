# D1 交付目标预检：隔离 RDT 候选

本贡献属于 Task `delivery-target-preflight` generation `0`、Delivery `ab2f681d-68b8-4678-8f76-bb4dfad94c6b`。范围由[整体 PRD](../../../prd.md)及[本批规划](../design.md)定义。状态为 `proposed`；完整候选供原 candidate Check 消费，不是 shared current。

适用前驱为 immutable Git `e30c7bb5d4c24bc075dc14cfcd04c1da00fcf78e`。以下三份候选保留该提交对应完整单元的全部正文、稳定身份、历史来源与关系，仅修改候选状态并补交付目标预检段落。候选内继承的相对引用按表中实际目标位置解析；当前物理位置不形成第二套 current。晋升时由原 RDT owner 重读真实目标、整合差额并将状态恢复为 `current`。

| 完整 proposed | 实际目标及既有 stable unit | 本轮要求 → 设计责任 → 验证关系 |
| --- | --- | --- |
| [requirements](proposed/requirements.md) | `docs/requirements/current/task-delivery-lifecycle.md` / `RDT-REQ-LIFECYCLE` | `BEH-DELIVERY-TARGET-PREFLIGHT`；承接 Task R1–R4，保留 R154、R531、BEH567 的原职责和条件 |
| [design](proposed/design.md) | `docs/design/current/task-delivery-lifecycle.md` / `RDT-DES-LIFECYCLE` | `CON-DELIVERY-TARGET-PREFLIGHT` → `BEH-DELIVERY-TARGET-PREFLIGHT`；承接 Task R1–R5 |
| [test](proposed/test.md) | `docs/test/current/task-delivery-lifecycle.md` / `RDT-TST-LIFECYCLE` | `SCN-TARGET-01..05` → `CON-DELIVERY-TARGET-PREFLIGHT` → `BEH-DELIVERY-TARGET-PREFLIGHT`；承接 Task R1–R6、AC1–AC5 |

变更类型为原单元内增加，不删除、拆分或替换既有身份与适用约束。完整详细方法仍由 `trellis/skills/guru-team/packages/guru-author-task-plan/references/planning-body.md` 第4节单写，三个模板仅消费，Approval 沿原 Policy 维度判断，Delivery Review 保留发布前核对。没有 runtime、公共 DTO/schema、phase 或发布能力变化，不创建共享索引或前驱台账。

Architecture 继承 `docs/architecture/README.md` 在上述固定 Git 的 `active` 身份。独立 candidate assessment 已返回 `baseline_current / no_architecture_impact`；此贡献不写 Architecture，也不替代后续阶段的独立判断。本 Task 起点及当时 main 目标均为 e30，无未交付继承前驱，不承担旧 Task 交付。

候选只定义预期与证据边界。行为对照、安装、candidate Check、final integration、最终 Check 和 committed Review 各消费自己的实际结果；本文不预填通过或新版优胜。原 candidate Check 之后，才由原 RDT owner 进入 `promotion / final_integration` 写入、读回三个真实目标，再由实施者重绑全部实际 after 差额进入最终质量链。shared README/index、其他完整单元及 Architecture 不在拟写集合内。
