# 09 Resource Ownership、Finish 与 Cleanup

## 1. 要解决的问题

Branch、linked worktree 与 remote branch 的删除资格取决于资源取得时的 owner，不取决于当前 path、name、
task branch、Finish branch 或用户后来选中该资源。Branch rebind 又会在同一 generation 内留下多个历史
resource incarnation。Resource ownership 必须成为独立 ledger，并由 Finish 封存、Cleanup 消费。

## 2. Resource ledger authority

Ledger 是 ignored repository-local control state，按 TaskLifecycleKey 分区。它不进入 tracked task metadata，
不保存绝对 path。每个 resource instance 使用独立 `resource_id` 与 `binding_revision`。

### 2.1 Local branch resource

```text
LocalBranchResource = {
  resource_id,
  task_lifecycle_key,
  binding_epoch,
  binding_revision,
  branch_ref,
  ownership,
  state,
  responsibility_role,
  expected_cleanup_head
}
```

`branch_ref` 是完整 `refs/heads/*`。`expected_cleanup_head` 只在 Guru-owned resource 进入 cleanup-pending 时
封存；caller-owned record 不承担 HEAD freshness。

### 2.2 Linked worktree resource

```text
LinkedWorktreeResource = {
  resource_id,
  task_lifecycle_key,
  binding_epoch,
  binding_revision,
  branch_ref,
  ownership,
  state,
  expected_cleanup_head
}
```

Ledger 不保存 worktree path。Live worktree 由 common dir、branch ref、TaskLifecycleKey 与 expected head 解析。
同 branch 出现多个 registered worktree 时进入 topology conflict。

Primary checkout 不建立 linked-worktree resource。

### 2.3 Remote branch resource

```text
RemoteBranchResource = {
  resource_id,
  task_lifecycle_key,
  binding_epoch,
  binding_revision,
  remote_repository_ref,
  branch_ref,
  ownership,
  state,
  expected_cleanup_head
}
```

Remote identity 使用 portable repository ref + `refs/heads/*`。Local remote alias 只用于当前调用解析 endpoint，
不成为 resource identity。

Handoff转移remote responsibility时必须同时保留原`binding_epoch`、`binding_revision`、`state`与
`responsibility_role`。`responsibility_role`只有`current_delivery`、`historical_cleanup`与`checkpoint_transport`；
它决定destination导入后是否建立current successor，不得从branch name或resource排序推断。

### 2.4 Supersession receipt ref

Machine transfer使用独立portable control ref。Canonical ref固定为
`refs/heads/guru-task-lifecycle/<TaskId>`；TaskId格式与repository-local case-fold uniqueness保证ref可构造且唯一：

```text
SupersessionReceiptRef = {
  task_id,
  remote_repository_ref,
  receipt_ref,
  state: retained_control
}
```

该ref按TaskId稳定，history中的每个record绑定exact TaskLifecycleKey与handoff id，并承载prepared、released、
consumed与artifact-deletion commit。它不是Delivery remote
resource，不参与current branch association，不进入Finish inventory或Normal Cleanup。首次建立与后续更新只由
`guru-transfer-task-machine`执行；已存在ref必须fresh验证其history属于同repository与TaskId，否则transfer阻塞。
`refs/heads/guru-task-lifecycle/*`是保留control namespace，任何Create、Reactivate、Ensure Checkout、Rebind、
Delivery target或missing-association candidate validator都必须拒绝该namespace。

## 3. Ownership establishment

Ownership 只在 resource instance 首次取得时写入：

| Pre-state 与动作 | Ownership |
| --- | --- |
| Guru 创建 local branch | Guru-owned |
| Guru 创建 linked worktree | Guru-owned |
| Guru 首次创建 remote branch | Guru-owned |
| mutation 前已存在的 branch/worktree/remote branch | caller-owned |
| historical ownership 无法证明 | caller-owned for normal Cleanup |

Rebind、session switch、checkout move、rename、Finish 与用户选择均不得改变 ownership。

## 4. Resource states

每个 instance 只处于以下一个状态：

| State | 含义 |
| --- | --- |
| `current` | 当前 branch association 正在使用 |
| `portable_auxiliary` | active generation使用的checkpoint transport remote resource，不属于current branch association |
| `preserved` | caller-owned，已退出 current，Guru 不再管理 |
| `preserved_unknown` | ownership 丢失，按 caller-owned 保守处理 |
| `reassociated` | 同一physical resource已由后续binding revision接续；old instance不再承担current或Cleanup责任 |
| `handoff_cleanup_pending` | planned machine handoff后由source-machine handoff Cleanup独立处理 |
| `transferred_out` | portable remote responsibility已封存在released handoff artifact，不再由source ledger处理 |
| `retained_control` | supersession receipt ref长期保持可达，不进入task resource Cleanup |
| `cleanup_pending` | Guru-owned，已封存 expected cleanup identity |
| `cleaned` | Cleanup 已删除 exact resource |
| `already_absent` | Cleanup 验证 exact resource 已不存在 |
| `manual_deleted` | terminal manual cleanup 已删除用户本次指定 resource |
| `cleanup_conflict` | live identity/freshness 不匹配，等待修复或 manual route |

Caller-owned resource 从 `current` 退出后直接进入 `preserved`。Guru-owned resource 在 rebind 或 Finish 时进入
`cleanup_pending`。`portable_auxiliary`在active generation保持独立责任；Finish时Guru-owned转`cleanup_pending`，
caller-owned转`preserved`。

`reassociated`只用于同一physical linked worktree被后续binding revision继续使用。Old instance保存
`successor_resource_id`，new instance沿用原ownership并成为唯一current worktree record；old instance不得再次
进入Finish或Cleanup candidate set。

## 5. Remote write 与 remote resource

本模型只有以下三个owner能写remote ref：

- `guru-checkpoint-task-state`写exact checkpoint transport ref；
- `guru-publish-task-delivery`写exact Delivery remote ref；
- `guru-transfer-task-machine`写exact TaskId supersession receipt ref。

Checkpoint与Publication在第一次操作exact remote branch前读取live remote并使用同一ownership合同：

- remote branch 不存在且owner创建成功：新增 Guru-owned remote resource；
- remote branch 已存在且被当前 task合法采用：新增 caller-owned remote resource；
- remote branch identity 与当前owner的checkpoint或Publication contract不匹配：mutation block，不写 ledger；
- 后续 push 只更新同 resource instance 的 live HEAD，不改变 ownership。

Checkpoint transport resource建立后固定使用`responsibility_role=checkpoint_transport`与
`state=portable_auxiliary`。Publication delivery remote使用`responsibility_role=current_delivery`；rebind退役的
remote responsibility使用`responsibility_role=historical_cleanup`。

Checkpoint与Publication均不得把local branch或linked worktree ownership投影为remote ownership。Checkpoint
remote ref只证明task artifact portability，不形成PR、Delivery、Completion或Publication semantic result。

Machine transfer不得写checkpoint或Delivery ref。它只在已审查handoff transaction内创建或fast-forward
supersession receipt ref；该ref固定为`retained_control`，不使用Guru-owned/caller-owned删除资格，也不因Finish、
Cleanup或Reactivate退出可达history。

Remote ownership只回答terminal deletion资格，不回答Publication write authority。采用caller-owned remote
branch后，Publication仍必须通过当前scope、reviewed content、PR/remote identity与用户已确认副作用计划取得
push/update authority；通过后允许更新该remote ref，但Finish时该resource进入`preserved`，Normal Cleanup不
删除。缺少Publication authority时停止push，不得以Guru不负责Cleanup为由推导可写。

## 6. Finish

Finish 是当前 generation resource inventory 的 sealing owner，不执行删除。它固定执行：

1. 验证 current TaskLifecycleKey、Closure result 与 active status；
2. 按问题02对Closure完整action set执行live freshness validation；失败时不开始Finish并返回Closure owner；
3. 验证 ledger 中恰好一个 current resource set；
4. 把 current Guru-owned branch/worktree/remote resource 转为 `cleanup_pending`；
5. 为每个 Guru-owned pending resource读取并封存 exact current HEAD；
6. 把 current caller-owned resource 转为 `preserved`；
7. 只检查当前机器ledger中仍属于该generation Finish inventory的历史binding revision；这些resource必须已
   处于preserved、cleanup-pending或terminal state；`handoff_cleanup_pending` source-local inventory与
   `transferred_out` responsibility由machine handoff owner排除，`retained_control` receipt ref永久排除，不得重新
   纳入destination Finish；
8. 封存 generation resource inventory identity；
9. archive task artifact并形成 Finish result；
10. 关闭 current branch association；
11. 使该 generation 的 session binding 在下一次读取时失效。

Finish success 不要求 Cleanup 已执行。Ledger 缺失或存在两个 current set 时 Finish 不猜测 ownership，返回
resource inventory recovery。

Finish以exact transaction identity跨越archive move、inventory seal与terminal result projection。Archive move
成功但seal/result尚未完成时保持`finish_in_progress`，只由同一Finish owner继续；archive、seal与tracked
terminal projection全部存在但返回值丢失时，owner重读三者并rematerialize同一result，不创建第二个Finish。
Seal丢失且ownership无法恢复时，Finish仍完成tracked terminal projection并把CleanupState固定为
`manual_required`；它不重造Guru ownership，也不把archive presence单独当作Finish success。

## 7. Cleanup

### 7.1 Entry

Normal Cleanup 只消费：

- exact TaskLifecycleKey；
- sealed Finish result identity；
- 同 generation 的 sealed resource inventory；
- live Git/GitHub facts。

Public Finish -> Cleanup handoff 不携带 absolute path 或 caller-authored resource list。Cleanup 从 ledger 读取
全部 `cleanup_pending` Guru-owned instances。

### 7.2 Resolution and order

Cleanup 对每个 resource fresh 解析，固定顺序如下：

1. linked worktree；
2. local branch；
3. remote branch；
4. 对应 remote-tracking ref。

Remote-tracking ref 是 remote branch cleanup 的派生本地 residue，不是独立 ownership authority。

一个 resource conflict 只阻断该 resource 及其依赖项。其它独立 resource 继续收敛。Local branch 只有在同
resource incarnation 的 linked worktree 已 cleaned/already-absent 后才删除。

### 7.3 Per-resource result

| Live result | Normal Cleanup 行为 |
| --- | --- |
| exact Guru-owned resource 存在且 HEAD匹配 | 删除并记 `cleaned` |
| exact resource 已不存在 | 记 `already_absent` |
| HEAD 不匹配 | 记 `cleanup_conflict`，不删除 |
| branch 被 checkout/in use | 记 `cleanup_conflict`，不删除 |
| worktree dirty | 记 `cleanup_conflict`，不删除 |
| repository/remote identity 不匹配 | 记 `cleanup_conflict`，不删除 |
| caller-owned/preserved | 不进入 Normal Cleanup candidate set |
| retained_control receipt ref | 不进入任何task Normal Cleanup candidate set |
| ownership record缺失 | 不推断，进入 terminal manual cleanup discovery |

Cleanup 完成后形成 generation-specific result。Partial Cleanup 保留未收敛 item，重复调用对 cleaned 与
already-absent item 幂等。

## 8. Runtime-loss recovery

### 8.1 Active lifecycle ledger loss

Active generation 的 ledger 丢失时：

1. 保留已验证 TaskId、generation 与 current branch candidate；
2. 重新发现当前 existing branch/worktree/remote resources；
3. branch association仍存在时沿用其 binding epoch/revision；association 同时丢失时建立新 epoch/revision 0；
4. 所有 transaction 前已存在资源按 caller-owned 建立；
5. 不重造历史 Guru ownership；
6. 旧 orphan resources 只在 terminal manual cleanup 中处理。

该恢复保证 Normal Cleanup 不会误删调用方资源，代价是失去自动删除资格。

### 8.2 Terminal ledger loss

Archived generation 的 sealed inventory 丢失时，Finish result仍保持 terminal，Normal Cleanup 不运行。系统
进入 manual cleanup discovery，不从 task branch、archive summary、path naming 或 remote branch name 重造
ownership。

## 9. Manual terminal cleanup

Manual cleanup 是独立 user-directed deletion route，不是 Normal Cleanup fallback。固定流程：

1. 用户声明 manual cleanup intent；
2. resolver展示当前 live resource candidates 与 portable identity；
3. 用户逐项选择 exact target；
4. owner对每项执行repository identity、exact ref/resource identity、path registration、dirty/in-use与active
   current-resource exclusion validation；
5. 展示 exact deletion plan；
6. 在当前对话取得独立确认；
7. 只删除 confirmed targets；
8. 记录 `manual_deleted` result；
9. 不修改历史 ownership 为 Guru-owned。

Manual cleanup不要求重新证明已经丢失的历史Guru ownership或历史TaskLifecycleKey归属。删除资格只来自当前
用户exact selection、live resource identity、资源不是任何active task的current resource，以及独立确认。
未选资源保持不变。Dirty worktree、identity mismatch 与 active task current resource 不进入删除。

## 10. Finish、Cleanup 与 Reactivate

- Finish sealed 后 Reactivate 才具备资格；
- Cleanup completion 不是 Reactivate 前置条件；
- 新 generation 不得采用旧 generation `cleanup_pending` 的同一 ref；
- 旧 generation Cleanup 能在 Reactivate 后继续，且只处理旧 ledger；
- 新 generation Finish/Cleanup 不读取旧 generation receipt；
- manual cleanup 必须验证 target 不是任何 current TaskLifecycleKey 的 current resource。

## 11. Cross-machine responsibility transfer

计划内active handoff不复制machine-local ledger。`guru-transfer-task-machine`固定执行：

1. 验证portable task checkpoint、current TaskLifecycleKey与唯一source association；
2. 要求source working tree不存在未同步内容；
3. 创建或验证TaskId稳定的supersession receipt ref，并在该ref写入`machine-handoff.json`的`prepared`状态；
   destination不得消费prepared handoff；
4. source caller-owned local resource进入`preserved`；
5. source Guru-owned linked worktree/local branch进入`handoff_cleanup_pending`，封存独立source-machine
   handoff Cleanup inventory，不再进入该generation后续Finish inventory；
6. source ledger中全部未收敛portable remote resource进入`transferred_out`；
7. 关闭source association并使source session stale；
8. 把`machine-handoff.json`更新为`released`并同步；artifact只包含handoff id、mode、TaskLifecycleKey、source
   binding epoch/revision、current branch ref、checkpoint commit/ref、supersession receipt ref，以及按resource id排序的全部未收敛
   portable remote resource repository/ref/ownership、原binding epoch/revision、原state、responsibility role与head
   rule；不含local path或machine identity；receipt ref当前expected head由released commit identity提供，不在artifact
   内自引用；其它remote resource记录release时fresh expected head；
9. source invocation返回`source_released`，唯一consumer运行`machine_handoff_cleanup`；cleanup完成或保留
   source-local pending result后，流程停止并等待destination从receipt ref独立consume；
10. destination消费released artifact，以checkpoint commit为content identity，并在artifact声明的current branch ref
   上按实际create/reuse facts建立local branch/worktree resource与new epoch/rev0 association；current branch ref不得从
   checkpoint ref、remote resource role、branch naming或candidate排序推导。完整portable remote responsibility set按原
   ownership导入ledger：一个`current_delivery` record建立new epoch/rev0 successor并保留predecessor resource id；
   `historical_cleanup`保留原epoch/revision与cleanup state，`checkpoint_transport`保留`portable_auxiliary` state，
   不得变成current。零个`current_delivery`是尚未Publication的合法状态，destination仍按current branch ref与
   checkpoint commit建立association；多个`current_delivery`固定为handoff conflict；
11. destination验证唯一current association后把artifact更新为`consumed`，增加destination binding
    epoch/revision并同步；
12. 再删除consumed artifact并同步；released、consumed与deletion commits必须保持在supersession receipt ref可达
    history中，共同形成portable supersession receipt；只有删除完成且history receipt可解析才返回handoff success；
13. `guru-cleanup-task-resources:machine_handoff_cleanup`独立删除source
    `handoff_cleanup_pending` resource；失败只保留source-local handoff cleanup result，不阻断destination
    lifecycle。

Prepared、released、consumed任一结果丢失均由同一handoff id恢复，不创建第二个handoff。Prepared只允许
source recovery；source在prepared后不可用时，用户明确选择unavailable-source recovery后，由destination以
同一handoff id转换为`mode=unavailable_source`的released recovery artifact，prepared snapshot不转移任何
ownership。Released只允许destination consume，consumed只允许artifact deletion recovery。

源机器不可用且不存在prepared artifact时，Destination在建立association前创建或验证TaskId稳定的supersession
receipt ref，并在该ref同步`mode=unavailable_source`的released recovery artifact；它携带TaskLifecycleKey、checkpoint/ref和“失效本
transaction之前全部machine-local association”的supersession rule，不携带或重造source ownership。
Destination随后把全部pre-existing resource记为caller-owned，本次新建local resource仍按实际create facts
记为Guru-owned，建立new epoch/rev0，再按步骤11-12形成consumed/deletion history receipt。Source orphan
resource不进入destination Normal Cleanup，只在源机器恢复后进入manual cleanup；源机器旧association即使
仍存在本地文件，也因portable receipt而不是current。

## 12. 当前设计结论

本问题固定以下结论，最终状态仍由全量审核决定：

1. ownership ledger 按 TaskLifecycleKey、binding epoch、revision 与 resource incarnation 归属；
2. ledger 不保存 absolute path；
3. unknown ownership 在 Normal Cleanup 中固定按 caller-owned；
4. Finish 只 seal inventory 与 archive，不删除 resource；
5. Cleanup 只删除 exact Guru-owned cleanup-pending resource；
6. rebind 历史 resource 全部保留到 preserved 或 cleanup terminal state；
7. terminal ownership loss 只进入独立 manual cleanup；
8. manual cleanup不以无法证明的历史task relation重新制造fail-close；
9. planned machine handoff转移全部未收敛portable remote responsibility，source local Guru resource转入独立handoff Cleanup；
10. unavailable-source recovery不重造source ownership；
11. handoff保留每个remote incarnation的原binding/state/role，只有唯一current role建立destination successor；
12. supersession receipt ref是长期保留的portable control authority，Finish与Cleanup均不得删除；
13. Reactivate 不阻止旧 generation Cleanup，但禁止复用其 unresolved ref。
