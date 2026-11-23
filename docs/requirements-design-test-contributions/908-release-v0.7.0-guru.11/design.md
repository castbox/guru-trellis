# #908 design 拟写

状态：integrated_pending_review。独立 committed Review 尚未发生，本状态不表示质量通过。适用前驱为 Git `2acab7fadebf57c2f2560451b9ff2a050d8811f5` 的 design current units。

Architecture assessment 为 `baseline_current / architecture_impact`，change path 为 `target_native`。设计消费 [908 Architecture contribution](../../architecture/contributions/908-release-v0.7.0-guru.11.md) 和 [ADR-POSTCOMMIT-INDEPENDENT-REVIEW](../../architecture/adr/postcommit-independent-review.md)：现有 Architecture current owners、consumer 关系和 ADR decision authority 原位更新，不保留 dual-read、第二 authority 或兼容 adapter。

本贡献的所有实际 design current targets 及其完整 after 如下：

- [task-delivery-lifecycle](proposed/docs/design/current/task-delivery-lifecycle.md) -> [current](../../design/current/task-delivery-lifecycle.md)
- [knowledge-maintenance](proposed/docs/design/current/knowledge-maintenance.md) -> [current](../../design/current/knowledge-maintenance.md)
- [completion-closure](proposed/docs/design/current/completion-closure.md) -> [current](../../design/current/completion-closure.md)

设计差额将 D531、D636、D637、D649、D710、D713 和 D900 中仍指向独立 Delivery Review 的现行职责改为现有 Publication preparation/readiness 链。Publication 单写 readiness、准确中文 Refs-only 载荷和预览，并按确认执行发布事务；Merge 仍独立核当前候选与 live 资格。Architecture 同步修正七个 current units，并把 ADR 状态收敛为 `accepted`，同时保留 #794 attribution、历史证据和未验证边界。

没有新增 writer、状态、恢复协议或抽象。原 RDT owner 已把完整 after 整合到 current 并读回；Architecture contribution 与 ADR 已进入 current relation，但独立 committed before/after Review 仍未发生。
