# Task / Delivery 生命周期设计

知识单元：`RDT-DES-LIFECYCLE`。状态：`current`。适用版本：`current-main-0.7.0-guru.114`；晋升前完整定义为 immutable Git `39169628f5f79cb48673eae96a36670e73f4dbbb:docs/design/current/task-delivery-lifecycle.md`（RDT `.113`），更早迁移来源和稳定身份保留。需求：[RDT-REQ-LIFECYCLE](../../requirements/current/task-delivery-lifecycle.md)；测试：[RDT-TST-LIFECYCLE](../../test/current/task-delivery-lifecycle.md)。本单元定义能力职责与协作，不定义第二套公共 state/schema。

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

`D636-04/05`：global workflow 只编排显式 stable skill 与唯一 typed consumer，step-local package 单写内部行为。原 Delivery Review 判断最终范围、载荷和分层验证；Merge重新核对非 Draft PR、实际 HEAD/body 与完整当前 gate链。Refs-only/Closure独占关闭、Task Completion 与 slice事实分工不变。一次性 matching 迁移经原 commit/publication owners 恢复实际在途状态和已执行动作，旧安装固定版本、新安装成套切换；无 current 双读或第二 phase/store；#637 后继候选行为由下文完整职责承接，#638 未来组合仍按实际交付顺序验证。

## 最终 Check、Commit、Review 与晋升

`D531-04`、`D600-01..03 / CON600-01..03`：Phase2 review 覆盖完整 tracked/untracked candidate 与 proposed authority targets，先比较 immutable before authority，再由原 owners 按 live expected-current 晋升并读回验证适用性。最终 Check 包含其实际差额；TaskCommit 包含最终内容；fresh committed Architecture 与 Branch Review 基于固定完整范围独立重算。原 [ADR-030](../../architecture/adr/030-promotion-before-final-check.md) 拥有时序后继决定，ADR-028 保留版本适用性与内容/集成分离。

Check、TaskCommit、Branch Review 各保留 semantic Gate。Check 的 pass 不等于 commit；clean 现有候选从原公共事实导出当前 Review 输入，不新 commit。dirty exact stage/commit 后以实际新 H 进入完整 Review。finding-fix、fresh-final 和 bounded continuity 保持各自 entry；旧 candidate 结果不能借路径相同当 current。零候选使用 [] 并保持真实完整审查，非空全 rejected 与零候选分别记录；两者均不自动通过。

`R578` 工程事实采用不转移 semantic owner：当前 reviewer先独立确定 check set，再审原命令的定义、依赖、预期、参数、工具链和环境是否适用。当前 judgment/result总是新作，合法事实适用则不机械重跑；缺失/未知/变化只补受影响检查。无新公共 reviewer字段、账本或退休checkpoint恢复。

## 候选适用性职责与正式结果

`D637-01..04 / CON637-01..04`：唯一共享规则位于 canonical workflow-contract 的 Candidate Applicability And Coverage。Architecture、Check、TaskCommit、Branch Review、Delivery Review、Publication、Merge 在原 step-local 职责中读取并执行；workflow/continuation/平台入口只路由，不复制判断。公共 Skill/profile/exit、GateResult、Task schema 和确定性 runtime 保持，不增加覆盖 DTO、reviewer 状态、第二 reader 或长期 cache。

原完整覆盖与 Hr..Hi 全部差额、真实冲突双方/组合语义及受影响未改 consumers 组成当前完整覆盖。当前 owner 自己建立范围、风险和检查集合，分别判断工程事实、当前语义和 Git/PR 事实。合法公开结果/原调用对象、Git/正文定位范围；原始命令结果另核定义/版本、输入/依赖、环境/工具链/参数/期望，不能以计划 ref 推断执行。证据不足补审或补跑命中项；组合影响不明完整审。当前 Check/full_review 仍绑定真实当前 candidate 和 predecessor，不将旧输出换标签。

独立性是未参与当前实现的实际职责；首次完整独立及原 Architecture first-read order 保留，合规 reviewer 后继可接续并依次承担 Architecture 和 Branch Review。finding 闭合与当前最终覆盖是两个实际判断，可以由同合规 reviewer 完成；保留 introduced_head/fix_head/closure_head 及原验证，matching 的 fresh_final_review 不再强制换人和相同全量重做。缺原通过覆盖或已消费私有状态时不补造 pass；实际公开来源不足则补真实工作。

原阶段用原 summary/evidence 或必要 owner-private 短期 checkpoint 承接结论；不跨读、不重建退休数据。Delivery Review/Publish/Merge 核自身 payload/Issue/candidate/live 资格并消费适用内容结论。真实 authority/scope/依赖改变回最早 owner；普通 HEAD/阶段/身份或无关 target 前进只触发适用性判断。MIGRATION-637 成套切换 matching workflow/preset/packages/consumers，先由原 producer 恢复已经发生的事务，再同 key 原阶段重判当前结果，零重复 mutation 或空提交。source/dogfood 编辑不代表活动 Task 已采用。

ADR-034 明确替代 ADR-019/029 及现行 finding 流程中无条件 fresh reviewer/相同完整重审片段；ADR-028 固定候选、ADR-030 晋升先于最终 Check、ADR-033 Draft 非最终结果与 #636 真实 Check predecessor 保留。实际 #636 matching 组合与 #638 未来未验证边界分别报告，原 RDT/Architecture single-writer 不变。

## Delivery Review / Publish / Merge

`D531-05`：Readiness 由原 Delivery Review 单写中文 PR payload、scope/验证/安全/部署与 Refs-only意图。最终 Ready Publication 仅 push/创建或恢复同事务 PR，expected-head Merge 仅合精确当前候选和真实 required checks。公共 projection记录实际远端事实，不把其 phase 当门禁。

原事务在远端已成功但输出/投影丢失时，先确认实际 identity与成功结果，复用同事务完成 projection，零重复 mutation。历史 published/merged结果保留，即使当前 gate stale；该事实不代替新的 Review。已正式关联的人工双亲 merge 由原 Merge recovery读真实 actual head、Publication relation、CI/delta后记录；不再 merge。Completion 再审actual-vs-published与whole scope；独立未完成CI不被合并事实变为pass。

## 完整规格与未迁移边界

精确公共 I/O、阶段 profile、typed exit/consumer、hash/HEAD关系、private恢复输入由 [canonical packages](../../../trellis/skills/guru-team/packages/) 与 [workflow](../../../trellis/workflows/guru-team/workflow.md) 单写。本迁移不展开 Git对象摘要算法、provider实现、完整升级迁移矩阵/软件 Release 等专属能力，也不以历史test结果证明当前candidate。它们仍由 [legacy inventory](./README.md) 指向原authority。
