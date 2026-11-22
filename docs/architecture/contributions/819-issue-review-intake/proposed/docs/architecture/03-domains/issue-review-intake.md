# Issue 审核、评论与开工复核

Identity：`ARCH-DOM-ISSUE-REVIEW-INTAKE`。状态：integrated_pending_review。原 Architecture owner 在完整实施与真实工程结果后执行 final_integration，写入并读回本完整单元；尚待 TaskCommit 与独立 committed Review。原语义 owner 为 `guru-maintain-architecture-baseline`，精确内容由 Git revision 与本 locator 定位。来源为 [Issue #819](https://github.com/castbox/guru-trellis/issues/819)，固定 before 为 `4f2adef1f7b099f78bb8429e8b8facd66dce3bfc`。

## 职责与权威

本单元定义已有 Issue 从 Sync 进入开工复核、按缺口补审，以及创建和复审评论的职责边界。它不定义 Task 后续生命周期，也不把评论变成开工许可。详细公共字段、schema、命令和逐出口 projection 由 [canonical packages](../../../trellis/skills/guru-team/packages) 与 [workflow](../../../trellis/workflows/guru-team/workflow.md) 拥有。

需求与配对策略见 [局部 Intake 需求](../../requirements/current/local-fix-intake.md)、[Issue 内容需求](../../requirements/current/issue-content.md) 及各自指向的 Design/Test。必要决定见 [ADR-ISSUE-REVIEW-INTAKE](../adr/issue-review-intake.md)。原 architecture baseline、design constitution、change contract 和各语义 owner 保持原职责。本单元不建立独立 ledger、审核身份、评论期限或覆盖认证。

## 原流程与本次整合定义

before 的 Readiness 只在 Discovery、Clarify、Wording 的完整链之后判断开工；本轮 receipts 是该入口的必要输入。它不能直接采用已有 Issue 中仍适用的完整审核材料，局部步骤也不能合法回到 Readiness。Create 的创建终点没有共同的可读审核评论。

本次整合的流程在原 Sync 后按对象薄路由。明确已有 Issue 进入原 `guru-review-change-request` 的 `existing_issue_intake`。该 AI owner 读取完整 live Issue、讨论和评论、必要前置与相关代码，再判断已有材料的覆盖、适用性和真实缺口。它可以直接 ready，也可以选择最早必要的局部补审、必要完整链、基线刷新或 blocked。脚本不能由评论格式或 receipt 数量推断覆盖。

无 Issue、草稿和 `no_issue` 保留原完整方法及各自终点。仅创建在正式内容和评论读回后结束；创建并开工从正式 Issue 重新进入 Sync 与先行 Readiness。Task 创建、规划、实施和交付门禁仍由原 owner 执行。

## 七个原 owner

| Owner | 当前完整责任与直接返回 |
| --- | --- |
| Sync | 读取固定来源或实际同步，提供真实来源与原 transition；刷新后回原 Readiness，不自行判断 Issue 是否充分。 |
| Readiness | 拥有当前覆盖、前置、缺口、ready 和路线判断；消费局部结果后重新判断剩余工作。 |
| Discovery | 完整链保原调查；`issue_readiness_supplement` 仅完成明确事实缺口，返回同次 Readiness。 |
| Clarify | 保来源角色、范围与需求判断；局部需要上下文时沿原事实往返；完成后回 Readiness。独占评论正文规则。 |
| Wording | 保完整标题/正文扫描与保义审核；局部结束回 Readiness，发现需求缺口时不替代 Clarify 判断。 |
| Create Issue | 消费真实已审正文与评论，创建并读回正式内容，再评论并读回；只在全部完成后返回 created。 |
| Create Task | 消费 ready 的最小创建输入，独立审定集成 branch、delivery target 与原 Issue disposition。 |

局部结果经 `issue_review_return` 回同一 Issue、固定来源和 continuation。成功完成一个局部步骤不触发默认剩余完整链。多缺口按本次剩余事实由 Readiness 继续选择。只读复核不写评论；局部覆盖不能表述成完整审核。

## 来源与返回关系

新入口和局部返回完整保留 `base_source={kind,selected_ref,commit}`。read 原样采用真实 `git_object` 来源；实际 sync 从原结果归一化为 `synced_branch`。最小来源不能反拼完整链所需的旧 transition 或 receipts；必要完整链继续消费真实 Sync 结果。

ready 仅投影 `creation.reviewed_base_source`。`creation.selected_base_ref` 是独立的 Task 集成 branch，`delivery_target` 是未来交付目标。当前 Create Task 选择 profile 2.0 与共享 creation 3.0；旧 1.0 资产仅保历史验证。来源 commit 必须是同仓 commit 且等于 acquisition.decision_head；同步来源 branch 与集成 branch 的身份条件由原 normalization 在新建和恢复共同验证。local HEAD 条件仅属于新建 prepare，成功结果恢复不因后来 branch 前进失效。固定对象不重解后来 ref，也不要求 primary main 等于旧 commit 或保持 clean。

普通遗漏、来源失配和过期事实回原 producer 恢复。无关时间、HEAD 或 Agent 变化不自动废除仍适用的内容判断。本单元不增加锁、并发压力、攻击输入或额外 crash 协议。

## 评论生产与恢复

`guru-clarify-requirements/references/issue-review-comment.md` 是唯一评论正文规则。Create 与 Clarify 共用它，评论表达实际对象、实际覆盖、结论及尚未解决的开工条件；没有强制模板、marker、署名或期限准入。Readiness 自行判断完整 live 材料，历史清楚评论可以被采用，定位标记不能证明覆盖。

Create 的顺序为创建 Issue、正式内容读回、评论发布、评论读回，随后 created。原单次 attempt 只定位该操作已经成功的 Issue/comment。中断恢复先确定已成功对象，只补剩余动作，不重复创建，也不把部分完成表述为 created。Clarify 复用原 repo-bound source_actions、POST/PATCH 和 readback；未知结果按原动作恢复。它仅在实际复审且本次写范围明确时发布或更新准确评论。

## 分发、迁移与知识写入

七包、workflow/routing、公共 Interface/schema、graph、manifest、examples 及实际消费者同批适配。`MIGRATION-819.md` 说明固定旧 provider 的已执行操作恢复及新入口，不建立长期 dual-reader。原 Create Task 的固定旧成功结果恢复仍由 `MIGRATION-813.md` 拥有。

canonical 是唯一长期源码；tools owner 通过匹配的完整来源更新受管副本，保 Task/session、用户内容与 peer 指针，并处理 sidecar、mode、drift 和 reapply。源码和 schema 检查不证明已安装 Agent 的实际行为，mock 不证明 live GitHub 动作。

共享知识由原 RDT 和 Architecture maintenance owners 单写。完整拟后定义先隔离，完整实施和真实工程结果后执行 final_integration、读回全部目标，状态仅为 integrated_pending_review。TaskCommit 纳入全部 after；同一次独立 committed Review 判断固定 B..H 的架构与质量，才能建立 reviewed_promoted。此单元不增加提交前独立 Architecture 或 candidate Check。

## 证据边界

配对 Test 记录实际执行、失败、恢复和未验证边界。工程运行、matching 安装、实际 Agent 分流、live GitHub 创建/评论、独立 committed Review、交付和 Task Completion 各有独立证据，不能互相替代。本单元已由原 owner 完成共享整合/readback。配对 Test 记录真实工程、matching 采用及直接 ready 观察。随后，原 Clarify standalone 已在 #819 发布并读回[最小审核评论](https://github.com/castbox/guru-trellis/issues/819#issuecomment-6863818636)，经原上下文刷新返回原 caller，没有进入 Task 路由或创建新 Task。该观察只证明本次评论发布、读回及回程，不证明 Create 真实新建、评论更新、外部未知结果恢复或全部 Agent 分支。验收中曾只读 private runtime 辅助核对旧完整链和字段，因此不声明全程仅依靠 public projection 或 native 隔离。具体执行与辅助核对边界由配对 Test 单写；完整 AC、独立 committed Review、交付及 Task Completion 仍未成立。
