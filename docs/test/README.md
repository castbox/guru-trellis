# Test SSOT

| Identity | Status | Locator | Relations |
| --- | --- | --- | --- |
| `current-main-0.7.0-guru.114` | active | [版本入口](./versions/current-main-0.7.0-guru.114/test-strategy.md) | Architecture `current-main-0.7.0-guru.105` / [authority](../architecture/README.md) |
| RDT-TEST-CURRENT | current | [完整单元导航](./current/README.md) | Task/Delivery; Completion/Closure; knowledge maintenance; native compatibility |
| RDT109-LEGACY | legacy_unmigrated | [原完整来源](./versions/current-main-0.6.17-guru.109/test-strategy.md) | [范围与稳定引用映射](../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md) |
| RDT109-PINNED-TASK | historical_applicable | [固定旧导航](https://github.com/castbox/guru-trellis/blob/bdb5185c673c91b2fb5cfc66ffbb33849904a69c/docs/test/README.md) | immutable Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`; 原 Task 阶段适用版本 |
| RDT110-PREDECESSOR | historical_applicable | [固定前驱 .110](https://github.com/castbox/guru-trellis/blob/33f18a768c9c8d901f34b899934ac40c3d97cc5b/docs/test/versions/current-main-0.6.17-guru.110/test-strategy.md) | `current-main-0.6.17-guru.110`; immutable Git `33f18a768c9c8d901f34b899934ac40c3d97cc5b`; 完整单元与关系在同 tree 解析 |
| RDT111-PREDECESSOR | historical_applicable | [固定前驱 .111](https://github.com/castbox/guru-trellis/blob/0543731bf52aa80842fde5db47332380de513cf0/docs/test/versions/current-main-0.7.0-guru.111/test-strategy.md) | immutable Git 0543731bf52aa80842fde5db47332380de513cf0；同tree解析完整单元及引用 |
| RDT112-PREDECESSOR | historical_applicable | [固定前驱 .112](https://github.com/castbox/guru-trellis/blob/b470580d4f79f61c66d72db97861fe1564b5e746/docs/test/versions/current-main-0.7.0-guru.112/test-strategy.md) | immutable Git `b470580d4f79f61c66d72db97861fe1564b5e746:docs/`；同 tree 解析完整单元和引用 |

| RDT113-PREDECESSOR | historical_applicable | [固定前驱 .113](https://github.com/castbox/guru-trellis/blob/39169628f5f79cb48673eae96a36670e73f4dbbb/docs/test/README.md) | immutable Git 39169628f5f79cb48673eae96a36670e73f4dbbb；在同 tree 读取完整单元与关系 |
