# #292 设计：唯一 Planning Author 与真实 Phase 1 集成

## D1 Authority、边界与当前对象

Direct Source 为 [#292 current body](https://github.com/castbox/guru-trellis/issues/292)，本轮读取 `2026-10-10-r27`；requirements 在 prd.md，执行安排在 implement.md。正文明确未引入历史 comments 为 current authority，因此本轮不把历史 comments 当规范来源。

项目 Architecture authority：`docs/architecture/README.md`（本轮 active `current-main-0.6.17-guru.83`）；constitution：`docs/architecture/00-foundation/design-constitution.md`；change contract：`docs/architecture/06-governance/change-contract.md`。RDT authority 从 `docs/requirements/`、`docs/design/`、`docs/test/` 的 current manifests fresh 读取，本轮 `current-main-0.6.17-guru.84`。这些身份只描述当前轮，不冻结后续 main。

首次规划的创建基线背景（非当前候选的接口声明）：该基线的 canonical `trellis/skills/guru-team/registry.json` 无 Author，workflow 的 Planning Architecture 唯一回 Approval；Architecture 2.0 impact current 要求真实 contribution 与 reviewed_candidate，不能表达 contribution 尚未产生的前置候选评估；三个 qualifiers 的 planning_scenario_set 固定 caller=Approval，要求现存三份 docs。当前未提交候选已安装 D3/D5/D7 所设计的 Author、目的专属 Planning 3.0 和 qualifier 扩展；这只说明候选接口状态，不证明实际行为或验收通过，不以旧 profile 代理 Author。

仅迁移 Phase 1 集成。Clarify 保留需求意图/来源角色/真实选择，Discovery 保留 context evidence，Architecture 保留独立判断，Wording 保留受控 rewrite，Approval 保留批准，Execution 保留 activate/resume_execution，Delivery/Completion 与 promotion 保留原职责。脚本只校结构、当前文件/身份/receipt、唯一映射；来源语义、充分性、路径选择和 pass 由 Markdown Skill 中的 AI 完成。

## D2 来源设计处置矩阵

下表是唯一长期来源设计处置载体。来源定位均为 #292 current body 的具体章节与条款，处置 retain 表示保留原语义；本轮没有改变或拒绝其规范承诺。字段与 API 版本是本规划的实现细化，不修改 source。后续 change/reject 必须在本表记录差异、理由、影响与上游处理；产品/scope 回 Clarify，Architecture 决定回 Architecture owner，技术约束不能靠 task plan 接受覆盖。

| 来源定位 | 原承诺 | 处置 | 当前落点 | 理由、影响与上游处理 |
| --- | --- | --- | --- | --- |
| 唯一 writer 与边界，第1-3段 | Author 单写三份 docs/官方 JSONL；Wording、Approval 独立；只迁移 planning 集成 | retain | D1、D3、D7 | 不吸收上游或执行/终态职责。 |
| 来源设计显式承接合同，第1-3段与表格 | fresh 读真实来源；区分规范设计与建议；逐项定位与处置 | retain | D2、D4 | 本表不复制进 prd/implement；建议不自动成为约束。 |
| 来源设计显式承接合同，retain/change/reject及最后两段 | 真实偏离有理由及上游处理，Approval 逐项检查 | retain | D2、D7 | 普通技术细化直接处理，真实约束变化不静默处理。 |
| Closed Author profiles 与当前入口，八行 | 八个 profile 独立闭合 input/exit/consumer | retain | D3 | 两种 Delivery reason 使用同一 profile，保留两个 router。 |
| 同节 Completion 各出口段 | remaining_work/evidence_pending/requirements/implementation 各归原 owner | retain | D8 | 不虚构 Completion plan_revision_required。 |
| 同节公开 I/O 段 | 最小 handoff，consumer 拥有 input，无 private aggregate | retain | D3、D5 | 只有当前 consumer 所需候选事实跨前置边界。 |
| 实际入口集成与 Phase 1 sequence，第1段 | 所列 docs 状态与恢复到 Author 或 resolution/stop | retain | D4、D8 | 不从文件齐全推导批准，不重置任务。 |
| 同节 brainstorm 第2-4段 | 加载/方法复用成立，不能竞争写作、重复澄清或例行确认 | retain | D4 | upstream trellis-* 不 patch/delete。 |
| 同节 sequence 与其后两段 | requirements_ready/plan_ready；Wording 后最终 Architecture 相邻回 Approval | retain | D5、D7 | 保留一个 Architecture owner及current router。 |
| Requirements convergence 与前置 Architecture，第1-3段 | 先 PRD；substantive design/implement 前真实候选评估；独立隔离 | retain | D4、D5 | candidate 不等于已存在 contribution，不输出虚构 reviewed_candidate。 |
| 同节最后两段 | 两个回程；sync/repair 重入原目的；最终 current 独立判定 | retain | D5、D8 | 前置 DTO 不跨写作/Wording 重放，最终不回 Author 循环。 |
| Architecture alignment 与 task-local proposal，第1-3段 | current refs、impact/path、真实贡献和必要 ADR | retain | D9、D10 | 任务内 proposal，本轮已有 impact，最终独立 owner决定。 |
| 同节 serialized promotion 段 | 首次 committed full-diff review 后晋升，再复查 | retain | D9 | 不在 planning 晋升 shared current。 |
| Delivery Policy 与 Docs SSOT Plan，full/partial/staged | implement 唯一 policy，Delivery 和 Completion 不代写 | retain | D6 | 本任务 full；另外两策略属于 Author 必须支持的行为。 |
| 同节 Docs Plan 段 | 四策略，RDT owner 单写，delta 在 final Phase2前 reconcile | retain | D6、D9 | implement 定义本任务计划，design 不复制执行 policy。 |
| Qualification、Wording 与 Approval，第1-3段 | 三 qualification owners、七 Wording语义、独立 Approval | retain | D7 | 新 Author candidate profile 不冒充旧 Approval profile。 |
| 同节最后段 | 不以固定调用数代替真实门禁和重入 | retain | D5、D8 | 有真实变化时重做依赖门禁。 |
| Freshness、恢复与活动重规划，第1-3段 | 依赖范围失效、同任务恢复、#468 resume、不吞执行修正 | retain | D8 | 不新增生命周期或恢复 store。 |
| 同节最后段 | 最小 call-local/private状态，无ledger/cache/授权 | retain | D3、D5、D8 | candidate只在当前调用链内，消费后释放。 |
| 迁移与完成标准，第1段及1-10 | 必须真实激活、退役旧边、正常 prompt与来源 A-D/native证据 | retain | D11、D12 | package通过不等于Issue完成；implement列验证入口与缺口。 |
| 迁移与完成标准，最后段 | 定向验证，最多一个clean throwaway，Release分离 | retain | D12 | 不执行完整累计矩阵或发布。 |

## D3 Author package 与最小 public I/O

新增 stable id `guru-author-task-plan`，`judgment_mode=semantic`。每个 profile 执行：读取当前合法 input/identity/authority → 正向收敛或写作 → AI Review Gate → 仅真实 choice/副作用的当前对话 → recorder/validator → 一个 typed exit。无 tracked gate report，无新增持久化。canonical package 位于 `trellis/skills/guru-team/packages/guru-author-task-plan/`，interface 注册真实命令、独立 schema 和唯一 consumer；安装投影沿原 preset。

每个输入是闭合 schema。共同 identity 为 mode、task_ref；generation/source/checkout 从原 live owners验证，不另建身份。首次 source_selection 若仍在相邻前序结果中，由 current入口薄传；丢失则回原 Clarify/context producer fresh 恢复，不从 PRD/metadata重建。source_selection 使用当前 #250 数据 shape，不创造第二 source 模型。

| Profile | profile专有输入与正向职责 | 正常出口 |
| --- | --- | --- |
| initial_review | current created/current Phase1 source route；收敛需求并形成真实 call-local候选 | requirements_ready |
| active_task_scope_change | 实际 scope_ready 的 source_selection/revision_refs 经原 router 薄投影；保留任务身份并重做受影响需求 | requirements_ready |
| wording_reentry | Wording content_changed 及受影响规划 reason；reread三份 docs并判断最早依赖 | requirements_ready（设计事实变化）或plan_ready（仅等价措辞） |
| approval_revision | Approval revision_required 的最小 revision actions；修订业务规划，不代替批准 | requirements_ready（需求/设计变化）或plan_ready（仅执行计划缺口） |
| delivery_plan_revision | 两个 router各自投影 reason：delivery_policy_gap或next_independent_delivery，加原owner返回的具体缺口；保留总scope | requirements_ready或plan_ready，按真实依赖变化选择 |
| requirements_revision | 原 requirements router完成Clarify后的当前 source route/reason；不得携带Author预选需求决定 | requirements_ready |
| solution_planning | 只接受candidate_assessment的实际baseline_current薄投影；生成design/implement及官方JSONL | plan_ready |
| architecture_conflict_resolution | 原Architecture规划router的实际conflict/contract gap与目的；需求冲突回Clarify，机制冲突修订当前候选 | requirements_ready；真实未决scope则clarify_scope |

所有 profiles 还声明 clarify_scope 和 blocked，分别交原 `guru-task-plan-clarify-scope-router` 与新具名 stop `task-plan-author-blocked`。原因是缺scope选择或真实authority/input缺口，不以缺本次owner result请求例行确认。

requirements_ready output：exit_id、task_ref、candidate。candidate仅含 `design_facts`（当前评审对象的最小机制/责任事实）与 `constraint_refs`（直接source locator），用于无design文档时Architecture读候选，不含PRD叙事、验收/已批准结论。已有设计则candidate分支为 `design_locator`；两分支独立schema，不能大量nullable。唯一consumer为现有Architecture planning入口，其独立input由薄projection加planning_purpose=candidate_assessment及fresh live authority。该候选是当前调用内的对象，不写另一个proposal文件、URI resolver或缓存。

plan_ready output：exit_id、task_ref。Wording consumer由task_ref构造其固定三份文件input；Author不输出重复文件列表、scan或digest。clarify_scope只输出task_ref和具体scope question refs；blocked只输出task_ref和真实missing_refs。profile/input绑定留在owner调用验证；router不用reason文字分类。

## D4 Author 写作与原生入口

requirements_convergence 先fresh读取D1与source roles，完成prd；对所有load-bearing接口、顺序、owner、兼容承诺建立当前调用内候选。无规范设计承诺时写依据，不制造空矩阵。不得以适配current Architecture为理由静默降低需求。调用D7资格owner后，形成requirements_ready进入D5；前置current结果返回solution_planning才写实质design/implement。Architecture incomplete按既有router修订候选；不得假称它是baseline_current。

solution_planning编写D2矩阵、当前方案、Architecture任务贡献、implement唯一policy/Docs计划，并用原task.py add-context维护implement.jsonl/check.jsonl的业务语义。task.py是确定性writer；Author拥有context选择，不能让上游brainstorm成为另一个业务writer。

Current create/start/prompt/continue/resume以及压缩后流程先做原TaskId/generation、session binding与checkout resolution。status=planning进入initial_review；in_progress只在planning authority变化时进入对应reentry；其它状态保留原route。no-PRD、PRD-only、design-only、three-doc、official seed、partial/stale均由Author读取当前状态并按缺口收敛；文件数量不是批准或identity依据。mismatch返回resolution/stop，不建替代task。

平台发现或选择trellis-brainstorm后，加载当前Guru workflow的Phase1 dispatch，再由Author写作；方法复用不触发第二访谈、第二规划或planning consent。真正新scope选择回Clarify。修改仅在Guru自己的workflow/Skill/thin入口，不patch/delete upstream trellis-start/continue/brainstorm或hooks；如果真实native验证暴露只能上游修改的阻断，报告精确入口与上游依赖，不能声称#292完成。

## D5 Architecture planning 3.0 的目的专属迁移

同一 `guru-maintain-architecture-baseline:task_impact_sync`，仍stage=planning、四profiles与七exits。新planning 3.0 input要求 `planning_purpose=candidate_assessment|final_plan`，两种input独立schema：前者包含D3候选，后者只指当前design locator。保留原 baseline/constitution/change-contract/continuation freshness字段的当前直接consumer；不新增lifecycle stage。interface/aggregate按精确version+stage分派。

candidate_assessment baseline_current 3.0 output只投影现有current router消费的task、purpose、source_profile、current authority refs及Author写作需要的impact_kind；impact分支带change_path、必要ADR的decision refs/理由，no-impact分支只带理由。前置owner对真实候选执行现有独立方法及project checks，但不要求未来contribution，不输出reviewed_candidate/promotion_state，不假称贡献被审查。full check facts与候选绑定留在该轮owner证据，不进handoff。Author基于当前assessment编写真实贡献；这条输出不能被Approval或publication解释为current最终规划。

final_plan input基于Wording后的实际design和current authority。其baseline_current 3.0 output保留当前final消费所必需的contribution locator/identity、current binding、impact/change_path和promotion_state约束，要求真实reviewed_candidate或合法promoted状态；无impact仍不制造贡献/ADR。最终评估按Architecture合同选择适用的fresh独立评估，不由caller改前置DTO补造。唯一current router按purpose：candidate_assessment→Author solution_planning；final_plan→Approval。最终结果与Approval相邻，Author/Wording之间不转发它。

其余六个出口的planning 3.0目的绑定同轮input并在重入中保留：sync_required回原Architecture；baseline_incomplete回原bootstrap/repair再fresh评估同目的；architecture_conflict/contract_incomplete回原planning router的Author conflict profile（需求冲突再Clarify）；fitness_regression保留原check/修正语义，不能作为planning success；blocked原stop。未知、多出口、purpose/consumer mismatch fail closed。bootstrap/repair本身的2.0current不能冒充planning 3.0，router重建同purpose的新task_impact_sync调用。

迁移是direct evolution：planning 2.0入口在切换后退役，旧无purpose planningDTO不猜回程；中断的旧Planning调用fresh进入新owner。非planning的task_impact_sync、bootstrap/repair/promotion保留合法2.0，无双planning parser、fallback或legacy writer。更新全部受控消费者、schema登记、例子/eval/readme和安装投影；新schema id与migration文档明确版本差异。project change-contract对新planning3.0的绑定属于任务贡献，先不改shared current authority；非planning2.0绑定不变。最终晋升时由原Architecture owner将该限定事实加入shared change-contract，不把全仓合同强改3.0。

## D6 Delivery 与 Docs 的设计承接

Author支持full/partial/staged；各策略的完整执行定义仅在implement.md。partial输入必须有独立slice理由、remaining work与Completion条件；staged必须有有序stages/current stage、entry/exit、remaining stages与最终条件。缺/含糊/越界回Author修订；Delivery Review只判断slice符合policy，Completion只判断整task。两者不临场创造policy，不新增ledger。

Docs SSOT仍是ssot_first/delta_first/bootstrap_or_repair_docs/no_docs_update_needed四个决策值。Author规划，RDT owner单写durable authority和reconciliation；no_docs_update_needed不是Skill exit。该任务选用策略及落点只在implement.md；delta_first最终Phase2前reconcile。

## D7 Qualification、Wording、Approval

三qualification owners新增closed `author_candidate_set`，caller固定guru-author-task-plan，input以当前task+candidate refs/source与实际候选locators绑定，写作前不要求不存在三份docs，也不伪装Approval。它们保留现有planning_scenario_set给Approval和全部非Author合同。Author先消费normal/solution实际结果，再以eligible refs调用root；ordinary feature得到其 applicability disposition。没有新状态文件或资格缓存；scope/mechanism/diagnosis/blocked走原owner映射，mechanism删除/替换不自动成为scope选择。此前 #292 规划资格沿当时已安装合同完成，不将旧结果改称新 Author profile 的执行证据；本次局部方案写作按 D9.1 的真实前置 Architecture 结果交原 Author。

Wording固定审三份current docs并执行其七个planning维度；pass router进入final_plan Architecture；content_changed经原change router回Author，按实质变化fresh从最早阶段重做；未知exit停止。

Approval current八维review不变，增加显式逐项读D2：规范承诺是否完整、retain是否有具体落点、change/reject是否有rationale和完成所需上游处理，policy/Docs计划是否唯一明确。不得以provenance=true代替。只消费final_plan matching currentArchitecture结果；前置结果不能批准。approved仅证明语义充分，consumer仍是原展示/对话接受/pair guard→Execution；批准和接受互不代替。

## D8 依赖失效与两条 Delivery 回程

| 实际变化或原出口 | 精确承接 |
| --- | --- |
| source/scope规范变化 | 原Clarify→scope_ready→Author active_task_scope_change/requirements_revision→受影响资格与候选Architecture→写作→Wording→final Architecture→Approval |
| 仅设计机制变化 | Author候选→fresh候选Architecture→写作和依赖门禁；不重复未变需求访谈 |
| 仅等价措辞变化 | Author wording_reentry reread→完整current Wording→final Architecture适用性判断→Approval；不重做不依赖它的资格 |
| Approval revision_required | Author approval_revision，按具体revision actions失效依赖阶段 |
| Delivery Review planning_revision_required | 保留guru-task-delivery-planning-router，reason=delivery_policy_gap→Author delivery_plan_revision |
| Completion additional_delivery_required | 保留task-delivery-planning-router，reason=next_independent_delivery→Author delivery_plan_revision |
| Completion remaining_work | 原active-task-continuation，只有planning authority变化才重入Author |
| Completion evidence_pending | Completion自身补证据与重审，不强制重规划 |
| Completion requirements_revision_required | 原task-requirements-revision-router→Clarify→Author requirements_revision |
| Completion implementation_revision_required | 原guru-resume-implementation，不吞并Phase2 ingress |
| interruption/compression、合法前序result丢失 | live绑定同TaskId/generation/source/checkout；回丢失producer fresh输出，不从文件齐全/旧private状态推断pass |
| task/base变化 | 原reconcile owner分类影响，再从最早受影响owner继续；informational RelatedWork更新不自动重规划 |

每次mapped re-entry自动接续，不索取routine确认。initial planning展示/接受后由Execution activate；in_progress approved replan同样展示/接受/pair guard后resume_execution，TaskId/generation/branch/checkout/status保持。授权只在当前对话，不写任何artifact/DTO。

## D9 任务局部 Architecture contribution

这是本任务design内的唯一Architecture proposal，identity由当前文件内容及locator供局部validator绑定；不另建proposal JSON或审查账本。预期change path为target_native：新增独占writer是现有target要求的实现，planning3.0直接迁移受控consumer，不保留旧路径。路径与必要ADR最后由fresh独立Architecture owner判定。

Before：ARCH-CUR-056/ARCH-DOM-039/ARCH-INT-042承接#250后Planning拥有设计处置但writer未命名；Planning Architecture只有Approval回程且必须先有贡献；brainstorm native仍可能按上游合同先写PRD。

After（目标设计；当前未提交候选已有对应接口，实际行为仍按本任务验证合同判断）：Author单写planning；前置评估以真实候选为对象，final以真实贡献为对象，两目的归同Architecture owner；Thin入口实际dispatch；qualifier各自扩展Author输入，Approval保留独立职责。影响的是planning semantic owner、公共接口与distribution；不改变TaskId/正式task writer、source/closure、execution或promotion owner。

九concerns：authority-binding适用，首次规划的2.0接口描述属于创建基线背景，不构成本轮评估绑定，也不证明曾执行过2.0评估；当前已安装候选的planning评估绑定 `guru-maintain-architecture-baseline:planning:3.0` 并明确 `candidate_assessment` 或 `final_plan`。shared change-contract 的现行2.0绑定尚未晋升，本任务仅提出D5所定义的planning限定迁移；非planning接口、project descriptor与check-result保留2.0。当前任务贡献不改shared authority，后续由原Architecture owner按D5/D9顺序晋升；constitution-binding适用，读取D1唯一authority不复制原则；boundary-and-decision适用，D1/D5与D10；owner-and-single-writer适用，D3/D7；compatibility-and-exit适用，D5/D11删除旧planning；gap-and-deviation适用，保留closed ARCH-GAP-006/008/012，不扩大其生命周期，当前缺口由本task封闭；parallel-scope适用，只写任务内候选，禁止直接竞争shared current；evidence-and-freshness适用，D8与implement中的真实runtime/native证据；review-and-promotion适用，真实贡献与必要ADR经独立committed review后晋升。

Project check沿 `guru-trellis-architecture-convergence:repository:1` / `guru-trellis-architecture-convergence@1` 的既有AI协议。当前planning评估判断边界/消费者/前后设计，implementation、Phase2和BranchReview分别审实际候选；native和install效果在本轮未验证。外部/production业务集成不适用；未通过运行证明的accepted native行为保持evidence gap，不能用规划语义通过替代。

允许task-isolated package/workflow/测试/贡献；禁止planning阶段修改shared current Architecture/RDT、跨task改owner/GAP、兼容fallback和授权存储。expected current在实际promotion轮fresh解析，不固定为本轮身份。顺序：proposal→Phase2→TaskCommit→首次独立完整committed BranchReview→原Architecture/RDT owners serialized promotion→fresh Phase2/Commit/full BranchReview→DeliveryReview。promotion pending不得进入DeliveryReview。必要ADR候选见D10；晋升时由原owner写唯一durableADR，不提前分配全局ADR号。

### D9.1 scope_ready 显式迁移贡献

本段由原 Author 承接同轮真实 candidate_assessment 的 architecture_impact / target_native 判断；依据 ARCH-FND-004、ARCH-DOM-039 与 ADR-292-SCOPE-READY-CANDIDATE。该判断针对必要职责拆分与现有 router 的薄投影，不替代当前实现验证、final_plan 或 Approval。

Before：外部 Direct Source 正常变化后，Clarify active clear 要求三份已更新 planning 和 active_task_scope_update，而唯一 Author active profile 又要求 Completed Clarify；context refresh 无法打断 writer 前置循环。该旧 action payload 实际只是 planning/authority hash 和 reentry bookkeeping，没有独立 lifecycle 更新字段，也没有 mutation executor。

After：Clarify active private4.0 在 AI 完成当前 scope 判断后产生 scope_ready1.0，输出仅 exit_id/mode/task_ref/source_selection/revision_refs。原 clear-router 使用独立 consumer1.0，删除 exit_id、固定加入 active_task_scope_change，其余四字段直传原 Author input1.0。Author 先收敛受影响需求和候选，再原 Architecture 前置评估，再 Author solution 写作、Wording、final Architecture、Approval，最后经原展示/接受/pair guard 到 resume_execution。Clarify 不写 planning、不改生命周期、不携带 planning hashes 或旧 task action。revision_refs 必须由 Clarify AI 根据真实修订选择。

兼容退出：private3.0、public clear3.0、原 clear consumer2.0 保留原字节；其它 profiles 与 owners 不变。旧 active 成功结果只能原 Clarify fresh re-entry，不能转换成新 pass。非 current/mechanism-only active clear 仍回中断 consumer；新 task 仍由原 intake 创建；source mutation 先 refresh_context，missing context 保留原 needs_context 四 profile 回程。in_progress 不重跑 initial activation。不存在新 executor、router、wrapper 或 shared authority 晋升。

九 concerns 的增量：authority/constitution 依 D1/D9；boundary/owner 是 Clarify scope 与 Author writer 的前后切分；compatibility/exit 是上述显式版本和 fresh producer；gap/deviation 不新建 GAP；parallel scope 仅当前任务；evidence/freshness 区分 wrapper 投影与 native AI；review/promotion 保留 D9 原 committed review 后的原 owner 晋升顺序。当前 contribution 与 ADR 仍 task-local、未晋升。

## D10 ADR candidate：唯一 Planning writer与两目的Architecture边界

状态：task-local候选，未晋升。Decision：规划业务语义由Author独占，需求决定/Architecture/Wording/Approval保留独立owner；同Architecture planning使用目的专属3.0合同，candidate_assessment不要求未产生贡献，final_plan仍审真实贡献并相邻交Approval。

替代方案及取舍：让现有Approval兼任writer会破坏独立门禁；另建prewrite Architecture owner会复制责任；只加purpose沿用贡献必填会在无docs正常首次规划失败；双读planning2.0会重新产生歧义回程。所选方案新增必要closed输入/输出并同步迁移consumer；代价是所有受控planning caller及投影必须同批准备后切换。无constitution例外，无新shared cache/ledger/GAP lifecycle。ADR必要性来自新增单写owner和公共planning兼容退出，而非每项变更都生成ADR。

### ADR-292-SCOPE-READY-CANDIDATE

状态：task-local candidate，未晋升。决定：新增必要 scope_ready 出口与 active private4.0，复用原 clear-router 薄投影至原 Author；scope judgment 在 planning write 之前完成。必要性来自正常外部 source 更新暴露的 writer 循环和公共出口兼容边界。

替代方案：继续要求 Clarify 写三份 planning 会制造第二 writer；由 Author 先绕过 Clarify 会跳过真实 scope 判断；给旧 clear 填入新字段会静默破坏已发布公共合同；新增 router/owner 或转换旧 pass 会增加不必要职责与歧义。所选方案只新增必要独立 schema/exit，代价是 matching workflow/preset 必须同步应用，旧 active 调用 fresh re-entry。无 constitution 例外，不新增 lifecycle、缓存、授权存储或 shared promotion。

## D11 生效顺序与退出

先准备Author package和qualifier新profile、Architecture目的专属schema/runtime、Approval/Wording消费者，再更新registry/interface/workflow/platform为唯一可达链，最后apply/reapply投影并验证。单次候选交付中才切换runtime，不在Author缺失时激活新mandatory edge。期间未发布candidate不是第二受支持runtime路径；不引入feature flag。

同task删除旧未命名writer文案、直接Planning→Approval竞争边、planning2.0无purpose入口及其专属schema/例子/测试入口。共享2.0 schema仅保留非planning具名consumer。README/MIGRATION-292说明matching preset+workflow同步更新及中断旧规划fresh reentry，拒绝从旧DTO猜continuation。canonical/dogfood/installed/interfaces和全部声明平台projection一致；不清除upstreamskill发现。

## D12 可验证性与限制

行为测试必须执行真实installed/public wrappers并观察消费者接续，文本/constant比对仅证明投影，不能证明AI写作或semantic gate。native验证覆盖正常prompt、brainstorm、官方seed与缺/stale docs、来源A-D承接与普通遗漏阻断、revision/source变化、真实压缩恢复、initial/active展示和Execution。审批遗漏负例由正常author遗漏的去敏样例形成，不篡改hash/artifact或故意绕过来制造问题。

新装与既有update/reapply在一个代表性clean throwaway及其真实existing状态上验证，声明平台做定向projection/入口审查；完整多平台matrix和Release另属专门owner。native压缩/真实prompt执行能力缺失时写明验收缺口并停在当前owner，不能改称模拟通过。具体验证分组、命令和证据落点见implement.md，不在此复制测试矩阵。
