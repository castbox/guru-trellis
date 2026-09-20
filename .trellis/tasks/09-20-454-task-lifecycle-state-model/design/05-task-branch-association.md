# 05 Current Branch Association 与显式 Rebind

## 1. 要解决的问题

TaskId 不等于 branch，TaskRef 也不等于 branch。每个稳定active TaskLifecycleKey需要一个current branch，
供实现、review、Publication与Finish定位当前交付线。唯一例外是planned machine handoff已经released、
destination尚未consume的transaction state；该状态恰好零个current branch且只允许handoff owner继续。
该关系必须支持显式rebind，同时保留旧资源的ownership与Cleanup responsibility。

## 2. Current Branch Association

每个稳定active TaskLifecycleKey恰好拥有一条path-free association：

```text
CurrentBranchAssociation = {
  task_lifecycle_key,
  binding_epoch,
  binding_revision,
  branch_ref
}
```

固定合同：

- `branch_ref` 使用完整 local ref identity，例如 `refs/heads/codex/454-state-model`；
- `binding_epoch` 是 repository-local opaque identity，用于隔离 control state 完全丢失前后的 rebind history；
- 每个 epoch 的 `binding_revision` 从 0 开始，每次成功 rebind 加 1；
- resource ledger 中的 current set 必须匹配同一 epoch、revision 与 branch ref；
- association 不保存 checkout path、HEAD、base HEAD、remote-tracking SHA 或 session identity；
- association 存在于 ignored repository-local control state，不进入 tracked task metadata；
- 同 TaskLifecycleKey 不得同时存在两条 current association；
- association只有在未被TaskId稳定supersession receipt ref可达Git history中同一TaskLifecycleKey的较新
  machine-handoff receipt取代时
  才具备current资格；receipt中的source epoch/revision精确失效planned handoff源association，
  `unavailable_source` receipt失效该transaction之前的全部machine-local association；
- planned machine handoff已released、destination尚未consume时为唯一transaction exception：source association
  已标记`transferred_out`，全局resolution为`handoff_released`且零current；该状态只允许handoff recovery或
  destination consume；
- archived generation 不存在 current association。

TaskId、generation、TaskRef 与 branch ref 的 equality 分别验证，任一字段不能替代另一个字段。

## 3. Initial binding

Create 与 Reactivate transaction 在 checkout acquisition 后建立新 epoch 的 revision 0：

1. 验证 exact TaskLifecycleKey；
2. 验证 acquired branch ref；
3. 写入 branch/worktree resource instances 及 ownership；
4. 生成新 binding epoch，写入 revision 0 association；
5. 从 live Git 重新解析唯一 checkout；
6. 验证 checkout 中 task artifact 的 TaskId、generation 与 active status。

上述写入属于同一 owner transaction。缺失任一 post-condition 时不得返回 created/reactivated success。

## 4. Rebind entry contract

Rebind 只接受 active TaskLifecycleKey。两条 route 共享以下前置条件：

- 当前 association 唯一且可验证；
- current execution checkout 已唯一解析；
- target branch 不是 Delivery target branch；
- target branch 不属于保留的 `refs/heads/guru-task-lifecycle/*` control namespace；
- target branch 不被另一个 active TaskLifecycleKey 占用；
- target branch ref 不承担另一个 unresolved resource incarnation；
- 当前不存在 Finish transaction、Cleanup mutation、Reactivate transaction或其它 Git operation。

随后必须选择以下恰好一条 route。

### 4.1 `same_checkout_new_ref`

该 route 专门处理 planning/implementation 期间仍有 task artifact 或业务 working tree 的合法换 branch：

- target local branch ref 尚不存在，且没有 registered checkout绑定该 ref；
- current checkout 保持原 path、common dir与HEAD；
- mutation 使用同一 checkout 上的 branch create + switch；
- mutation 前封存 index tree identity与working tree byte/status identity；
- mutation 后二者必须 exact match，task artifact仍在同一 checkout且TaskLifecycleKey/status匹配；
- 不要求 current checkout clean，但 dirty内容不得包含未完成Git operation产生的中间状态；
- 新 local branch由本 transaction创建，记为Guru-owned；现有linked worktree未被创建，沿用原ownership。

该 route不移动working tree；它只把同一index/working tree从old ref关联到同一HEAD创建的新ref。任一 byte、
index entry、HEAD或path变化都使transaction失败并恢复old branch association。

### 4.2 `existing_target`

该 route 只在可验证 clean boundary执行：

- current checkout clean；
- target branch已存在，且target checkout通过acquisition contract；
- target checkout包含exact TaskId、generation与active task artifact；
- current HEAD是target HEAD的ancestor，包含equality；
- current workflow owner已确认target HEAD是当前accepted scope的合法接续点。

Rebind不把source commit或working tree复制到target。Target比current HEAD更前时，rebind后Planning approval、
Phase 2 check、Branch Review、closeout Publication、Delivery Review、Delivery Publication、Completion、Closure与
Finish eligibility全部失效，并从current
scope owner重新建立。Target不包含current HEAD、缺少task artifact或需要内容迁移时固定返回
`rebind_reconcile_required`；用户先完成独立reconcile，再重新发起rebind。

## 5. Rebind mutation

成功 rebind 使用以下固定顺序：

1. fresh 读取 current association、ledger、current HEAD 与 target live facts；
2. `same_checkout_new_ref` 在current checkout创建并切换新ref；`existing_target`取得target checkout；
3. 按route建立target resource incarnation：新ref为Guru-owned，既有target按pre-state投影ownership，复用的
   physical linked worktree沿用其既有ownership；
4. 把旧 current binding revision 下的 local branch与remote branch转为retired state；离开old branch的
   physical linked worktree转为`reassociated`并由new revision successor接续，不进入重复Cleanup；
5. 保持 binding epoch 不变，写入 revision `n + 1` association，唯一指向 target branch；
6. 验证旧 association 不再 current，target association 恰好一个；`same_checkout_new_ref`额外验证HEAD、
   index、working tree、path与task artifact不变；
7. 验证 session 重新解析时得到 target association；
8. 提交 ledger 与 association transaction；
9. 按问题10 evidence invalidation matrix使exact slots失效：`same_checkout_new_ref`保留Planning，
   `existing_target`使Planning stale；两条route均使base reconcile、Task Commit pair、Phase 2、Branch Review、
   closeout Publication、Delivery Review、Delivery Publication、Completion、Closure与Finish eligibility stale。

相同 branch ref、相同 resource set 与相同 revision intent 的请求返回 `already_bound`，不增加 revision。

## 6. 旧 resource incarnation 的收敛

旧资源按 ownership 进入固定状态：

| Ownership | Rebind 后状态 | Freshness responsibility |
| --- | --- | --- |
| caller-owned branch/worktree/remote branch | `preserved` | 无后续 HEAD freshness requirement |
| Guru-owned branch/worktree/remote branch | `cleanup_pending` | rebind 时封存 `expected_cleanup_head` |
| ownership unknown | `preserved_unknown`，按 caller-owned 处理 | 无后续 HEAD freshness requirement |
| 同一 physical worktree 被新 revision继续使用 | old instance=`reassociated`，new instance沿用ownership | 只由new instance承担current/Finish责任 |

`preserved`与`preserved_unknown`表示普通lifecycle不再修改、验证HEAD或删除该资源。资源后续被调用方提交、
移动、删除均不影响current task lifecycle；只有问题09定义的用户定向terminal manual cleanup能删除。

`cleanup_pending` 保留到当前 generation 的 Finish/Cleanup。其 local/remote branch ref在 cleanup
responsibility收敛前不能成为任何 task 的新 current delivery resource。

## 7. Same-ref reuse

同一 Git ref 的 reuse 使用以下封闭规则：

| 前一 resource state | 是否允许新绑定同 ref |
| --- | --- |
| `current` | 禁止 |
| `cleanup_pending` 且资源仍存在 | 禁止 |
| `cleanup_pending` 且 Cleanup 尚未确认 absent | 禁止 |
| `cleaned` 或 `already_absent` | 允许 |
| caller-owned `preserved` | 允许，但重新绑定时形成新的 caller-owned resource incarnation |
| `preserved_unknown` | 允许，但新 incarnation 仍按 caller-owned 建立 |

新的 resource incarnation 使用新的 resource id 与 binding revision。它不复用前一 incarnation 的 ownership、
expected head、Cleanup result 或 semantic evidence。

## 8. Missing association recovery

Association 丢失时按以下顺序恢复：

1. 验证 TaskLifecycleKey 为 active；
2. 读取同 key 的 resource ledger；
3. ledger 恰好存在一个 `current` resource set 时，以该 set 的 epoch、revision 与 branch重建 association，
   保持原 ownership；
4. ledger 不存在 current set 时，进入共享 candidate discovery/selection；
5. 用户选定 target 后执行完整 branch、task artifact、exclusivity 与 checkout validation；
6. ownership ledger 同时丢失时，生成新 binding epoch，从 revision 0 建立 association；所有 transaction
   前已存在资源按 caller-owned 建立；
7. 建立新 association 后重新验证 epoch、revision、branch 与 ledger current set 唯一匹配。

恢复前必须先读取TaskId稳定supersession receipt ref可达history中同一TaskLifecycleKey的最新machine-handoff
receipt。Local ledger即使
仍标记`current`，其epoch/revision已被receipt取代时也不得恢复；planned handoff转destination consume，
`unavailable_source` recovery转目标机器new epoch/rev0，旧机器后续只进入manual cleanup。

重复 association、两个 current resource set、branch exclusivity conflict 与 generation mismatch 不进入自动
恢复，固定返回 `branch_association_conflict`。

## 9. Failure rollback

Rebind 在提交步骤 8 前失败时必须恢复：

- 原 association 及原 revision；
- 原 binding epoch；
- 原 resource states 与 ownership；
- 原 session resolution；
- target transaction中新建 Guru-owned resource 的 absence；
- target 预存在 caller-owned resource 的原状。

`same_checkout_new_ref`回滚固定先在同一checkout切回old ref，再删除transaction新建target ref，并重新验证
HEAD、index、working tree、path与task artifact均等于mutation前identity。任一项无法证明时返回
`resume_rebind`，携带exact transaction identity供同一owner恢复，不继续另一rebind。

若 mutation 已提交但结果丢失，同一 owner通过 TaskLifecycleKey、binding epoch、expected old revision、
new revision 与 target branch ref 恢复 exact result。它不得再次增加 revision。无法证明 epoch 或 old/new
revision 时返回`resume_rebind`，不得同时保留两个 current branch。

## 10. 当前设计结论

本问题固定以下结论，最终状态仍由全量审核决定：

1. current branch association 是 path-free ignored control state；
2. 每个稳定active TaskLifecycleKey恰好一个current branch；handoff_released中间态恰好零个且禁止普通owner；
3. rebind 保持 TaskId、generation 与 binding epoch，只增加 binding revision；
4. dirty lifecycle使用same-checkout-new-ref并保持index/working tree bytes不变；existing-target只在clean、
   artifact-matching、content-compatible boundary执行；
5. rebind不承担reconcile、commit migration或working tree transfer；
6. old caller-owned resource 进入 preserved，old Guru-owned resource 进入 cleanup pending，复用的physical
   worktree通过reassociated successor避免重复Cleanup；
7. same-ref reuse 由前一 resource responsibility 是否收敛决定；
8. rebind failure 必须恢复 exact previous association 与 ownership state。
9. machine-handoff supersession receipt是跨机器判定旧association stale的portable freshness authority，不保存
   branch path、machine identity或session identity。

Binding epoch 不进入 tracked task metadata、session binding 或 public task identity。它只服务 association、
resource ledger 与同 owner transaction freshness。全部 local control state 丢失后新建 epoch，是在不猜测
历史 revision 的前提下拒绝旧 transaction 的唯一方式。
