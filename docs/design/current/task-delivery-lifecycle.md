# Task / Delivery 生命周期设计

本次晋升的完整前驱：Git `7a7b60743499653ffeb81f6b31e627a02c33f579:docs/design/current/task-delivery-lifecycle.md`。贡献与窄替代边界见 [#635 追踪](../../requirements-design-test-contributions/635-portable-lifecycle/traceability.md)。
知识单元：`RDT-DES-LIFECYCLE`。状态：`current`。authority identity：`guru-trellis-rdt`；精确内容由完整Git revision与locator定位；晋升前完整定义为 immutable Git `39169628f5f79cb48673eae96a36670e73f4dbbb:docs/design/current/task-delivery-lifecycle.md`（RDT `.113`），更早迁移来源和稳定身份保留。需求：[RDT-REQ-LIFECYCLE](../../requirements/current/task-delivery-lifecycle.md)；测试：[RDT-TST-LIFECYCLE](../../test/current/task-delivery-lifecycle.md)。本单元定义能力职责与协作，不定义第二套公共 state/schema。

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

## Scope、内容边界与恢复

`D531-03`：Clarify 先确认整个 authority 变化，实际当前 stage owner 使用公共 rework/stop，保留 DeliveryKey/candidate/commit/PR/history 并交同 Author。planning/checking/reviewing/publishing 的回程使用实际受影响 owner；reviewing/publishing 不能只按 phase 猜 interrupted step。实施阶段由原 coordinator 通过公共 scope revision 接口承接，不加新 Skill/state owner。全部撤回 stop/release 后进入 whole Completion，绝不投影 delivered。原 provider 只负责自己的缺口；独立 consumer 工作继续。

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

## 完整规格与未迁移边界

精确公共 I/O、阶段 profile、typed exit/consumer、hash/HEAD关系、private恢复输入由 [canonical packages](../../../trellis/skills/guru-team/packages) 与 [workflow](../../../trellis/workflows/guru-team/workflow.md) 单写。本迁移不展开 Git对象摘要算法、provider实现、完整升级迁移矩阵/软件 Release 等专属能力，也不以历史test结果证明当前candidate。它们仍由 [legacy inventory](README.md) 指向原authority。
