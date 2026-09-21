# 12 最终一致性审查

## 1. 审查范围与结论口径

本轮重新读取`prd.md`、`design/01`至`design/11`、当前canonical Skill interfaces与workflow exit graph，不复用
此前pass结论。审查范围固定为：

- 10条global invariant；
- 16个lifecycle scenario；
- 22条acceptance criteria，包括`AC-454-02A`；
- 31条reachability constraint；
- primary transition matrix、8组active runtime-loss matrix、archived intent matrix与11-slot evidence invalidation matrix；
- 11个owning design中的tracked authority、ignored control state、live Git facts、public Skill I/O与migration cutover；
- #454 substrate、#443/#436 contract reconcile、受影响 package migration 与 #434 production graph activation 的
  跨任务依赖顺序；
- Create、Activate、Resume、Repair、Rebind、Checkpoint、Machine Transfer、Delivery、Publication、Merge、Completion、
  Closure、Finish、Cleanup与Reactivate的联合可达性。

审查边界是PRD声明的happy path、honest-but-fallible、单repository lifecycle与明确恢复场景。本审查不证明
代码实现、测试执行、业务repository安装或production cutover已经完成。

最终结论：问题01至11分别收敛，联合状态机不存在已知authority冲突、不可达合法路径、无owner状态、
永久fail-close或责任丢失。当前设计在PRD声明边界内完整覆盖需求。

## 2. 本轮发现与修订

本轮累计58个finding均已回写对应owning design，当前无open finding。

| Finding | 原问题 | 最终修订 |
| --- | --- | --- |
| F-454-D1 | association与ledger全丢失后revision 0与旧transaction混淆 | 引入repository-local binding epoch；new epoch/rev0使旧transaction失效 |
| F-454-D2 | Finish success被拆成独立archive与seal | 唯一成功态固定为archive tree + sealed Finish；中间态只由同一Finish recovery继续 |
| F-454-D3 | task artifact identity mismatch被当作zero-checkout | authority conflict优先于candidate selection，禁止创建第二checkout绕过 |
| F-454-D4 | Rebind只处理local branch/worktree | 同revision的local、worktree与remote resource统一退役并保留责任 |
| F-454-D5 | Closure隐含单一Issue disposition | 固定完整action set、逐项状态、部分成功恢复与external-change conflict |
| F-454-D6 | caller-owned永不删除与terminal manual cleanup冲突 | Normal Cleanup永不删除；manual route只删除用户逐项选择、fresh验证并独立确认的exact resource |
| F-454-D7 | session仍保存TaskRef/locator | stored session只保存TaskId + generation，TaskRef每次fresh解析 |
| F-454-D8 | clean-only rebind阻断dirty active task | 增加same-checkout-new-ref，固定保持HEAD、index、working tree、path与artifact bytes |
| F-454-D9 | 跨机器恢复假设未提交artifact自动可见 | 增加task-state checkpoint、explicit ref transport与`task_artifact_not_portable` |
| F-454-D10 | 跨机器只恢复checkout，未转移association与responsibility | 增加planned handoff、unavailable-source recovery与source-local handoff Cleanup |
| F-454-D11 | session write failure与lifecycle rollback边界不清 | artifact/association/ledger提交即成立；session失败只进入pointer recovery或explicit-task mode |
| F-454-D12 | identity/source/target/zero-checkout/repair缺少唯一owner | 补齐identity、lifecycle repair、source、retarget、binding establishment与ensure-checkout owners |
| F-454-D13 | source correction与retarget未完整使evidence stale | Planning、base reconcile、Task Commit、Phase 2、Branch Review、closeout Publication、Delivery Review、Delivery Publication、Completion、Closure与Finish eligibility统一失效 |
| F-454-D14 | Multi-Issue Closure未区分no-mutation basis | 固定`relation_has_no_close_authority`与`already_closed_at_review`，后者reopen进入external conflict |
| F-454-D15 | 单一current TaskLifecycleKey与并行task冲突 | state vector改为operation-scoped，禁止多个task共享current resource |
| F-454-D16 | checkpoint能写remote但无remote ownership合同 | Checkpoint与Publication共享首次create/reuse ownership规则 |
| F-454-D17 | handoff只转移单个remote resource | 转移同generation全部未收敛portable remote resource set |
| F-454-D18 | handoff artifact删除后旧机器无法判断association失效 | released/consumed/deletion history形成portable supersession receipt |
| F-454-D19 | source在prepared后不可用造成永久阻塞 | 同handoff id进入unavailable-source takeover，不创建第二transaction |
| F-454-D20 | released artifact记录carrier expected HEAD产生自引用 | carrier expected HEAD由released commit identity提供，artifact只记录head rule |
| F-454-D21 | Finish重新吸收source handoff inventory | Finish只封存current-machine inventory，排除handoff cleanup、transferred-out与retained-control |
| F-454-D22 | Closure冻结集合缺少source与Delivery target | in-progress transaction冻结TaskLifecycleKey、Completion、source、scope、target、binding、evidence与action set |
| F-454-D23 | Closure result形成后Finish未fresh读取全部Issue | Finish在任何local mutation前验证完整action set，变化固定回到Closure external-change review |
| F-454-D24 | base reconcile没有统一下游evidence invalidation | 每次成功reconcile固定使Task Commit pair及全部下游slot stale；Planning按semantic impact决定 |
| F-454-D25 | machine transfer缺少receipt ref remote-write authority | `guru-transfer-task-machine`独占TaskId-stable receipt ref create/update |
| F-454-D26 | remote handoff丢失历史resource incarnation状态 | artifact保留resource id、epoch、revision、state、ownership与responsibility role |
| F-454-D27 | Cleanup删除唯一supersession receipt | receipt ref固定`retained_control`，永不进入Finish、Normal Cleanup或manual cleanup |
| F-454-D28 | active ledger loss同时被判invalid与recoverable | `missing`固定为degraded recovery；`conflict`固定为invalid state |
| F-454-D29 | Planning到implementation activation没有owner | 新增deterministic `guru-activate-task`独占`planning -> in_progress` |
| F-454-D30 | unified state缺少scope/evidence currentness | 增加AcceptedScopeIdentity与11个EvidenceCurrentness slots |
| F-454-D31 | Closure in-progress仍允许authority/content mutation | transaction期间所有会改变frozen authority或evidence的mutation不可达 |
| F-454-D32 | public migration没有完整exit/consumer/projection | 新增独立public-contract migration设计与activation三方一致gate |
| F-454-D33 | archived source correction造成Reactivate循环 | Source owner只产出`source_correction_ready`，Reactivate在g+1 transaction原子应用 |
| F-454-D34 | existing Finalizer archive行为与Finish ownership冲突 | Finalizer与Merge不archive，terminal archive只由Finish执行 |
| F-454-D35 | handoff未携带current branch ref，zero `current_delivery`无法恢复 | artifact显式携带current branch ref；destination用该ref + checkpoint commit建association |
| F-454-D36 | Publication/Merge closing effect抢占Closure authority | 退役closing keyword writer、Issue read与`closure_mismatch`，Issue mutation只在Closure发生 |
| F-454-D37 | affected stage owners与minimal output projection不完整 | 补齐Clarify、Delivery Review/Publish、Rename及全部stage handoff named DTO |
| F-454-D38 | pre-cutover premature archive只写“Restore或Finish” | 按PR merged state固定两条Restore profile，旧Finalizer archive永不视为Finish |
| F-454-D39 | manual cleanup handoff缺少terminal Finish identity | 新增`TerminalFinishRefDTO`，manual selection始终绑定exact terminal generation |
| F-454-D40 | Planning approved直接进入Activation，绕过workflow pause | `approved`唯一consumer恢复为`phase-1-task-activation`，pause后只调用Activation owner |
| F-454-D41 | `rebind_reconcile_router`没有确定owner | 改为named non-terminal stop，保持原state；用户完成独立history reconciliation后重试 |
| F-454-D42 | closeout与Delivery两条merge链被混成一条 | 每个merge cycle固定选择一条链，只在`merged|delivered`后汇合；additional Delivery使用后续cycle |
| F-454-D43 | cross-machine validation错误分配给Session owner | destination binding只由Checkpoint + Machine Transfer组合建立，Session随后只写pointer |
| F-454-D44 | premature archive违反reachability却又被migration声明支持 | 把`archive_tree + FinishState=none`列为唯一pre-cutover degraded state并提高resolution precedence |
| F-454-D45 | DTO总规则禁止HEAD字段，但Reconcile/Merge direct consumer需要 | 只允许named operation DTO携带相邻consumer所需commit/head identity，禁止进入durable task authority |
| F-454-D46 | post-merge restore默认原head branch仍存在 | 从live merge commit采用或provision non-target recovery branch，Merge只恢复result不重放mutation |
| F-454-D47 | `public output path field count=0`会错误排除portable TaskRef | activation计数只禁止machine-local checkout/workspace path，repository-relative TaskRef继续作为合法locator |
| F-454-D48 | Completion把closeout与Delivery强制绑定同一Branch Review/Publication前置 | evidence slots拆为closeout与Delivery两组，Completion只消费当前merge lineage要求的slot |
| F-454-D49 | post-merge premature archive恢复后无法满足普通closeout evidence lineage | `TaskMergeResultDTO.merge_lineage=pre_cutover_recovered`固定消费restored/live merge事实进入migration Completion profile，不伪造旧review pass |
| F-454-D50 | Rebind idempotent result与Create/Reactivate/Rebind/Ensure transaction recovery缺少public exit | 增加`already_bound`及四个same-owner resume exit，全部使用exact transaction/result identity |
| F-454-D51 | base continuity pass丢失原`resume_target` | 新增`BaseContinuityResultDTO`，continuity router只按该target恢复原stage |
| F-454-D52 | archived source correction只传result ref，Reactivate无法确定性取得已审查source | 新增`SourceCorrectionReadyDTO`，固定携带`current_source`、`reviewed_source`、scope identity与target relation |
| F-454-D53 | retained task metadata仍让`scope`、relation与`meta`形成潜在第二authority | 为全部tracked字段固定处置；`children`/`parent`新写入只使用TaskId，legacy `subtasks`停止新写 |
| F-454-D54 | supersession receipt branch可能被branch discovery重新选为task branch | `refs/heads/guru-task-lifecycle/*`固定为reserved control namespace，全部acquisition/rebind/target validator拒绝 |
| F-454-D55 | Reactivate recovery未定义transaction generation指旧代还是新代 | public transaction固定绑定target `g+1`，private transaction同时验证source `g`与target `g+1` |
| F-454-D56 | Finish result把Cleanup seal误写成Finish authority的一部分 | Finish result固定包含terminal archive projection与sealed generation resource inventory；Cleanup result由独立Cleanup owner产生，不能反向组成Finish result |
| F-454-D57 | #454、受影响 package 与 #434 的实现顺序未形成硬性依赖合同，可能先激活上层 graph 再固化旧 substrate 假设 | 固定为“#454 contract 定稿 -> #443/#436/#434 contract reconcile -> #454 substrate 实现 -> package/schema/projection/route migration -> fresh reconcile #434 -> #434 production graph 实现与 activation”；历史 #443/#436 task 文档和旧 Issue evidence immutable，#434 只消费 substrate 不复制 authority |
| F-454-D58 | Session Association 要求 path-free `TaskLifecycleKey` handoff，但 Public Contract Migration 为 Bind success exits 使用含 `task_ref` 的 `TaskArtifactDTO` | Bind 六个成功 exits统一改为`TaskLifecycleDTO`；consumer按TaskId fresh派生TaskRef，session stored/public payload均不携带`task_ref` |

## 3. 单项收敛审查

| Problem | Result | 收敛依据 |
| --- | --- | --- |
| 01 Stable Task Identity | pass | immutable TaskId、mutable TaskRef、legacy establishment与portable boundary闭合 |
| 02 Authority Relations | pass | source、scope、target、Completion、Closure与Finish freshness各有唯一owner |
| 03 Lifecycle Incarnation | pass | generation只由Reactivate递增；activation、Finish、premature-archive migration与旧generation隔离 |
| 04 Checkout Acquisition | pass | adopt/provision统一post-state；existing active checkout由Ensure owner闭环 |
| 05 Branch Association | pass | epoch/revision、两条rebind route、rollback与handoff supersession闭合 |
| 06 Live Checkout Resolution | pass | move、zero/multiple、repository-control与cross-machine portability均有唯一route |
| 07 Resolution and Selection | pass | automatic/manual共用validator，authority conflict不可被selection绕过 |
| 08 Session Association | pass | payload只含TaskId + generation，explicit-task mode与A -> B -> A闭合 |
| 09 Ownership/Finish/Cleanup | pass | complete ledger、remote roles、Finish seal、Normal/manual/handoff Cleanup分区闭合 |
| 10 Composition/Migration | pass | state vector、31 constraints、11-slot chain-specific invalidation、transition/loss matrices、atomic cutover与跨任务实施顺序一致 |
| 11 Public Contract Migration | pass | 每个新增/受影响owner拥有完整exit、minimal output、唯一consumer、旧identity处置与跨任务承接边界 |

## 4. Global invariant review

| Invariant | Result | Joint evidence |
| --- | --- | --- |
| I-454-01 Stable identity | pass | 01 identity + 03 generation + 10 migration |
| I-454-02 Minimal portable facts | pass | 01 TaskRef boundary + 02 target + 06 live facts + 11 operation DTO |
| I-454-03 Source/scope/Closure separation | pass | 02 action-set model + 11 closing-effect retirement |
| I-454-04 Unique current branch/rebind | pass | 05 association/rebind + 09 resource succession + receipt history |
| I-454-05 Live checkout only | pass | 04 acquisition + 06 resolver + 09 path-free Cleanup |
| I-454-06 Auto/manual same validation | pass | 07 shared protocol + 06/09 applications |
| I-454-07 Path-free session | pass | 08 stored binding + 04 lifecycle/session commit boundary |
| I-454-08 Conservative ownership | pass | 09 ledger/runtime loss/manual route/complete remote transfer |
| I-454-09 Independent terminal owners | pass | 02 Completion/Closure + 03 incarnation + 09 Finish/Cleanup + 11 graph |
| I-454-10 One composition model | pass | 10 state model + 11 public graph and cutover gate |

## 5. Lifecycle scenario review

| Scenario | Result | Design coverage |
| --- | --- | --- |
| R-454-01 Issue-backed create | pass | 02 source boundary + 04 acquisition + 11 Create exits |
| R-454-02 no-Issue create | pass | 02 empty action set + 04/10 create path |
| R-454-03 pre-created checkout | pass | 04 adopt route，pre-existing resource caller-owned |
| R-454-04 Guru provision | pass | 04 create/reuse matrix，实际新建resource才是Guru-owned |
| R-454-05 resume/cross-session | pass | 08 binding/switch + 06 resolver |
| R-454-06 control-state loss | pass | 05 association + 08 session + 09 ledger + 10 eight-state matrix |
| R-454-07 explicit rebind | pass | 05 same-checkout-new-ref、existing-target与non-terminal reconcile stop |
| R-454-08 Publication/remote | pass | 09 remote-write ledger + 11 Closure effect exclusion |
| R-454-09 Finish/Cleanup | pass | 09 sealed/manual inventory、per-resource Cleanup与handoff exclusion |
| R-454-10 Reactivate | pass | 03 generation+1 + 04 shared acquisition + 09 old Cleanup isolation |
| R-454-11 rename/archive/move | pass | 01 TaskId/TaskRef + 03 archive + 06 live move |
| R-454-12 parallel task isolation | pass | 10 operation-scoped vector与constraint 28 |
| R-454-13 archived intent isolation | pass | 03 intent rules + 10 premature-archive precedence与archived matrix |
| R-454-14 cross-machine recovery | pass | 06 portability + 09 branch/ref/remote responsibility transfer + 10 handoff states |
| R-454-15 Planning activation/re-entry | pass | 03/10 status transition、Planning currentness与11 workflow pause |
| R-454-16 Closure-to-Finish external change | pass | 02 complete live reread + 10 freeze/refresh route + 11 typed exits |

## 6. Acceptance criteria review

| AC | Result | Design coverage |
| --- | --- | --- |
| AC-454-01 | pass | 10 complete vector、31 constraints、precedence与transition matrices |
| AC-454-02 | pass | 01 identity + 06 portability/live resolution + 09 receipt |
| AC-454-02A | pass | 01 explicit identity establishment + conflict matrix |
| AC-454-03 | pass | 02 source/scope/Completion/Closure + 04 create paths |
| AC-454-04 | pass | 04 adopt/provision unified post-state |
| AC-454-05 | pass | 07 shared resolution protocol + named non-terminal invalid-target behavior |
| AC-454-06 | pass | 06 moved checkout behavior |
| AC-454-07 | pass | 10 eight active loss combinations + 09 terminal loss |
| AC-454-08 | pass | 08 A -> B -> A/multi-session + 03 generation invalidation |
| AC-454-09 | pass | 05 rebind + 09 multi-revision inventory |
| AC-454-10 | pass | 05 same-ref reuse + resource incarnation identity |
| AC-454-11 | pass | 05 preserved state + 09 manual-only deletion |
| AC-454-12 | pass | 06 live resolver/common-dir operations + 09 path-free Cleanup |
| AC-454-13 | pass | 09 Normal Cleanup matrix + terminal manual cleanup |
| AC-454-14 | pass | 02 live base facts + 10 invalidation matrix |
| AC-454-15 | pass | 10 zero-reader/zero-writer activation gate + 11 retired IDs |
| AC-454-16 | pass | 10 exact tracked-field authority/storage + 11 producer/output/consumer projection |
| AC-454-17 | pass | 03 intent isolation + 10 archived precedence |
| AC-454-18 | pass | 05 dirty same-checkout route + clean existing-target route |
| AC-454-19 | pass | 09 current branch ref、zero/one current-delivery、complete remote set与receipt history |
| AC-454-20 | pass | 02/10 Closure freeze与Finish pre-mutation freshness |
| AC-454-21 | pass | 11 complete exits、per-cycle merge-chain selection、Closure-effect retirement与premature-archive migration |

## 7. Forbidden-state audit

| Forbidden condition | Result | Blocking rule |
| --- | --- | --- |
| path参与durable identity | absent | path只存在current acquisition/resolution/deletion plan |
| TaskRef/branch/Issue替代TaskId | absent | candidate必须回验canonical TaskId |
| source保存Closure disposition | absent | source只保存Issue/no-Issue identity |
| base reconcile改写metadata HEAD | absent | HEAD/base HEAD只存在live facts或相邻operation DTO |
| clean-only rebind永久阻断dirty task | absent | same-checkout-new-ref保持bytes不变 |
| rebind隐式承担history迁移 | absent | invalid target保持原state并进入named reconciliation stop |
| checkpoint冒充Task Commit/Phase 2 | absent | checkpoint只提供portable task-state bytes |
| 跨机器复制path/session/local ledger | absent | 只传TaskLifecycleKey、current branch ref、checkpoint、receipt与remote set |
| zero `current_delivery`无法恢复 | absent | declared branch ref + checkpoint commit建立destination association |
| planned handoff同时有两个current association | absent | released state零current，consume后destination唯一current |
| unavailable recovery无法失效旧association | absent | portable supersession receipt使旧machine state stale |
| prepared后source loss永久fail-close | absent | same-id unavailable-source takeover |
| session failure回滚lifecycle | absent | lifecycle commit与session pointer分离 |
| Closure期间authority/content变化 | absent | frozen set mutation全部不可达 |
| partial Closure回滚已关闭Issue | absent | 完成item保留，只继续pending |
| Merge提前关闭或验证Issue | absent | closing effect与`closure_mismatch`均retired |
| caller-owned retired HEAD阻断current lifecycle | absent | preserved state无freshness责任 |
| Normal Cleanup删除caller-owned/unknown | absent | candidate set只含Guru-owned cleanup-pending |
| manual cleanup缺少terminal identity | absent | `TerminalFinishRefDTO`绑定exact Finish generation |
| Finish重新吸收source handoff inventory | absent | current-machine inventory与handoff Cleanup分区 |
| receipt ref被Cleanup删除 | absent | retained-control永久排除 |
| old Finalizer archive被当作Finish | absent | premature archive只进入Restore migration |
| pre/post-merge premature archive走同一路径 | absent | 两个profile按live PR merged state互斥 |
| 多个active task共享current resource | absent | operation-scoped vector与constraint 28 |
| generic router执行semantic judgment | absent | router只验证discriminator/current state并映射named owner |
| Delivery cycle被closeout evidence错误阻塞 | absent | Completion按exact merge lineage选择closeout或Delivery slot set |
| post-merge migration伪造旧review pass | absent | `pre_cutover_recovered` lineage只证明live merged PR/commit，Completion重新判断scope/evidence |
| receipt ref被选为task branch | absent | reserved control namespace在全部branch target validator中被拒绝 |
| dual-read/dual-write长期兼容 | absent | one-step activation前old reader/writer/consumer count为0 |

## 8. Authority completeness

全部mutable fact都有唯一owner：

1. TaskId由Create/Identity Establishment拥有；
2. generation由Reactivate拥有，非法authority只由Lifecycle Repair修复；
3. source由Source Reconcile拥有；
4. accepted scope由Clarify Requirements active-task profile拥有；
5. Delivery target由Retarget拥有；
6. branch association由Create、Reactivate、Binding Establishment、Rebind与Machine Transfer exact mutation拥有；
7. execution checkout由live resolver解析，zero/multiple topology由Ensure Checkout闭环；
8. session pointer由Bind Task Session拥有；
9. resource ledger由acquisition、Checkpoint、Publication、Rebind、Transfer、Finish与Cleanup exact mutation拥有；
10. stage evidence由Planning、Base Reconcile、Task Commit、Phase 2、Branch Review、Closeout Publication、
    Delivery Review、Delivery Publication、Completion与Closure各自拥有一个slot；
11. terminal result与archive projection只由Finish拥有；
12. resource deletion只由Cleanup exact profile拥有；
13. pre-cutover premature archive recovery只由Restore Archived Task migration profiles拥有；
14. Issue disposition与mutation只由Closure拥有。

Public migration已经覆盖本设计引用的全部新增owner、实质变化owner、两条merge链及pre-cutover migration。
Retired workspace与archived-review IDs只存在migration inventory，没有active consumer。没有字段同时承担两类
authority，也没有合法recovery依赖stored path、old mapping、closing keyword或generic router semantic判断。

## 9. Text、scope与side-effect audit

文档固定以下边界：

- `task_workspace`只出现在问题背景、retired ID或migration说明，不再是领域对象；
- `worktree_path`、`source_checkout`与`base_head`只作为停止读取的legacy字段出现；
- “或”只用于封闭枚举、互斥route与确定性状态组合，不表达未决设计选择；
- 禁用模糊措辞扫描无命中；
- task目录仍为planning artifact；未修改Issue、production code、业务repository、commit、push或PR。
- #434 只作为 #454 substrate 的后置 consumer；本 task没有提前激活 #434，也没有把 #443/#436 历史 task 文档或
  旧 Issue evidence 回改成新 contract 证据。

## 10. Final feasibility judgment

在PRD声明的正常协作、单repository lifecycle、无hostile actor、无分布式锁/并发压力/crash-consistency扩张、
不提前激活#434的边界内，11个owning design已经单项收敛并联合闭合。16个场景、22条AC、31条reachability
constraint、8组active runtime-loss组合、57个已修订finding、跨任务依赖顺序与完整public contract graph之间不存在已知矛盾、
冲突或缺漏。

该结论证明统一task lifecycle模型在声明范围内具备一致且可实现的完整设计，不证明实现或验证已经完成。
Task继续保持`planning`；后续实现必须一次性迁移全部production consumer，并在activation前证明旧mapping reader、
writer、active domain reference、pre-Closure closing-effect owner与old public ID consumer均为零。
