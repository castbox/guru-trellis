# ADR 候选：由 Publication 单独负责发布准备与远端事务

当前状态为提议。适用于 #900 的正常发布、回程和在途恢复。来源为 [#900](https://github.com/castbox/guru-trellis/issues/900)、#736 第 8 项和 AC7 的发布部分、ARCH-DOM-017、ADR-POSTCOMMIT-INDEPENDENT-REVIEW 与 ADR-009。

采用 Publication 作为 readiness 和预览的唯一语义入口。它通过既有角色记录真实 readiness，使用已有事务执行及回读已确认的远端操作。独立 Review 与适用架构资格仍是新动作前置。Merge 仍独立处理实际合并。

直接迁移受控消费者可以减少单独 `ready` 入口的公开装配，同时要求 workflow、owner 声明、接口和投影成套切换。旧入口的正常写入责任随切换结束。已执行的事实由原事务或固定原 provider 恢复，剩余写入遵循当前发布条件。历史证据保留其版本和 producer。采用与恢复范围由 MIGRATION-900 落实。

若消费方要求长期兼容、既有事务无法保留原身份或既有 Task/Delivery API 无法承接合法回程，先回方案与架构职责重新评估。验证先观察实际公开入口及效果，再观察在途操作和分发切换。具体计划见 [设计](design.md) 和 [实施计划](implement.md)。
