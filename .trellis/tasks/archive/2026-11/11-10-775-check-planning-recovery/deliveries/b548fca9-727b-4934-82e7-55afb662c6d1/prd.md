# D1：Check 规划回退交接与恢复需求

## 1. 整体来源与术语

本批使用 [Task 整体 PRD](../../prd.md) 的公共 accepted_scope；其 revision 由 Task 公共记录给出。选定 DeliveryKey 为 Task `775-check-planning-recovery`、generation `0`、Delivery `b548fca9-727b-4934-82e7-55afb662c6d1`。scope_ref 选择 R1、R2、AC1、AC2、AC3；planning_root 为本目录。

| 来源 | 章节、角色与用途 |
| --- | --- |
| [Issue #775](https://github.com/castbox/guru-trellis/issues/775) | 完整正文；要求与兼容约束，定义本批正常场景及两项最小验收 |
| [整体 PRD](../../prd.md) | 第4–7节；完整场景、行为和验证责任 |
| [Check runtime](../../../../../trellis/skills/guru-team/packages/guru-check-task/runtime/delivery.py) | `_binding`、`invoke`；现状证据，定位先要求 Planning、再清除 Planning 的回退过程 |
| [Author 输入](../../../../../trellis/skills/guru-team/packages/guru-author-task-plan/schemas/public-delivery-approval-revision-input.schema.json) | 必需 revision_actions；现有消费合同 |

current_scope 是范围归属，不是需求变更。恢复指原已执行回退的交接恢复，不代表重新通过任何阶段。

## 2. 整体与本批目标、非目标

本批全量覆盖整体 R1/R2：使范围内 reapprove_plan 的实际输出能进入原 Author，并使 Planning 已清除的同一次回退可由原 Check 恢复或经真实判断纠正。两项共享同一因果链，不拆为独立身份。

保留整体非目标：不修改业务仓功能，不重演 Backend #1175，不接管业务 Task 完成，不扩展其他 Issue、完整 native 链或多平台/Release 矩阵。不通过替代身份、补造 pass、强改 phase 或改旧 artifact/digest 实现恢复。本执行段发布 PR 后等待协调器处理合并。

## 3. 本批起点、前序结果、依赖与剩余责任

这是首次 D1，尚无前序 Delivery。起点 HEAD／固定 development baseline B 为 `313d80215f65777fc70893a90c6d8dce8005d6dd`；PR 目标为 main。Task 与本 Delivery 已合法创建，当前 phase 为 planning，尚无 Planning/Check/Review/readiness 通过结果。

已有生产 Check fixture、phase2 recorder/checker、原 rework 操作和 Author schema可复用。当前旧实现把所有 scope_decisions 投影为 proposal_refs，非空时省略 actions；已回退重试仍要求 Planning 结果。无外部前置节点。D1 承担全部已选行为和验证，不预留另一批修复这些缺口；Task Completion、Closure、归档仍由后续原 owners 判断，发布 PR 不代表完成。

## 4. 本批调用方、场景与流程

- S1：原 Check 对合法 checking 候选发现范围内规划修复，真实记录 current_scope + reapprove_plan。它返回携带具体动作的 planning_stale，依法回退同一 Delivery；正式薄投影进入原 Author。
- S2：原 Check 发现真实需求权威或范围变化，保留真实 scope_decisions 并交原 Clarify；不能清空决策或制造动作以进入 Author。
- S3：原 Check 已实际完成上述回退，Planning、Check、full_review、readiness 结果已清除。原 owner 读取原结果、原调用身份和当前 Task/Delivery；一致时恢复交接，需要纠正时先完成当前语义判断再生成有效交接。不得再次 rework。
- S4：恢复期间真实身份、候选内容或范围发生变化，返回受影响原 owner；保留当前业务改动，不把任意 planning 状态当成同次回退。

## 5. 完整行为、条件与约束

R1：AI 区分 current_scope 与真实需求变化，并负责具体修订动作和路线。范围内 reapprove_plan 输出必须能通过正式薄投影满足 Author 的实际输入；每个受支持 planning_stale 分支都有唯一可执行 consumer。真实范围变化仍交原 Clarify。公开合同变化写明成套采用及旧结果处理；不预设运行时每次跨包加载 schema 或额外门禁。

R2：同一次已发生规划回退的原 Check 恢复不再依赖已依法清除的 Planning pass。恢复或合法纠正复用原结果和实际状态；不创建替代 Task/Delivery，不重复回退、不生成 Planning/Check pass，不改写旧 artifact/digest。当前身份、内容、范围发生真实变化时返回受影响原 owner。恢复不能覆盖候选或业务改动，不能成为任意 planning 状态放行器。修复前同类现场有最小明确兼容路径。

机制约束：复用原 owner、typed exits、投影及已有 recorder 结果，不新建通用事务、跨阶段账本、授权记录或全链 digest。普通文件用于原状态或结果存储，不能把 OS/process/descriptor 当业务 authority。具体方案及来源约束处置由本批 design 第3节唯一承载。受管投影经原工具升级 owner 同步，保留 Task/session。

## 6. 本批验收、验证方式与未决项

| AC | 条件、入口与输入 | 独立可观察结果 |
| --- | --- | --- |
| AC1 | 复用同组 fixture；实际 Check 入口接收正常 current_scope + reapprove_plan 语义结果 | 实际 planning_stale 输出保留具体动作，经正式薄投影通过真实 Author 输入 schema；不要求 Author 全部写作 |
| AC2 | 原公开流程实际产生 planning_stale 回退，Planning 已清除；调用原声明恢复／纠正入口 | 同一 Task/Delivery 可继续交接；不再次回退，不生成通过结果；兼容旧现场只覆盖新入口／转换实际改变部分 |
| AC3 | 执行命中代码、输出／consumer schema、workflow投影、canonical/dogfood及drift定向检查 | 受影响无决策、真实范围变化及成功 Check 回归保持；matching副本一致，sidecar经原owner处理 |

AC1/AC2 共享前置与已有证据，不重复 Task 创建。测试必须触达真实生产分支并以消费者合同和实际状态判断，不能只验证 producer 自身。当前未执行实现验收，不预填通过。无待用户决定的需求问题；恢复边界和兼容技术细节由 Author／Architecture 收敛。

## 7. Canonical 引用与本轮差额

| Authority | 本批用途与差额 |
| --- | --- |
| [分发架构](../../../../../docs/architecture/04-integrations/distribution.md) 的“公开执行资料与原生产能力” | 现有 no-scope Author 交接扩大为所有范围内合法回退，并补原 owner 恢复边界；最终整合由 Architecture owner承接 |
| [当前生命周期 requirement](../../../../../docs/requirements/current/task-delivery-lifecycle.md) 的 R713 | 保留原 owner／最小 handoff，补 #775 的范围内非空决策与回退恢复要求 |
| [当前生命周期 design](../../../../../docs/design/current/task-delivery-lifecycle.md) 的 D713 | producer／router／真实 consumer 及恢复入口的具体差额由本批设计展开 |
| [当前生命周期 test](../../../../../docs/test/current/task-delivery-lifecycle.md) 的 T713-03 | 复用公开执行验收边界，补 AC1/AC2；不重新继承已取消的 native矩阵 |
| [验证规范](../../../../spec/workflow/quality-guidelines.md) 的 Test And Validation Value、Validation Scope Ownership | 复用足够层级的真实入口fixture和受影响回归，不做声明自证或完整Release矩阵 |

本阶段只完成本批需求与候选输入；共享 RDT／Architecture 的正文与晋升由原 owners 在其边界维护。
