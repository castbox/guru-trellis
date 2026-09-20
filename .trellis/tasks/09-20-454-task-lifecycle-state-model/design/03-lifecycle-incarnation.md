# 03 Lifecycle Incarnation 与 terminal result 隔离

## 1. 要解决的问题

同一 TaskId 会经历初次 active lifecycle 和零次或多次 Reactivate。若 session、branch、Finish、Cleanup
只按 TaskId 归属，旧 archived lifecycle 的控制状态就会驱动新一轮工作。Lifecycle Incarnation 必须成为
所有 generation-sensitive state 的共同 discriminator。

## 2. Canonical generation

Tracked `task.json.lifecycle_generation` 是当前 generation authority，固定合同如下：

- 新建 task 写入整数 `0`；
- legacy task 缺失该字段时读取为 `0`，不因读取而产生 tracked rewrite；
- `0` 及以上整数合法；
- boolean、负数、浮点数、字符串与超出实现整数范围的值非法；
- 除 Reactivate 外没有 mutation 修改该字段；
- Reactivate 每次成功恰好执行 `old + 1`；
- generation 不回退、不跳号、不按时间、archive count 或目录推导。

所有 generation-sensitive identity 使用：

```text
TaskLifecycleKey = TaskId + lifecycle_generation
```

TaskRef 不参与 generation equality。

### 2.1 Invalid legacy generation repair

Missing generation固定按0读取，不触发repair。类型非法、负数或与可验证durable result冲突时，
`guru-repair-task-lifecycle`是唯一repair owner：

1. 收集tracked task、active/archive locator与全部可验证generation-bound durable result；
2. 若这些事实唯一证明一个非负整数，展示exact repair mutation并在当前对话确认后写入；
3. 若无法唯一证明，展示候选与冲突，要求用户指定candidate；
4. 对用户candidate重新验证其不会把另一个generation的Completion、Closure、Finish、Cleanup或resource
   responsibility改归当前generation；
5. 验证失败时保持`invalid_task_lifecycle`，不得用0、最大值、archive count或session hint猜测；
6. repair只修正非法authority，不承担Reactivate increment。已有合法generation永久不进入该Skill。

## 3. Generation-sensitive state

下列 state 必须绑定 exact TaskLifecycleKey：

- current branch association 与 binding revision；
- session association；
- resource ownership ledger entries；
- Delivery result；
- Completion result；
- Closure result；
- Finish transaction/result；
- Cleanup transaction/result；
- Reactivate input 与 result。

只绑定 TaskId、TaskRef、branch 或 receipt path 的旧合同不足以证明 lifecycle identity。

## 4. Active、Finish 与 archived 状态

每个 generation 依次经历以下封闭状态：

```text
active(planning) -> active(in_progress) -> finish_in_progress -> archived(finish_sealed)
```

固定规则：

- Create与Reactivate均进入`active(planning)`；
- `guru-approve-task-plan:approved`只形成Planning semantic result，不改task status；
- `guru-activate-task`是`planning -> in_progress`的唯一mutation owner，消费current approved DTO，调用确定性
  activation executor并返回`activated`、`session_binding_recovery_required`或`blocked`；
- activation结果丢失且task已为`in_progress`时，同owner只读恢复并rematerialize`activated`，不得第二次执行
  status transition；
- `active(planning)`允许Planning及其前置authority修订，不允许Phase 2、Delivery、Completion、Closure或Finish；
- `active(in_progress)`允许Delivery、Completion、Closure与branch rebind；Planning re-entry不把status回退为planning，
  而是通过stale Planning evidence阻断下游，直到重新approval；
- `finish_in_progress` 只允许同一 Finish transaction recovery；
- `finish_in_progress` 是 transaction state；task artifact 在该 transaction 内可能仍位于 active tree，也可能
  已移动到 archive tree；
- `archived(finish_sealed)` 是唯一稳定成功 post-state，表示 tracked archive locator 与 terminal result均已
  形成；
- `archive locator + no Finish result`只在能证明由pre-cutover Finalizer形成时作为migration degraded state，
  由`guru-restore-archived-task`恢复同一generation的active状态；它不是成功post-state，不具备Reactivate或
  Cleanup资格；
- Cleanup 在 `archived(finish_sealed)` 后独立运行，不改变 task lifecycle status；
- Cleanup 完成与否不改变 generation，也不决定 task 是否 archived。

Finish 必须封存一个 generation，不能把多个 generation 的结果合并为一个 receipt。Archive move 成功但
result 尚未 sealed 时仍属于 `finish_in_progress`，只进入同一 Finish recovery，不具备 Reactivate资格。

## 5. Reactivate

Reactivate 的 entry 条件全部满足后才执行 generation increment：

1. exact archived TaskId 与 TaskRef 匹配；
2. archived generation 合法；
3. 该 generation 存在 sealed Finish result；
4. 不存在未收敛的 Finish transaction；
5. 当前意图明确为 Reactivate；
6. 新 generation 的 source/scope、target 与 checkout acquisition 已完成语义审查；若 archived source需要纠正，
   同时持有current `source_correction_ready` DTO。

Reactivate transaction 原子完成：

- generation 从 `g` 更新为 `g + 1`；
- archived TaskRef 迁移为 active TaskRef；
- lifecycle status 进入新 generation 的 `active(planning)`状态；
- 若存在`source_correction_ready`，写入其中已审查的source；否则沿用current source；
- 建立新 generation 的 branch association 与 ownership entries；
- 旧 generation session association 全部失效；
- 不复制旧 branch association、Completion、Closure、Finish 或 Cleanup result 到新 generation。

Reactivate私有transaction identity同时绑定`source_generation=g`与`target_generation=g+1`。任何
`resume_reactivation` public handoff中的`TransactionRefDTO.lifecycle_generation`固定等于target generation
`g+1`；同一owner恢复时必须从private transaction重新验证source generation `g`的sealed Finish与archived
artifact仍匹配。它不得用source generation `g`作为public transaction generation，也不得把target generation
`g+1`接到旧generation的Finish或Cleanup authority。

旧 generation 的 sealed Finish 与 Cleanup authority 仍只服务旧 generation 的历史恢复和资源清理。它们
不能驱动新 generation。若旧 Guru-owned resource 仍等待 Cleanup，新 generation 不得复用其 ref，直到旧
resource responsibility 收敛。

## 6. Finish recovery 与 Reactivate 意图隔离

面对 archived locator 或 terminal-looking state，调用方必须先声明以下一个意图：

- `finish_recovery`：恢复同一 generation 的未完成 Finish transaction；
- `reactivate`：从 sealed archived generation 创建下一 generation。

两者互斥：

- 存在 `finish_in_progress` 时只进入 Finish recovery；
- 缺失 sealed Finish result 时 Reactivate 被拒绝；
- sealed Finish result 已成立时不再创建第二个 Finish transaction；
- 同一次 resolution 不返回两条候选 route；
- archive presence、唯一 checkout、旧 session 或用户打开旧目录均不能推断意图。

## 7. Stale invalidation

任一 state 的 generation 与 current tracked generation 不一致时：

| State | 行为 |
| --- | --- |
| session association | 删除或标记 stale，不自动重绑 |
| current branch association | 不作为 current；按旧 generation resource responsibility 处理 |
| Completion/Closure | 拒绝当前 lifecycle mutation |
| Finish result | 只允许旧 generation Cleanup/历史读取 |
| Cleanup result | 只说明旧 generation resource outcome |
| public handoff | `lifecycle_generation_mismatch` |

旧 generation state 不是损坏数据；它只是不能成为 current generation authority。

## 8. Recovery matrix

| 状态 | 唯一 owner/route |
| --- | --- |
| generation 缺失的 legacy active task | 读取为 generation 0，继续当前 state recovery |
| generation 类型非法 | `invalid_task_lifecycle`，先修复 tracked metadata |
| active generation 无 session | Session Association recovery |
| active generation 无 branch association | Branch Association recovery |
| archived generation 有未完成 Finish transaction | Finish recovery |
| archived generation 有 sealed Finish，用户声明 Reactivate | Reactivate |
| archived generation 有 sealed Finish，用户声明 Cleanup | Cleanup |
| Reactivate 后收到旧 generation DTO | 拒绝并重新解析 current TaskLifecycleKey |
| 旧 generation Cleanup 尚未完成 | 继续旧 generation Cleanup，不阻塞新 generation 的非冲突 ref |
| 新 generation 请求复用旧 cleanup-pending ref | `resource_ref_unavailable` |

## 9. 当前设计结论

本问题固定以下结论，最终状态仍由全量审核决定：

1. 初始 generation 为 0；
2. legacy 缺失 generation 按 0 读取；
3. Reactivate 是唯一 generation increment owner；
4. 所有 control state 与 lifecycle result 绑定 TaskLifecycleKey；
5. `guru-activate-task`独占planning到in-progress transition，Planning approval不直接改status；
6. Finish recovery 与 Reactivate 使用互斥 intent；
7. archived source correction先形成candidate DTO，再由Reactivate原子应用到新generation；
8. 旧 generation Cleanup 保留自身 authority，但永不驱动新 generation；
9. 非法 generation 只由 `guru-repair-task-lifecycle` 修复，合法 generation 只由 Reactivate 递增。
