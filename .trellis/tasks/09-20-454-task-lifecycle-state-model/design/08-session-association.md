# 08 Path-free Session Association

## 1. 要解决的问题

Session association 只回答“当前 session 正在处理哪个 task generation”。当前实现同时保存 TaskRef、绝对
task workspace root 与 repository common dir，并把 workspace validation 当作 session identity。该模型在
rename、checkout move、跨机器与无稳定 context key 的平台上产生不必要的永久阻塞。

## 2. Stored binding

Session store 按 repository common-dir 与 platform context key 分区。每条 binding 的领域 payload 只包含：

```text
SessionAssociation = {
  task_id,
  lifecycle_generation
}
```

固定规则：

- repository scope 由 common-dir store 提供，不复制到 payload；
- TaskRef 由 TaskId fresh 解析，不持久化；
- branch 由 Current Branch Association fresh 解析；
- checkout path 由 live checkout resolver fresh 解析；
- binding 不保存 HEAD、base HEAD、ownership、resume checkpoint、semantic pass 或用户授权；
- context key 只用于定位 session record，不进入 public task identity；
- session record 是 ignored、machine-local、可丢失 state。

Schema version 与存储 bookkeeping 不属于领域 payload，不能被 consumer 当作 task authority。

## 3. Binding resolution

读取 session binding 后固定执行：

1. 在 common-dir repository scope 内按 TaskId 扫描 current canonical task artifact；
2. 验证 TaskId 唯一且格式合法；
3. 读取 tracked lifecycle generation；
4. 要求 generation 与 binding exact match；
5. 派生 current TaskRef；
6. 验证 task status 与 requested continuation intent；
7. active task 继续解析 current branch association 与 execution checkout；
8. archived task 只进入用户已声明的 Finish recovery、Cleanup 或 Reactivate intent。

Session binding 只选择 TaskLifecycleKey。它不能证明当前 branch、checkout、workflow phase 或 semantic result。

## 4. Bind、resume 与 rebind

### 4.1 Initial bind

Create/Reactivate transaction 完成 TaskLifecycleKey 后：

- context key 存在：写入 exact TaskId + generation，随后重新读取验证；
- context key 不存在：不写 session file，返回 `explicit_task_mode`。

缺失 context key不回滚task、branch association或resource ledger。Context key存在但write/verify失败时，
lifecycle仍已成功，返回`session_binding_recovery_required(TaskLifecycleKey)`并在当前invocation进入
explicit-task mode。Session owner只重试pointer write，不得重复Create、Reactivate、Rebind或checkout
acquisition。

### 4.2 Resume

Binding 存在且 current TaskLifecycleKey 匹配时返回 `session_resumed`。随后仍必须执行 branch 与 checkout
resolution。Binding 存在但 TaskRef 已 rename 时，从 TaskId 派生新 TaskRef，不执行 session repoint。

### 4.3 Missing binding

Binding 丢失时使用共享 resolution protocol：

- 用户显式给出 TaskId；
- 用户从 validated active task candidates 中选择；
- current invocation 已持有可信 TaskLifecycleKey 时直接验证该 key。

验证成功且 context key 存在时写入新 binding；context key 缺失时只在当前 invocation 使用 explicit-task
mode。自动推导失败不阻塞合法显式 TaskId。

## 5. Explicit-task mode

Explicit-task mode 是无持久 session context 时的完整支持路径：

- 当前 invocation 持有 verified TaskLifecycleKey；
- 每个 owner仍执行相同 TaskId、generation、branch 与 checkout validation；
- public handoff 传递下游直接需要的 TaskLifecycleKey，不传路径；
- 当前 invocation 结束后不假设下一 invocation 仍绑定该 task；
- 下一 invocation 再次要求 explicit TaskId 或 candidate selection；
- 平台后续提供 context key 时，重新验证后写入普通 session binding。

因此，task creation 不再因 session identity unavailable 产生不可恢复 fail-close。

## 6. Task switch A -> B -> A

Session switch 是 pointer mutation，不是 task state mutation。A -> B 固定执行：

1. 读取当前 binding 并验证 A 的 TaskLifecycleKey；
2. 独立验证 B 的 TaskId、generation、status 与 requested intent；
3. 验证 B 的 branch/checkout resolution 不依赖 A；
4. 原子把 session payload替换为 B；
5. 重新读取并验证 B binding；
6. 不修改 A 的 branch association、ownership、TaskRef 或 lifecycle result。

B validation 失败时保留 A binding。B -> A 使用完全相同流程，重新读取 A 的 current generation；旧 A
generation 已 Reactivate 时，旧 binding target 被拒绝，必须选择新 generation。

多个 session 能同时绑定同一 TaskLifecycleKey。Session association 不承担 task lock 或 ownership。

## 7. Reactivate invalidation

Reactivate 从 generation `g` 进入 `g+1` 后，任何仍保存 `(TaskId, g)` 的 binding 在下一次读取时返回
`session_generation_stale`。它不自动升级到 `g+1`，因为用户必须明确进入 reactivated task。

用户选定新 generation 并通过验证后，当前 session 写入 `(TaskId, g+1)`。其它 session 保持 stale，直到
各自重新绑定。

## 8. Invalid/corrupt binding

| 状态 | 唯一行为 |
| --- | --- |
| session file 缺失 | missing-binding recovery |
| TaskId 不存在 | 删除 invalid pointer 前展示诊断，进入 selection-required |
| TaskId 重复或 collision | `guru-establish-task-identity` conflict route |
| generation mismatch | stale binding，不自动升级 |
| stored TaskRef/workspace/path legacy fields存在 | 忽略，不参与 resolution |
| branch association missing | Session TaskLifecycleKey 保持，转 Branch Association recovery |
| checkout missing | Session TaskLifecycleKey 保持，转 Checkout acquisition |
| context key unavailable | explicit-task mode |
| context key存在但write/verify失败 | 保持lifecycle success，session-binding recovery + explicit-task mode |
| switch target invalid | 保留 current valid binding |

## 9. Public handoff

Session owner的成功 output 只传下游直接需要的：

- `TaskLifecycleDTO`，字段恰好为 TaskLifecycleKey 的 `task_id + lifecycle_generation`；
- current resume target。

需要读取 task artifact 的 consumer 按 TaskId 派生 TaskRef并重新验证。Public output 不传 session file path、
context key、common-dir path、checkout path、branch、HEAD 或 `task_ref`。Bind 的成功 output 不得改用
`TaskArtifactDTO`。

## 10. 当前设计结论

本问题固定以下结论，最终状态仍由全量审核决定：

1. stored session payload 只有 TaskId 与 generation；
2. TaskRef 不再持久化到 session；
3. rename 与 checkout move 不要求 session repoint；
4. 缺失 context key 使用 explicit-task mode；
5. A -> B -> A 只切换 pointer，不覆盖 task state；
6. Reactivate 不自动升级旧 session binding；
7. session write failure不回滚或重放已成功的lifecycle mutation；
8. session success 不替代 branch、checkout 或 semantic validation。
