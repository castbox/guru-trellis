# #454 Phase C 实施计划

## 1. 计划目标与停止边界

本计划只覆盖 #454 Phase C。交付目标是得到一组 package-ready、未激活的 lifecycle substrate 与 public owner
contracts，供 Phase D443、Phase D436 和 Phase E434 后续消费。

本 Planning 轮次只写 task-local 文档并完成 Phase 1 semantic approval。它不执行以下动作：

- 不运行 `task.py start`，`task.json.status` 保持 `planning`；
- 不修改生产代码、schema、workflow、registry、manifest、preset、overlay 或 platform projection；
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

Phase C 是本 task 的首个独立 Delivery slice。它只交付 substrate 与 package-ready canonical contracts；它不要求
Phase D443、Phase D436 或 Phase E434 已完成。

独立可交付条件：

- fixed Fork prerequisite已形成 exact reviewed commit并通过本计划列出的 Fork验证；
- Guru lifecycle kernel与common-dir stores通过 package/runtime tests；
- `guru-create-task`、`guru-establish-task-identity`、`guru-establish-task-branch-binding`、
  `guru-ensure-task-checkout`、`guru-rebind-task-branch`、`guru-activate-task` 具备完整 canonical package contract；
- shared DTO/schema 与每个 Phase C owner 的 input/output/consumer projection闭合；
- canonical package-ready bytes保持 inactive，不写 registry selector、active manifest、installed/platform projection
  或 workflow edge；
- old mappings与`guru-create-task-workspace`仍作为当前 production predecessor保留，但 Phase C 新代码零读取、
  零写入，退役由 Phase E434 activation transaction完成。

剩余工作 owner：Phase D443、Phase D436 与 Phase E434 各自任务。Phase C 不替这些 owner 迁移或激活。

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
- package-ready `guru-ensure-task-checkout` canonical package。

Behavior：实现 `adopt_invocation_checkout` 与 `provision_linked_worktree`；所有自动/人工target使用同一live
validator；path只存在call-local plan/transaction；repository-control operation使用common-dir facts且不依赖历史
checkout path。

Tests：primary/linked adopt、new/reuse provision、wrong repository、detached、base branch、dirty、HEAD drift、zero/
multiple candidate、worktree move、explicit target fresh revalidation、output loss recovery、zero mapping access。

Exit：`checkout_substrate_ready`。

Recovery：provision transaction按reviewed disposition记录Guru新建资源；失败只删除本transaction新建且身份仍匹配
的资源。caller-owned资源原字节保留。

### C4 Branch association、establishment 与 rebind substrate

Canonical package/runtime surfaces：

- `trellis/skills/guru-team/runtime/task_lifecycle/branch_store.py`；
- `trellis/skills/guru-team/runtime/task_lifecycle/branch_resolution.py`；
- `trellis/skills/guru-team/runtime/task_lifecycle/rebind.py`；
- common-dir branch association schemas；
- package-ready `guru-establish-task-branch-binding` 与 `guru-rebind-task-branch` canonical packages。

Behavior：store位于Git common-dir；key为TaskLifecycleKey；record只保存generation、revision与portable branch ref；
missing走establishment，conflict走invalid；rebind只实现same-checkout-new-ref与clean existing-target两条route；
不同历史返回named reconciliation stop。

Tests：revision 0初始化、strict increment、binding/ownership四象限恢复、unique/zero/multiple candidate、dirty
same-checkout字节保持、existing-target exact artifact、rollback、output loss recovery、reserved control ref rejection、
same ref resource incarnation exclusion。

Exit：`branch_substrate_ready`。

Recovery：mutation transaction保存exact pre-state；rollback恢复association与ledger revision。禁止stash、merge、rebase、
cherry-pick、reset或force push。

### C5 Path-free session store 与 resource ownership ledger

Canonical package/runtime surfaces：

- Fork提供的official common-dir session store由C1完成；Guru只新增session DTO adapter与consumer validators；
- `trellis/skills/guru-team/runtime/task_lifecycle/resource_ledger.py`；
- common-dir resource ledger schemas、Finish seal input primitives与Cleanup resolution primitives；
- package-ready `guru-establish-task-identity` 的legacy identity establishment contract。

Behavior：session payload严格为TaskLifecycleDTO；resource ledger按resource incarnation记录acquisition origin、ownership、
portable ref、revision、state与responsibility role；unknown ownership按caller-owned；ledger missing与conflict分开；
普通Cleanup只看到Guru-owned cleanup-pending set。

Tests：context key有/无、A->B->A、多session、generation invalidation、ledger五种acquisition projection、rebind retired
resource、active missing恢复为caller-owned、terminal missing进入manual selection、remote role、Finish seal inventory、
receipt ref retained-control排除。

Exit：`control_stores_ready`。

Recovery：session write失败不回滚已成立lifecycle；ledger mutation失败由同一transaction恢复。无法证明的历史ownership
不补写为Guru-owned。

### C6 Task creation 与 Phase C public owners

Canonical packages：

- `guru-create-task`；
- `guru-establish-task-identity`；
- `guru-establish-task-branch-binding`；
- `guru-ensure-task-checkout`；
- `guru-rebind-task-branch`；
- `guru-activate-task`。

每个package提供 `SKILL.md`、`interface.json`、commands、schemas、examples、consumers、runtime、scripts、tests与evals。
Create只消费reviewed `existing_issue | standalone_request`，不创建Issue；Activation独占
`planning -> in_progress`；同owner recovery不得重复mutation。

Package-ready boundary：

- canonical package与package-owned consumer schemas完成；
- registry继续保持predecessor selection，不增加integrated selector；
- extension active manifest不枚举新active graph；
- installed `.trellis/guru-team/**`、`.agents/.codex/.claude/.cursor`投影不发布新major；
- canonical workflow与dogfood workflow不增加production mandatory invocation。

Tests：workflow/standalone parity、entry preconditions、semantic gate先于recorder/executor、side-effect confirmation不持久化、
created/recovery/blocked exits、no-Issue、prebuilt/provision checkout、session explicit-task mode outcome、activation initial/
recovery、unique consumer、unknown/multiple exit fail closed、package tree completeness与3000-line gate。

Exit：`phase_c_packages_ready_inactive`。

Recovery：每个owner只恢复自己的transaction。output loss执行read-only rematerialization；不得重复创建task、branch、
worktree、binding或ledger entry。

### C7 Subtraction、Docs SSOT 与 Phase C validation

Retirement action在Phase C只建立zero-new-reader/zero-new-writer证明；production deletion留给Phase E434 atomic activation。

Validation set：

- Fork exact commit build、focused task/session/generated tests；
- lifecycle kernel、checkout、branch、session、ledger与六个package的unit/contract/eval tests；
- canonical package inventory与public I/O/consumer graph checks；
- source preparation、upstream ownership、dogfood overlay drift、recursive sidecar、managed Python routing；
- one representative clean throwaway，证明fixed Fork生成official primitives并安装Phase C canonical package-ready bytes；
- static search证明Phase C新代码对task/workspace mapping、`worktree_path`、`source_checkout`、legacy session path字段
  零读取零写入；
- touched non-generated file 3000-line report；
- task validator、format/lint/type checks与secret scan。

明确不运行完整多平台Release matrix；该证据仍归 #410。Phase C不把focused throwaway描述为Release Gate通过。

Exit：`phase_c_validated_inactive`。

## 5. Subtraction 与兼容策略

Direct evolution选择：replace + synchronized later retirement。

- Phase C新增target-native substrate，新代码不读写old mappings；
- predecessor `guru-create-task-workspace`、mapping runtime与旧session contract在Phase C保留为active production，
  只因Phase E尚未切图；
- Phase D迁移package major，但不翻active selector；
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
- `docs/architecture/**` 与 `docs/requirements-design-test-contributions/454-task-lifecycle-state-model/**`；
- `README.md`、canonical workflow/package README与preset README中的current source/ownership/migration说明。

这些shared路径只在实施/检查阶段修改。本Planning不直接修改shared current authority。

## 7. Final acceptance

Phase C通过条件：

1. P0、P1、C0、activation与C1至C7按顺序完成，每个boundary/slice满足entry、validation、exit与recovery合同；
2. fixed Fork exact commit是official task/session primitive唯一source，Guru diff中无`.trellis/scripts/**` patch；
3. lifecycle substrate与六个owner package-ready且inactive；
4. #456标为Phase D/E的33项不被Phase C越权实现或激活；
5. new substrate对old mappings零读取零写入，old production predecessor未被半切换；
6. shared DTO每个字段都有named direct consumer，每个exit有唯一consumer；
7. no-Issue、rename、move、session loss、binding/ledger loss、rebind与output-loss recovery具备deterministic tests；
8. current Architecture contribution完成独立Phase 2、Task Commit、full-diff Branch Review与promotion前置；
9. focused validation与Release matrix边界如实报告；
10. 所有touched non-generated code file不超过3000行，或在同一slice先完成reviewed split。

Phase C完成后仍禁止production activation。后续固定进入Phase D443，再进入Phase D436，最后由Phase E434 fresh
reconcile并执行atomic activation。
