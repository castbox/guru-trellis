# Architecture Baseline SSOT

版本：`current-main-0.7.0-guru.104`；状态：`active`；predecessor：`current-main-0.7.0-guru.103`。普通读取按下表职责定位完整正文；历史版本和贡献不替代 current 定义。

| Identity / role | Status | Locator | Relations |
| --- | --- | --- | --- |
| FOUNDATION | accepted_constraints | [baseline](./00-foundation/baseline.md) / [constitution](./00-foundation/design-constitution.md) | 横向约束；constitution-v1 |
| ARCH-FND-STACK-001 | accepted_selection | [项目栈选择](./00-foundation/stack-selection.md) | [trellis-extension-stack@1.0](../../trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md) |
| CURRENT | evidence_bound | [system](./01-current/system.md) | [EVIDENCE](./evidence/current-evidence.md) |
| TARGET | accepted_target | [target](./02-target/target.md) | [GAP](./05-gaps/current-to-target.md) / [PLAN](./07-plans/roadmap.md) |
| DOMAIN | current_boundaries | [ownership](./03-domains/ownership.md) | [INTEGRATION](./04-integrations/distribution.md) |
| ARCH-GOV-001..012 | current | [rules](./06-governance/rules.md) | [change contract](./06-governance/change-contract.md) / ADR-005/028/030/031/033 |
| ADR | historical_decisions | [index](./adr/README.md) / [ADR-031](./adr/031-current-effective-knowledge.md) | current 正文保留替代范围与来源 |
| ARCH100-PINNED-TASK | historical_applicable | [固定旧authority](https://github.com/castbox/guru-trellis/blob/bdb5185c673c91b2fb5cfc66ffbb33849904a69c/docs/architecture/README.md) | immutable Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c:docs/architecture/` |
| ARCH101-PREDECESSOR | historical_applicable | [前驱完整 authority](https://github.com/castbox/guru-trellis/blob/33f18a768c9c8d901f34b899934ac40c3d97cc5b/docs/architecture/README.md) | `current-main-0.6.17-guru.101`；successor `current-main-0.7.0-guru.102`；immutable Git `33f18a768c9c8d901f34b899934ac40c3d97cc5b:docs/architecture/` |
| RDT | active | [Requirements](../requirements/README.md) / [Design](../design/README.md) / [Test](../test/README.md) | `current-main-0.7.0-guru.113` |

各分区职责保持。新正文收敛 ARCH-GOV-008/009/011 的已接受后继，并增加完整知识和两层栈关系；其它分区保留原正文及适用边界，不宣称所有历史能力均已重新迁移。迁移来源/旧 Task 退出见 [MIGRATION-331](../../trellis/presets/guru-team/MIGRATION-331.md)，本轮贡献见 [331](./contributions/331-current-effective-knowledge.md)。实际验证和未验证边界只由 [唯一 Test](../requirements-design-test-contributions/331-current-effective-knowledge/test.md) 维护。知识接受、CURRENT 实现、Delivery、Task Completion 与软件 Release 分开判断。

ARCH102-PREDECESSOR / historical_applicable：[固定前驱 .102](https://github.com/castbox/guru-trellis/tree/0543731bf52aa80842fde5db47332380de513cf0/docs/architecture)。在同一 immutable Git tree 解析完整authority及必要引用。

#630新增职责由[贡献](./contributions/630-native-compatibility.md)、[ADR-032](./adr/032-managed-text-lf.md)及current/domain/integration完整单元承接。实际结果只由[#630唯一Test](../requirements-design-test-contributions/630-native-compatibility/test.md)拥有；知识版本与软件Release/Task Completion分开。

#636 的职责后继见 [贡献](./contributions/636-early-draft-pr.md)、[ADR-033](./adr/033-early-draft-feedback.md) 与 ARCH-CUR-075 / ARCH-DOM-058 / ARCH-INT-061。实际实现、安装、Agent和远端结果仅由 [#636 唯一Test](../requirements-design-test-contributions/636-early-draft-pr/test.md)记录；知识晋升不证明软件Release、业务采用或Task完成。
