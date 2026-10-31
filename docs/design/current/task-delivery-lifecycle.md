# Task / Delivery 生命周期设计

本次 #679 拟整合的完整前驱：Git `e6c3b8276d62ac174ab42cba5bca4d5784be2ca3:docs/design/current/task-delivery-lifecycle.md`。来源及窄补充见 [#679 追踪](../../requirements-design-test-contributions/679-session-continuation/traceability.md)。

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/design/current/task-delivery-lifecycle.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

并行 #663 晋升的完整前驱：Git `e9583202b67750d7b3ec2b7eab4b037c0c52a226:docs/design/current/task-delivery-lifecycle.md`；来源及窄修改见 [#663追踪](../../requirements-design-test-contributions/663-contract-continuity/traceability.md)。

更早晋升的完整前驱：Git `319202beab79c7666ecdb855291bf117e43d407e:docs/design/current/task-delivery-lifecycle.md`。贡献与窄替代边界见 [#657 追踪](../../requirements-design-test-contributions/657-workflow-continuation-conflicts/traceability.md)。
知识单元：`RDT-DES-LIFECYCLE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由完整Git revision与locator定位；较早历史完整定义为 immutable Git `39169628f5f79cb48673eae96a36670e73f4dbbb:docs/design/current/task-delivery-lifecycle.md`（RDT `.113`），更早迁移来源和稳定身份保留。需求：[RDT-REQ-LIFECYCLE](../../requirements/current/task-delivery-lifecycle.md)；测试：[RDT-TST-LIFECYCLE](../../test/current/task-delivery-lifecycle.md)。本单元定义能力职责与协作，不定义第二套公共 state/schema。

## 稳定设计身份

`DES-001/002/003` 继续拥有canonical/orchestration/AI-runtime分工；`DES-004/005` 继续拥有生命周期与tracked history/短期runtime边界；`CON-001/002` 保留公共兼容和semantic判断责任。下文按这些identity和D531后继展开，旧Task开发phase/Finalizer执行位置不再是当前入口。

## Authority、调用与数据责任

`D531-01/08`：上游 public Task schema 2.0、Delivery API 拥有身份、阶段、公共 Planning/Check/Review/Delivery/Completion facts。Guru `runtime/delivery_projection` 只封装明确公共操作与最小事实投影，不根据本地 phase 或 artifact 推导 semantic pass。TaskId 与 generation 标识整个 Task；DeliveryKey 在 Task/generation 内选定切片，planning_root 由公共 create 返回，不能由目录 inventory 或 caller 自造。

Global workflow 独占 mandatory Skill 调用、顺序、每个 typed exit 的唯一 consumer 和 fail-closed stop；每个 package Interface 独占公共输入/独立出口 schema。平台 prompt/launcher/hook 只加载和路由，不复制 step-local 行为。AI 审查 scope、source、风险、充分性、finding 与 route，runtime 只 executor/validator/最小 recorder。公共 output 是直接 consumer 的最小 DTO，不传 aggregate、完整证据、私有 digest、恢复 intent 或授权；相邻转换为薄、确定性 projection。

Source 关系与 Closure 意图分离：issue exact_source/reference_only/follow_up/parent 或 no_issue 由原 identity/Clarify owner 管理；切片 Publication 不修改来源资格。非 exact link 不创造 close authority。

## Creation 与 Author/Activation

`D531-02` 承接 `D292` 的唯一 writer 分工。Creation 从 Task 整体 accepted scope、历史切片与未分配范围判断本 slice，执行明确 create/select，仅分配稳定 Delivery 身份和 public planning_root。create/select 输出丢失由同 owner 以相同 operation/UUID 恢复；新的空切片不能掩盖旧身份。无 context 只在原明确 key 的合法公共校验条件下使用调用期关系，有 context 则必须符合实际 current，不用 fallback 隐藏 stale/冲突。

唯一 Author 写四种实际正文（Task PRD、Delivery PRD/design/implement）及本切片 manifests。`D154-01/02 / CON154-01/02` 拥有 source-sufficiency 调查、内容深度和来源承诺处置；详规由 [planning-body](../../../trellis/skills/guru-team/packages/guru-author-task-plan/references/planning-body.md) 及该 package templates 单写。RDT 当前正文不复制模板。每个承诺的 retain/refine/replace/defer/reject 处置在 design 唯一位置明确，技术展开不改变 source 目标。Policy/Docs Plan 同样只在 implement 唯一位置拥有。

Architecture 候选评估先于 Author 实质 solution；最终 Wording-current facts 之后的 final_plan 紧邻 Approval。Wording 和 Approval 只审各自语义，不写 Author 文档。Activation 独占公共 planning role，消费真实 approved DTO 的局部 freshness，调用公共 record_gate 产生新的 planning-accepted result。该 receipt 交 implementation/Check predecessor；Approval freshness 不成为公共 Gate result identity 或跨阶段 authority。

`D657-01/02 / CON657-ADMISSION/SELECTION`：初始 Task Creation checked created 只服务原创建区间；既有续接通过原身份/绑定/checkout owner 后，实际阶段 owner 承担写入资格。Delivery created wire 不变，原 workflow consumer 读取公共 current phase 和实际未完成义务后按唯一 continuation 进入原 owner；Planning 只有初始需求义务才进入 initial Author，已有工作恢复适用 Author/Wording/Architecture/Approval，当前 approved 进入 Activation。query 只提供客观可用性，scope/gate 充分性仍由原语义 owner判断；不新增 phase cache、router Skill、DTO 或状态 authority。初始创建精确 validator 不放宽。

## Scope、内容边界与恢复

`D531-03 / D657-03 / CON657-SCOPE`：Clarify pre-Author scope_ready2.0 先交 scope-only Author 根 PRD，Clarify acceptance 单写 accept_scope，再由 post-Author 含 task_key 结果交实际当前 stage owner 使用公共 rework/stop。两种 closed shapes 不互换，不使用旧 clear、private4/public1 或旧 Author profile；no_change 保留适用结果，无 Delivery 按真实义务显式 Creation/Completion。原 stage owner 保留 DeliveryKey/candidate/commit/PR/history 并交同 Author。planning/checking/reviewing/publishing 的回程使用实际受影响 owner；reviewing/publishing 不能只按 phase 猜 interrupted step。实施阶段由原 coordinator 通过公共 scope revision 接口承接，不加新 Skill/state owner。全部撤回 stop/release 后进入 whole Completion，绝不投影 delivered。原 provider 只负责自己的缺口；独立 consumer 工作继续。

固定内容由原 Author/implementation owner从真实 Delivery facts 构造 B，candidate 为完整 B..实际 H 加 dirty 内容。D2 从真实前序 delivery_result 取后继起点；同 Delivery 恢复保持 B。PR target 是集成目标，不代替 B。正式 [fixed development source](../../requirements-design-test-contributions/567-fixed-development-baseline/requirements.md) 与 ADR-028 窄替代旧默认追赶/祖先资格：普通各阶段零 Reconcile；真实触发进入原 owner 固定一次 target，保留其 ordinary/resolved/committed/continuity/同操作恢复。

每写批次由 read-only checkout boundary 核对 public identity、binding、Git 注册 worktree/cwd/branch。所有 editor 使用该 root 内明确路径；不 stage/覆盖无关 dirty，工作区位置不成为 Task identity。

## 早期提交与 Draft 反馈职责

`D636-01`：原 TaskCommit 拥有早期独立闭合输入、精确内容检查和真实提交；复用原 dirty 分类、中文消息、敏感检查、真实 hook/隔离事务与同提交 receipt。早期提交和 clean committed re-entry 不要求完整 Check，不写最终 gate；最终提交 profile 继续绑定真实 Check。只有原提交 owner 能把实际提交投影为早期候选 DTO，后者只交原 Publication，不作为正式 Branch Review seed。

`D636-02`：原 Publication 拥有同 PR 的早期 Draft 创建/更新、Ready 回退和最终 Ready。局部事务明确当前动作和终点；`ensure_draft` 在新未审 HEAD push 之前完成。同仓/base/head、唯一 Open PR、快进 lineage、元数据收敛和实际远端 readback 复用原 executor。Draft 终点不调用最终 record_publication；最终 Ready 仍消费当前 readiness 和原完整链。Ready 修订由其原 publication role 合法 rework 回 implementation，不能由别的 stage 冒用角色。恢复从原事务与实际 preimage/postimage 继续，不建第二 ledger，也不把历史成功当新候选通过。

`D636-03`：workflow 唯一反馈 consumer 固定 B/H，同时调度独立 Branch Review 早期完整内容分析与风险匹配验证。原 Review 新早期 profile 不读 Check 私有结论、不写 public full_review；最终正式 owner在真实 Check predecessor 下 fresh 判断和记录，不能自动从早期结果映射 passed。Check 仍拥有完整 scope 与最终判断；早期执行事实是否仍适用由当前原 owner审查，不新增跨阶段 review cache。HEAD H 与组合 T/M 是不同验证对象；冲突/无merge ref/CI未触发时保留 HEAD 支持入口和具体组合缺口。

`D636-04/05`：global workflow 只编排显式 stable skill 与唯一 typed consumer，step-local package 单写内部行为。原 Delivery Review 判断最终范围、载荷和分层验证；Merge重新核对非 Draft PR、实际 HEAD/body 与完整当前 gate链。Refs-only/Closure独占关闭、Task Completion 与 slice事实分工不变。一次性 matching 迁移经原 commit/publication owners 恢复实际在途状态和已执行动作，旧安装固定版本、新安装成套切换；无 current 双读或第二 phase/store；#637 后继候选行为由下文完整职责承接，#638组合由T638实际验证，不继承旧绿色。

## 最终 Check、Commit、Review 与晋升

`D531-04`、`D600-01..03 / CON600-01..03` 与 `D638-01..05`：原implementation拥有固定B/实际HEAD和全量paths的candidate/begin_check，原Check拥有完整候选质量判断及合法checking→implementing rework，原Architecture/RDT拥有实际final_integration写入。workflow只编排这些既有owners与typed exits，不新增Task phase/API操作/Skill。

先独立Architecture phase2比较immutable before与完整implementation/proposed targets，再原Check delivery_candidate_check完整审查。candidate_checked不调用public Check writer；其唯一consumer只能进入原两maintenance的最终整合。原owners一次固定实际目标、读取命中单元并合成完整有效条件；真实差额沿唯一候选适用合同补独立审核及受影响未改consumers，义务变化回相应原owner。随后写入、readback及适用性判断。

implementation用同B、实际HEAD和全部after差额重新candidate/begin_check。最终Architecture/Check验证新的content_ref，最终Check record_gate才进入reviewing。TaskCommit、独立committed Architecture/BranchReview覆盖真实最终内容；Ready/Finish仅no_change或真实reviewed_promoted。no-change仍走合法回程，不制造空贡献、ADR或commit。稳定knowledge identity与精确Git快照分开，ordinary promotion无需总入口必写/global successor；公共API版本继续真实版本化。

Check、TaskCommit、BranchReview各保留semantic Gate。clean候选从真实公共事实进入Review，无新commit；dirty精确提交后以实际H进入完整Review。finding-fix、fresh-final和bounded continuity保留原entry，完整空集/全rejected均不自动passed。原工程事实按定义、依赖、预期、参数、工具链/环境采用，缺失/未知/变化补命中项；当前judgment/result实际新作，无新账本或退休checkpoint重建。

Arch非Planning5.0/Delivery3.0、RDT impact/promotion2.0、Check private6.0和直接consumers经MIGRATION-638成套迁移；Planning3.0/Delivery1.0、bootstrap/repair保持。未晋升、已晋升但未Review、已有Review分别由原owner重判或补缺，不转换旧pass、不重复完成写入。candidate输出丢失按实际phase/写入事实回原producer及implementation重绑，不直接改公共state。

## 候选适用性职责与正式结果

`D637-01..04 / CON637-01..04`：唯一共享规则位于 canonical workflow-contract 的 Candidate Applicability And Coverage。Architecture、Check、TaskCommit、Branch Review、Delivery Review、Publication、Merge 在原 step-local 职责中读取并执行；workflow/continuation/平台入口只路由，不复制判断。公共 Skill/profile/exit、GateResult、Task schema 和确定性 runtime 保持，不增加覆盖 DTO、reviewer 状态、第二 reader 或长期 cache。

原完整覆盖与 Hr..Hi 全部差额、真实冲突双方/组合语义及受影响未改 consumers 组成当前完整覆盖。当前 owner 自己建立范围、风险和检查集合，分别判断工程事实、当前语义和 Git/PR 事实。合法公开结果/原调用对象、Git/正文定位范围；原始命令结果另核定义/版本、输入/依赖、环境/工具链/参数/期望，不能以计划 ref 推断执行。证据不足补审或补跑命中项；组合影响不明完整审。当前 Check/full_review 仍绑定真实当前 candidate 和 predecessor，不将旧输出换标签。

独立性是未参与当前实现的实际职责；首次完整独立及原 Architecture first-read order 保留，合规 reviewer 后继可接续并依次承担 Architecture 和 Branch Review。finding 闭合与当前最终覆盖是两个实际判断，可以由同合规 reviewer 完成；保留 introduced_head/fix_head/closure_head 及原验证，matching 的 fresh_final_review 不再强制换人和相同全量重做。缺原通过覆盖或已消费私有状态时不补造 pass；实际公开来源不足则补真实工作。

原阶段用原 summary/evidence 或必要 owner-private 短期 checkpoint 承接结论；不跨读、不重建退休数据。Delivery Review/Publish/Merge 核自身 payload/Issue/candidate/live 资格并消费适用内容结论。真实 authority/scope/依赖改变回最早 owner；普通 HEAD/阶段/身份或无关 target 前进只触发适用性判断。MIGRATION-637 成套切换 matching workflow/preset/packages/consumers，先由原 producer 恢复已经发生的事务，再同 key 原阶段重判当前结果，零重复 mutation 或空提交。source/dogfood 编辑不代表活动 Task 已采用。

ADR-034 明确替代 ADR-019/029 及现行 finding 流程中无条件 fresh reviewer/相同完整重审片段；ADR-028 固定候选、ADR-030 晋升先于最终 Check、ADR-033 Draft 非最终结果与 #636 真实 Check predecessor 保留。实际#636/#637/#638 matching组合与其未验证边界分别报告，原 RDT/Architecture single-writer 不变。

## Delivery Review / Publish / Merge

`D531-05`：Readiness 由原 Delivery Review 单写中文 PR payload、scope/验证/安全/部署与 Refs-only意图。最终 Ready Publication 仅 push/创建或恢复同事务 PR，expected-head Merge 仅合精确当前候选和真实 required checks。公共 projection记录实际远端事实，不把其 phase 当门禁。

原事务在远端已成功但输出/投影丢失时，先确认实际 identity与成功结果，复用同事务完成 projection，零重复 mutation。历史 published/merged结果保留，即使当前 gate stale；该事实不代替新的 Review。已正式关联的人工双亲 merge 由原 Merge recovery读真实 actual head、Publication relation、CI/delta后记录；不再 merge。Completion 再审actual-vs-published与whole scope；独立未完成CI不被合并事实变为pass。

## 跨环境 source 与既有 PR 恢复

`D635-03/04/05 / CON635-PUBLICATION/ENVIRONMENT/DISTRIBUTION` 保留原 public Task/Delivery/session 模型和 step-local owners。Identity 从已选 repository、明确 source ref/commit 与公共 key 验证活动记录和必要代码；Establish/Ensure/Bind 只建立当前 common-dir 的合法 branch/worktree/session 关系。共享记录不携带原机路径或资源资格。原语义 owner 重判当前适用性，可核验工程命令按已有候选合同采用，不复制 gate pass 或要求无变化全链重跑。

Publish 的 `delivery_remote_draft_recovery` 与 `delivery_remote_ready_recovery` 各自使用闭合输入，显式选择已有 `pr_ref` 与承载 Task/Delivery/必要代码的 `source_commit`。source 未入 main 仍可合法；它与 candidate head 不同时，核完整历史关系和内容差额。PR 的 remote head ref 与本地 binding 分开，不用 B 的 branch 查找或新建第二 PR，不改 B 的 binding。

Draft recovery 读取精确 repository/base/head/key 与当前已审 payload，复用原 executor 补剩余 Draft、push 或 metadata。已完成部分只读回；新未审修订先按 #636 退 Draft。Ready recovery 核当前公共 candidate/readiness、reviewed head、payload 和实际 PR 状态；当前资格缺失返回原 Review/Check，不能从历史 Ready/phase 恢复 pass。确有剩余 Ready/metadata 动作时仍用原 writer。两个入口均不创建 PR，remote 更新仍受精确 full ref/expected-head 与当前动作边界约束。

MERGED 保留原 `delivery_merged_recovery`：公共 Publication 与真实 PR 双亲、actual head、target 历史相互关联后只补 Delivery fact，不再次 merge。Completion 独立判断 actual 差额、CI 和整体范围。Closure 的最小共享输入及正式 Finish 历史由终态单元定义；它们不成为 Publication 的第二状态模型。

local branch/worktree/runtime 责任限对应 common-dir；remote ref 是共享资源。Cleanup 继续核 generation、ownership、full ref/expected head，未知或推进后资源保留。旧 pending 不成为另一 Task 或不同合法新资源的准入条件；同资源未完责任不放松。matching source/native/Guru 完整迁移归原工具/安装 owner，public profiles 和直接 consumers 成套演进，不手写 dogfood 或 `.version` 绕过旧数据前置。

`D657-04 / CON657-DISTRIBUTION`：原 Discovery/Review/verifier 的当前可读前置与实际模型一致；身份/阶段严格性保留，退役字段/status/Finalizer 不成为准入。完整 matching consumer 修订由 MIGRATION-657 定位，历史固定旧资产不自动转换为当前结果。

## 完整规格与未迁移边界

精确公共 I/O、阶段 profile、typed exit/consumer、hash/HEAD关系、private恢复输入由 [canonical packages](../../../trellis/skills/guru-team/packages) 与 [workflow](../../../trellis/workflows/guru-team/workflow.md) 单写。本迁移不展开 Git对象摘要算法、provider实现、完整升级迁移矩阵/软件 Release 等专属能力，也不以历史test结果证明当前candidate。它们仍由 [legacy inventory](README.md) 指向原authority。

## D649：原规划、实施与检查职责

**D649-01 / CON649-LIMIT** 承接 R649-01。原 Author 的 planning-body、authoring、Delivery implement 模板及既有示例拥有五项阶段限制写作方法。Policy 定义本批及后继责任，Docs Plan 定位当前规范、指南及派生说明；global workflow 和平台入口不复制方法。

**D649-02 / CON649-CONVERGE** 承接 R649-02/03。实施 owner 修复行为及断言；原 RDT／Architecture owners 在各自知识边界准备完整 proposed 定义。原 Check 读取有效预期、实现、当前说明和真实 consumer，判断过期限制及错误断言；绿色命令不替代判断。Delivery Review 的阶段成果方法归其原 contract，整体维度和缺口路由归 [终态设计](completion-closure.md#d649阶段成果与原终态边界)。公共 API、profile、DTO、state、exit 和 recorder 不改变。

## 流程合同连续性职责

**D663-01 / CON663-REPAIR** 承接 R663-01：Bootstrap Interface 声明出口字段 rename 与 caller 自有上下文 authoring，repair schema/runtime核同 owner profile/continuation；workflow仅按既有回程调用。wire output不承载原 caller 已有的完整输入，不形成持久化 handoff。

**D663-02 / CON663-ARCHIVE** 承接 R663-02：Branch Review 正式 archived example 与其 closed schema 一致，原 recorder/checker/invoke 消费真实归档身份。archive/Completion/Closure/planning/range/PR snapshot和只读职责继续由原 owner核验，成功出口仍停止于原 disposition。

**D663-03 / CON663-BEFORE** 承接 R663-03：原 Architecture validator 在精确 before Git revision核既有三个 locator的存在或显式缺失，原 current/result消费者按 matching schema承接。完整固定B..H及当前新增文件仍由独立Architecture/Review判断，不用缺失事实推导当前文档充分性。具体字段与API以 Architecture canonical package及ADR-CONTRACT-CONTINUITY单写。

**D663-04 / CON663-MAINTENANCE** 承接 R663-04：final integration router仅将维护输入投影为原Bootstrap/repair可消费的phase2，原promotion上下文留在调用期；维护后重读真实authority/targets/candidate，回同一原promotion。维护出口不直接进入final Check，不新增业务状态、route record或第二writer。

**D663-05 / CON663-DISTRIBUTION** 承接 R663-05：canonical package是精确公共合同来源；测试执行public example/schema/projection/consumer组合，AI另核动态职责与正常路径。MIGRATION-663定位直接成套演进；source修改和投影一致不代表旧安装或业务已采用。

## D679：接收者前置事实与原 owner 接续

**D679-01 / CON679-RECEIVE** 承接 R679-01。普通执行的原 workflow created consumers、唯一 continuation 与 Planning 编排显式调用原 Identity/Ensure，然后按接收者自身事实进入原 Bind 和 Selection。五个 Planning Skills 在自己的 entry 中核相同前置；Architecture 在原 baseline-first 之后按 purpose 核接收事实；final_plan 按 D694-01 只读核对象，其他 purpose 保原恢复。workflow 只拥有跨 Skill 顺序，step-local Skills 仍拥有内部判断和写入。adapter.current 的有 context / 无 context 边界不变，不新增绑定 writer、wrapper、状态或全局映射。

**D679-02 / CON679-DIAGNOSTIC** 承接 R679-02。Author/Architecture 原 planning guard 按公共 kind、selected key、generation、phase、scope 顺序检查；更早的 resolve/API 首失败保原具体条件。外层 stale_identity/出口不变，session.task、session.delivery、delivery.phase、current.error/current.kind/current.key、delivery_key.lifecycle_generation 和 delivery.scope_ref.authority 定位实际条件。runtime 只报客观事实，不 bind/select 或决定语义 route。其余 Wording/Approval/Activation 保原 guard，由明确 caller 接续承担补缺与错误分流。

**D679-03 / CON679-PROJECTION** 承接 R679-03。原 Readiness recipe 从真实 Wording transition 投影 locator/mode/continuation，standalone 请求身份与 source 对齐，caller locator 保自己的合法值。normalization 保持；原 recorder 派生、checker receipt 和正式 invoke 唯一出口承接。原 native runner 从实际 public profile 选择提示，不替 Agent 构造身份、判断通过或修复 consumer。

**D679-04 / CON679-PRESENTATION** 承接 R679-04。Human artifacts 调用方提供真实 TaskRef/key；原 Approval package-owned resolver 继续解析精确切片。Task-only 直接检查精确根 PRD；archive 使用实际归档 ref/key。原命中测试执行文档 argv 并观察实际路径/缺文件/不创建与不选择，而非仅断言字符串。

上述变更不改公共 schema/typed exits/phase/helper 参数，不新增兼容双读或 Architecture authority。matching workflow、五 Planning packages、Readiness 与直接 consumers 成套采用，诊断迁移见 MIGRATION-679。历史归档不为工具安装转换；含旧数据的 checkout 沿原 tools-only owner维护工具，普通preset检查继续严格。RDT 完整拟写先经候选 Check，再原 final_integration/readback 和最终质量链；source/package、installed、Agent 及外部采用分别证明。

## D694：Architecture 本地只读对象入口

**D694-01 / CON694-OBJECT** 承接 R694-01。原 Architecture package invoke 的 Planning 本地 helper 使用已有 planning_purpose，只对 final_plan 读取真实 current 后复用原显式 Task/C4/checkout、public relationship/profile 校验。no_current_task、匹配 Task 的 no_current_delivery 及匹配 current 可核对象；不同 key、terminal、error 保原处理。原非终态 planning、scope/root/design freshness 及 owner-result 校验继续执行。共享 DeliveryProjection.current(key) 和 official session/selection writers 不变，不新增持久状态、wrapper、public field/profile 或全局 fallback。

**D694-02 / CON694-ROUTE** 承接 R694-02。workflow 只路由一次性 final_plan 到原 Architecture Skill，Skill 独占 authority-first、对象校验、独立判断和无写入边界。其实际 output 沿 Interface 当前 aggregate、Delivery planning branch、direct current projection 到 current router，再按 purpose 投影相邻 Approval 当前输入。Approval 自身 guard 保持。其他出口回原 consumer，普通恢复仍由原 Identity/Ensure/Bind/Selection 写必要 runtime。matching workflow/package/preset 成套采用，无数据迁移；理由及取舍由 [ADR-EXPLICIT-REVIEW-OBJECT](../../architecture/adr/explicit-review-object.md) 拥有。

本差额窄修订 D679-01，保留其他原职责和错误合同。候选完整拟写先 Check，再原 owner final_integration/readback；最终候选重绑、Check 和 committed Review 覆盖实际内容。
