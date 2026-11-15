# Issue 审核、评论与开工复核

Identity：`ARCH-DOM-ISSUE-REVIEW-INTAKE`。状态：`integrated_pending_review`。原 Architecture owner 在 #850 的 final_integration 整合本完整定义并逐份读回；尚待 TaskCommit 与独立 committed Review。原语义 owner 为 `guru-maintain-architecture-baseline`。本次窄替代依据为 [ADR-850-DEFAULT-WORDING-RETIREMENT](../adr/850-default-wording-retirement.md)，固定前驱为 Git `a72981db56d2070d8140b468cab3a97ae82effd3`。#819 的来源仍为 [Issue #819](https://github.com/castbox/guru-trellis/issues/819)，其历史 before 为 `4f2adef1f7b099f78bb8429e8b8facd66dce3bfc`。

## 职责与权威

本单元定义已有 Issue 从 Sync 进入开工复核、按缺口补审，以及创建和复审评论的职责边界。它不定义 Task 后续生命周期，也不把评论变成开工许可。详细公共字段、schema、命令和逐出口 projection 由 [canonical packages](../../../trellis/skills/guru-team/packages) 与 [workflow](../../../trellis/workflows/guru-team/workflow.md) 拥有。

需求与配对策略见 [局部 Intake 需求](../../requirements/current/local-fix-intake.md)、[Issue 内容需求](../../requirements/current/issue-content.md) 及各自指向的 Design/Test。必要决定见 [ADR-ISSUE-REVIEW-INTAKE](../adr/issue-review-intake.md)。原 architecture baseline、design constitution、change contract 和各语义 owner 保持原职责。本单元不建立独立 ledger、审核身份、评论期限或覆盖认证。

## 原流程与本次整合定义

before 的 Readiness 只在 Discovery、Clarify、Wording 的完整链之后判断开工；本轮 receipts 是该入口的必要输入。它不能直接采用已有 Issue 中仍适用的完整审核材料，局部步骤也不能合法回到 Readiness。Create 的创建终点没有共同的可读审核评论。

本次整合的流程在原 Sync 后按对象薄路由。明确已有 Issue 进入原 `guru-review-change-request` 的 `existing_issue_intake`。该 AI owner 读取完整 live Issue、讨论和评论、必要前置与相关代码，再判断已有材料的覆盖、适用性和真实缺口。它可以直接 ready，也可以选择最早必要的局部补审、必要完整链、基线刷新或 blocked。脚本不能由评论格式或 receipt 数量推断覆盖。

无 Issue、草稿和 `no_issue` 保留Discovery→Clarify→Readiness完整方法及各自终点；独立Wording及专属证明依赖退出，原owner仍执行完整语义判断。仅创建在正式内容和评论读回后结束；创建并开工从正式 Issue 重新进入 Sync 与先行 Readiness。Task 创建、规划、实施和交付门禁仍由原 owner 执行。

## 六个原 owner

| Owner | 当前完整责任与直接返回 |
| --- | --- |
| Sync | 读取固定来源或实际同步，提供真实来源与原 transition；刷新后回原 Readiness，不自行判断 Issue 是否充分。 |
| Readiness | 拥有当前覆盖、前置、缺口、ready 和路线判断；消费局部结果后重新判断剩余工作。 |
| Discovery | 完整链保原调查；`issue_readiness_supplement` 仅完成明确事实缺口，返回同次 Readiness。 |
| Clarify | 保来源角色、范围与需求判断，承接具体内容/措辞缺口及Issue/draft有界只读审核；局部需要事实时沿原context往返，完成后回同次Readiness。独占评论正文规则；不取得Readiness开工判断。 |
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

实际受影响packages、workflow/routing、公共 Interface/schema、graph、manifest、examples 及实际消费者同批适配。`MIGRATION-819.md`保留原入口历史；`MIGRATION-850.md`拥有本次Wording退出的新版本及在途切换。固定旧provider已开始的操作先恢复同一对象再匹配更新，不建立长期dual-reader。原 Create Task 的固定旧成功结果恢复仍由 `MIGRATION-813.md` 拥有。

canonical 是唯一长期源码；tools owner 通过匹配的完整来源更新受管副本，保 Task/session、用户内容与 peer 指针，并处理 sidecar、mode、drift 和 reapply。源码和 schema 检查不证明已安装 Agent 的实际行为，mock 不证明 live GitHub 动作。

共享知识由原 RDT 和 Architecture maintenance owners 单写。完整拟后定义先隔离，完整实施和真实工程结果后执行 final_integration、读回全部目标，状态仅为 integrated_pending_review。TaskCommit 纳入全部 after；同一次独立 committed Review 判断固定 B..H 的架构与质量，才能建立 reviewed_promoted。此单元不增加提交前独立 Architecture 或 candidate Check。

## 新路径的内容身份、显式审核与证据边界

Clarify的source title/body token与语义identity分别绑定；Readiness核实际对象/源内容并执行自己的十维与live reread，不把token当授权或semantic pass。局部focus只约束实际缺口，context返回保同Issue/source/continuation/focus；不补造full-chain receipts。完整Intake、Issue创建的前序复核与最小评论继续由原owner承担。

显式Issue/draft措辞审核在原Clarify有界只读profile结束于user-response，不要求Task/Delivery绑定，不修改对象，也不产生ready。显式文件审核由原review-change的explicit_files/wording_only承接，snapshot精确选定Markdown的完整当前bytes，包含未变更文件。该profile只审核表述与含义保留，不继承range profiles的实现完整度、测试及三视角前置；原range方法与wire保持。public input aggregate2.0同批加入该1.0分支。真正修订回原内容writer；等义只刷新直接依赖，需求、机制、Architecture或验收变化回原受影响owner。

配对Test分别记录生产wrapper、真实Agent、matching采用和外部GitHub动作；源码、schema、mock、评论、贡献或历史结果不能相互替代。原历史观察仍可从固定before与原Test读取，本次整合不重写其结果。shared-current晋升仍须原final_integration/readback、TaskCommit及一次独立committed Review。

## #819 历史证据边界

以下保留固定前驱 `a72981db56d2070d8140b468cab3a97ae82effd3` 中 #819 的原观察截止，不作为 #850 的验证结果。

配对 Test 记录实际执行、失败、恢复和未验证边界。工程运行、matching 安装、实际 Agent 分流、live GitHub 创建/评论、独立 committed Review、交付和 Task Completion 各有独立证据，不能互相替代。本单元已由原 owner 完成共享整合/readback。配对 Test 记录真实工程、matching 采用及直接 ready 观察。随后，原 Clarify standalone 已在 #819 发布并读回[最小审核评论](https://github.com/castbox/guru-trellis/issues/819#issuecomment-6863818636)，经原上下文刷新返回原 caller，没有进入 Task 路由或创建新 Task。该观察只证明本次评论发布、读回及回程，不证明 Create 真实新建、评论更新、外部未知结果恢复或全部 Agent 分支。验收中曾只读 private runtime 辅助核对旧完整链和字段，因此不声明全程仅依靠 public projection 或 native 隔离。具体执行与辅助核对边界由配对 Test 单写；完整 AC、独立 committed Review、交付及 Task Completion 仍未成立。

## #850 整合与当前验证边界

本定义承接已批准的实际方案及当前实现。原 owners 已执行本次完整定义整合与 readback，状态仅为 `integrated_pending_review`。配对 [Test](../../test/current/local-fix-intake.md) 及 [#850 Test](../../requirements-design-test-contributions/850-wording-retirement/test.md) 分开记录实际工程汇总、可读的受管采用原文、真实 Agent 观察与未验证项。源码工具结果不能替代语义或整个调用链证明。

本轮工具采用为 `local_candidate`，`formal_fork_source_lock` 仍为 `unverified`。真实有界 draft/file 审核、缺源 blocked、live Readiness 以及隔离 Planning 返工后 approved 各只证明其实际观察；它们不是正式 #850 Planning 的替代结果。#819 的 `wording_only` 真实往返已在受控本地三来源 fixture 中实际完成：Readiness 补审、单次 PATCH/GET、Clarify supplemented、同次 Readiness ready。首错保留，不能称首次正确；该观察不证明 live GitHub 写入、完整链或全部正常分支。未将全 I07、全部验收、独立 committed Review、远端交付或 Release 写成通过。
