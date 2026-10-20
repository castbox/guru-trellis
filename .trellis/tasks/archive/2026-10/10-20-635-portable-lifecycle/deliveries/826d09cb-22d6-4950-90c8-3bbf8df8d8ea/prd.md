# 跨环境生命周期基础 D1 需求

## 1. 整体来源与术语

本批属于 Task `635-portable-lifecycle`，generation `0`，Delivery `826d09cb-22d6-4950-90c8-3bbf8df8d8ea`。公共 planning_root 为 `deliveries/826d09cb-22d6-4950-90c8-3bbf8df8d8ea`。整体 accepted_scope 为根 `prd.md`，revision `sha256:911172f5ef106c3aa51ae8d01e7fd66abfb220c25e211cc0fe6c5f24a1354e99`。

| 来源 | 章节、角色及用途 |
| --- | --- |
| [整体 PRD](../../prd.md) | 第3–8节是本批整体范围、R1–R5与AC-V1–V8的已接受要求；本批不重新选择范围 |
| [Issue #635](https://github.com/castbox/guru-trellis/issues/635) | 全文为原始需求；2026-10-20重读，updatedAt为2026-10-19T09:43:23Z；方案方向不代替Architecture判断 |
| `docs/requirements/current/task-delivery-lifecycle.md` | 身份、唯一Planning、恢复、最终检查及Delivery/Task责任的current authority |
| `docs/design/current/task-delivery-lifecycle.md` | 公共Task/Delivery模型、原owner、适用性与副作用恢复的current design authority |
| `docs/architecture/README.md`、`00-foundation/design-constitution.md`、`06-governance/change-contract.md` | 当前职责、五原则与实际project-check authority；不是预填通过证据 |
| `trellis/presets/guru-team/source/trellis-source.json` | 当前采用上游`1e22a77b8edcec0269252436c1f6df6c52d99734`，CLI/Core `0.7.0-castbox.5`；source构建已验证，目标安装仍须独立证明 |
| Guru tag `v0.7.0-guru.3`，commit `7d20a930341dae3e7dd2d214660ce3b99e28d863` | 固定旧格式来源；第3节列实际归档样本，不靠版本号判定合法性 |

本批沿用Task、Delivery、shared Finish、local resource responsibility的整体定义。共享终态、当前语义判断、本机资源责任和工程命令结果相互区别。本批尚无已接受solution；规范性来源设计的唯一处置在后续design第3节维护，不在本PRD重复建矩阵。当前`source_selection=[]`。

## 2. 整体与本批目标、非目标

本批是首个且覆盖全部整体要求的Delivery。原consumer把本机Finish/Cleanup回执作为共享任务准入条件，导致独立clone无法继续已经完成共享归档的同一Task。D1目标是在原owner和公共模型边界内完成R1–R5/AC-V1–V8，覆盖新格式、指定正式旧归档、活动接续、既成副作用恢复、两条再次Finish及资源隔离。

不以Reactivate fallback替代全链交付，不以登记上游依赖替代Completion。原Agent退出或原机不可用后的替代执行者继续同一生命周期；不支持两个独立环境同时主导同一生命周期。保留原owner合法并行子Agent。

不实现scheduler、分配服务、暖池、控制中心、锁/租约或第二生命周期authority。不迁移未发布dirty修改，不恢复developer identity/workspace journal/mappings，不发现其他clone未发布incarnation。不扩大到攻击/伪造、TOCTOU、压力、fault injection或非常规crash矩阵。不写Backend/业务仓，不跨仓实现CLI/Core，不执行完整Release矩阵、tag或Release。

## 3. 本批起点、前序结果、依赖与剩余责任

本Task无前序Delivery。当前D1仅由公共Creation分配身份与planning_root，尚未Activation、实施、Check、Review、commit或发布。开发起点为`7a7b60743499653ffeb81f6b31e627a02c33f579`；内容B已由原projection解析为该SHA，PR target为castbox/guru-trellis:main；design第1节记录二者，不能用后续origin/main漂移替代内容范围。

前置#636/#637/#638已CLOSED；#638实施PR646合并`6482d01e0863440b41c0a13ea89d62cfc0a747bf`，归档PR647合并`7a7b60743499653ffeb81f6b31e627a02c33f579`。这些事实仅说明前置可用，不证明本批验收通过。本批保持其Draft、后继候选适用性和晋升先于最终Check语义。

指定旧样本为固定tag中的`.trellis/tasks/archive/2026-10/10-08-503-mixed-task-identity-reservation/`：合法id `issue-503-mixed-task-identity-reservation`、顶层generation0、结构化exact_source #503、completed状态；无当前Completion/Closure数组。`finish-summary.json`为schema整数2，generator为`guru-team.finalize-task`。归档创建commit `b61304bdd30c6545fca734f8c02d33df0ea738c3`，bookkeeping PR505合并`b0289465d0d83f41f1979401aff081e0c30849e0`，该归档树无原active路径。本批不修改该历史样本、不操作#133业务现场；还需由原owner审查其完整终态证据和受支持转换。

上游公共前置已由 [Trellis PR #55](https://github.com/castbox/Trellis/pull/55) 合入，merge为`1e22a77b8edcec0269252436c1f6df6c52d99734`，精确merge的main CI为`39449964080`且成功。新增独立`formal_archive_reactivation`；普通conversion/manual resume保代、当前Task2 reopen要求Completion的合同不变。原独立Architecture已只读复核实际API足以承接原`legacy_boundary_convergence`方向，未发现新增provider缺口；该复核不是正式final_plan或Approval。具体I/O、采用与迁移差额只在design第5节维护。Guru canonical source lock已采用精确merge，matching Core→CLI构建与source validator通过；Guru目标安装及原生消费尚未完成。

本批该依赖的owner为`castbox/Trellis` CLI maintenance + Core Task生命周期。前置必须给出原生正式旧归档接续操作：保留原TaskId/source/history，不制造旧Completion/Closure，严格递增generation一次，并提供同操作/已有后继恢复及下一实际owner可消费结果。Guru只负责当前语义判定与原package确定性适配。公共能力已合并不等于所选安装具备该能力。matching source/build与目标采用未核实前，停止依赖它的真实转换/Reactivate写入；独立调查和需求规划继续。不得在Guru自建公共模型或重复上游实现。

全部未交付责任仍留在本D1。整体Completion必须检查R1–R5/AC-V1–V8真实证据、全部实际Delivery、satisfying PR均已MERGED且可达live main，再分别执行Closure、Finish和精确Cleanup。依赖声明、归档入口probe、源码通过或单个Delivery合并均不足以完成Task。

## 4. 本批调用方、场景与流程

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

## 5. 完整行为、条件与约束

以下为本批实际承接的全部R1–R5；其共享定义来自整体PRD，本批行为完整展开。

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

以下约束同样约束本批实施与验证。

1. 原全局 workflow 只编排 stable skills 和唯一 typed consumers；step-local skill 独占内部语义。脚本只 executor/validator/最小 recorder，不能代替 scope、Review、readiness 或 Completion 判断。
2. 保留 Finish 先投影归档、合并 bookkeeping 并验证目标，再封存本机资源的顺序；保留 Cleanup 的 repository/ref/expected-head 语义。修依赖倒置不能直接删除合法性校验。
3. 保留 #636 Draft 及同 PR 恢复、#637 后继候选适用性、#638 晋升先于最终 Check。公共结果、工程执行事实和当前语义判断分别处理；真实 Check、首次完整独立 Branch Review、readiness、expected-head 均不可削弱。
4. 公共 skill/exit/schema/command 的变化提供明确版本或兼容迁移。canonical/workflow/声明平台/dogfood/完整 preset 成套同步。reapply/update 保留用户修改，逐项处理 sidecar；不改全局 CLI、上游源码或 node_modules。
5. 验证范围为证明本 accepted scope 的最小可靠集合。至少一个独立 common-dir clone 原生端到端样本；安装验证最多一个代表性样本。#630/Release owner 的完整矩阵不是本 Task 门禁，也不能声称已验证。
6. 本轮基线 clone 的普通 preset apply 曾在写前被旧归档迁移前置阻塞；随后使用仓库已有 source bootstrap 恢复 managed Python，并通过正式 Sync 和只读 dogfood drift。该结果不证明完整 apply/reapply 成功。实施验证必须采用匹配受支持原入口，保留该真实边界，不迁移无关归档来制造安装成功。
7. 任何 Git/GitHub 副作用保持当前对话的精确边界；授权不写入 tracked、runtime、checkpoint 或 archive。本整体 PRD 不授予 commit/push/PR/merge/closure/cleanup 或业务写入权限。

## 6. 本批验收、验证方式与未决项

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

当前没有产品范围或来源选择待用户补答。design第5节的公共API已实际合并；精确merge的matching构建与canonical source-lock采用已完成；待完成的是原transport/Reactivate及全链适配、目标native/下一owner消费。本批design/implement已展开三项实际机制、全链owner分类、最小恢复输入、迁移与执行验证计划，交原Wording、Architecture final_plan和Approval。实际实现/安装/原生验收仍由后续原owner执行；不能以未来验证未执行阻塞规划，也不能预填成功。完整D1范围保持，依赖登记不算交付，不改成fallback-only。

## 7. Canonical 引用与本轮差额

| 当前authority与命中单元 | 本轮差额及后续owner |
| --- | --- |
| `docs/requirements/current/task-delivery-lifecycle.md` 身份/恢复/交付事实；`docs/requirements/current/completion-closure.md` Completion到Reactivate | 补充共享事实可恢复、必须重审、本机责任与真实缺输入的明确承接；原RDT owner维护完整单元 |
| `docs/design/current/task-delivery-lifecycle.md` D531-01/03/08、恢复；`docs/design/current/completion-closure.md` | 解开共享终态对本机receipt依赖，保持公共模型和原owner；方案见design；正式API和source采用已完成，Guru适配及目标消费待实施 |
| `docs/test/current/task-delivery-lifecycle.md`、`docs/test/current/completion-closure.md` | 补AC-V1–V8的命中验证，不以手写fixture代替独立clone原生样本；原RDT owner负责测试知识 |
| `docs/architecture/README.md`、`06-governance/change-contract.md` | 候选涉及公共生命周期/本机资源职责及上游依赖；原Architecture已评估候选路径；完整final_plan仍需实际设计、贡献和必要ADR |
| `trellis/skills/guru-team/packages/`对应Identity/Bind/Planning/Check/Review/Publish/Merge/Completion/Closure/Finish/Cleanup/Reactivate；`trellis/workflows/guru-team/workflow.md` | 逐项核实producer/consumer与缺失入口，只改证实的依赖倒置；公共API变化提供迁移，workflow不复制step-local行为 |
| `trellis/presets/guru-team/`与声明平台dogfood副本 | 匹配完整分发、reapply/drift/sidecar；当前bootstrap+只读drift不能宣称完整apply或安装样本通过 |

本轮完成本批需求、design/implement方案、实际依赖定位及task-owned贡献/ADR候选；Policy与Docs Plan位于implement唯一位置。真实候选已获独立Architecture评估，仍须当前Wording、final_plan和Approval；共享CURRENT保持原值。已合并公共能力的正式采用与原生消费不能被新台账、seal fixture、空Delivery或直接修改schema2记录替代。所有验收继续待实施。
