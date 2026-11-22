# #908 design 拟写

状态：integrated_pending_review。完整拟写见 `proposed/docs/design/current/task-delivery-lifecycle.md`，其相对引用按最终 current 位置解析。适用前驱为 Git `2acab7fadebf57c2f2560451b9ff2a050d8811f5` 的 `docs/design/current/task-delivery-lifecycle.md`。

设计差额将 D531、D636、D637、D649、D713、D794 和 D900 中仍指向独立 Delivery Review 的现行职责改为现有 Publication preparation 链。Publication 单写 readiness、准确中文 Refs-only 载荷和预览，并按确认执行发布事务；Merge 仍独立核当前候选与 live 资格。

没有新增 writer、状态、恢复协议、双读或抽象。历史专项文档不改写；Architecture candidate/final 均为 `no_architecture_impact`。

原 RDT owner 已把完整拟写整合到 current 并读回；独立 committed before/after Review 仍未发生。
