# Architecture Baseline SSOT

Identity：`guru-trellis-architecture`；状态：`active`。精确内容由完整Git revision与locator定位。下表仅定位正文、状态及历史来源；普通Task不要求写本入口或递增全局版本。

| Identity / role | Status | Locator | Relations |
| --- | --- | --- | --- |
| FOUNDATION | accepted_constraints | [baseline](./00-foundation/baseline.md) / [constitution](./00-foundation/design-constitution.md) | 横向约束；constitution-v1 |
| ARCH-FND-STACK-001 | accepted_selection | [项目栈选择](./00-foundation/stack-selection.md) | [trellis-extension-stack@1.0](../../trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md) |
| CURRENT | evidence_bound | [system](./01-current/system.md) | [EVIDENCE](./evidence/current-evidence.md) |
| TARGET | accepted_target | [target](./02-target/target.md) | [GAP](./05-gaps/current-to-target.md) / [PLAN](./07-plans/roadmap.md) |
| DOMAIN | current_boundaries | [ownership](./03-domains/ownership.md) | [INTEGRATION](./04-integrations/distribution.md) |
| ARCH-GOV-001..012 | current | [rules](./06-governance/rules.md) | [change contract](./06-governance/change-contract.md) / ADR-005/028/030/031/033/034 / ADR-KNOWLEDGE-FINAL-INTEGRATION |
| ADR | historical_decisions | [index](./adr/README.md) / [ADR-031](./adr/031-current-effective-knowledge.md) | current 正文保留替代范围与来源 |
| ARCH100-PINNED-TASK | historical_applicable | [固定旧authority](https://github.com/castbox/guru-trellis/blob/bdb5185c673c91b2fb5cfc66ffbb33849904a69c/docs/architecture/README.md) | immutable Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c:docs/architecture/` |
| ARCH101-PREDECESSOR | historical_applicable | [前驱完整 authority](https://github.com/castbox/guru-trellis/blob/33f18a768c9c8d901f34b899934ac40c3d97cc5b/docs/architecture/README.md) | `current-main-0.6.17-guru.101`；successor `current-main-0.7.0-guru.102`；immutable Git `33f18a768c9c8d901f34b899934ac40c3d97cc5b:docs/architecture/` |
| RDT | active | [Requirements](../requirements/README.md) / [Design](../design/README.md) / [Test](../test/README.md) | `guru-trellis-rdt` |
| ARCH102-PREDECESSOR | historical_applicable | [固定前驱 .102](https://github.com/castbox/guru-trellis/tree/0543731bf52aa80842fde5db47332380de513cf0/docs/architecture) | immutable Git `0543731bf52aa80842fde5db47332380de513cf0`；同tree解析完整authority和必要引用 |
| ARCH104-PREDECESSOR | historical_applicable | [固定前驱 .104](https://github.com/castbox/guru-trellis/tree/39169628f5f79cb48673eae96a36670e73f4dbbb/docs/architecture) | immutable Git `39169628f5f79cb48673eae96a36670e73f4dbbb`；同tree解析完整authority和必要引用 |
| ARCH105-PREDECESSOR | historical_applicable | [固定前驱 .105](https://github.com/castbox/guru-trellis/blob/9cec623833b61814f1175f31acde4fa81334cdb0/docs/architecture/README.md) | immutable Git `9cec623833b61814f1175f31acde4fa81334cdb0:docs/architecture/`；同tree读取原完整正文和必要关系 |
| ADR-KNOWLEDGE-FINAL-INTEGRATION | accepted | [knowledge-final-integration](./adr/knowledge-final-integration.md) | ARCH-GOV-008 / ARCH-DOM-053 / ARCH-INT-056 |

未列入代表迁移的能力仍由原完整正文及其必要来源拥有；[MIGRATION-331](../../trellis/presets/guru-team/MIGRATION-331.md)定位未迁移范围，[MIGRATION-638](../../trellis/presets/guru-team/MIGRATION-638.md)定位本次时机/身份切换。知识接受不证明Delivery、Completion、安装采用或Release。
