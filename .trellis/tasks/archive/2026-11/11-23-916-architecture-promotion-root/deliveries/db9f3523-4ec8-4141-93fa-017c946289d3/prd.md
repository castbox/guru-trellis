# D1 修复独立架构单元晋升的写前目标审查

## 1. 整体来源与术语

本 Delivery 选取[整体需求](../../prd.md)的 AC1、AC2，承接 R1 至 R4。适用范围和版本取自当前 Delivery 的公共 scope_ref。拟写目标包含文件定位、写入前内容和拟写后的完整内容。实际结果是原 Architecture owner 完成写入和读回后，正式入口返回的整合结果及可见文件差异。

| 来源 | 角色 | 用途 |
| --- | --- | --- |
| [#916 期望行为与验收](https://github.com/castbox/guru-trellis/issues/916) | 直接要求 | 确定普通误列、合法根变化和临时仓库验收 |
| [历史整合提交](https://github.com/castbox/go-guru/commit/53c520cfe45b5eb1043ee6cc4fd95dc7fdf67350) | 历史事实 | 对照同时改写共享根版本和说明的现象 |
| [#638](https://github.com/castbox/guru-trellis/issues/638) 与 [#711](https://github.com/castbox/guru-trellis/issues/711) | 已接受约束 | 保留最终整合 owner、稳定根入口与独立单元发现 |

## 2. 整体与本批目标、非目标

本批覆盖 #916 全部行为。原 Architecture owner 审查实际拟写目标，修订普通独立晋升中误列的共享根目标，并完整写入和读回适用目标。本批还验证同一入口允许真实的根查找合同或必要关系变化。业务仓库仍是历史证据来源。

## 3. 本批起点、前序结果、依赖与剩余责任

本 Task 尚无前序 Delivery。开发基点为 `main@8604558695dfd9d8ea2181406a87ece70d9eea63`，交付目标为 `origin/main`。该基点已有稳定根与原晋升读回合同。正式验收依赖与基点及待验候选匹配的临时仓库环境和原晋升入口。整体 Completion 仍须核对本批实际交付及 AC1、AC2 的可重跑证据。

## 4. 本批调用方、场景与流程

原 Architecture owner 在最终整合接收完整拟写。在首次写入前，该 owner 核对适用目标、完整内容与真正受影响关系。

- **D1-S1**：从同一临时仓库基点分别推进两个互不依赖的 Delivery 变更。一个拟写仅为更新版本说明而误列根 README。原 owner 在写前修订该方案。两次实际晋升分别写各自的完整单元及必要关系，读回结果，保留根 README 和根身份。
- **D1-S2**：一个正常拟写改变根自身的查找合同或必要关系。原 owner 核对实际理由，写入并读回合法根变化及其真正受影响关系。

## 5. 完整行为、条件与约束

原 owner 在写前审查每个拟写目标。根入口仅为本版摘要、全局版本或逐项登记而被列入时，先修订拟写目标。根本身的身份、范围、状态、位置、查找合同或必要关系有实际变化时，由原 owner 维护。独立单元维护完整定义与实际关系，沿 #711 的目录和稳定标识查找。写入和读回沿原最终整合入口。目标或读回与原合同不一致时，沿原 owner 的重读或回程处理。既有来源设计的处置由本批 design 第3节展开。

## 6. 本批验收、验证方式与未决项

- **AC1**：对 D1-S1 记录同一基点、两个独立触发输入、原 owner 写前处理、实际 diff 和正式调用结果。每个 diff 应包含对应单元及必要关系，根字节与根身份应与基点一致。
- **AC2**：通过同一正式入口执行 D1-S2。记录触发输入、写前依据、实际写入、读回及正式调用结果。合法根变更应出现在真实 diff。
- 原 owner 在实施前观察当前受支持路径，定位仍可复现的遗漏。历史冲突不替代当前行为观察。临时仓库数据和命令须足以重跑。

## 7. Canonical 引用与本轮差额

需求、设计和验证基础分别为 [R711](../../../../../docs/requirements/current/knowledge-maintenance.md#r711独立知识单元与稳定发现)、[D711](../../../../../docs/design/current/knowledge-maintenance.md#d711目录发现局部导航与原-owner-切换)和[知识维护测试单元](../../../../../docs/test/current/knowledge-maintenance.md)。Architecture 入口与组织关系见[根入口](../../../../../docs/architecture/README.md)，具体晋升合同由[原 Skill](../../../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/references/contract.md#final-integration-promotion-60--delivery-40)单写。本轮差额是写前目标审查及其实际入口观察，沿用既有稳定发现和最终整合行为。
