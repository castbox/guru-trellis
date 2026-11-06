# Test SSOT

| Identity | Status | Locator | Relations |
| --- | --- | --- | --- |
| `guru-trellis-rdt` | active | [目录发现入口](./current/README.md) | Architecture `guru-trellis-architecture` / [authority](../architecture/README.md) |
| RDT114-PREDECESSOR | historical_applicable | [固定前驱 .114](https://github.com/castbox/guru-trellis/blob/9cec623833b61814f1175f31acde4fa81334cdb0/docs/test/README.md) | immutable Git `9cec623833b61814f1175f31acde4fa81334cdb0:docs/`；同tree解析原完整正文与关系 |
| RDT-TEST-CURRENT | current | [目录发现入口](./current/README.md) | 完整定义位于本层 current/**；跨层关系由所属正文维护 |
| RDT109-LEGACY | legacy_unmigrated | [原完整来源](./versions/current-main-0.6.17-guru.109/test-strategy.md) | [范围与稳定引用映射](../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md) |
| RDT109-PINNED-TASK | historical_applicable | [固定旧导航](https://github.com/castbox/guru-trellis/blob/bdb5185c673c91b2fb5cfc66ffbb33849904a69c/docs/test/README.md) | immutable Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`; 原 Task 阶段适用版本 |
| RDT110-PREDECESSOR | historical_applicable | [固定前驱 .110](https://github.com/castbox/guru-trellis/blob/33f18a768c9c8d901f34b899934ac40c3d97cc5b/docs/test/versions/current-main-0.6.17-guru.110/test-strategy.md) | `current-main-0.6.17-guru.110`; immutable Git `33f18a768c9c8d901f34b899934ac40c3d97cc5b`; 完整单元与关系在同 tree 解析 |
| RDT111-PREDECESSOR | historical_applicable | [固定前驱 .111](https://github.com/castbox/guru-trellis/blob/0543731bf52aa80842fde5db47332380de513cf0/docs/test/versions/current-main-0.7.0-guru.111/test-strategy.md) | immutable Git 0543731bf52aa80842fde5db47332380de513cf0；同tree解析完整单元及引用 |
| RDT112-PREDECESSOR | historical_applicable | [固定前驱 .112](https://github.com/castbox/guru-trellis/blob/b470580d4f79f61c66d72db97861fe1564b5e746/docs/test/versions/current-main-0.7.0-guru.112/test-strategy.md) | immutable Git `b470580d4f79f61c66d72db97861fe1564b5e746:docs/`；同 tree 解析完整单元和引用 |

| RDT113-PREDECESSOR | historical_applicable | [固定前驱 .113](https://github.com/castbox/guru-trellis/blob/39169628f5f79cb48673eae96a36670e73f4dbbb/docs/test/README.md) | immutable Git 39169628f5f79cb48673eae96a36670e73f4dbbb；在同 tree 读取完整单元与关系 |

## 稳定发现与维护

采用边界：`knowledge-navigation-1`。本入口保留体系身份、范围/状态、真实版本与历史边界；下级 `current/README.md` 说明限定目录发现，不枚举全部单元。先判断问题/Task/阶段适用版本，再用 `rg --files docs/test/current` 与稳定 ID、别名或概念限定检索，读取完整正文及必要 R/D/T/Architecture 关系。核原 owner 的晋升依据、来源与状态；文件存在或搜索命中不能证明 current。accepted target、未晋升 contribution/proposed、历史和被替代定义保持区分。

独立主题的日常维护只写所属完整单元/能力目录和真实受影响关系，不修改总入口登记、全局版本或合并历史，也不转移到共享 index/manifest/metadata。入口自身身份、范围、状态、位置、查找合同或必要关系真实变化时，原 owner 才维护本入口。同能力或同一有效关系的重叠由原 owner 语义整合，Git 文本合并不能证明一致。

旧 Task 保留其阶段适用 Git/版本读取；最终整合命中已迁移单元时写真实当前目标，不双写旧索引。未迁移 `.109` 范围继续使用上表原完整来源。切换、恢复与安装采用由 [MIGRATION-711](../../trellis/presets/guru-team/MIGRATION-711.md) 定义；本页不是软件发布或业务采用证明。
