# Architecture Change Contract

Identity：`guru-trellis-architecture-change-contract-v1`；状态：`current`；required concern set：`guru-trellis-architecture-change-concerns-v1`。本文件是本仓库 task-local Architecture change contract 与 project-check protocol 的项目 authority；Guru Team public package只定义可复用 shape 和 routes。

## Required concerns

| Concern | Required current meaning |
| --- | --- |
| `authority-binding` | Planning 绑定 `guru-maintain-architecture-baseline:planning:3.0` 与明确的 `candidate_assessment` 或 `final_plan`；非 Planning impact/promotion 绑定 `guru-maintain-architecture-baseline:6.0`（Delivery4.0）；bootstrap/repair 保留原2.0合同；同时绑定明确阶段适用的 baseline 与本 change-contract identity |
| `constitution-binding` | 绑定 current constitution locator、status、version/content identity 与实际命中的原则 refs |
| `boundary-and-decision` | 记录 requirement/behavior authority、current/target boundary、decision/GAP refs 与唯一 change path |
| `owner-and-single-writer` | 明确 current/target semantic owner、task writer 与 shared-current promotion single-writer |
| `compatibility-and-exit` | legacy/adapter 适用性、owner、可验证退出与旧实现删除条件；`target_native` 不保留 dual-read |
| `gap-and-deviation` | 区分计划关闭、保留、新增和恶化的 GAP/偏移，并为每项保留 owner 与 closure condition |
| `parallel-scope` | 列出允许的 task-isolated scope 与禁止竞争的 shared current/GAP/owner 范围 |
| `evidence-and-freshness` | 绑定 design responsibility、before/after、test/runtime/external evidence 与当前 invocation freshness |
| `review-and-promotion` | 绑定 contribution、必要 ADR、完整候选与晋升前 authority、全部拟写内容、expected-current 与 promotion state；Branch Review 阶段另绑定精确 committed range |

每项必须显式判定 `applicable|not_applicable` 并给出理由；architecture impact 不得以空值代替判断。范围、风险、authority、持久化、SDK、外部、owner 或架构边界扩大时，旧结果 stale 并重新进入 Architecture owner。

## Stage-applicable authority（ADR-028）

每次读取 live authority 后，原语义 owner 判断本阶段实际适用的基线、规则与候选；无关整体 CURRENT、安装版本或共享 ref 前进不自动使在途结论 stale。真实 scope、规划假设、实现、依赖或明确立即适用规则改变时仍回对应原 owner，旧快照不能遮蔽这些变化。内容候选与 integration target 分离；不以 latest-target ancestry 代替完整内容审查或当前 PR 资格。

shared-current integration 自身绑定写前 live expected-current；错配只由原维护 owner 按实际差额处理。Planning 批准后，实施及工程自检完成，原 maintenance owners 在提交前 final_integration 读取完整拟写与真实目标并写入/readback；无 candidate Check 或提交前独立 implementation Architecture 前置。TaskCommit 纳入全部 after，implementation 用固定 B/H 构造完整 committed candidate/begin_check，由新的独立 reviewer 在同一次完整 Review 先判断 Architecture before/after，再完成九维与完整区间审查。九 concern、descriptor identity、check id/version 与 result contract 保持。ADR-028 固定内容及阶段适用性保留；当前整合/审查时机由 [ADR-POSTCOMMIT-INDEPENDENT-REVIEW](../adr/postcommit-independent-review.md) 窄替代 ADR-KNOWLEDGE-FINAL-INTEGRATION 和 ADR-033 的命中片段。

## Constitution applicability consumption

在原 Architecture、Planning 与独立完整 Review 职责内，按唯一 current constitution 的完整五原则判断本次采用的机制及直接影响，包含没有实现 diff 的复用；不单独提高其中一条的地位。具体必要性、作用范围、代价、替代与证据方法只读取原 `guru-maintain-architecture-baseline/references/contract.md`；保护提出方责任沿原 `guru-qualify-root-cause` 的 Protection 合同消费，完整知识与存量处置沿原 `guru-maintain-requirements-design-test-ssot/references/current-knowledge.md` 消费，不在项目另写第二套方法。

项目原九 concerns 和 project-check 使用既有 reason、evidence、before/after 与真实贡献承接这些判断。改变本项目 Architecture 规范性投影时，由原 Architecture owner 准备隔离完整 proposed 定义，并沿提交前 final_integration/readback、TaskCommit、committed after 绑定和一次独立完整质量链实际写入；RDT owner 只写自身三层 authority。当前 Task 的存量义务仍归原 Planning/Completion，不因基线晋升或拆 Delivery消失；新决策生效、新需求交付、旧实现迁完及环境切换分别表达。无 Architecture 影响保持原轻量路径，不创建空贡献、ADR、逐能力字段、原则评分或永久台账。

当前 Requirement 必要而 mechanism 多余时，由当前阶段 qualification owner 经既有 `mechanism_revision_required` consumer 返回设计/实现 remove/replace，保留 accepted scope。Requirement-authority 本身冲突由 Architecture `architecture_conflict` -> `guru-architecture-baseline-planning-router` 返回 Planning，需修订 source scope 时进入既有澄清并取得新 current 后重审。缺适用证据使用 `contract_incomplete`，真实选择/依赖使用已有澄清/blocked。合并 Review 的实际 Planning 修订、当前 implementation finding 和真实 scope choice 分别回原 Author、implementation 与 Clarify；精确当前 exits 由原 Review Interface 和唯一 router 拥有，旧 planning_stale/已回退输出只按 matching 迁移合同恢复。Project-check 在现有九 concern 和 before/after 中判断这一消费，不新增 descriptor、exit 或脚本语义判定。

## Change paths and lifecycle

- `target_native`：新能力直接进入 target boundary，不新增 legacy authority 或 compatibility layer。
- `legacy_boundary_convergence`：仅在旧边界仍有真实依赖时保留局部 compatibility，并明确 remaining debt、owner、退出和删除条件。
- `dedicated_refactor_slice`：在行为/API/规则不变前提下，以单一主写的小切片收敛旧实现，要求可验证、可观测、可回滚和明确删除条件。
- `no_architecture_impact`：只记录 current baseline/constitution、task/stage 与可审核理由，不创建 contribution、ADR 或 project-check burden。

阶段顺序为 Planning candidate_assessment→Author solution→Wording→final_plan→Approval/Activation→implementation/完整隔离拟写与工程自检→原 owners final_integration/readback→TaskCommit→完整 committed candidate/begin_check→同次独立 Architecture before/after 与九维/full Review→Delivery Review/readiness→Publication→Merge/整体终态。首次 reviewer 新开且未参与实现，审查期间冻结 B/H 不写候选。修复由原 owner 形成后继提交；仍独立的同 reviewer 按 ADR-034 采用可核验覆盖，补审全部差额和影响，覆盖丢失或影响不明补足完整审核。提交前 integrated_pending_review 不得进入 readiness/Publication/Finish；只有真实 no_change 或 reviewed_promoted 可进入原下游资格判断。

## Current project-check descriptor

- descriptor identity：`guru-trellis-architecture-convergence:repository:1`。
- check id/version：`guru-trellis-architecture-convergence` / `1`。
- entrypoint：`docs/architecture/06-governance/change-contract.md`；这是 AI 语义检查协议，不是替代判断的脚本。
- applicable scope：stage invocation、authority binding、path exclusivity、required concern completeness、before/after regression、single-writer、parallel stale、contribution/ADR review 与 promotion freshness。
- rule refs：`ARCH-GOV-006..009`；decision refs：`ADR-005`、`ADR-009`；gap refs：`ARCH-GAP-006`、`ARCH-GAP-008`。
- result contract：`guru-project-architecture-check-result-2.0`；freshness source 是当前 task candidate 或 exact committed range。

稳定失败路由为：缺适用 contract/constitution/check facts -> `contract_incomplete`；与 current authority 冲突 -> `architecture_conflict`；新增或恶化偏移、owner 扩张、无退出双写或 closed GAP 重现 -> `fitness_regression`；明确阶段适用的 baseline、constitution、contribution/candidate stale，或本次 promotion 写前 expected-current 错配 -> `sync_required`；无关整体版本/ref 推进不构成此路由。AI 根据 applicability 与 task 真实依赖决定 `blocking`，runtime 只验证 descriptor/result 一一绑定、locator、freshness 与 route consistency。

## Current Planning boundary

`guru-author-task-plan` 独占整体 scope PRD 与每 Delivery PRD/design/implement 的规划语义写作及已有 revision 回程，Clarify 的来源/scope 判断、Architecture 独立评估、Wording 受控 rewrite 与 Approval 批准分别归其原 owner。`candidate_assessment` 评估真实候选但不要求尚未产生的 contribution，不输出 promotion_state；其 current consumer 是 Author solution_planning。`final_plan` 评估 Wording-current design 与真实 contribution/必要 ADR，保留 reviewed_candidate 或合法 reviewed_promoted 约束，current consumer 只为相邻 Approval。前置结果不能替代最终结果；两目的仍属于同一 Architecture owner/stage，project descriptor/result 保持2.0。独立 final_plan 使用完整显式对象的只读入口；无绑定或同Task/generation无选择不先写执行选择。原 Task/C4/唯一checkout、public关系/profile、非终态planning、scope/root/design freshness及不同选择/实际error拒绝保持。空历史 reviewer 在authority后核对象，再读设计/consumers，最后解释归属。该入口不改生命周期/session/资源/规划/shared baseline，正式成功仍只交相邻Approval，后者保自身选择；其他目的/stages及普通恢复writers不变。窄替代及理由见[ADR-EXPLICIT-REVIEW-OBJECT](../adr/explicit-review-object.md)。

Clarify当前Task/Delivery scope profiles先判断范围，返回无task_key的pre-Author scope_ready2.0；原clear-router交Author task_scope_requirements写实际根PRD，scope_requirements_ready及原selection再交Clarify task_scope_requirements_acceptance。只有acceptance核真实AuthorityRef并accept_scope，输出含task_key的post-acceptance scope_ready；其consumer才按义务进入原stage合法rework/stop、显式Creation或Completion。三种scope_action均保留该顺序，不能把pre结果当发布或post结果重复写根PRD。无current Delivery不造空切片。

Wording change refs、Approval revision actions与Delivery/Completion修订经显式projection回唯一writer。旧#292 private4/scope_ready1、active_task_scope_change Author及Task-status activation/resume只属固定旧完整安装，不作current fallback。旧planning2.0无purpose入口也不回退；非Planning6.0/Delivery4.0与bootstrap/repair保持。完整matching切换见MIGRATION-657，公共created wire、原初始Creation validator、原producer恢复及唯一continuation保持；既有Task按当前identity/binding/checkout和实际stage gates续接，Delivery created consumer重读公共phase并核实际未完成义务后进入适用owner。只有真实initial requirements且符合入口才initial Author；已有planning回适用Author/Wording/Architecture/Approval，当前approved进入Activation，缺失/过期输出回原producer。该窄决定由ADR-035拥有，不新建descriptor、状态authority或授权存储。

#531以ADR-024迁移上述Planning责任：Task整体scope-only由Author写作后Clarify审查；Delivery candidate/final两目的独立Architecture、Wording、Approval与Activation保持原owner，同DeliveryKey/planning_root回程。Task-only Completion/Finish仍使用task_impact_sync，不将Delivery与Task结果换标签。

## 当前候选、晋升与恢复输入

非 Planning `6.0` / Delivery `4.0` input 显式绑定 `before_authority` 与完整 `candidate`。前者定位固定 Git authority 的 baseline、constitution 和 change-contract，后者绑定当前 head/content identity。Branch Review 的 before Git revision 等于精确 committed range 的 base。 before authority 也须如实表示该固定 revision 中尚不存在的既有 locator；显式缺失集合只覆盖原 baseline、constitution 和 change-contract 三路径，省略仍要求全部存在。原 validator 逐项核 Git tree，当前 authority、完整候选和 B..H 的独立审核保持。具体公共表示由原 Architecture package 单写；决定见 [ADR-CONTRACT-CONTINUITY](../adr/contract-continuity.md)。新 CURRENT 必须作为受审差额比较，不能以其自身证明符合旧约束。Planning purpose `3.0`、bootstrap/repair、九 concerns、descriptor/check/result identities 与原 owners 保持。

promotion 在 final_integration 绑定批准 Planning、完整实现、真实工程结果、贡献及完整 proposed targets，不要求尚未发生的 committed_range 或独立 candidate Check/implementation Architecture pass。原 owner 写前重读 live expected-current 和各 target；整合仍有效条件后写完整内容并读回全部实际 targets，判断语义、依赖和验证义务是否保持。baseline_current/promotion_state=integrated_pending_review 只表示真实整合；其 candidate 直接供 implementation 形成包含真实 after 的待审提交及 committed candidate，before_authority 供 Review 保持原比较来源。TaskCommit 不跨读维护 private 状态，也不消费独立审核 pass。实际额外变更或适用性变化回原 owner；committed Review 真实判断 before/after 后才可 reviewed_promoted。

部分晋升写入由原 owner 按同一个唯一 intent 区分 completed、pending、conflict；只补未冲突的 pending 内容。冲突或 intent 不明确时停止。完成后输出丢失，只从仍匹配的实际文件和原 intent 恢复同一结果，不创建新 successor 或长期账本。不可重新推导的恢复内容仅在有直接 consumer 时进入 owner-private 短期运行状态，消费后删除；授权信息不写入任何状态。

本合同直接给出当前顺序；[ADR-POSTCOMMIT-INDEPENDENT-REVIEW](../adr/postcommit-independent-review.md) 拥有本地提交后一次独立完整审核决定，[MIGRATION-794](../../../trellis/presets/guru-team/MIGRATION-794.md) 定位公共版本和在途恢复。ADR-KNOWLEDGE-FINAL-INTEGRATION 的 single-writer、完整 targets、expected-current、readback、before authority 和普通恢复保留；其重复候选/最终 Check 时机被窄替代。旧 `.100`、ADR-005 及原证据仍可追溯，不成为当前执行前置。

## 当前知识和通用源的项目读取关系

按本阶段实际问题选择完整知识单元与必要关系，不以历史增量回放替代当前定义。RDT 和 Architecture 各由原维护方拥有正文与晋升，导航只定位。Architecture 的 FOUNDATION/CURRENT/TARGET/GAP/PLAN/ADR/EVIDENCE 仍分工；本文件不把 accepted target、推断或验证缺口提升为实现事实。

本项目采用 [ADR-KNOWLEDGE-NAVIGATION-ISOLATION](../adr/knowledge-navigation-isolation.md) 的独立导航写入边界。Architecture 根只声明体系、职责目录、发现方法和历史/未迁移范围；各完整单元自身保留稳定 identity/alias、原 owner、状态、适用来源、晋升依据及必要关系。日常独立主题不得向根或任一共享列表登记，也不向 system/ownership 或 ADR index 转移登记。查找时在阶段适用的职责目录内限定检索，完整读取命中正文并核来源和晋升状态；现有目录名、文件存在或搜索命中不产生 current。

RDT 与 Architecture 的原维护方分别维护自身正文；新增、修改、改名、替换或删除时，同步真实受影响的稳定引用和必要关系。需要旧引用转换时只保留定位说明或准确 Git 来源，不保留第二活动正文。共同修改同一能力或有效关系属于真实重叠，原 owner 必须整合仍有效条件；路径不同或文本自动合并不能豁免该判断。这里不新增 project-check descriptor、runtime registry 或脚本语义判断。

[迁移合同](../../../trellis/presets/guru-team/MIGRATION-711.md)区分安装匹配规则与项目文档切换。未达完整性、关系和适用验证条件时保原 authority，候选保持 proposed，并明确未迁移范围；达条件后新任务停止旧共享索引写入。旧 Task 仍可读其阶段版本，但 final integration 命中已迁移单元时由原 owner 重读真实目标并写当前完整定义，不继续旧索引双写。切换前失败保原入口；切换后通过原 repair 或受审 successor 修正，历史快照和原始证据不改。

[技术基线选择](../00-foundation/stack-selection.md)定位本项目选定的公共技术栈源、准确版本、项目约束和差异。Architecture owner 在本项目范围维护投影，源维护方在公共源范围维护完整定义。源或引用缺失、范围冲突、迁移未完成时，明确受影响结论并进入原 repair/澄清，保留原 authority。源版本推进不自动替换已选版本或要求旧 Task 重写。当前组织候选的迁移与普通读取退出由 [MIGRATION-331](../../../trellis/presets/guru-team/MIGRATION-331.md)定位，最终状态由原 owner 晋升和真实 Test/EVIDENCE 决定。

## 审查前远端路径退出与原事务恢复（ADR-033 的窄替代）

当前链在一次独立完整 Review 通过前不 push、不创建 PR。原 early Draft 新发布边退出，不通过改变旧 profile 含义继续使用。原 Delivery Review 保留 readiness 和真实 payload/剩余责任/证据边界判断；Publication 只消费当前 ready/readiness，再执行已审精确动作。

旧 Draft 已发生 push、PR、metadata 或绑定事实由原完整 provider 准确恢复，不重复外部动作、不把 Draft 变最终通过。尚未发生的远端动作停止，交 MIGRATION-794 原迁移 owner 接回当前独立 Review/readiness后，按同 PR 和原事务资格接续。既有 PR/remote HEAD 保留；没有 current fallback、旧 pass 转换、第二状态 authority 或扩大的发布权限。

## 候选适用性与独立职责（ADR-034）

Architecture 原 owner 保留首次独立读取顺序及当前 project-check 判断。后继读取合法原覆盖、Hr..Hi 全部真实差额、冲突双方/组合语义及受影响未改 consumers，分别确定保留、失效和补充；原覆盖不足补审，影响无法界定完整评估。同合规独立 reviewer 可以接续并依次完成 Architecture 与 Branch Review，各 matching stage 的判断和 formal result 仍实际发生。新架构事实回原评估；HEAD、阶段或身份变化本身不要求重建。

工程事实按定义/版本、输入/依赖、环境/工具链/参数/期望采用或补命中项，计划 ref 不证明执行，同树不证明环境。原公开结果/调用对象、精确 Git/正文与原命令为合法依据；初次 implementation_required 无 passed full_review，refs 只定位缺陷。缺来源补真实工作，不跨读或重建退休 private，不加账本、覆盖 DTO 或 digest 链。同一次真实审查的 check/full_review 及 predecessor 绑定、finding ancestry、当前 payload/Issue/live 判断保留。

唯一执行定义由 [workflow-contract](../../../trellis/presets/guru-team/spec/workflow/workflow-contract.md#candidate-applicability-and-coverage)单写；本合同只拥有项目职责和 concern/project-check 承接，不新增 descriptor/check/result identity。ADR-034 窄替代无因 fresh reviewer/相同完整重审；ADR-028 与九 concerns、single-writer、完整质量覆盖保持；ADR-030/033 的命中时机按 ADR-POSTCOMMIT-INDEPENDENT-REVIEW 窄替代。matching安装沿MIGRATION-794，旧安装固定或原 owner 成套切换，同 key 原阶段恢复，不由新语义豁免当前旧安装的门禁。

合同承接判断由上述唯一执行定义承接：原 Author/Architecture 从实际入口追踪新生产者输出、持久完成状态与真实消费者的使用前提，核对复用参数的对象、存在阶段、状态和顺序；同次提交后独立完整 Review 核对消费者可用性。测试声明边界、正式路径条件和合法 fixture 的方法只读取 [Test And Validation Value](../../../trellis/presets/guru-team/spec/workflow/quality-guidelines.md#test-and-validation-value)。入口、默认路径或启用范围扩大后，原 owner 明确保留、失效和补证范围，不用生产者成功、局部绿色或历史 pass 代替当前充分性。项目九 concerns/project-check 消费该方法与真实证据，不复制业务领域定义、不新增阶段或证明台账。Delivery 判断继续区分公共源码、dogfood、目标正式采用与业务效果；项目指导的必要差额仍由所属 authority owner 承接。

## 稳定知识身份与真实目标

Architecture authority identity为guru-trellis-architecture，RDT为guru-trellis-rdt。完整单元保留既有identity，精确来源用完整Git revision与repo-relative locator；普通promotion允许同authority identity，不强制总README target、global successor或逐Issue摘要。独立主题的定位由单元自身及真实受影响引用维护；共享入口只在其自身身份、scope/status、位置、发现合同或必要跨体系关系实际变化时更新，不将每个单元定位变化变成共享登记。真实public API/schema版本独立保留，bootstrap仍保留distinct successor合同。目标branch/commit、bytes与恢复intent只在原owner调用或有直接consumer的短期private状态；无全仓hash清单、第二current或授权记录。
