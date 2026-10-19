# 早期 Draft 原 owner 设计责任当前 authority

版本：`current-main-0.7.0-guru.113`；状态：`active`；前驱：`current-main-0.7.0-guru.112`。继承 Architecture `current-main-0.7.0-guru.104/active`，来源为 [Architecture authority](../../../architecture/README.md)。RDT 与 Architecture 各由原 owner 晋升，本入口只定位完整当前知识。

| Scope identity | Status | Complete definition | Relations |
| --- | --- | --- | --- |
| RDT-LIFECYCLE | current | [Task/Delivery](../../current/task-delivery-lifecycle.md) | 原稳定identity与迁移边界保持 |
| RDT-COMPLETION | current | [Completion/Closure](../../current/completion-closure.md) | 原整体完成/Closure职责保持 |
| RDT-KNOWLEDGE | current | [知识维护](../../current/knowledge-maintenance.md) | 两套原owner及技术栈源关系保持 |
| RDT-NATIVE | current | [三系统兼容](../../current/native-compatibility.md) | [R630→D630→T630](../../../requirements-design-test-contributions/630-native-compatibility/traceability.md) |
| RDT109-LEGACY | legacy_unmigrated | [原完整来源](../current-main-0.6.17-guru.109/design-main.md) | 仅未列入已迁移单元的对象，不覆盖current定义 |

本版将 #636 的早期有界提交、同 PR Draft 反馈、独立固定候选分析与风险验证承接进完整生命周期单元；最终完整质量、Refs-only/整体 Closure、ADR-028 和 ADR-030 保持。Completion/knowledge/native 等未受影响单元保留。完整前驱定义通过 immutable Git `b470580d4f79f61c66d72db97861fe1564b5e746:docs/` 读取并在同 tree 解析引用，不将旧版本页与后来 mutable current 混读。实际执行和未验证边界唯一见 [#636 Test](../../../requirements-design-test-contributions/636-early-draft-pr/test.md)；知识晋升不证明软件 Release、真实 GitHub 全部场景或整体 Completion。
