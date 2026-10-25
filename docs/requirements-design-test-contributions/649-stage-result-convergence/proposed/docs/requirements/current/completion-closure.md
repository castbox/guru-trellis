# 整体 Completion、Closure 与终态收尾

本次晋升的完整前驱：Git `7a7b60743499653ffeb81f6b31e627a02c33f579:docs/requirements/current/completion-closure.md`。贡献与窄替代边界见 [#635 追踪](../../requirements-design-test-contributions/635-portable-lifecycle/traceability.md)。
知识单元：`RDT-REQ-COMPLETION`。状态：`current`。前驱为 RDT `.109` 的有效终态能力；固定迁移源 Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。当前定义适用于已迁移范围；旧 Task 保持其阶段适用来源。

## Completion 判断整个 accepted scope

`R436-01`、`R454-D436-01`、`R531-06 / BEH531-COMPLETION` 保持身份。原 `guru-review-task-completion` 读取当前 Task/generation、整体 accepted scope、各 generation 的实际 Delivery facts、必要规划正文和条件、当前 authority、剩余工作与证据。Delivery 全终态或一个 full slice 合并都不证明整体完成：未分配 scope、改变的验收和必要因果证据仍须判断。它实际读取 Author planning-body 与四类模板，在原职责内判断全量、部分、后续交付和历史接受的关系，不代写规划。

Completion 可以在当前没有 Delivery 时处理证据补充或 Reactivate validation。不能为纯证据/收尾建立空 Delivery，不能复用旧 merge DTO 冒充当前批准。相同结果输出丢失恢复原 result；只有完整语义 `completed` 才调用公共 complete_task 并交 Closure。公共记录不是新的语义证明。

仍缺已接受工作时使用 `remaining_work`；需要修改需求 authority 时用 `requirements_revision_required`；实施修订或新的业务切片分别用 `implementation_revision_required`、`additional_delivery_required`。必要效果证据尚缺时用 `evidence_pending`；具体缺失 authority/dependency 或无法形成可靠判断才用 `blocked`。这些结果保留同 Task 活动，不归档，不把普通 pending 当 blocked。

`evidence_pending` 只交原 evidence_refresh。没有新证据就等待已明确的获取条件；新证据到达后重读当前整体 scope 和全部相关 Delivery facts，再作当前判断。refresh 保留 Task identity，不要求 current Delivery，不恢复历史 completed。当新工作是实际实施而非补证时，进入 genuine same/new Delivery。

## 证据层次、目标与因果结论

`R383-02/06/07/08` 保持；共同语义唯一正文是 [causal-completion-semantics](../../../trellis/presets/guru-team/spec/workflow/causal-completion-semantics.md)，不另立因果状态机。Completion 从 accepted scope 区分普通 feature、diagnosis、mitigation、implementation-only repair、production root-cause repair 及混合目标。

普通 feature 满足其 RDT 范围即可，不强加生产证明或 incident 问卷。diagnosis/mitigation 可以在本身要求与证据满足时完成，同时诚实保留未知原因、期限/退出和残余风险；若 diagnosis 要求找出原因，原因未知仍是工作未完。implementation-only repair 可以在 code/test 范围完成并说明 production effect unverified；这些结论不能关闭仍要求 production/root-cause closure 的 source 或 parent。

只有 accepted scope 要求生产根因修复时，才按原失败的关键输入条件、状态、处理路径、运行条件与结果判断 same-input 或有充分理由的严格等价生产证据。样本数相同、错误率降低、绿色测试、merge/deploy/smoke/fallback 本身不足以证明根因消除。必须区分诊断、实现、静态、集成、外部、生产效果、根因、缓解和剩余风险；错误改名、延后、转移到别的阶段/owner、排除合法输入不能冒充修复。

不强迫危险重放一次性输入，也不自动申请生产访问。合法取得且适用的既有/等价证据可以充分；不充分时保留具体缺口、现有 acquisition owner 和 refresh 条件。同一 accepted goal 的当前资格/机制未变时复用仍适用判断；语义或因果条件改变回原资格 owner。脚本、fixture 或工作流认知测试不能证明业务生产效果。

## 真实交付、历史与补证

`BEH-557-02/03`、`BEH567-06`、`BEH569-09` 保持。人工合入由原 Merge 正式记录后，Completion 分别读实际 Delivery head 与原 Publication，比较 published-to-actual 和完整 PR 差额（包括原候选以外路径）、当前 accepted authority、实际 CI/reviews 和必要证据。原 head 的旧门禁不证明实际 head 已审。仍适用或等价的证据可用；变化回受影响原 owners。pending/cancelled/missing/failed 保持真实状态；非必要 CI 不扩大 accepted scope。不能要求另一 merge 或从已合并推导 completed。

当前公共 facts 已充分时，不将 history discovery 设为新前置。需要历史时由原 Merge query1/query2 执行有界准备/扫描，明确 result 的 task identity、repo、base、cutoff 和 deliveries。cutoff 只证明其覆盖；后续无关提交不触发重新查询或同步。已知同 Task 新 Delivery 或必要证据变化时，只补缺失事实并重判受影响结论；旧 cutoff 不证明未知后续完整。查询失败和合法空结果分明，bookkeeping 不是 business Delivery。

Completion 消费原 Architecture `task_impact_sync(stage=acceptance_finish)` 当前 eligibility；不重标 Branch DTO、不因 caller 更换重复同 assessment，也不重新晋升已接受贡献。变化、缺 committed review/promotion 回原 owner。必要长期 authority 更新或不适用依据必须实际检查。

## Closure 处置源 Issue

`R436-02`、`R454-D436-02`、`R547-01..08 / BEH547-*` 保持。原 `guru-complete-task-closure` 只消费当前 Task/generation/accepted scope 的 Completion completed ResultRef，重读来源关系、scope、target、binding、content/evidence 和精确 action set。Task 完成与来源 Issue 剩余责任分别判断。

`exact_source` 只表示资格，并不要求关闭。当前 Task scope 完成但源 Issue 保留显式责任时，用 `retain_open`，保持相同 TaskId/generation/source；不改成 reference_only/no_issue 以换取归档。其动作要求 provider OPEN，无 close；纯 retain 返回 `no_mutation`，public source_result=null。no-Issue 使用空动作；reference_only/follow_up/parent 无 close authority，不因链接增加关闭目标。

合法 `close` 要求当前已审查的精确动作和对话副作用边界，实际完成后必须观察 CLOSED；`already_closed_at_review` 观察 CLOSED 且零重复 close；`retain_open` 观察 OPEN；非 exact relation 的 `no_close_authority` 保持其无关闭语义。exact_source 不能对自身使用 no_close_authority；非 exact source 不能借 close/retain 动作升级资格。存在额外 Issue 时逐项审核原多 Issue action set 的真实资格。

Closure 冻结同一事务的最小恢复输入，授权从不持久化。blocked review 保留原理由，不创建新事务或执行 provider mutation。输出丢失、公共投影失败恢复同一事务，不能再次关闭已关闭 Issue。来源/scope/action authority 改变、应 CLOSED 被 reopen 或应 OPEN 被关闭，返回 external_change_conflict，交原 Closure fresh review；不能由 Finish 擅自 close/reopen。aggregate closed 仅表示动作集含 close/already-closed，不代表每个 Issue 或 exact source 已关闭；源 retain 即使别的动作 close 仍不投影 source_closed。

## Finish 与 Cleanup

`R436-03/04`、`R454-D436-03/04` 保持。原 Finish 只消费当前 Closure ResultRef，从原只读 API 读取冻结 action set，比较当前 source 并重读每个必要 OPEN/CLOSED 状态。漂移返回 closure_refresh_required，不由 Finish 另选 disposition。缺原结果 reader 就在终态写入前停止。

Finish 独占 archive projection、bookkeeping commit/push/PR 和 expected-head merge，各真实副作用沿当前对话边界。它保存整个 scope、Delivery planning/history 和未验证边界，保持 schema-2 aggregate 字节语义，不写 retired status/completedAt/commit/pr_url/archive_dir。归档前只退休 exact Task/generation session pointers。仅归档投影且尚未进入目标历史时，恢复唯一原 Finish 事务；共享 Finish 已成立而本机 seal pending 不阻止 Reactivate。

bookkeeping 不是业务 Delivery，无 Issue-closing keyword，无新旧 Delivery trailers，不递归触发 Completion。Finish 不要求 Task 分支包含最新 target，也不重审已交付开发 gates；实际 archive merge 可达当前 target、唯一 archive 和 active copy 移除，才证明 terminal persistence。输出丢失复用原事务；无关后续 target 推进不使其失效。最终 seal 绑定 exact generation、Finish 结果和实际 bookkeeping head，target merge 另证明持久化。Finish 退休 binding，不删除资源。

正常 Cleanup 仅消费当前 ResourceSealRef 与 common-dir ledger，fresh 审查 exact owned refs/worktree/paths、内容、可达性和仍有 consumer 的状态，只处理已选 Guru-owned 资源。caller-owned/未知/别的 Task 资源保留。原 linked checkout 将被删除时，必须从保留 checkout 执行或进入明确 manual route。缺 terminal ownership 走 explicit manual selection；machine handoff 有独立入口。失败不撤回 Completion/Closure/Finish，不用旧 generation receipt 删除当前资源。Cleanup 实际结果与归档成功分开。

## Reactivate 和旧状态边界

`R434-03`、`R436-05`、`R454-D436-05` 保持。仅正常完成且 terminal 可唯一验证的 archive 可以 Reactivate。原 owner 读原 scope、实际历史 Deliveries、准确共享终态、恢复原因与当前开发选择；优先继续已存在后继，没有后继才保留 TaskId/source 严格增代，并重新建立当前环境的合法 session/branch/checkout binding。原 session、Finish/Cleanup 资源 authority 不复用，也不作为共享 Finish 证明；本机 seal/manual Cleanup 仅保留原资源责任。当前 active/archive 按公共模型保持唯一。

按源 Issue 查 archive 时，实际 committed source/finish summary/Git identity 共同定位；空旧 summary index 不能排除 exact source，未结构化 source 的命中仍只是候选，须原 source correction。正常 Reactivate、显式 legacy manual-archive 恢复和未完 Finish transaction 三者分路，不回填不存在的 Completion/Closure/Finish/seal。新 generation 仅需验证时可直接以新证据进入 Completion，不制造业务 Delivery。旧完整安装/旧 schema 转换归原 maintenance/migration owner，本单元不把 source 已修改当旧业务已恢复。

## 跨 clone 的 Closure 输入与共享终态

`R635-02/03/05 / BEH635-REACTIVATE/RECOVER/MIGRATION` 明确区分共享终态、本机资源责任与缺失必要输入。原 Closure 仅保存其跨 clone consumer 无法从公共结果重新推导的最小动作输入：原 ResultRef、Completion 关系、source 和精确 action set。载体随 Task 在明确 source ref/commit 可获取，并由公共 Closure evidence 关联。它不声明动作完成，不保存授权、原机 binding、工程记录或审查历史。

无私有交易时，原 Closure 可从该载体与公共记录核准确 Task/generation/scope、Completion/source、原 ResultRef 和每项 live provider 状态，只恢复同一已经满足的结果投影，零 provider close。真实动作尚未完成或 authority 漂移时回原 Closure 审查剩余行为；不能把载体变成授权或从 CLOSED 猜原归属。Finish 从原公共 evidence/authority reader 取得准确动作集合，再逐项核当前状态。历史无载体结果不补造原集合；确实缺原动作输入时报告其影响，已完成旧 archive 不追补新载体。

共享 Finish 由准确 archive commit 中的 TaskId/generation/source/scope、该版本 Completion→Closure/summary 关系、精确 bookkeeping PR/target、active 移除和 archive 一致性证明。archive 已进入所选目标历史后，目标后续前进或后继 active 出现不否定该历史；不要求 HEAD 等于旧 merge，不要求把 merge SHA 写回自身 archive，不递归创建 Finish PR。原机 seal、退出和 Cleanup pending 仅保留原机责任。

Reactivate 先读当前可获取后继。唯一合法后继继续其 generation；没有后继才由公共 writer 严格增代，保留 TaskId、source、规划和交付历史，不继承 gate 或创建空 Delivery。当前 Task2 使用公共 reopen 的真实 Completion 条件。受支持正式旧 schema1 固定兼容集包括 Guru `.3`、合法 id/顶层 generation/结构化 source/completed、summary2 和准确归档已合入目标；经 matching formal maintenance 一次收敛，不能补造旧 Completion/Closure/seal 或自动当人工归档。人工历史继续原 maintenance，未完成 closeout 回原 Finish；不扩任意旧格式。

新环境由原 Establish→Ensure→Bind 恢复自己的合法资源，不能清理 A 或另一 Task。再次工作按实际进入新 Delivery 或无 Delivery 的 evidence-refresh，再独立 Completion/Closure/Finish。至少一个独立 clone 原生样本分别证明两条再次完成链；fixture、source 或安装通过不替代它。

## 关系和来源

前序：[生命周期](task-delivery-lifecycle.md)。设计：[`RDT-DES-COMPLETION`](../../design/current/completion-closure.md)。测试：[`RDT-TST-COMPLETION`](../../test/current/completion-closure.md)。[迁移追踪](../../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md) 保留各旧 identity 与替代范围。公共 DTO/profile/exit 的精确规格在 [Completion](../../../trellis/skills/guru-team/packages/guru-review-task-completion/SKILL.md)、[Closure](../../../trellis/skills/guru-team/packages/guru-complete-task-closure/SKILL.md)、[Finish](../../../trellis/skills/guru-team/packages/guru-finish-task/SKILL.md)、[Cleanup](../../../trellis/skills/guru-team/packages/guru-cleanup-task-resources/SKILL.md)、[Reactivate](../../../trellis/skills/guru-team/packages/guru-reactivate-task/SKILL.md) 各原 owner；本能力正文不复制接口或共同因果规范。

## R649：阶段成果维度与缺口分类

**R649-04 / BEH649-DIMENSIONS**：原 Delivery Review 和 Completion 按实际对象、能力、operation、环境及声明，分别判断合同 authority、源码实现、制品部署／入口可达、初始化／启用、消费者采用和原业务请求 E2E。每项使用实际证据，或说明不适用的对象及理由；不新增统一证据字段或表格门禁。合同合入、源码存在、部署成功均不推出其余维度。未启用只阻断实际依赖该状态的启用、采用、验收或完成声明，不否定已独立成立的合同、源码及部署。

**R649-05 / BEH649-GAP**：Completion 先确定未满足的 requirement、能力和 operation，再区分四类责任。必要消费者或代码未实现，回原实施／真实后续 Delivery；有效要求已确定而方案自加无依据前置，回原 Author／Architecture 修订机制；来源或 accepted scope 真正冲突，回原 Clarify；有有效要求且必要的外部证据尚未取得，沿原 evidence_refresh，说明缺口、原获取 owner 和恢复条件。无关未知仅保留边界，范围满足时可以合法完成。以上行为消费既有出口，不增加新 disposition 或状态。

**R649-06 / BEH649-CUTOFF**：结果正文限定观察候选、已执行检查及截止点。正文之后才发生的正式 Check、Review、Delivery、Completion 或 Git／PR 事实，由其原公开结果和准确引用承接；正文不追写自己的最终 pass 或 HEAD。确需修正文档时，由原 writer 在合法候选边界修改，纳入受影响 Check／Review，不因“补结果”豁免。Closure／Finish 仍只处置终态、归档及 bookkeeping，不接管共享文档；不为追记完成制造空 Delivery 或额外提交。
