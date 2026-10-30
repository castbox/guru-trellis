# Architecture 发现阶段 fitness 出口合同：整体需求

## 1. 来源与术语

| 来源 | 条款与角色 | 本 Task 用途 |
| --- | --- | --- |
| Direct Source [castbox/guru-trellis#690](https://github.com/castbox/guru-trellis/issues/690) | 当前正文的目标与范围、正常复现、验收标准及完成边界；要求 | V1–V4 为完整验收，V5 为消费方现场边界，非验收项 |
| [D1 规划](deliveries/1ec01507-6702-48cf-ab94-4e4f52bd6c2f/prd.md)及同目录 design.md、implement.md | 已交付切片的历史约定 | 保留 D1 当时的切片范围与 V5 后续责任表述，不据此覆盖当前整体完成边界 |
| [PR #691](https://github.com/castbox/guru-trellis/pull/691) | 源码交付与验证证据 | 定位已合并的 V1–V4 成果及其未验证边界 |

已确认根因是原诊断的源码证据；ABTest 仅为真实触发背景。#663 的归档 PRD 为历史约束，不授予本次验收通过。公共合同以当前 canonical `trellis/skills/guru-team/packages/guru-maintain-architecture-baseline/` 的 interface、input、semantic result、runtime、output 和 consumer 为准。

`implementation_discovery` 是原发现阶段；`fitness_regression` 表示 Architecture owner 判定适用回归；`return_route=implementation|check` 指向既有 `guru-architecture-baseline-check-router` 的原责任 owner。DeliveryKey 和 planning_root 为当前公共身份，不是新恢复协议。

## 2. 背景与问题

业务 #822 的合法发现调用通过输入及 AI result 校验后，在正式 stdout 输出校验报 `schema_mismatch/stdout`。原诊断基线 main@00b1b6f29 的 Delivery fitness 输出及 interface consumer 遗漏该阶段，runtime 原样投影 stage，导致真实发现不能交还实施。现场 schema 反事实结果不是修复后正式 wrapper 或业务原生流程证明。后续源码交付事实见第8节；消费方现场仍未验证。

## 3. 目标与非目标

整体目标是补齐公开合同链，完成 V1–V4 的正式出口、完整承接、定向兼容和安装投影验收。V1–V4 构成本 Issue 和 Task 的完整验收范围。消费方安装采用或现场验收不作为 Completion、Closure 或 Finish 的前置条件；原 Completion 依据当前整体要求和实际交付证据判断完成。Delivery 合并不证明现场 block 已解除，消费方现场仍未验证。

不承担 ABTest Key 接线、业务 reconcile/部署/PR 合并、全流程审计、安全加固或完整多平台 Release 安装矩阵。不得改标 phase2、改报 baseline_current、删除 finding 或绕过 validator。

## 4. 真实调用方、场景与流程

S1：原 Architecture owner 在有效 Task/Delivery 和合法候选上，以 delivery_task_impact_sync、stage=implementation_discovery 判断回归，通过正式 `scripts/invoke.sh --invocation -` 返回原阶段 fitness_regression。相同 stdout 经实际 Delivery output、interface 聚合 output 和当前 consumer 接受，既有 router 按 return_route 交还原 owner。

S2：现有 implementation/check 两种 return_route 均保留。Planning、phase2 和 final_integration 继续沿原合法合同；普通错误和过期身份检查保持。

S3：canonical 经现有 preset apply/reapply 分发到 dogfood 与声明平台，sidecar 逐个处理，drift 检查证明当前受影响包一致。

S4（消费方现场边界，非本 Task 验收场景）：消费方自行沿业务仓流程更新安装与执行。该独立采用不阻塞本 Task 完成；源码 owner 不擅自写业务仓，也不将源码或 fixture 结果当作实际现场恢复。

## 5. 行为要求

R1：让 S1 正式返回 fitness_regression。保留原 stage、Delivery 身份、planning_root、regression_refs 和 return_route，不规避原失败边界。

R2：同步 runtime 选中的 Delivery output、interface 声明的 public-output-fitness-regression-index-5.0 聚合及 consumers/workflow/fitness-regression-5.0；delivery-1.0 consumer 按当前引用和分发确定兼容修改，不能仅修后者。只处理本次合法阶段组合，不泛化历史 API。

R3：新增去敏最小等价回归，保持 profile/stage/exit/身份关系和原失败条件。用测试仓自己的有效候选及 Task/Delivery 替换业务专有值，不依赖临时现场文件、原会话、secret 或业务 checkout。正式集成状态沿支持 API 建立；自动回归可复用受控 fixture，但必须经过正常身份、候选和 schema 校验。

R4：测试作者可提供受控 owner result 验证确定性执行，该证据不证明独立 AI 语义审核，也不证明消费方现场恢复。消费方现场复验不属于本 Issue 或 Task 的完成条件。不增加人为伪造、攻击或故意绕过负例，不删除合法失败样本。

R5：canonical、dogfood 和声明平台合同一致；执行定向 reapply/drift 和 sidecar 处理。若确需 clean throwaway，最多一个代表安装，完整矩阵仍由 Release Gate 承担。

R6：兼容增补枚举保持公共 id。已有合法输入、stage、return_route 语义和普通 stale 检查保持；若方案要求破坏 API，先由原 owner 提供明确迁移合同。

## 6. 约束与依赖

Markdown 中 AI 拥有发现、充分性与 route 判断；脚本只验证客观合同。使用官方 marketplace/preset，不修改上游、全局 npm 或 node_modules。现有测试 fixture、正式 wrapper 和安装工具为本次验证入口；没有业务持久化字段变化，因此不需要数据迁移。V5 仅说明消费方自行采用的边界，不构成本 Task 的验收依赖；业务 reconcile、ABTest 修复和部署成功仍不属于本次成功声明。

## 7. 可观察验收与验证方式

| AC | 要求/场景 | 输入、入口和预期观察 |
| --- | --- | --- |
| V1 | R1/R3/S1 | 有效状态及等价样本执行正式 wrapper；修复前在 stdout schema 边界失败，修复后保留原阶段返回 fitness_regression |
| V2 | R2/S1 | 同一实际 stdout 通过实际 Delivery、当前聚合及当前 consumer；身份/root/refs/route 保持。结构校验与 AI router 行为分开报告 |
| V3 | R6/S2 | 两种 route、受影响 Planning/phase2/final_integration 定向回归通过；普通 stale 检查保持，不跑全阶段笛卡尔积 |
| V4 | R5/S3 | 受影响包 canonical/installed/platform 一致，reapply/drift、权限和 sidecar 检查；不据此宣称完整 Release 矩阵通过 |
| V5（非验收项） | R4/S4 | 不要求消费方安装采用或现场验收；明确消费方现场仍未验证，不宣称现场 block 已解除 |

V1–V4 是完整验收范围。V5 不阻塞 Completion、Closure 或 Finish，也不因本 Task 完成而变为现场已验证。

## 8. 实际未决项

没有必要的待决产品范围选择。D1 已通过 [PR #691](https://github.com/castbox/guru-trellis/pull/691) 合并至 main，合并提交为 `2f70796103406683a2f63adfb6b54d247a7433a5`。该交付覆盖 V1–V4：三个 schema 修正、正式 wrapper 前后对照、六种阶段/回程组合、Architecture contract suite，以及 source/installed、受管 reapply/parity/drift 验证。具体检查与未验证项由原 PR 及 Delivery 结果承载，不重复建立完成账本。

历史 D1 文档和原 Issue 交付评论中将 V5 留作整体验收的表述，记录当时的要求；当前整体完成边界以本 PRD 第3、7节和 live #690 为准。原 Clarify 接受本轮根需求后，由原 Completion 重新判断整体完成，无需新建源码 Delivery。完整 Release 矩阵、官方 upgrade/update 和 formal fork source lock 仍未由 D1 证明。消费方现场仍未验证；业务 reconcile、ABTest 修复和部署成功均不作完成声明。
