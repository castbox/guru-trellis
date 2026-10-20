# #635 跨环境可接续的任务生命周期整体需求

## 1. 来源与术语

唯一 Direct Source 为 [castbox/guru-trellis Issue #635](https://github.com/castbox/guru-trellis/issues/635) 的完整正文。2026-10-20 fresh 回读时，Issue 为 Open、没有评论，正文更新时间为 `2026-10-19T09:43:23Z`。正文 R1–R5、V1–V8、正常前提、方案约束、非目标和整体完成条件全部有效。本 Task 不编辑该 Issue。

| 来源 | 章节与角色 | 本 Task 用途 |
| --- | --- | --- |
| live #635 | 全文为要求；其中状态归属、共享 Finish 边界、原 owner、公共模型与迁移边界为规范性约束 | 定义整体范围与验收；具体来源设计处置由选定 Delivery 的 design 唯一维护 |
| [现行生命周期要求](../../../docs/requirements/current/task-delivery-lifecycle.md)与[设计](../../../docs/design/current/task-delivery-lifecycle.md) | 已有可复用要求和设计 | 保留 Task/Delivery 分工、固定候选、真实 Check、独立完整 Review、readiness、expected-head 与独立终态 owners |
| #454、#557、#577 的已归档规划及现行 canonical packages | 历史来源与当前实现证据 | 复用身份/绑定恢复、已合并 Delivery 恢复、人工历史归档维护；不重开其全部范围或复用旧 gate pass |
| #636、#637、#638 的 live 合并事实与当前 main | 前置交付事实 | 保留早期 Draft、候选适用性、共享知识晋升的原子能力；不重新实施前三项 |
| #133 业务案例及其 PR 引用 | 问题证据与正式旧格式兼容边界 | 仅用于规划固定去敏同构样本；不授权业务仓数据恢复、安装或修改 |

TaskId 在整个历史中保持不变。`generation` 区分生命周期 incarnation。Delivery 是同一 Task 内的真实交付切片。共享事实指可移植 Task/Delivery 记录、可获取 Git 历史及 live GitHub 对象。本机责任指选定 Git common-dir 内的 session、checkout、branch binding、资源 ownership 和原操作私有恢复输入。MERGED Delivery、Task Completion、Closure、Finish、Cleanup 是不同事实。

## 2. 背景与问题

部分原 consumer 将本机事务或资源回执作为共享任务终态的前提。这些记录不随 clone/pull 转移，导致同一 Git 历史在另一环境被解释为 Finish 未完成。搬运 runtime 或补造 seal 不能消除这项依赖。

本轮开发基线为 `main@7a7b60743499653ffeb81f6b31e627a02c33f579`。fresh 核验 #636、#637、#638 均已关闭；#638 的 PR #646 与归档 PR #647 均 MERGED，后者合并提交即当前基线。主项目本地 main 未同步且必须保留原位；本 Task 在独立 clone 的 linked worktree 推进。

在正常独立 clone 中，没有复制原 `.git` 或 private runtime。对已合并 #638 正式归档执行原 Reactivate 的只读 `archived_identity` 核验，返回 `finish_result_unsealed / manual_finish_result`。当前 `verify_finish_seal` 在缺少本机资源账本时要求本机 manual Finish/Cleanup 记录。这是共享终态准入的当前复现，不是原生 Reactivate 或 V1 通过证据。

未发布代码、不可重新推导的必要事务输入和资源 ownership 仍有直接 consumer。不能把所有 runtime 当缓存，也不能整体提交本机运行目录。其余生命周期 owner 是否存在同类依赖，须逐项核对代码、真实 caller 和测试，不能由目录名称推断。

## 3. 目标与非目标

整体目标是交付“跨环境可接续的生命周期基础”。原 Agent 不再主导或原机不可用后，替代 Agent 在独立 clone/checkout 中凭可获取共享事实继续同一 Task/Delivery及下一实际 owner，无需原机停止回执。保留原 owner 合法并行子 Agent 的实现、检查和审核职责；两个独立环境同时主导同一生命周期不受支持。

范围覆盖 Create/Identity/Bind、Planning/Check/Review、Publish/Merge、Completion/Closure/Finish/Cleanup/Reactivate 全链状态归属、活动 ref 接续、既成副作用恢复、两条再次完成路径、资源隔离、正常双 Task 并行、指定正式旧归档兼容，以及 matching 分发迁移。只加 Reactivate fallback 不能完成本 Task。

不实现 scheduler、分配服务、自动批准/合并策略、暖池、控制中心、锁/租约或第二生命周期 authority。不恢复 developer identity、workspace journal/mappings，不迁移 dirty 未发布工作，不要求发现其他 clone 的未发布 incarnation。不增加攻击/伪造、TOCTOU、压力、fault injection 或非常规 crash-consistency 矩阵。不修改 Backend 或其他业务现场，不跨仓实现 CLI/Core，不执行完整 Release 矩阵、tag、Release 或发布 override。

## 4. 真实调用方、场景与流程

| 场景 | 调用方、前置与触发 | 必须处理的行为及可观察结果 |
| --- | --- | --- |
| S1 正式归档跨 clone 继续 | A 经正式 owners 完成归档并合入目标；B 无 A 私有状态，选择同 repository/Task | 核验精确共享 Finish 及可获取后继；没有后继才公共 Reactivate，TaskId 不变且 generation 只增加一次；已有后继则继续原后继 |
| S2 新业务工作再次完成 | B 在 S1 后有真实新切片 | 经新 Delivery、真实质量门禁、交付，再整体 Completion→Closure→Finish；不能依赖 A 的 seal/退出/Cleanup |
| S3 仅补验证再次完成 | B 在 S1 后仅需证据更新 | 由 TaskKey 的 evidence-refresh/Completion owner 接续，再 Closure→Finish；不创建空 Delivery，不继承旧 gate |
| S4 未入默认分支的活动接续 | 活动 Task/Delivery/必要代码已提交到明确可获取 ref/commit | 原 Identity/Establish/Bind/continuation 恢复同一身份与实际 Delivery；只刷新缺失或依赖变化命中的工作，保留仍适用工程结果和历史 |
| S5 远端副作用已发生 | 私有 Publish/Merge/Closure 事务或回执丢失，远端对象及必要输入可获取 | 原 owner 核对精确归属；Open Draft/metadata/Ready 接续剩余动作，MERGED 与 exact-source disposition 只恢复已发生子动作；不重复创建、合并或关闭 |
| S6 资源残留与双 Task | A 的共享 Finish 已成立但本机资源待清理；B 使用不同合法资源，另有独立 Task | 本机责任不跨 common-dir 认领；旧 generation/旧 expected head 不删除新资源或推进后的 remote ref；一个 Task 的缺状态不阻塞另一个 |
| S7 旧归档分类 | 选定受支持正式旧归档、人工历史归档或未完成 closeout | 正式旧归档经公共转换/接续保留同一 Task 并交下一 owner；人工历史沿 #577；未完成 closeout 回原事务，不补造终态 |
| S8 真正缺失 | ref/commit不可获取、必要输入或未发布代码仅在原机、身份或归属不唯一 | 返回具体缺口、受影响步骤与原 owner；保留原环境及无关状态，不伪造成功或自动 stash/reset/清理 |

## 5. 行为要求

### R1 状态归属与最小共享事实

对全链准入/接续状态逐项给出 producer、直接 consumer、共享或本机职责、生命周期、缺失入口和阻塞范围。在现有 Architecture/生命周期 SSOT 落实四类处置：共享事实可恢复、必须重审、仅本机资源责任、实际输入缺失。代码与测试必须证明归属，不能只列目录或把整体范围内的阻塞留作后续而关闭。

Task identity、accepted scope、Delivery/Completion/Closure 历史及已发布结果从可移植公共记录和 live Git/GitHub 解释。session、checkout 路径、binding 和 ownership 由当前环境的原 owner 恢复或重建。owner-private checkpoint 仅服务当前执行及同操作恢复，不能成为跨机判断既成共享事实的唯一 authority。

仅在证明现有记录不足后，才补充跨机直接 consumer 无法重新推导的最小结果。复用公共 Task/Delivery 模型或既有任务级位置并提供迁移合同；不建立审计数据库、全局恢复台账或第二状态机。

### R2 共享 Finish 与 Reactivate

共享 Finish 独立核验 TaskId/generation/source/accepted scope、该版本要求的 Completion/Closure 关系、精确 bookkeeping PR/归档提交已进入所选目标分支、该归档结果移除 active 记录，以及 archive/finish-summary 一致性。`completed`、目录存在、Issue Closed 或 PR Merged 单独均不足以证明资格。

目标前进或后续 Reactivate 后，以准确归档提交和历史验证终态。不要求当前 HEAD 等于旧 merge SHA，不因当前树后来出现 active 记录而否定历史 Finish。不要求将 merge SHA 写回自身归档提交，也不递归创建额外 Finish PR。

共享终态成立后，原机 seal、binding 退出或 Cleanup 未完成只保留原机后续责任；不能否定共享 Finish或阻止 B 使用不同合法资源。B 核对 repository、TaskId/generation、source/scope、归档提交和可获取后继。已有新 incarnation 就继续它；没有后继才由公共操作严格递增 generation，保留 TaskId/历史，按实际工作进入规划、证据更新或 Delivery owner。不得要求原机 Finish/Cleanup/task-resources/session/checkpoint，不创建替代 Task、空 Delivery或继承旧 pass。

未入目标分支的归档不能报告正式完成。可唯一定位的未完成 closeout 回原事务；不能唯一恢复时报告具体缺口。

### R3 活动接续及既成副作用

接续前提是必要代码和 Task 记录已提交且可获取。明确 repository、TaskId/generation、承载记录/代码的 source ref 与 commit，并验证 Task/Delivery/提交关系。活动记录不必先合入默认分支，不按 branch、Issue title 或当前目录猜 identity。唯一可验证 source 自动承接；合法候选有歧义时只问实际缺失的选择，不索取原 Agent 隐藏目录或重复 routine 选择。

原 owner 亲自判断语义和工程结果适用性。无法证明时回原 producer 重审；阶段、文件或旧 prose 不证明 pass。按 #464/#578 的现行职责仅补缺失或依赖变化命中的检查。换机/checkpoint 丢失本身不重开 Intake/Planning/Delivery、不重跑全链，也不继承 pass/freshness token。

原 Publish/Merge/Closure 核对 repo、Task/Delivery/generation、原输入/远端对象及 commit 与 Open PR、MERGED Delivery PR、source Issue disposition 的精确关系。Draft 或 metadata/Ready 未完成时，原 Publish 完成必要审查和剩余动作；不重建 PR、不直接宣告 Ready。Ready 已完成仍须重判当前 readiness；MERGED 不代表 Task Completion，Closed、标题或查询成功不证明 Closure/归属。

只恢复已完成子动作，不重复 PR create、merge 或 disposition，不造新 Delivery/gate。输入/结果不符或关联不唯一时回原 owner 并说明缺口。仅原机存在的 dirty 未发布修改或必要输入不满足无损迁移前提；准确报告影响并保留原环境。

### R4 资源、generation 与正常并行

local branch/worktree/ignored runtime 的责任限定在对应 Git common-dir；同名 local branch 不跨 common-dir 相互认领。remote branch 是 repository identity + 完整 remote ref 标识的共享资源，不能当机器私有文件。

残留资源由原资源 owner 管理。ownership 缺失沿既有保守处置，不反推 Guru ownership、不补造 Cleanup。旧资源待清理不能撤销共享 Finish；B 接续不授予清理 A 本机资源的权限。确实复用同一有未完成责任的资源时保留原冲突检查。

旧 generation 回执不能操作新 generation 资源。旧 Cleanup 对已推进的共享 remote ref 继续核 ownership、精确 ref 与 expected head；不匹配时保留新提交、交回原 owner，不删除或退回新 ref。不同 Task 的独立 branch/worktree，其 checkpoint、绑定恢复和 Cleanup 不得互为准入条件；不建立仓库级单队列或全局 current-task authority。

### R5 指定正式旧归档与两仓职责

最低兼容集包括当前公共 Task schema 2，以及 #133 同构正式旧归档：原安装 Guru `0.7.0-guru.3`、合法 id、顶层 lifecycle_generation、结构化 source、completed 状态、finish-summary schema 2，且精确归档 PR 已合入目标分支。旧格式没有当前 Completion/Closure 数组，不能要求补造历史结果。

Planning 必须使用原安装 source/固定归档样本，说明受支持格式边界、旧终态证据、公共转换/接续及下一 owner。版本号不证明合法性。不扩任意旧格式；复用 #577，但正式归档不能自动改为人工历史归档。保留 TaskId、来源、规划和交付历史，不批量改档或补造 Completion/Closure/Finish/Cleanup/seal。找回原机隐藏 receipt 不是最终方案。

CLI/Core 拥有公共 Task/Delivery/session 模型；Guru 拥有 Markdown 语义及原 package 的确定性适配。确需上游能力时，明确 owner、API、prerequisite 与配对边界，并暂停依赖它的真实写入；独立必要工作继续。仅登记依赖或手工绕行不算交付。本 Task 不授权跨仓实现或 Guru 复制公共模型。

## 6. 约束与依赖

1. 原全局 workflow 只编排 stable skills 和唯一 typed consumers；step-local skill 独占内部语义。脚本只 executor/validator/最小 recorder，不能代替 scope、Review、readiness 或 Completion 判断。
2. 保留 Finish 先投影归档、合并 bookkeeping 并验证目标，再封存本机资源的顺序；保留 Cleanup 的 repository/ref/expected-head 语义。修依赖倒置不能直接删除合法性校验。
3. 保留 #636 Draft 及同 PR 恢复、#637 后继候选适用性、#638 晋升先于最终 Check。公共结果、工程执行事实和当前语义判断分别处理；真实 Check、首次完整独立 Branch Review、readiness、expected-head 均不可削弱。
4. 公共 skill/exit/schema/command 的变化提供明确版本或兼容迁移。canonical/workflow/声明平台/dogfood/完整 preset 成套同步。reapply/update 保留用户修改，逐项处理 sidecar；不改全局 CLI、上游源码或 node_modules。
5. 验证范围为证明本 accepted scope 的最小可靠集合。至少一个独立 common-dir clone 原生端到端样本；安装验证最多一个代表性样本。#630/Release owner 的完整矩阵不是本 Task 门禁，也不能声称已验证。
6. 本轮基线 clone 的普通 preset apply 曾在写前被旧归档迁移前置阻塞；随后使用仓库已有 source bootstrap 恢复 managed Python，并通过正式 Sync 和只读 dogfood drift。该结果不证明完整 apply/reapply 成功。实施验证必须采用匹配受支持原入口，保留该真实边界，不迁移无关归档来制造安装成功。
7. 任何 Git/GitHub 副作用保持当前对话的精确边界；授权不写入 tracked、runtime、checkpoint 或 archive。本整体 PRD 不授予 commit/push/PR/merge/closure/cleanup 或业务写入权限。

## 7. 可观察验收与验证方式

下列为待实施的验收，不预填通过。

| AC / 来源 | 对应场景与要求 | 原生入口、输入与预期观察 |
| --- | --- | --- |
| AC-V1 / V1 | S1–S3；R1/R2/R3 | A 经正式 owners 归档并合入目标；B 无 A 私有记录的独立 common-dir clone，从原生入口接续同一 TaskId，generation 仅增一次。分别完整执行新 Delivery→Completion/Closure/Finish及 evidence-refresh→Completion/Closure/Finish；后者无空 Delivery。覆盖 target前进及A seal/退出/清理待处置；不能复制.git或用手写completed/seal fixture代替原生成功 |
| AC-V2 / V2 | S4；R1/R3 | 用可获取但未入默认分支的活动ref/commit；B无A session/binding/checkpoint恢复同Task/Delivery及下一owner。保留适用工程结果与历史，不继承pass；已有后继不重复递增 |
| AC-V3 / V3 | S5；R1/R3 | 分别有Open PR、MERGED Delivery PR、exact-source Issue disposition无私有receipt的样本。Open覆盖Draft/metadata未完成和Ready已完成；原Publish补剩余动作或恢复事实并重判readiness。精确输入/对象进入唯一consumer，零重复副作用、零新Delivery/gate；可复用适用现有测试 |
| AC-V4 / V4 | S6；R2/R4 | A共享Finish成立而旧资源待清理，B用不同合法资源继续，既不要求先清A也不声称A已清理。两个common-dir同名local branch不串认；旧Cleanup遇推进remote ref保留新提交且不删除新generation资源 |
| AC-V5 / V5 | S8及未完成S1/S5；R2/R3 | 未合入归档、身份/副作用归属冲突、不可获取ref/commit、未发布代码/必要输入分别返回具体缺口和原owner，保留无关状态。已满足R2终态不能因缺本机seal归为未完成 |
| AC-V6 / V6 | S6；R4 | 两Task在独立branch/worktree正常推进；一方runtime缺失或Cleanup pending不阻塞/改写另一方绑定、内容、资源。原owner合法并行子Agent分工保留；不增加压力或锁测试 |
| AC-V7 / V7 | S7；R5 | 固定0.7.0-guru.3/schema2同构正式旧归档无原机记录，经受支持入口继续同Task并由下一实际owner消费。人工历史仍走#577；未完成closeout回原事务。不补历史、不批量改档、不操作业务现场 |
| AC-V8 / V8 | 全场景；R1–R5 | canonical/package/runtime、public I/O/unique-consumer、dogfood/installed/声明平台、reapply/drift、sidecar及git diff --check通过。报告原生独立clone样本与最多一个代表安装样本的真实层次；不泛化Release/多平台或业务成功 |

整体 Completion 需核对所有真实 Delivery、上述完整要求及适用证据。随后 Closure、Finish、精确 Cleanup 分别由原 owner 处理，并核实 satisfying PR 全部 MERGED 且可达 live main。Delivery 合并或依赖登记均不足以关闭整体 Issue。

## 8. 实际未决项

当前没有需要用户补答的产品范围或来源选择。技术方案仍由选定 Delivery 的 Author/Architecture 核验：全链每种状态的真实 consumer、公共API是否足以支持正式旧归档与再次Finish、以及无私有receipt的原Publish/Closure恢复输入。它们不能由本PRD预判已支持。

若公共能力不足，保留精确owner/API/prerequisite和受影响写入停点；不改变R1–R5/V1–V8，不把依赖登记当完成。scope-only写作不创建Task根design/implement，不批准Planning、不激活实施。
