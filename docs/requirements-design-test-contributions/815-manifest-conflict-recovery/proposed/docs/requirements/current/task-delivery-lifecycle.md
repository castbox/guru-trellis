# Task 与 Delivery 生命周期

导航别名：`R531-01..05/08`；`R636/BEH636`；`R637/BEH637`。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/requirements/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

本次 #679 拟整合的完整前驱：Git `e6c3b8276d62ac174ab42cba5bca4d5784be2ca3:docs/requirements/current/task-delivery-lifecycle.md`。来源及窄补充见 [#679 追踪](../../requirements-design-test-contributions/679-session-continuation/traceability.md)。

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

## 本地待审提交与 early Draft 迁移

`R636-01..07 / BEH636-01..07` 的精确本地提交、真实 hook、同提交恢复、真实远端事实和 Refs-only/Closure 边界保留。#794 通过 [MIGRATION-794](../../../trellis/presets/guru-team/MIGRATION-794.md) 窄替代审核前新 push/PR资格及旧 early profiles 的直接 Publication consumer，不静默改变旧 profile。当前 TaskCommit pre-review profiles 在已激活的 implementing Delivery 核批准 Planning、真实工程自检、必要文档整合及精确提交内容，形成本地待审 H；提交不表示实现已独立通过。clean reentry 不 stage、不造空或重复 commit，输出只交固定候选审核。

当前链在独立完整 Review 通过前不 push、不创建 PR。旧 Draft 已发生 commit、push、PR、绑定、metadata 或状态变化，由原固定完整 provider 准确恢复同操作结果，读回同 PR/HEAD/payload，不重复副作用、不把 Draft 当最终 Publication 或 pass。尚未发生的远端动作停止在原 migration owner，接回当前独立审核和 readiness 后，按同 PR 与原事务资格补剩余步骤；不能因为旧 pending存在先发布再补审。

固定 B/H 的内容审核与风险验证分别判断分支 H 和目标 T/组合 M。无关 target 前进不打断内容判断；文本冲突、缺 PR merge ref 或 CI未触发保留具体组合缺口及恢复条件，不由 Guru 接管业务 CI。作者工程自检和旧早期分析只作为适用事实，不能供新的正式 full_review pass。所有业务 PR仍 Refs-only，整体 source Issue关闭归原 Closure；Merge、Completion与终态不被本次合并。

## 提交前整合与一次独立完整审核

`R531-04 / BEH531-CANDIDATE`、`R530-01..05`、`R600-01..06 / BEH600-01..06`、`R638-01..07` 的完整范围、真实知识写入和最终质量责任继续；重复 candidate/final Check时机由本节替代。Planning批准后，implementation完成全部代码、完整隔离 proposed、选定测试/静态/diff检查及真实结果。原 Architecture/RDT owners 在提交前 final_integration 固定实际 target branch/commit，读适用 before、完整proposal、真实current及必要关系/consumer，保留所有有效条件，实际写入/readback并判断适用性。无独立candidate Check或提交前独立implementation Architecture pass前置。no_change无空贡献、ADR或提交；普通晋升不要求全局版本或共享逐项登记。

整合只表示文档已写入并待独立审核；Architecture明确 integrated_pending_review，不能称reviewed_promoted。TaskCommit的 semantic Gate针对形成精确待审本地候选，纳入全部实现/正文/关系/导航after，保原hook和事务。implementation随后以原固定B、实际committed H和全部paths调用公开constructor/begin_check；不手填content_ref、不以dirty候选或旧H冒充冻结提交。

新的独立 reviewer 未参与当前实现，审查期间冻结B/H不改候选。它先完整读固定B的constitution/baseline/change contract，再读H、完整diff和实际受影响未改consumers，形成implementation Architecture before/after判断后才读必要Task叙述解释归属。它在同次完整Review承接requirements、design、implementation、tests、docs_ssot、cross_layer、compatibility、deployment_and_operations、verification_completeness九维、完整固定区间、减法/可维护性/兼容与全部Branch Review职责。Planning独立candidate/final Architecture保留，不成为当前通过。命令绿色、九个true、旧pass或作者自检不替代当前充分性。

真实通过后，同一原Review owner先记录check（predecessor=Planning），再记录full_review（predecessor=该check）；两槽都是一次实际判断的真实投影，不是两个独立审查步骤。只有两结果都完成才输出passed并交原Delivery Review。Architecture只有实际整合完成且该committed before/after独立判断通过才reviewed_promoted；pending不能readiness/Publication/Finish。实施缺陷回原implementation修复和后继提交，真实Planning修订回最早原Author/Architecture/Approval，实际scope变化回原Clarify；保合法Planning、固定B和仍适用覆盖，不因finding自动扩scope。

没有候选使用真正空集，全rejected不自动通过。每个适用职责都判断范围和充分性，工程结果只证明其实际层次。窄reference alignment只承接原窄条件，不替代完整或实质正文审核。新CURRENT不能以自身证明符合原约束，完整before authority保持比较起点。输出丢失核同key/B/H/候选与真实结果，只补尚缺步骤或恢复同结果；必要语义覆盖丢失须真实补审，不补造full_review，不循环写Review SHA。

## 候选适用性与完整覆盖

`R637-01..08 / BEH637-01..08` 拥有以下完整行为。首次候选仍取得未参与当前实现者的完整独立审核。后继候选由当前原 owner 读取可核验原覆盖、Hr..Hi 全部实际差额、冲突双方语义与组合影响，以及受影响的未改 consumers，明确保留、失效和补充范围，对精确当前完整候选亲自形成结论。不能复制旧 pass；原覆盖不足补哪段审哪段，组合影响无法界定时完整审核。

工程执行事实、当前语义判断、Git/PR 事实分别判断。原命令的定义/版本、输入/依赖、工具链、环境、参数和期望仍适用且原始结果可核验时采用；变化、缺失、新检查或不明项补跑命中检查。计划 AuthorityRef 不证明命令已执行。同树只解决内容绑定，不证明环境或 required checks 未变；导航、版本和文档冲突须按行为含义检查，无关 target 前进不触发整合。

独立性按未参与当前实现的实际职责判断。首次仍由合规独立 reviewer 建立完整理解；后继可由同一合规 reviewer 接续，也可先形成 Architecture 判断再完成 Branch Review。阶段、HEAD 或 reviewer 身份变化本身不要求重建同质评估。各阶段仍亲自判断并通过原正式入口产生当前结果；作者自检、Planning、早期反馈、闭合声明或原工程命令不能替代这些判断。

finding/整合修正后，原合规 reviewer 核闭合、修订差额及受影响覆盖，再作当前最终完整结论；取消无条件更换 reviewer 和重复完整相同审核的要求。`fresh_final_review` 保留 wire 值，matching 迁移后表示闭合之后的当前最终完整覆盖，而非强制新身份。finding ancestry、当前 candidate/check/full_review predecessor 和原 recorder/validator 仍真实执行；closure 不等于 pass。

合法来源为现有 public Task/Delivery 结果、实际原公开结果/调用对象、精确 Git 和当前正文，以及仍可核验的原命令结果。passed full_review 可定位原范围/plan/outcome；首次 implementation_required 没有 passed full_review，finding refs 只定位缺陷，已建立的理解不能补造覆盖。缺少合法依据时补真实审核；不跨 owner 读私有状态、不重建退休 checkpoint、不增加 review/test 账本、全链 digest 或授权记录。

Delivery Review、Publication 和 Merge 分别核当前 payload、Issue 语义、候选及 live 事实，消费仍适用的内容判断，不重做无实质变化的业务设计审核。真实 scope、前提或依赖变化回最早受影响 owner；同 Delivery 恢复不制造新身份或空提交。唯一共享执行定义由 canonical workflow-contract 的 Candidate Applicability And Coverage 小节拥有，七个原 owner 显式读取，平台只加载/路由。matching 完整安装和在途退出按 MIGRATION-637；旧完整安装固定或沿原维护 owner 成套切换，source 编辑不热迁移开发 Task。

本行为保留 R531/R567/R578/R600/R636 的有效条件、首次独立完整、同次真实 check/full_review 与各当前正式结果。只替代无因新 reviewer/完整相同重审和相邻阶段抵消复用的片段。实际 #636 接口组合由后交付项验证；#638的当前组合按T638实际验证，历史#637结果不证明该组合通过。Completion/Closure/Release 各保留独立责任。

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

**R649-03 / BEH649-CHECK**：原提交后独立完整 Review 从有效合同确定正确预期，检查实际行为、当前说明、断言及受影响未改 consumer 是否一致。测试仍保护旧限制时，即使命令通过也须指出缺陷。Delivery Review 分别判断本切片适用成果维度；维度及整体缺口的完整定义见 [Completion](completion-closure.md#r649阶段成果维度与缺口分类)。任何局部结果均不替代整体 accepted scope。

## 正常流程合同连续性

**R663-01 / BEH663-REPAIR**：Bootstrap 返回 repair_required 后，原 caller 使用声明的出口薄投影及自身当前 mode、continuation 和必要基线上下文进入同一 owner 的 repair。字段来源明确；不从 producer 私有结果恢复输入。repair owner 实际继续原维护，原新仓、已有仓及独立修复路径和普通 missing/mismatch 阻塞保持。

**R663-02 / BEH663-ARCHIVE**：归档审核 caller 依 Interface 指定正式 example 填合法 archive/Delivery/HEAD/PR snapshot，即可由原 recorder/checker/invoke 消费。只读范围不要求当前 Check，不写 active gate，不重开 Task或推进业务阶段；结果保持原 disposition stop。

**R663-03 / BEH663-BEFORE**：固定 B 早于本 Delivery 首次建立 Architecture authority 时，原 owner 明确表达 B 中既有路径的真实缺失并核实。完整 B..H、当前 authority与全部新增文件仍独立审核；不能移动 B、以 H 冒充 before、跳过门禁或作通用 freshness 豁免。B 已有文件的原路径保持。

**R663-04 / BEH663-MAINTENANCE**：final_integration promotion 请求 Bootstrap 后，caller 保留同一 Task/DeliveryKey、planning_root 和调用期 continuation，按声明的 phase2 maintenance 输入进入原 owner，再 fresh 回同一次 promotion。whole-task/Delivery 及既有 repair 回程均闭合；维护成功不等于 integrated_pending_review、reviewed_promoted 或业务阶段推进。

**R663-05 / BEH663-DISTRIBUTION**：当前公开输入例子同时匹配 profile/aggregate schemas，出口通过声明 projection 与唯一 consumer 输入组合；动态 stage、首次 before 缺失和正常返工/恢复/stop保持语义。canonical、完整 installed、dogfood 与声明平台按 matching preset 成套采用，明确迁移、mode、sidecar和未验证层次。精确接口仍由原 packages 单写。

## R679：明确接收会话、首失败与文档展示

**R679-01 / BEH679-RECEIVE**：主会话承接创建结果或独立审核会话接收明确 TaskId/generation、DeliveryKey 和 planning_root 后，普通执行接收先核接收者自己的身份、唯一 checkout 与公共 current。存在 context 而缺 Task 绑定时，经原 Identity/Ensure/Bind 恢复该明确对象；同 Task 缺选择时，经原 Creation Selection 选择明确的非终态切片。匹配事实复核复用，不重复写；恢复后重读 key、generation、phase、scope、root，并回原未完 profile/purpose。已有 Planning 不重跑初始 Author，必要前序缺失或过期回原 producer。新绑定不是切片选择，也不是阶段通过。真正无 context 沿原 explicit-task 校验。独立 Architecture final_plan 使用下述 R694-01 的只读对象入口；其他入口不用显式 key 隐藏有 context 的缺失、冲突或错误。

**R679-02 / BEH679-FIRST-FAILURE**：接收调用区分 no_current_task、no_current_delivery、current、terminal_delivery、error，以及不同选择和真实 generation/phase/scope 失配。诊断指出本次首先失败条件与原 owner；恢复后再读其余条件。不同合法选择不覆盖，终态不重开，损坏/不可读/API不支持或 checkout 歧义不当作缺绑定。原 Author/Architecture planning 校验保拒绝强度、错误 code 和出口形状，细化具体 field_path/remediation；早于 Delivery guard 的真实 API 错误也保留。精确诊断与 matching 迁移见原 package 及 MIGRATION-679，不新增状态模型。

**R679-03 / BEH679-STANDALONE**：standalone_request 是来源 profile，执行 mode 独立。Readiness 使用真实 Wording producer 请求身份与 mode，调用方定位可不同；source_request_sha256 仍绑定完整当前 draft authority。普通消费者构造错误后，当前 Agent 重读未改 source/适用 producer，完整重建 consumer 并重审自身十维，再消费原 record/check/invoke 的真实结果。不得只补字段、改 producer、手写派生 linkage 或 receipt；真实 source/authority 或前序变化回原 producer。精确字段和可执行 recipe 仍由原 Readiness package 单写。

**R679-04 / BEH679-ARTIFACTS**：明确选定 Delivery 的展示把真实完整 key 传原 resolver，展示实际 planning_root 中存在的文档。尚无或无当前 Delivery 的 Task-only 停点，只展示该精确 TaskRef 内存在的整体根 PRD，不猜选、构造 key 或创建空切片。Finish 后明确切片使用实际 archive TaskRef/key。实际 resolver 调用和正常缺文件行为须验证，文本一致只证明分发。

上述行为保持 R531/R657 的 Task/Delivery 公共模型、单 writer 与原义务，Architecture first-read/独立性和适用结果保持。不能修改 context 环境借用别的会话，不能从 inventory 唯一项或 phase/文件推导身份与 pass。对应职责见 D679-01..04，验证见 T679-01..06；本批来源与窄补充边界见 [#679 追踪](../../requirements-design-test-contributions/679-session-continuation/traceability.md)。

## R694：一次性 final_plan 评审对象

**R694-01 / BEH694-OBJECT**：仅独立 Architecture `delivery_task_impact_sync / planning / final_plan` 接收完整显式对象时，无 Task 绑定或同 Task/generation 无 Delivery 选择可直接只读校验并正式评审，不先调用 Identity/Ensure/Bind/Selection，不创建持久执行选择。匹配选择复用，真正无 context 的原显式入口保持。对象校验覆盖当前 TaskId/generation、C4、唯一注册 checkout、公开 Task/Delivery 关系及 profile、非终态 planning、accepted_scope/scope_ref、planning_root 和实际 design freshness。其他 Task/key、terminal、损坏绑定、API/read error 和真实失配保实际首失败及原 owner。

**R694-02 / BEH694-BOUNDARY**：一次性评审不改业务、规划、shared baseline、生命周期、session 或资源。原空历史独立 reviewer 先读 constitution/baseline/change-contract，再核对象、设计与实际 consumers，最后读解释归属；AI 独立形成结论。实际 typed stdout 保 key/root/purpose/freshness，只有原成功出口进入相邻 Approval。Approval 仍满足自身合法选择。其他 Planning owners、实施和 Architecture purposes/stages 保原选择与恢复职责；普通恢复允许原 owner 必要 session runtime 写入。

上述两项仅替代 R679-01 中独立 final_plan 的持久绑定前置。R679 其他条件、原错误/出口/consumer 和 public I/O 不变。职责见 D694-01/02，验证见 T694-01..04；来源与替代见 [#694 追踪](../../requirements-design-test-contributions/694-final-plan-object/traceability.md)。


## R713：正常公开执行合同

**R713-01 / BEH713-CONTRACT**：受支持的业务Agent从正式安装的平台入口，依workflow、Skill及其公开引用、Interface、命令help、适用profile的输入/semantic authoring/输出合同和实际结果完成正常首次执行、合法返工和原结果恢复。当前与历史支持profile、实际输入载体及producer→consumer关系明确。公开输入完整承接既有成功域；Issue/no_issue给正向可执行例，优先引用既有来源定义。完整结果不冒充正常作者输入，公共producer身份原样承接，私有派生字段由原recorder产生。

**R713-02 / BEH713-EXECUTION**：AI选择范围、固定B、paths、阶段及semantic结论。原生产执行owner公开所需确定性Candidate构造，复用既有范围/内容算法；原Delivery operation执行begin-check/rework。新Git桥接只服务实际Git checkout、C4和当前pull_request Delivery；上游既有git_free内容引用及合法consumer保留原边界，不增加无Git Delivery。业务Agent不导入Guru私有实现填补调用能力；维护Guru本身的源码诊断不作为普通public-only验收。

**R713-03 / BEH713-RECOVERY**：原错误owner给出可机器判定的具体字段/约束、所属合同与原恢复入口。输入错误、真实stale和内部故障保持各自语义，未知根因只说明已确认范围。先捕获原exit/stdout/stderr，再按原合同消费receipt.result、checker receipt和唯一typed exit；运输成功不代表阶段通过。真实内容变化重新进入最早受影响owner，不重算旧摘要续命。

当前合并 Review 的范围内规划修复保留 current_scope 判断，并向原 Author 交接具体 revision_actions；current_scope 不因记录了范围归属而成为新需求选择。真实需求范围变化仍交原 Clarify。固定旧 provider 的每种 planning_stale 输出必须经原声明薄投影满足其真实 consumer 输入，不能只由 producer schema 自证。

对于固定旧 provider 中已执行的同一次规划回退，原 Check 仍能依据原结果、同一 Task/Delivery 和当前实际状态恢复交接，或在真实当前判断后合法纠正。不得要求本次回退依法清除的 Planning pass，不重复回退，不创建替代身份或补造通过结果，不改旧 artifact/digest，不覆盖当前候选或业务改动。真实身份、内容或范围变化返回受影响原 owner。修复前已回退旧结果只使用实际既有原因果来源转换；来源缺失时报告具体缺口并返回原 owner，不能用当前值拼造原事实。恢复不代表 Planning/Check 通过或可发布；不新增通用事务、跨阶段账本、授权记录或全链 digest。

**R713-04 / BEH713-EVIDENCE**：本项按当前适用性采用已有 source、组件、原公开命令、consumer、matching 安装、synthetic 与局部 native 结果，保留各自实际证明范围。普通字段/authoring/result/receipt 错误、真实 stale 和同结果恢复保留原首次失败、公开纠正、key/B 及仍适用证据。真实 Agent 的当前语义前提仍由原 owner 执行，host 不代填判断或私有身份；结构或命令结果不证明模型行为。#713 取消新增首次正确 preTask→Finish 完整 native 链、独立 N3 public-only 恢复链及旧 fixture 接续验收，取消不记为通过，也不形成必需补证支线。

**R713-05 / BEH713-DISTRIBUTION**：固定 B 及本项差额的 43 active packages、127 commands、180 structured profiles 须完成导航、输入/输出与 consumer 核对。F1–F13 按真实调用语义定位证据和未验证行为，公开支持域保持；本项不追加 F10 或其余非等价 family/profile/caller/goal 的 native 代表。eval 三辅助逐职责对照生产入口，必要生产知识/事实归原 owner；合法 fixture、环境、替身、运输和独立观测保留。R5 保留职责与模块回归验收，取消完整方法加载、Planning→同 fixture Activation/resume 和 Drift 的新增模型补证。canonical、dogfood、声明平台与代表性 matching 安装经原 owner 成套采用；reapply/drift/sidecar/mode 与真实旧 consumer 保持。采用仍匹配的已有实绩，仅刷新实际变更依赖；取消为上述 native 重复准备环境、恢复损坏 clean 或再次安装。完整 Release 矩阵、部署、业务采用和 #711/#712 新范围不由此推定。

本节承接 #713 的 S1–S5、AC1–AC4、缩减后的 AC6–AC8 与 AC9；AC5 取消。取消的是本项新增验收，生产职责、公开支持域、已知正确性修复和原生命周期条件保持。N1 首装配失败、N3 public-only 不充分、F10/H2 非通过、R5 方法不足/resume execution_error/Drift fitness_regression，以及旧 clean 后续损坏保留原观察边界；R3 仅 runtime 准备通过，未启动 native。不清理、续跑或改写这些结果，不将旧 clean 损坏归因 installer 或称其当前可用。

本节保留 #710 正常语义 authoring 与完整结果消费职责，当前由合并 Review 的 matching 合同承接；旧11字段/完整6.0结果只按其固定provider合法消费和恢复，不转换新pass。设计D713、测试T713保各自历史含义。当前原知识final_integration/readback→TaskCommit→完整committed candidate→一次独立Review→Delivery Review/readiness→Publication/Delivery及Completion/Closure/Finish继续；合并前保fresh merge gate，无新状态authority、wrapper或账本。


## R779：委托后的结果承接

**R779-01 / BEH779-DELEGATION**：已委托工作包由执行者自主完成等待、常规环境诊断、原断言、产物取回和终态汇总；计划外范围、机制或风险仍回原 discovery。正常推进时，主协调者推进互不影响的工作或按平台能力有界等待，不默认重复跟踪同一日志并连续补发过程指令。日志片段、页面 PASS、命令终态、产物通过和工作包完成分别判断。

介入只针对需原 owner 决定的真实阻塞、范围/机制变化、冲突写入、用户停止或执行者无法继续。诊断先核本次进程、日志和产物的对应关系及具体缺口；未知终态保持未知。必要查询、证据读取和 adb 保留。接管先查已有工作并沿可用原句柄继续，不默认重启，也不要求逐命令上报 PID、句柄或 hash。

执行者在当前对话提供最小完成内容、实际终态、结果位置及未完成项。冲突写入在自然边界暂停并确认当前终态且暂不启动下一轮后进行，完成后通知恢复；无冲突并行、无写入需求继续原委托。已交叠按实际影响披露失效证据并补必要验证，不一律重跑。主协调者仍核要求与结果、交新缺陷给原 owner；适用执行事实可采用，只有具体缺口或不一致才补查/重跑。新增要求作为明确差额，提交后合并完整 Review 保留原九维及独立区间职责。

精确协作方法由 [canonical Phase 2 合同](../../../trellis/presets/guru-team/spec/workflow/workflow-contract.md#phase-2--implementation-and-check) 单写，职责见 D779-01，验证见 T779-01/02。来源为 [#779](https://github.com/castbox/guru-trellis/issues/779)；本项只修方法及实际受管同步，不承接 #734 的预算、规模或设备/重放验收，不新增公共数据、运行状态、持久 handoff、授权记录或逐轮审批，也不承诺实际节省效果。来源、前驱与窄增加边界见 [#779 追踪](../../requirements-design-test-contributions/779-delegation-results-intervention/traceability.md)。


## R792：当前步骤的流程上下文

来源：[Issue #792](https://github.com/castbox/guru-trellis/issues/792)。本节增加原生命周期的发现与加载能力，保持上文全部阶段、mandatory Skill、typed exit、唯一consumer和原AI语义owner。

**R792-01 / BEH792-AUTHORITY**：全局顺序、显式调用与路由只有一个长期workflow authority；复用既有标记和各Skill consumer合同提供确定性投影，不维护第二图、长期位置缓存或wrapper Skill。

**R792-02 / BEH792-QUERY**：AI持有一个合法原出口后，一次公开查询取得唯一consumer、必要入口与前置合同。unknown、multiple、unmapped和matching漂移停止。脚本不解释条件router或判断前置充分性、scope、pass和route intent；AI按原owner完整合同继续。

**R792-03 / BEH792-LOAD**：正常入口取得当前阶段/步骤所需内容及适用全局约束，不要求无关全量router/stop或历史详情。原native phase/step与唯一continuation的结构接口保持，原producer恢复和接收会话职责保持；查询成功或phase不能产生语义通过。

**R792-04 / BEH792-LEGACY**：正常流程只识别旧状态并转交原维护owner。实际入口加载其家族、转换、控制退役、历史恢复和准确来源；不按版本号截断、不批量转换/退役Task、不改历史归档、不重做#712/#64。

**R792-05 / BEH792-ADOPTION**：查询说明真实前置、最小输入、直接输出消费和普通错误恢复。改变的公共命令及受影响canonical/dogfood/声明平台沿原owner成套迁移，保留受支持在途工作。正常新runtime直接采用受管reference；verifier原旧before只读观察不赋当前执行资格。source、installed、实际AI和外部效果分别证明，不以文件缩短、关键词或固定降幅验收；完整多平台安装/升级/Release矩阵不属于本项。

职责D792-01..04、场景T792-01..06位于同名三层单元。本节不改变#793 qualifier触发，不合并身份查询或#794 Check/Review，不承接#734。当前观察由[#792 Test](../../requirements-design-test-contributions/792-step-context/test.md)定位。

## R794：合并审核、真实消费者与迁移

来源为 [Issue #794](https://github.com/castbox/guru-trellis/issues/794) 全文，固定前驱Git `4d565c97b5abf634d76ede2d18eed0a57f13bb76` 的本单元。

- **R794-01 / BEH794-INTEGRATE**：工程自检及原知识完整整合/readback在TaskCommit前完成；无独立candidate/final Check循环，整合事实不宣称独立通过。
- **R794-02 / BEH794-INDEPENDENT**：新独立 reviewer在固定committed B..H完成一次Architecture before/after、原九维与全部Branch Review；冻结候选，修复回原writer后继提交。
- **R794-03 / BEH794-RESULTS**：原Review同时拥有check/full_review，真实通过后顺序记录两个必要公共结果；缺槽/旧pass/历史PR不能代替当前充分性。
- **R794-04 / BEH794-COVERAGE**：原reviewer仍独立时可接续；原覆盖/工程事实按适用性采用，所有真实差额、base组合/冲突和受影响未改consumer覆盖；无法界定或覆盖丢失时补足完整审核，caller不缩B。
- **R794-05 / BEH794-PUBLISH**：通过前无新push/PR；后仍由原Delivery Review/readiness和Publication判断载荷、实际交付、剩余责任及未验证范围，终态不合并。
- **R794-06 / BEH794-RECOVERY**：匹配新公共版本/消费者和原provider边界显式切换；旧Check/已提交/旧Draft实际阶段及已发生动作准确恢复，不重复副作用、不改名旧pass；pending远端动作回当前审核/readiness。
- **R794-07 / BEH794-ADOPTION**：canonical、packages/runtime/schema、spec、workflow/routing及实际受影响平台沿原owner成套采用，保Task/session/用户内容和sidecar；定向验证分清组件、实际Agent、安装及外部效果，不扩完整Release矩阵。

R531/R530/R600/R636/R637/R638/R710/R711/R713 的未替代条件、source身份、固定B、原single-writer、完整结果消费/恢复和历史观察保持。当前精确输入/出口/命令与薄投影由原canonical packages独占，迁移由MIGRATION-794定位；设计D794、测试T794在对应完整单元承接。


## R815：受管 manifest 冲突恢复

来源为 [Issue #815](https://github.com/castbox/guru-trellis/issues/815)，完整前驱为 Git `cb8b4ce349b54cd832ff5b8f72602c5a721ce875` 的本单元。

- **R815-01 / BEH815-PREIMAGE**：正常两分支 canonical 及各自 installer 输出发生 managed manifest 冲突时，原 Reconcile/Git 冲突步骤固定 prior H 中已生成的完整旧 manifest blob，临时恢复工作文件供原 tools inventory 读取。原 provenance/hash 保持，临时前像不得作为最终候选。
- **R815-02 / BEH815-COMBINATION**：原 tools owner 对组合 canonical 的实际受管差异逐路径 preserve/replace，由原 installer 生成最终 manifest 和投影；经目标 installed/native/drift、sidecar/mode 验证后，原 resolved 路径核最终树、父序及零 unmerged。
- **R815-03 / BEH815-CONTINUITY**：保持同 Task/Delivery、branch、checkout、PR，以及原 resolved 的当前 Task 自然 dirty metadata 例外。保留无关 Task/session/peer；失败和未知 mutation 沿原输入、frozen plan 与事务恢复，不重放。
- **R815-04 / BEH815-RETIREMENT**：同 PR 后继 action 通过原 Publication `retire_completed` 核验并退役已完成私有事务，公共发布事实保持。未知或未完成动作先恢复原操作，不手删事务或构造新的 pass。
- **R815-05 / BEH815-ADOPTION**：原 public I/O、语义门禁和 owner 不变，完整 matching source 经原工具 owner 同步并验证实际目标。开发 local_candidate 保留正式 source-lock 未验证边界；clean committed H 的正式 source_locked 采用是后继原操作。本项独立交付及 Task 终态责任保持，不绑定发布版本。

精确接续步骤归原 canonical packages；职责 D815、场景 T815 位于同名完整单元。证据及窄增加范围见 [#815 追踪](../../requirements-design-test-contributions/815-manifest-conflict-recovery/traceability.md)。本节不引入通用恢复框架、授权存储、审计 ledger 或完整矩阵；前文未替代条件保持。
