# 三系统运行与安装一致性当前 authority

版本：`current-main-0.7.0-guru.112`；状态：`active`；前驱：`current-main-0.7.0-guru.111`。继承 Architecture `current-main-0.7.0-guru.102/active`，来源为 [Architecture authority](../../../architecture/README.md)；本轮必要字节决策的晋升仍由原Architecture owner独占，不由本RDT知识晋升替代。

| Scope identity | Status | Complete definition | Relations |
| --- | --- | --- | --- |
| RDT-LIFECYCLE | current | [Task/Delivery](../../current/task-delivery-lifecycle.md) | 原稳定identity与迁移边界保持 |
| RDT-COMPLETION | current | [Completion/Closure](../../current/completion-closure.md) | 原整体完成/Closure职责保持 |
| RDT-KNOWLEDGE | current | [知识维护](../../current/knowledge-maintenance.md) | 两套原owner及技术栈源关系保持 |
| RDT-NATIVE | current | [三系统兼容](../../current/native-compatibility.md) | [R630→D630→T630](../../../requirements-design-test-contributions/630-native-compatibility/traceability.md) |
| RDT109-LEGACY | legacy_unmigrated | [原完整来源](../current-main-0.6.17-guru.109/requirement-main.md) | 仅未列入已迁移单元的对象，不覆盖current定义 |

本版只增加#630原生兼容完整单元；既有单元、历史identity、未迁移范围与其条件不改。公共接口完整规格仍归原canonical owner。原current-main-0.7.0-guru.111完整定义可在固定Git `0543731bf52aa80842fde5db47332380de513cf0:docs/` 读取，并在同一tree解析引用；不将旧版本页与后来mutable current混读。实际验证、首次失败及未验证边界由 [#630唯一Test](../../../requirements-design-test-contributions/630-native-compatibility/test.md) 单写。知识晋升、软件Release、外部采用和Task Completion分开判断。
