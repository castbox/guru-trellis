# 发现阶段 fitness 出口：D1 需求

## 1. 整体来源与术语

整体权威为本 Task 根 `prd.md`，accepted_scope revision `sha256:400b4d26abfb52f7404bdae13351a2481948f9bbdf9efa1f67db8f6e8cccb3d2`。本批 scope_ref 仅选择 V1、V2、V3、V4。Direct Source [#690](https://github.com/castbox/guru-trellis/issues/690) 的完整目标、正常复现和约束保持；V5 属于整体后续责任。公共 DeliveryKey 和 planning_root 从原 Creation 输出取得。原始阶段、出口、consumer 和 router 术语见根 PRD 第1节及当前 Architecture package interface。

## 2. 整体与本批目标、非目标

当前合法 implementation_discovery 回归在 stdout 被阶段枚举拒绝。本批补齐正式输出及当前 consumer 合同，提供可独立合并的源码、回归和安装投影证据。保留原 stage、DeliveryKey、planning_root、regression_refs、return_route 及普通身份校验。

不承担现场更新、ABTest、业务 reconcile/部署、完整审计或 Release 矩阵。不得改标阶段、改报 baseline_current、删除 finding 或绕过 validator。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首个 Delivery，没有前序。起点为 main@00b1b6f29a5ad7f6591f0ef43573ef8ba798222b；输入及 semantic result 已接受发现阶段，output/current consumer 尚缺枚举。现有受控 fixture、正式 public wrapper 和 preset reapply 为依赖。

本批完成根 PRD V1–V4。V5 留给原业务 Architecture owner：正式来源可安装并依业务仓授权采用后，重新审核同条件并确认实施承接。整体 Completion 在该证据缺失时不能宣称现场解除；源码 Delivery 不等待它。

## 4. 本批调用方、场景与流程

D1-S1：有效 Task/Delivery 和候选中，原 owner 以 delivery_task_impact_sync、implementation_discovery 判断 fitness_regression；正式 wrapper 保留所有身份及回归信息，实际 stdout 被 producer、聚合及当前 consumer 接受，原 router 按 implementation/check 接续。

D1-S2：既有 Planning、phase2、final_integration 与两种 return_route 保持；普通无效或过期身份仍返回原错误。

D1-S3：canonical 修改经现有 apply 同步完整安装与平台投影，再 reapply/drift 和 sidecar 核验。

## 5. 完整行为、条件与约束

根 PRD R1–R6 全部作为本批兼容边界适用。具体补齐 runtime 选中的 Delivery output、interface 聚合 public-output-fitness-regression-index-5.0、当前 fitness-regression-5.0 consumer 和仍受引用/分发的 delivery-1.0 consumer；不能只修兼容文件。保留公共 id 及现有字段，不泛化其它历史 API。

测试样本必须保持原 profile/stage/exit、身份关系、root/refs/route，用测试仓有效身份和候选替换业务专有值。沿正常身份、候选、schema 与正式 wrapper 边界执行；自动回归可提供受控 owner result，它仅证明确定性承接。不得增加人为伪造或攻击负例。规范性来源设计的唯一处置由本批 design 第3节维护。

## 6. 本批验收、验证方式与未决项

| AC | 需求/场景 | 验证输入、入口和观察 |
| --- | --- | --- |
| V1 | R1/R3/D1-S1 | 等价有效 fixture 经正式 wrapper：修复前 stdout schema_mismatch，修复后原 stage fitness_regression |
| V2 | R2/D1-S1 | 同一实际 stdout 通过 runtime output、interface aggregate/current consumer；字段完全保持。AI router 消费与结构验证分开报告 |
| V3 | R6/D1-S2 | 两种 route 及受影响 Planning/phase2/final_integration 最小回归，原 stale 检查保持 |
| V4 | R5/D1-S3 | canonical/installed/platform parity、reapply/drift、sidecars 定向检查；至多一个必要代表 clean install |

没有待决产品范围选择。实际测试和安装尚待执行；业务 V5 和完整 Release 矩阵不属于本批成功声明。

## 7. Canonical 引用与本轮差额

`docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` 为 Architecture 约束。`docs/architecture/04-integrations/distribution.md` 的 ARCH-INT-001/006 为分发约束；`.trellis/workflow.md` 的 guru-architecture-baseline-check-router 为既有回程。当前 Architecture package interface/runtime/schemas 拥有具体公开合同；`tests/test_contract.py` 为验证扩展点。

本轮修复实现对已有合法阶段承诺的遗漏，不新增流程、owner、状态或共享设计选择。实际 Architecture 影响由独立 owner 判断；知识维护策略在 implement 的 Docs Plan 明确，不预创建空 contribution。
