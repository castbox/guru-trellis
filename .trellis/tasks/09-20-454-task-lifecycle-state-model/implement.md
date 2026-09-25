# #454 Phase C 与 Phase D0 实施计划

## 1. 计划目标与停止边界

本计划覆盖 #454 Phase C substrate，以及在进入 Phase D443/D436 前必须完成的 Phase D0 stage-evidence contract
migration。Phase C 交付未激活的 lifecycle substrate、public contract primitives 与 planned stable IDs；完整
canonical Skill packages 由 E434 与 selector/workflow/projection 在同一原子激活边界交付。Phase D0 修正
Reconcile、Task Commit 与 Branch Review 的承接合同，使后续 package migration 能在同一 #454 状态模型上运行。

本 task 已完成 Phase 1 semantic approval/activation 并处于 `in_progress`。本实施计划定义切片顺序与停止边界，
但不自行授权以下动作：

- 不重复运行 `task.py start` 或伪造 activation recovery；
- 不越过当前获批切片修改 workflow、active selector、active graph、installed/platform projection；
- 不创建 Fork/Guru Issue、task、branch、worktree、commit、push 或 PR；
- 不执行 merge、rebase、base reconcile、source-lock mutation或 production activation。

## 2. Current authority 与实施前置

实施读取以下 authority，并在每个 slice 开始前 fresh reread：

- live Issue `castbox/guru-trellis#454`；
- 本 task 的 `prd.md`、`design.md` 与 `design/01..12`；
- `origin/main@b4b42b49592d7bbc41caf8c0318056a0adcf6f72` 中 #456 的四份 reconcile 文档；
- current Architecture Baseline `current-main-0.6.17-guru.58`、Design Constitution v1、Architecture change
  contract v1；
- current fixed Fork source record `castbox/Trellis@43fffc170927c85d9f7fc106cc5a059e80d4530b`；
- Guru ownership inventory schema 3.0 与 subtraction-first compatibility policy。

### 2.1 Mandatory implementation admission and base reconcile

当前 task HEAD `b695adc928c2064bd27f07e2bb3bbbd034540571` 落后于
`origin/main@b4b42b49592d7bbc41caf8c0318056a0adcf6f72`，merge-base 为
`361da96327824503ffb4fb4189291b3b9b4e23ae`。

当前 task 从 Planning 进入实施必须按以下顺序执行：

1. **P0 current-session association**：现有正式 session owner fresh验证 exact task、worktree、branch、repository和
   lifecycle state。当前 session未绑定时，只走该owner已声明的rebind/recovery typed route；entry preconditions不满足
   时停在`planning_execution_blocked`。禁止手工写session、复制旧record、修补legacy mapping/task metadata，禁止用
   Phase C尚未激活的target package自举当前task；
2. **P1 committed Planning identity**：fresh approval覆盖的task-local Planning bytes必须形成一个exact local planning
   checkpoint commit。执行前单独展示stage文件、commit message、命令与“无push/remote mutation”，取得当前对话
   确认。commit后重新验证approval仍绑定同一内容；
3. **C0 post-plan pair guard**：fresh只读验证selected base `main`。approved DTO以
   `resume_target=task_activation`进入pair guard；`new_pair`在status仍为`planning`时调用
   `guru-reconcile-task-base:post_plan`；
4. 构建temporary candidate，完成normal-scenario/mechanism qualification与三维semantic review；
5. 展示exact task branch、prior task HEAD、old/new base、candidate tree、local merge commit message和零远端副作用，
   取得独立确认后完成受控reconcile；
6. 重新运行task validation、Planning delta classification与Architecture implementation-discovery re-entry；
7. `reconciled(resume_target=task_activation)`返回后，调用正式activation owner；只有checked `activated` result使
   task进入`in_progress`，随后才进入C1。

P0/P1/C0任一正式前置不满足时保持`planning`。C0 exit：`base_reconciled_and_plan_current`，随后必须成功消费
activation result。冲突、scope expansion、Architecture drift或#456 mapping变化时返回原Planning/Architecture
owner，不开始生产编辑。

## 3. Delivery policy

Phase C 是本 task 的首个独立 Delivery slice。它只交付 substrate、contract primitives 与 planned stable IDs；它不要求
Phase D443、Phase D436 或 Phase E434 已完成。C1、C2、D0、C3、C4 与 C5 已交付；PR #465、#470、#471
分别只完成 C3、C4、C5，不表示 C3-C7 已全部完成。当前 generation 4 交付 C6 task creation substrate 与
C7 subtraction/Docs SSOT/validation；D443、D436、E434 与 #434 activation 仍未完成。C6-C7 只增加非激活的
runtime/schema/Docs candidate 与 planned stable IDs，
不创建对应 canonical package directory，不切换 production graph。任何 finding fix 后均须重建 fresh Phase 2、
Task Commit 与完整 Branch Review。

独立可交付条件：

- fixed Fork prerequisite已形成 exact reviewed commit并通过本计划列出的 Fork验证；
- Guru lifecycle kernel与common-dir stores通过 package/runtime tests；
- shared DTO/schema、runtime substrate 与 E434 后续 package composition 所需的 activation inputs 闭合；
- `guru-create-task`、`guru-establish-task-identity`、`guru-establish-task-branch-binding`、
  `guru-ensure-task-checkout`、`guru-rebind-task-branch`、`guru-activate-task` 只预留 stable planned IDs；planned rows
  不携带 package/interface/I/O 字段，也不对应 canonical package directories；
- canonical extension manifest允许写入 `planned_skill_ids`，但不写 active/integrated registry selector、active graph
  manifest、installed/platform projection 或 workflow edge；
- old mappings与`guru-create-task-workspace`仍作为当前 production predecessor保留，但 Phase C 新代码零读取、
  零写入，退役由 Phase E434 activation transaction完成。

剩余工作 owner：Phase D443、Phase D436 与 Phase E434。D0 已在本 #454 task 内完成，因为它是本 task 自身 fresh
Phase 2 与完整 Branch Review 的必要承接修复；它不替 D443/D436 迁移 lifecycle package，也不替 E434 激活
production graph。

## 4. 实施切片

### C0 Base reconcile 与 authority refresh

Affected state：当前 task branch与 `origin/main`，无预先列定生产文件。

Entry：P0 current-session association已由现有正式owner证明；P1 planning checkpoint commit已完成且fresh approval仍
current；task status仍为`planning`；worktree clean；selected base与remote facts fresh。

Actions：严格执行2.1的C0步骤。禁止手工merge/rebase替代`guru-reconcile-task-base`，禁止在reconcile前激活task。

Validation：

- `git merge-base HEAD origin/main` 与 owner输入一致；
- reconcile后 #456 四份文档、Architecture `.58` 与 current ownership inventory可在工作树读取；
- task-local Planning artifacts无冲突丢失；
- task validator和 `git diff --check`通过。

Exit：`base_reconciled_and_plan_current`投影回`task_activation`；checked activation result完成后才进入C1。

Recovery：P0失败保持planning且零tracked写入；P1/C0任一Git mutation需要其独立当前对话确认。reconcile未开始时
零写入；中断或冲突由`guru-reconcile-task-base`同一owner恢复。不得reset、另建worktree、伪造recovery或丢弃用户
改动。

### C1 Fixed Fork task/session primitives

Repository owner：`castbox/Trellis`。当前 source base：
`43fffc170927c85d9f7fc106cc5a059e80d4530b`。实现前必须在 Fork repository 建立独立 live Issue/task/branch；
当前计划不预分配其编号或 branch name。

Exact framework modules：

- `.trellis/scripts/common/task_store.py`：create写 immutable `task.json.id` 和 generation `0`；rename只改 locator/
  display/back-reference；archive保留 TaskId/source/generation；不写 current branch authority；
- `.trellis/scripts/common/task_utils.py`：TaskId/TaskRef resolution、active/archive exact identity与collision检查；
- `.trellis/scripts/common/session_storage.py`：common-dir session record schema，领域payload严格为
  `task_id + lifecycle_generation`；
- `.trellis/scripts/common/active_task.py`：按TaskId fresh派生TaskRef，移除path-bearing session authority和rename
  repoint dependency；
- `.trellis/scripts/task.py`及关联 tests：public task CLI command wiring与create/rename/archive/start/current行为；
- Fork template/extraction source与golden/generated tests：保证init/update生成的上述文件来自同一 Fork source。

Fork acceptance：

- rename前后 `task.json.id` 字节相同，TaskRef/name发生预期变化；
- active/archive uniqueness同时拒绝 exact collision和case-fold collision；
- missing generation读取为0且不产生tracked rewrite，非法generation失败关闭；
- session record不含absolute path、TaskRef、branch、HEAD、ownership或authorization；
- context key缺失时不写session record；
- init/update generated bytes与Fork template/extractor一致；
- `pnpm install --frozen-lockfile`、Fork build、task CLI TypeScript tests、task/session Python tests与generated
  golden tests通过；
- touched non-generated file逐个执行3000-line检查，达到阈值时先机械拆分或小范围解耦。

Exit：`fork_prerequisite_ready(exact_commit)`。Guru repository只消费该 exact commit，不复制Fork源码。

Recovery：Fork transaction与PR recovery归Fork task。Guru source lock在Fork result进入 reviewed状态前保持原值。

### C2 Shared lifecycle kernel 与 DTO/schema primitives

Canonical Guru surfaces：

- `trellis/skills/guru-team/contracts/task-lifecycle/`：TaskId、TaskRef、TaskLifecycleKey、source/target关系、
  branch association、checkout candidate/result、resource record与Result/Transaction DTO schemas；
- `trellis/skills/guru-team/runtime/task_lifecycle/`：schema loader、normalization、TaskId/TaskRef resolver、generation
  validation与公共错误类型；
- `.trellis/spec/workflow/data-contracts.md`、`skill-package-contract.md`、`companion-scripts.md` 与
  `quality-guidelines.md` canonical/preset spec sources：只写 durable SSOT和测试口径；
- `trellis/presets/guru-team/source/trellis-source.json`、README和Architecture/RDT task-owned contribution：仅在
  Fork exact candidate reviewed后更新来源与设计承接。

Rules：

- runtime只读取Fork提供的official task/session primitives，不复制`.trellis/scripts/common/**`；
- TaskId与TaskRef严格分离；public DTO只携带direct consumer需要的最小字段；
- no-Issue与Issue source使用closed discriminated union；
- old mapping、legacy path和removed task metadata仅作为迁移盘点，不进入新reader；
- 不新增durable task identity index、compatibility alias、dual-read或dual-write。

Tests：schema正反例、TaskId exact/case-fold collision、rename/archive locator、generation 0/invalid、source union、
TaskLifecycleDTO与TaskArtifactDTO consumer projection、no absolute path/HEAD/authorization字段、source/installed schema
identity。每个非生成runtime文件保持不超过3000行。

Exit：`lifecycle_kernel_ready`。

Recovery：纯schema/runtime slice在单一Guru branch回滚；source-lock变更与Fork exact commit一起回滚，不得保留
mixed source identity。

### C3 Checkout acquisition 与 live resolution

Canonical package/runtime surfaces：

- `trellis/skills/guru-team/runtime/task_lifecycle/checkout_acquisition.py`；
- `trellis/skills/guru-team/runtime/task_lifecycle/checkout_resolution.py`；
- `trellis/skills/guru-team/runtime/task_lifecycle/git_facts.py`；
- shared schemas for acquisition plan、candidate、resolution与selection；
- `guru-ensure-task-checkout` 的 `state=planned` registry row 与 canonical `planned_skill_ids` stable-ID reservation；
  C3 不创建该 ID 对应的 canonical package directory。

Behavior：实现 `adopt_invocation_checkout` 与 `provision_linked_worktree`；所有自动/人工target使用同一live
validator；path只存在call-local plan/transaction；repository-control operation使用common-dir facts且不依赖历史
checkout path。

Tests：primary/linked adopt、new/reuse provision、wrong repository、detached、base branch、dirty、HEAD drift、zero/
multiple candidate、worktree move、explicit target fresh revalidation、output loss recovery、zero mapping access。

RDT candidate：`docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c3/` 独立承接 C3
Requirements、Design、Test 与 traceability；已提升的
`docs/requirements-design-test-contributions/454-task-lifecycle-state-model/` 继续只证明 C2+D0，保持 immutable。
Focused C3 evidence 与完整 preset suite 分开报告；raw apply 若因故意未同步的 installed projection 产生 conflict，
该 case 与 suite 保持未通过，不得通过越权同步 installed/platform bytes 修复。

Exit：`checkout_substrate_ready`。

Recovery：provision transaction按reviewed disposition记录Guru新建资源；失败只删除本transaction新建且身份仍匹配
的资源。caller-owned资源原字节保留。

Branch Review finding-fix（2026-09-22）：

- `BR454-C3-P1-003` 已修复：Git live-fact runner 将 `FileNotFoundError/OSError` 转换为共享
  `LifecycleContractError`，`inspect_registered_worktree()` 将已消失 cwd 的 registration 收敛为
  `inspection_error` candidate；真实 stale registration fixture 证明 discovery 仍可选出另一合法 checkout；
- `BR454-C3-P1-004` 已修复：公共 runtime error shape 精确保留 `code`、`field_path`、`remediation`，移除
  `details` 字段和全部第四参数调用；`target_path_conflict` 正常路径与 contract tests 精确断言 key set，并拒绝
  `message`、`details` 和 unknown alias；
- `BR454-C3-P2-005` 已修复：`CheckoutRequest` 与 `CheckoutAcquisitionPlan` 移除 `clean_required` opt-out，candidate
  validator 无条件拒绝 non-empty dirty paths，既有 dirty fixture 与字段闭包测试通过；
- finding-fix 验证：lifecycle runtime `unittest discover` 51项通过；task-lifecycle Python compile通过；task
  validate通过（缺失的 `implement.jsonl` / `check.jsonl` 按validator现有合同跳过）；workspace boundary `status=ok`；
  `git diff --check`通过；四参数error调用、legacy mapping/path authority静态命中均为0；本轮touched code/test
  文件均低于3000行。

本轮未运行或改写完整package/preset suite，已知installed projection conflict与完整Release matrix继续保持未通过/
未验证边界，不构成C3 activation或Branch Review重新通过。

Post-promotion Branch Review finding-fix（2026-09-23）：

- `BR454-C3-P2-006` 已修复：`.60` Design 的 `D454-05` 与已提升 error contract 对齐，只声明稳定
  `code`、`field_path`、`remediation`，不再保留已移除的 `details`；
- `BR454-C3-P2-007` 已修复：task lifecycle schema runtime 为 `date-time` 注册与现有 contract 一致的闭合
  RFC 3339 checker，覆盖大小写 `T/Z`、calendar validity、offset、year `0000` 与合法 leap second，并新增有效/
  非法 timestamp regression；
- `BR454-C3-P2-008` 已修复：provision creation、existing-checkout reuse 与 output-loss recovery 共用同一
  acquisition-disposition projection；恢复原 transaction 的 `action`、ownership 与 created flags，同时继续以 fresh
  branch/HEAD/checkout facts 拒绝 identity 已变化的 replacement resource；
- finding-fix 验证：lifecycle runtime `unittest discover` 52项通过；task-lifecycle Python compile通过；两组直接
  regression 39项通过；`git diff --check`通过。

本轮已运行完整 repository validation：package integration `19/20`，唯一失败仍为
`guru-complete-task-closure` 的既有相对 `$ref` 解析缺陷；runtime `119/128`、integration `38/44` 的失败仍位于
installed projection、Finish/later-slice contract 与临时 Git fixture 边界；preset suite 共 `272` 项，结果为
`2 errors, 3 skipped`，两项错误分别是 raw apply 的既有 installed projection conflict 与 parallel-finish fixture
中的同一 conflict。上述结果均不得记为通过，但未命中本轮六路径 finding-fix。C4-C7、D443、D436、E434 与完整
Release matrix继续保持后续或未验证边界。该 finding-fix 需要重新建立 fresh Phase 2、Task Commit 与完整 Branch
Review，不能复用旧 gate。

### C4 Branch association、establishment 与 rebind substrate

Canonical package/runtime surfaces：

- `trellis/skills/guru-team/runtime/task_lifecycle/branch_store.py`；
- `trellis/skills/guru-team/runtime/task_lifecycle/branch_resolution.py`；
- `trellis/skills/guru-team/runtime/task_lifecycle/rebind.py`；
- common-dir branch association schemas；
- planned `guru-establish-task-branch-binding` 与 `guru-rebind-task-branch` IDs 所需的 activation inputs；完整
  canonical packages 由 E434 交付。

Behavior：store位于Git common-dir；key为TaskLifecycleKey；record保存repository-local application control identity
`binding_epoch`、epoch内revision与portable branch ref。Association与ownership current set必须共享同一epoch、revision
与branch。单侧control state丢失时从存续侧恢复原epoch；association与active ownership全部丢失时才建立new epoch/
revision 0。Rebind只实现same-checkout-new-ref与clean existing-target两条route，保持epoch不变并严格递增revision；
不同历史返回named reconciliation stop。

Candidate label/id只服务当前选择与展示，不是freshness token。Discovery跳过全部保留的
`refs/heads/guru-task-lifecycle/*` control refs；mutation与output-loss recovery都绑定并fresh验证reviewed expected HEAD，
不能用candidate label、排序或branch name替代HEAD freshness。

Tests：epoch schema/store parity、revision 0初始化与strict increment、binding/ownership四象限的epoch恢复、全部control
state丢失新epoch、rebind保持epoch、unique/zero/multiple candidate、candidate label非freshness、mutation/recovery expected
HEAD drift、retained control-ref discovery exclusion、dirty same-checkout字节保持、existing-target exact artifact、rollback、
output loss recovery与same-ref resource incarnation exclusion。Epoch延续、新epoch、candidate-label/HEAD分离与retained-ref
过滤必须由独立回归用例证明，不得只依赖聚合四象限或schema循环断言。

Exit：`branch_substrate_ready`。

Recovery：mutation transaction保存exact pre-state；rollback恢复association与ledger revision。禁止stash、merge、rebase、
cherry-pick、reset或force push。

C4 Branch Review finding-fix（2026-09-23）：

- C4 contribution与批准设计`b695adc9`重新对齐：`binding_epoch`恢复为repository-local application control identity，
  由association、ownership、rebind与same-owner recovery共同验证；普通rebind保持epoch，只有association与active
  ownership全部丢失时才建立new epoch/revision 0；
- candidate label/id只作为call-local选择标签，不再承担freshness；establishment/rebind mutation与output-loss recovery
  绑定reviewed expected HEAD并在执行/恢复时fresh reread；
- branch discovery显式跳过retained `refs/heads/guru-task-lifecycle/*` control refs，不把machine-handoff receipt
  namespace暴露为普通branch candidate；
- C4 Test contribution把上述语义拆成实际新增的独立回归场景，不再用聚合runtime计数或同一循环内subcase声明独立
  覆盖。

C4 Phase 2 finding-fix（2026-09-23）：

- `same_checkout_new_ref` 在调用 `git switch -c` 前即进入rollback eligibility；如果 `post-checkout` hook在Git已经
  创建并切换target ref后返回非零，rollback以fresh branch state确认原branch已恢复，并且只删除仍指向reviewed
  pre-state HEAD且未被任何registered checkout使用的target ref；
- rebind transaction移除重复的`target_binding_epoch`，unchanged epoch只从
  `source_binding.binding_epoch`派生，避免一个checkpoint同时表达互相矛盾的source/target epoch；
- 新增成功same-checkout rebind后target HEAD前进的独立lost-output recovery regression，证明recovery继续绑定
  reviewed HEAD并fail closed；
- finding-fix targeted evidence为task-lifecycle runtime `93/93`、Python compile、task validation、schema/JSON parse、
  `git diff --check`与touched non-generated file 3000-line check全部通过。task validation仍将不存在的可选
  `implement.jsonl`、`check.jsonl`标记为skipped。

本 finding-fix 仅记录当前文档与对应实现/测试修订目标，不表示 fresh Phase 2、Task Commit 或完整 Branch Review 已
通过；这些门禁必须基于finding-fix后的current committed candidate重新执行。C5-C7、D443、D436、E434、#434
activation与完整Release matrix状态不变。

C4 Finalizer recovery finding-fix（2026-09-24）：

- `FIN454-C4-P1-001`：首次 Publication 尚无 Finalizer predecessor transaction 时，workflow 允许远端分支不存在、
  等于 reviewed commit，或为 reviewed commit 的严格历史祖先；现有 provenance reprepare preflight 却只接受前两种
  拓扑，导致合法的 `09f96f40... -> 4863eac4...` fast-forward publication 在任何 Git/GitHub 副作用前错误返回
  `finalization_stale`；
- 修复只收敛无 predecessor transaction 的 preflight：严格历史祖先继续进入 reprepare，并由后续 replacement
  transaction 绑定 exact `pre_push_remote_head`；ahead、diverged 或 ancestry 无法证明的 remote 继续 fail closed；
  已存在 predecessor transaction 的 exact old Publication HEAD 合同保持不变；
- Phase 2 authority review 发现 `.62` 的 `REQ-048`、`DES-046`、`TST-032` 与 `SCN-044` 仍只允许 absent/exact
  remote，与 workflow 的 strict historical ancestor 合同冲突；本 finding-fix 同步 task planning 与 current RDT，
  明确 ahead、diverged、unknown/unprovable commit 均 fail closed，旧 Architecture invocation 因此 stale 且不得复用；
- 回归使用真实临时 Git graph 覆盖 remote absent、equal、strict historical ancestor、ahead、diverged 与 unknown
  commit，不 mock `is_ancestor()`；canonical/dogfood runtime 继续要求字节一致。该修复只恢复当前 C4 Finalizer
  正式路径，不表示 Finalizer、Delivery 或 C4 merge 已完成；
- 实际验证：Finalizer provenance `21/21`、recovery `46/46`、完整 Finalizer package `109/109` 通过，task validator、
  canonical/dogfood runtime parity 与 `git diff --check` 通过；未重跑 preset `85/86`、完整 repository validation 或
  Release matrix，不得扩大验证声明；
- 修复会使当前 committed candidate、Phase 2、Task Commit、Branch Review 与 Publication 证据失效。定向验证完成后，
  必须从 fresh Phase 2 开始依次重建，禁止复用失败 invocation 的 gate、authoring 输入或 confirmation identity。

### C5 Path-free session store 与 resource ownership ledger

Canonical package/runtime surfaces：

- Fork提供的official common-dir session store由C1完成；Guru只新增session DTO adapter与consumer validators；
- `trellis/skills/guru-team/runtime/task_lifecycle/resource_ledger.py`；
- common-dir resource ledger schemas、Finish seal input primitives与Cleanup resolution primitives；
- planned `guru-establish-task-identity` ID 所需的 legacy identity establishment activation inputs；完整 canonical
  package 由 E434 交付。

Behavior：session payload严格为TaskLifecycleDTO；resource ledger按resource incarnation记录acquisition origin、ownership、
portable ref、revision、state与responsibility role；unknown ownership按caller-owned；ledger missing与conflict分开；
普通Cleanup只看到Guru-owned cleanup-pending set。

Tests：context key有/无、A->B->A、多session、generation invalidation、ledger五种acquisition projection、rebind retired
resource、active missing恢复为caller-owned、terminal missing进入manual selection、remote role、Finish seal inventory、
receipt ref retained-control排除。

Exit：`control_stores_ready`。

Recovery：session write失败不回滚已成立lifecycle；ledger mutation失败由同一transaction恢复。无法证明的历史ownership
不补写为Guru-owned。

#### C5 generation 3 implementation candidate（2026-09-24）

- 继续复用同一 `454-task-lifecycle-state-model` identity、
  `codex/454-task-lifecycle-state-model-c3-c7` branch 与现有 worktree；Reactivate generation 3 的 archive 删除和
  active task move 保持原样，不创建第二个 Issue、task、branch 或 worktree。
- C5 采用宽松且最小充分绑定：official schema-2 session record 只承载 `task_id + lifecycle_generation`；缺少
  context key 时返回 `explicit_task_mode`，零个或多个 discovery candidate 进入人工选择，显式 target 继续使用同一
  live validation contract。严格校验只约束已建立 authority 的 DTO、epoch、revision、branch 与 resource incarnation
  一致性，不把自动发现失败解释为 lifecycle 终止。
- Guru 只增加 official session primitive 的薄 adapter/consumer validation 与 common-dir resource ledger；不复制
  `.trellis/scripts/common/**`，不创建第二 session store、legacy mapping reader、alias、dual-read 或 dual-write。
- ownership 无法证明时固定为 caller-owned。active ledger missing 可在 current binding/live resources 验证后保守恢复；
  terminal ledger missing 不补写历史 ownership，进入 manual cleanup selection。普通 Cleanup 只投影
  `guru_owned + cleanup_pending`，retained `refs/heads/guru-task-lifecycle/*` control refs 永不进入普通 cleanup set。
- `guru-establish-task-identity` 只增加 `state=planned` metadata；本 slice 不创建其 package/interface/command/route，
  不修改 active selector、production workflow、installed/platform projection、D443、D436、E434 或 #434 activation。
- Task-isolated Architecture/RDT contribution 位于
  `docs/architecture/contributions/454-task-lifecycle-state-model-c5.md` 与
  `docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c5/`。当前状态为
  `contribution_candidate`；focused implementation、Phase 2 Architecture/RDT owner、serialized promotion、Task Commit、
  independent full Branch Review、Publication、Finalizer 与 Delivery 均尚未宣称通过。

### C6 Task creation substrate 与 activation inputs

Planned target Skill IDs：

- `guru-create-task`；
- `guru-establish-task-identity`；
- `guru-establish-task-branch-binding`；
- `guru-ensure-task-checkout`；
- `guru-rebind-task-branch`；
- `guru-activate-task`。

Phase C/C6 完成这些 owner 所需的 shared runtime、schemas、consumer requirements 与 activation inputs，但不为
`state=planned` row 创建 `SKILL.md`、`interface.json`、commands、package-local schemas/examples/consumers/runtime/
scripts/tests/evals。Create只消费reviewed `existing_issue | standalone_request`，不创建Issue；Activation独占
`planning -> in_progress`；同owner recovery不得重复mutation。完整 package composition 由 E434 承接。

Planned-ID boundary：

- registry可新增`state=planned` metadata，但 planned row 只声明 future stable consumer id，不携带 package/interface/
  route/I/O 字段，且 active/integrated selector继续保持predecessor selection；
- canonical extension manifest可将该ID列入`planned_skill_ids`，但`active_skill_ids`与active graph保持不变；
- canonical package directory在E434原子激活前必须不存在；
- installed `.trellis/guru-team/**`、`.agents/.codex/.claude/.cursor`投影不发布新major；
- canonical workflow与dogfood workflow不增加production mandatory invocation。

Tests：shared runtime/schema contract、no-Issue、prebuilt/provision checkout、session explicit-task mode outcome、activation
input requirements、planned/active inventory分离、planned IDs无canonical package directory与3000-line gate。Workflow/
standalone parity、entry preconditions、semantic gate、typed exits、consumer closure与package tree completeness由E434在
完整package形成后验证。

Exit：`phase_c_activation_inputs_ready`。

Recovery：每个 substrate owner只恢复自己的transaction。output loss执行read-only rematerialization；不得重复创建
task、branch、worktree、binding或ledger entry。

### C7 Subtraction、Docs SSOT 与 Phase C validation

Retirement action在Phase C只建立zero-new-reader/zero-new-writer证明；production deletion留给Phase E434 atomic activation。

Validation set：

- Fork exact commit build、focused task/session/generated tests；
- lifecycle kernel、checkout、branch、session、ledger与activation-input focused tests；
- active canonical package inventory、planned stable-ID inventory与“planned ID无package directory”检查；
- source preparation、upstream ownership、dogfood overlay drift、recursive sidecar、managed Python routing；
- one representative clean throwaway仅在当前 slice 的 accepted scope需要时证明fixed Fork生成official primitives；
  Phase C不声称安装planned package bytes；
- static search证明Phase C新代码对task/workspace mapping、`worktree_path`、`source_checkout`、legacy session path字段
  零读取零写入；
- touched non-generated file 3000-line report；
- task validator、format/lint/type checks与secret scan。

明确不运行完整多平台Release matrix；该证据仍归 #410。Phase C不把focused throwaway描述为Release Gate通过。

Exit：`phase_c_validated_inactive`。

### D0 Stage Evidence Contract Migration

Purpose：在 D443/D436 前修正现有 Reconcile/Task Commit/Branch Review 的阶段证据承接。该 slice 只处理
operation-scoped Git integration identity 与 review lineage，不新增 durable `base_head`、不改变 TaskId/
TaskLifecycleKey，也不把 Git HEAD 写入 tracked task authority。

Canonical owners：

- `guru-reconcile-task-base`：`post_plan`、`post_check`、`post_commit` 三个 pre-review profile，以及
  `post_branch_review`、`post_publication`、`finalizer_base_mismatch` 三个 post-review profile；
- `guru-create-task-commit`：继续只交付 exact committed candidate，不负责构造 old/new base pair；
- `guru-review-branch`：full review 与 bounded continuity 两种互斥 profile；
- canonical workflow、package interface/schema/consumer projection、dogfood installed copy 与 focused tests。

Pre-review contract：

1. pair guard fresh解析 selected base。只有 current selected base 已是 current task HEAD 的祖先时才返回
   `unchanged`；不得把同一时刻读取的 base SHA 同时冒充 old/new pair；
2. base 尚未进入 task committed history 时，从 live Git 唯一 merge-base派生 operation-scoped old base，构建
   candidate并完成semantic impact review；
3. compatible result在用户确认 exact branch、expected prior task HEAD、new base、candidate tree、双亲顺序、merge
   message与零远端副作用后，创建 expected-head-bound 本地双亲 merge commit，parents 固定为
   `[prior_task_head, new_base_head]`；
4. `post_plan`保留`resume_target=task_activation`；`post_check`与`post_commit`形成merge commit后固定回 fresh
   Phase 2，旧 Phase 2、Task Commit 与 Branch Review evidence全部 stale，不得直接进入 Task Commit或full Branch
   Review。

Full Branch Review contract：

- 首次/full review只审查 committed `origin/<selected-base>...reconciled-HEAD`；selected base必须是review HEAD祖先；
- `post_commit`不是 bounded continuity entry；current base尚未进入task history时不得用triple-dot审查替代reconcile；
- bounded continuity只允许`post_branch_review`、`post_publication`与`finalizer_base_mismatch`，并要求prior full
  Branch Review commit、new base与current reconciled HEAD满足ancestry和candidate tree identity合同；
- continuity只承接已存在的full review，不得为首次full review造出pass。

Base updates carried into migration ledger：

- #459 的日期前缀 TaskRef locator 行为保留到 D436 Reactivate major替换；target实现仍以`task.json.id`为TaskId
  authority，不复制旧 locator/result结构；
- #460/#462 的created Issue target provenance、schema 3.0一致性与output-loss recovery不重复创建Issue的行为保留到
  E434切换`guru-create-task`；target实现不复用旧nested result/digest或workspace mapping。

Validation：Reconcile/Branch Review package unit/contract tests、base-continuity integration、workflow/package contract、
consumer projection、canonical/installed parity、preset reapply/drift、task validation、`git diff --check`，并证明
`.trellis/scripts/**` diff为零。

Exit：`stage_evidence_contract_ready`。该exit只表示D0 candidate完成；随后对本task执行正式base reconcile，并按
`fresh Phase 2 -> fresh Task Commit -> full Branch Review`重建证据。它不表示C3-C7、D443、D436或E434完成。

## 5. Subtraction 与兼容策略

Direct evolution选择：replace + synchronized later retirement。

- Phase C新增target-native substrate，新代码不读写old mappings；
- predecessor `guru-create-task-workspace`、mapping runtime与旧session contract在Phase C保留为active production，
  只因Phase E尚未切图；
- Phase D0先修正stage-evidence承接；D443/D436再迁移package major，但不翻active selector；
- Phase E在一个activation transaction中切换workflow/registry/manifest/projections并删除old readers/writers/IDs；
- 不存在兼容alias、长期adapter、dual-read、dual-write或两套owner同时active的中间态。

完整disposition见 `planning/phase-c-migration-retirement-ledger.md`。

## 6. Architecture 与 Docs SSOT

本变更是 `architecture_impact / target_native`：它改变task identity、session、branch、checkout、resource ownership
与Fork/Guru owner boundary。Planning contribution位于 `planning/architecture-change-contract.md`；shared current
Architecture/RDT只在独立Branch Review后由serialized promotion owner更新。

Durable Docs SSOT候选：

- `.trellis/spec/workflow/data-contracts.md`；
- `.trellis/spec/workflow/skill-package-contract.md`；
- `.trellis/spec/workflow/companion-scripts.md`；
- `.trellis/spec/workflow/quality-guidelines.md`；
- 已提升且 immutable 的 `docs/requirements-design-test-contributions/454-task-lifecycle-state-model/**`；
- C3 task-isolated candidate `docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c3/**`；
- task-local `planning/architecture-change-contract.md`，shared `docs/architecture/**` 只允许 serialized promotion owner 写入；
- `README.md`、canonical workflow/package README与preset README中的current source/ownership/migration说明。

这些shared路径只在实施/检查阶段修改。本Planning不直接修改shared current authority。

## 7. Final acceptance

Phase C通过条件：

1. P0、P1、C0、activation与C1至C7按顺序完成，每个boundary/slice满足entry、validation、exit与recovery合同；
2. fixed Fork exact commit是official task/session primitive唯一source，Guru diff中无`.trellis/scripts/**` patch；
3. lifecycle substrate与六个owner的activation inputs就绪，stable IDs保持planned，且planned IDs不存在canonical
   package directory；
4. #456标为Phase D/E的33项不被Phase C越权实现或激活；
5. new substrate对old mappings零读取零写入，old production predecessor未被半切换；
6. shared DTO每个字段都有named direct consumer，每个exit有唯一consumer；
7. no-Issue、rename、move、session loss、binding/ledger loss、rebind与output-loss recovery具备deterministic tests；
8. current Architecture contribution完成独立Phase 2、Task Commit、full-diff Branch Review与promotion前置；
9. focused validation与Release matrix边界如实报告；
10. 所有touched non-generated code file不超过3000行，或在同一slice先完成reviewed split。

Phase C完成后仍禁止production activation。后续固定先完成Phase D0，再进入Phase D443与Phase D436，最后由
Phase E434 fresh reconcile并执行atomic activation。#459、#460/#462 仅以迁移账本中的行为保证被承接，不把旧
predecessor数据模型带入target graph。

## Publication finding-fix（2026-09-23）

- `PUB454-C3-P2-009`：active task 已进入 `in_progress / lifecycle_generation=1`，但工作树仍跟踪上一轮
  `completed` closeout 生成的 `finish-summary.json`。该旧摘要绑定 commit `2ba449e3a2456479bbb58bad48d22ae02451c859`，
  不能作为当前 generation 的 Finalizer 输出。
- 修复：删除 active task 中的 tracked 旧摘要，恢复 `guru-finalize-task` 对摘要的唯一所有权；当前 generation 的
  `finish-summary.json` 必须在正式 Finalizer transaction 中重新生成为 untracked archive output，并随 task move
  进入 archive。
- 验证：先执行 focused Finalizer preflight，确认旧的 archive-output classification/subset 错误消失；再执行 task
  validator 与 `git diff --check`。本次 finding-fix 使既有 Publication 证据失效，后续必须从 fresh Phase 2、Task
  Commit、full Branch Review 到 fresh Publication 依次重建，不得复用上一轮 ready/finalization 结果。

## Branch Review finding-fix（2026-09-22）

- `BR454-C3-P2-010`：`recover_checkout_acquisition()` 在原 provisioned linked worktree 已移除、同一
  branch/HEAD 又由 caller 于新路径重新创建时，把 replacement registration 当作原 transaction 的 moved checkout，
  并恢复为 `created_worktree_for_existing_branch / guru_owned / created_worktree=true`。这会把 caller-created
  resource 错误交给后续 Cleanup。
- 修复：output-loss recovery 只接受原 call-local transaction 的 exact `target_path`；不同路径固定返回
  `acquisition_result_mismatch`。普通 `git worktree move` 仍由 live checkout resolution 支持，但不在 output-loss
  recovery 窗口中猜测为同一 transaction；未新增 durable path、workspace mapping、receipt 或第二 ownership owner。
- 回归：新增 same branch/same HEAD replacement 用例，证明 recovery fail closed 且不修改 replacement resource；
  原 output-loss rematerialization、changed-HEAD replacement rejection 与 worktree-move resolution 用例继续通过。
- 验证：targeted regression `1/1`、完整 lifecycle runtime `53/53`、task-lifecycle Python compile、DTO JSON、
  `git diff --check` 通过。该 finding-fix 必须重新建立 fresh Phase 2、Task Commit 与完整 Branch Review；不得复用
  `f7718c21` 的 `implementation_required` checkpoint 或更早 Publication/Finalizer 证据。

## Branch Review finding-fix（2026-09-23）

- `BR454-C3-P2-011`：仅绑定 exact path、branch 与 HEAD 仍不能证明 output-loss recovery 找到的是原 transaction
  创建的 linked worktree；原资源被移除后，honest caller 可在同一路径用同一 branch/HEAD 创建 replacement，旧恢复逻辑
  会错误恢复 `guru_owned` disposition 并把 caller resource 交给后续 Cleanup。
- Solution mechanism qualification 已以 `BR454-C3-MECH-012` 返回 `qualified_current`；正式 continuation 为
  `solution-mechanism:33fd356ff8c91a1ae48892d7`。机制只在 transaction-created linked worktree 的 Git
  administrative directory 写入一份闭合普通 JSON provenance marker，绑定 transaction/result、task/generation、
  branch/HEAD、target、disposition、action 与 ownership projection；recovery 必须同时满足 fresh live Git facts 与
  marker exact match。existing-checkout reuse 继续为 caller-owned，不写 marker。
- Architecture implementation-discovery 已返回 `baseline_current`，绑定 current `.60` 与新的 task-owned
  `architecture-contribution-454-task-lifecycle-state-model-c3-provenance-v1`；promotion state 为
  `reviewed_candidate`。该 marker 不是 task/session/branch/workspace/resource-ledger authority，不引入 lock、inode、
  PID、process、FD、signal、workspace mapping、resource ledger 或第二 ownership owner，`git_facts.py` 无需修改。
- Marker lifecycle：provision 成功后创建；read-only output-loss recovery 只验证、不修改；`git worktree remove` 随原
  administrative directory 一并移除，因此 same-path/same-branch/same-HEAD replacement 缺少 marker 并 fail closed；
  direct handoff 在调用 `post_acquire` 前先 retire marker。Implementation review 已修正 callback ordering，避免下游
  consumer 已接受 resource 后 marker 删除失败又触发 rollback；marker retirement 或 callback 失败均只回滚本
  transaction 创建且身份仍匹配的资源。
- Focused 验证：checkout substrate `27/27`、完整 task lifecycle runtime `56/56`、Python compile、task-lifecycle
  JSON parse、ownership `32 active + 1 planned`、task validator、workspace boundary、legacy mapping/path-authority
  零命中、forbidden OS/process/lock mechanism 零命中、touched file line limits 与 `git diff --check` 均通过；
  marker coverage 包含正常 output-loss recovery、different-path 与 same-path replacement rejection、missing/mismatched
  marker、successful handoff 前 retirement 及 callback failure rollback。
- Fresh broader repository validation 保持真实非通过边界：package integration `19/20`，唯一 error 仍为
  `guru-complete-task-closure` 相对 `$ref`；shared runtime `119/128`（`6 failures, 3 errors`）；lifecycle integration
  `38/44`（`6 failures`）；preset suite `272` 项为 `2 errors, 3 skipped`，两项 error 仍是 raw apply installed
  projection conflict 与 parallel-finish fixture 中的同一 conflict。上述失败未命中本次 provenance marker 路径，
  但不得记为 suite 通过；C4-C7、D443、D436、E434 与完整多平台 Release matrix 继续为后续或未验证边界。

## Branch Review finding-fix（2026-09-24）

- `BR454-C4-P2-SSOT-001`：`.62` Architecture、Requirements、Design、Test 入口与 C4 contribution provenance 仍只
  绑定 C4 branch association/establishment/rebind contribution 加 immutable `.61`，没有显式承接同一 committed
  range 中新增的 Finalizer strict-ancestor recovery 与 `pre_push_remote_head` transaction authority。该缺口属于
  正常维护中的 source binding/provenance 不完整，不通过 branch、PR 或路径元数据补偿。
- `BR454-C4-P2-TXN-002`：当前 Finalizer runtime 已由 application-level replacement transaction 绑定 exact
  `pre_push_remote_head`，但 regression 只覆盖独立 ancestry preflight，没有覆盖正式
  `execute_finalization_transition_result` composition、transaction 写入与后续 pre-mutation preflight 的同一
  remote identity。修复只增加真实 Git graph 的执行级回归，不改变 runtime 机制，不引入锁、并发、fault injection
  或 OS/process authority。
- 两个候选均已通过 `guru-qualify-normal-scenario` 与 `guru-qualify-solution-mechanism` 的
  `branch_review_candidate_set` qualification，结果均为 `qualified_current`；本轮实现完成后必须从 fresh
  Phase 2、Task Commit 与完整 Branch Review 重新建立 gate，不能复用本轮 `implementation_required` 或此前
  Architecture/Publication/Finalizer evidence。C5-C7、D443、D436、E434、#434 activation 与 Release matrix
  仍不在本 slice 内。
- finding-fix 已补齐 `.62` Architecture/RDT 入口、C4 contribution/manifest 与 current trace 的 Finalizer
  provenance source binding，并新增正式 `execute_finalization_transition_result` composition 回归。验证结果：
  Finalizer provenance `22/22`、完整 Finalizer package `110/110`、Python compile、YAML/JSON parse、task validator、
  touched non-generated file line limit 与 `git diff --check` 通过；validator 继续将不存在的可选
  `implement.jsonl`、`check.jsonl` 标为 skipped。上述结果只证明本 finding-fix implementation candidate，尚未
  建立 fresh Phase 2、Task Commit 或完整 Branch Review。

## C4 Finalizer recovery finding-fix（2026-09-24）

- `FIN454-C4-P1-002`：正式 Finalizer invocation 已合法从 reviewed content `3c9ecc58` 创建 provenance tail
  `af719fbb`，并建立 `ordinary_publication/push_content` transaction；remote 与 transaction-bound
  `pre_push_remote_head` 仍为历史 merged PR #469 的 `09f96f40`，当前没有 Open PR，且尚未 push 或 archive。
  现行 recovery classifier 在承认该 identity-matched transaction 的 current ownership 前，错误地把同
  branch/base 的历史 terminal PR 解释为 current candidate 冲突。
- Reactivate branch reuse 的正常恢复以已有且身份匹配的 `ordinary_publication/push_content` transaction 为 current
  owner。没有 Open PR 时，同 branch/base terminal PR 只作为历史事实；live remote 等于 transaction
  `pre_push_remote_head` 时允许执行一次到 `publication_head` 的 fast-forward，等于 `publication_head` 时视为合法
  push-output-loss/converged state 并继续同一 transaction recovery。remote 位于这两个 allowed heads 之外、
  ahead/diverged/unknown/unprovable，出现 Open PR drift，或 transaction identity 不匹配时均 fail closed。
- 该恢复不增加宽泛 fallback、PR 人工选择 API、force push 或第二 ledger，也不删除、改写或手工绕过 transaction。
- 实现删除 transaction-owned no-Open-PR 路径对 terminal PR inventory 的读取，保留既有 transaction plan validation
  与 remote allowed-head preflight；canonical/dogfood runtime 字节一致。新增真实 Git regression 覆盖历史 terminal
  PR、`pre_push_remote_head`、`publication_head` 与 allowed-head 外 drift。验证结果为 recovery `47/47`、完整
  Finalizer package `111/111`、Python compile、task validation 与 `git diff --check` 通过。
- 上述结果只证明当前 finding-fix implementation candidate，不表示 fresh Phase 2、Task Commit、Branch Review、
  Publication、Finalizer 或 Delivery gate 已通过。C5-C7、D443、D436、E434、#434 activation 与完整 Release matrix
  仍未完成。

## C4 Branch Review transaction endpoint finding-fix（2026-09-24）

- `BR454-C4-P1-003`：transaction-bound remote guard 把 distinct intermediate `branch_review_commit` 与
  `pre_push_remote_head`、`publication_head` 一并视为合法恢复端点；当 remote 由正常外部操作推进到 review commit
  但尚未到 publication commit 时，现行 preflight 会错误放行后续 publication push。
- 修复保持 transaction 为唯一 current recovery owner，只允许 transaction 创建时观察到的
  `pre_push_remote_head` 与 exact `publication_head`。中间 review commit、allowed heads 外 remote、Open PR drift 与
  transaction identity drift 均继续 fail closed；不增加严格 branch/session 绑定、人工选择 API、force push、第二
  ledger 或 fallback。
- 真实 Git regression 使用三个互异 commit，分别表示 historical remote、branch review 与 publication；明确断言
  historical remote 和 publication endpoint 可恢复，而 intermediate review commit 返回
  `finalizer_remote_head_drift`。Architecture 已返回 `fitness_regression -> implementation`；修复后必须重建 fresh
  Phase 2、Task Commit 与完整 Branch Review，当前 Publication 与 Finalizer transaction 不得继续消费。
- Fresh implementation validation：Finalizer recovery `47/47`、完整 Finalizer package `111/111`、task validator、
  canonical/dogfood runtime parity 与 `git diff --check` 均通过；Finalizer transaction SHA-256 仍为
  `af9efa059754058b63c24398856adc4ef65c9c6fa48cf472c731ac94a8b86b3b`，本轮未修改该 transaction。

## C4 same-base transaction reprepare finding-fix（2026-09-24）

- `FIN454-C4-P1-004`：合法 C4 finding-fix 在 predecessor provenance Publication `af719fbb` 后形成
  `e1dd7c7c -> d3ac0a07`，current Branch Review、Publication 与 live HEAD 已重新绑定同一 reviewed descendant，
  selected base `origin/main@77fa1a2` 未变化。现行 classifier 只接受 base 演进后的 fresh-reviewed descendant，
  因而把同 owner、同 base、尚无 Open PR 的 pre-push reprepare 错误判为
  `provenance_tail_transaction_rebind_invalid`。
- 修复遵循宽松且最小充分的绑定原则：只要求 existing unbound
  `ordinary_publication/push_content` transaction 的 task/repository/base/head branch/mode/stage 一致；predecessor
  review 到 Publication 相等或为合法 provenance tail；selected base 已包含于 predecessor Publication lineage；
  current Branch Review、Publication、live HEAD 相等且严格后继；task 未 archive 且没有 Open PR。历史 terminal PR
  不作为 current candidate。
- remote 只接受 transaction-owned `pre_push_remote_head` 或 exact `publication_head`；中间 reviewed commit、其它
  remote endpoint、Open PR、identity/lineage/tail/state drift 均 fail closed。合法路径复用既有
  `reprepare_required/provenance_metadata_tail` 与 replacement transaction，不增加 schema、public DTO、人工
  selector、fallback、force push、第二 ledger 或 branch/session/path 严格绑定。
- 真实 Git regression 覆盖 old-review -> valid old provenance tail -> two finding-fix commits、历史 terminal PR
  忽略、Open PR 拒绝、两个 transaction-owned remote endpoint 接受、中间 remote 拒绝，以及 replacement
  transaction 绑定 current plan 与实际 observed remote。该 finding-fix 完成后必须从 fresh Phase 2、Task Commit
  与完整 Branch Review 重新建立 gate；当前 Publication/Finalizer 输入不得继续消费。
- Fresh implementation validation：Finalizer provenance `23/23`、recovery `48/48`、完整 package `113/113`、
  canonical/installed runtime parity、canonical/dogfood spec parity、Python compile、task validator、专用 dogfood
  drift 与 `git diff --check` 均通过。raw preset apply 仍因三项既有 pre-E434 task-lifecycle installed sidecar 返回
  `conflict`，未被清除、覆盖或误报为通过；该边界与此前 preset `85/86` 一致。本段不表示 Phase 2、Task Commit、
  Branch Review、Publication、Finalizer 或 Delivery 已通过。C5-C7、D443、D436、E434、#434 activation 与完整
  Release matrix 状态不变。

## C5 implementation review finding-fix（2026-09-24）

- `C5-P1-SESSION-001`：session adapter 原实现先写 official record，再 fresh resolve `TaskId + generation`；stale
  target 会返回 `session_invalid` 但留下无效 binding。修复改为 mutation 前先走 official resolver，只有 exact current
  lifecycle 可写；write 后仍重新读取 exact schema-2 record。该顺序不增加 branch/path/Issue selector，context key
  缺失仍进入 `explicit_task_mode`。
- `C5-P1-RECOVERY-002`：新增 transaction schema没有runtime producer/consumer，active-missing 与remote-delivery
  mutation 在成功后丢失 output 时也无法只读恢复。修复删除 speculative checkpoint schema，并让两个操作只在现有
  ledger 等于 exact expected successor 时 rematerialize 原结果；任何 revision、ownership、ref 或 cleanup-head mismatch
  继续返回 conflict，不重复 ownership mutation。
- `C5-P2-PARITY-003`：Cleanup runtime DTO 与 resource ledger schema 未完整承接 role/state/ownership/ref 不变量。
  修复增加 runtime closed validation，并使 ledger schema拒绝非retained role使用control ref、role/state/ownership
  不一致等组合。严格性只作用于已建立 authority，不改变 unique candidate自动选择、zero/multiple人工选择和explicit
  target同validator路径。
- 本轮仍只修改 C5 substrate、candidate contribution 与 task-local实施记录；shared current `.62`、production workflow、
  installed/platform projection、D443、D436、E434 与 #434 activation 均未修改。修复后必须重新运行 focused runtime、
  schema、compile、task validator、line limit 与 `git diff --check`，再进入 fresh Architecture/Phase 2。

### C5 独立 checker finding closure（2026-09-24）

- `C5-P1-REMOTE-004`：checker 建议用 pre-mutation ledger revision/snapshot identity 约束 remote-delivery
  output-loss recovery。该建议会把局部幂等读取升级为严格 transaction protocol，与 #454 的宽松最小充分绑定原则及
  不新增第二 transaction store 的边界冲突。实际 closure 明确区分：active-missing 仍要求 exact whole-ledger
  successor；remote-delivery 只要求 exact current resource incarnation 仍绑定同一 branch/epoch/revision。无关合法
  retained-control mutation 不使该结果失效，也不触发 ledger rewrite。
- `C5-P1-BRANCH-005`：ledger 原先只校验 current worktree 与 current branch 的 ref 一致，current delivery 仅校验
  epoch/revision。修复使 current delivery 同样必须绑定 current branch 的完整 ref；不一致在构造 successor、读取或恢复
  时均返回 conflict。该约束只作用于已建立 resource authority，不参与 task discovery 或 selector。
- `C5-P2-PARITY-006`：runtime 仅按 reserved prefix 识别 retained-control ref，而 schema 另有 suffix domain。修复让
  runtime 与 schema 共同要求合法 Git branch ref 并保留 `guru-task-lifecycle` reserved namespace，非法空格等 suffix
  在两侧均被拒绝。
- 新增 focused coverage 验证 mismatched delivery branch rejection、非法 retained-control ref runtime/schema parity，
  以及无关 retained-control mutation 后 exact current delivery 仍可只读 rematerialize。本 closure 不新增 selector、
  transaction token、checkpoint schema、branch/session/path 严格绑定或 ownership 推断。

### C5 第二轮独立 checker finding closure（2026-09-24）

- `C5-P1-CURRENT-007`：runtime/schema 原先允许只有 `current_worktree` 或 `current_delivery`、没有
  `current_branch` 的孤立 ledger。修复要求任一 current attached resource 都必须存在唯一 current branch，再执行
  epoch/revision/ref alignment；该不变量只验证已建立 ledger，不参与 candidate discovery、task selection 或人工绑定。
- `C5-P2-REF-008`：retained-control ref 的 runtime/schema 正则虽已同构，但共同遗漏 ASCII control/space domain。
  修复在两侧拒绝 `0x00-0x20` 与 `0x7f`，并增加 tab、newline、NUL、DEL parity 负例；合法 reserved control ref
  继续可用于 handoff/receipt responsibility。
- reviewer 同时确认 `C5-P1-REMOTE-004` 的最小充分 closure 成立：无关合法 ledger mutation 后，相同 current
  remote incarnation 仍只读 rematerialize，未新增 ledger-wide expected revision、transaction token 或第二 store。

### C5 promotion 后完整 Branch Review finding-fix（2026-09-25）

- `C5-BR-FINISH-SEAL-RETRY-001`（P2）：首次以 H1 seal 后，普通输出丢失重试若传入 H2，原实现不再修改已退休的资源，
  却返回 H2，导致 Finish 返回值与 Guru-owned cleanup HEAD 不一致。修复在同一 ledger 记录 exact Finish result/HEAD；
  同身份重试只读返回，不同 result/HEAD 拒绝，Cleanup 验证 sealed result。保留后续合法 retained-control 记录时的
  Finish 身份；不增加第二 store、通用 ledger transaction token、strict selector 或 production graph 激活。
- 对应 closed schema、runtime、focused tests 与合同说明同步。该编辑仅形成 finding-fix candidate；须在定向验证后
  重新运行 fresh Phase 2、Task Commit 与包含既有 `.63` promotion 的完整 Branch Review，不复用此前 gate。

### C6/C7 promotion 后完整 Branch Review finding-fix（2026-09-25）

- `C6C7-BR-TASK-ID-001`（P1）：创建准备原先只扫描 task artifacts，未检查 Git common-dir 中尚未退休的 C5
  resource ledger。现在复用唯一 ledger 的 `iter_ledgers()`，在 mutation 前拒绝相同 TaskId（含大小写折叠）
  的未解决责任记录；不新建索引或路径 authority。
- `C6C7-BR-RECOVERY-002`（P2）：创建 output-loss recovery 原先只比对 current ledger 的 role、epoch、revision
  和 ownership，可能将不同 branch 的 ledger/binding 当作相同结果。现在对 current branch/worktree 的 portable
  ref 与 C4 binding 做 exact 比对，不一致 fail closed，不重复任何控制状态 mutation。
- 两项均通过正常路径资格与 application-level mechanism 门禁。新增真实 Git/store API 回归；focused composition
  `14/14`、完整 lifecycle `127/127`、Python compile、task validator、`git diff --check` 已通过。package integration
  `19/20` 与 managed verifier fixture 不声明通过。此处是修复候选，仍须 fresh Phase 2、Task Commit 与另一位
  独立 reviewer 覆盖 `origin/main...HEAD` 全范围，随后才可进入 Publication。

### C6/C7 fresh final review finding-fix（2026-09-25）

- `C6C7-BR-CROSS-CHECKOUT-ID-003`：创建预检只扫描当前 checkout 的 task artifact；旧 task 在另一已注册
  worktree 归档且资源责任已退休时，相同 TaskId 可被新创建输入接受。Issue #454 的 repository-lifecycle
  TaskId 唯一性要求覆盖此正常路径。修复从 Git common-dir 的 worktree registration 枚举 task inventory，
  保留现有未退休 ledger 检查；不可读取的注册 checkout 在创建前阻断，不推断身份或创建额外持久状态。
- 正常路径和 application-level mechanism 资格均已分类。真实 Git/worktree 回归覆盖另一 checkout 独有的归档
  与缺失旧 ledger；composition `15/15`、完整 lifecycle `128/128`、Python compile、task validator 与
  `git diff --check` 通过。本项仍须 fresh Phase 2、Task Commit 与另一位完整范围审查。

### C7 current projection finding-fix（2026-09-25）

- `C6C7-BR-STALE-SPEC-PROJECTION-004`：`.64` 已经是唯一 active Architecture/RDT，两个项目本地
  `.trellis/spec/` 使用规则却仍声明 `.63/active`。普通 gate 的读入与自身 freshness 条款发生冲突。
  经正常路径与机制资格分类后，直接演进两个 subordinate current 使用投影至 `.64` 与 C6/C7 source；
  不修改 immutable `.63`、共享 `.64` authority 或引入第二状态。此修复须重新通过 Phase 2、提交和完整 Branch Review。

## Phase D443：Bind package major migration（generation 5，2026-09-25）

本轮从 `origin/main@81659a0d9437358061a6442616e3fc4aaa1872ab` 续接同一 #454 task identity，
通过现行 Reactivate owner 恢复到 generation 5，执行分支为 `codex/454-d443-bind-task-session`。
历史 C1-C7 和 #443 归档结论不是本轮的 package/check/review pass。

### 范围与 owner

- 迁移 canonical `trellis/skills/guru-team/packages/guru-bind-task-session/` 的 Skill、interface、
  public input/output schema、consumer projection、runtime、examples 和 package-local tests；保留五个成功 exit
  与 router ID，新增 `explicit_task_mode`，blocked 只输出 ReasonDTO。
- TaskLifecycleDTO 仅包含 `task_id + lifecycle_generation`（包括 generation 0）。TaskRef 由直接 consumer fresh
  派生；Bind 不持有 branch、checkout、resource ledger 或机器路径 authority。manual recovery 仅重建当前
  official schema-2 session pointer，不修复 task/workspace mappings。
- 使用 C5 official-backed session adapter 和 C2-C4 live identity/checkout/binding substrate；不得复制 Fixed Fork
  task/session store。#456 归档 reconcile 的 `443-*` rows 是迁移 inventory，#454 当前合同优先于旧 #443
  package 与 `.64` 中继承的旧 D443 描述。
- 本轮只形成 package-ready canonical candidate；#434/E434 独占 workflow routers、registry selector、active
  manifest、installed/platform publication 和旧 production edge retirement。D436 Reactivate/Completion/Closure/
  Finish/Cleanup 仍是下一实施单元；不修改 #434 dirty worktree 或业务仓库。

### 验证与交付门禁

1. 以实际 official session port 和真实 Git checkout fixture 验证 resume、rebind、switch、reactivate、
   pointer-only manual recovery、context-key 缺失的 explicit mode、generation 0、stale/mismatch zero-write。
2. 校验 schema/interface/exits/consumer/projection 闭包、canonical package 与 shared DTO 一致性，并检查
   target Bind package 没有 legacy mapping/path authority。运行相关 package/runtime tests、task validator、
   `git diff --check` 和 touched non-generated code 行数检查。
3. Docs/Architecture impact 按当前 package delta fresh 审查；只有独立 contribution 审核后才可串行提升 shared
   current。finding fix 后重跑 Phase 2、Task Commit 与完整 `origin/main...HEAD` Branch Review。
4. Publication 只可声明 D443 package-ready、非激活；PR 使用 `Refs #454`，不得 `Closes #454`。push、PR、
   merge、Finish 和 Cleanup 各由其正式 owner 验证真实前置。完整多平台 Release matrix 留给专门 Issue。

## Phase D436：terminal lifecycle package major migration（generation 6，2026-09-25）

### 当前身份与交付边界

同一 task `454-task-lifecycle-state-model` 经正式 Reactivate 从 generation 5 恢复到 generation 6；
目标 base 是 `main@0ac48e5d24e6d2c32cf2d69080109a6a7adaee9e`，工作分支为
`codex/454-d436-lifecycle-packages`。旧 task archive 和 D443 审查只证明历史切片，不证明本次 Phase 2。
本轮只交付五个已存在的 canonical package major 与 task-local/共享知识增量：
`guru-reactivate-task`、`guru-review-task-completion`、`guru-complete-task-closure`、
`guru-finish-task`、`guru-cleanup-task-resources`。#456 `436-*` 账本定义 replace/retire/retain，
#454 当前 PRD 和设计定义最终状态模型；#436 的历史 package 作为迁移输入。

### 实施顺序

1. 各 package 独立迁移 `SKILL.md`、interface、按 exit 封闭 schema/examples/consumer、runtime 与
   package-local tests。共享 DTO、Git common-dir ledger、session adapter、checkout/binding API 均作为 C2-C7
   唯一 substrate 使用；缺失能力先明确归属，不在 package 内建立第二套 store。
2. Reactivate 保留 stable TaskId 并建立下一 generation；Completion 汇总 scope/Delivery/evidence；Closure
   冻结并收敛 source action set；Finish 校验 Closure 和归档持久化后封存 ledger；Cleanup 仅按当前 seal
   删除 Guru-owned 资源，人工/跨机器 route 独立闭合。每个 producer output 与 consumer input 使用显式薄投影。
3. 定向运行五组 package tests、共享生命周期 runtime/contract、schema/interface/exits/consumer 校验；
   对正常 no-Issue、Issue source、Reactivate、旧 generation 失效、Closure 外部变化、Finish seal 与 Cleanup
   caller-owned 保留做组合回归。`git diff --check`、task validator、touched 非生成文件行数检查必须通过。
4. D436 的 Architecture 与 RDT contribution 先独立审核，串行提升 shared current；提升后的 diff 再 fresh
   执行 Phase 2、Task Commit 和完整 `origin/main...HEAD` Branch Review。finding fix 使此前 gate 失效。
5. Publication/Finalizer/Merge 只交付 D436 非激活 canonical package-ready slice。PR 仅 `Refs #454`，
   Issue 保持 Open；不得切换 workflow、registry selector、active manifest、installed/platform projection，
   不触碰 #434 dirty worktree、业务仓库或完整 Release matrix owner。

### 退出与未验证边界

成功退出要求五个 canonical package 自洽、target exits 均有唯一声明 consumer、定向/组合验证和完整
Branch Review通过，且 shared current 文档与当前 candidate 一致。E434/#434 将来独立负责一次性切图、
完整 package-ready gate、installed/platform/reapply 与生产激活；专门候选 Release matrix 不由本切片代跑。

### D436 提交后验证

- 当前候选 `01a7bba4914dbd739d43e1c3691e9c939299a3fb` 基于 `main@0ac48e5d24e6d2c32cf2d69080109a6a7adaee9e`；PR #474 仅引用 #454，Issue 仍开放。
- 五个 package、共享 lifecycle runtime 与 package integration 合跑：`pytest --import-mode=importlib` 226/226 通过；`git diff --check origin/main...HEAD` 通过。
- 本条记录是当前候选的验证事实，不代替 post-promotion Architecture/Phase 2、Task Commit、完整 Branch Review 或 Publication 的正式 typed exit；这些步骤仍须基于后续当前候选完成。

### D436 Branch Review finding-fix

- 完整范围的独立审查发现三个当前正常路径缺陷：合法 rename 后 Finish 错误地将可变目录名当作 TaskId；真实两父 merge 后 Reactivate 错比 target merge SHA 与 ledger 中的 bookkeeping PR head；缺失 ownership 时 Finish 的人工 Cleanup 结果无法在原 checkout 被删除后支撑 Reactivate。
- Finish 现在校验已解析的 TaskId；Reactivate 分别校验 bookkeeping commit 与 target merge 的祖先关系。人工终态在 Git common-dir 保存最小 Finish identity，Reactivate 只在匹配的人工 Cleanup `cleaned` receipt 存在时恢复；未完成 Finish 或单纯丢失 ledger 仍阻断。
- Finish/Reactivate 定向测试 39/39；后续补强为真实 linked worktree 与 branch 的成对人工 Cleanup，并验证只选在用 branch 仍被阻断。`29ccfef5` 候选的 Cleanup 15/15、Reactivate 19/19，五包、共享 lifecycle runtime 与 package integration 组合 231/231 通过，`git diff --check` 通过。旧候选的 230/230 不作为后续证据。
- 对 `origin/main...29ccfef5` 的新独立完整审查发现 normal Cleanup 输出丢失后同一 Finish seal 输入重试被 ledger revision 错误阻断。修复在现有 Git common-dir Cleanup owner 中保存以 TaskId/generation/Finish result/inventory 精确绑定的最小 `cleaned` receipt；同输入恢复同一输出，错误 inventory 仍阻断。新独立回归与五包、共享 lifecycle runtime、package integration 合跑 232/232。该 finding-fix 后仍须重新完成当前候选 Phase 2、Task Commit、完整 Branch Review、Publication 与 Finalizer，不能复用 `29ccfef5` 的 gate。
- 对 `origin/main...50ab858a` 的 fresh final review 发现 Closure canonical `commands.json` 仍公开可选 `--facts` 和已删除的 `schemas/live-facts.schema.json`，而 runtime 入口不接受该参数。正常调用者按声明执行会得到 `invalid_arguments`。本轮删除这两个过时声明，保持 Closure 自行读取 live Issue state，不恢复第二个 facts authority；package asset test 校验精确 flags 和全部 schema binding 的文件存在。Closure 定向 12/12、五包及共享 runtime/package integration 组合 232/232、source package validator（32 active packages、102 commands）、task validator 和 `git diff --check` 通过。本次修复仍须重建 fresh Phase 2、Task Commit、完整 Branch Review、Publication 和 Finalizer；E434/#434 激活与完整 Release matrix 未验证。
