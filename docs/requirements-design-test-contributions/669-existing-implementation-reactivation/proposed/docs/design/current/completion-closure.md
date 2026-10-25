# Completion、Closure 与终态责任设计

本次 #649 最终整合的完整前驱：Git `4fea68613de4181d7cb55532b8758515472ba31b:docs/design/current/completion-closure.md`。贡献、#657 继承及原来源见 [#649 追踪](../../requirements-design-test-contributions/649-stage-result-convergence/traceability.md)。

更早晋升的完整前驱：Git `7a7b60743499653ffeb81f6b31e627a02c33f579:docs/design/current/completion-closure.md`。贡献与窄替代边界见 [#635 追踪](../../requirements-design-test-contributions/635-portable-lifecycle/traceability.md)。
知识单元：`RDT-DES-COMPLETION`。状态：`current`。固定前驱 RDT `.109` / Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。需求：[RDT-REQ-COMPLETION](../../requirements/current/completion-closure.md)；测试：[RDT-TST-COMPLETION](../../test/current/completion-closure.md)。稳定 `D531-06`、`D454-D436-01..05` 与 `D547` 关系保持，公共接口以各原 package 为准。

## 稳定设计身份

`DES-005/009` 保留Task历史/归档/精确资源关系。旧workspace mapping及Finalizer负责整段closeout的片段，由D531-06/D454-D436与现行官方公共Task/session、Closure/Finish/Cleanup职责窄替代，历史不改写。`DES-008` 的证据分层边界保持。

## Completion application owner

原 `guru-review-task-completion` 拥有 whole-task causal judgment。输入为 public Task identity、accepted scope、实际跨 generations Delivery/evidence facts、适用 RDT/Architecture 与当前 source；不是某次 merge 的摘要。delivery_completion、delivery_evidence_refresh、delivery_reactivation_validation 分别承接合并/撤回后的完整判断、已知证据获取条件满足后的重判、合法新 generation 的验证。后两者不要求 current Delivery；Reactivate 消费实际 archive anchor，不制造新 business slice。

Completion 实际加载四类 planning正文合同，读全 Task requirements 和适用 Delivery bodies、必要关系/条件及历史结果。它区分当前要求与旧 Delivery 当时接受范围。current evidence/fact身份属于调用期判断绑定；公共 complete_task只记录已判断结论，不是语义判定器。

只有 `completed` 的现有最小 ResultRef 交 Closure。remaining_work、requirements_revision_required、implementation_revision_required、additional_delivery_required、evidence_pending、blocked 使用各自唯一 consumer；原因只说明真实缺口与路线。evidence_pending只回原 evidence_refresh，未有新证据不制造re-entry循环；实际代码遗漏不是纯pending。whole scope变更由Clarify，新的独立slice由Creation，当前修订回最早原owner。

## Evidence authority 与实际内容

原 [causal common spec](../../../trellis/presets/guru-team/spec/workflow/causal-completion-semantics.md) 唯一拥有证据维度和semantic dispositions。Completion按accepted目标选择适用证明，不新增统一生产门槛、证据字段表、因果账本或审批。source/parent仍要求production/root-cause闭环时，诊断/缓解/implementation-only Task 可完成自己的scope但不能以此关闭source。严格等价证据由AI比较真实原故障条件；合法既有证据可用，不安全重放不强迫，缺口保留原 acquisition owner/condition。

原 Merge recovery的terminal fact仅声明actual content/head，不是新gate。Completion独立比较原Publication→actual head、完整PR差额、accepted scope、真实CI/reviews及必要效果证据。旧gate适用性仅覆盖原candidate；新增路径不能藏在原candidate范围外。公开MERGED可可靠同时CI pending/failed，二者分开。不相关CI不添scope；scope-required gap回原owner或evidence_pending，不重复merge。

原 Merge history query拥有有界Git准备和cutoff：caller不fetch、不整合Task，不按远端最新SHA作资格。actual public facts充分就不调用；需要时消费公开result3.0及显式query context，补已知缺失同Task事实，不让bookkeeping进入business lineage。结果丢失由原query产生明确新cutoff，不能猜前次截点。

Architecture acceptance_finish是原owner新作当前eligibility；still-applicable独立conclusion与工程事实可用，不把Branch DTO重标为该结果。缺committed review/promotion或真实变化沿原路线；Completion另审whole scope。

## Closure source disposition owner

`guru-complete-task-closure`只接受当前Completion completed ResultRef。它从真实source relation、scope、target、binding和evidence形成精确action set；exact_source eligibility与close意图分离。每个action只作用本次明确Issue，不沿Related/Coordination/Follow-up链扩张。

`retain_open`是正常exact_source处置，源scope仍有显式责任时保留同身份，要求provider OPEN，零close，public source_result=null。no_issue空集和非exact no_close_authority不变；source角色不为Finish改写。close/already_closed_at_review要求CLOSED，其中后者不mutation；aggregate closed仅反映动作集中有closing action。混合集的source retain与另Issue close分别投影，不能由aggregate推断source_closed。

AI先review完整动作集及其真实副作用边界，executor再冻结最小原事务输入、重读provider状态、执行明确close和公共projection。blocked先返回，不创建transaction或provider mutation。loststdout/投影失败用TransactionRef恢复原动作；实际已closed不重close。authority或requiredOPEN/CLOSED状态漂移回external_change_conflict。授权和过程不进任何状态。

## Finish terminal persistence owner

`guru-finish-task`只消费Closure ResultRef，通过共享只读API读exact action set，检查当前source与每个应OPEN/CLOSED状态。不能接受caller另带一个不绑定的动作列表，也不能close/reopen源。漂移回Closure。archive projection、本地/远端bookkeeping、expected-head merge三项实际mutation分别保留其原语义边界。

归档包含Task整体scope、所有Delivery规划及历史、证据限制；schema-2 public aggregate的status/completedAt/commit/pr_url等retired字段不写。原Fixed Fork session API仅退休exact Task/generation pointers。archive locator由finish-summary拥有。只有投影、尚未证明归档进入target时恢复同Finish transaction，不以archive存在冒充Reactivate；共享Finish已成立不再要求原机seal完成。

bookkeeping使用不带Issue closing关键字及business Delivery trailers的已审载荷，不产生Delivery fact，不递归Completion。local commit head与target merge commit分开：前者绑定资源seal的实际cleanup refs，后者证明archive已存在remote target且active copy已移除。普通后继target提交不使已证明可达的merge失效，也不要求Task追赶target或重跑business gates。正常原事务恢复不重复archive/PR/merge；缺terminal ownership发manual_cleanup_required，不虚构资源ledger。

## Cleanup 与 Reactivate owner

Cleanup消费exact当前ResourceSealRef/common-dir ledger，fresh检查所有选中ref/path、未提交内容、commit reachability、ownership及consumer；保留未知/caller-owned/peer资源。它删除资源，不撤销Completion/Closure/Finish。执行checkout位于删除目标内时转保留checkout或manual selection，禁止把自己删掉后虚报清理成功。machine-handoff和显式manual selection有各自输入，不借其它receipt。

Reactivate只接可唯一验证的共享Finish终态；先复用实际后继，无后继才严格递增generation保留TaskId/source，重建当前binding/session与唯一active副本。源Issue检索读committed源/Git archive事实，summary索引不足不排除真实命中；unstructured来源要原source correction。手工历史归档由legacy owner负责；未完Finish事务由Finish恢复，不伪造终态。原机manual Finish/Cleanup receipt只归对应本机资源owner，不作为共享终态准入。验证-only新generation直接走Completion，历史Finish/Cleanup/session都不是当前authority。

## 最小共享 Closure 载体与恢复

`D635-01/02 / CON635-SHARED-FINISH/CLOSURE` 窄替代本机 receipt 参与共享终态资格的片段。原 Closure 在精确动作集语义审查后、provider 动作前，按同一冻结输入生成原 ResultRef 和 `closeout/closure/<safe-result-id>.json`。文件名仅将 result_id 的 UTF-8 作无 padding base64url 编码。独立 `guru-closure-shared-result-1.0` 只含 schema_version、result_ref、completion_result_id、source、action_set；没有 terminal、授权、path/binding、gate 或扫描历史字段。

原 public `close_task` evidence 关联载体 AuthorityRef。`read_terminal_closure_result` 从公共 Closure evidence 经既有 authority resolver 读取并核对 Task/generation、ResultRef、Completion/scope/source 与动作集合，继续给 Finish 原 snapshot2.0。terminal 由实际动作类型和公共结果核一致，carrier 不自行证明完成；Finish 保持逐 Issue live 核验。载体随 Task archive，历史路径沿原 artifact_origin 解释，新结果使用独立文件，现有结果不覆盖，无额外索引。

闭合 `closure_shared_result_recovery` 接受精确 TaskRef/ResultRef/载体 AuthorityRef。公共结果存在时核同一结果读回；投影丢失时由原 AI 重新审查准确 Completion/source/actions 和 live 状态，才按原 result_id 补投影。该 profile 零 provider close，不从共享载体恢复授权。required CLOSED 仍 OPEN、required OPEN 已 CLOSED、source 或关联改变均回原 Closure；剩余真实 close 由原正常 profile 重新审查。旧无载体 archive 不制造输入，未发布或确实缺失的必要载体只阻塞它的真实 consumer。

Reactivate 原语义 owner 从准确 Git archive、该版本终态关系和精确 bookkeeping PR/target 判定共享 Finish，确定性 helper 只读取/校验事实。先检查当前可获取后继；正式 schema1 用 matching `inspectFormalArchiveReactivation`，无后继才同一正式公共 operation；Task2 使用原 public reopen。verified root 的同前驱 sibling 等代/较早快照不另建 incarnation，更新或冲突候选保留原诊断，不在 Guru 建第二 parser。applied 只用真实 key/ref 交原环境 owners；prepared/pending 不能声明 active。

共享 archive 已入 target 历史后，A 的本机 seal、binding 退出与 Cleanup 与 B 的共享准入分离。同一资源的真实责任冲突仍有效，B 不取得 A 的清理权。未进入 target 的唯一未完 closeout 才回原 Finish transaction，无法唯一恢复则报告具体必要输入。版本号、目录、status 或一个 MERGED PR 不代替完整资格。

## D669：已有实现恢复的原 owner 承接

**D669-01 / CON669-ENTRY** 对应 R669-01/02。原 Reactivate 新增独立 existing-implementation profile；旧 clean-base 输入不扩义。公开 input 只选择准确原生命周期、archive anchor 和原 PR；本 owner 的调用期 semantic 输入绑定审核后的 base、实际实现 HEAD、准确 acquisition 和本地内容。Interface 选择独立 schema/aggregate，迁移见 [MIGRATION-669](../../../trellis/presets/guru-team/MIGRATION-669.md)。外部退出保持原真实 key/ref/route，不传审查快照。

**D669-02 / CON669-CONTENT** 对应 R669-03/05。Git facts 提供逻辑 index entries 和 tracked/untracked 内容、类型、执行位；原 C3 在精确 HEAD/branch/注册仓库/任务预期下接受这一已审状态。raw index 的缓存刷新不成为内容漂移；原 capture/rebind consumers 保留原义。observer 只提供 Git/gh 客观事实，AI 仍判断来源、范围和充分性。摘要服务当前比较，不绑定授权或代替语义批准。

**D669-03 / CON669-RECOVERY** 对应 R669-04/06。先发现公共后继，无后继才由原 reopen/formal writer 增代；C4/C5/Bind 保持本机单写与 caller ownership。必要同操作交易将真实 base 与实现 HEAD 分开，合法 Task 写入前后分别比较；旧 transaction2.0 不重解释。输出丢失接续原实际结果，缺私有 receipt 不再创建 incarnation。PR repository/base/head 由 repo-bound gh 只读复核；恢复没有远端 mutation/Cleanup。

**D669-04 / CON669-VALIDATION** 对应 R669-07。一个代表完整安装中，driver 提供真实 Git/public 前驱及受控 provider，实际 AI owner 核全部语义前置并调用 installed 公开入口；安装、恢复、后续正式审核分别记录。完整多平台 Release 矩阵由其独立任务负责。架构完整职责仍由 ARCH-DOM-060/shared lifecycle 拥有，不增加第二 migration owner、allow_dirty policy 或审批账本。

## 原规格

[Completion](../../../trellis/skills/guru-team/packages/guru-review-task-completion/SKILL.md)、[Closure](../../../trellis/skills/guru-team/packages/guru-complete-task-closure/SKILL.md)、[Finish](../../../trellis/skills/guru-team/packages/guru-finish-task/SKILL.md)、[Cleanup](../../../trellis/skills/guru-team/packages/guru-cleanup-task-resources/SKILL.md)、[Reactivate](../../../trellis/skills/guru-team/packages/guru-reactivate-task/SKILL.md) 拥有完整profile、独立schema/exit/consumer及runtime事实校验。本正文替代该能力的历史拼接，不复制其细节成第二接口。各旧ID、继承条件和窄替代关系见 [traceability](../../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md)。

## D649：阶段成果与原终态边界

**D649-03 / CON649-DIMENSIONS** 承接 R649-04。原 Delivery Review contract 与 Completion Skill 分别在原 evidence／reason／summary 中说明适用六维及依据、环境或不适用理由。部署或入口探针只证明实际观察层；启用、采用和业务 E2E 保留独立要求。不新增六维 schema、公共 DTO 或统一证明表。

**D649-04 / CON649-GAP** 承接 R649-05。Completion 先比较整个 accepted scope、所有真实 Delivery 和必要证据，再使用原 implementation／additional Delivery、Author／Architecture、Clarify、evidence_refresh 或 completed consumer。必要实现遗漏和无依据机制前置不伪装成外部待补证据；局部 gate 只影响真实依赖 operation。

**D649-05 / CON649-CUTOFF** 承接 R649-06。原 RDT owner 维护当前结果入口，正式后序结果由原 public facts 与 Git／PR 承接。Closure／Finish 仅增加对既有写入责任的说明，不取得 Docs writer 权限。正文确有修订时，原候选适用性合同判断受影响覆盖；不回填自己的最终 pass，不新增完成账本或递归提交。
