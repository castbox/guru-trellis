# #850 Architecture 隔离贡献

状态：proposed。Task为850-retire-default-wording-gate/generation 0；D1为eb5ddae6-a516-41a4-9058-fb5d5d59c20b。固定before为Git a72981db56d2070d8140b468cab3a97ae82effd3。来源为#850职责承接、完整迁移与在途条款；change_path=target_native。本贡献只拥有本Task拟变更的完整单元，不是shared-current或质量通过结果。

## 目标与原维护责任

原Architecture owner在实施及真实工程结果后重读实际shared targets，语义整合下列完整定义并readback；TaskCommit与独立committed Review审actualbefore/after。原RDT owner单独维护其requirement/design/test关系。普通独立主题不登记root/index、递增无关global version或改其它Task贡献。

实际拟写目标：docs/architecture/03-domains/issue-review-intake.md的完整能力；01-current/system.md中的ARCH-CUR-056/058；03-domains/ownership.md下列稳定单元；新增ADR-850-DEFAULT-WORDING-RETIREMENT到docs/architecture/adr/850-default-wording-retirement.md。另含`docs/architecture/06-governance/change-contract.md`的完整`Change paths and lifecycle`与`Current Planning boundary`章节，保留九concerns、descriptor/check identity及其它未变章节。另含runtime-location明确Git对象与实际副作用完整章节、distribution ARCH-INT-044和ownership ARCH-DOM-061完整单元；原历史before/验证结果保持。其余定义及历史结果保持。新ADR仅窄替代独立Wording机制，前驱历史由固定before及原来源定位。

## 完整拟后定义：Issue Review Intake

# Issue 审核、评论与开工复核

Identity：`ARCH-DOM-ISSUE-REVIEW-INTAKE`。拟后继状态：proposed。该前驱的整合叙述保留历史含义；本后继正文尚未晋升。原语义 owner 为 `guru-maintain-architecture-baseline`，精确内容由 Git revision 与本 locator 定位。来源为 [Issue #819](https://github.com/castbox/guru-trellis/issues/819)，固定 before 为 `4f2adef1f7b099f78bb8429e8b8facd66dce3bfc`。

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

配对Test分别记录生产wrapper、真实Agent、matching采用和外部GitHub动作；源码、schema、mock、评论、贡献或历史结果不能相互替代。原历史观察仍可从固定before与原Test读取，本拟定义不重写其结果。shared-current晋升仍须原final_integration/readback、TaskCommit及一次独立committed Review。

## 完整拟后定义：Current system 单元

## ARCH-CUR-056：唯一 Phase 0 Intake 与来源回程（.83）

`ARCH-CUR-056`（reviewed #250 contribution；promotion 新 diff gates pending）：Clarify 以六个独立 profiles 拥有 Intake 语义；standard/reviewed 保留 Sync→Discovery→Clarify 顺序，四类 context request 精确保留原 profile/target/continuation 与必要 caller identity。两 qualifier confirmation 各回原 owner。Clarify 只产出最小 selected locator/section/role，经当前Readiness 交给 Planning fresh reread；最终设计处置仍只在 design.md。Interface 1.8 的具名 profile selector 是薄 schema projection，不新增语义 router、表达式引擎、来源缓存或未来 Author 前置。current-only successor/migration 显式退役旧固定回程；实际证据和恢复边界只由[唯一 Test](../../requirements-design-test-contributions/250-phase0-intake-owner/test.md)拥有。原 task/source/Closure/恢复 owners、软件轴与 GAP lifecycle 保持。

## ARCH-CUR-058：唯一 Planning writer 与当前 scope／continuation

原Author独占Task整体scope-only PRD，以及当前声明的delivery_ profiles的选定Delivery三正文和context。workflow显式调用原owner；upstream brainstorm只提供讨论方法，不成为第二writer。整体范围先经Clarify source/scope判断，再由task_scope_requirements写根PRD；只有原Clarify task_scope_requirements_acceptance审查实际AuthorityRef并accept_scope。pre-Author scope_ready2.0无task_key，post-acceptance结果含实际task_key；后者才按当前义务进入原stage rework/withdrawal、显式Creation或Completion。无current Delivery不造空切片；两次结果不能互换。

同一Architecture owner的planning3.0 candidate_assessment消费真实候选并回Author solution_planning；final_plan消费实际当前方案及真实贡献/必要ADR，只回相邻Approval。独立 final_plan 的完整显式对象经原 Architecture 本地入口只读校验，无绑定或同 Task/generation 无选择时不先写 session；匹配选择复用，其他选择、terminal、error 和真实失配回原 owner。TaskId/generation、C4/唯一checkout、公开关系/profile、planning/scope/root/design freshness 都保持。该对象不授予执行选择，Approval 仍核自身合法选择；其他目的和 stage 保原恢复。决定见 ADR-EXPLICIT-REVIEW-OBJECT。原内容/Approval及Delivery修订经薄projection回唯一Author，实际批准仍交原Delivery Activation记录公共Planning。TaskId/generation、公共模型和各原writer保持。Author按当前source/candidate前置写作，Approval保留planning_scenario_set；bound planning Discovery recovery仍归原context owner，sync purpose只在当前调用承接。无第二Architecture/Approval writer、旧planning dual reader、长期规划cache或授权存储。旧#292 Task-root profiles、private4/scope_ready1、Task development-status activation/resume属于固定旧完整安装，不作为当前入口；精确历史见该单元Git前驱和[原贡献](../contributions/292-unique-planning-author.md)。

初始Task Creation及其原操作恢复保留精确created准入。既有活动Task通过当前TaskId/generation、合法common-dir binding、唯一checkout和实际阶段owner继续写入，不要求原机created/runtime，不放宽初始恢复validator。Delivery Creation/Selection的created wire保持；其唯一consumer重读同key的current selection/phase和root，planning中真实尚需初始requirements且符合Author前置才进initial Author；其余均走唯一continuation的实际未完成义务，包括已有planning的适用Author/Architecture/Approval或当前approved到Activation。缺失/过期输出回原producer，phase不重启初始Author。选择和恢复保留key、phase、规划和适用结果，phase不产生gate pass。

本条与[ADR-035](../adr/035-current-continuation-scope-routing.md)窄替代ADR-011/023/024命中的旧恢复和scope路由，保留原producer恢复、唯一continuation、官方API、独立语义门禁和终态责任。current执行细节由canonical workflow/packages单写，matching切换见[MIGRATION-657](../../../trellis/presets/guru-team/MIGRATION-657.md)。[本批Test](../../requirements-design-test-contributions/657-workflow-continuation-conflicts/test.md)分别拥有source、installed/native、Agent及未验证结果；知识接受不证明业务采用、Task完成或Release。

## 完整拟后定义：Ownership 单元

`ARCH-DOM-039`（#250 reviewed）：Clarify 唯一拥有 Intake 意图、requirement authority、selected source roles、Issue intent 与真实选择；Discovery 只拥有 context evidence/coverage，Readiness保留独立判断并薄relay；原内容owner保留完整保义和清晰度判断，Planning 单写最终设计处置。Create Issue/Create Task、scope-change、两 qualifiers、#468 execution recovery 与终态 owners 保持；Intake intent 不授予 Closure authority。Architecture/RDT 各由原 owner 串行 expected-current promotion，无第二来源模型、shared cache 或授权存储。

`ARCH-DOM-041`：Author单写Task整体scope PRD及所选Delivery规划和revision；Clarify先判断来源/scope，Author根PRD后由原Clarify acceptance核AuthorityRef并accept_scope。pre-Author与post-acceptance scope_ready2.0由原clear-router分别消费；只有post结果交当前stage合法rework/stop，Clarify不取得stage writer。Discovery单写context evidence，原normal/solution/root owners分别判断候选资格；Architecture两目的独立评估与Approval保持原职责；原内容owner承担实际措辞质量，当前Planning由原Delivery Activation记录。各回程仍为显式最小projection，不解释来源或重建producer private；execution/Task writer、Delivery/Completion/Closure/Finish/Reactivate及RDT/Architecture晋升owners各自保持单写。当前取舍见ADR-022/024/035；ADR-023的旧DTO/profile/status片段只适用固定旧完整安装，原先判断后写作及唯一writer原则继续继承。无第二来源authority、store或审批链。

`ARCH-DOM-043`（#531、#752）：上游拥有 Task/Delivery 公共模型、identity/selection/session 和确定性转换。Plan2 纳入全部 eligible registered workspaces，由 Fork 公共 parser/group/executor 校验 current-schema peer、完整 parsed Task 等价性、原 branch binding 和唯一 live authority checkout；Guru 只投影原 binding 与完整 inventory，不复制 group 算法、不新增 copy 模型或 binding writer。合法 defer peer 保留原 bytes/modes 与业务元数据，不形成额外 lifecycle、Delivery 或 session selection authority。只有 selected workspace 中 projected Task 能进入原 Guru private-owner conversion；peer 不因相同 TaskId 进入转换。原 frozen-plan、backup、resume/rollback 和旧 consumer 退出条件继续有效。Architecture final_plan 仅接入受限只读评审对象，不把对象写为选择，也不放宽其他 consumers。Guru 拥有整体 scope 判断、每 Delivery 唯一 Author/Architecture/Approval 及 TaskCommit/提交后合并完整 Review/readiness 语义门禁。Publish/Merge 各自核原输入和真实远端副作用后投影公共事实；私有事务可用时恢复原操作，缺失时仅从明确共享 source/PR 和当前资格恢复已发生动作，history 不产生 current gate pass。Completion/Closure/Finish/Cleanup/Reactivate 保留原职责；无 Delivery 时整体需求、证据或收尾合法，不造空 Delivery。ADR-024 明确旧 Task 开发 writer 和激活分叉退出；旧安装迁移仍须公共 Plan2 与 Guru 私有 owners 各自就绪，不产生双 authority。

`ARCH-DOM-045`（#548，#657 current承接）：官方model/session/C4仍拥有公共事实，独立final_plan按原Architecture包只读入口核完整对象，其余执行接收保原绑定/选择恢复；Creation独占其pending生命周期，Author只调用producer retirement端口。Creation/Selection保持原created wire，原workflow consumer重读公共current key、generation/root及phase，只有planning中真实尚需初始requirements且符合Author入口才交初始Author；其余按唯一continuation的实际未完成义务交原owner，包括已有planning的适用Author/Architecture/Approval或当前approved到Activation。缺失/过期输出回原producer，保留phase、规划和适用结果。既有Task写入资格来自当前identity/binding/checkout及stage gates，不要求初始created；原初始恢复validator不变。Discovery/Review不索取退役metadata branch或Task development status，standalone verifier不指向current Finalizer。原说明与证据见[#548贡献](../contributions/548-creation-recovery.md)，当前窄决定见ADR-035；stage/public writer及Task终态owners不变。

`ARCH-DOM-051`（#599）：canonical managed-spec 单写清晰写作规则；当前输出 Agent、写作 owner 和独立 child 负责完整读取及自检，既有审核 owner 在原范围内判断语义与清晰度。workflow、Skill 和平台入口只承接加载定位，preset 只拥有受管分发与用户指令保护；独立Wording及专属scanner/receipt退出，显式措辞请求由原Clarify或review-change按对象有界只读承接。Architecture/RDT 原 owners 继续分别晋升各自 shared-current，无新增语言审核 owner 或授权存储。

`ARCH-DOM-055`（#154）：原 Author 独占规划正文、模板和示例；Discovery 调查事实，Clarify 判断来源和范围，Architecture 按原独立方法评估，Approval、实施、Check、Delivery Review 与 Completion 分别承接原职责。普通遗漏回最早受影响 owner，技术细化不自动改变产品范围。模板填充只写选定 Task/Delivery 规划；RDT 与 Architecture 原 owners 单写长期贡献晋升，不建立第二方案或授权存储。详见 [贡献](../contributions/154-planning-body-contract.md) 与 ADR-022/024。

`ARCH-DOM-056`（#153）：Clarify 单写 Issue 内容正文并保留来源、意图、范围及正文整理判断；Clarify承担实际表述与保义审核，Readiness和Create Issue分别保留完整性/交付单位判断及已审草稿创建/回读。Author 仍单写 Planning 来源合同，managed spec 仍单写语言规则，preset 只拥有受管分发。范围外缺口先说明实际影响，真实范围选择回原 Clarify；不增加第二 writer、内容评分器或审核阶段。Architecture/RDT 原 owners 各自单写 shared-current，具体差额见 [贡献](../contributions/153-issue-content-ssot.md)。

## 完整拟后定义：Architecture change contract 受影响章节

目标为`docs/architecture/06-governance/change-contract.md`。以下两节替换同名完整章节，其余章节与九concerns/check合同保持；不得仅追加覆盖说明而留下旧current前置。

## Change paths and lifecycle

- `target_native`：新能力直接进入 target boundary，不新增 legacy authority 或 compatibility layer。
- `legacy_boundary_convergence`：仅在旧边界仍有真实依赖时保留局部 compatibility，并明确 remaining debt、owner、退出和删除条件。
- `dedicated_refactor_slice`：在行为/API/规则不变前提下，以单一主写的小切片收敛旧实现，要求可验证、可观测、可回滚和明确删除条件。
- `no_architecture_impact`：只记录 current baseline/constitution、task/stage 与可审核理由，不创建 contribution、ADR 或 project-check burden。

阶段顺序为 Planning candidate_assessment→Author solution→final_plan→Approval/Activation→implementation/完整隔离拟写与工程自检→原 owners final_integration/readback→TaskCommit→完整 committed candidate/begin_check→同次独立 Architecture before/after 与九维/full Review→Delivery Review/readiness→Publication→Merge/整体终态。首次 reviewer 新开且未参与实现，审查期间冻结 B/H 不写候选。修复由原 owner 形成后继提交；仍独立的同 reviewer 按 ADR-034 采用可核验覆盖，补审全部差额和影响，覆盖丢失或影响不明补足完整审核。提交前 integrated_pending_review 不得进入 readiness/Publication/Finish；只有真实 no_change 或 reviewed_promoted 可进入原下游资格判断。


## Current Planning boundary

`guru-author-task-plan` 独占整体 scope PRD 与每 Delivery PRD/design/implement 的规划语义写作及已有 revision 回程，Clarify 的来源/scope 判断、Architecture 独立评估与 Approval 批准分别归其原 owner；原内容与审核 owner 在各自范围承担表述、保义及完整条件判断，独立 Wording 与专属 scanner/receipt 前置退出。`candidate_assessment` 评估真实候选但不要求尚未产生的 contribution，不输出 promotion_state；其 current consumer 是 Author solution_planning。`final_plan` 评估原 Author 当前实际 design 与真实 contribution/必要 ADR，保留 reviewed_candidate 或合法 reviewed_promoted 约束，current consumer 只为相邻 Approval。前置结果不能替代最终结果；两目的仍属于同一 Architecture owner/stage，project descriptor/result 保持2.0。独立 final_plan 使用完整显式对象的只读入口；无绑定或同Task/generation无选择不先写执行选择。原 Task/C4/唯一checkout、public关系/profile、非终态planning、scope/root/design freshness及不同选择/实际error拒绝保持。空历史 reviewer 在authority后核对象，再读设计/consumers，最后解释归属。该入口不改生命周期/session/资源/规划/shared baseline，正式成功仍只交相邻Approval，后者保自身选择；其他目的/stages及普通恢复writers不变。窄替代及理由见[ADR-EXPLICIT-REVIEW-OBJECT](../adr/explicit-review-object.md)。

Clarify当前Task/Delivery scope profiles先判断范围，返回无task_key的pre-Author scope_ready2.0；原clear-router交Author task_scope_requirements写实际根PRD，scope_requirements_ready及原selection再交Clarify task_scope_requirements_acceptance。只有acceptance核真实AuthorityRef并accept_scope，输出含task_key的post-acceptance scope_ready；其consumer才按义务进入原stage合法rework/stop、显式Creation或Completion。三种scope_action均保留该顺序，不能把pre结果当发布或post结果重复写根PRD。无current Delivery不造空切片。

真实 content change refs、Approval revision actions与Delivery/Completion修订经显式projection回唯一writer。Author 的 delivery_content_revision 读取实际变化，语义未变只刷新直接依赖，实质变化回原受影响 owner；不将旧 Wording pass 或 content_changed 标签冒充当前判断。旧#292 private4/scope_ready1、active_task_scope_change Author及Task-status activation/resume只属固定旧完整安装，不作current fallback。旧planning2.0无purpose入口也不回退；非Planning6.0/Delivery4.0与bootstrap/repair保持。完整matching切换见MIGRATION-657，公共created wire、原初始Creation validator、原producer恢复及唯一continuation保持；既有Task按当前identity/binding/checkout和实际stage gates续接，Delivery created consumer重读公共phase并核实际未完成义务后进入适用owner。只有真实initial requirements且符合入口才initial Author；已有planning回适用Author/Architecture/Approval，当前approved进入Activation，缺失/过期输出回原producer。该窄决定由ADR-035拥有，不新建descriptor、状态authority或授权存储。

#531以ADR-024迁移的历史Planning责任为：Task整体scope-only由Author写作后Clarify审查；Delivery candidate/final两目的独立Architecture、Wording、Approval与Activation保持原owner，同DeliveryKey/planning_root回程。Task-only Completion/Finish仍使用task_impact_sync，不将Delivery与Task结果换标签。该句记录#531前驱含义；#850当前只退役独立Wording及专属前置，保留上述唯一writer、双Architecture目的、Approval与Activation。


本次 current-only 匹配切换与在途接续由 `MIGRATION-850.md` 拥有；已开始的固定旧 provider 操作在该完整版本完成或恢复后再更新。当前规划从同一对象和实际未完成义务续接，复用仍适用覆盖，不重建 Task/Delivery、不清空合法选择或有效规划，不制造 Wording pass。显式 Issue/draft 由原 Clarify 有界只读承接，选定 Markdown 全文由原 review-change 的 explicit_files/wording_only 承接；均无 Task/session 前置、无对象写入或隐含 ready。项目九 concerns、descriptor/check/result identity、提交前真实整合/readback及提交后一次独立完整Review职责保持。窄决定见 `ADR-850-DEFAULT-WORDING-RETIREMENT`；canonical packages与workflow仍单写具体公共合同。


## 完整拟后定义：其它直接受影响的当前关系

下列目标只替换命中的完整章节或稳定单元；同文件的其它完整定义及历史观察保持。原九concern适用判断见D1 design第9节，由原Architecture直接消费，不创建另一份记录。

### runtime-location：明确Git对象与实际副作用

目标：`docs/architecture/01-current/runtime-location.md` 的同名完整章节，稳定identity仍为ARCH-RUNTIME-LOCATION。


原guru-sync-base的operation=read以明确repo/ref/commit返回baseline_ready，固定Git tree来源与工作区候选分别绑定。对象可读时无需该分支检出或无关checkout干净；不fetch/ff、不隐式追ref变化。原operation=sync保留唯一目标、dirty/ff及HEAD/local/remote一致性，返回synced。只读成功不等于同步或正式gate。

Discovery读取固定tree的实际blob/history/archive证据，草案通过独立candidate_file字节绑定；current→history→语义审核继续由原owner执行。来源variant经当前base_current→context_current→clarity_current→readiness_current、原Clarify回程及实际Issue/Task创建consumer成套承接；独立Wording与专属linkage退出。无Task、外部worktree及正常未提交草案可以读审，不能冒充committed Review或远端发布。错基线、普通候选变化和缺正式身份回原纠正/刷新/拒绝。

Task Creation的固定来源消费承接Issue #813，适用before为main `5c6a4591db7165ece045e6b0eb789c21d06d7d38`，落实既有ADR-RUNTIME-LOCATION。当前creation输入明确reviewed_base_source的kind/selected_ref/commit；git_object的固定commit决定审核起点，selected_ref只定位所采用来源，不以其当前指向或本地同名branch HEAD判定freshness。独立selected_base_ref保留Task基线branch及非base/target资格职责，delivery_target保留未来交付仓库/分支职责。原AI读取实际ready来源并完成薄projection；脚本只校验对象和关系，不选择来源语义或重建上游通过。

原Creation/composition在record/create及check/recover共用来源归一化和commit/acquisition绑定。git_object验证同repository可用的精确commit对象及acquisition.decision_head一致；synced_branch从实际同步输出薄投影，新建前保留来源branch标准化一致及local HEAD相等检查。两者继续原exact source、common-dir、TaskId/generation、branch binding、注册位置和ownership/session约束。固定对象来源不要求移动或清理primary。真实对象/acquisition不一致给出字段级原owner恢复，不通过放宽身份条件制造成功。

已完成创建的check/recover重读原结果和原control/session关系，不再执行precreation uniqueness，不重复创建Task、branch、worktree或C4/C5；原source.commit须与真实acquisition起点一致。恢复保留原session分流：同Task/generation/ref保持原绑定；session_record_missing仅由原session owner重新attach；不同或无效session阻塞；context_key_unavailable保留explicit-task模式。后来正常ref前进不把原结果改成缺失。当前输入版本和旧schema/API退出由MIGRATION-813单写：新版本成套迁移受控consumer，旧schema字节保留验证，旧成功操作由完整固定旧provider恢复，旧待执行输入以实际上游来源经当前原owner重审。不新增current旧parser、自动kind猜测、来源台账或第二恢复writer。

代价限定为原创建合同的一个必要source值、共享归一化、原错误投影和直接consumer迁移。对象可读性与本地同步状态分别检查，减少无关primary同步等待；不增加协调阶段、锁或跨Task状态。只有来源语义、合法创建/恢复consumer、原Task基线或同步副作用合同变化时重评。RDT拥有完整需求/设计/验证，Architecture拥有本责任定义；实际链路、目标安装、Delivery和Task整体完成各由原owner以真实结果证明。


### distribution：ARCH-INT-044

目标：`docs/architecture/04-integrations/distribution.md`。

`ARCH-INT-044`：Author package、目的专属Architecture planning3.0、原Clarify内容职责、Approval及Discovery合同由canonical marketplace/preset投影至shared/dogfood/声明平台。当前Task/Delivery scope采用scope_ready2.0两次承接，Task根PRD只由scope-only Author写，accept_scope只由原Clarify acceptance执行；旧#292 private4/scope_ready1、旧profile和status consumer不作为current fallback。原两目的评估、qualifier Author input、最小projection和各owner保持；旧planning2.0无purpose入口退出，中断调用fresh原owner重入，非Planning采用当前6.0/Delivery4.0，pinned历史validation assets保留。完整matching切换和在途恢复见[MIGRATION-657](../../../trellis/presets/guru-team/MIGRATION-657.md)。live registry/Interface定义inventory；[#292 Test](../../requirements-design-test-contributions/292-unique-planning-author/test.md)保留原结果，#657当时actual source/installed/Agent及未验证层只见[#657 Test](../../requirements-design-test-contributions/657-workflow-continuation-conflicts/test.md)。知识晋升和源码一致不证明旧业务安装、远端发布或完整Upgrade/Release矩阵。 #850直接退出独立Wording及专属scanner/receipt，当前后继版本与受控consumer按MIGRATION-850成套切换，不覆盖已发布schema path/id。显式Issue/draft及Markdown全文各由原Clarify/review-change有界只读承接；旧固定provider已开始操作先原对象恢复再匹配更新。原#292/#657 Test只保各自历史观察；本批生产wrapper、真实Agent、managed更新/退役和未验证层由本Task配对Test记录，不从源码或历史结果推定安装采用或Release。

### ownership：ARCH-DOM-061

目标：`docs/architecture/03-domains/ownership.md`。

`ARCH-DOM-061`（#795 reviewed source）：Discovery 继续独占 context evidence/coverage 与 owner-result authoring 诊断。Git-object record 先校验当前 owner-result 结构，再由同一 owner 读取 fixed Git evidence 和生成派生 identity；共享 schema validator 提供字段诊断，共享 dispatcher 只保留真实未知异常的维护路由。普通同范围结构错误保留原失败，可由原 Discovery owner 用完整正确输入重跑原 record/check/invoke；Clarify、Readiness、Architecture、Check 与安装 owner 保原职责；独立Wording退出，实际表述与保义由原内容/审核owner在原范围承担。同步来源 owner-result 3.0 与当前 Git-object 4.0 各保留明确版本和 consumer，不形成第二来源模型。

## 决定、兼容、GAP与成本

必要ADR候选位于本Task D1的architecture/adr-wording-retirement.md，拥有本次决定、替代方案、成本、固定旧provider退出与复审条件。project concerns、source/semantic token、完整迁移和验证入口见本D1 design第4–8节，不复制另一套接口定义。既有GAP006/008闭合历史及其它GAP生命周期不变；没有新永久GAP或长期兼容layer。目标旧包及专属依赖退出，未完成的固定旧操作由原provider完成后切换，历史保可读。

并行范围仅为本贡献与本Task规划，禁止其它Task、shared current、全局导航和无关版本竞争。final_integration按真实expected-current重读目标，同能力真实重叠由原owner整合；贡献存在、预定检查或安装代码不代表完成。实际证据由原工程、Test、独立Review与终态owners分别提供。
