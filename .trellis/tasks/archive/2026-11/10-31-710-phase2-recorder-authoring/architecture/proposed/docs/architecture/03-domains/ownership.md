# DOMAIN Ownership

| Identity | Domain | Authority |
| --- | --- | --- |
| `ARCH-DOM-001` | workflow lifecycle | global workflow + 23 step-local Skill interfaces |
| `ARCH-DOM-002` | task/workspace/history | task scripts、workspace creator、finalizer、merge owner |
| `ARCH-DOM-003` | semantic governance | planning/check/review/publication/SSOT Skills |
| `ARCH-DOM-004` | deterministic runtime | canonical shared runtime 与 package runtime |
| `ARCH-DOM-005` | distribution | marketplace workflow、preset installer、overlay、manifest |
| `ARCH-DOM-006` | repository knowledge | RDT authority、Architecture authority、minimal spec projection |
| `ARCH-DOM-007` | compatibility harness | #260 live-derived matrix 与 A/B fixture；只证明 task-local lifecycle/provider/archive/recovery/reachability，不成为 #248 Acceptance 或 #252 cleanup public owner |
| `ARCH-DOM-008` | architecture lifecycle governance | `guru-maintain-architecture-baseline` 拥有 impact/path/check/review/promotion 语义；项目 Architecture Baseline/change contract 拥有 decision、GAP、owner、concern 与具体 check semantics；global workflow 只拥有 stage order 和唯一 router |
| `ARCH-DOM-009` | Finalizer provenance | `guru-finalize-task` 拥有 source/target binding、两棵临时 checkout 与 metadata-tail producer；installer 独占 manifest source provenance；`guru-verify-extension-installation` 独占 standalone failure evidence；不存在 shared resolver、跨 lifecycle 调用或第二 writer |
| `ARCH-DOM-010` | repository release orchestration | 仓库私有 `release-guru-trellis-version` 只拥有正式发布两阶段编排、fresh authority/candidate 分类与独立动作边界；既有 task lifecycle owner 和 tag/smoke/Release/Issue closure/cleanup 边界继续各自单写结果 |
| `ARCH-DOM-011` | solution mechanism qualification | `guru-qualify-solution-mechanism` 独占机制资格；normal-scenario owner、caller severity/route 与 deterministic runtime 不复制该判断 |
| `ARCH-DOM-012` | archived-task recovery | Merge 独占 task-work finding 分类；`guru-restore-archived-task` 独占原身份本地恢复；Phase 2 与后续 gates fresh 重跑 |
| `ARCH-DOM-013` | public wrapper and closeout transaction | 每个 Skill 的原 command 独占 Happy/compatibility mode；Interface 独占 public wrapper path；preset/validator/matrix/eval 只消费 Interface，shared scripts 不承接 package-private facade |
| `ARCH-DOM-014` | post-review base continuity | Reconcile 独占 compatible base advance 的 semantic classification 与确认后的 local reconciliation commit；Review Branch 独占 bounded continuity judgment；Publication 独占 current reviewed-content acceptance；Finalizer 只投影 prior review identity，不复制任一 owner 的判断或写入；此为旧默认，固定内容/实际触发的当前责任以后继 ARCH-DOM-048 为准 |
| `ARCH-DOM-015` | Issue reference and closure ownership | Guru lifecycle 内，current user/live external authority 与 lifecycle owner持有 requirement/source reference；Publication 独占 Issue reference/closure intent；Finalizer 执行 reviewed payload并投影 exact body SHA-256；GitHub 执行默认分支 closing keyword；Merge mutation前验证 live body identity且只验证 live result；无 task-local classification aggregate 或第二 closure owner |
| `ARCH-DOM-016` | active-task continuation | Guru workflow独占detailed continuation；adjacent DTO的consumer、deterministic producer recovery、semantic owner fresh rerun与activation owner各保持单写；upstream独占extractor和thin entries |
| `ARCH-DOM-017` | active-task Delivery capability | Delivery Review独占slice readiness与PR payload truth；Delivery Publish独占push/PR/Draft/Ready及同计划恢复；Delivery Merge独占merge readiness、受控merge commit与Delivery result；Reconcile独占resolved-tree commit；#434独占production graph activation，#436独占Completion及其后续lifecycle |
| `ARCH-DOM-018` | post-delivery terminal lifecycle | Completion、Closure、Finish、Cleanup与Reactivate各自拥有独立semantic judgment、最小DTO与owner-private recovery；#434独占production graph activation，shared authority promotion仍由Architecture/RDT owners串行完成 |
| `ARCH-DOM-019` | task identity session binding | official Trellis task/session store拥有稳定task identity与底层resolver/persistence；`guru-bind-task-session`独占lifecycle-aware resume/rebind/switch/reactivate/manual-recovery判断与最小runtime write；独立 final_plan 的一次性对象评审由原 Architecture 本地入口只读核验，不产生绑定或第二writer，普通执行恢复仍保本owner必要runtime写入；#438保留creation attach，#436保留terminal lifecycle receipts，#434独占production route activation |
| `ARCH-DOM-020` | platform inventory and exact selection | pinned upstream `AI_TOOLS` owns the complete 22-platform inventory and canonical `AITool`/`cliFlag` mapping；Guru preset owns projection descriptors and managed paths；each installed repository manifest/provenance owns its exact selected set；dogfood consumes only Claude/Codex/Cursor；OpenCode remains explicit-only for guru-trellis |
| `ARCH-DOM-021` | task lifecycle identity and stage evidence | Fork 独占 official TaskId/TaskRef/generation/session primitives；Guru shared lifecycle catalog/runtime 独占 package-neutral DTO、normalization、resolver adapter 与稳定错误；Reconcile 独占 integration commit，Task Commit 独占 exact committed candidate，Branch Review 独占 full/continuity review；本边界不替代 `ARCH-DOM-019` 的现有 deferred binding owner |
| `ARCH-DOM-022` | task checkout substrate | Guru shared lifecycle runtime 独占 call-local checkout plan/candidate/resolution/selection、common-dir live facts、adopt/provision transaction、bounded rollback 与 read-only recovery；machine path 不进入 durable task/session/branch/resource authority；`guru-ensure-task-checkout` 仅是 planned ID，E434 独占完整 package 与 activation |
| `ARCH-DOM-023` | checkout acquisition provenance | acquisition transaction独占transaction-created worktree marker写入，output-loss recovery是唯一只读consumer，direct handoff独占retirement；marker不成为task/session/branch/workspace/resource authority，replacement resource不得继承Guru ownership |
| `ARCH-DOM-024` | task branch association | C4 shared lifecycle runtime 独占 Git common-dir TaskBranchBinding、live candidate discovery、establishment/rebind transaction 与 lost-output recovery；C5 ownership owner只通过窄 port提供current/snapshot/restore/establish/rebind/unresolved-ref能力，不向C4暴露ledger representation；E434独占planned package activation |
| `ARCH-DOM-025` | session and resource control | Fixed Fork official schema-2 session store 独占持久化；C5 adapter 独占 path-free TaskId/generation 投影，缺 context key 不写 session。C5 resource ledger 独占 Git common-dir incarnation/ownership、active conservative recovery、remote HEAD advance、Finish seal 与 Cleanup resolution；C4 只消费 `OwnershipPort`，E434 独占 planned package/production activation |
| `ARCH-DOM-026` | task creation and activation inputs | 独立 Issue owner 仍负责 draft Issue；C6 shared composition 消费 reviewed target 与 C2-C5 primitives，建立 TaskId/generation 0、初始 binding/ledger、optional path-free session，并只读恢复 exact creation result。未来 `guru-create-task` 与 `guru-activate-task` 在 E434 package/graph activation 才获得完整 semantic gate、status mutation 与 recovery；C6 input preparation 只校验 planning/current base 连续性，不越权执行 activation |

跨 domain 只使用 interface/schema/typed projection；不得读取对方 private checkpoint 作为 public contract。

## #418 只读复审归属

`ARCH-DOM-002/003/008/013/015` 的 owner 不变；[ADR-010](../adr/010-archived-review-authority.md)
在这些既有边界内划分以下责任，不新增 domain writer：

- Finalizer 原 executor 负责双端归档映射收敛；只读 reader 只验证，不修复映射。
- Merge 只判断当前是否需要归档复审并捕获 PR 快照，不提前批准 merge。
- Branch Review 独占当前完整范围 `B...A` 的独立复审；Publication 独占现有 PR payload 的新语义判断。
- Finalizer 独占原 H 的归档连续性校验和原 `ready_for_merge` handoff；Merge 仍独占最终操作及结果验证。
- Architecture 在三个原阶段分别独立判断 current/blocked；只读来源不进入 promotion/repair 写入。

该链不替代 `ARCH-DOM-012` 的真实 task-work finding 恢复，也不增加 Issue closure owner。

## #419 Active-task continuation 归属

- workflow只分类并调用原owner，不生成semantic pass或mutation success。
- workspace created-result、activation、Phase 2与Task Commit的恢复分别留在原producer。
- Branch Review与Publication成功checkpoint退休后，跨会话只允许fresh semantic review。
- upstream start/continue/hooks/platform/meta不进入Guru preset或managed inventory。

## #435 Active-task Delivery 归属

- 三个Delivery packages只提供additive capability；当前production workflow仍使用原22 invokes / 98 exits图。
- `delivered`只表达一个业务Delivery完成并保持task active；它不是task completion、Issue closure、archive、Finish或Cleanup。
- Merge owner写受控merge commit trailer；历史发现只读GitHub/Git immutable facts，不读取PR body、当前branch存活或task-local ledger作为identity authority。
- #434在#435与#436 capability均ready后原子激活新图并退休旧edges；#436单独拥有Completion、Closure、Finish、Cleanup与Reactivate。

## #443 Task identity session binding 归属

- task.json、artifact locator、repository common dir、live Git/worktree与official runtime mappings共同提供identity facts；新package不复制task/session store。
- binding/rebind/switch/resume/manual recovery只由`guru-bind-task-session`判断并执行；public DTO不携带runtime binding identity或private snapshot。
- #438 creation attach、#436 Reactivate/Finish/Cleanup generation/receipt、#434 global route cutover保持各自单写；package存在不表示production route可达。

#408 的独立手动请求不进入上述 Guru lifecycle domain，由当前会话 AI 依
[全局操作边界](../../../trellis/workflows/guru-team/workflow.md#manual-gitgithub-operations)
执行已明确的 Git/GitHub 操作。它不新增 lifecycle owner，也不改写 task、Finalizer 或 archive 的完成状态。

`ARCH-DOM-028`（#454 D436）：Completion 独占 scope 完成判断；Closure 独占 source Issue disposition
及冻结 action set；Finish 独占 archive/bookkeeping 与 terminal resource seal，不删除资源；Cleanup
独占 Guru-owned 删除结果，保留 caller-owned；Reactivate 独占 archived TaskId 的下一 generation。
C3/C4/C5 与 Fixed Fork 分别持有 checkout、binding、ledger 和 task/session persistence；五个 package
只消费这些单写事实。共享 Finish 的 archive/bookkeeping 结果与本机 seal、binding 退役分别核验；本机未完责任不撤销已成立的共享结果。旧代资源结果只归原 common-dir/generation，Reactivate 核准确共享历史并优先复用实际后继，Cleanup 继续核当前资源责任。

`ARCH-DOM-027`（#454 D443）：Bind 独占当前 session route 判断与官方 pointer 写入/校验。
C2-C4 拥有 TaskId、live checkout、branch binding，C5 ledger 与 Fixed Fork adapter 分别拥有 resource
ownership 和 schema-2 persistence。Bind 不从 TaskRef、路径、branch/HEAD 或旧 mapping 派生新 authority；
manual recovery 只补官方 pointer。E434 才将新 owner 接入 production graph。

`ARCH-DOM-029`（#434 current）：Delivery Review/Publish/Merge 单写每轮业务交付，Completion
单写 whole-task 判定；Closure 单写 Issue action set，Finish 单写 bookkeeping/archive/seal，Cleanup
单写同代 Guru-owned 资源移除，Reactivate 单写新代控制态。#434 只拥有全局边、精确 consumer
投影与旧边退休，不复制 #435/#436/#443 或 D443/D436 的 step-local semantics。
当前 Create/Commit/Change Context/Delivery/Publish/Merge/Reconcile 使用 TaskId/generation、
common-dir branch binding 与 registered checkout，不从退休的 task metadata/path 构造身份。
旧归档 source Issue 搜索先验证唯一 terminal TaskId；在途旧链不进入本图。
前述 #435/#443 deferred 表述保留为 `.55/.57` predecessor history，不是 `.67` current。

`ARCH-DOM-030`（#454 generation 7 current）：official Fork task writer 独占
TaskId/source/create/rename/archive；Guru lifecycle 只验证同一身份域并生成私有
handoff ref。session 仍只有一个当前焦点指针，可按 TaskId 切换或重绑；不保存
多绑定历史。Cleanup 在 terminal ledger 丢失时只执行显式确认的当前候选删除，
或在 Finish branch 消失后记录零删除结果；Reactivate 从同 TaskId、同代的
准确共享 Finish 历史判定资格，不以 cleaned receipt 为跨环境前置。任何 Git HEAD、Issue、checkout、developer 或 assignee
均不构成 task identity 或 session binding authority。

`ARCH-DOM-031`（#467 current）：official Fork 仍是任务写入者；Guru 的既有
`prepare_creation_inputs` 只检验提议 TaskId/TaskRef 与目标 resource ledger。
Architecture 与 RDT 各自串行晋升 shared current，release 编排只消费其结果，
不新增 task writer、版本状态 writer 或安装资产 owner。

`ARCH-DOM-032`（#481 current）：official Fork 单写人员字段已删除的 task.json；
Guru create-task 单写 reviewed 调用输入和既有 TaskId/generation 控制态，不再投影
人员身份。旧归档由 inventory owner 提取实际 TaskId 防复用。明确支持的正式 schema1
归档由原 Reactivate 核准确历史、来源和终态，再调用 Trellis 正式公共操作一次增代；
其余旧格式保留只读诊断或原独立维护路线，不进入普通 current 执行。session adapter、TaskBranchBinding、common-dir resource ledger 与 checkout
继续各自单写，caller/guru 归属不从旧归档推断。#292 独占 Phase 1 author。

`ARCH-DOM-033`（#490 current）：Guru creator 仍拥有 C6 正式输入/恢复，official task.py 仍单写 task.json；reference_only 是现有 source disposition，无新 writer/owner/public Skill，不能授予 Issue closure。Closure/session/branch/checkout/resource 的原 ownership 保留；follow_up/parent 不是新任务创建能力。Architecture/RDT 各自仅通过 expected-current `.70 -> .71` promotion 更新 shared authority。

`ARCH-DOM-034`（#495 reviewed）：AI migration owner 判断真实来源、定制/interface 协调与 task/delivery/recovery 处置；Fork 单写 core/task，Guru/preset 单写安装，current lifecycle owners 单写当前控制面。备份锚点不因 resume 吸收新工作；required Skill/overlay projection 与原 preimages 允许 canonical-only 回退，暂停新增工作阻塞覆盖。共享 RDT/Architecture 由 expected-current `.74→.75` 串行晋升；ADR-018 扩展来源，保留 ADR-017 owners/current-only/删除出口。

AGENTS core/preset精确projection由正式Fork collector/installer拥有；migration复用原preimages保护所有默认或preserve安装的暂停新工作，完整bytes/mode回退资格不新增writer/state。

## #503 身份职责后继（.76）

`ARCH-DOM-034` 的 #503 successor：Guru substrate reader 拥有身份占用/selected 严格读取，Fork 官方 task writer 已由独立 #29 交付。migration owner 与单写边界不变；无第二索引/store/writer。task contribution 与 expected-current `.75→.76` RDT/Architecture 晋升分别由对应 owner 串行执行。

`ARCH-DOM-035`（#382 reviewed）：normal-scenario、solution-mechanism、root-cause 分别拥有场景、authority 承载与因果候选准入。原 stage owner 继续拥有其实现/证据/完成判断；#383 拥有共同完成语义，root qualification 不创建第二 SSOT。runtime 只校结构与事实，不判断根因。RDT/Architecture promotion 保持既有 expected-current 单写 owners；无资格缓存、数据库或审批链。

`ARCH-DOM-036`（#383 reviewed）：共同 spec 单写共用语义；root 只判候选准入，各 stage owner 单写本阶段 evidence sufficiency/route，Delivery Review 审 payload、Publish 执行，Completion 独占 whole-task 完成判断，Closure 拥有 source Issue action-set，Finish 承接 terminal bookkeeping。Delivery/Reactivate 的原 evidence slots 与 current anchor 保持；unknown production effect 由同 task pending/refresh 承接。Architecture/RDT 原 owner 串行 expected `.79→.80` promotion，没有新 writer、审批链或公共 causal DTO。

`ARCH-DOM-037`（#468 reviewed）：Planning 审规划，workflow 展示/对话承接和全局 route，原 execution owner 审/执行 resume、单写 completed result 并拥有 recovery/retirement；Check 只消费正式 current producer 并调用原 owner retirement。Clarification/Delivery/Completion/Closure/Finish/Reactivate 原职责和 #464 dependency-scoped invalidation 保持。Architecture/RDT 各自原 owner 串行 expected `.80→.81` promotion；不增加授权存储或审批链。

`ARCH-DOM-038`（#453 reviewed）：原 Skill 单写 semantic 判断、内部 owner/checkpoint 与 public exit，共享 dispatcher 单写声明驱动的 CLI transport；具名 caller 校验后投影 result，workflow 只消费真实 public invoke DTO。Architecture/RDT 原 promotion owner 按 expected `.81→.82` 串行更新共享 authority；无新增授权状态、reviewer ledger 或业务 writer。

`ARCH-DOM-039`（#250 reviewed）：Clarify 唯一拥有 Intake 意图、requirement authority、selected source roles、Issue intent 与真实选择；Discovery 只拥有 context evidence/coverage，Wording/readiness 保留独立判断并薄 relay，Planning 单写最终设计处置。Create Issue/Create Task、scope-change、两 qualifiers、#468 execution recovery 与终态 owners 保持；Intake intent 不授予 Closure authority。Architecture/RDT 各由原 owner 串行 expected-current promotion，无第二来源模型、shared cache 或授权存储。

`ARCH-DOM-040`（#521 reviewed）：selector 只判 mode；原 task-free execution owner 单写位置 suitability、有界编辑和扩张回程；Guru workflow caller 消费 upstream 无 Task 返回而不接管 upstream entries/hooks。C6 创建前置拥有 new-primary 拒绝，既有 Task recovery/branch/session/resource、base Sync 与 Cleanup 各自保留 writer。原 Change Request Review 拥有无 Issue/workflow 输入兼容，不改 producer transition 或 Task gates。Architecture/RDT 原 owner 各自 serialized promotion；无 Task-free lifecycle、第二 acquisition owner 或迁移账本。

`ARCH-DOM-041`：Author单写Task整体scope PRD及所选Delivery规划和revision；Clarify先判断来源/scope，Author根PRD后由原Clarify acceptance核AuthorityRef并accept_scope。pre-Author与post-acceptance scope_ready2.0由原clear-router分别消费；只有post结果交当前stage合法rework/stop，Clarify不取得stage writer。Discovery单写context evidence，原normal/solution/root owners分别判断候选资格；Architecture两目的独立评估、Wording与Approval保持原职责，当前Planning由原Delivery Activation记录。各回程仍为显式最小projection，不解释来源或重建producer private；execution/Task writer、Delivery/Completion/Closure/Finish/Reactivate及RDT/Architecture晋升owners各自保持单写。当前取舍见ADR-022/024/035；ADR-023的旧DTO/profile/status片段只适用固定旧完整安装，原先判断后写作及唯一writer原则继续继承。无第二来源authority、store或审批链。

`ARCH-DOM-042`（#530）：原 TaskCommit 单写 dirty exact commit 或 clean committed candidate 的当前事实核验及原 DTO 投影；Check 单写 Phase2 内容算法与证据，Reconcile 单写 integration commit，BranchReview 单写完整/continuity review，workflow 只路由。BranchReview 不读取 producer 私有 checkpoint；Architecture/RDT shared-current 仍由原 promotion owners 串行更新，不能由 clean 状态代替 gate。

`ARCH-DOM-043`（#531）：上游拥有Task/Delivery公共模型、identity/selection/session与确定性转换；Architecture final_plan只拥有受限只读评审对象接入，不把对象写为选择，也不放宽其他consumers；Guru只拥有整体scope判断、每Delivery唯一Author/Wording/Architecture/Approval及Check/TaskCommit/fullReview/readiness语义门禁。Publish/Merge各自核原输入与真实远端副作用后投影公共事实；私有事务可用时恢复原操作，缺失时只从明确共享source/PR与当前资格恢复已发生动作，history不产生current gate pass。Completion/Closure/Finish/Cleanup/Reactivate原owner保持；无Delivery时整体需求、证据或收尾合法，不造空Delivery。ADR-024明确旧Task开发writer及激活分叉退出；旧安装迁移仍须公共Plan2与Guru私有owners各自就绪，不产生双authority。

`ARCH-DOM-044`（#547）：Completion 审完整当前 scope，Closure 审源剩余责任并冻结完整动作集，以最小共享载体关联原公共结果；Finish 读取精确动作集并核 live 状态后归档/bookkeeping，Cleanup 独占删除；公共 Task2 仍由上游拥有。retain_open 不授予第二处置 owner，aggregate closed 不成为 exact source authority；实现落点与旧 consumer 退出见[贡献](../contributions/547-retain-source-open.md)及 ADR-025。

`ARCH-DOM-045`（#548，#657 current承接）：官方model/session/C4仍拥有公共事实，独立final_plan按原Architecture包只读入口核完整对象，其余执行接收保原绑定/选择恢复；Creation独占其pending生命周期，Author只调用producer retirement端口。Creation/Selection保持原created wire，原workflow consumer重读公共current key、generation/root及phase，只有planning中真实尚需初始requirements且符合Author入口才交初始Author；其余按唯一continuation的实际未完成义务交原owner，包括已有planning的适用Author/Wording/Architecture/Approval或当前approved到Activation。缺失/过期输出回原producer，保留phase、规划和适用结果。既有Task写入资格来自当前identity/binding/checkout及stage gates，不要求初始created；原初始恢复validator不变。Discovery/Review不索取退役metadata branch或Task development status，standalone verifier不指向current Finalizer。原说明与证据见[#548贡献](../contributions/548-creation-recovery.md)，当前窄决定见ADR-035；stage/public writer及Task终态owners不变。

`ARCH-DOM-046`（#557）：原 Merge 独占手动终态的归属与 public record_delivery 投影；history 只读既有公共事实，原 Completion 保留 actual content/authority/CI 与整个 Task 证据判断。无新 owner、writer、importer 或 ledger，详见[贡献](../contributions/557-manual-merged-delivery-recovery.md)。

`ARCH-DOM-047`（#566）：公共模型/模板/转换/恢复仍由 Trellis 单写；Guru 两个 semantic 维护闭环、原资产/私有控制/runtime owners 分工，Reconcile 与 Completion 保留业务职责。 责任见[贡献](../contributions/566-single-checkout-upgrade.md)与 ADR-027，实际结果和边界见[唯一 Test](../../requirements-design-test-contributions/566-single-checkout-upgrade/test.md)。不表示正式依赖/业务采用、软件发布或 Task Closure。

`ARCH-DOM-048`（#567）：原 Author/implementation owner 拥有内容范围选择，shared DeliveryProjection 只投影已有公共事实；原阶段 owner 判断 authority/证据适用性，Check/full_review 分别实际审查当前候选。Reconcile 只拥有必要的固定目标整合与原恢复能力；Merge 判断真实合并资格并执行 expected-head 事务，Completion/Finish 各自承接整体事实和 bookkeeping。Architecture/RDT 原 promotion owners 独占 shared-current 写入，expected-current 不成为全部在途任务的开发资格。无新增 coordinator、store、writer 或审批链。详细机制与旧 consumer 退出由[贡献](../contributions/567-fixed-development-baseline.md)、ADR-028 与唯一 Design 承接。

`ARCH-DOM-049`（#569）：原Merge history拥有固定截点事实及临时Git准备，public Task parser只读，原Completion/独立/恢复AI拥有适用性、补证与后续route；原manual recovery共用候选hash、默认上下文保持。Architecture/RDT原promotion owners仍单写shared-current；无第二历史authority。详见[贡献](../contributions/569-fixed-cutoff-history-query.md)。

`ARCH-DOM-050`（#578）：原阶段 owner 独占当前完整范围、消费者、检查集合、工程事实适用性及新语义结果；原执行者只拥有原命令事实。Architecture/RDT 原 promotion owners 串行写 shared-current，原 private state consumer/retirement 不变；无跨 owner 私有状态消费或第二 ledger。

`ARCH-DOM-051`（#599）：canonical managed-spec 单写清晰写作规则；当前输出 Agent、写作 owner 和独立 child 负责完整读取及自检，既有审核 owner 在原范围内判断语义与清晰度。workflow、Skill 和平台入口只承接加载定位，preset 只拥有受管分发与用户指令保护；`guru-review-contract-wording` 保留原固定范围和出口。Architecture/RDT 原 owners 继续分别晋升各自 shared-current，无新增语言审核 owner 或授权存储。

`ARCH-DOM-052`（#589 D7）：上游公开内容 owner 独占不可变对象摘要与序列化；原 Merge manual/history owner 继续拥有历史准备、逐候选比对、事实归属与恢复。公开 context 只在同一操作/实际仓库内复用不可变计算事实，不接管业务或阶段判断。原 tools owner 负责从 clean source 正式采用及 receipt，Architecture/RDT 原 owners 分别单写 shared-current；无新 owner、ADR、GAP 或双写。

`ARCH-DOM-053`：原Architecture独占拟晋升独立评估、final_integration写入/恢复及适用性；原RDT独占三层正文晋升；原Check独占完整候选检查、合法rework及最终public Check。implementation独占candidate/begin_check与真实after重绑，workflow仅消费candidate_checked并调原owners。TaskCommit、committed独立Architecture、BranchReview、Delivery/Publish/Merge及整体终态owners保持原职责。候选结果不形成最终门禁，窄引用对齐不能承接实质正文。无新Skill、公共phase、调度器、store或账本；详见[ADR-KNOWLEDGE-FINAL-INTEGRATION](../adr/knowledge-final-integration.md)。

`ARCH-DOM-054`（#577）：公共 Trellis 保持 Task/Delivery/session/binding、legacy projection 与恢复回退的唯一 writer。`guru-maintain-legacy-task` 只拥有独立维护意图、精确对象与写集、同操作 Guru checkpoint、原 owner 调用和实际目标续接。原 Publish/Merge 核验历史，原 Publish/Merge/Finish 及明确选定 gate owners 分别解释和处置自己的私有 controls；`source_task_ref` 指向物理归档，`task_ref` 保留原活动控制归属。原 Identity/Bind 共用 installed public active resolution 和选定 checkout；C4 仍拥有首次 branch binding，历史 reservation 不成为第二 current authority。当前 scope、真实新 Delivery Planning、整体 Completion 和未完成 closeout 分别回原 owners；原 upgrade owner 保留历史工具来源判断。独立评估、Architecture/RDT 晋升及发布职责不转移。指定正式 schema1 由 Reactivate 经 Trellis formal operation 单次收敛，原 manual archive_resume 保代合同不改义；未完成 closeout 仍归原事务。责任及旧 consumer 退出条件读 [贡献](../contributions/577-manual-archive-resume.md)、ADR-024/027 与 [ADR-PORTABLE-SHARED-LIFECYCLE](../adr/portable-shared-lifecycle.md)。

`ARCH-DOM-055`（#154）：原 Author 独占规划正文、模板和示例；Discovery 调查事实，Clarify 判断来源和范围，Architecture 按原独立方法评估，Wording、Approval、实施、Check、Delivery Review 与 Completion 分别承接原职责。普通遗漏回最早受影响 owner，技术细化不自动改变产品范围。模板填充只写选定 Task/Delivery 规划；RDT 与 Architecture 原 owners 单写长期贡献晋升，不建立第二方案或授权存储。详见 [贡献](../contributions/154-planning-body-contract.md) 与 ADR-022/024。

`ARCH-DOM-056`（#153）：Clarify 单写 Issue 内容正文并保留来源、意图、范围及正文整理判断；Wording、Readiness、Create Issue 分别保留表述审核、完整性/交付单位判断和已审草稿创建/回读。Author 仍单写 Planning 来源合同，managed spec 仍单写语言规则，preset 只拥有受管分发。范围外缺口先说明实际影响，真实范围选择回原 Clarify；不增加第二 writer、内容评分器或审核阶段。Architecture/RDT 原 owners 各自单写 shared-current，具体差额见 [贡献](../contributions/153-issue-content-ssot.md)。

`ARCH-DOM-057`（#630）：installer原owner独占Guru声明文本LF、root attributes有界块和精确EOL恢复；用户.gitattributes整体、块外字节与上游entry归属不转移。raw validator继续真实字节校验。base/schema/bootstrap与TaskCommit各原owner承担系统Path、file URI、原生Bash/stdin及UTF8候选协议，source owner通过canonical source lock选定的精确Fork/CLI/Core配对接入原生维护，不使用overlay patch。窄替代条件由[ADR-032](../adr/032-managed-text-lf.md)拥有；#630的`.5`实际结果及限制保留在[#630唯一Test](../../requirements-design-test-contributions/630-native-compatibility/test.md)。#687采用结果由[#687 Test](../../requirements-design-test-contributions/687-adopt-castbox6/test.md)拥有，不因更新来源转移原owner职责。

`ARCH-DOM-058`（#636）：TaskCommit原owner独占早期有界提交/clean恢复与最终Check绑定提交，原executor保持唯一Git提交writer。Publication原owner独占同PR Draft/Ready往返、先Draft后push、元数据与同操作恢复；早期Draft不写最终PublicationFact。原BranchReview拥有固定B/H的早期完整分析，但不写full_review，最终仍由原独立owner在真实Check前置下判断和记录。workflow只调度唯一typed consumer与并行工作；原Check/DeliveryReview/Merge、Completion/Closure/Finish/Cleanup、RDT/Architecture单写职责保持。必要性、迁移退出及边界见 [贡献](../contributions/636-early-draft-pr.md)与 ADR-033，无第二账本、公共phase或兼容双读。

`ARCH-DOM-059`（#637）：原 Architecture/Check/TaskCommit/Branch Review/Delivery Review/Publication/Merge 各拥有本阶段范围、原覆盖适用性、实际差额和当前结论；同合规独立 reviewer 可接续并依次执行 Architecture/Branch Review，作者自检不替代。工程事实仍归实际执行者，当前采用和补跑由当前 owner 判断；public Task/Delivery 仍由官方 API 单写。workflow/continuation/平台入口只加载路由，唯一共享规则由 workflow-contract 单写。原 RDT/Architecture owners 分别独占 expected-current 晋升，private consumer/retirement、原事务和终态职责不变。精确替代见 ADR-034；不新增 owner、store、cache、公共 DTO 或审核账本。


## 跨环境共享事实与本机责任

`ARCH-DOM-060`：公共 Trellis 继续唯一拥有 Task/Delivery/session/binding、格式解析、reopen、formal archive projection 及维护恢复。Guru 原 Identity 从明确 repository/source ref/commit 与公共 key 核验可获取代码和 Task/Delivery 关系；原 Establish/Ensure/Bind 在当前环境建立合法 checkout、branch binding 与 session。共享记录不承载原机路径或资源权属，不按 branch、标题或目录猜身份。无可验证来源或关联不唯一时，只阻塞该 Task 的实际原 owner。

原 Author/Approval/Activation、Check、完整 Review、Readiness 各自判断当前资格。可核验公共结果和工程命令事实按原候选适用合同消费；缺 private checkpoint 本身不要求重开 Intake、Planning、Delivery 或无变化整链重跑。文件、phase 和历史 prose 不产生当前 pass；真实 scope、authority、依赖或候选变化回最早受影响 owner。

原 Reactivate 核准确 archive commit 中的 TaskId/generation/source/scope、该版本终态关系、summary/archive 一致性及精确 bookkeeping PR/target 历史，且归档结果移除了原 active。Task2 核真实 Completion→Closure；明确支持的正式 schema1 核固定前驱合同，不补造旧 Completion/Closure/gate。summary、completed、Issue CLOSED 或单个 MERGED PR 不能单独放行。后续 target 前进或 active 后继不否定准确历史，也不要求 merge SHA 写回自身归档或新增递归 Finish PR。

先核当前可获取的同 Task 后继；验证匹配则继续实际 generation，不重复 reopen/prepare。不承诺发现其它 clone 的未发布 incarnation。没有后继时，Task2 沿公共 reopen 与 relocation，指定 schema1 沿已核 matching capability 的 formal operation 严格增代一次。真实 applied key/ref 交原环境 owners，再由 Continuation 进入真实新 Delivery 或无空 Delivery 的 Completion validation；不继承旧 gate。人工历史归原 legacy owner，未入 target 的唯一未完 closeout 回原 Finish；无法唯一恢复时返回具体缺口。

对于已存在实现提交和原开放 Draft PR 的恢复，原 Reactivate 提供独立 existing-implementation 输入，不把旧 clean-base profile 改为通用 dirty 准入。AI 分别核准确目标 base、实际实现 HEAD、完整已审核本地内容、PR repository/base/head、前驱及资源责任；只读 observer 提供 Git/gh 事实，摘要只服务当前逻辑内容比较。C3 对准确已审 checkout 承接，public writer 仍唯一增代，C4/C5/Bind 和当前 Delivery gates 保持原职责。现有 raw-index snapshot/rebind consumers 不因本场景更改语义。

逻辑内容比较覆盖 index entries 的 path/OID/mode/stage，以及 tracked/untracked 字节、文件类型和执行位；普通 index 缓存刷新不是内容变化。原操作合法 Task 写入与已审本地差额按精确前后状态区分，不整体忽略 .trellis。当前 HEAD/branch、PR、内容或 ownership 失配时停止并保留现场；输出丢失或合法后继接续不再次增代。恢复不自动提交/推送工具升级差额、不修改原 PR、不关闭 Issue 或清理资源。历史 Completion/Closure 保持历史身份，不能转换为当前 gate。

新增闭合 profile/schema、matching 安装与旧 transaction 语义边界由 [MIGRATION-669](../../../trellis/presets/guru-team/MIGRATION-669.md) 拥有。当前取舍沿 ADR-PORTABLE-SHARED-LIFECYCLE 和 [#669 contribution](../contributions/669-existing-implementation-reactivation.md)；无新 writer、GAP、全链 digest 或授权存储。代表安装的实际 AI 原生样本可以使用真实 Git/受控 provider，只证明其实际层次，不证明真实 GitHub/backend 或生产效果。

原 Closure 独占完整 action_set 和 source disposition，单写 task-local `closeout/closure/<safe-result-id>.json`，仅保留 schema_version、ResultRef、completion_result_id、source、action_set。safe-result-id 仅为 result_id 的 UTF-8 base64url 无 padding 文件名映射。public Closure evidence 关联该 AuthorityRef；原 Closure recovery 与 Finish 是直接 consumers。公共 Completion/scope/source 关系、精确 result/key 和 live required OPEN/CLOSED 状态仍须核验；载体不授予 close 权限，也不断言 terminal。原恢复 profile 只补丢失公共投影且零 provider close，剩余真实 close 回正常 Closure 当前动作边界。Finish 使用原 snapshot 投影逐 Issue 重核，不从 aggregate closed 推导 source_closed。载体随 Task 归档及原 artifact_origin 解析，已有结果不覆盖；旧已完成 archive 不补造载体，未发布必要输入精确阻塞其真实 consumer。

原 Publish 拥有独立闭合的精确 Open PR Draft/Ready recovery profiles。明确 pr_ref 与 source_commit 绑定同 Task/Delivery、Planning、候选和 repo/base/head/owner；source 未入 main 仍可合法，与 candidate head 不同时核真实历史和完整差额。只复用同一个 Open PR并补未完成动作，绝不另建 PR；相同 head/payload 不重复 push/edit，已 Ready 不产生当前 readiness。Draft 不写最终 PublicationFact，新的未审修订仍先退 Draft。当前 Readiness 不适用回原质量 owner。MERGED 沿原 Merge 手动恢复核公共 Publication、真实双亲/actual head/target 后只补 Delivery fact，不重复 merge；Completion 仍判断 actual 差额、CI 和整个 scope。

本机 branch/worktree/ignored runtime 责任限定对应 common-dir/generation；共享 remote ref 以 repository/full ref/expected head 核验。旧 seal、binding 退出或 Cleanup pending 不撤销共享 Finish，也不阻塞另一 Task 或不同合法新资源。同一资源未完责任仍冲突；B 不取得 A 清理权。Cleanup 保留未知 ownership、新代资源及已推进 remote ref，不删除或回退新提交。原合法子 Agent 并行职责保持；不引入双主、锁、scheduler、全局恢复台账或第二 authority。


## Phase 2 authoring 与结果消费职责

原 guru-check-task AI 独占完整九维语义、finding、验证适用性、Docs/Architecture 消费和出口判断。原 recorder 只接收既有最小语义 authoring，生成 Task 定位、capture commit 与 Phase 2 内容身份；AI 不计算、复制或选择这些结果字段。原 checker 验证 recorder 的同一完整结果，原 public invocation 消费该结果并发唯一出口。字段与 argv 由原 package contract 单写，本单元不建立第二接口。

完整 6.0 是原 recorder 输出及 checker/invoke 的合法消费格式。recorder 的完整结果输入沿 [MIGRATION-710](../../../trellis/presets/guru-team/MIGRATION-710.md)显式退出；当前受控调用同步迁移，不保留无直接 consumer 的双 authoring、compat 开关或自动重绑。既有完整结果的原恢复、freshness 和真实内容变化拒绝保持；Phase 2 与 public candidate 两种内容 token 各服务原 consumer，不能互换。

候选 Check、原 owners 最终整合、implementation 实际 after 重绑与最终 Check 仍沿 ARCH-DOM-053。native 运输只能提供合法 public 身份、前置事实与执行能力，不能代当前语义 owner 填结果或把纠偏重试称首次成功。该选择的理由、范围、迁移和重审触发由 [ADR-PHASE2-RECORDER-INPUT](../adr/phase2-recorder-input.md)拥有；实际命令、native、安装和未验证边界仅由 [#710 Test](../../requirements-design-test-contributions/710-phase2-recorder-authoring/test.md)记录。
