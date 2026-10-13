# #531 设计：公共 Delivery authority 与 Guru 语义 owner

当前来源与副本迁移方案以 §16 的 Plan2 补修候选为准；§11 保留公共基础接口，§15 保留5181的真实失败。本文已沿当前 candidate_assessment 回原Author完成方案写作；Wording、final_plan、Approval仍须消费各自实际当前结果。历史批准和上游安装证据不授予新 Guru 门禁。

当前机制重规划以 §16 为来源绑定，公共基础接口沿用 §5/§11；本文所有 ce363、当时 PR OPEN、
B01/B02 初次闭合及 D2 未提供的叙述均为首轮历史记录，不是当前合同或准入结论。
当前公共接口保持 §5 的职责映射；涉及迁移与 candidate 的旧差额由 §11 明确替换。
原 owner/生命周期和 accepted scope 保留。2026-10-13 已整合 #292/#530 的 main@bebf1993，本轮 current Architecture .86 / RDT .89；前置候选先修订这些来源/版本绑定，实质方案写作以前置 Planning3 candidate_assessment 为准入，最终审查使用独立 final_plan。旧 .84/.85 通过仅为历史事实。

术语：上游历史交付阶段D1/D2与某Task首个/后继Delivery不同；后者始终各有公共UUID并走同一生命周期。上游当前完成边界按#31的2026-10-13正文，本文历史阶段不增加其现行门禁。

## 1. 设计对象、来源与当前差额

本候选以当前 canonical workflow 与 trellis/skills/guru-team/packages 为实现事实，.trellis/workflow.md、.agents/.codex 为安装投影。官方扩展依据：[workflow](https://docs.trytrellis.app/advanced/custom-workflow.md)、[marketplace](https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md)。生命周期判断写Markdown，Python/shell只执行、校验和记录有consumer的最小结果。

current Architecture：docs/architecture/README.md，current-main-0.6.17-guru.86 active；constitution：docs/architecture/00-foundation/design-constitution.md，guru-trellis-design-constitution-v1 current；change contract：docs/architecture/06-governance/change-contract.md，guru-trellis-architecture-change-contract-v1。RDT current-main-0.6.17-guru.89。当前extension 0.7.0-guru.3与Fixed Fork 0.7.0-castbox.3是独立版本轴，不表示本重构已发布。

### 1.1 唯一来源设计处置矩阵

下表拥有本 Task 的规范性来源处置；PRD/implement 只引用，不另建第二矩阵。#292 已经合入 main@8b55f624，不能再按未交付处理；#530 产品 d7cde2f062a25b43fe1f554b3187506457225820 已经由 PR #540 合入，PR #541 归档后 main@bebf1993。本树 HEAD f03e8a04c487e64722e90697543ec7398de2b338 已整合该 base 与 .86/.89 authority；9bee7/.85/.88 是历史前序，不沿用其门禁。正式合同逐项迁移见 §14。

| 具体来源及原承诺 | 处置 | 当前落点 | 理由、影响与上游处理 |
| --- | --- | --- | --- |
| #531「目标模型」：Task 整体责任、所有 Delivery 独立 Planning | retain/migrate | §2、§12.1：整体需求与 Delivery 五份规划分离 | 保留整体责任，删除 Task 开发阶段；这是本 Issue 明确迁移，不修改来源 scope |
| #31「两仓职责与明确交接」「跨仓接口先行」「当前范围与独立完成条件（2026-10-13）」：唯一公共模型、先候选后切换、上游独立验收 | retain | §5/§11 公共基础合同与 §16 当前1e400140提交/185e CLI/45bb Core/API1/schema2/Plan2 | 公共 parser/store/迁移执行仍归上游；Guru 仅拥有自身语义、私有转换与自身 joint；旧 SDK/legacy 隔离兼容及后续 breaking release 由上游负责，不要求 Issue CLOSED 或 Guru 结果才能结束 #31 |
| 上游 plan2-worktree-copies design「继承副本」「branch binding」「恢复」：完整盘点、唯一active authority与原快照 | retain | §16.2—16.4：原Upgrade提交真实branch_bindings；公共executor合法性判断与preserve | 新185e包已独立审查、可安装且PR36合入；替换§15的当前接口依赖停止点。Guru不建副本authority，不改binding，不换包接续旧plan；matching evidence仍须本仓执行 |
| #292「唯一 writer」及 ADR-022：Author 八 profiles、四 exits，Approval 不写规划 | migrate | §12.1—12.3：八个 Delivery profiles；整体 scope-only 写作仍归同一 Author | 原 Task-root PRD 变为整体需求来源，三份开发计划改归 Delivery。新增有明确消费者的 scope-only profile/exit，既不建立 Task Planning，也不另建 Author；shared ADR 变更只走后续 promotion |
| #292「来源设计显式承接」：retain/change/reject、落点和上游处理 | retain | 本矩阵；每个 Delivery design 自己承接其实际来源 | 不用 provenance flag 或空表替代承诺审查；真实 scope 选择回 Clarify，技术细化不制造问答 |
| #292「Requirements convergence」：先需求、实际候选评估、后 solution writing | retain/migrate | §12.2、§12.3 | Delivery requirements_ready 仍先到 candidate_assessment；scope-only 输出不能进入 Architecture/Approval 冒充 Delivery 规划 |
| #292「两个 Architecture 回程」与 current change-contract Planning3 | retain/migrate | §3、§12.3；同一 Architecture owner、明确 purpose | candidate_assessment 回 Author，Wording-current final_plan 直达 Approval；不重放前置结果，不保留 Planning2 fallback |
| #292「scope_ready」「change_refs」「revision_actions」及 ADR-023 | retain/migrate | §12.2—12.3，独立版本化 input/output/consumer | 先有 Clarify scope 判断再写作；公共 scope 绑定由原 scope owner消费实际 requirements 输出，不能要求预先写完规划形成循环 |
| #292「Delivery Policy」「Docs SSOT Plan」「promotion」 | retain | implement §2/§4；§9 task-local proposal | full Policy、delta_first、final Phase2 前 RDT reconciliation、committed Review 后晋升不改变；未晋升不能 Publish |
| #530「最新 base 复核」「验收」：clean 当前候选正式接续首次完整 Review | retain/migrate | §5.3、§11.3；原 TaskCommit 的 delivery_committed_reentry | #530 已交付正式 committed_reentry 输入/输出；按 §14 保留完整 clean/base/HEAD/Check/首次 Review 责任，迁移对象与五 blob 来源读取，不复制旧 checkpoint writer 或新增 clean authority；旧 backend 现场另用受控副本验证 |
| #468 活动重规划、输出丢失与局部 freshness | retain/change | §6、§8：同 Delivery rework 与原 owner recovery | 保留正常接续；Task activate/resume_execution 在新安装退出，当前 #531 legacy 执行安装仍按原合同重规划 |
| #532/#535 零候选完整 Check/Review | retain/migrate | §5.3、implement V01/V09 | []/all_rejected 仍需完整 evidence、freshness、finding 与独立审查；不能为了零候选绕过这些职责 |
| #531「既有能力」「成功后的投影恢复」：私有事务、历史事实与当前 pass 分离 | keep in Guru/migrate | §6、§11.3：Publish/Merge/history 原 owner | 中文 Refs-only、CI、expected-head/trailers、adoption/metadata/Ready 保留。远端成功先恢复事实，再判断当前义务；不新增 ledger 或重复动作 |
| #531「整体完成与无 Delivery」：Completion 各回程及独立收尾 | retain/migrate | §7、§11.2 | Task 完成重新判断遗漏 scope；无 Delivery 补证据/验证/收尾合法；Reactivate 新 generation 不复用旧 pass |
| #531「原始阻塞」「迁移与验收」：149/444/155、installed/native、平台/drift | retain | §11.4、implement V01—V15 | 使用真实旧形态受控副本；不改业务树、不补 provider，不把样本、joint、原会话恢复或 Release 混报 |

不采用 Guru 私有 Delivery 模型、旧 cycle 自动变 identity、第二状态机、phase=gate pass、任意 set-status、授权存储或无消费者审计 ledger；这些均与以上来源承诺冲突。

2026-10-12 最新只读核验：上游 D1 基础提交为 1f479eaf65c1ce661d7aa69d1b68affc6eeb2c92。完整 Review 发现的 publication 更新、无会话身份 hook、Droid 实际模板及三处规范冲突已由原 owner 修复；修复后的完整源码与新安装样例均获独立 Review，无剩余 D1 finding。新 Core/CLI 本地包、源码增量与实际单/多 Delivery 收尾证据已固定于§5.4。该候选源码随后提交为 ce36314b1ef5b44230883af9c1139a6244c13155，PR #32 OPEN；固定candidate为该提交与下述同源包。它已审查可安装，不证明合入、发布或 Guru joint。D1 为 opt-in 集成起点；D2 拥有旧数据迁移、default cutover 与旧 consumer 退出，旧安装切换另须 D2。

## 2. 权威与产物归属

| 对象 | 唯一authority/writer | 直接consumer与边界 |
| --- | --- | --- |
| Task身份/source/generation/Delivery关系/整体完成结果 | 上游公共合同执行端；Guru创建、阶段执行、Completion与Reactivate各自语义owner提供其最小结果 | resolution、Completion、收尾；无Task开发状态路由 |
| 整体accepted scope/总体验收 | 当前需求authority owner | Delivery规划与整体Completion；计划修订不能暗改整体scope |
| Delivery身份/公共阶段/合法转换 | 上游；授权的阶段owner经同一接口写入 | continuation/context读取；不接受任意状态字符串 |
| Delivery计划、切片与验收、planning JSONL | 唯一Author；确切定位由上游公共planning locator承接 | Wording/Architecture/Approval/实施/恢复；D1/D2同合同 |
| gate的最小不可重推导结论 | 各自Guru门禁owner | 该出口唯一consumer；phase不能重建批准 |
| candidate/commit/PR/merge历史事实 | Git/GitHub；原事务/history owner核验 | 对象事实与当前适用性分别输出；不储存完整可推导scan |
| publication子步骤/恢复checkpoint | Guru Publish owner-private runtime | 同一事务恢复，consumer结束即retire；不成为公共阶段 |
| Completion/Closure/Finish/Cleanup | 各自原owner | 公共整体完成只有一个结果authority；归档/清理不倒写完成 |

Task整体authority和Delivery三份docs必须分离。创建Task后先由当前workflow语义判断建立D1，再从其Planning开始。后继D2在首次Planning前建立新identity，并指出与整体scope的关系。返工、多个commit/PR更新、base整合均保留同Delivery。Task generation仅用于正式Reactivate，不能用来表达Delivery返工。

固定 D1 接口的 Task 根 prd.md 保留整体 scope；DeliveryRecord.planning_root 为 deliveries/<delivery_id>，承载该 Delivery 的 prd.md、design.md、implement.md、implement.jsonl、check.jsonl。绑定最终候选时复核该定位，Guru 不重新定义公共目录。已交付D1计划可由固定Git版本定位；未交付计划须保持当前可恢复内容。不能让D2覆盖D1唯一恢复依据，也不复制每轮tracked审计历史。原planning-content token只保留给邻接确定性consumer的用途；不得扩为跨全链authority或批准。

## 3. 阶段 writer、consumer 与薄投影

以下是职责序列，名称并非上游公共phase枚举。

| Guru阶段owner | 写入的真实结果 | 唯一下一consumer/公共承接 |
| --- | --- | --- |
| Intake/当前需求Clarify | Task边界或整体authority修订 | Task创建或受影响Delivery规划；不得以create确认接受未来计划 |
| Author | Delivery三份docs、官方context JSONL、来源设计处置 | Wording/Architecture/Approval各自读同一当前计划；Author不批准 |
| Wording | 措辞审查结果、实际 change_refs | Planning pass→Architecture final_plan→相邻 Approval；content_changed 回唯一 Author；不代替设计充分性 |
| Architecture | purpose-bound 当前评估/贡献/必要ADR结果 | candidate_assessment→Author solution_planning；final_plan→相邻 Approval；其它 stage 保持各自 consumer |
| Approval | 当前Delivery计划充分性结论 | 计划展示与当前对话接受，再由实施入口进行合法公共转换 |
| 实施owner | 实际候选内容 | 正式Check；普通method检查不自动转phase |
| guru-check-task | passed/implementation_required/planning_stale/blocked | passed→TaskCommit；其余回原owner/stop |
| guru-create-task-commit | dirty真实commit或clean既有候选committed | guru-review-branch；内容已提交与提交动作分开 |
| guru-review-branch | 完整committed diff独立判断 | passed→Delivery Review；finding→实施；scope→澄清；continuity与archive profiles保留 |
| guru-review-task-delivery | 当前slice readiness、remaining scope与中文Refs-only payload | ready→Publish；planning/implementation/scope/blocked出口保持职责 |
| guru-publish-task-delivery | 真正push/PR/metadata/Ready结果 | ready_for_merge→Merge；stale/reprepare/resume仍原owner |
| guru-merge-task-delivery | expected-head实际merge、delivered/completion_seed | Completion；公共Delivery交付事实投影 |
| guru-review-task-completion | 当前整体scope和全部事实的因果完成判断 | 完成→Closure；其它回程见第7节 |

每个public output字段必须有该exit的直接consumer。实现时逐项列出现有producer output→上游input→上游output→Guru consumer input，并由接口真实shape确定最小identity/freshness token。只有一个薄显式projection，不要求consumer理解producer内部digest/checkpoint。

公共阶段转换在owner实际行为及适用gate完成后发生；如果上游coarse phase包含多个Guru门禁，Guru在阶段内部继续按真实证据路由，不能新增公共phase或第二状态authority。continue/start/context/展示/压缩恢复只有读取和路由权，没有替其它owner写pass的权力。发现原生Skills先加载当前workflow选owner/profile；原生方法可复用，不能先完成一个native gate再重复Guru gate。

## 4. 原能力迁移清单

| 现有资产 | 保留能力 | 迁移及旧路退出 |
| --- | --- | --- |
| TaskLifecycleDTO、C4 branch/resource、C5 session/checkout | 同一TaskId/generation，唯一注册checkout，精确资源owner | 接公共Task/Delivery当前查询；checkout路径不变身份；不要求每Delivery新工作树 |
| Task planning/in_progress/completed、activate/resume_execution | 批准后实施、活动replan及输出丢失恢复 | 改Delivery实施入口；删除Task阶段reader/writer及首次/后继分支，恢复不得再写status |
| task-root planning docs与content token | 唯一Author、计划freshness与旧计划恢复 | 接公共Delivery planning定位；固定历史版本可读；token仅原邻接consumer |
| Phase2 checkpoint与passed DTO | complete scope check、对应candidate/base、lost stdout恢复 | 改Delivery身份绑定；无phase推断pass；消耗后retire |
| TaskCommit dirty与#530 clean候选 | 提交必要增量/正式接续既有HEAD | 单owner两种内容事实路径；clean不stage不commit不写tracked证明 |
| Branch Review / continuity / archived review | 独立完整范围、finding/scope/基线连续性判断 | 保持原profiles语义，绑定当前Delivery候选；旧pass只恢复原对象不能覆盖新义务 |
| current slice/policy、delivery_cycle_ref | reviewed slice、同计划PR adoption、历史关联 | cycle是旧事实定位而非identity，归属由history/原transaction owner映射 |
| Publish事务 | push_content→bind_pr→converge_metadata→mark_ready→ready | 全部保留owner-private；成功结果再投公共阶段，不上提子步骤 |
| Merge与trailers/history | expected-head、真实CI、first-parent+GitHub结果 | 保存旧trailers读取/归属能力；新写字段按上游身份/API显式迁移，不静默改公共出口 |
| Completion/Closure/Finish/Cleanup/Reactivate | 整体责任与独立恢复 | 绑定公共Task完成结果、新generation及真实Delivery历史；无空Delivery义务 |
| native/platform/natural-language/task-free入口 | 正确owner、手动与formal区别 | 全量受管projection一致，保留无Task路径；不在入口复制门禁 |

## 5. 实际上游公共接口映射与准入差额

当前引用 §16 的1e400140产品提交与185e CLI/45bb Core同源安装包；ce363 为 §5.4 的历史 D1 接口快照。当前实际公共定义位置：
- packages/core/src/task/v2/{types,operations,store,index}.ts，package.json 的 ./task/v2 export。
- packages/cli/src/templates/trellis/delivery-contract.md 与 workflow-delivery-v1.md。
- packages/cli/src/templates/trellis/scripts/common/{delivery_schema,delivery_operations,delivery_store,delivery_session,runtime_contract}.py。

接口声明 Task schema 2.0、Delivery API 1.0、SDK @mindfoldhq/trellis-core/task/v2；TaskKey 为 task_id/lifecycle_generation，DeliveryKey 再加不透明 UUID delivery_id。公共 phases 为 planning、implementing、checking、reviewing、publishing、delivered、stopped；11 个 role 由唯一 [trellis-runtime-contract] 指定 owner。Task aggregate 的 accepted_scope/deliveries/completion_results/closure_results 是唯一公共状态，新增 schema 不含 writable Task status/commit/pr_url/completedAt。Guru 仅消费，不复制 schema 或另设 ledger。

| 项 | 实际接口定位与 Guru producer→公共承接→consumer | 尚待闭合的证据或行为 |
| --- | --- | --- |
| I01 identity/create/relation | scope owner → accept_scope；slice creation owner → create_delivery(key,scope_ref,profile=pull_request) → 同 Delivery Author。create_delivery 在 Planning 前分配 UUID，重复同 identity/scope/profile 返回 unchanged | 固定候选下 Guru creation owner 的实际声明、恢复示例与 D1/D2 installed 结果 |
| I02 current/no-current | C4/C5 Task → schema-3 binding；getCurrentDelivery/get_current_delivery → current、terminal_delivery、no_current_delivery、no_current_task、error。select_delivery/release_delivery 只改 selection → start/continue/Completion | Guru 现有 session/runtime 到上游 resolver 的薄转换、真实平台 bridge；不得从唯一 inventory 猜选 |
| I03 planning定位 | Author → DeliveryRecord.planning_root 与 plan_ref → Wording/Architecture/Approval/实施；Task root PRD 单独持有整体 scope | 复核 #292 唯一 Author 与 JSONL consumer 迁移；历史 generation 的计划读取不能误用仅 current-generation planning_directory |
| I04阶段/writer | Approval 实际计划接受后 → planning record_gate → implementing；实施 → begin_check → checking；Check → check record_gate → reviewing；完整 Branch Review → full_review record_gate，仍 reviewing；Delivery Review → readiness record_gate → publishing | 当前 Approval approved 只表示语义充分性，公共 planning accepted 必须在 workflow 展示/当前对话接受后由实施入口转换，不能提前写；fresh Check 与提交后 HEAD 的 candidate 接续见本节约束 |
| I05返工/退出 | 当前 stage owner → rework(target_role,reason,affected_results,scope_ref?) → 最早受影响 owner；全撤回 → stop(reason,scope_decision) + release_delivery → 无 Delivery 的 Completion | 在对应阶段声明唯一调用 owner；需求已修订时 scope_ref 更新限定 planning；停止与 selection 释放是两动作，丢输出由原 owner 接续 |
| I06成功事实/投影恢复 | Publish ready_for_merge → record_publication(PublicationFact) → 原 Merge；Merge delivered → record_delivery(DeliveryFact) → Completion。两操作都支持 historical_success；同 result_id 的相同 payload 重试返回 unchanged | 固定候选的 TS/Python/Guru PR verifier 真实结果恢复；两操作实际支持历史事实恢复；正文与最终修复候选的行为一致性须复核，不能用历史成功绕过新动作门禁 |
| I07整体完成/收尾 | Completion completed → complete_task(current scope/generation,delivery_result_ids) → Closure；Closure actual disposition → close_task(completion_result_id) → Finish；Reactivate → reopen_task → 新 generation | 归档执行消费公共完成/关闭结果；Finish/Cleanup 私有恢复仍原 owner；历史结果适用性由 Completion 判断，不靠 result_ids 数量自动完成 |
| I08迁移/版本 | D1 opt-in API/runtime；D2 原 owner 的旧 schema/session/default cutover 迁移 → Guru 私有迁移与 installer/version 诊断 → 成套新 reader/writer | 公共 Plan2 已提供并审查，实际版本/安装/API 见 §11；正常注册工作树继承副本的支持组合仍有§15的具体公共接口缺口，旧安装切换要求该前置、Guru 私有迁移及匹配验证。成套切换前保留原完整发行安装，不能混用 reader/writer |
| I09原生/无Task | 原生 quality 与 delivery_check 分 profile；full Review/readiness/deliver/complete 各 owner；当前 workflow declaration + continuation → Guru 唯一 owner，task-free 保留 | 真实 CLI/平台入口与 package 安装闭环证据，原生 manual/local_commit/pull_request 由上游验证；Guru 只声明自身 pull_request，不硬编码为全局政策 |

实际 payload 的薄映射采用以下约束，实施前在固定候选上转为对应 adapter 与契约测试：

1. GateResult 引用 result_id、owner_role/id、outcome、scope_ref、plan_ref、candidate、predecessor_result_id、obligations、evidence。Planning 无 candidate/predecessor；Check predecessor 是实际 Planning；full_review 是实际 Check；readiness 是实际 full_review。Wording/Architecture/qualifications 保持 Guru 内部职责，不各造公共 gate。
2. CandidateRef 的 kind/content_ref/paths/head_ref/base_ref 分别绑定真实内容、提交与基线。paths 由 scope owner 明确包含完整候选；上游 computeCandidateContentRef 排除 lifecycle/session/private 文件，不能以 excluded task.json 推定所有 Task docs 都应排除。计划和 obligation refs 只绑定该 gate 的实际输入，不能变成授权 token。
3. Guru dirty Check→TaskCommit 改变 HEAD 但可能不改变被审查内容；Check candidate 不可因提交而被静默换成新 HEAD。固定 D1 接口支持的接续为：reviewing 当前 full_review owner 判断提交影响后调用 rework(target_role=implementation,affected_results=[check,full_review,readiness])；实施 owner 用 begin_check 登记同内容、实际新 HEAD 的 candidate；Check owner 判断旧验证对当前内容/计划/基线的适用性，生成新 candidate-bound Check result，然后首次独立完整 Review。完整 Planning 不失效，仍有效测试结论不强制重跑；发生实质变化才补执行受影响验证。不能由 Check owner 在 reviewing 越权 rework，不能由 Reviewer 代写 Check。clean 接续保留当前 HEAD、当前适用 Check，无新 commit。最终 candidate 须验证该合法接续，不把此静态设计当运行通过。
4. PublicationFact 从实际 repo/PR/reviewed_head/target_ref/publication_ref 和原候选投影；DeliveryFact 再含真实 merge_commit。store 的 verifyFact 由原 producer 只读核验 PR 事实；historical_success 跳过当前 gate/candidate 适用性条件，但不跳过实际事实核验，不反推任何当前 pass。
Publication 返工保留原成功事实，未交付同一PR在fresh readiness/current candidate下以新result_id更新当前slot；repo_ref/pr_number/original owner_id保持，仅当当前 readiness 已审查 target 变化时更新实际 target。历史P2成功可由原producer经store真实PR head/body/target核验恢复；不补gate、不重做远端动作。已交付历史保持不可变，空terminal slot恢复必须与原delivery事实一致。保留P1直到P2核验投影成功；Guru不新增retired-result ledger补偿该公共职责。

5. OperationOutput 的 record/key/phase/result_id/changed 是 store receipt。Guru adapter 只将该出口直接 consumer 所需 key/result token 投为手头 DTO；完整 record 不直接塞进 public Skill output。store exact preimage 与 digest 只供邻接确定性写入，不提升为 workflow authority。
6. complete_task 不自动判定整体 scope 充分；停止的切片不代表满足验收；当前 scope 可复用旧 Delivery 成果由 Completion 审查。close_task 的 no_mutation/source_closed 承接当前 Guru disposition，具体 Issue 关闭仍由 Closure owner 按实际关系执行。

B01/B02 的 ce363 初次闭合保留为历史；当前接口候选及 Plan2 按 §11 核验。B03 是 Guru 版本化 I/O、writer 与实际 installed 接续，随本任务实施闭合；B04 的公共迁移 API 已提供，尚缺 Guru 私有迁移支持组合与真实旧形态匹配验证；5181的真实注册工作树继承副本接口缺口保留于§15；当前§16公共补修已交付，剩余是Guru承接与matching验证，不能继续写作上游未提供接口。上游旧 SDK/显式 legacy workflow 最终退休按其 2026-10-13 当前范围归后续 breaking release，不是 #31 或 Guru 切换的额外前置。B04 未齐时不能切旧安装，但不阻止在固定可安装候选上实施本仓 consumer。Issue CLOSED 不是前置。


### 5.1 最小 producer → 公共输入 → 输出 → consumer 实例

以下为引用固定 D1 接口的设计转换规则。右侧新增绑定必须在固定 candidate 上完成版本化 Skill I/O 迁移；不是当前 main 已接受的新 DTO，不手工生成 formal pass。

| 现有真实输出与源位置 | adapter 读取的必要当前输入 | 公共操作及 receipt | 直接 consumer |
| --- | --- | --- | --- |
| guru-check-task/examples/public-passed-output.json：task_ref、phase2_commit_anchor | 已解析 DeliveryKey、当前 scope_ref/plan_ref、candidate、Planning result_id、该 Check owner 的实际结论 | record_gate(role=check,outcome=passed,predecessor_result_id=实际Planning)；receipt.key/result_id | TaskCommit 保留 phase2_commit_anchor；提交后影响判断读取 key/result_id，不把 receipt.record 当 public output |
| guru-create-task-commit/examples/public-committed-output.json：task_ref、base_ref、branch_review_commit | 当前公共 phase/candidate；实际提交范围及仍有效 Check | 不存在公共 commit 操作；内容/HEAD 未变化不写公共记录；HEAD变化按本节第3条原 owner 序列接续 | 首次完整 Branch Review，完整 origin/base...branch_review_commit；committed 本身不是 Review pass |
| guru-publish-task-delivery/examples/public-ready-for-merge-output.json：task_ref、delivery_cycle_ref、repo_ref、pr_number、expected_head_sha、publication_body_sha256 | 原 Publish transaction 的 DeliveryKey、实际候选、最小原 producer result_id、中文 payload 的既有定位/版本和 PR live facts | record_publication：repo_ref/pr_number 原值，reviewed_head=expected_head_sha，target_ref=实际selected目标，publication_ref=原payload定位/版本；receipt.key/result_id | 原 Merge public input 保留其必要 PR/HEAD/body token；cycle_ref只供原私有事务，不成为 DeliveryKey |
| guru-merge-task-delivery/examples/public-delivered-output.json：task_artifact、merge_result | task_artifact 与原 transaction DeliveryKey 一致；PR已合入/真实HEAD/merge commit与原candidate | record_delivery：result_id=merge_result.result_id，repo_ref/pr_number/reviewed_head 原值，merge_commit=merge_commit_sha，target_ref=实际目标；历史恢复显式 historical_success | Completion 保留当前 completion_seed 所需事实并读公共 key/result_id；原 source disposition 不变 |
| Completion 的实际 completed 结论 | 当前 TaskKey、整体 accepted_scope、全部成果适用性与遗漏义务结论 | complete_task；receipt.key/result_id，不靠已知deliveries数量推导 | Closure 使用确切 completion_result_id；Finish/Cleanup 使用各自当前合同，不新增 Delivery |

task_ref 通过现有 Task identity resolver 定位，不能从路径字符串推导 TaskId；DeliveryKey 从公共 selection 或原 transaction 的明确关系恢复。当前 public outputs 不带 scope、plan、candidate 或 stable DeliveryId，adapter 不能仅凭旧 DTO 空填这些值。额外 input 属于当前 owner 实际调用上下文；最终 public handoff 仅携带下一个 consumer 不能自行解析且必须读取的最小 key/result token。

Plan_ref 的落地采用实际 AuthorityRef：指向该 Delivery 的 design.md 与确切内容版本；prd.md、implement.md 和实际受影响工程义务以各自 AuthorityRef 放入该 owner 的 obligations。三份文件充分性仍由 Planning 审查；不能把现有 composite planning-content token 塞进单文件 revision 并声称满足 store 的 verifyAuthority。只有实际被 gate 消费的义务进入 obligations，不把所有审计输入打包。

当前已读已提交 CLI packages/cli/src/templates/trellis/scripts/delivery.py 的 current/list/select/release/apply、closed operation aliases、candidate 与 contract；delivery-workflow.ts 在运行前核验版本、API能力及 active legacy/schema-2 组合。它们已随候选安装；上游原生证据见§5.4，不是 Guru 已安装证据；本仓不运行其 mutation 迁移自己的 Task，命令细化以固定 candidate 为准。

### 5.2 接口差额的准确归属

- 已有公共能力：stable key、coarse phases、合法返工/退出、session selection、两类 historical_success、整体结果与原生 profile；不再归为“上游未定义接口”。
- 上游 D1 准入：B01/B02 已闭合，修复 candidate 的独立源码 Review、重打包/安装及原生样例证据见§5.4。Guru 不替其提交修复或发布 package；后续 source/API 变化 fresh 重判适用性，不按版本字符串自动接受。
- Guru 设计/集成证据缺口：B03；本节已明确映射来源和合法接续序列，仍须完成最终 versioned input/output 及实际 wrapper/installed 验证。旧 DTO 缺 stable key 的事实不能靠脚本猜测消除。
- 联合切换缺口：B04；上游公共迁移与 Guru 私有 cycle/history/transaction 迁移分别由原 owner 实现，installer 支持组合和旧路退出共同验证。不要求 D2 先完成才设计或开发合格 D1 的 adapter。


### 5.3 Guru 版本化 I/O 与唯一 writer 迁移设计

本节选择 Guru 自有接口迁移方式；公共 DeliveryKey、操作、aggregate 与 applicability 仍引用上游，不在 Guru schema 复制定义。以下新 Skill/profile/schema 是 #531 的设计目标，当前安装不具备，不能据此调用 runtime。

- 新建 guru-create-delivery：semantic closed loop，在已解析 Task/checkout 与当前整体 scope 下审查一个明确切片，使用公共 create_delivery/select 建立首次 Planning 身份。它拥有重复输出恢复和真实切片选择，不创建 Task/branch/worktree。created 输出只交 DeliveryKey 给唯一 Author；scope_revision_required 回 Clarify；selection_required 回该创建 owner 处理真实选择；blocked 停止。同范围正常恢复复用原 UUID，不能重新分配来掩盖已发生创建。
- 新建 guru-activate-delivery：semantic closed loop，消费当前 Delivery Planning Approval 的最小结果与公共 DeliveryKey，承接 workflow 当前计划展示/对话接受后记录实际 planning accepted，并进入实施。delivery_started 只交 key/planning_accepted_result_id 给实施；planning_refresh_required 回 Approval；invalid_delivery_state/blocked 停止。首次 D1、后继 D2 和同 Delivery 返工共用该合同；旧 Task activate/resume_execution 与 status mutation 退出。结果丢失恢复原 key/result，不重做已完成转换或新建 Delivery；尚未转换且当前对话无法确定接受时，仍回原展示/接受路径，不从 phase 补造接受。
- Task scope 的两个真实语义来源保持分开：Clarify 拥有 accept_scope 的需求修订判断，Reactivate 拥有 reopen_task 的正式重开判断。两者只将实际结论交同一个无状态 scope projection 执行端；该模块作为公共 task_scope role 的唯一确定性 writer，只调用对应闭合操作，不判断范围/完成/route，也不持有第二状态。
- 实施 Agent 拥有实际候选生成及交付 Check 的语义判断；唯一无状态 implementation projection 接收该 owner 的明确 candidate 并调用 begin_check。global coordinator 只路由，不自行造候选或 gate。TaskCommit 是提交事实 owner，不占用一个虚构公共 commit role。
- Check/full_review/readiness/publication/delivery/completion/closure 分别声明现有 guru-check-task、guru-review-branch、guru-review-task-delivery、guru-publish-task-delivery、guru-merge-task-delivery、guru-review-task-completion、guru-complete-task-closure。Wording、Architecture、唯一 Author、TaskCommit、Finish/Cleanup 是各自原责任，不能竞争写这些公共 result slots。

| Guru 边界 | 新合同的最小必需输入/输出 | 旧合同与唯一 consumer 的迁移 |
| --- | --- | --- |
| Author/Wording/Architecture/Approval | 输入明确 DeliveryKey，解析上游 planning_root；Approval approved 输出 key 与原 Guru planning_result_id | 保留 #292 唯一 Author 和内部 profiles，不复制第二 writer；当前 task-root locator/version 在 schema-2 安装不再用作 Delivery plan。approved 唯一 consumer 改为 guru-activate-delivery；Guru token 不成为公共 Planning result |
| 正式 Check | 输入 key、当前 profile 所需原 gate/reconciliation seed；passed 输出 key、phase2_commit_anchor、公共 check result_id | 原 initial_check/finding_fix_rerun/planning_reentry/resolved_reconciliation 的语义和正常回程保留；每个 profile 用独立 delivery 输入 schema，普通 method 无正式写入。passed 唯一 consumer 仍 TaskCommit |
| TaskCommit | 输入 key、当前 Check token/anchor；committed 输出 key、base_ref、branch_review_commit | 原 dirty/recovery 与 #530 committed_reentry 保留；clean 不 stage/commit/hook。公共 Check token由当前输入读取，不复制完整 Check evidence。consumer 是完整 Branch Review 前的候选接续路由 |
| Branch Review → Delivery Review | 输入 key、base_ref/head 与实际当前 Check；passed 输出 key、branch_review_commit、public full_review result_id | 完整 Review/continuity/archive profiles 分开；continuity 不投 full_review pass。passed 唯一 consumer 保持 Delivery Review，后者输入读取当前 full_review result |
| Delivery Review → Publish | ready 输出 key、原 Publish 必需的中文 payload/head 与 readiness result_id | payload/current slice/policy 的必要字段按现有 consumer 保留；不传 scan/history/Architecture reasoning。ready 唯一 consumer 保持 Publish |
| Publish → Merge | ready_for_merge 输出 key、repo/PR/expected_head/body token 及 publication result_id | cycle_ref 仅原 private transaction；Merge 不解析 Publish checkpoint。外部动作成功而公共写失败时 Publish 恢复同事实，不能输出未完成投影的 ready_for_merge |
| Merge → Completion | delivered 输出公共 key/result_id；Completion从公共事实解析真实 PR/head/merge 与 TaskKey | 迁移原 task_artifact/merge_result seed；只保留 Completion 立即必须读的不可重推内容，不重复整份 aggregate。historical_success 仍只是事实恢复 |
| Completion/Closure/Finish/Reactivate | 输入 TaskKey及该 profile 的最小结果 token；completed/closed/no_mutation交对应 result_id | no-current Delivery 合法；Completion 的 evidence_refresh/reactivation_validation 不要求 key 中含 delivery_id。历史 delivery_key 只定位其原事实，不成为当前 execution selection。Finish/Cleanup资源输入按现有资源owner保持 |

新增 Creation/Activation 使用各自简洁 schema 1.0。既有 Skills 保留 stable id，新增明确命名的 Delivery profile/schema，采用与旧 Task 输入不同的 schema id（命名含 delivery-1.0），按每个 typed exit 分别定义 output；不得把 delivery_key 做成所有旧 profile 的 optional 字段或在一个巨型 DTO 混合 Task/Delivery 状态。消费者 schema、registry projection、examples、wrapper 和平台加载同一轮更新。已实读 #292 的八 profiles/四 exits 与 #530 committed_reentry 的正式输入及唯一 committed consumer；新增 delivery_committed_reentry 输入/出口 schema 与旧形状明确隔离，实际差额见 §14；stable TaskCommit owner 不变。

Planning 的两种结果身份必须分开：Approval 的 planning_result_id 保持现有 Guru 邻接 freshness token，只由 Activation 校验，不写入上游 GateResult.result_id、evidence 或跨阶段 public handoff。公共 planning role 的唯一 owner_id 声明为 guru-activate-delivery；该 owner 在合法转换时生成稳定的 GateResult.result_id，按实际 scope_ref/plan_ref/obligations 记录 outcome=accepted，candidate/predecessor 为该 role 的空值。上游返回的同一个 result_id 以 planning_accepted_result_id 交实施；实施交正式 Check 时，Check 的 predecessor_result_id 引用它。Approval 不调用公共 record_gate，不竞争 Planning slot。Activation 已成功但输出丢失时，由其读取原 result 和当前绑定物化同一输出；freshness token 或公共 phase 都不能单独重建 Approval 的语义结论。

采用直接演进，不在新 Guru 包中并行保留两套活动 runtime。未升级 legacy 安装继续使用原固定发行包，合格 D1 的新受控安装只消费 schema-2/API-1.0 Delivery profiles；D2 就绪后一次迁移自有数据并成套更新 controlled consumers。升级/apply 在任何 workflow/schema 写入前诊断不支持组合；旧 DTO 不自动重解释。历史 reader 只归原恢复/迁移 owner，不用于活动执行 fallback；其最后 consumer 迁移后同任务删除。上游 D1 自有 legacy /task 窗口由上游合同拥有，不在 Guru 扩展为永久兼容。若届时出现必须保留的新外部 consumer，先回原 Planning owner展示具体例外，未获具体例外接受前不得添加兼容实现。

当前 getGateApplicability/get_gate_applicability 已提供每个 fixed slot 的 missing/applicable/not_applicable、result_id、code。Guru continuation 使用它区分可用记录与缺失/绑定失效，再由原 owner 校验真实文件、scope、candidate/base和当前义务；不把 applicable 当 semantic sufficiency 或跳过完整 Branch Review。此读取接口已随 D1 candidate 绑定，修复后仍须核对接口是否变化。

### 5.4 历史 ce363 候选与当时验证边界

| 绑定对象 | 本轮实读 identity / evidence | 使用边界 |
| --- | --- | --- |
| Source | castbox/Trellis，codex/31-native-delivery-lifecycle，固定提交 ce36314b1ef5b44230883af9c1139a6244c13155，PR #32 OPEN；打包时的source provenance为父提交1f479eaf加修复增量，candidate.json 的 source_diff_sha256 为 83287c8586b6e95707ae9f967ecb14801c488c8b240e2b314c4f733b2f8010ad | 打包增量核验时git diff值一致；提交后11项package_increment全匹配ce36314b树（含两个fixture），包内容未因提交改变；完整源码Review在提交前覆盖同一内容，不冒充提交后的第二formal Review |
| CLI 包 | 0.7.0-castbox.3，mindfoldhq-trellis-0.7.0-castbox.3.tgz，SHA256 b6f29f7f8be8c63513bb75fe36d726abe116306f55dcfb599b5a2c203a1ac609 | 实读包hash固定安装对象；不按同版本字符串复用旧包资格 |
| Core 包 | 0.7.0-castbox.3，mindfoldhq-trellis-core-0.7.0-castbox.3.tgz，SHA256 d9fe25c74e4157a0f2d1bf91f8a02a93de8761edb82affe5ff9002923f3d3905 | /task/v2 export存在；Task schema 2.0、API 1.0 |
| 本地定位与安装 provenance | /tmp/trellis-31-rework-candidate-path.txt 指向 trellis-31-rework-candidate-1gr4zp9t；其 candidate.json、installed/ 和 samples/ | 原 owner 的可安装候选；installed CLI 700/Core 258文件与tarball匹配，33 Python文件、公共contract/workflow与source匹配；不是Guru安装 |
| 完整源码 Review | 上游 Task research/source-review-rework.md：baseline 5c760463680ffc10a3f26957b330c57a4b0c3ff8→HEAD加完整增量；四项finding闭合，无剩余D1 finding | 真实独立read-only源码 Review；已审查内容随后提交；不是提交后的第二formal gate |
| 新 installed Review | research/installed-review-rework.md：三个完整切片均独立PASS，无findings | manual UUID 0e2b3470-4e1d-4ce1-91a3-2fd1901902a3；local UUID d217a25e-23a5-48d3-97e5-4bce09d3f1e4、f800f20c-3105-499a-95d6-01329c8af409；D2保留D1 |
| 原生交付重试/收尾 | /tmp/trellis-31-rework-samples-finish.log：manual单Delivery、local两Delivery均PASS，独立Completion/no-mutation Closure；原owner实际执行 | 无Guru原生proof；不是Guru PR-based闭环、远端成功或joint验收 |
| publication 修复安装验证 | /tmp/trellis-31-rework-installed-publication.log：rework 30步、history recovery 11步在真实store入口PASS | 使用模拟PR postconditions，未发生真实远端PR/merge；真实远端验证仍归V10/V11 |

上游原 owner 最新完整证据为 Core 442 PASS + 1 existing SQLite capability SKIP、CLI 1928 PASS（86文件）、两包 lint/typecheck/build PASS、Python 0 errors/48 existing warnings、Python3.9 compile 73文件及runtime/hook parity。初次CLI两例fixture失败与修复后重跑分开记录于其 execution.md，不能抹掉失败。Guru只引用该owner证据，不重复上游完整套件。

旧包 ba42c0d6…/66d7d0ca… 已被上述修复包取代，旧installed-review-final.md不绑定新identity。当时 candidate 满足已审查、可安装条件；其固定 ce363/tar 绑定仅服务历史记录。当前实施固定 §11 的最终5181/tar/API，不复用该段的旧准入。D2公共迁移/default cutover、Guru真实installed/joint、软件Release及原业务会话恢复仍未通过。

### 5.5 版本化边界的确定落点与恢复最小输入

Guru owned input 的新增 profile 名采用 delivery_<existing_profile>；output 保留现有 exit id，以独立 output schema代替旧形状。schema id 命名为 guru-<skill-action-object>-input-delivery-<existing-profile>-1.0 和对应 output-delivery-<exit>-1.0。Creation/Activation 是新 skill id，不伪装旧Task激活。Registry、consumer projection、examples、wrapper、平台加载在同一候选内成套更新；#292/#530 若有实质 API 演进先 fresh 对照再记录差额，不静默覆盖。

新 Guru DTO 的 delivery_key 是上游 DeliveryKey 的不透明承载；Guru schema仅约束自身闭合顶层字段，不复制上游字段schema。输入读取由公共 getCurrentDelivery 与 parseTaskRecordV2 的真实关系校验，写入由 parseTaskOperation/公共 store验证；没有第二 key validator/model。无 Delivery 的 Completion/closeout profiles 使用 task_key；不添加 nullable delivery_key 来合并所有输入。

Creation 在首次调用前为一次明确切片分配 UUID，并在其 ignored owner-private 创建 checkpoint 保留 key、scope_ref/profile 的最小恢复输入。其唯一consumer是同Creation的 create/select输出恢复：公共记录已创建但 selection/DTO未完成时读取该明确key继续，不从inventory唯一项猜身份，也不另建Task或UUID；完成后retire。该checkpoint不记录slice判断历史或授权，不成为公共身份authority。

Publish/Merge 原 private transaction在远端动作前已具有明确DeliveryKey、原candidate/result关联；公共写失败或stdout丢失由原transaction核验live事实并重用该结果。真实返工产生新candidate及新result，旧PR/merge事实仍由Git/GitHub与原事务恢复，不能用旧publication slot阻止新发布，也不能把旧结果投影成当前readiness。公共publication替换/保留的精确行为必须由修复后上游contract确定，Guru不自行添加publication历史ledger解决该finding。

## 6. 返工、局部失效与成功事实恢复

Creation 在创建 UUID/pending 前校验当前公共声明实际支持的 profile；schema 能表达
某原生 profile 不代表 Guru 已支持其 writer。旧调用因 unsupported profile 留下的
pending，只由同 Creation 在 Task/generation/scope 仍一致且公共 inventory 确认该
key 从未创建 Delivery 时结束，再承接当前合法输入。已有公共 Delivery 必须保留原
identity 并走原恢复，不能更换 profile。caller 不手删 checkpoint、不换 token
掩盖失败，也不借该修复新增 profile 支持。

方案变化：同Delivery回Author，Wording/Architecture/Approval按实际影响重入；整体scope变化：Clarify先更新authority，再回受影响Delivery。已交付Delivery保持事实，新实现走后继Delivery。部分撤回仍返工；全部撤回使用I05停止/unbind，保留提交/PR，关闭PR独立确认。Completion重新判断已撤回义务，不把退出当验收满足。

| 变化/缺失 | 最早owner及处理 |
| --- | --- |
| 信息性Issue更新、语义不变的措辞 | 当前owner判断依赖范围，不自动整链replay |
| 计划/切片实质变化 | Author/Approval及受影响Architecture；保留已提交事实 |
| 实现finding | 实施→freshCheck→dirty必要commit或clean接续→独立Review |
| base演进 | Reconcile/pair guard判连续性或整合；整合候选freshCheck/Review；基线单独演进不触发需求重写 |
| readiness/payload/livePR义务变化 | Delivery Review或Publish原owner；不借公共phase沿用stale pass |
| 公共phase滞后、仍适用gate | 原事务读回结果→同Delivery/candidate/result投影；无需重复gate或远端动作 |
| 同期authority/内容/基线实质变化 | 恢复原历史成功，同时由正确owner重审继续执行义务；两个结论不混写 |
| semantic结果丢失且无仍有效checkpoint | 原semantic owner fresh re-entry；文件/阶段不能补造pass |
| provider局部缺口 | 对应场景保留blocked，独立有真实consumer工作继续；不补provider业务 |

Publish可从既有同计划事务/真实PR恢复adoption、metadata及Ready；Merge从expected-head、live merged状态与trailers核验真正结果。若远端已成功公共projection失败，原owner恢复同一结果后再接I06；不反过来从公共阶段猜push/PR/merge成功。恢复历史结果不以重新取得当前gate为记录前提；当前新动作必须通过当前gate。

历史发现仍由Merge/history owner读first-parent trailers和GitHub；bookkeeping PR不成为业务Delivery。旧cycle_ref源自Task/HEAD/PR payload，不能直接改名当DeliveryId。先核验PR、merge、Task归属与generation，再调用上游身份/迁移接口。无法唯一归属时诊断原owner，不任意造D1。只有公共consumer无法重推的最小归属映射按明确consumer持久化，具体承载随I08绑定；不新增ledger。

## 7. 整体完成与无Delivery路径

Completion重新读整体accepted scope、未分配工作、全部适用历史成果/证据。所有已知Delivery合入不能推出完成。各出口责任保持：
- remaining_work→active-task-continuation；additional_delivery_required→同Task下一Delivery建立/规划。
- requirements_revision_required→整体Clarify；implementation_revision_required→受影响实施owner。
- evidence_pending→同Completion evidence_refresh；Delivery-based补证据或Reactivate-only validation均不强制新Delivery。
- completed→Closure；blocked→原stop。

Closure仅应用exact source disposition，no_issue/reference_only/follow_up/parent均no_mutation；Publish/Merge与bookkeeping均Refs-only。closed/no_mutation→Finish；resume_closure/external_change_conflict仍原owner处理。
Finish持久化真正Completion/Closure并归档，success/manual_cleanup_required→Cleanup；resume_finish/closure_refresh_required各回原owner。Cleanup精确资源，remaining/manual路径不撤销完成，handoff路径保持。
Reactivate只从正常finished archive，保留Task身份/历史，建立新generation/current authority；未完成closeout仍原事务，不冒充reactivation。新generation不复用旧批准/close/cleanup结果；历史成果可由当前Completion评估，不强制重复交付。

## 8. 旧安装迁移与退出

顺序：只读版本/topology/dirty inventory→检查支持组合→原owner恢复未完成事务事实→上游自有schema/session迁移与Guru私有迁移→新reader/writer成套应用→公共identity/query核验→native continuation定向验收→退役旧route/checkpoint写入。

旧status只提供历史线索，不能单独定新phase或pass。active planning/in_progress、archived completed、多PR、legacy header、session缺失、clean既有HEAD、在途Publish/Merge分别核验。没有可恢复gate就fresh原owner，历史成功独立保留；completed字段不冒充新公共整体完成结论。旧原文件/资源保留至明确consumer完成或合法cleanup。

迁移是有界版本窗口；同一安装一次只运行一个公共模型writer。切换前缺候选/API或无法迁移时拒绝应用，维持原完整版本；切换后不让旧writer继续写，不加永久dual-read/status fallback。回退只有在原owner核验新数据/远端事实不会被旧版误解释后才进入回退，不能直接回装旧入口掩盖迁移。用户修改由官方.new/.bak处理及明确处置，不静默覆盖。

## 9. Architecture change candidate

候选路径为 legacy_boundary_convergence，供独立Architecture owner判断；上游target-native公共模型与Guru旧consumer有真实迁移依赖，不能宣称无impact或永久adapter。当前 Planning task-owned contribution 直接承载于本 design.md 的第9节及所引用的设计事实，不另建审计文件：contribution_locator 为 .trellis/tasks/10-12-531-task-delivery-lifecycle/design.md，contribution_identity 为当前正式 invocation 实读文件的 sha256:<实际文件SHA256>。仅当前独立 owner 可给予 reviewed_candidate；此文绑定不自授 reviewed。接口绑定后的实现贡献由原 owner 投入 docs/architecture/contributions/531-task-delivery-lifecycle.md，再绑定其实际内容identity；shared current只由promotion owner按expected current串行更新，本设计不晋升baseline。

| Required concern | 适用性与本候选事实 |
| --- | --- |
| authority-binding | applicable：guru-maintain-architecture-baseline:planning:3.0、candidate_assessment/final_plan、current .86、change-contract-v1；若演进fresh重读 |
| constitution-binding | applicable：current constitution，公共模型单authority/薄projection/迁移退出是实际必要职责 |
| boundary-and-decision | applicable：Task开发owner退役、Delivery承接、两仓边界；ARCH-GOV-006..009、ADR-005/009，修复候选接口与D1准入已绑定，D2切换证据待补 |
| owner-and-single-writer | applicable：上游公共writer、Guru原stage semantic writer、唯一Author、shared promotion单writer |
| compatibility-and-exit | applicable：旧active/archived/API/安装支持，I08及本章删除条件；不新增永久双写 |
| gap-and-deviation | applicable：现有ARCH-GAP-006/008职责需独立owner判影响；不先宣称关闭；新旧authority混用不得扩大 |
| parallel-scope | applicable：#531独立Task；#292/#530只读引用，禁止覆盖其候选和shared current |
| evidence-and-freshness | applicable：before为Task路由+cycle事务，after为公共Delivery+原门禁；I01..09与installed/native证据待补 |
| review-and-promotion | applicable：必要ADR候选为owner与兼容退出决策，基于固定接口独立审核；未review/promotion不得Publication |

ADR候选只讨论“公共Delivery是唯一执行authority、Guru私有事务保留及旧Task阶段退出”这一实际owner变化；不编造ADR编号、未来插件或状态引擎。项目check协议为change-contract中的guru-trellis-architecture-convergence/1；Planning审查当前设计，Phase2审查实际before/after，Branch Review独立从完整committed range重算，promotion diff再走fresh gates。

### 9.1 必要 ADR 候选：公共 authority 与旧 owner 退出

Task-local ADR candidate identity 为 531-delivery-authority-owner-exit-candidate-v1，adr.required=true，locator 为本 design.md 的本节；正式调用的 regular-file locator 使用上面的 contribution_locator，段落由本标题定位。它是独立 owner 待审候选，不是共享 current ADR 或已完成 promotion。

当前决策差额是 Task 开发阶段及 cycle/事务承接转为上游 Delivery aggregate 的唯一公共 authority。保留 Guru 已存在的语义判断、私有发布事务、历史归属和收尾责任；Creation/Activation 两个闭环分别拥有实际创建关系与接受后转换，Approval 不占公共 Planning writer。替代方案“Guru自建Delivery状态”和“永久Task-status fallback/双写”会竞争公共 authority；“直接使用原生门禁替代Guru全部门禁”不能保留现有 policy/consumer，因此不进入本候选。

迁移代价是原固定发行安装到 schema2 安装的一次数据及公共 I/O 演进；版本诊断在应用前发生，D1只允许受控 opt-in 集成，D2与Guru私有迁移就绪才切换旧安装。退出条件是本设计第8节与 implement P5 的对应旧consumer已迁移及 installed/reapply证据成立；保留历史读取只服务明确原owner，旧开发writer退出。ARCH-GAP-006/008 的适用性、是否关闭与后续贡献由 Architecture owner 根据实际before/after核验，当前不宣称关闭。后续 committed Review、promotion及其新增diff重审仍按当前合同执行。

## 10. 当前设计与执行边界

中文职责设计、迁移策略、writer/consumer、版本化I/O、返工/退出、事实恢复/失效及联合验收按本文收敛；当前仍待正式规划审查，不以文档存在宣称完成。当前 candidate 与副本迁移绑定 §17 mixed候选及§17.2局部内容投影，基础公共接口沿用 §11；仍须 fresh 独立 Architecture、Wording、qualifications 及 Planning Approval。同 Task 活动机制重规划通过后，由旧完整执行 owner 按 resume_execution 承接，不重复首次激活。actual wrapper/adapter 与 private 迁移验证是实施产出；旧安装实际切换必须等待自身匹配证据。本文不自授 pass，不冒充实现、joint 或原业务恢复。

## 11. 历史最终5181来源与沿用的基础迁移合同

### 11.1 历史精确来源与旧证据

上游最终 source fingerprint 为 `5181ab6671cc2ed441feaa33e080f830e57c4f8266d927355cf69d272b85d77f`，
包含 HEAD `8822539b319b97dc91650a2de6a2b19e2471b552` 与最终清单冻结增量；fingerprint不是Git SHA。
产品已合入 PR #34（`bd18d5c91ffb10e3ee9e783f04dadc5cb3fccd14`），最终main/PR #35为
`780819aa98057038a7d6e21b5d66c11d61c23518`。#31 已独立 COMPLETED；其完成不授予 Guru 门禁。
CLI/Core版本为 `0.7.0-castbox.3`，API1/schema2；最终CLI tar SHA为
`6763278a436c754e9d97e85d9ae953983541b97041e0f0d167a9b8cde0434c16`，
Core tar SHA为 `45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`。
实际来源与包定位为上游最终 candidate manifest、independent-final-package/evidence及归档#31 implement；
逐文件核验CLI713/Core270与包相等。两轮最终独立审查与上游CLI2178/Core475属于上游证据，
不是本仓重跑、Guru joint或原会话实际恢复。

原077 source `077bb02966156b10f5d7477fedd9d6f8c2953dcd113434cf2ff48393307f2c25`、
CLI `d09b905a539a0f695d2d2d603eeb20fdd925e98d81f710f04af754fed013e20d`及原Planning/installed
证据保持各自身份；research/candidate077-private-migration.md不覆盖。ce363/B05真实失败不重标通过。
两个source manifest逐entry对比CLI source/test共24路径变化；installed CLI树单独比较25路径不同，
两种基线计数不混用。Core及公共Delivery schema/operations/store/session/runtime_contract保持相同；
Plan2 signatures与projection validator兼容，模板、init及session实现不同，不沿用旧templates identity。
旧SDK /task、Plan1、显式legacy workflow隔离保留；最终退休由上游后续breaking release负责。
#531仍须完成自身matching joint，不以#31 CLOSED代替该门禁，也不将Guru验收设为上游结束前置。

### 11.2 公共 Plan 2.0 与唯一 writer

公共定义引用 installed CLI `commands/migration2-schema`、`commands/migration2`
及 Core `/task/migration-v2`，不在 Guru 复制 schema/model 或推导阶段。真实签名：
`collectMigration2Templates(root, reviewedSources?)` 返回 prospective Map；
`migration2TemplateCandidate(files)` 返回 templates candidate identity；
`migrate2(options,input)` 由 CLI `migrate --from <live-version> --plan <file>`
按 schema_version 2.0 分流；Core `validateTaskV2Projection(source,projection)`
只校验原语义 owner 给定的完整转换，不自行决定 Delivery 归属。

| 数据/动作 | 语义 writer | 确定性 consumer 与恢复 |
| --- | --- | --- |
| 完整 occupied active/archive、安装、workspace/session、templates/workflow 与 artifact dispositions | Upgrade 原 owner 盘点；Task/scope、阶段、历史 owner 分别给出各自事实 | 上游 Plan2 校验原 raw bytes/modes、目标及所有 occupied 记录；缺失不自动补齐或重冻结 |
| Task/Delivery 公共转换、schema3 session、规划路径和 receipt ownership | 各原 owner 给出明确 public projection | 上游唯一 executor；Guru 不解析或重写其状态算法 |
| Guru custom workflow | Guru workflow/Upgrade owner | 显式 template_id=guru-team；通过实际声明/bytes，移除旧 bundled native receipt claim，不冒用 native identity |
| 旧 cycle/PR/merge→DeliveryKey | Publish/Merge/history 原语义 owner 核验唯一 Task/generation/candidate/实际远端事实 | 只投影原 private transaction 必需关联；active公共历史结果仍由原producer执行；archived完整历史事实在prospective Plan2目标记录中转换，见下文 |
| 没有 DeliveryKey 的旧 gate/DTO | 原 Planning/Check/Review/Readiness producer | 不能机械加 key 变成 current pass；保留仍有效内容/历史，fresh 重入最早受影响 owner |
| 旧 Completion/Closure/Finish 与 archive | 各原整体/收尾 owner | 足够真实前序才转换结果；否则 source snapshot/history-only；status/date不制造完成或允许Reactivate |
| 升级 writes/恢复/rollback | Upgrade 原 owner 审查上游实际 preview 和私有额外写集 | 备份完整多 workspace、archive、common/local session及自有 checkpoint原 bytes/modes；same-plan恢复，不刷新失败计划/rollback anchors |

最终包更换来源后必须由原Upgrade owner重新prepare：077的collector模板及fork checkpoint保持原来源供同计划恢复，不能换包沿用旧templates identity或重冻结原rollback anchors。最终包fresh init默认native-delivery-v1；custom workflow隐式reinit保留原workflow/mode/receipt，显式切换走原activation边界。schema2 task.py create/start只建立/绑定Task，不自动创建Delivery；Guru显式scope收敛、Creation与Activation顺序保持。session/Plan2盘点覆盖所有注册workspace及common/local session；上游只跳过Git明确prunable、路径不存在且无lexical .git的sibling，其余现存/损坏/foreign记录仍需正常诊断，不由Guru缩减盘点。

archived Task不能调用active store重复record_delivery；真实历史成功不依赖当前gate，但必须先由原Publication/Merge owner核验唯一归属并给Plan2 prospective目标record完整publication_result与delivery_result。PublicationFact携带Merge恢复consumer所需candidate关联，仅投影merge事实不足。转换后的原Merge owner核验exact公共facts、真实PR/commit message/parents/base后只读返回同结果；缺facts返回原stale_identity(delivery_result)，回该prospective转换owner。不得reopen archive、私写公共schema或制造currentpass。

普通 apply 仍阻止未迁移 active legacy writer；已完成 schema2 切换中保留的明确
history-only/deferred旧记录只保留身份和历史 consumer，不进入执行/选择/gate。
必须以实际迁移 dispositions 与当前 declaration 界定该路径，不能用任意旧文件存在
或仅相同版本号放行。migration preview使用 prospective Plan2 前置，不要求来源已
满足新普通安装合同；上游 dry-run/freshness 与原 raw source拒绝保持。

新升级 profile 与私有 plan 显式版本化：既有历史 Plan1 仅留迁移 consumer，不静默
解释为Plan2。新 `delivery_upgrade` profile 独立 input/schema，使用上游完整 Plan2
和各自原 producer 的最小私有转换输入。初次、resume、rollback仍各自独立；当前
新运行流不双读旧开发状态。正式 source_locked 继续要求已提交 clean来源；受控
local_candidate 的源头在 private plan 冻结 HEAD、完整 managed source bytes/modes
及包身份，副作用前逐项验证，结果明确 formal-source-lock未验证。不用dirty HEAD
或版本号冒充冻结内容，不为该临时验证建立第二可发布源 authority。

### 11.3 已提交 clean 规划迁移与事务恢复

当前来源以§17的mixed候选为准；本节及§12.3/§14的字节等价均遵循§17.2：默认严格原bytes/modes；仅显式 markdown_relative_links_v1 可接受同目标的确定性destination投影，其余bytes/modes不变。

Plan2 将旧 Task-root五份规划/context按实际 byte/mode 映射到某个明确 Delivery
planning_root，保留旧来源。映射本身不是新业务内容，不要求把新路径先提交。
仅当真实 Plan2 映射目标在旧 HEAD 缺路径时，TaskCommit 原 owner 保留供 committed_reentry 消费的最小 private 来源关联：
DeliveryKey、实际原 commit及五份 committed规划的repo-relative来源路径。
不复制内容/hashbundle、审查历史、用户过程或全量迁移ledger。首次创建该关联须由
本 owner根据实际 Plan2 write set和旧 Git对象审查，不从目录名/旧status猜测。

五规划映射不吸收安装产品差异。完整旧安装的真实tracked增量先按§13处置；零安装增量不提交，原业务候选不重复提交。随后clean接续时仍验证 stable Task身份/source/generation、current Check/candidate、
HEAD/base与无在途操作。当前五份规划必须等于正式来源commit中实际blob（或§17.2显式窄投影的精确结果），且原commit
是当前HEAD祖先；所选Delivery/公共scope与当前 plan_ref需一致。当前或原HEAD路径
本已存在时按原直接校验；只有真实映射缺路径时才读取该最小关联。内容实质变化走
dirty/fresh planning，不借迁移跳过Check/首次完整独立Review。正常dirty commit已
承载新路径后原关联consumer完成并退役，不将它扩为跨阶段批准token。

Publish/Merge旧事务的private来源绑定不能直接被改key。各原 owner提供有界migration
profile，审查同cycle、同Task/generation、真实candidate/PR/result和当前义务后，只
转换自身恢复输入的最小关联，保持已发生的副作用与原重试位置；失败同owner继续。
历史成功可先由原producer写公共事实，不能顺带制造当前门禁。没有唯一归属/真实事实
只阻塞该事务/场景，独立Delivery继续；不补provider、不建立永久cycle映射authority。

### 11.4 受控切换与 matching readiness

先构造真实旧形态前序，再在受控副本盘点并执行 fresh-reviewed Plan2/private转换、
新Guru整套apply、§13真实安装写集处置、public current/native continuation和原owner接续。
#149同Task活动replan、#444旧HEAD/root规划的clean接续、#155局部依赖保留分别验证；
不提前布置未来Delivery路径来使测试通过。多Delivery、返工/退出、noDelivery整体
补证据及输出丢失接续继续验证。旧 bootstrap manual若不属于新Guru PRprofile，
其原native owner可依据明确scope撤回记录stop/release；此安装准备不等于旧断点验收。

readiness只在上述实际consumer和exact pair定向验证足够后由Guru owner判断；缺项
准确返回接口/私有迁移/远端证据边界。上游原生/default采用与受控自定义workflow接口由上游owner独立验收；
旧API及legacy最终退休已移出#31范围。Guru不自授上游批准，不等待Issue CLOSED，
也不把本仓joint结果设为上游结束前置。remote Publish/Merge真实成功、原业务
会话实际迁移及完整Release矩阵分别保留边界；局部模拟不冒充远端成功。

## 12. #292 唯一 Author 的对象迁移与完整入口

### 12.1 Task 整体需求与 Delivery Planning 分离

本节为 #531 待实施、待独立评估的 Guru API 演进，当前 legacy 安装不能调用。
上游 installed task_store.cmd_create 在 schema2/no-start 创建 accepted_scope=null 和
root PRD seed；create_delivery 明确要求 scope_ref.authority 等于 accepted_scope。
当前 canonical create→Author initial_review 仍按 Task-root 三文档，而 scope projection
在 Author 前读 authority；若要求先有完整 Task 规划才能发布 scope，正常首次入口形成
循环；若直接把 seed 当 scope 收敛，则丢失 #292 的唯一需求 writer。不能从这个缺口
推导上游缺 API：公共 accept_scope 已存在，缺的是 Guru writer/consumer 次序。

同一 guru-author-task-plan 新增独立 task_scope_requirements profile：输入仅 mode、
task_ref、原 Clarify 的 source_selection/revision_refs；正向只收敛 root prd.md 的整体
需求、总体验收和来源定位。不得写 root design/implement/JSONL，不要求 DeliveryKey，
不进入 Architecture、Approval 或实施；因此没有 Task Planning 状态或第二方案 authority。
root PRD 是当前来源的整体需求视图，公共 accepted_scope 仍是唯一接受关系；不能用
文件存在推导接受，不能把切片政策/实施步骤写到 root PRD。该 profile 的资格只覆盖
需求收敛本身，真实产品选择仍回 Clarify，方案资格留给 Delivery 八 profiles。

独立出口 scope_requirements_ready 只含 task_ref 与 root requirements_locator；唯一
consumer 是原 Clarify 的 Task-scope continuation。它 fresh 读取该正文和原 source
selection，作整体 scope 判断，使用 installed AuthorityRef 真实定位/版本调用
accept_scope；输出复用版本化 scope_ready 语义并交显式 Creation/受影响 Delivery router。
原 Clarify 不写 PRD，Author 不冒用公共 task_scope owner_id，projection 不判范围。
source selection 为当前相邻 producer 提供，丢失回原 Clarify，不从 PRD/metadata 重建。
scope_only 也有 clarify_scope/blocked 两个原出口，分别唯一回 Clarify/stop。

新安装新 Task：Clarify 当前来源→Task create/C4/C5→Author scope-only→原 Clarify
accept_scope→Creation 一个明确切片/上游 UUID→Delivery Author initial_review。
整体需求修订：Clarify 先判真实 scope 与 source_selection→同 Author scope-only→
原 Clarify 发布新 authority→受影响 Delivery owner 合法 rework/退出；尚无 Delivery
时按实际义务进入 Creation 或 Completion，不自动造空 Delivery。Clarify 判断与公共
publication 分为同 owner 的前后两个闭合输入 profile，后者消费实际 scope-only 输出，
没有新增 scope 判断 owner。未变整体 scope 的技术返工直接 Delivery Author，不改 root。

整体 scope 已合法接受后的局部接续由当前原阶段 owner 独占：planning、check、
full_review、readiness、publication、delivery 使用各自 delivery_scope_revision
profile；implementing 由现有实施 adapter 承接。原 owner 读取实际 accepted_scope，
判断受影响义务及最早回程，然后薄投影既有公共 rework(target_role=planning,
scope_ref=当前 accepted_scope)。不得放宽 Author 对旧 scope_ref 的拒绝，也不得为
正常部分范围变化创建新 Delivery。只有当前 Delivery 的受影响门禁失效，其 candidate、
publication/delivery 历史事实及其它 Delivery 保留。delivery_scope_revised 的最小
输出仅交同 key 的 Author active_task_scope_change，不复制 scope authority 或 gate。
转换成功而输出丢失时由原 owner 读回同 key、planning phase 与相同 scope_ref 恢复
同一输出；这些事实只证明转换完成，不证明新规划已批准。

### 12.2 八个 Delivery Author profiles 与独立最小接口

所有原 profiles 保持原判断职责，以 delivery_<original_profile> 独立 schema 1.0
输入 DeliveryKey/task_ref；运行时从公共 resolver 取得当前 planning_root，官方
add-context --delivery 使用实际 UUID。三文档及两个 JSONL 均归该 Delivery；历史
计划用固定 Git 版本/公共归属读取，D2 不覆盖 D1。现有 task_ref 不再作为规划根目录。

| 原 profile→Delivery profile | 实际 producer 与新增必要输入 | 输出与最早 consumer |
| --- | --- | --- |
| initial_review | Creation created.key/planning_root、当前 source_selection | requirements_ready.key/candidate→Architecture candidate_assessment |
| active_task_scope_change | Clarify 的实际 scope_ready、revision_refs/source_selection、明确受影响 key | requirements_ready→candidate_assessment；整体 root 已由 scope-only收敛 |
| wording_reentry | Wording content_changed.key/change_refs | 等价措辞 plan_ready→Wording；实质方案 requirements_ready→candidate_assessment |
| approval_revision | Approval revision_required.key/revision_actions | 执行计划-only plan_ready；需求/方案 requirements_ready；真实 scope 回 Clarify |
| delivery_plan_revision | Delivery Review policy_gap 或 Completion next_independent_delivery；revision_refs | 同 key policy_gap 回实际方案依赖；next Delivery 先 Creation 新 key，再初始规划，不回写旧 key |
| requirements_revision | 原 Clarify source_selection/revision_refs、当前 key | requirements_ready→candidate_assessment |
| solution_planning | 原 Architecture 实际 candidate_assessment、key/authority route字段 | plan_ready.key→Wording，无重复 candidate pass |
| architecture_conflict_resolution | Architecture 实际 purpose/conflict_refs、key | requirements_ready→fresh候选评估，未决产品选择 clarify_scope |

requirements_ready 的 candidate 只为当前 design_locator 或实际设计事实与 constraint_refs；
plan_ready 只为 task_ref/key，不扩大全历史/hash bundle。两个返回 Clarify/stop 的输出
仅含原 consumer 必需的 reason/ref。消费方独立定义 Delivery input 并显式 projection；
不能让 consumer 读 Author owner-result 或把旧 Task profile 加 optional key。

### 12.3 purpose、接受、迁移及失效

Delivery requirements_ready→Architecture candidate_assessment 3.0→同 key Author
solution_planning→plan_ready→Wording planning_artifacts→Architecture final_plan 3.0→
Approval→当前计划展示/必要接受→Activation。候选 current 只回 Author；final current
只回 Approval。Wording change_refs、Approval revision_actions、Clarify scope_ready
按实际 producer 原值薄投影，只补 closed profile/current identity，禁止用旧 Planning2
或旧私有回程代替。Architecture/Approval 读取公共 planning_root、真实 candidate 与
最小 Guru freshness，不从 phase 推断 reviewed/approved。Activation 是唯一公共
planning role，写真实 accepted gate 后进入 implementing；不保存用户接受信息。

Author interface 从八 profiles/四 exits 演进为九 profiles/五 exits，采用新 aggregate
schema 2.0 与逐出口 consumer 并成套更新 registry/workflow/examples/platforms。
新增 scope-only不是新 Skill wrapper，它独立拥有完整需求写作、语义 gate、返工和
三个出口；八个开发 profiles 仍属于同 Author。旧 Task-root开发 inputs/四 outputs
仅留旧固定安装，受控迁移后退出；新运行版本不接受 legacy fallback，不静默改旧 schema。

旧 task-root PRD 同时含整体需求和 D1切片时，由原 Author 根据实际来源在受控副本
区分整体 PRD 与 D1规划；有真实内容变化必须回 fresh受影响Planning，不机械拆文本。
字节等价的公共 Plan2路径映射及已提交clean候选按 §11.3 消费原 Git对象，不为迁移
制造新提交。旧 Wording/Architecture/Approval 缺 key 的 pass不能机械补 key变当前pass；
旧提交/PR/merge事实保留。新 source/API、scope-only或回程机制实质变化均重新资格与
候选评估；本文新增机制不由之前 077 candidate assessment 自动授予通过。

正常 Check candidate_mismatch 的既有真实复现属于本次 projection consumer迁移：
普通内容修改后上游 verify_candidate 正确拒绝，Guru _binding 尚漏映射并报 internal_error。
保持公共模型与拒绝条件，在该原 owner 将 LifecycleContractError 映为现有 stale_identity
及原重入；不得靠隐藏 mismatch 放行。局部 cause资格与同输入前后验证在实施前完成。

## 13. 完整旧安装写集处置与 clean 前置

本节承接实际contract_incomplete及fresh candidate_assessment回程，是方案写作；不声称final_plan/Approval或事务执行完成。
真实旧Guru安装将workflow/scripts/platform受管文件纳入Git；完整Plan2/preset升级会形成真实安装内容增量，
不能把它们列为metadata例外。五规划文件的字节等价路径映射只由§11.3的原TaskCommit source bridge承接。

由原Upgrade owner在prepare/preview分别审查公共迁移、原私有迁移与真实安装写集，保留business commit及
五规划来源；安装内容增量属于安装维护工作，依既有task-free或用户独立Git操作边界，单独展示精确路径/HEAD/
消息与真实验证后取得该commit确认。它不是业务候选重复提交、不包含未来Delivery五规划、gate或无关文件，
也不产生TaskCommit/Check/Review pass。未同意该真实增量提交时保持升级结果与待处置边界，不制造clean。
原业务commit仍须是当前HEAD祖先；安装commit后refresh实际candidate与fresh Check，再由原TaskCommit
committed_reentry验证五规划source bridge、metadata/current scope及真实clean进入首次完整独立Review。
零真实安装增量时直接保留原HEAD，不新增commit。受控验证可提交其真实安装写集以证明这一合法前序，
必须明确与原business commit/规划映射分别展示，不预提交未来规划路径使bridge验证退化。

此候选不新增安装state authority、commit executor或fallback；实际安装副作用仍归Upgrade，独立Git结果与
workflow residue分报。正式业务树要由原owner另处理，#531不自动执行或迁移其它registered workspaces。

安装增量commit改变真实Git事实，原Upgrade恢复/rollback必须重新验证适用条件；不rewind Git、不刷新原rollback anchors，也不删除规划来源关联来伪造clean。§13只使用既有独立Git边界，不新增公共commit role、自动提交executor、metadata豁免或状态authority。


## 14. #530 已交付 clean 接续的来源处置与候选迁移

本节是对实际 d7cde2f062a25b43fe1f554b3187506457225820 的 contract.md、
committed-reentry-envelope/public input/output schema、runtime/committed_reentry.py 与
workflow post_commit 路由的承接。PR #540 merge 6cdcfbac、PR #541 merge bebf1993 是交付事实，
不授予本候选当前 Check/Review。本树已通过独立本地 base merge 承接 main@bebf1993，
current 为 .86/.89；原 .85/.88 审查仅为历史。原 owners fresh 重入当前规划，
不会重复 base merge、首次 Task 激活或修改 shared authority。

| 已交付来源的具体条件/接口 | 处置与 Delivery 候选落点 | 理由、直接 consumer 与失效回程 |
| --- | --- | --- |
| invoke --committed-reentry -，输入 profile/mode/task_ref/source_exit/phase2_commit_anchor | migrate：delivery_committed_reentry 明确 mode/task_ref/delivery_key/check_result_id；输出 committed 携 key、check_result_id、base_ref、branch_review_commit | same TaskCommit 唯一 semantic owner；Check 的公共 result 定位适用 candidate，替代旧私有 capture anchor，不将旧 DTO 自动解释成新 DTO；Branch Review 消费真实 HEAD/range |
| 当前 in_progress Task、唯一 checkout 与正式身份 | change：公共同 TaskId/generation/source 与唯一 C4 checkout/current Delivery/合法阶段 | Task 不再有开发状态；不能保留 in_progress 作为新路径门禁。current selection/Check 适用性由上游查询，identity 不符回原 binding/selection owner |
| 无 MERGE_HEAD、CHERRY_PICK_HEAD、REVERT_HEAD、rebase-merge、rebase-apply、sequencer 在途 Git 标记 | retain：TaskCommit 逐个真实 git-path 检查 | 原 Git operation recovery 先完成；不创建重复 commit 或强行跳 Review |
| 全 worktree clean（含 untracked/index） | migrate：完整 status；仅 reviewed_content_metadata_path 明列的公共 Task/Delivery metadata 与五份规划位置变化可由等价来源校验承接 | 真实业务/installer/workflow/spec dirty 一律阻塞并回 exact dirty commit。§13 安装增量独立处置；五 blob bridge 不吸收产品增量或变更计划 |
| 非空 selected base_branch；origin/base 优先，无则 local base | retain：读取公共 Task record 的明确非空 base，不使用 dirty prepare 的 main 缺省 | 缺失返回 stale_identity/base_branch，原 base/binding owner 解决后 fresh Check；合法明确 base 才继续。历史 nullbase 默认通过只属于被替换候选 |
| base commit 为 HEAD 祖先、HEAD 不等于 base、base...HEAD 非空完整 diff | retain：实际 base_ref/HEAD/range 验证 | 不满足回当前 base pair guard/Reconcile；整合后受影响门禁重评，不能拿旧 capture 承接新 HEAD |
| HEAD:task.json 与当前 Task metadata 整体相等 | change：HEAD 中稳定 id/generation/source 保持一致；公共 scope/base/Delivery relation/results 等合法 Plan2 metadata 由公共 authority、当前 Check 与来源读取验证 | 公共 gate 写入不应制造重复业务提交。不能仅稳定 identity 就放行：当前 accepted scope/obligations/plan/candidate 必须由 applicability 与 verify_candidate 约束，真实 scope/plan 改动回最早原 owner |
| 原 Phase2 checker passed、checkpoint mode/task、HEAD/capture/public anchor 三者相等 | migrate：正式 Check result_id 精确匹配当前公共 slot，gate_applicability=applicable，verify_candidate 验证内容、history、base 与 planning；candidate.head_ref=实际 HEAD | 公共结果唯一 authority；不写第二 Phase2 checkpoint。陈旧/丢失返回正式 Check owner，不从阶段/文件推断 pass；旧 checkpoint 只归迁移 consumer |
| 真实 HEAD 已含 root 五规划 | migrate：先读当前公共 planning_root 的 HEAD blob；仅真实 Plan2 路径搬迁缺 blob 时消费原 TaskCommit 最小来源 bridge | 原 source_commit 五 blob 字节与当前文件等价才承接；真实改动走 dirty 路径。不预提交未来规划、不制造空 commit，业务 candidate ancestor 保留 |
| semantic gate passed；revision-required/blocked 保持 | retain：AI 对 candidate、source、scope、base、完整证据与 migration 差额亲自审查，再由 validator 校验 | runtime 成功只证明客观事实；metadata 排除不等于完整 Check 或独立 Review 通过 |
| committed 输出进入 post_commit pair guard，然后 fresh Branch Architecture 与首次完整 independent Branch Review | retain：薄投影到相同 owners；Branch Review 明确 delivery_full_task_branch_review 与当前完整 base...HEAD | continuity/Check 不替首次 Review；clean 路径不 stage、不 commit、不重写 HEAD。基线变化回 Reconcile，finding 回实施/Check |
| 原 checkpoint 消费后 unlink，丢 stdout 回原 producer | migrate：不删除公共 Check 事实；公共 result 由各原 owner 查询及 applicability 判断，TaskCommit 重读同 candidate 物化相同 committed 输出 | 保留可恢复事实；不重做提交、不创建私有 clean 状态或记录授权；当前门禁变化仍独立重审 |

该候选只迁移已交付职责，未声称运行验证完成。显式 selected base fixture 与完整旧安装
前序必须匹配最终冻结候选重新执行；缺 base 的真实旧安装必须得到准确诊断并交原 owner，
不得以自动填值当作原会话恢复。§11.3/§13 分别只拥有五规划来源和真实安装增量前序。

本次 base 新带入的 runtime/committed_reentry.py、committed-reentry-envelope 与对应
Task input schema、test_committed_reentry.py 及 eval helper 属于旧固定安装的 Task 合同。
新 Guru 候选不注册旧活动入口；原 TaskCommit/eval owner 逐项核对 direct consumer，
把仍必要的 clean、Reconcile 后 fresh Check、首次完整 Review 与丢输出行为迁入
Delivery 调用链，退出新包内无 consumer 的旧执行资产。历史 schema 若仍有明确
迁移校验 consumer 只服务该 consumer；不能仅因历史资产存在恢复 legacy runtime。
原已发布固定包与 immutable Git 历史保留，故不在其它工作树删除其资产。整合后
定向36项中旧调用的6 FAIL/1 ERROR保持真实结果，迁移后重新验证，不按旧通过替代。


## 15. 历史5181的注册工作树副本接口缺口与重入

本节承接原独立final_plan实际contract_incomplete的三个missing refs：
531-PLAN2-REGISTERED-WORKTREE-COPY-DISPOSITION、
531-PLAN2-UPSTREAM-OWNER-DEPENDENCY-AND-REENTRY、
531-EXACT155-DIRTY-PLANNING-SOURCE-CLASSIFICATION。整体需求不缩减；本节是原Author
的来源约束/候选修订，不宣称新的Architecture current、Approval或迁移执行成功。

本节记录5181候选当时的真实接口缺口和停止点，不是当前尚缺上游接口的声明；当前处置以§16为准。失败、raw来源和未执行事实保持。

### 15.1 当时的实际支持组合与缺口

同Git common-dir的两个注册业务工作树分别承接Task149与Task155；正常Git继承使
两树均保留两个同TaskId/generation0的Task1.0记录，task.json字节一致，规划在各
分支有不同版本。真实common BranchBindingStore能定位各Task唯一当前checkout，
metadata的branch为空不能推断未绑定。source149为exact_source、source155为
reference_only，selected base为dev。这些事实不能由Guru省略、改ID或复制覆盖。

最终5181 installed CLI migrate2 dryRun在完整workspace/Task盘点下报
Task identity collision 149-normal-price-promotion-current。只转换各当前checkout
中的Task、对非当前副本使用合法defer并保留source rawbytes/modes，仍报同错；
实际非空source的active history_only不满足location合同。预览未执行公共或私有
迁移，完整受控文件bytes/modes及原owner只读回查均未变。初次harness误标legacy
已纠正为Task1.0；无schema_version是该旧schema正常形态，误标失败不作为产品缺陷。

实际来源：上游780819aa packages/cli/src/commands/migration2.ts的全局identities
检查在disposition处理前，对每个valid source id入表；同最终installed
dist/commands/migration2.js:377–381一致。migration2-schema.ts只允许
convert_active/convert_archive/current/defer/history_only，没有能表示这些真实
active继承副本的合法处置。完整registered-workspace及occupied Task盘点又禁止
省略。§11.2的公共转换接口存在，不等于这一具体正常旧拓扑已可转换。

| 来源承诺 | 处置及当前落点 | Owner、依赖与退出 |
| --- | --- | --- |
| #31设计§8/§10.3全注册workspace/occupied Task/session盘点与原字节保留 | retain：Upgrade盘点所有真实副本及原binding；不任意合并各分支规划版本 | 公共Plan2原owner需提供已审查可安装的副本处置/唯一执行归属支持；具体API签名由上游确定，本设计不虚构接口 |
| 最终Plan2全局TaskId检查与现有五种disposition | gap：当前合法处置均不能承接真实active继承副本 | 停在原Upgrade prepare/preview，公共写入与Guru私有关联前；保持原完整安装/文件/Task身份/业务commit/session，返回原owner明确依赖 |
| #149/#155真实旧形态恢复验收 | retain：不能用单workspace或新bootstrap成功样本替代 | 上游交付这一支持组合后，原Author绑定实际candidate/API，fresh受影响candidate assessment、solution、Wording、final_plan、Approval及installed回归，再由原Upgrade判断切换 |

Guru只保留团队语义与薄projection，不在本仓实现去重/副本ledger、新公共身份、
临时authority或状态替代，不patch上游/已安装包，不删除来源Task或绕开全部inventory。
受影响迁移与matching readiness保持未完成；其它已有公共API上的独立设计、
consumer定向验证、#530职责承接和本地base整合准备可继续，不以#31 CLOSED
或等待Issue重新CLOSED作为重新设计的前置。来源候选改变时只刷新受影响依赖，
旧失败与各旧快照结果保持其身份。原业务工作树迁移仍由原owner另处理。

### 15.2 #149/#155当前规划与局部依赖事实

#149原HEAD e27bfb7e56dd62c46c9024b79e5c2b3d68f84ba4中五规划与当前字节一致，
但这只证明来源blob形态，不授当前Check/Review或迁移通过；其规划记载D3a/PR461
已交付、D2b为planning_candidate，继续同Task活动重规划。
#155原HEAD150f743eef8d81ac0f5188f582a10136c2d47acf含旧规划路径，但当前
prd/design/implement三份新内容不同于HEAD，两JSONL一致。属于真实dirty/fresh
Planning，不满足§11.3clean来源bridge；保留当前内容，由原writer/门禁/正常必要
提交路径承接，不造source_commit、预提交未来路径或重复历史业务提交。

#155当前规划记载D1/PR454已交付且remaining_work，P406-1/P406-2仅阻奖励恢复
与真实ELIGIBLE，独立查询工作可继续。该局部缺口不升级为全部工作停摆，
Plan2迁移阻塞也不授予接管provider业务。历史交付事实、当前门禁、受控接续
和原会话实际恢复分别记录；当前均未证明原owner会话恢复。

## 16. Plan2 副本补修的当前来源事实与候选约束

### 16.1 新候选的真实身份与证据层级

上游独立补修 Task `plan2-worktree-copies` 的设计、`research/quality-review.md`、
`research/final-verification.md` 与提交实读：产品提交为
`1e40014023de53ddfd9368b3fb4d0a7a31e92293`，父提交 `780819aa98057038a7d6e21b5d66c11d61c23518`，
[PR #36](https://github.com/castbox/Trellis/pull/36) 已合入，headRefOid仍为同一产品提交，CI build SUCCESS；merge状态不改变包身份。
原打包source manifest（排除Task文档）的1257项本地snapshot fingerprint为
`17ea37fbfcfe81a7e2c43f223cacdeee6ebd4c90cd28fff74c143a75bebd1a50`，不是Git SHA。
CLI tar `185ed1db6865b72138bb10b6d799225721bf50fddfb370f84d8ec330558f472d`；
Core tar `45bbfee507ed4964649610f703a90ba01c5f5cea21fb95d0845f92ed45302967`。
1255个regular source entries已核bytes/modes。另2项gitlink中docs-site原manifest记780819aa，产品commit实际gitlink为587a1c8d；marketplace均为7d5298d。该manifest是本地snapshot，不能冒充committed tree identity；本Task不修改上游manifest。迁移产品来源绑定上述真实commit、两份migration2源码与实际tar，继承的未初始化submodule目录不成为产品接口来源。
两包仍为0.7.0-castbox.3，API1/schema2/Plan2；CLI713/Core270个实际installed regular files
已逐项核验byte/mode与tar相同。相同版本/Core不使旧CLI/templates/plan等价。

上游独立审查无未解决finding，原owner全CLI2225通过/Core475通过和1optional skip、
受控packed installed四条跨checkout session/current/Delivery路由及preview/replay/rollback是
上游证据；本Task仅重新核验包与源码身份，不重复其full suite。旧timeout失败保留。
补修不重开#31，不以Guru joint为上游完成条件；PR merge、正式Release及本仓joint
各自不是上述本地candidate已审查可安装的替代证明。

### 16.2 必须消费的实际公共约束

真实定义在提交的 `packages/cli/src/commands/migration2-schema.ts:135` 与
`migration2.ts:604` 起；同源installed `dist/commands/migration2` 承接。
Plan2可选 `branch_bindings` 为 `{task_id,lifecycle_generation,source:RawSnapshot}[]`；
目标只由公共executor派生为common-dir下
`trellis/task-branches/<task_id>/<generation>.json`，不接受caller自定路径或改写binding。
每个已有binding的active projected Task及每个重复组必须有原bytes/mode快照。
public binding五字段schema/version/id/generation/revision/branch按上游校验；实际branch
须在完整eligible注册project roots中唯一checkout，并选择同一个active authority。

同Task继承副本只有exact id/generation/immutable source（含disposition）一致、
不同canonical roots/directories、一个active convert_active或current及其余active legacy
defer才合法。Mutable metadata/各分支规划可不同；all-defer、archive/history或实际身份
冲突继续诊断。原snapshot用于same-plan恢复，迁移后target不成为新source。
defer副本及其规划/raw mode、binding均preserve，不能添加其公共Delivery或migration资产。
只有唯一projected authority进入公共session/current解析；不是Guru自行去重。

已有Guru extension marker的Git roots按当前公共missing-binding合同要求明确binding；
unique active Task有live binding时同样需要reviewed snapshot。Git-free无binding支持
保持，上游不接受Git-free binding rows。正常binding/topology/branch/bytes/mode变化回
原prepare，不刷新旧rollback anchors或用锁保证。本文不扩张上游的失败矩阵/加固范围。

这些规范性来源约束在§1.1唯一矩阵retain，Guru具体承接如下。


### 16.3 原Upgrade owner的具体薄承接与停止点

原 `guru-upgrade-installation:delivery_upgrade` 继续拥有prepare/preview及私有迁移审查；
`runtime/delivery_upgrade.py`、`delivery_upstream.py` 只冻结事实、传参和执行原公共端。
新private plan冻结本节产品来源与真实安装包、完整managed Guru candidate及实际templates。
旧5181/077计划、已发生写集和rollback anchors保持原来源，仅由其原same-plan owner恢复；
新的185e来源必须fresh prepare，不能修改旧plan的包字段来绕过重新准备。

prepare完整列出所有eligible registered roots、occupied active/archive、原raw Task、
每分支的五规划、common/local sessions、安装receipt和workflow。使用原C4事实定位common-dir
binding，逐个冻结实际bytes/mode，薄投影成公共 `branch_bindings` 的三字段row。
row不包含target path或新的branch/revision值；固定路径、schema/group合法性、原snapshot
freshness和唯一checkout都由公共executor检查。已有binding的unique active Task亦提交row；
缺失或branch/topology变化交原binding/checkout或prepare owner，不静默填main或新建binding。
Git-free合法无binding组合维持原公共支持，不添加Git-free row。

对实读的同TaskId继承副本，Upgrade依据原C4与当前checkout给定一个实际active
convert_active/current，其他真实active legacy副本为defer，并提交完整来源和dispositions。
不由Guru合并分支规划、重写identity/source或实现group校验。公共executor若因immutable
source/generation不一致、没有唯一authority、非法archive/history组合而拒绝，保持原文件，
回原prepare/source owner给精确诊断；不能将不同任务伪装成继承副本。符合公共合同的
所有defer peers保留Task及其规划/raw modes/binding，不创建公共Delivery或Guru私有迁移资产。
同组Task只有projected authority进入session/current解析，各session row仍使用实际原来源。

公共dry-run返回的完整write set由Upgrade审查，再进行原public migrate2执行与自身私有
关联转换；私有事务/历史归属仍由原Publish/Merge/TaskCommit owner给定最小转换。
结果按原Upgrade已声明的migration/continue出口消费，不新增copy-specific出口、ledger或
私有状态authority。成功后丢stdout读取同一plan的公共/私有结果，不新建Delivery、不重复
写入；普通partial-write恢复/rollback依公共same-plan合同，绑定快照和旧anchors不重冻结。
本节不授予在原业务树执行迁移的权限。

### 16.4 新候选定向验收与事实层级

在受控旧安装副本fresh盘点和preview，随后按真实支持组合执行：有继承副本及原binding、
有binding的unique active Task、Git-free原合法组合；不重复上游full suite或完整失败矩阵。
核验唯一public current Task/Delivery、common/local session与实际registered checkout；
defer peers的Task/五规划/binding bytes与mode保持，且未新增Delivery或私有迁移资产。
真实binding/topology变更通过正常owner操作后必须得到prepare重入，不能手工伪造payload。
preview零写入、正常resume/replay/rollback保留原snapshot分别观察；public成功后的Guru
关联或stdout丢失从原owner接续，不能用副本preserve替代整体事务恢复证据。

#149仍保留真实已交付D3a和当前D2b候选，以五blob来源证明clean计划形态，再在同Task
当前Delivery fresh规划/接受进入实施。#444沿§11.3/§13/§14验证clean候选与首次完整Review，
不为路径迁移重复业务提交。#155真实dirty三规划保留，按必要writer/提交链承接，P406局部
缺口仍只阻奖励/真实ELIGIBLE，有必要consumer的独立查询继续；不自动实现provider。

上游包/source审查、Guru实现、matching installed/joint、原owner业务会话实际恢复是四层
证据。本节只完成当前设计；旧10/2项与d052/077样例不授予185e新candidate通过，当前
TaskCommit的6 FAIL/1 ERROR保留至真实consumer迁移后重跑。V01—V15、full Policy及
RDT .89/Architecture .86的原writer/promotion顺序不变。原#531运行安装仍是完整legacy，
尚未成套切换。真实远端Publish/Merge与原业务实际恢复单列未验证，不用本地模拟补pass。

## 17. mixed predecessor 安装候选与真实安装修复

上游新增可安装 CLI 绑定产品提交 98075f3af510c250508fc5ca62df172610048083；
其四份实施/spec 文件与打包前 source manifest 逐项匹配。CLI tar SHA256 为
5aeeb81ca72508081b7dd94ddb7a19f69444714f78b3a38858d908196cc77916，
Core 保持45bb，实际独立安装713/270文件的字节与mode全部相同。版本号仍是
0.7.0-castbox.3，不能只凭版本选择包。API1、Task2、Plan2、runtime templates不变；
仅 Plan2 source.task_schema=mixed 时，convert/defer 行显式提供实际
source_task_schema=legacy或1.0，current/history_only行不提供。原完整inventory、
history归属与私有迁移仍由原owners审查，不复制上游fixture计划。

PR #38 首次 Ubuntu CI 2284通过/1失败，失败为测试快照中的maintenance.lock变化；
上游原owner已审查夹具补修，产品包未变，新CI尚未取得。这不是Guru联合验收pass，
不以本地测试抹掉该失败，也不等待Issue重新关闭才设计或做受控安装验证。

scope原owner模块的真实installed调用曾因installer清单漏scope_revision.py失败。
修复仅补canonical受管runtime清单、source清单闭合校验及正常clean/reapply入口测试；
必须经原installer安装后重入同D1，禁止手补安装文件。旧失败候选与样本保留其身份，
新的受控source以实际bytes/modes冻结，不把base HEAD当正式source lock。

### 17.1 安装闭合与实际旧规划引用缺口

原 installer 的 MANAGED_SPEC_PATHS 漏 bootstrap-repository-ssot.md，导致真实 clean
apply 后 canonical drift 检查缺项。修复只补原 installer 的 canonical→installed
spec 映射，保留现有冲突、backup、reapply 合同；不手补 target，不放宽 drift。
同来源新副本 clean apply、reapply、三平台投影及原 drift 已实际通过。旧缺项样本
保留，历史失败不是新来源的通过证据。

真实 #149 mixed 迁移保持同 Task/gen0、三个已核验历史 Delivery 与当前 D2b，
原 e27 候选和五份规划 bytes/modes 保留；原 Upgrade、安装及 native continuation
已执行。但五规划从 Task root 搬到 Delivery planning_root 后，十个原相对 Markdown
引用失效。公共 Task artifact_origin 只拥有 Task/archive 的 typed AuthorityRef
定位，不定义这一规划文档的引用基址；TaskCommit 的私有五 blob bridge 只能由
TaskCommit 消费，不能扩为其它 Planning owner 的公共来源 authority。
在上游提供明确合法消费合同或可安装修订前，不声称该副本 Planning/Activation/
clean Review 已通过，不改业务规划掩盖、不重复业务提交、不建立 Guru 替代模型。

### 17.2 上游确认的 Plan2 内容投影与 Guru 来源等价合同

上游原 owner 已确认当前 Plan2 artifact target_content 可以承载薄内容投影，
但不存在自动赋予字节等价的公共接口。采用既有 Plan2，不新增公共模型字段。
迁移原 owner 逐文档核验原 Git blob 与相对引用的实际目标，将支持的 Markdown
链接 destination 按原 source 文档目录解析，再相对新 Delivery 文档目录投影。
只改变这些 destination 字符，正文、anchor/query、外部链接、context JSONL 与
文件 modes 不变。不存在的原目标、不能可靠定位的 Markdown 结构或有真实语义
变化，返回原 Author/迁移 owner；不得自动放行或泛化为通用链接引擎。

TaskCommit 自有来源输入/短期 association 增加显式可选
planning_projection=markdown_relative_links_v1；无该字段仍严格保持原字节比较，
原已保存 association 不自动升级。原 TaskCommit AI gate 独立审查实际 Plan2
write set、引用目标不变、Task/gen/scope 与五文件来源关系后才写该最小模式。
validator 从原 commit/source paths 与公共 planning_root 确定性重算投影字节，
精确核对目标和 Plan2；任意其它改动仍需真实 dirty 路径，不被归一掉。
clean 接续只由 TaskCommit 消费该私有来源；Planning consumers 只读正常可解析的
新文档，不读取 private bridge、不解释 origin。成功真实内容提交退役 association。
此为 #531 自有私有提交来源合同的明确兼容扩展，不改变上游状态 authority。

必须在新执行副本 fresh Plan2 执行，不篡改已完成旧 plan/recovery；保留十链接失效
样本及原失败。实际证明引用目标、正文其余 bytes、历史事实与原候选 ancestry，
然后由原 owners fresh Planning/Activation/Check/clean/首次完整独立 Review 验收。

§17.2 支持形态限定：UTF-8 Markdown 普通 inline `[label](destination)` / image destination，可带 `<destination>` 和普通引用标题；保留 query/fragment、外部 scheme、绝对路径、fragment-only；不改 fenced code 与 inline code。相对 destination 不含空白、转义或括号，原实际文件目标须存在。reference definition、无法可靠定位的语法交原迁移/Author owner，不自动归一化。JSONL 始终逐字节保持。当前 source-disposition 矩阵中旧185e身份只保留历史用途，实际新实施以§17 mixed CLI/Core包及本节局部兼容差额为准。
