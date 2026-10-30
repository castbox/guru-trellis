# Architecture 发现阶段 fitness 出口合同：整体需求

## 1. 来源与术语

Direct Source 为 [castbox/guru-trellis#690](https://github.com/castbox/guru-trellis/issues/690)，完整正文的目标与范围、正常复现、V1–V5 及交付边界为要求。已确认根因是当前源码证据；ABTest 仅为真实触发背景。#663 的归档 PRD 为历史约束，不授予本次验收通过。公共合同以当前 canonical `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/` 的 interface、input、semantic result、runtime、output 和 consumer 为准。

`implementation_discovery` 是原发现阶段；`fitness_regression` 表示 Architecture owner 判定适用回归；`return_route=implementation|check` 指向既有 `guru-architecture-baseline-check-router` 的原责任 owner。DeliveryKey 和 planning_root 为当前公共身份，不是新恢复协议。

## 2. 背景与问题

业务 #822 的合法发现调用通过输入及 AI result 校验后，在正式 stdout 输出校验报 `schema_mismatch/stdout`。当前 main@00b1b6f29 的 Delivery fitness 输出及当前 interface consumer 遗漏该阶段，runtime 原样投影 stage，导致真实发现不能交还实施。现场 schema 反事实结果不是修复后正式 wrapper 或业务原生流程证明。

## 3. 目标与非目标

整体目标是补齐公开合同链、完成 V1–V4 源码 Delivery，并保留 V5 后续整体验收责任。不能把 Delivery 合并当成现场 block 已解除。业务安装正式采用后，原业务 Architecture owner 必须重新审核并确认实际返回实施 owner；没有该证据时 Task/Issue 的整体验收仍留待原 Completion 判断。

不承担 ABTest Key 接线、业务 reconcile/部署/PR 合并、全流程审计、安全加固或完整多平台 Release 安装矩阵。不得改标 phase2、改报 baseline_current、删除 finding 或绕过 validator。

## 4. 真实调用方、场景与流程

S1：原 Architecture owner 在有效 Task/Delivery 和合法候选上，以 delivery_task_impact_sync、stage=implementation_discovery 判断回归，通过正式 `scripts/invoke.sh --invocation -` 返回原阶段 fitness_regression。相同 stdout 经实际 Delivery output、interface 聚合 output 和当前 consumer 接受，既有 router 按 return_route 交还原 owner。

S2：现有 implementation/check 两种 return_route 均保留。Planning、phase2 和 final_integration 继续沿原合法合同；普通错误和过期身份检查保持。

S3：canonical 经现有 preset apply/reapply 分发到 dogfood 与声明平台，sidecar 逐个处理，drift 检查证明当前受影响包一致。

S4：正式修复可安装后，原业务 owner 沿业务仓自己的授权与发布流程更新安装，重新审核原发现条件，观察实际出口及实施承接；源码 owner 不擅自写业务仓。

## 5. 行为要求

R1：让 S1 正式返回 fitness_regression。保留原 stage、Delivery 身份、planning_root、regression_refs 和 return_route，不规避原失败边界。

R2：同步 runtime 选中的 Delivery output、interface 声明的 public-output-fitness-regression-index-5.0 聚合及 consumers/workflow/fitness-regression-5.0；delivery-1.0 consumer 按当前引用和分发确定兼容修改，不能仅修后者。只处理本次合法阶段组合，不泛化历史 API。

R3：新增去敏最小等价回归，保持 profile/stage/exit/身份关系和原失败条件。用测试仓自己的有效候选及 Task/Delivery 替换业务专有值，不依赖临时现场文件、原会话、secret 或业务 checkout。正式集成状态沿支持 API 建立；自动回归可复用受控 fixture，但必须经过正常身份、候选和 schema 校验。

R4：测试作者可提供受控 owner result 验证确定性执行，该证据不证明独立 AI 语义审核。正式业务现场由原 Architecture owner 新审核。不增加人为伪造、攻击或故意绕过负例，不删除合法失败样本。

R5：canonical、dogfood 和声明平台合同一致；执行定向 reapply/drift 和 sidecar 处理。若确需 clean throwaway，最多一个代表安装，完整矩阵仍由 Release Gate 承担。

R6：兼容增补枚举保持公共 id。已有合法输入、stage、return_route 语义和普通 stale 检查保持；若方案要求破坏 API，先由原 owner 提供明确迁移合同。

## 6. 约束与依赖

Markdown 中 AI 拥有发现、充分性与 route 判断；脚本只验证客观合同。使用官方 marketplace/preset，不修改上游、全局 npm 或 node_modules。现有测试 fixture、正式 wrapper 和安装工具为本次验证入口；没有业务持久化字段变化，因此不需要数据迁移。业务 V5 依赖正式修复的安装来源与业务仓自己的操作授权，不阻塞源码 PR 提交或合并。

## 7. 可观察验收与验证方式

| AC | 要求/场景 | 输入、入口和预期观察 |
| --- | --- | --- |
| V1 | R1/R3/S1 | 有效状态及等价样本执行正式 wrapper；修复前在 stdout schema 边界失败，修复后保留原阶段返回 fitness_regression |
| V2 | R2/S1 | 同一实际 stdout 通过实际 Delivery、当前聚合及当前 consumer；身份/root/refs/route 保持。结构校验与 AI router 行为分开报告 |
| V3 | R6/S2 | 两种 route、受影响 Planning/phase2/final_integration 定向回归通过；普通 stale 检查保持，不跑全阶段笛卡尔积 |
| V4 | R5/S3 | 受影响包 canonical/installed/platform 一致，reapply/drift、权限和 sidecar 检查；不据此宣称完整 Release 矩阵通过 |
| V5 | R4/S4 | 正式修复安装后由原业务 Architecture owner 重新审核同条件，确认实际出口交还实施；没有该证据则明确现场未验证 |

## 8. 实际未决项

没有源码范围的待决选择。V1–V4 待实施验证；V5 是合并后原业务 owner 的后续整体验收。重入条件为正式来源可安装、业务 owner 沿本仓自身流程采用并提供原发现条件的 fresh 语义与出口证据。源码交付不宣称业务 reconcile、ABTest 修复或部署成功。
