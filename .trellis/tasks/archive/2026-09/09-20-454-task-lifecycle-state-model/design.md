# #454 详细设计导航

## 设计方法

本文件只维护问题顺序、依赖关系与收敛状态。每个核心问题使用独立设计文件，完成当前问题的反例审查
后才进入下一个问题。任何单项设计通过都不代表整体模型已经成立；最终必须由组合状态矩阵证明全部
设计能够同时成立。

状态定义：

- `未开始`：尚未形成设计结论；
- `草案`：已有具体设计，但尚未完成当前问题审查；
- `单项收敛`：当前问题的状态、失败行为和迁移边界已经闭合；
- `组合验证`：该设计已进入全量状态矩阵，且未与其他设计冲突。

## 问题序列

| 顺序 | 问题 | 独立设计文件 | 当前状态 | 完成条件 |
| --- | --- | --- | --- | --- |
| 01 | 稳定 Task Identity 与可变 Task Locator | `design/01-stable-task-identity.md` | 组合验证 | create、rename、archive、Reactivate、legacy establishment 和唯一性无歧义。 |
| 02 | Task Source、Accepted Scope、Delivery Target 与 Closure 分离 | `design/02-task-authority-relations.md` | 组合验证 | source、scope、target 与 closure 各有唯一 owner。 |
| 03 | Lifecycle Incarnation 与 terminal result 隔离 | `design/03-lifecycle-incarnation.md` | 组合验证 | Reactivate 不复用旧 session、Finish 或 Cleanup authority。 |
| 04 | 预建 checkout 与 Guru provision 的双入口 | `design/04-checkout-acquisition.md` | 组合验证 | 两种入口产生同一 task state，ownership 投影唯一。 |
| 05 | Current Branch Association 与显式 rebind | `design/05-task-branch-association.md` | 组合验证 | 任一时刻恰好一个 current branch，历史 resource 不冲突。 |
| 06 | Live Execution Checkout Resolution | `design/06-live-checkout-resolution.md` | 组合验证 | move、跨机器、零/多 checkout 均有唯一结果或恢复入口。 |
| 07 | 自动推导、候选选择与显式指定 | `design/07-resolution-and-selection.md` | 组合验证 | 自动和人工 target 使用同一验证合同，不发生错误推导或永久 fail close。 |
| 08 | Path-free Session Association | `design/08-session-association.md` | 组合验证 | resume、跨 session、A→B→A 与 binding loss 均不串线。 |
| 09 | Resource Ownership、Finish 与 Cleanup | `design/09-resource-ownership-cleanup.md` | 组合验证 | caller-owned 保留、Guru-owned 可清理、unknown ownership 可人工处置。 |
| 10 | 统一状态矩阵与迁移切换 | `design/10-composition-and-migration.md` | 组合验证 | 全部 reachable state 有唯一 owner、route 或 terminal stop，旧 mappings 退出。 |
| 11 | Public Skill I/O 与迁移闭包 | `design/11-public-contract-migration.md` | 组合验证 | 全部新增与实质变化 owner 具有完整 exit、minimal output、唯一 consumer 与旧 identity 处置。 |

## 整体可行性结论

问题01至11已分别完成单项审查，并通过`design/12-final-consistency-review.md`对16个lifecycle scenario、
22条acceptance criteria、33条reachability constraint、11个evidence slot、8组active runtime-loss组合、
forbidden states与public owner completeness执行联合复核。60个finding已全部回写owning design。当前结论是在PRD声明边界内整体
设计可实现，不存在已知矛盾、冲突或缺漏。

该结论证明整体设计可进入实施，但不代表全部实现、测试、业务 repository 安装或 production cutover 已完成。
本 task 已完成正式 Phase 1 planning/approval/activation 并处于 `in_progress`；每个实施切片仍须分别完成 fresh
Architecture、Phase 2、Task Commit 与 Branch Review，且不得把局部 candidate 解释为后续切片或 production
cutover 已完成。

## 跨任务实施顺序与依赖边界

本 task 的设计定稿不是 #434 production graph 的激活授权。涉及 #443、#436、#434 的后续工作必须严格按以下
顺序执行：

1. 先完成 #454 substrate design 与 migration contract 的定稿；本 task在此阶段只定义共同 lifecycle substrate、
   public contract、迁移边界和 activation gate，不接管 #443、#436 或 #434 的 semantic owner。
2. 对 #443、#436、#434 做 contract reconcile。reconcile 只更新当前 package、schema、projection、workflow
   consumer 和规划合同对 #454 新接口的承接；不提前激活 #434，也不把旧设计中的 `workspace`、旧 session payload、
   旧 Reactivate exits 或重复 resource ledger 保留为生产语义。
3. 实现 #454 substrate，包括 stable identity、generation、checkout acquisition/resolution、branch association
   与 rebind、path-free session、resource ownership ledger、Finish/Cleanup 边界以及统一 public I/O。
4. 在 #454 substrate 可被消费后，迁移受影响的 #443、#436 及其它 package 的代码、schema、projection、workflow
   route 和 installer/overlay 引用。迁移必须以 #454 contract 为唯一共同 substrate，不复制一份 identity、session、
   checkout、ledger 或 Reactivate 实现。
5. 重新 reconcile #434，使其只消费已迁移的 #443/#436 contract 与 #454 substrate；随后才实现并激活 #434 的
   Delivery、Completion、Closure、Finish、Cleanup production graph。

上述顺序禁止反向执行。特别是，不能先实现或激活 #434 再回头实现 #454；否则 #434 会把旧 workspace、session、
Reactivate 和 resource ownership 假设固化到 production graph，形成必须返工的第二套 authority。

历史 #443、#436 task 文档、旧 Issue evidence 和已经形成的历史审查结论保持 immutable。新 contract reconcile、
package migration 和实现差异必须由当前 package 的迁移记录或新的 migration task 承接，不通过回改历史 task 文档
制造“历史上已经符合新 contract”的假象。

## Phase C 实施边界收敛

Phase C planning 绑定以下 current authority：

- live Issue `castbox/guru-trellis#454`，2026-09-21 fresh reread；
- `#454@b695adc928c2064bd27f07e2bb3bbbd034540571` 的 PRD 与 12 份 owning design；
- `origin/main@b4b42b49592d7bbc41caf8c0318056a0adcf6f72` 中已归档的 #456 四份 reconcile 文档；
- current Architecture Baseline `current-main-0.6.17-guru.58`、Design Constitution
  `guru-trellis-design-constitution-v1` 与 change contract
  `guru-trellis-architecture-change-contract-v1`；
- fixed Fork source `castbox/Trellis@43fffc170927c85d9f7fc106cc5a059e80d4530b`。

当前 task branch HEAD 为 `b695adc928c2064bd27f07e2bb3bbbd034540571`，与
`origin/main@b4b42b49592d7bbc41caf8c0318056a0adcf6f72` 的 merge-base 为
`361da96327824503ffb4fb4189291b3b9b4e23ae`。Current production workflow 对该 pair 的顺序固定为：

1. 当前 session 必须先由现有正式 session owner 绑定到 exact planning task；session 缺失时唯一合法路径是调用当前正式
   rebind/recovery owner。其 entry preconditions 不满足时 fail closed，不从 task inventory、旧 session record、
   mapping、branch name 或未来 Phase C package 推断绑定；
2. fresh Planning approval 的 task-local bytes 必须先形成 exact committed task HEAD。该 planning checkpoint commit
   需要独立展示精确文件、命令与零远端副作用并取得当前对话确认；它不是 implementation activation；
3. approved DTO 以 `resume_target=task_activation` 进入 post-plan pair guard；`new_pair` 在 task 仍为 `planning` 时
   调用 `guru-reconcile-task-base`，完成 temporary candidate、semantic review 与 exact local merge confirmation；
4. `reconciled` 返回 task activation router 后，才调用正式 activation owner完成 `planning -> in_progress`；
5. activation checked result进入Phase 2后，C1才可开始生产编辑。

当前执行入口不得通过直接调用 `set_active_task`、复制旧 session record、补写 legacy mapping/base metadata、直接调用
upstream `task.py start`、伪造 output-loss recovery 或绕过 `start-task.sh` 来修复 session。正式 session owner无法证明
当前绑定时，本task保持 `planning` 并返回 Planning blocker。完成 C0 semantic review 与用户对 exact Git mutation 的确认
前，禁止修改Phase C生产文件。

### Framework 与 extension ownership

`.trellis/scripts/common/task_store.py`、`active_task.py`、`session_storage.py`、`task_utils.py` 与
`.trellis/scripts/task.py` 是 fixed Fork 生成并拥有的 framework surface。Guru ownership inventory 不声明
`.trellis/scripts/**`，因此 Phase C 禁止通过 preset overlay、dogfood patch、安装后改写或 Guru package 内复制
第二套 task/session store 来满足需求。

Phase C 使用两个串行 owner boundary：

1. `castbox/Trellis` Fork prerequisite：从 fresh verified Fork base 修改 official task/session primitives，使
   immutable TaskId、rename/archive locator、path-free session payload 与 common-dir store 成为 framework
   capability；该工作必须在 Fork repository 的独立 Issue/task/branch 中完成，当前 Planning 不虚构其 Issue id、
   branch 或 candidate commit。
2. `castbox/guru-trellis` substrate：只在 Guru-owned canonical package/runtime/schema/docs/test surface 实现
   branch association、checkout acquisition/resolution、resource ledger、shared DTO 与 Phase C public owner
   packages，并把 source lock 更新到通过 Fork build/test 的 exact candidate。Phase C 不修改 active registry
   selector、extension active manifest、installed/platform bytes或 production workflow edge。

Fork prerequisite 未形成 exact reviewed commit，或该 commit 未通过 Fork build、task/session focused tests 与
Guru source preparation validation时，Guru substrate 的 framework-dependent slices 保持 blocked。该阻塞不得
通过兼容 alias、dual-read、dual-write、旧 mapping fallback 或复制 official Python 模块规避。

### Phase ownership

- Phase C：lifecycle kernel、TaskId/TaskRef/generation normalization、checkout acquisition/resolution、branch
  association/establishment/rebind substrate、path-free common-dir session storage、common-dir resource ledger、
  task creation、shared DTO/schema primitives、planned stable IDs 与 E434 所需的 activation inputs；`planned`
  registry row 不拥有 canonical package tree。
- Phase D0：在D443/D436前迁移Reconcile、Task Commit与Branch Review的stage-evidence承接。Pre-review compatible
  reconcile创建expected-head-bound本地merge commit；post_check/post_commit固定回fresh Phase 2；bounded continuity
  只承接已有prior full Branch Review。该阶段不建立durable `base_head` authority。
- Phase D443：`guru-bind-task-session` major migration及其五个保留 success exits、`explicit_task_mode`、schema、
  runtime 与 package-owned source projections。
- Phase D436：Reactivate、Completion、Closure、Finish、Cleanup major migration；Phase C 只提供它们消费的
  substrate和DTO，不改这些 package 的 active major contract。
- Phase E434：fresh reconcile 后为 planned IDs 交付完整 canonical packages，并一次性切换 workflow、registry
  selectors、active manifest、installed/platform bytes与旧 edge retirement；Phase C 与 Phase D 均不得提前创建
  planned package tree 或激活。

具体文件、切片、测试、entry/exit criteria 与 rollback boundary 以 `implement.md`、
`planning/phase-c-surface-inventory.md` 和 `planning/phase-c-migration-retirement-ledger.md` 为 Phase C 实施计划
SSOT。
