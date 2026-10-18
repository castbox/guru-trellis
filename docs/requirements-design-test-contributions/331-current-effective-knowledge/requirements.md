# #331 当前有效知识需求差额

来源：[Issue #331](https://github.com/castbox/guru-trellis/issues/331)，目标、五组行为、验证/验收和边界；provenance=`source_confirmed`。状态 `promoted_source`；固定迁移比较起点是 main Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`，RDT `.109` / Architecture `.100`。文件存在不证明晋升或验收。

| Requirement / behavior | 本轮完整差额与唯一正文 | Design / test |
| --- | --- | --- |
| R331-01 / BEH331-01 | 按问题和阶段选择完整适用单元，保留全部有效条件/否定/例外/顺序，current/target/unconfirmed/history/superseded分明；不靠摘要或版本历史拼出普通当前答案。见 [knowledge](../../requirements/current/knowledge-maintenance.md)。 | D331-01/04 → T331-01/04/05 |
| R331-02 / BEH331-02 | 局部一致R/D/T/Architecture影响；稳定身份不绑定位置，replacement/deletion/split/merge可追溯；贡献隔离，晋升后完整定义含所有增量。见 [knowledge](../../requirements/current/knowledge-maintenance.md)。 | D331-02/04 → T331-02/03/05 |
| R331-03 / BEH331-03 | 原RDT和Architecture owners不变；通用技术栈source/version与项目选择/约束/差异分别拥有正文和适用关系；不越界共享写或声称外部采用。见 [knowledge](../../requirements/current/knowledge-maintenance.md)。 | D331-03 → T331-04/05 |
| R331-04 / BEH331-04 | 完整单元/薄导航/历史各自职责，日常Planning/实施/最终Check/Review/promotion实际使用；AI判断与确定性执行分开。见 [lifecycle](../../requirements/current/task-delivery-lifecycle.md) 与 [knowledge](../../requirements/current/knowledge-maintenance.md)。 | D331-01/04 → T331-01/03/05/06 |
| R331-05 / BEH331-05 | 实际迁移代表性三主题RDT与Architecture治理，保留旧版本/阶段适用/引用/历史；缺口原repair，切换/恢复和旧读取退出明确；canonical/installed/update/reapply保持。见 [knowledge](../../requirements/current/knowledge-maintenance.md)。 | D331-05 → T331-03/04/05/06 |
| R331-06 / BEH331-06 | 实施前固定九场景覆盖的同语义多次真实Agent对照；逐样本正确性/成本/维护/首次失败和修复，分开行为、机械、安装与外部证据。见 [knowledge Test](../../test/current/knowledge-maintenance.md)。 | D331-06 → T331-01..06 |

实际采用是三组完整R/D/T正文：[Task/Delivery](../../requirements/current/task-delivery-lifecycle.md)、[Completion/Closure](../../requirements/current/completion-closure.md)、[Knowledge](../../requirements/current/knowledge-maintenance.md)。旧有效identity及后继关系见 [traceability](./traceability.md)，不是全部历史语料迁移声明。Architecture能力和generic/project正文由原owner单写，本贡献只引用公开位置与关系。无新公共API/Skill/schema/状态机，无恶意模型、压力加固、生产业务修改或完整Release矩阵。
