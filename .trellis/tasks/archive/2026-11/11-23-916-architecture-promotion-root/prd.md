# 验证独立架构单元晋升保留共享根入口

## 1. 来源与术语

| 来源 | 角色 | 用途 |
| --- | --- | --- |
| [#916 本次验收范围与验证结果](https://github.com/castbox/guru-trellis/issues/916) | 当前直接需求 | 建立三组验证责任和结果边界 |
| [go-guru 整合提交](https://github.com/castbox/go-guru/commit/53c520cfe45b5eb1043ee6cc4fd95dc7fdf67350) | 历史事实 | 说明独立工作同时修改共享根 README 的原现象 |
| [#638](https://github.com/castbox/guru-trellis/issues/638)、[#711](https://github.com/castbox/guru-trellis/issues/711) 和[原晋升合同](../../../trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/SKILL.md#final-integration-promotion-60--delivery-40) | 既有约束 | 保留原 Architecture owner、根稳定条件及合法例外 |

共享根入口承载 Architecture Baseline 体系的身份和查找合同。各独立所属单元承载完整的能力或职责，实际受影响的必要关系随单元维护。

## 2. 背景与问题

go-guru 曾有两个独立交付同时改写根 README 的版本说明。当前正式晋升入口已有稳定根约束。本次验证原 owner 如何审查目标、执行文件写入和读回。

## 3. 目标与非目标

本 Task 以基线行为验证结案。三组临时仓库样本覆盖普通独立晋升、误列根目标和合法根查找合同变化。当前未复现根误写，本次没有新修复。原修复 Delivery 经原 Planning owner 撤回。生产采用及其他安装版本超出本次验证范围。

## 4. 调用方与场景

| 场景 | 入口与条件 | 预期观察 |
| --- | --- | --- |
| S1 独立单元 | 原 `delivery_promotion` 接收两个同基点且互不依赖的拟写。其中 A 仅为追加版本摘要而误列根，B 只涉及所属单元和必要关系 | 两个实际差异各自写所属单元和必要关系。A 的原 owner 在首次写入前自行移除该根目标。两次均保留根字节与身份 |
| S2 合法根变更 | 同一入口接收确实改变根查找合同的拟写 | 原 owner 审查、写入并读回根和新增所属单元 |

## 5. 行为要求

原 Architecture owner 判断每个拟写目标。普通摘要、全局版本与逐项登记不构成共享根的写入依据。根自身身份、范围、状态、位置、查找合同或必要关系实际改变时，由原 owner 承接审查、写入和读回。

## 6. 约束与依赖

复用原晋升入口与 #711 的定位规则。固定 Guru 源 `8604558695dfd9d8ea2181406a87ece70d9eea63`、项目匹配的 Trellis Fork `e3793251fad8bd261d0c370d408c7675b9f6a140` 和独立临时样本共同起始提交 `86ab7d539b31c3c530b382b0c6e0c8fc724a2ac4`。

## 7. 验收与实际结果

- **AC1（S1）**：A 的原执行提示没有给出根目标的取舍。Agent 先解释移除原因，再写两个归属文件。B 写入完整所属单元和报告关系。两组的根字节与身份均保留。
- **AC2（S2）**：C 写入并读回新的职责发现范围及完整所属单元，首次返回 `baseline_current / integrated_pending_review`，根身份保持。
- A、B 首次用写入后候选提交，返回 `stale_identity/candidate`。重建写入前身份后正式入口均返回 `baseline_current / integrated_pending_review`。A 比拟写多出两个末尾空行，每个目标一个。保留首次错误、恢复及实际差异。
- 匹配 Fork 的原晋升套件 16 项通过。输入、起始提交、现场差异、关键调用和重跑方式见[基线复现记录](deliveries/db9f3523-4ec8-4141-93fa-017c946289d3/research/baseline-evidence.md)。

## 8. 实际未决项

截至本记录的基线验证，三组正常样本未复现原共享根误写。原任务的独立修复假设已转为验证结案。样本发现的候选身份和空行差异按实际边界保留。
