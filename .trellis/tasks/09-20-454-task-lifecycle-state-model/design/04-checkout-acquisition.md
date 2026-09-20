# 04 预建 checkout 与 Guru provision 的双入口

## 1. 要解决的问题

Task lifecycle 必须同时接受两种真实入口：调用方在首个 prompt 前已经创建并进入 checkout，以及 Guru
在 task creation 或 Reactivate transaction 中创建 checkout。两种入口必须产生同一 task、branch、session
和 ownership 后置状态，不能继续通过 `workspace_mode` 建立两个领域模型。

## 2. 两个封闭 acquisition route

Checkout acquisition 只有以下两个 route：

```text
adopt_invocation_checkout
provision_linked_worktree
```

Route 是当前 Create/Reactivate transaction，以及 Rebind 的 existing-target route 的语义选择，不写入 task
metadata。Rebind 的 `same-checkout-new-ref` 不取得第二个 checkout，归问题 05 的 branch-ref mutation。Transaction
完成后，下游只看到统一的 current branch association、resource ledger 与 live checkout。

## 3. Adopt invocation checkout

### 3.1 Entry validation

采用当前 invocation checkout 前必须 fresh 验证：

1. checkout 是 Git 注册 worktree；
2. checkout 的 common dir 与当前 repository context 相同；
3. checkout 绑定 `refs/heads/*`，不是 detached HEAD；
4. checkout clean；
5. branch 不是 selected Delivery target branch；
6. branch 不被另一个 active TaskLifecycleKey 占用；
7. HEAD 等于当前 reviewed decision head；
8. repository identity、source authority 与 task creation/reactivation input 仍匹配；Reactivate携带
   `source_correction_ready`时，tracked current source必须匹配DTO的old source，new source只在Reactivate原子
   transaction内写入；
9. create 场景中不存在同 TaskId artifact；Reactivate 场景中 exact archived TaskId/generation 匹配。

路径只用于当前调用定位 checkout，不进入 output identity、task metadata、session binding 或 resource ledger。

### 3.2 Ownership

Adopt 不把既有资源改写为 Guru-owned：

| Invocation checkout 类型 | branch ownership | linked worktree ownership |
| --- | --- | --- |
| primary checkout | caller-owned | 不存在 linked-worktree resource |
| linked checkout | caller-owned | caller-owned |

Adopt 成功只建立 current association 和 caller-owned ledger projection，不创建第二个 worktree。

## 4. Provision linked worktree

Provision 根据 reviewed branch ref、decision head 与机器本地 `worktree_root` 执行。`worktree_root` 只属于
本机配置与当前副作用计划，不进入任何 task/session identity。

Provision 分为三个确定性事实组合：

| Live pre-state | 执行动作 | branch ownership | worktree ownership |
| --- | --- | --- | --- |
| branch 不存在，未注册 checkout | 从 decision head 创建 branch 与 linked worktree | Guru-owned | Guru-owned |
| branch 已存在且 HEAD 等于 decision head，未注册 checkout | 为 existing branch 创建 linked worktree | caller-owned | Guru-owned |
| branch 已在一个合格 registered checkout | 精确复用该 checkout | caller-owned | caller-owned |

以下状态不进入 provision mutation：

- existing branch HEAD 与 decision head 不一致；
- branch 已被另一 TaskLifecycleKey 占用；
- 同 branch 存在多个 registered checkout；
- target path 已存在但不是 exact registered checkout；
- checkout dirty、detached 或属于 foreign common dir；
- selected branch 等于 Delivery target branch。

这些状态进入共享 resolution/selection 协议，不通过 `--force` 覆盖。

## 5. Atomic transaction boundary

Checkout acquisition 不是独立 terminal domain object。它必须与 Create、Reactivate 或 Rebind 的 owner
transaction 原子闭合，原因是独立 acquisition 成功而 task mutation 失败会留下没有 lifecycle owner 的
Guru-owned branch/worktree。

固定 transaction 顺序：

1. 语义 owner 选择 route、branch ref 与 ownership projection；
2. mutation 前重新读取 decision head、branch、worktree topology 与 task identity；
3. 创建或采用 checkout；
4. 写入或移动 task artifact；
5. 建立 current branch association；
6. 写入 resource ledger；
7. 验证统一 post-state；
8. 尝试写入 session association；无 context key时进入 explicit-task mode，session write/verify失败时进入
   session-binding recovery；
9. 返回 lifecycle success 与唯一 session outcome：`session_bound`、`explicit_task_mode` 或
   `session_binding_recovery_required`。

步骤 3 至 7 任一步失败时：

- 删除本 transaction 新建且仍匹配 exact identity 的 Guru-owned worktree；
- 删除本 transaction 新建且仍匹配 exact identity 的 Guru-owned branch；
- 保留 caller-owned branch/worktree；
- 恢复原 task locator、branch association与ledger；步骤 3 前存在的 session binding保持原状；
- 若 exact rollback 无法证明，返回 recovery-required，并保留 transaction identity供同一 owner 恢复。

步骤 3 至 7 的统一 post-state 是 lifecycle commit boundary。Session 不是该 transaction 的 commit participant：

- context key缺失不回滚 lifecycle，返回 `explicit_task_mode`；
- context key存在但 session write/verify失败不回滚 lifecycle，返回
  `session_binding_recovery_required(TaskLifecycleKey)`；
- 该结果由 Session owner重试 exact pointer write，当前 invocation仍以 verified TaskLifecycleKey进入
  explicit-task mode；
- session recovery不得重复 Create、Reactivate、Rebind或acquisition mutation。

## 6. Create 与 Reactivate 的差异

两条 lifecycle 使用同一 acquisition contract，但各自 owner 不合并：

| 场景 | acquisition 前 identity | task artifact mutation |
| --- | --- | --- |
| Create | reviewed TaskId candidate + generation 0 | 首次创建 active task artifact |
| Reactivate | exact archived TaskId + generation g+1 | archive locator 移回 active locator并递增 generation |

`guru-create-task-workspace` 这一 public 概念在迁移后退出。Create owner 改为 task creation 语义，不再返回
workspace identity。Reactivate owner继续独立存在。二者与 Rebind 引用同一 checkout-acquisition contract 与
deterministic runtime primitive，不复制 route、validation 或 ownership 规则；acquisition 不单独暴露为会
留下 provisional resource 的 public Skill。

已有active TaskLifecycleKey且current branch association已成立时，zero-checkout recovery由独立
`guru-ensure-task-checkout`承接。该Skill调用同一acquisition primitive，但其transaction owner已经是现有
TaskLifecycleKey：它只采用或创建绑定current branch的checkout、写入对应worktree resource ledger并验证live
resolver success，不创建task、不修改branch association、不产生第二套acquisition规则。Multiple-checkout
topology repair也由该Skill在用户选定retain target与逐项确认repair action后完成。

## 7. Unified success state

无论采用哪条 route，成功后都必须满足：

- exact TaskLifecycleKey 已存在；
- 恰好一个 current branch association；
- branch association 不含 path 或 HEAD；
- resource ledger 对实际取得的 branch/worktree 各有一个 ownership record；
- execution checkout 可通过 live resolver 唯一解析；
- task artifact 位于该 checkout 且 identity/generation/status 匹配；
- session association 已建立，或明确进入当前调用的 explicit-task mode；
- task metadata 不含 `worktree_path`、`source_checkout`、workspace slug 或 decision head authority。

## 8. Failure matrix

| 状态 | 唯一结果 |
| --- | --- |
| 合格 primary invocation checkout | adopt，branch caller-owned |
| 合格 linked invocation checkout | adopt，branch/worktree caller-owned |
| branch 与 worktree 均不存在 | provision，两者 Guru-owned |
| existing branch 精确匹配，无 checkout | provision，branch caller-owned、worktree Guru-owned |
| existing registered checkout 精确匹配 | reuse，两者 caller-owned |
| invocation checkout dirty/detached/foreign | reject target，进入 selection-required |
| branch HEAD 与 decision head 不同 | stale decision，重新审查 |
| branch 被其它 task 占用 | branch conflict |
| session context key 缺失 | task lifecycle 成功，当前调用进入 explicit-task mode |
| session write/verify 失败 | task lifecycle 成功，返回 session-binding recovery，当前调用进入 explicit-task mode |
| mutation 失败且 Guru-created rollback 完成 | transaction failed，无残留 Guru-owned resource |
| mutation 失败且 exact rollback 未完成 | same-owner recovery required |

## 9. 当前设计结论

本问题固定以下结论，最终状态仍由全量审核决定：

1. route 只有 adopt invocation checkout 与 provision linked worktree；
2. 预存在的 branch/worktree 永远不因采用而变为 Guru-owned；
3. acquisition path 与 decision head 只存在于当前 transaction；
4. acquisition 与 owning lifecycle mutation在步骤 3 至 7 原子闭合，不产生 task workspace identity；
5. session context 缺失不再使已成功的 task creation 永久失败；
6. session write失败不回滚已提交 lifecycle，也不重复 lifecycle mutation；
7. `guru-create-task-workspace` 的 workspace 语义与 public id 在迁移中退出；
8. 已有active lifecycle的zero-checkout recovery由`guru-ensure-task-checkout`闭环承接。
