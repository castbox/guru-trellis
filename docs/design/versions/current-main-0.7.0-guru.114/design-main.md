# 早期 Draft 原 owner 设计责任当前 authority

版本：`current-main-0.7.0-guru.114`；状态：`active`；前驱：`current-main-0.7.0-guru.113`。继承 Architecture `current-main-0.7.0-guru.105/active`，来源为 [Architecture authority](../../../architecture/README.md)。RDT 与 Architecture 各由原 owner 晋升，本入口只定位完整当前知识。

| Scope identity | Status | Complete definition | Relations |
| --- | --- | --- | --- |
| RDT-LIFECYCLE | current | [Task/Delivery](../../current/task-delivery-lifecycle.md) | 原稳定identity与迁移边界保持 |
| RDT-COMPLETION | current | [Completion/Closure](../../current/completion-closure.md) | 原整体完成/Closure职责保持 |
| RDT-KNOWLEDGE | current | [知识维护](../../current/knowledge-maintenance.md) | 两套原owner及技术栈源关系保持 |
| RDT-NATIVE | current | [三系统兼容](../../current/native-compatibility.md) | [R630→D630→T630](../../../requirements-design-test-contributions/630-native-compatibility/traceability.md) |
| RDT109-LEGACY | legacy_unmigrated | [原完整来源](../current-main-0.6.17-guru.109/design-main.md) | 仅未列入已迁移单元的对象，不覆盖current定义 |

本版将 #637 候选适用性与覆盖要求合入完整生命周期单元，保留 R531/R567/R578/R600/R636 的有效条件、首次独立完整审核、当前正式结果、Refs-only/Closure、ADR-028/030/033。Completion、knowledge、native 等未受影响单元保持。完整前驱在 immutable Git `39169628f5f79cb48673eae96a36670e73f4dbbb:docs/` 的同 tree 解析，不混读旧版本页与后来 mutable current。实际执行与未验证边界唯一见 [#637 Test](../../../requirements-design-test-contributions/637-candidate-review-reuse/test.md)；知识晋升不证明软件 Release 或整体 Completion。
