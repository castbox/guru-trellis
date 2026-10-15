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
| `ARCH-DOM-019` | task identity session binding | official Trellis task/session store拥有稳定task identity与底层resolver/persistence；`guru-bind-task-session`独占lifecycle-aware resume/rebind/switch/reactivate/manual-recovery判断与最小runtime write；#438保留creation attach，#436保留terminal lifecycle receipts，#434独占production route activation |
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
只消费这些单写事实。Finish 成功后本代 binding 退役，旧代结果不成为 Reactivate/Cleanup 的当前 authority。

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
或在 Finish branch 消失后记录零删除结果；Reactivate 仅验证同 TaskId、同代
Finish 的 cleaned receipt。任何 Git HEAD、Issue、checkout、developer 或 assignee
均不构成 task identity 或 session binding authority。

`ARCH-DOM-031`（#467 current）：official Fork 仍是任务写入者；Guru 的既有
`prepare_creation_inputs` 只检验提议 TaskId/TaskRef 与目标 resource ledger。
Architecture 与 RDT 各自串行晋升 shared current，release 编排只消费其结果，
不新增 task writer、版本状态 writer 或安装资产 owner。

`ARCH-DOM-032`（#481 current）：official Fork 单写人员字段已删除的 task.json；
Guru create-task 单写 reviewed 调用输入和既有 TaskId/generation 控制态，不再投影
人员身份。旧归档由 inventory owner 仅提取实际 TaskId 防复用，exact TaskId 或严格
exact-source Issue clue 只能得到只读拒绝诊断；Reactivate/Finish 不接收其生命周期
候选。session adapter、TaskBranchBinding、common-dir resource ledger 与 checkout
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

`ARCH-DOM-041`：Author 单写任务规划及 revision；Clarify 单写 scope/来源角色，Discovery 单写 context evidence，原 normal/solution/root owners 分别判断候选资格，Architecture 单写两目的评估，Wording 单写措辞门禁，Approval 单写批准。scope_ready 的 clear-router、Wording/Approval revision 与 Delivery/Completion 回程只做显式最小 projection，不理解来源语义或重建 producer 私有状态。原 execution/Task writer、Delivery/Completion/Closure/Finish/Reactivate 与 Architecture/RDT serialized promotion owners 保持各自职责。当前设计决策为 ADR-022/023；无第二来源、authority、state store 或审批链。

`ARCH-DOM-042`（#530）：原 TaskCommit 单写 dirty exact commit 或 clean committed candidate 的当前事实核验及原 DTO 投影；Check 单写 Phase2 内容算法与证据，Reconcile 单写 integration commit，BranchReview 单写完整/continuity review，workflow 只路由。BranchReview 不读取 producer 私有 checkpoint；Architecture/RDT shared-current 仍由原 promotion owners 串行更新，不能由 clean 状态代替 gate。

`ARCH-DOM-043`（#531）：上游拥有Task/Delivery公共模型、identity/selection/session与确定性转换；Guru只拥有整体scope判断、每Delivery唯一Author/Wording/Architecture/Approval及Check/TaskCommit/fullReview/readiness语义门禁。Publish/Merge各自的私有事务恢复真实副作用后投影公共事实，history不产生current gate pass。Completion/Closure/Finish/Cleanup/Reactivate原owner保持；无Delivery时整体需求、证据或收尾合法，不造空Delivery。ADR-024明确旧Task开发writer及激活分叉退出；旧安装迁移仍须公共Plan2与Guru私有owners各自就绪，不产生双authority。

`ARCH-DOM-044`（#547）：Completion 审完整当前 scope，Closure 审源剩余责任并冻结 retain/close 动作，Finish 只核验冻结结果并归档/bookkeeping，Cleanup 独占删除；公共 Task2 仍由上游拥有。retain_open 不授予第二处置 owner，aggregate closed 不成为 exact source authority；实现落点与旧 consumer 退出见[贡献](../contributions/547-retain-source-open.md)及 ADR-025。

`ARCH-DOM-045`（#548）：官方 model/session/C4 仍拥有公共事实，Creation 独占其 pending 生命周期，Author 仅调用 retirement 端口；各规划 gate 原 owner 不变。明确选择与 Creation 自动恢复分属原操作边界，详见[已晋升贡献](../contributions/548-creation-recovery.md)。

`ARCH-DOM-046`（#557）：原 Merge 独占手动终态的归属与 public record_delivery 投影；history 只读既有公共事实，原 Completion 保留 actual content/authority/CI 与整个 Task 证据判断。无新 owner、writer、importer 或 ledger，详见[贡献](../contributions/557-manual-merged-delivery-recovery.md)。

`ARCH-DOM-047`（#566）：公共模型/模板/转换/恢复仍由 Trellis 单写；Guru 两个 semantic 维护闭环、原资产/私有控制/runtime owners 分工，Reconcile 与 Completion 保留业务职责。 责任见[贡献](../contributions/566-single-checkout-upgrade.md)与 ADR-027，实际结果和边界见[唯一 Test](../../requirements-design-test-contributions/566-single-checkout-upgrade/test.md)。不表示正式依赖/业务采用、软件发布或 Task Closure。

`ARCH-DOM-048`（#567）：原 Author/implementation owner 拥有内容范围选择，shared DeliveryProjection 只投影已有公共事实；原阶段 owner 判断 authority/证据适用性，Check/full_review 分别实际审查当前候选。Reconcile 只拥有必要的固定目标整合与原恢复能力；Merge 判断真实合并资格并执行 expected-head 事务，Completion/Finish 各自承接整体事实和 bookkeeping。Architecture/RDT 原 promotion owners 独占 shared-current 写入，expected-current 不成为全部在途任务的开发资格。无新增 coordinator、store、writer 或审批链。详细机制与旧 consumer 退出由[贡献](../contributions/567-fixed-development-baseline.md)、ADR-028 与唯一 Design 承接。

`ARCH-DOM-049`（#569）：原Merge history拥有固定截点事实及临时Git准备，public Task parser只读，原Completion/独立/恢复AI拥有适用性、补证与后续route；原manual recovery共用候选hash、默认上下文保持。Architecture/RDT原promotion owners仍单写shared-current；无第二历史authority。详见[贡献](../contributions/569-fixed-cutoff-history-query.md)。
