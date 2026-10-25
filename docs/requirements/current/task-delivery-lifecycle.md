# Task 与 Delivery 生命周期

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/requirements/current/task-delivery-lifecycle.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

并行 #663 晋升的完整前驱：Git `e9583202b67750d7b3ec2b7eab4b037c0c52a226:docs/requirements/current/task-delivery-lifecycle.md`；来源及窄修改见 [#663追踪](../../requirements-design-test-contributions/663-contract-continuity/traceability.md)。

更早晋升的完整前驱：Git `319202beab79c7666ecdb855291bf117e43d407e:docs/requirements/current/task-delivery-lifecycle.md`。贡献与窄替代边界见 [#657 追踪](../../requirements-design-test-contributions/657-workflow-continuation-conflicts/traceability.md)。
知识单元：`RDT-REQ-LIFECYCLE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由完整Git revision与locator定位；较早历史完整定义为 immutable Git `39169628f5f79cb48673eae96a36670e73f4dbbb:docs/requirements/current/task-delivery-lifecycle.md`（RDT `.113`），更早迁移来源和稳定身份保留。

## 身份、整体责任与入口

`REQ-001/003/004/005/008/010`、`BEH-001..006`、`R531-01 / BEH531-OWNERS` 保持身份。Task 承担整个 accepted scope 的要求、来源和完成责任。Delivery 承担一个明确切片的独立规划、候选、检查、审核和交付结果。D1 与 D2 使用同一种公共 Delivery 模型；D2 不能覆盖 D1 的文档、历史或结果。公共 Task/Delivery 状态归官方 Trellis API，Guru 不另建状态机，也不写 schema-2 Task 的开发 `status`。

新变更先由原 mode owner 判断 standard intake 或 task-free；Issue 的存在、文件数和路径不能单独决定模式。标准 Intake 依次同步所选 base、发现当前变更上下文、澄清来源/要求、审查措辞及独立可交付性，再由原 Creation 创建 Task 和绑定的执行位置。信息查询不创建 Task。已绑定 Task 的变化走原当前 owner，不从 Intake 重建身份。缺失、重复或不唯一的公共身份、出口、consumer、安装合同或 checkout 关系须停止或进入其原恢复路线，不能由 inventory 的唯一候选猜选。

AI 判断 scope、来源、关联、finding、充分性和路线。确定性工具只执行明确动作、读事实或校验结构/内容绑定。mandatory step 由 global workflow 以稳定 Skill id 调用，step-local Skill 独占完整内部行为。semantic Gate 的脚本成功不代替语义判断。只处理诚实协作中的合法正常路径、普通错误与过期状态，不增加对抗伪造或未要求的并发/崩溃机制。公共 Skill/exit/schema/path 的破坏变化必须有显式迁移。

`R657-01 / BEH657-ADMISSION`：初始 Task 创建和原操作结果恢复保留原 checked created 与精确创建校验。既有活动 Task 经正式 TaskId/generation、合法 binding/rebind、唯一 checkout 及适用 session/explicit-task 解析后，由实际阶段 owner 判断写入；原 created DTO 或原机私有 runtime 不可得不能单独阻塞。正常无范围变化保留仍适用工程结果，真实缺失或歧义回原 owner。每批 source/test/task 写入前仍执行 live checkout boundary，不重建 Task 或空 Delivery，不补造初始创建、资源或历史 pass。

`R657-02 / BEH657-SELECTION`：创建和明确选择已有 Delivery 都保留原 created DTO，其含义是实际 key/root 已建立或选定。唯一 consumer fresh 读取同 key 的公共 current phase；只有 planning 中真实初始需求义务且符合 Author profile 前置时进入 initial Author；已有 Planning 恢复实际 Author/Wording/Architecture/Approval，当前 approved 进入 Activation，缺失或过期结果回原 producer。其余活跃阶段回原 continuation。保留 key、phase、规划、历史及仍适用结果；不能以 created 名称重置阶段或以 phase 冒充门禁。输出丢失经原 producer 恢复同结果，后续按真实阶段承接。

## 切片建立与唯一 Planning

`R531-02 / BEH531-PLAN` 与 `R292-01..12/14/15` 保留。原 Clarify 接受整个 Task 要求后，原 `guru-create-delivery` 在首次 Planning 前建立或明确选择 DeliveryKey、scope_ref 和上游 planning_root。创建只建立 Delivery，不另建 Task/branch/worktree。方案返工、base 变化或同一 PR 更新保留同 Delivery；确有后续独立工作才建立下一切片。局部 provider 缺口仅阻塞实际依赖它的场景，已经确认必要且独立的工作继续，consumer 不接管 provider。

唯一 `guru-author-task-plan` 写 Task 整体 PRD，以及选定 Delivery 的 PRD、design、implement 和 context manifests。Task 整体文档不冒充 D1 计划。Author 先充分读取真实来源，区分要求、已有规范性设计、建议、实现证据和历史；无法取得必要来源时说明缺口并沿原澄清路线。不能通过省略条件或把技术细化当需求改变来制造通过。

`R154-01..05 / BEH154-01..05` 保持。Task PRD 陈述整体要求；Delivery PRD 陈述本批目标、起点、前序事实、依赖及剩余责任。design 展开真实职责、契约、行为、条件、失败、兼容、来源承诺处置和可验证设计；唯一逐项规范性来源设计处置只在 design 维护。implement 明确有依赖顺序、验证、停止/恢复、唯一 Delivery Policy 与唯一 Docs SSOT Plan。full、partial、后续和返工均保留整体与本批区别；已有 detailed 承诺不能缩成标题或链接。章节、适用字段、裁剪和深度由 Author 的现行 planning-body/templates 定义。

Planning 在实质 solution 写入前先取得真实 candidate 的独立 Architecture assessment；Author 消费实际结果完成方案。最终文档经过独立 Wording、Architecture final_plan 和 Approval。无真实 candidate 不产生候选通过。Architecture/Wording/Approval 不代写 Author 正文；Brainstorm 仅在原 owner 之下复用方法。Approval 的当前正式结果交原 Activation；文件存在或 public phase 不是批准。

原 `guru-activate-delivery` 读取三份当前中文规划、明确切片及相邻 Approval 实际 freshness，完成当前计划展示/接受边界后，唯一使用公共 planning writer 记录真实 Planning 结果。调用方不能从文件重算 token 冒充 Approval。恢复读回同 operation/result，不重复公共写入；真实计划变化回最早受影响 Planning owner。授权仅存在会话，不写入任何 artifact。

## 固定内容范围、实施与返工

`BEH567-01..05`、`R531-03/08 / BEH531-REWORK/DEPENDENCY` 保持。开发基线、每个 Delivery 的固定内容 B..H 和 PR integration target 分离。原 owner 从真实 Delivery facts 选择 B；D2 消费实际前序交付结果。恢复保持同 B 和 DeliveryKey。候选覆盖 B..HEAD 全部提交内容及实际 dirty 增量，不用随 fetch 漂移的 origin ref 代替固定 B。

实施只在已核验的当前 Task checkout 写入。每个写批次前重新检查 TaskId/generation、branch binding、注册 worktree 和 cwd；不修改无关 dirty。source/test/task 文件均受同一边界约束。

`R657-03 / BEH657-SCOPE`：whole-scope 变化先由原 Clarify 返回不含 task_key 的 pre-Author scope_ready2.0，唯一 scope-only Author 写根 PRD，再由 Clarify acceptance 审查并执行 accept_scope。只有含真实 task_key 的 post-Author scope_ready2.0 才交当前阶段 owner；不重复根需求写入。revised/no_change/withdrawal_required 均保留两段职责，no_change 沿实际适用性续接；无 current Delivery 按义务进入显式 Creation 或 Completion，不为撤回创建空切片。受影响 Delivery 的实际当前阶段 owner 读取已发布的整体 authority，合法 rework 后交同一 Author更新受影响 PRD/design/implement并刷新命中门禁。仅清除受影响结果，不以旧 gate 资格阻挡 scope 修订，不改历史已交付事实。整个切片撤回由实际当前 owner 执行公共 stop/release，保留 candidate/commit/PR/history；停止不是交付或整体完成。PR 关闭及资源删除各有原 owner。

远端 ref、无关共享 CURRENT、archive 或工具版本前进，不强迫换源、同步、重写贡献或整链重审。实际冲突、必需检查具体集成失败、原 Merge 确认的既有服务端更新要求、明确依赖纳入或用户主动同步，才进入原 Reconcile；一次固定目标，按真实差额恢复原阶段，不追赶新目标或制造空提交。立即适用规则、scope、依赖和方案的实质变化仍回原 owner。

## 早期提交、Draft 反馈与并行候选验证

`R636-01..07 / BEH636-01..07` 由 #636 增加。TaskCommit 在已激活且处于实施阶段的当前 Delivery 中，以有界 AI 内容审查、最小自检、敏感内容检查、精确 staging 和目标核验形成早期真实提交。该提交仍执行原 hook/事务和同提交输出恢复，但不把完整 task Check、最终 Branch Review、全部编译或重型集成/race 作为统一前置。最小命中命令由当前 Planning 按风险选定。早期提交输出不证明任何最终 gate。

原 Publication 在同 Task/Delivery 的唯一同仓 Open PR 上创建或更新 Draft；正文准确区分已执行、失败、SKIP、未执行和待完成项目。冲突解决或问题修正形成新候选后，经原提交/发布 owner 更新同 PR，不在本地等待最终审核才能先发布反馈，不造空提交或新 Delivery。所有 Draft 和最终 Delivery 正文均 Refs-only；即使 full/default target，Issue 关闭仍由整体 Closure 独占。

同 PR 已 Ready 而需要发布未最终审核的修订时，由原 Publication 先读回真实状态/HEAD，合法 rework 失效受影响的 Check/full_review/readiness，并确保远端退回 Draft 后才推送新候选。身份、planning、固定 B、PR 与已发生历史事实保留。新候选取得全部适用最终证据后，才可沿原最终 Publication 再转 Ready；旧 HEAD 的 readiness 不放行新 HEAD 或 Merge。

Draft 后在同一固定 B/H 并行启动独立完整内容分析和风险匹配验证。目标分支前进不中断该内容审核。分支 HEAD H 的验证与目标 T/组合候选 M 的验证分别标识；文本冲突、没有 PR merge ref 或 pull_request CI 未触发不阻止固定分支内容审核和受支持 HEAD 命中检查。组合检查保留具体缺口及恢复条件，Draft 的存在不证明远端 CI 已执行。业务 CI 入口缺失由业务 owner处理，Guru 不因此接管业务 CI。

原 Branch Review 的早期分析结果只供当前实现/Check 判断和修正，不写 public full_review，不自动复用为正式 pass。正式 full_review 保留真实 Check predecessor；Check、完整独立 committed Review、readiness、Ready/Merge 各自判断实际候选。早期反馈不推迟、取消或降低完整最终质量义务。

原 producer 恢复已成功但输出丢失的 commit、Draft 创建、push、metadata 和 Draft/Ready 转换，先读回同操作实际状态/HEAD/payload，再接续剩余动作。不能创建重复 PR、空提交或以历史 Ready 冒充新通过。公共 I/O、阶段和受控 producer/consumer 必须显式成套迁移，canonical/workflow/platform/dogfood 同步；Draft 不是新公共 phase 或最终 PublicationFact，也不产生第二状态 authority。

## 最终检查、提交和独立审核

`R531-04 / BEH531-CANDIDATE`、`R530-01..05`、`R600-01..06 / BEH600-01..06` 与 `R638-01..07` 保持原独立职责和最终质量要求。实施先完成所选 Docs 策略的完整隔离贡献和 proposed 正文。implementation以固定B、实际HEAD及全部提交/dirty paths调用原candidate/begin_check进入checking；独立Architecture phase2和原Check delivery_candidate_check先读晋升前authority、完整候选及受影响未改consumers，判断完整候选。

候选通过时原Check以既有rework(target_role=implementation, affected_results=[readiness])回implementing，再输出candidate_checked，不写最终public Check。唯一consumer调用原Architecture/RDT final_integration：一次固定真实命中目标、保留双方有效条件并补审真实差额/组合/未改消费者，原owner写完整组合并读回。no-change跳过写入，不制造空贡献或ADR。普通晋升不要求全局版本递增或总入口必写；稳定identity和精确Git内容分别管理。

implementation以同B、实际HEAD及全部晋升/关系/导航paths重建candidate/begin_check，回checking；最终Architecture/Check覆盖新content_ref与全部实际差额。只有最终Check record_gate进入reviewing，随后精确TaskCommit、fresh独立committed Architecture/完整BranchReview。写前candidate、candidate_checked、candidate_ready或reviewed_candidate不能进入TaskCommit、full_review或Ready。无知识写入也执行合法候选回程，无空提交。

Check审当前完整scope、需求/设计/测试/兼容/Docs/Architecture及实际consumer。真实候选问题按正常场景/机制/因果准入；不扩恶意篡改情形。完整审查没有候选则用真正空集；全rejected不自动passed。工程结果只证明实际层次。候选失败不晋升，实质前提/义务变化回最早受影响owner，实际写入不以“只是文档”豁免。

dirty候选由原Commit精确stage/commit；clean已提交候选在fresh最终Check和当前适用性下直接首次完整Review，不造空/重复commit。BranchReview读固定B..H全diff，包括全部晋升及非最后commit；Phase2不能代替独立committed判断。finding修复后当前结果覆盖真实最终候选；窄reference alignment只承接其声明的引用/状态，不替代完整或实质正文审查。晋升前authority保持比较起点，不用新CURRENT自证或循环补Review SHA。

## 候选适用性与完整覆盖

`R637-01..08 / BEH637-01..08` 拥有以下完整行为。首次候选仍取得未参与当前实现者的完整独立审核。后继候选由当前原 owner 读取可核验原覆盖、Hr..Hi 全部实际差额、冲突双方语义与组合影响，以及受影响的未改 consumers，明确保留、失效和补充范围，对精确当前完整候选亲自形成结论。不能复制旧 pass；原覆盖不足补哪段审哪段，组合影响无法界定时完整审核。

工程执行事实、当前语义判断、Git/PR 事实分别判断。原命令的定义/版本、输入/依赖、工具链、环境、参数和期望仍适用且原始结果可核验时采用；变化、缺失、新检查或不明项补跑命中检查。计划 AuthorityRef 不证明命令已执行。同树只解决内容绑定，不证明环境或 required checks 未变；导航、版本和文档冲突须按行为含义检查，无关 target 前进不触发整合。

独立性按未参与当前实现的实际职责判断。首次仍由合规独立 reviewer 建立完整理解；后继可由同一合规 reviewer 接续，也可先形成 Architecture 判断再完成 Branch Review。阶段、HEAD 或 reviewer 身份变化本身不要求重建同质评估。各阶段仍亲自判断并通过原正式入口产生当前结果；作者自检、Planning、早期反馈、闭合声明或原工程命令不能替代这些判断。

finding/整合修正后，原合规 reviewer 核闭合、修订差额及受影响覆盖，再作当前最终完整结论；取消无条件更换 reviewer 和重复完整相同审核的要求。`fresh_final_review` 保留 wire 值，matching 迁移后表示闭合之后的当前最终完整覆盖，而非强制新身份。finding ancestry、当前 candidate/Check predecessor 和原 recorder/validator 仍真实执行；closure 不等于 pass。

合法来源为现有 public Task/Delivery 结果、实际原公开结果/调用对象、精确 Git 和当前正文，以及仍可核验的原命令结果。passed full_review 可定位原范围/plan/outcome；首次 implementation_required 没有 passed full_review，finding refs 只定位缺陷，已建立的理解不能补造覆盖。缺少合法依据时补真实审核；不跨 owner 读私有状态、不重建退休 checkpoint、不增加 review/test 账本、全链 digest 或授权记录。

Delivery Review、Publication 和 Merge 分别核当前 payload、Issue 语义、候选及 live 事实，消费仍适用的内容判断，不重做无实质变化的业务设计审核。真实 scope、前提或依赖变化回最早受影响 owner；同 Delivery 恢复不制造新身份或空提交。唯一共享执行定义由 canonical workflow-contract 的 Candidate Applicability And Coverage 小节拥有，七个原 owner 显式读取，平台只加载/路由。matching 完整安装和在途退出按 MIGRATION-637；旧完整安装固定或沿原维护 owner 成套切换，source 编辑不热迁移开发 Task。

本行为保留 R531/R567/R578/R600/R636 的有效条件、首次独立完整、最终 Check 与各当前正式结果。只替代无因新 reviewer/完整相同重审和相邻阶段抵消复用的片段。实际 #636 接口组合由后交付项验证；#638的当前组合按T638实际验证，历史#637结果不证明该组合通过。Completion/Closure/Release 各保留独立责任。

## 交付事实与整体完成

`R531-05 / BEH531-FACT`、`R434-01`、`BEH-557-01..04` 保持。Delivery Review 判断本切片 readiness、真实中文 PR 载荷、验证层次、安全和部署影响。所有业务 Delivery PR 使用 Refs-only；即使目标是默认分支且本批 full，也不提前关闭源 Issue。Publish/expected-head Merge 仅执行其已审查事务，实际远端成功、公共投影和当前 gate 适用性相互区别。输出丢失从原事务恢复同一实际结果，不重复 push/PR/merge；历史成功不制造新 pass。

已正式发布的 Delivery 后来被人工合并时，只能由原 Merge 的显式 recovery 读已有公共 Task/Delivery/Publication 关系、真实双亲合并及实际 head，记录事实并进入整体 Completion。事实不要求伪造 trailers，也不要求第二次 merge。实际内容变化、CI、gate 适用性和未覆盖范围由 Completion/受影响原 owners 判断，不能凭 MERGED 推断完成。

Delivery 合并只产生 slice 结果。Task 未分配范围、未完成要求和缺失必要证据仍归整体 Completion。Completion、Closure、Finish、Cleanup、Reactivate 的完整能力定义在 [completion-closure](completion-closure.md)。

## 跨环境活动接续与状态职责

`R635-01/03/04/05 / BEH635-STATE/RECOVER/RESOURCE/MIGRATION` 增加跨环境正常行为。原执行者不再主导同一生命周期时，B 从可获取、已提交的 source ref/commit 读取同 repository、TaskId/generation、source/scope、Delivery 和必要代码。该 ref 不必已进入默认分支；唯一可验证来源自动承接，有实际歧义才询问缺失选择。不复制 A 的 `.git`、runtime、session 或资源账本，不迁移仅在 A 的 dirty 工作。不承诺发现其他 clone 未发布状态，不支持两个环境同时主导该生命周期。

| 状态与 producer | 直接 consumer 与恢复行为 | 缺失边界 |
| --- | --- | --- |
| 公共 Creation/Task 的 identity、source、accepted scope | Identity、Clarify、Creation、Completion 读取共享记录与明确 Git 对象 | 真实 source/代码不可获取或身份不唯一回原 Identity/scope owner，不创建替代 Task。 |
| 公共 Delivery 的 key、planning_root、历史与远端关联 | 原阶段 owner/continuation 继续真实切片 | 缺唯一 selection/必要正文只阻塞对应 producer；不按 inventory、phase 或 PR title 猜选。 |
| Author/Activation、Check/full Review 的结果及实际正文 | 原 Planning/Check/Review/Readiness 亲自重判适用性 | 换机/private checkpoint 丢失不自动重开 Intake/Planning/Delivery；缺语义覆盖补审，缺工程事实补命中检查，不继承 pass。 |
| Publish/Merge 的准确 PR/commit 与公共结果 | 原 Publish/Merge 核 source、key、repository/base/head、原输入和真实状态，恢复已发生子动作 | Draft/metadata/Ready 剩余工作由 Publish 完成；MERGED 只交 Completion，缺归属回原 owner，不重复 create/merge。 |
| Completion/Closure/Finish 的公共结果、必要动作输入与归档历史 | 原 Closure/Finish/Reactivate 分别核完整关系、provider 和目标历史 | 仅 OPEN/CLOSED、MERGED 或目录存在不足；不可推导的必要输入缺失说明 consumer，不索取整套原机目录。 |
| 当前环境 Bind/session、C4 与资源 ownership | 原 Establish/Ensure/Bind 和 Cleanup 在当前 common-dir 恢复本机执行责任 | 不跨 common-dir 认领同名 local branch，不把未知 ownership 当 Guru 所有。 |

原有同操作私有恢复继续适用。私有事务不可得而明确共享 source/对象充分时，原 Publish 使用独立既有 PR 恢复入口，原 Closure 使用其最小共享动作载体，原 Merge 使用既有公共 MERGED recovery；不根据历史 Ready、Close 或输出存在制造当前资格。每个语义 owner 沿候选适用性规则亲自判断，仅补缺失或变化命中的工作。

remote branch 是 repository identity 与完整 remote ref 标识的共享资源。旧 Cleanup 继续核 generation、ownership 和 expected head；ref 已推进或属于新代时保留新提交并交原资源 owner。A 的旧资源 pending 不否定已证明的共享终态，也不阻止 B 使用不同合法资源；同一确有未完责任的资源仍受原冲突检查。两个 Task 的独立绑定、checkpoint 和清理不得互设准入；B 接续不授予清理 A 的权限。

`R657-04 / BEH657-CONTRACT`：Discovery 当前身份使用 TaskId/generation、common-dir binding 和唯一 checkout，不要求 metadata branch 或旧 Task development status。Delivery Review 使用真实 current candidate/gates；standalone verifier 的旧输入诊断回合法 source_repository_verification 准备，旧在途事务仍归其固定原 owner。公共 I/O、唯一 consumer、matching native/Guru packages、workflow、spec、平台和完整 preset 成套迁移。旧完整安装沿 pinned 原 owner 或匹配维护路径处理在途事务，不转换旧 pass。source 采用、实际安装、原生 Agent 和完整 Release 证据分别报告。共享 Finish 与指定旧格式的完整条件由 Completion/Closure 单元拥有。

## 关系和来源边界

设计：[`RDT-DES-LIFECYCLE`](../../design/current/task-delivery-lifecycle.md)。测试：[`RDT-TST-LIFECYCLE`](../../test/current/task-delivery-lifecycle.md)。知识 owner/适用性：[`RDT-REQ-KNOWLEDGE`](knowledge-maintenance.md)。来源及精确替代范围见 [迁移追踪](../../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md)。公共 profile/DTO/exit 的完整规格仍由 [canonical workflow](../../../trellis/workflows/guru-team/workflow.md) 和对应 [Skill packages](../../../trellis/skills/guru-team/packages) 独占；本单元拥有上述能力行为，不复制 schema。

## R649：阶段限制与当前成果

**R649-01 / BEH649-LIMIT**：存在真实阶段限制时，原 Author 在现有 Planning 内说明受限对象、原因、解除条件、适用阶段及后继责任。仅限制其实际依赖的能力或 operation；无变化时不制造清单、贡献或额外验证。Policy 拥有切片交付责任，Docs Plan 定位需要维护的当前定义、指南及派生说明；不建立第二套限制台账。

**R649-02 / BEH649-CONVERGE**：后继工作满足解除条件时，实施 owner 更新实际行为和适用断言，原 RDT／Architecture owner 在各自边界维护完整当前定义、指南及派生说明。当前正文不再继续指示已解除的限制；旧阶段观察保留来源和截止点，不改写成当时已完成。某能力未交付、未启用或证据缺失，不能泛化为同范围其它能力均不可用。

**R649-03 / BEH649-CHECK**：原 Check 从有效合同确定正确预期，检查实际行为、当前说明、断言及受影响未改 consumer 是否一致。测试仍保护旧限制时，即使命令通过也须指出缺陷。Delivery Review 分别判断本切片适用成果维度；维度及整体缺口的完整定义见 [Completion](completion-closure.md#r649阶段成果维度与缺口分类)。任何局部结果均不替代整体 accepted scope。

## 正常流程合同连续性

**R663-01 / BEH663-REPAIR**：Bootstrap 返回 repair_required 后，原 caller 使用声明的出口薄投影及自身当前 mode、continuation 和必要基线上下文进入同一 owner 的 repair。字段来源明确；不从 producer 私有结果恢复输入。repair owner 实际继续原维护，原新仓、已有仓及独立修复路径和普通 missing/mismatch 阻塞保持。

**R663-02 / BEH663-ARCHIVE**：归档审核 caller 依 Interface 指定正式 example 填合法 archive/Delivery/HEAD/PR snapshot，即可由原 recorder/checker/invoke 消费。只读范围不要求当前 Check，不写 active gate，不重开 Task或推进业务阶段；结果保持原 disposition stop。

**R663-03 / BEH663-BEFORE**：固定 B 早于本 Delivery 首次建立 Architecture authority 时，原 owner 明确表达 B 中既有路径的真实缺失并核实。完整 B..H、当前 authority与全部新增文件仍独立审核；不能移动 B、以 H 冒充 before、跳过门禁或作通用 freshness 豁免。B 已有文件的原路径保持。

**R663-04 / BEH663-MAINTENANCE**：final_integration promotion 请求 Bootstrap 后，caller 保留同一 Task/DeliveryKey、planning_root 和调用期 continuation，按声明的 phase2 maintenance 输入进入原 owner，再 fresh 回同一次 promotion。whole-task/Delivery 及既有 repair 回程均闭合；维护成功不等于 reviewed_promoted、最终 Check 或业务阶段推进。

**R663-05 / BEH663-DISTRIBUTION**：当前公开输入例子同时匹配 profile/aggregate schemas，出口通过声明 projection 与唯一 consumer 输入组合；动态 stage、首次 before 缺失和正常返工/恢复/stop保持语义。canonical、完整 installed、dogfood 与声明平台按 matching preset 成套采用，明确迁移、mode、sidecar和未验证层次。精确接口仍由原 packages 单写。
