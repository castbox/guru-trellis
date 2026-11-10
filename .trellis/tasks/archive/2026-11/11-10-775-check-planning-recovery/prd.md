# Check 规划回退交接与原结果恢复：整体需求

## 1. 来源与术语

| 来源 | 章节与角色 | 本 Task 用途 |
| --- | --- | --- |
| [Issue #775](https://github.com/castbox/guru-trellis/issues/775) | 完整正文；Direct Source、行为要求及验收权威 | 承接 R1、R2、最小验收和非目标；当前无评论 |
| [生产 Check](../../../trellis/skills/guru-team/packages/guru-check-task/runtime/delivery.py) | `_binding`、`planning_stale`；当前事实 | 定位交接与回退后前置缺口 |
| [Author 输入](../../../trellis/skills/guru-team/packages/guru-author-task-plan/schemas/public-delivery-approval-revision-input.schema.json) | `delivery_approval_revision`；当前接口约束 | 验证目标消费者实际接收条件 |
| [现有测试](../../../trellis/skills/guru-team/packages/guru-check-task/tests/test_candidate_check.py) | 生产入口 fixture；当前证据 | 复用已有前置与回退流程 |
| [流程合同](../../spec/workflow/workflow-contract.md) | Public Graph、Consumer Projection、Interaction Budget；项目约束 | 保留原 owner、语义判断和副作用边界 |

`current_scope` 表示候选属于已确认范围，不等于需求变化。`planning_stale` 是 Check 退回规划的出口，不是 Planning 或 Check 通过。Task 承担全部 R1/R2；Delivery 负责选定交付切片。

## 2. 背景与问题

Issue 记录的 Backend #1175 历史案例中，Check 发现 implement.md 的设计章节链接无效。AI 将其判断为 current_scope，并选择 reapprove_plan。Check 已依法将同一 Delivery 回退到 planning，清除了 Planning/Check/Review/readiness；但非空 scope_decisions 被全部投影为 proposal_refs，未携带 Author 必需的 revision_actions。输出通过 producer schema，投影后的 Author 输入却被拒绝。再次调用 Check 又要求已被此次回退清除的 Planning 结果。

当前 main 基线 `313d80215f65777fc70893a90c6d8dce8005d6dd` 的生产代码、公开输出和测试仍包含该差额。已有无 scope_decisions 的测试验证了 Author schema；非空 refs 测试只验证 producer 和 router，未验证最终 Author 接收。此 Task 修复框架交接，不重演业务仓历史现场。

## 3. 目标与非目标

整体目标是闭合原 Check → 原 Planning owner 的正常回退交接，并使已发生的同一次回退可由原 Check 恢复或合法纠正。两处属于同一独立交付单元。

不改变阶段顺序、独立审核职责、语义门禁或业务仓功能。不通过替代 Task/Delivery、手动交付、补造 pass、修改旧 artifact/digest 或强改 phase 绕过缺陷。不接管合同发布、PR 合并或业务 Task 完成；本执行段发布 PR 后等待协调器处置。#772、#773、#710 的独立范围及完整 native 矩阵不进入本 Task。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 行为与可观察结果 |
| --- | --- | --- |
| S1 范围内规划修复 | 原 Check 对合法当前候选作真实判断，保留 current_scope 决策并选择 reapprove_plan | 同一 Delivery 回到 planning；公开输出经正式薄投影后进入原 Author 输入，保留具体修复动作 |
| S2 真实范围变化 | 原 Check 识别需求权威或范围发生真实变化 | 交回原 Clarify；不为通过而清空真实 scope_decisions 或伪造动作 |
| S3 已回退结果恢复 | 原 Check 已执行 planning_stale，Planning pass 已被清除，调用方丢失输出或原交接需要语义纠正 | 原 owner 依据同一 Task/Delivery、原结果及实际状态恢复；需要纠正时先完成真实判断，再经声明入口产生有效交接；不重复回退或生成 pass |
| S4 恢复条件变化 | 当前身份、内容或范围已真实变化 | 返回受影响原 owner 重新判断；不覆盖当前候选或业务改动，不将任意 planning 状态视为合法恢复 |

## 5. 行为要求

### R1 Check 到原 Planning owner 的交接闭合

AI 负责区分范围内修复与真实需求变化。current_scope 记录不能仅因存在就成为新的需求选择。每个受支持的 planning_stale 输出必须有唯一、可执行的 consumer。reapprove_plan 的范围内修复携带 Author 实际需要的具体动作；真实需求变化交原 Clarify。

公开输出、声明薄投影和目标输入必须一致。验证须使用目标消费者真实输入合同，不能只验证 producer 自己的 schema。不预设每次回退新增跨 Skill schema 加载、查询或运行门禁；由原规划 owner 按具体修复和现有合同选择。AI 继续承担分类、动作及路线判断，脚本只记录或校验确定性事实。复用原 owner、typed exits 和投影机制；公共合同变化必须有明确兼容说明。

### R2 已发生规划回退的原 owner 恢复

原 Check 能依据同一 Task/Delivery、原结果及实际状态恢复交接。如原结果需要纠正，先作本次真实语义判断，再通过声明入口生成有效新交接。恢复不能再次要求此次回退依法清除的 Planning pass，不能重复执行回退，不能建立替代身份、强改 phase、补造旧 pass 或手改旧 artifact/digest。

恢复不得自动覆盖当前候选或业务改动。真实身份、内容或范围变化必须返回受影响原 owner。恢复仅证明规划交接可继续，不代表重新批准规划、Check passed 或可发布。优先复用现有结果与状态，不新建通用事务、跨阶段账本、授权记录或全链 digest。须明确承接修复前已回退现场的最小兼容路径，不能要求现场先恢复不存在的 Planning pass。

## 6. 约束与依赖

- 使用当前专属 worktree 和 `codex/775-check-planning-recovery`；交付和完成验证均以 main 为目标。保留其他执行者的改动、资源与证据。
- 流程判断留在 Markdown/AI owner；Python/shell 仅执行、记录或验证确定性事实。只覆盖诚实协作的正常流程、普通遗漏与 stale/mismatch。
- 受影响 canonical/dogfood/consumer 投影必须经原安装或升级 owner 同步，保留 Task/session，并检查 drift 和 sidecar。
- 不涉及业务数据或数据库迁移。存在公开 DTO/入口兼容变化，其具体机制和迁移边界由 Delivery 规划展开。
- 当前无外部前置节点；已有 Check fixture、Author 输入合同与原回退操作可复用。

## 7. 可观察验收与验证方式

| 验收 | 对应要求与入口 | 预期结果与边界 |
| --- | --- | --- |
| AC1 真实 Author 交接 | R1/S1；复用 Check fixture，以正常语义输入从实际 Check 入口产生 current_scope + reapprove_plan | 实际 planning_stale 输出按正式薄投影构造 Author 输入，通过其真实 schema，且保留具体修复动作；无需执行 Author 全部写作 |
| AC2 原 owner 恢复 | R2/S3；复用同组 fixture，由公开流程实际产生回退，在 Planning 已清除后调用声明恢复/纠正入口 | 同一 Task/Delivery 可继续规划交接；无重复回退，无 Planning/Check 通过结果；兼容旧现场复用已有结果和因果证据，只验证入口或转换实际改变部分 |
| AC3 受影响回归与分发 | R1/R2/S2/S4；执行改动命中的 package、consumer 投影、受管副本与 drift 定向验证 | 真实范围变化保留 Clarify 路线；受影响无 scope 决策和成功 Check 回归保持；matching 副本一致，无未处理 sidecar |

AC1/AC2 共享前置和证据，不各自从 Task 创建重跑。不新增重复场景，不要求业务仓验收、完整 Intake/Author/native Agent 全链或多平台/Release 矩阵。验收状态须由实际执行证据给出，本需求文档不预填通过。

## 8. 实际未决项

需求和验收边界已明确，无待用户选择的产品范围问题。具体 DTO 兼容、恢复入口和最小因果绑定由原 Author/Architecture 在 Delivery 规划中收敛。整体 Completion 必须在完整 accepted scope 交付后由原 owner 判断；PR 发布不是 Task 完成。
