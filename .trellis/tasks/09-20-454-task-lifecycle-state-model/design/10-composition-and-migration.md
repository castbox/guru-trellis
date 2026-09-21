# 10 统一状态矩阵与迁移切换

## 1. 组合目标

本文件不再新增局部领域对象。它把问题 01 至 09 组合成一个可判定状态机，并验证以下性质：

- 除create前置状态外，每次operation resolution只选择一个exact current TaskLifecycleKey；同一repository允许
  多个active task并存，但每个state vector独立求值且不得共享current resource incarnation；
- 任一稳定active generation只有一个current branch association；`handoff_released`事务态恰好零个且禁止
  普通lifecycle owner；
- 任一 resource incarnation 只有一个 ownership 与 terminal responsibility；
- 任一需要 checkout 的 operation 每次从 live Git 解析位置；
- 自动解析失败后仍存在经过同一 validator 的人工恢复入口；
- Completion、Closure、Finish、Cleanup 与 Reactivate 不共享可变 authority；
- 旧 `task_workspace`、path mappings 与 workspace public IDs 在同一 production cutover 中退出。

## 1.1 跨任务实施顺序与依赖边界

本组合设计定义的是 #454 lifecycle substrate 的消费合同，不是 #434 production graph 的提前实现计划。跨任务
执行固定为以下七个有序阶段；Phase D被拆成stage-evidence前置与两个package migration owner：

| 阶段 | 必须完成的工作 | 禁止事项 | 产出边界 |
| --- | --- | --- | --- |
| A | 定稿 #454 substrate design、state matrix、public I/O 与 migration contract | 不实现 #434 production graph | #454 可被其它 package 消费的稳定合同 |
| B | reconcile #443、#436、#434 的 package/schema/projection/workflow 承接 | 不激活 #434；不保留旧 workspace/session/Reactivate/ledger 生产语义 | 受影响 consumer 对 #454 contract 的明确承接 |
| C | 实现并完成 #454 substrate | 不在 #434 中复制 substrate authority | 可运行的 identity、generation、checkout、association、session、ledger 与 terminal-owner substrate |
| D0 | 修正Reconcile、Task Commit与Branch Review stage-evidence承接 | 不引入durable `base_head`，不以continuity替代首次full review | pre-review reconcile形成committed integration HEAD，post-review continuity边界闭合 |
| D443 | 迁移Bind package的代码、schema、projection与route | 不回改 #443历史task文档或旧Issue evidence | Session consumer消费TaskLifecycleDTO与Fork session primitive |
| D436 | 迁移Reactivate/Completion/Closure/Finish/Cleanup package的代码、schema、projection与route | 不回改 #436历史task文档或旧Issue evidence | terminal/reactivation consumer消费 #454 substrate |
| E | fresh reconcile #434 后实现并激活 Delivery 到 Cleanup graph | 不在 substrate 未就绪时实现或激活 #434 | #434 成为上层 lifecycle graph，消费而不重定义 substrate |

阶段之间是单向依赖：B依赖A，C依赖A，D0依赖A且必须在本task首次full Branch Review前完成，D443/D436依赖C与
D0，E依赖B、D443与D436。#454 不依赖 #434 的 production graph；#434只能在 #454 substrate 和受影响 contract
migration完成后消费它们。该关系不是并行双写，也不是长期兼容层。

### 1.1.1 #434 的消费边界

#434 只拥有上层 Delivery、Completion、Closure、Finish、Cleanup graph 的编排和语义判断，不重新定义或复制以下
#454/#443/#436 substrate：

- stable Task Identity 与 lifecycle generation；
- source、accepted scope、Delivery target 与 current branch association；
- checkout acquisition、live checkout resolver 与显式 branch rebind；
- path-free session association 与 session-loss recovery；
- resource ownership ledger、Finish inventory 与 Cleanup ownership boundary；
- Reactivate 的 generation、source-correction 与固定 exits。

#434 中出现的 `workspace rebinding`、`Workspace selection`、以 workspace 为中心的 Reactivate 描述，必须在
reconcile 时改写为 checkout acquisition、branch association、live resolver 与 generation-aware Reactivate。#434
不得建立第二个 resource ledger，也不得以 alternative 形式排除 #454 ledger；它只消费 #454 ledger contract。

### 1.1.2 历史 task 与迁移记录

历史 #443、#436 task 文档及其旧 Issue evidence 不回改。旧 task 只作为迁移输入或历史证据读取；新 contract
reconcile、schema/projection 迁移和实现差异由当前 package 的 migration record 或新 migration task 承接。迁移
记录必须明确 source contract、target contract、受影响 consumer、旧 identity 的处置和 activation 前置条件，不能
通过修改历史 task 文档把旧 graph 追溯标记为已迁移。

## 2. Unified state vector

每次 lifecycle resolution 使用以下完整向量：

```text
LifecycleState = (
  RepositoryContext,
  TaskIdentityState,
  TaskRef,
  LifecycleGeneration,
  WorkflowPhaseState,
  TaskArtifactState,
  TaskPortabilityState,
  SourceState,
  AcceptedScopeIdentity,
  DeliveryTargetState,
  BranchAssociationState,
  CheckoutResolutionState,
  SessionAssociationState,
  ResourceLedgerState,
  MachineHandoffState,
  EvidenceCurrentness,
  CompletionState,
  ClosureState,
  FinishState,
  CleanupState,
  DeclaredIntent
)
```

各维度封闭取值如下：

| Dimension | Values |
| --- | --- |
| TaskIdentityState | `valid`、`establishment_required`、`conflict` |
| WorkflowPhaseState | `planning`、`in_progress`、`not_active` |
| TaskArtifactState | `active_tree`、`archive_tree` |
| TaskPortabilityState | `local_only`、`portable`、`unavailable` |
| SourceState | `valid`、`establishment_required`、`conflict` |
| DeliveryTargetState | `valid`、`retarget_required`、`conflict` |
| BranchAssociationState | `current`、`missing`、`conflict`、`handoff_released`、`closed` |
| CheckoutResolutionState | `unique`、`zero`、`multiple`、`invalid`、`not_required` |
| SessionAssociationState | `current`、`missing`、`stale`、`invalid`、`unavailable`、`write_failed` |
| ResourceLedgerState | `complete`、`missing`、`conflict`、`sealed` |
| MachineHandoffState | `none`、`prepared`、`released`、`consumed`、`conflict` |
| EvidenceCurrentness | 每个固定slot分别为`absent`、`current`或`stale` |
| CompletionState | `none`、`passed`、`stale` |
| ClosureState | `none`、`in_progress`、`closed`、`no_mutation`、`stale`、`external_change_conflict` |
| FinishState | `none`、`in_progress`、`sealed`、`conflict` |
| CleanupState | `not_started`、`partial`、`complete`、`manual_required` |
| DeclaredIntent | `normal`、`establish_identity`、`establish_source`、`correct_source`、`prepare_reactivation_source_correction`、`mutate_scope`、`retarget`、`activate`、`reconcile_base`、`rebind`、`checkpoint_task_state`、`planned_machine_handoff`、`unavailable_source_recovery`、`finish_recovery`、`cleanup`、`manual_cleanup`、`reactivate` |

Path、HEAD、base HEAD、dirty paths 与 worktree topology 不是向量中的 durable state。它们是解析上述状态时
读取的 live facts。TaskPortabilityState也不是task metadata；它由exact task artifact是否进入explicit ref可达
Git history、以及目标机器能否取得该ref fresh解析。

`AcceptedScopeIdentity`是current requirement authority的内容identity，不是复制scope正文。`EvidenceCurrentness`
也不是新的总artifact或共享store；每个owner保留自己的最小result identity，resolver按以下固定slot对current
TaskLifecycleKey、scope identity、branch binding、HEAD/content与target relation逐项派生currentness：

```text
planning
base_reconcile
task_commit_pair
phase2_check
branch_review
closeout_publication
delivery_review
delivery_publication
completion
closure
finish_eligibility
```

Consumer只接受自己所需slot为`current`。Producer mutation按本文件的invalidation matrix把受影响slot派生为
`stale`；不存在跨Skill通用evidence bundle，也不允许一个slot替代另一个slot的semantic result。

Base pair不是上述slot之外的新durable authority。Pair guard/Reconcile每次fresh解析selected base、task HEAD与
merge-base。Pre-review compatible reconcile把new base纳入task committed history后，旧Phase 2、Task Commit与Branch
Review slot均stale；`post_check`与`post_commit`必须从fresh Phase 2重建。Post-review evolved-base只能在已有prior full
Branch Review时进入bounded continuity；continuity result是对新reconciled HEAD的独立review result，不复用旧pass。

## 3. Reachability constraints

以下约束定义全部稳定组合与已声明degraded recovery组合。明确列入runtime-loss、transaction recovery或
establishment matrix的状态是可恢复degraded state；其它违反约束的组合属于`invalid_lifecycle_state`，不得由
调用顺序补充解释。

1. `TaskIdentityState != valid` 时，除只读诊断与 identity establishment 外所有 mutation 不可达；
2. `active_tree` 的 source/Delivery target为 `establishment_required` 时，只允许对应 establishment；其它
   lifecycle mutation要求二者 valid；
3. `active_tree + BranchAssociationState=current + ResourceLedgerState=complete`是稳定状态；ledger=`missing`是
   runtime-loss matrix声明的degraded state，固定进入ownership recovery；ledger=`conflict`才是invalid control
   state；
4. `active_tree + BranchAssociationState=closed` 不可达；`active_tree + handoff_released`只在
   `MachineHandoffState=released`时可达；
5. `FinishState=in_progress` 不接受 rebind、retarget、Completion、Closure 或 Reactivate；
6. `archive_tree + FinishState=sealed` 是正常 archived terminal，BranchAssociationState 固定为 `closed`；
7. `archive_tree + FinishState=in_progress` 只表示新Finish的archive move已发生但尚未sealed，固定进入Finish
   recovery；`archive_tree + FinishState=none`只在能够证明由pre-cutover Finalizer形成时作为migration degraded
   state可达，按PR merged state进入`guru-restore-archived-task`的两个固定profile；其它来源的同组合为invalid；
8. `active_tree + WorkflowPhaseState=planning`允许Planning、authority establishment/correction、base reconcile、
   branch/checkout/session recovery、explicit rebind、checkpoint、machine handoff、rename与activation；它不允许
   Phase 2、Delivery、Completion、Closure或Finish。`active_tree + WorkflowPhaseState=in_progress`允许Planning
   re-entry与Phase 2及后续owner；archive_tree固定为`not_active`；
9. Completion每次只消费一个exact merge lineage。普通closeout lineage要求该cycle适用的Planning、Task Commit、
   Phase 2、Branch Review与closeout Publication slot均current；Delivery lineage要求该cycle适用的Planning、
   Delivery Review与Delivery Publication slot均current；`pre_cutover_recovered` lineage只要求Restore与Merge
   terminal-recovery已fresh证明exact merged PR/commit。Completion固定读取restored TaskArtifact、
   MergedPRRecovery result、`TaskMergeResultDTO`、current accepted scope、live merged PR/merge commit/tree与current
   planning artifact，基于这些事实独立判断完成性；它不要求也不重建旧Branch Review、closeout Publication、
   Delivery Review或Delivery Publication slot。
   未被当前lineage选择的slot保持absent或历史状态，不得被当作当前cycle前置条件；
10. `ClosureState=closed|no_mutation` 必须存在 current `CompletionState=passed`与current closure slot；
11. `FinishState=sealed` 必须存在current Closure result，且Finish entry freshness已经通过；
12. Cleanup 只绑定 sealed Finish 的同一 TaskLifecycleKey；
13. Reactivate 只从 archived + sealed Finish 进入，并创建 generation `g+1`与`WorkflowPhaseState=planning`；
14. 旧 generation Cleanup 能与新 generation active 并存，但两个 generation 不共享 resource instance；
15. Session generation 不匹配时固定为 stale，不自动升级；
16. Branch association epoch/revision 必须与 ledger current set 完全一致；
17. Caller-owned preserved resource 不承担 HEAD freshness，也不阻塞 current lifecycle；
18. Guru-owned cleanup-pending ref 未收敛前，任何 generation 不得重新占用该 ref；
19. Finish recovery 与 Reactivate intent 不得同时存在；
20. Manual cleanup 不得选择任一 active TaskLifecycleKey 的 current resource。
21. 两种cross-machine intent只接受`TaskPortabilityState=portable`；`local_only|unavailable`固定返回源机器
    checkpoint/sync route。
22. `ClosureState=in_progress`冻结其TaskLifecycleKey、Completion、source、scope、Delivery target、branch binding、
    evidence lineage与action set identity；base reconcile、source/scope/target mutation、rebind、checkpoint、machine
    handoff、Publication、Completion、Finish与Reactivate全部不可达，只允许同一Closure owner恢复。
23. `ClosureState=closed|no_mutation`进入Finish前必须fresh验证action set；required-closed Issue变化固定转
    `external_change_conflict`，Finish不得自行重判disposition。
24. `SessionAssociationState=write_failed`不回滚已提交lifecycle，固定进入`guru-bind-task-session` recovery或当前
    invocation explicit-task mode。
25. `planned_machine_handoff`建立destination association前必须关闭source association，把source
    Guru-owned local resource封存进独立handoff Cleanup inventory；portable remote responsibility只通过
    transient handoff artifact转移。
26. `unavailable_source_recovery`不消费source ledger；destination pre-existing resource固定caller-owned，
    source orphan resource只允许manual cleanup；destination建立association前必须先写入portable released
    recovery artifact，使此前machine-local association失去current资格。
27. `MachineHandoffState=prepared|released|consumed`时，普通resume、rebind、Publication、Completion、Closure、
    Finish与Reactivate均不可达；prepared进入source recovery，或在用户明确声明source unavailable后由同一
    handoff id进入unavailable-source takeover；released只进入destination consume，consumed只进入artifact
    deletion recovery。
28. 同一repository中的多个active TaskLifecycleKey分别拥有独立state vector、association、session与ledger；
    任一mutation只能改变显式选定TaskLifecycleKey及其resource，跨task共享current resource不可达。
29. 任一local association若被TaskId稳定supersession receipt ref可达history中同一TaskLifecycleKey的较新receipt取代，
    固定视为stale；planned handoff按source epoch/revision精确取代，unavailable-source recovery取代该receipt
    之前的全部machine-local association。
30. supersession receipt ref固定为`retained_control`，不得进入Finish inventory、Normal Cleanup或manual cleanup。
31. 任一mutation完成后必须按invalidation matrix更新EvidenceCurrentness；stale consumer不得继续执行或从其它
    slot推断pass。
32. `post_plan|post_check|post_commit`发现selected base尚未成为task HEAD祖先时，compatible reconcile必须创建
    expected-head-bound本地双亲merge commit；`post_check|post_commit`随后只进入fresh Phase 2，不得直接进入Task
    Commit、full Branch Review或bounded continuity。
33. Full Branch Review要求selected current base是review HEAD祖先。Bounded continuity只允许
    `post_branch_review|post_publication|finalizer_base_mismatch`，且必须存在prior full review commit并通过prior
    review/new base ancestry与candidate tree identity验证。

## 4. Resolution precedence

当多个维度同时缺失或 stale 时，固定使用以下 owner precedence：

| Order | Condition | Unique owner/route |
| --- | --- | --- |
| 1 | repository context 无法验证 | repository boundary stop |
| 2 | TaskId missing/invalid/collision | `guru-establish-task-identity` |
| 3 | Machine handoff prepared/released/consumed/conflict | exact `guru-transfer-task-machine` source recovery、unavailable-source takeover、destination consume或artifact deletion recovery |
| 4 | pre-cutover premature archive | `guru-restore-archived-task`按PR merged state选择固定migration profile |
| 5 | archived intent 未声明 | intent selection，不推断 Finish recovery/Reactivate |
| 6 | generation/status mismatch | `guru-repair-task-lifecycle`，Reactivate increment仍只属于`guru-reactivate-task` |
| 7 | source missing/conflict | `guru-reconcile-task-source` exact profile |
| 8 | Delivery target missing/conflict | `guru-retarget-task-delivery` |
| 9 | branch association/ledger missing | `guru-establish-task-branch-binding`，按 8 组矩阵执行 |
| 10 | association/ledger conflict | invalid control-state repair stop |
| 11 | operation 需要 checkout | calling owner先运行shared resolver；zero checkout固定转`guru-ensure-task-checkout` |
| 12 | session pointer missing/stale | Session Association bind/switch/explicit-task mode |
| 13 | active phase=`planning` | current Planning approval后由`guru-activate-task`进入in_progress |
| 14 | operation所需最早evidence slot absent/stale | 返回该slot原producer；不得跳到下游owner |
| 15 | Completion stale | `guru-review-task-completion` |
| 16 | Closure stale/in_progress/external conflict | `guru-complete-task-closure` exact profile |
| 17 | Finish in_progress/conflict | `guru-finish-task` recovery |
| 18 | Cleanup partial/manual_required | `guru-cleanup-task-resources` exact profile |

Task selection 与 session persistence 分离。调用方先通过显式 TaskId或当前有效 session确定 TaskLifecycleKey；
后续 session record 缺失不阻止 branch/checkout recovery。

### 4.1 Evidence invalidation matrix

下表是全部authority/content mutation的唯一invalidation规则。`current`表示保留现有slot，`stale`表示原producer
必须重建；未列出的下游slot同样按最早stale依赖传递失效。

| Event | Planning | Base reconcile | Task Commit pair | Phase 2 | Branch Review | Closeout Publication | Delivery Review | Delivery Publication | Completion | Closure | Finish eligibility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source correction | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| accepted-scope mutation | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| Delivery target retarget | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| base reconcile, no planning impact | current | current(new) | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| base reconcile, planning impact | stale | current(new) | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| same-checkout-new-ref rebind | current | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| existing-target rebind | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| checkpoint commit | current | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| destination machine-transfer consume | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| task content changes after any pass | current when planning bytes unchanged | stale | stale | stale | stale | stale | stale | stale | stale | stale | stale |
| new Branch Review result | current | current | current | current | current(new) | stale | current | current | stale | stale | stale |
| new bounded continuity result | current | current | current | current | current(new) | stale | current | current | stale | stale | stale |
| new closeout Publication result | current | current | current | current | current | current(new) | current | current | stale | stale | stale |
| new Delivery Review result | current | current | current | current | current | current | current(new) | stale | stale | stale | stale |
| new Delivery Publication result | current | current | current | current | current | current | current | current(new) | stale | stale | stale |
| new Completion result | current | current | current | current | current | current | current | current | current(new) | stale | stale |
| new Closure result | current | current | current | current | current | current | current | current | current | current(new) | current pending live freshness |

`current`表示保留原slot状态；原slot为absent时仍为absent。`current(new)`表示该event的owner形成新的current
result identity。Finish eligibility不是独立semantic artifact；它只在current Closure result存在且entry live
freshness通过时派生为current。Completion根据输入DTO类型与`merge_lineage`只选择一条lineage，禁止用另一条链的
历史slot补足当前cycle。

## 5. Primary lifecycle transition matrix

每个merge cycle在两条上游链中恰好选择一条。Task closeout链为Branch Review -> Publication Review -> Finalizer ->
Merge PR；active Delivery slice链为Delivery Review -> Publish Delivery -> Merge Delivery。同一cycle内两条链不互相
调用，只在各自形成`merged|delivered` result后汇合到Completion；Completion返回
`additional_delivery_required`时，同一TaskLifecycleKey的后续cycle进入Delivery链。Completion `completed`之后只
存在Closure -> Finish -> Cleanup。

| Current state | Intent/event | Preconditions | Mutation owner | Post-state |
| --- | --- | --- | --- | --- |
| no task | create Issue-backed task | fresh Issue intake + reviewed scope | `guru-create-task` | TaskId/gen0 active(planning)、new association epoch/rev0、ledger、one explicit session outcome |
| no task | create no-Issue task | reviewed standalone scope | `guru-create-task` | 同上，source=`no_issue` |
| no task | proposed draft | reviewed Issue payload | `guru-create-issue` | live Issue，随后 Sync + fresh Intake |
| legacy task | establish TaskId | explicit candidate + repository uniqueness | `guru-establish-task-identity` | immutable TaskId established |
| active_tree | establish/correct source | exact source choice + reviewed scope | `guru-reconcile-task-source` exact profile | source valid、dependent evidence stale |
| archive_tree + sealed Finish | prepare source correction | exact archived key + `reviewed_source` | `guru-reconcile-task-source:prepare_reactivation_correction` | no task mutation、`source_correction_ready` for Reactivate |
| active_tree | mutate accepted scope | reviewed current requirement change | `guru-clarify-requirements` active-task profile | scope identity更新、dependent evidence stale |
| active_tree | establish/retarget delivery target | reviewed target relation | `guru-retarget-task-delivery` exact profile | target valid、dependent evidence stale |
| active_tree(planning) | activate implementation | current Planning approved DTO | `guru-activate-task` | status=`in_progress`、activated或session recovery result |
| active_tree | resume | valid key + resolved control state | `guru-bind-task-session` / explicit-task route | 同 generation continuation |
| active_tree + session write_failed | recover session | exact TaskLifecycleKey | `guru-bind-task-session` recovery profile | session bound或explicit-task mode，lifecycle不重放 |
| active_tree | rename | valid TaskId | `guru-rename-task` | TaskRef 更新，TaskId/control state不变 |
| active_tree | external checkout move | valid Git registration move | caller Git operation | 下一 resolver 使用新 path |
| active_tree + zero checkout | ensure checkout | valid current association + reviewed acquisition | `guru-ensure-task-checkout` | same branch association + unique checkout + ledger resource |
| active_tree(in_progress) | reconcile evolved base before full review | current target + semantic impact review + expected-head-bound local merge commit | `guru-reconcile-task-base` pre-review profile | metadata不变、new reconcile result；post_check/post_commit回fresh Phase 2 |
| active_tree(in_progress) | reconcile evolved base after full review | current prior full review + semantic impact review + expected-head-bound local merge commit | `guru-reconcile-task-base` post-review profile | bounded continuity seed进入`guru-review-branch` continuity profile |
| active_tree | retarget | reviewed target relation change | `guru-retarget-task-delivery` | `base_branch` 更新，branch不变，旧 evidence stale |
| active_tree | rebind same checkout/new ref | unique checkout + target ref absent + no Git operation | `guru-rebind-task-branch` | HEAD/index/working tree不变、revision+1、唯一新 current branch |
| active_tree | rebind existing target | clean source + artifact/content-compatible target | `guru-rebind-task-branch` | epoch不变、revision+1、唯一target current branch |
| active_tree | checkpoint task state | local-only task artifact + confirmed commit/transport plan | `guru-checkpoint-task-state` | explicit ref可达portable artifact + remote resource ledger建立/更新 |
| active_tree | planned machine handoff | portable artifact + eligible source association/resources | `guru-transfer-task-machine` | `handoff_released` + source handoff Cleanup inventory + released handoff artifact |
| active_tree + handoff_released | destination resume | repository/ref/TaskId/generation/handoff、current branch ref与checkpoint commit匹配 | `guru-transfer-task-machine` destination-consume profile | destination在declared branch ref建立new epoch/rev0、完整remote responsibility set transferred、session/explicit mode、branch-bound evidence stale |
| active_tree + handoff prepared/released/consumed | handoff recovery | exact handoff id + state-specific facts | `guru-transfer-task-machine` recovery profile | source recovery、same-id unavailable-source takeover、destination consume或artifact deletion；不创建第二个handoff |
| portable task ref, source unavailable | recovery resume | explicit unavailable-source intent | `guru-transfer-task-machine` unavailable-source profile | released recovery artifact -> destination new epoch/rev0 -> consumed/deletion receipt；pre-existing resource caller-owned、all non-checkpoint evidence stale；随后Session owner建pointer |
| active_tree | Publish Delivery slice | current Delivery Review + live remote facts | `guru-publish-task-delivery` | Delivery PR/remote transaction ready；task仍active(in_progress) |
| active_tree | Finalizer prepare closeout PR | current Publication Review + live Git/GitHub | `guru-finalize-task` | closeout PR/remote transaction ready；task仍active(in_progress) |
| active_tree | merge Delivery/closeout PR | matching reviewed expected head + live merge facts | `guru-merge-task-delivery` / `guru-merge-task-pr` exact chain owner | delivered/merged result进入Completion；不archive task |
| active_tree | Completion passed | all scope/evidence complete | `guru-review-task-completion` | current Completion result |
| active_tree | Closure | current Completion + scope + live Issue | `guru-complete-task-closure` | `in_progress`、`closed` 或 `no_mutation` result |
| active_tree + Closure in progress | resume Closure | exact frozen action set | `guru-complete-task-closure` | continue pending items or external-change conflict |
| active_tree + Closure external conflict | re-review Closure | current Completion/scope/live Issue | `guru-complete-task-closure` semantic re-review | revised action set or explicit stop |
| active_tree | Finish | current Closure + live action-set freshness + complete resource inventory | `guru-finish-task` | archive_tree、association closed、Finish sealed |
| active_tree + current Closure | Finish freshness conflict | required-closed Issue changed | `guru-complete-task-closure:external_change_conflict` | Finish未开始、Closure重新review |
| archive_tree | Cleanup | sealed Finish + sealed ledger | `guru-cleanup-task-resources:normal_cleanup` | partial 或 complete resource result |
| archive_tree | Manual Cleanup | terminal ownership unavailable + exact selection | `guru-cleanup-task-resources:manual_cleanup` | selected resources manual_deleted |
| archive_tree | Reactivate | explicit intent + sealed Finish + reviewed source/scope/target | `guru-reactivate-task` | same TaskId、generation+1、new epoch/rev0 active(planning) |
| active_tree/archive_tree + Finish in progress | resume Finish | exact same transaction | `guru-finish-task` | sealed archive_tree 或 same-owner recovery |

每个 row 的 owner只消费当前 row 所需 authority。Delivery success不跳过 Completion，Issue closed不跳过
Closure，Finalizer/merge不提前archive，archive presence不跳过 Finish result，branch absence不证明 Cleanup success。

## 6. Active runtime-loss matrix

以下矩阵覆盖normal active state下session association、branch association与resource ledger的全部8个存在
组合。`P`表示present/valid，`M`表示missing；`write_failed`按session missing recovery处理，conflict进入invalid
control-state repair。Machine handoff非none时不使用本表，按resolution precedence直接返回handoff owner。

| Session | Branch | Ledger | Fixed recovery |
| --- | --- | --- | --- |
| P | P | P | 验证 TaskLifecycleKey，resolve checkout，正常 continuation |
| M | P | P | 保持 association/ownership；context key存在时重建 session，不存在时 explicit-task mode |
| P | M | P | 从唯一 ledger current set 恢复同 epoch/revision association；随后验证现有 session |
| P | P | M | 保持 association epoch/revision/branch；重建 current resources为 caller-owned；旧 orphan resource不自动处理 |
| M | M | P | 先从唯一 ledger current set恢复 association，再重建 session/explicit-task mode |
| M | P | M | 先按 association重建 caller-owned ledger，再重建 session/explicit-task mode |
| P | M | M | 当前 session只提供 TaskLifecycleKey；进入 candidate selection，建立新 epoch/rev0 caller-owned control state |
| M | M | M | 显式 TaskId/candidate确定 key；选择合法 branch，建立新 epoch/rev0 caller-owned control state，再 bind session/explicit-task mode |

`P/M/M` 不从 session、legacy branch field 或 cwd 推断 branch。Session只确定 TaskLifecycleKey，branch仍经过
共享 candidate protocol。新 epoch 使全部旧 rebind transaction失效。

Terminal ledger missing 不使用上表。Archived task 直接进入 `manual_cleanup_required`，不会恢复 Guru ownership。

## 7. Required scenario composition

### 7.1 Pre-created checkout

```text
reviewed source/scope/target
-> adopt_invocation_checkout validation
-> caller-owned branch/worktree projection
-> create task artifact
-> new TaskId/gen0 + branch epoch/rev0 + ledger
-> session bind or explicit-task mode
```

不创建第二个 worktree，不从 checkout name 推断 TaskId，不保存 checkout path。

### 7.2 Guru-provisioned checkout

```text
reviewed source/scope/target
-> provision branch/worktree
-> ownership按实际 create/reuse facts投影
-> create task artifact
-> new TaskId/gen0 + branch epoch/rev0 + ledger
-> session bind or explicit-task mode
```

Adopt 与 provision 的 post-state schema 完全相同。

### 7.3 Cross-session A -> B -> A

Session 1 绑定 A 不阻止 Session 2 绑定 A。单 session 从 A 切 B 时只替换 pointer，A 的 branch/ledger保持。
返回 A 时重新读取 A current generation；A 已 Reactivate时旧 generation binding被拒绝。

### 7.4 Rebind with historical resources

Revision 0 current resource退出：caller-owned进入 preserved，Guru-owned进入 cleanup-pending。Revision 1 成为
唯一 current。Finish seal同时覆盖 revision 0 pending与 revision 1 current Guru resources。Cleanup按 resource
instance逐项处理，不把“一条 Finish branch”当作完整 inventory。

### 7.5 Same-ref reuse

Caller-owned preserved ref已无 task freshness responsibility，重新选择时形成新 resource instance。Guru-owned
cleanup-pending ref在 cleaned/already-absent 前拒绝 reuse。Ref相同不表示 resource incarnation相同。

### 7.6 Caller-owned stale HEAD

Rebind 后 caller-owned旧 branch继续提交，HEAD与退出时不同。Current task的 Completion、Finish与 Cleanup不
读取该 HEAD，Normal Cleanup不删除该 branch，整个 lifecycle继续成立。

### 7.7 Checkout move and zero checkout

Registered `git worktree move` 后 live resolver取得新 path。Current branch没有 checkout时返回
`checkout_required`，reviewed acquisition创建或采用 checkout；association/session/metadata不写 path。

### 7.8 Archived intent

| Archived facts | Declared intent | Route |
| --- | --- | --- |
| Finish in progress | finish_recovery | 恢复 exact transaction |
| Finish in progress | reactivate | reject，先完成 Finish |
| Finish sealed | finish_recovery | return already sealed，不创建新 transaction |
| Finish sealed | reactivate | generation+1 transaction |
| Finish sealed | cleanup | old generation Cleanup |
| Finish sealed + terminal ledger missing | cleanup | manual_cleanup_required |

### 7.9 Reactivate before old Cleanup completes

Reactivate创建新 generation与新 epoch。旧 generation Cleanup仍读取旧 sealed ledger。新 generation不使用旧
cleanup-pending refs；其它 refs不受阻。两个 generation的 session、association、Finish与Cleanup result完全隔离。

### 7.10 Cross-machine recovery

Source machine先由`guru-checkpoint-task-state`、已有Task Commit随后由Publication传输、或Publication直接
证明exact task artifact位于目标机器可获取的explicit ref。

计划内handoff由`guru-transfer-task-machine`把source Guru-owned local resource封存进独立handoff Cleanup
inventory、关闭source association/session，并在TaskId稳定supersession receipt ref产生path-free transient handoff。Destination从explicit ref
解析TaskId、TaskRef与generation，并使用handoff声明的current branch ref和checkpoint commit建立new epoch/rev0；
local resource按实际create/reuse facts投影，全部未收敛portable remote responsibility从handoff接续。零个
`current_delivery`表示任务尚未Publication，不阻止按declared branch ref恢复；一个`current_delivery`建立new binding
successor；多个固定为handoff conflict。历史cleanup/checkpoint role保留原epoch/revision/state。Source handoff Cleanup
不进入destination Finish inventory。

Source不可用时，用户选择`unavailable_source_recovery`；destination不读取或重造source ledger，先写入
`unavailable_source` released recovery artifact，再建立new epoch/rev0；pre-existing resource全部caller-owned，
本次新建resource按create facts投影。Consumed/deletion commits保留在explicit ref可达history中，使旧机器
association固定stale。Artifact仍local-only时返回`task_artifact_not_portable`，不创建第二个task。

Supersession receipt ref固定为`retained_control`，不进入任一generation Finish/Cleanup。Destination consume后
Planning及全部非artifact evidence stale，必须从current phase owner重建。

### 7.11 Partial multi-Issue Closure

Closure固定完整action set。Issue A关闭成功、Issue B失败时整体保持`in_progress`；恢复时A live closed满足原
action且不重复mutation，只继续B。A后续被重新open时进入`external_change_conflict`并重做semantic review，
不自动重关；已完成外部mutation不回滚。

Closure整体收敛后、Finish开始前再次逐项读取live Issue。`closed_verified`或`already_closed_at_review` item重新
open时，Finish不写archive/ledger/association，固定返回Closure external-change owner；
`relation_has_no_close_authority`不因open/closed变化失效。

### 7.12 Manual cleanup without historical ownership

Terminal ledger丢失后，manual owner不要求证明历史Guru ownership或历史TaskLifecycleKey relation。用户选择
exact resource后，只验证repository/resource identity、registration、dirty/in-use与“不是任何active current
resource”，再展示并确认deletion plan。

### 7.13 Planning activation and stale re-entry

Create与Reactivate post-state固定为active(planning)。`guru-approve-task-plan:approved`只形成planning slot；
`guru-activate-task`验证该slot、TaskLifecycleKey、status与branch binding后原子写入`in_progress`。Mutation结果丢失
且status已是`in_progress`时只rematerialize`activated`。后续Planning stale只改变EvidenceCurrentness，不回退
status；最早stale slot precedence返回Planning owner，重新approval后继续原generation。

### 7.14 Closure-to-Finish freshness

Closure result已closed/no_mutation时，Finish先验证完整action set。Required-closed item变化时只形成
`closure_refresh_required`并返回Closure external-change profile；Finish transaction、archive move、inventory seal、
association close与session invalidation均尚未开始。Freshness通过后才建立Finish transaction identity。

## 8. Authority and storage table

| Fact | Storage | Key | Owner | Forbidden duplicates |
| --- | --- | --- | --- | --- |
| TaskId | tracked `task.json.id` | repository + TaskId | Create / `guru-establish-task-identity` | directory、branch、Issue、mapping |
| TaskRef | tracked tree location | TaskId resolution | `guru-rename-task` / `guru-finish-task` / `guru-reactivate-task` | absolute task path |
| Lifecycle generation | tracked `task.json.lifecycle_generation` | TaskId | Create/Reactivate | session/meta duplicate |
| Lifecycle status | tracked `task.json.status` | TaskLifecycleKey | `guru-create-task` / `guru-activate-task` / `guru-finish-task` / `guru-reactivate-task` | archive presence inference |
| Source identity | tracked `task.json.source` | TaskId | Create / `guru-reconcile-task-source` | disposition、PR/body inference |
| Accepted scope | tracked requirement/planning authority | TaskId | `guru-clarify-requirements` active-task profile | source object relation roles |
| Delivery target | tracked `task.json.base_branch` | TaskId | Create / `guru-retarget-task-delivery` | base HEAD、remote SHA |
| Current branch association | ignored common-dir control state | TaskLifecycleKey | `guru-create-task` / `guru-reactivate-task` / `guru-establish-task-branch-binding` / `guru-rebind-task-branch` / `guru-transfer-task-machine` | task.json.branch、session branch |
| Resource ownership ledger | ignored common-dir control state | TaskLifecycleKey + resource id | `guru-create-task` / `guru-reactivate-task` / `guru-establish-task-branch-binding` / `guru-ensure-task-checkout` / `guru-rebind-task-branch` / `guru-checkpoint-task-state` / `guru-publish-task-delivery` / `guru-transfer-task-machine` / `guru-finish-task` / `guru-cleanup-task-resources` | path mapping、existence inference |
| Session association | ignored common-dir session store | context key | `guru-bind-task-session` | TaskRef、branch、path、HEAD |
| Stage evidence currentness | invocation-time derivation from each owner result + live identity | TaskLifecycleKey + slot | each named producer owns only its slot | generic evidence bundle、cross-slot pass inference |
| Completion result | owner result/checkpoint + terminal archive projection | TaskLifecycleKey | `guru-review-task-completion` | Delivery result |
| Closure result | owner result/checkpoint + terminal archive projection | TaskLifecycleKey | `guru-complete-task-closure` | task source disposition |
| Finish result | tracked terminal archive summary + sealed generation resource inventory | TaskLifecycleKey | `guru-finish-task` | archive presence alone or Cleanup result |
| Cleanup result | ignored local cleanup result | TaskLifecycleKey + resource id | `guru-cleanup-task-resources` | branch absence inference |
| Checkout path/topology | live Git only | current invocation | Checkout resolver | any durable locator |
| HEAD/base HEAD/cleanliness | live Git/GitHub only | current operation | calling owner | task/session/ledger general freshness |
| Task portability | live Git object/ref availability | current checkpoint/resume operation | `guru-checkpoint-task-state` / `guru-publish-task-delivery` / `guru-transfer-task-machine` | metadata portable flag、path inference |
| Machine transfer supersession | tracked task-local `machine-handoff.json`，消费后从current tree删除；released/consumed/deletion history保持可达 | TaskLifecycleKey + handoff id | `guru-transfer-task-machine` source/destination/unavailable-source profiles | local path、machine identity、session、full ledger |
| Supersession receipt ref | TaskId-stable explicit Git ref | repository + TaskId | `guru-transfer-task-machine` | Delivery ref、checkpoint ref、Cleanup inventory |

### 8.1 Tracked task fields retained by Guru

Tracked字段使用以下封闭处置，不允许实现阶段再按字段名临时推断authority：

| Field | Post-cutover disposition | Exact consumer boundary |
| --- | --- | --- |
| `id` | immutable TaskId authority | identity resolver、全部TaskLifecycleKey owner |
| `status` | lifecycle phase/terminal authority | Create、Activate、Finish、Reactivate与phase router |
| `lifecycle_generation` | lifecycle incarnation authority | generation-sensitive owner |
| `source` | Issue/no-Issue source identity authority | Source Reconcile、Closure fresh reread |
| `base_branch` | Delivery target relation authority | Retarget、Base Reconcile、Publication/Delivery owner |
| `name`、`title`、`description` | portable display fields | Trellis task presentation；不得参与identity、scope或routing |
| `dev_type`、`priority`、`creator`、`assignee`、`createdAt`、`package`、`relatedFiles`、`notes` | portable task-management fields | 对应Trellis presentation/filter consumer；不得参与lifecycle identity或freshness |
| `scope` | legacy human-readable intake summary | 仅presentation/intake display；Planning、Completion与Closure不得把它当作accepted scope authority |
| `completedAt` | terminal presentation timestamp | 只由Finish成功投影；不得替代Completion、Closure或Finish result identity |
| `children`、`parent` | portable task hierarchy relation | 新写入只保存TaskId；legacy slug/TaskRef值只作candidate，semantic consumer必须先解析并验证TaskId |
| `subtasks` | retained legacy alias of `children`, no new relation authority | Guru新writer不得写入或同步该字段；legacy值只作hierarchy candidate，consumer解析并验证TaskId后只以`children`/`parent`为current relation authority |
| `branch`、`worktree_path`、`commit`、`pr_url` | retained legacy bytes, no Guru authority | production Guru reader/writer count固定为0 |
| `meta` | opaque upstream extension container | Guru不得在其中读写TaskId、generation、source、target、branch、path、HEAD、session、evidence、result或ownership副本 |

Legacy `base_head`、`entry_head`、workspace slug/path/mode、source checkout、重复Issue字段以及`meta`中的Guru
lifecycle副本同样停止读取。Migration不批量删除这些tracked bytes；新writer不得继续产生。`scope`与
`children`/`parent`保留只因存在明确presentation/relation consumer；`subtasks`只保留legacy bytes。它们都不形成
accepted scope或identity的第二authority。

### 8.2 Ignored repository-local layout

Implementation使用以下 ownership roots：

```text
<git-common-dir>/trellis/task-lifecycle/branches/<task-id>/<generation>.json
<git-common-dir>/trellis/task-lifecycle/resources/<task-id>/<generation>.json
<git-common-dir>/trellis/sessions/<context-key>.json
<git-common-dir>/trellis/transactions/<owner>/<transaction-id>.json
```

文件位置由 common dir提供repository scope；payload不复制本机 repository path。Branch/resource files使用
TaskLifecycleKey、binding epoch/revision交叉校验。旧 `.trellis/.runtime/guru-team/tasks/*.json` 与
`workspaces/*.json` 不迁移到上述 roots。

## 9. Public workflow and Skill migration

### 9.1 Fixed public owners

| Capability | Public owner after cutover |
| --- | --- |
| Issue creation | `guru-create-issue` |
| Task creation + atomic checkout acquisition | `guru-create-task` |
| Legacy TaskId establishment | `guru-establish-task-identity` |
| Invalid lifecycle metadata repair | `guru-repair-task-lifecycle` |
| Missing/corrected source relation | `guru-reconcile-task-source`，固定`establish_missing`与`correct_existing` profiles |
| Delivery target retarget | `guru-retarget-task-delivery` |
| Accepted scope mutation | `guru-clarify-requirements` active-task profile |
| Planning approval | `guru-approve-task-plan` |
| Planning activation | `guru-activate-task` deterministic owner |
| Task rename | `guru-rename-task` |
| Missing branch/control establishment | `guru-establish-task-branch-binding` |
| Explicit branch rebind | `guru-rebind-task-branch` |
| Existing active-task checkout acquisition/repair | `guru-ensure-task-checkout` |
| Portable task-state checkpoint | `guru-checkpoint-task-state` |
| Cross-machine transfer/recovery | `guru-transfer-task-machine`，固定source-prepare、source-recovery、destination-consume、artifact-deletion-recovery与unavailable-source profiles |
| Session bind/switch/resume | `guru-bind-task-session` new major contract |
| Base reconcile | `guru-reconcile-task-base` |
| Task work commit | `guru-create-task-commit` |
| Phase 2 semantic check | `guru-check-task` |
| Branch review | `guru-review-branch` |
| Delivery slice review | `guru-review-task-delivery` |
| Publication readiness review | `guru-review-task-publication` |
| Publication | `guru-publish-task-delivery` |
| Delivery merge | `guru-merge-task-delivery` |
| Ready task PR merge | `guru-merge-task-pr` |
| Finalization transaction | `guru-finalize-task` |
| Completion review | `guru-review-task-completion` |
| Closure transaction | `guru-complete-task-closure` |
| Finish/archive | `guru-finish-task` |
| Reactivate | `guru-reactivate-task` new major contract |
| Cleanup/manual cleanup | `guru-cleanup-task-resources` new major contract |
| Source machine handoff cleanup | `guru-cleanup-task-resources:machine_handoff_cleanup` |

Checkout acquisition 不暴露为独立 public Skill。它单独成功会留下没有 task lifecycle owner的 provisional
resources，因此不是完整 closed-loop capability。Create、Reactivate 与 Rebind共享同一 canonical
acquisition contract与 deterministic runtime primitive，并在各自原子 transaction内调用。

全部public owner的typed exits、唯一consumer、minimal projection与旧exit迁移由
`design/11-public-contract-migration.md`独占定义。本文件的owner inventory不能替代该producer/consumer合同；
任一owner缺少完整exit closure时production activation不可达。

### 9.2 Retired naming

| Old public identity | Disposition |
| --- | --- |
| `guru-create-task-workspace` | replaced by `guru-create-task` |
| `guru-task-workspace-created` | replaced by `guru-task-created` |
| `record-task-workspace-plan` | replaced by `record-task-plan` |
| `create-task-workspace` | replaced by `create-task` |
| `check-task-workspace-result` | replaced by `check-task-creation-result` |
| `recover-task-workspace-result` | replaced by `recover-created-task-result` |
| `invoke-guru-create-task-workspace` | replaced by `invoke-guru-create-task` |
| `check-workspace-boundary` | replaced by `check-task-checkout-boundary` |

旧 IDs 不保留 alias，不接受新 payload，不继续发布。`design/11-public-contract-migration.md`枚举package、schema、
command、consumer、stop、workflow marker、continuation、manifest与platform projection中的每个受影响旧 ID；
未列出的 workspace public ID 固定为 `retired_without_replacement`，且不能被实现阶段临时映射到相似新exit。

### 9.3 Configuration and vocabulary

- 删除 `workspace_mode`、workspace disposition、workspace slug 与 source checkout；
- 保留 `worktree_root`，唯一用途是 provision route 的 machine-local parent directory；
- adoption route 不读取 `worktree_root`；
- `checkout_acquisition` 只存在于 call-local semantic plan/transaction；
- active lifecycle 术语统一使用 `task`、`branch association`、`task checkout` 与 `resource ledger`；
- `workspace` 只在引用上游通用产品概念、历史字段或迁移说明时出现，不再表示 Guru domain object。

## 10. Legacy state migration

### 10.1 Tracked task normalization

| Legacy state | New reader behavior |
| --- | --- |
| valid `task.json.id` | 原样作为 TaskId |
| missing/invalid/colliding id | explicit identity establishment |
| missing lifecycle generation | read as 0，不立即写回 |
| legacy branch/worktree/path/base-head fields | 保留 bytes，停止读取为 authority |
| valid `base_branch` | 作为 Delivery target |
| missing/conflicting base target | explicit retarget establishment |
| missing `source` | explicit source-relation establishment；legacy scope/Issue fields只展示为候选 |
| legacy source含 disposition | 只提取 identity candidate；disposition不进入新 source |

任何 legacy hint 都不自动写入新 authority。合法用户选择经过新 validator后能完成 establishment。

### 10.2 Active task first use

新版本首次处理 legacy active task时：

1. 解析/建立 TaskId 与 generation；
2. 解析/建立 source 与 Delivery target；
3. 忽略旧 mappings 与 session workspace payload；
4. 从 live branch/checkouts发现 candidates；
5. 唯一 valid candidate自动建立新 binding epoch/rev0；零/多 candidate进入 selection；
6. 所有 pre-existing resource按 caller-owned建立；
7. 写入 path-free session，或进入 explicit-task mode；
8. 后续全部使用新模型。

旧 mapping存在与否不改变上述 route。

### 10.3 Archived task first use

- 只读历史不要求建立 branch/session/ledger；
- pre-cutover Finalizer造成的premature archive不构成Finish。PR未merged时进入
  `guru-restore-archived-task:pre_merge_restore`，采用exact PR head的non-target branch/checkout并返回Phase 2；
  exact PR已merged时进入`post_merge_restore`，从live merge commit采用或provision non-target recovery branch，
  随后只由`guru-merge-task-pr` terminal recovery恢复`merged` result并进入Completion；
- Finish recovery必须由显式 intent进入，并从 tracked archive/live Git重建 current owner facts；
- Reactivate必须验证 sealed Finish，再创建新 generation、new epoch/rev0；
- legacy terminal ownership无法证明时进入 manual cleanup，不读取旧 mapping重造 Guru ownership。

## 11. Atomic production cutover

Migration只允许一个 coordinated candidate，不存在长期 dual-read/dual-write mode。

### Stage A: inactive construction

在未被 workflow/registry/manifest选择的状态下完成：

- lifecycle kernel、stores、resolvers与validators；
- 新/新版 Skill packages和schemas；
- legacy first-use recovery；
- old-ID migration inventory；
- canonical、dogfood、installed与platform projection变更。

Production继续运行旧 graph；inactive code不写新 state。

### Stage B: complete consumer migration

把Create、task store、identity/source/target establishment、Checkpoint、Machine Handoff、active resolver、Session、Rebind、
Publication、Finalizer、Merge、Completion、Closure、Finish、Cleanup与Reactivate全部改为新authority。Publication、
Finalizer与Merge不得写Issue closing keyword、执行Issue mutation或验证Closure effect；Finalizer与Merge不得写
archive/terminal task state；只有Finish执行archive。Static
graph必须证明：

- old mapping reader count = 0；
- old mapping writer count = 0；
- active `task_workspace` domain reference count = 0；
- public output machine-local checkout/workspace path field count = 0；portable repository-relative `task_ref`
  不计入该项；
- `source_issue.disposition` consumer count = 0；
- pre-Closure closing-keyword writer count = 0；
- Merge closure-effect verifier count = 0；
- old public ID consumer count = 0。

任一 count非零时禁止 activation。

### Stage C: one-step activation

同一 reviewed change同时切换：

- canonical workflow invocation/exit markers；
- registry与extension manifest；
- dispatcher commands；
- public schemas/examples/consumer projections；
- preset、overlay与dogfood copies；
- platform discovery projections；
- README/spec migration contract。

Activation后只写新 control state。旧 mappings继续留在 ignored runtime，但所有 production code拒绝读取、
修复、同步或删除它们。

### Stage D: post-cutover recovery

Existing task按 10.2/10.3 first-use规则恢复。不存在后台批量 path迁移，不产生业务 repository metadata
cleanup commit，不要求用户先删除旧 runtime files。Pre-cutover premature archive必须先回到active graph；旧
archived review、archived Publication与archived Finalizer profile均不可调用。

### Rollback boundary

Activation前能整体撤回 inactive candidate。Activation后，只要任一 repository已写入新 association、ledger
或 session schema，就禁止恢复会重新写旧 mappings的 runtime。此时修复必须向前发布；旧版本不再是兼容
rollback target。

## 12. Live Issue authority deltas

2026-09-20 重新读取的 Issue #454 仍包含早期折中。当前规划根据后续用户共识固定替换以下条款，但本 task
不修改 Issue：

| Issue current wording | Final design wording |
| --- | --- |
| `task.json.source` 含 disposition | source只含 Issue/no-Issue identity；Closure独占 disposition |
| session保存 task ref | stored session payload只含 TaskId + generation |
| no context key时 task creation阻塞 | task creation完成，当前 invocation进入 explicit-task mode |
| selection-required跨 Skill输出 path-bearing candidate DTO | candidate facts只存在当前 owner对话/调用 |
| 单一 binding revision 在全丢失后重置且无隔离 | 新 binding epoch + revision 0，旧 transaction失效 |

Issue后续修订必须使用本规划的最终审查结论，不能继续保留这些已被替换的旧条款。

## 13. Composition result

本文件已给出完整state vector、33条reachability constraints、owner precedence、evidence invalidation、
主transition、8组active runtime-loss、required scenarios、authority/storage与atomic migration。
`design/11-public-contract-migration.md`独占public producer/consumer闭包；最终联合结论只由
`design/12-final-consistency-review.md`给出。
