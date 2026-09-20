# 01 稳定 Task Identity 与可变 Task Locator

## 1. 要解决的问题

用户结果要求同一 task 在 rename、checkout move、跨 session、跨机器、branch rebind、archive 和
Reactivate 后仍然是同一 task。

当前实现不能满足该结果：

- `task.py create` 同时把 slug 写入 `task.json.id` 与 `task.json.name`；
- `task.py rename` 把 `id`、`name` 和 task directory 一起改写；
- session record 使用 task path 与绝对 workspace path 解析当前 task；
- `task.py start` 在 `task.json.branch` 为空时把 invocation branch 写回 metadata；
- Reactivate 同时改写 branch、base branch、worktree path 和 lifecycle generation；
- 多个 public contract 只传递 `task_ref`，没有独立验证稳定 task identity。

因此，当前 `id` 实际上仍是可变 slug，`task_ref`、branch 和 workspace path 又被用来补足身份。根本修复
不是增加 rename 同步逻辑，而是把稳定身份与可变 locator 分开。

## 2. 当前 repository 证据

2026-09-20 对当前 repository 的 task artifacts 扫描结果：

- 190 个 task 均存在非空 `task.json.id`；
- 190 个 id 均符合 `[A-Za-z0-9][A-Za-z0-9._-]*`；
- 未发现大小写字符；
- 未发现重复 id；
- 未发现缺失 id。

这证明当前 repository 能原位采用 immutable id，不需要先批量重写历史 task。该事实不证明 business
repository 的 legacy task 也完整，因此仍需显式 identity establishment。

## 3. 领域对象

### 3.1 TaskId

`TaskId` 是 repository lifecycle history 内的稳定 task identity。它只在一个 repository scope 内唯一；
跨 repository 边界的完整身份是 `RepositoryIdentity + TaskId`。RepositoryIdentity 由调用边界的 repository
owner 提供和验证，不复制进 `task.json`，也不使用本机路径充当 portable repository identity。

固定合同：

- authority 是 tracked task artifact 中的 `task.json.id`；
- 值符合 `[A-Za-z0-9][A-Za-z0-9._-]*`；
- 比较使用精确字节值；唯一性校验同时拒绝 case-fold collision；
- create 或 legacy establishment 成功后永久不可修改；
- rename、archive、Reactivate、branch rebind、checkout move、session switch 均不改变它；
- task 完成与 resource Cleanup 后仍不得由无关 task 复用。

TaskId 不编码 Issue number、日期、branch、path、owner、platform 或 lifecycle state。创建时允许使用可读
slug 作为 reviewed candidate，但 candidate 只有在完整校验并写入后才成为 TaskId。

### 3.2 TaskRef

`TaskRef` 是当前 repository tree 内指向 task artifact directory 的 repo-relative locator。

固定合同：

- active、archived 和 reactivated task 分别拥有当前状态对应的 locator；
- rename、archive 与 Reactivate 会改变 TaskRef；
- TaskRef 不参与 task 相等性判断；
- 任何同时携带 TaskId 与 TaskRef 的 consumer 都必须读取 `TaskRef/task.json` 并验证其中 TaskId 相同；
- stale TaskRef 只表示 locator 已变化，不表示 task identity 消失或产生新 task。

### 3.3 TaskLifecycleKey

需要区分 Reactivate 前后 lifecycle 的 owner 使用：

```text
TaskLifecycleKey = TaskId + LifecycleIncarnation
```

本文件只固定 TaskId 是稳定部分。`LifecycleIncarnation` 的生成、递增和 terminal 规则由问题 03 设计，
不得反向改变 TaskId。

## 4. 唯一 authority 与禁止的替代来源

### 4.1 唯一 authority

在一个稳定 repository state 中，每个 TaskId 恰好对应一个 canonical tracked task artifact：

- active task 位于 active task tree；
- finished task 位于 archive tree；
- Reactivate 完成后，同一 artifact identity 回到 active tree。

repository 本身提供 TaskId 的作用域。TaskId 不保存本机 repository path、Git common-dir path 或 remote
URL；这些 live facts 不能改变 tracked task identity。跨 repository public handoff 必须由拥有该边界的
contract 另行携带 repository identity，不能把 repository scope 隐式省略为全局 TaskId。

### 4.2 禁止作为 identity authority 的事实

以下事实只能用于候选发现或当前操作，不能建立 TaskId：

- task directory name；
- `task.json.name`、title、description；
- Issue repository 或 number；
- branch name；
- checkout path、worktree name、workspace slug；
- session context；
- current HEAD、base HEAD、commit 或 PR URL；
- task/workspace mapping 与历史 runtime record。

这些事实与 TaskId 不一致时必须报告 conflict，不得用它们覆盖 `task.json.id`。

## 5. 状态与 mutation

### 5.1 Create

Create 必须按以下顺序建立 identity：

1. 取得 reviewed TaskId candidate；
2. 校验格式与 case-fold 形式；
3. 扫描 active task、archive task 与仍承担 lifecycle/resource responsibility 的记录；
4. 确认 exact id 和 case-fold id 均未被占用；
5. 在首次 task artifact 写入中写入 TaskId；
6. 返回的 task handoff 同时携带 TaskId 与当前 TaskRef。

任一校验失败时零 task write。`--force` 不得覆盖已有 task identity，也不得成为 TaskId 冲突绕过入口。

### 5.2 Rename

Rename 只改变：

- task directory 与 TaskRef；
- 可变 display/name 字段；
- 直接保存 TaskRef 的 back-reference。

Rename 不修改 `task.json.id`。以 TaskId 为 key 的 runtime state 不需要 repoint；仍保存 TaskRef 的短期
consumer 必须在 rename transaction 中更新，更新后重新验证 `TaskRef -> TaskId`。

### 5.3 Archive

Archive 把 canonical artifact 从 active locator 移到 archive locator，并更新 lifecycle status。TaskId 原字节
保留。稳定 post-state 必须满足：

- active tree 中不存在该 TaskId；
- archive tree 中恰好存在一个该 TaskId；
- archive TaskRef 指向的 metadata 仍声明同一 TaskId。

Archive 不依赖 `task.json.branch` 证明 task identity。branch 与 Finish freshness 属于后续问题。

### 5.4 Reactivate

Reactivate 输入必须同时声明 archived TaskRef 与 expected TaskId。mutation 前读取 archive metadata 并验证
两者一致。成功后：

- archive locator 退出 current locator；
- active tree 中出现一个新 TaskRef；
- `task.json.id` 保持原字节值；
- lifecycle incarnation 按问题 03 的规则变化。

Reactivate 不从 archive directory name 反推 TaskId，也不创建新 TaskId。

### 5.5 Legacy identity establishment

legacy task 出现以下任一状态时进入 `identity_establishment_required`：

- `task.json.id` 缺失；
- id 格式非法；
- exact id 与另一个 task 冲突；
- id 与另一个 task 发生 case-fold collision。

该状态不得自动使用 directory name、`name`、Issue 或 branch。`guru-establish-task-identity`只把这些值作为
非权威候选展示给用户。用户显式指定一个TaskId candidate后，执行与Create完全相同的格式和全repository
uniqueness校验；通过后执行一次tracked identity establishment mutation。该mutation必须同时完成以下闭合：

- 写入 canonical TaskId；
- 重新验证当前 TaskRef 仍指向同一 task artifact；
- 使可证明属于该 task 的现有 durable lifecycle result 绑定新 TaskId；
- 不复制、不猜测、不改写无法证明归属的 runtime state；
- 将缺失的 branch、session 与 resource control state 留给各自后续 recovery owner。

建立成功前，除只读诊断和 identity establishment 外的 lifecycle mutation全部阻塞。建立成功后 TaskId
永久不可修改。若两个 legacy task 共享同一 id，用户必须指定哪一个保留该 id，并为另一个指定不同 id；
系统不得按 active/archive、mtime、路径或当前 session 自动裁决。若已有不可变远端结果无法证明属于
所选 TaskId，identity establishment 必须停止并报告该 external result conflict，不能通过写入 TaskId
掩盖历史归属不确定性。

## 6. Resolution 合同

### 6.1 已知 TaskRef

1. 规范化为 repository-relative locator；
2. 验证 locator 位于受支持的 active 或 archive task tree；
3. 读取 `task.json`；
4. 校验 TaskId 格式；
5. 当调用方携带 expected TaskId 时，要求 exact match；
6. 校验 repository 内不存在另一个 canonical artifact 声明相同 TaskId。

成功结果是 `(TaskId, current TaskRef, lifecycle state)`，不是绝对路径。

### 6.2 已知 TaskId

1. 扫描 active 与 archive canonical task artifacts；
2. 使用 exact TaskId 匹配；
3. 同时检查 case-fold collision；
4. 恰好一个匹配时返回其 current TaskRef；
5. 零匹配返回 `task_not_found`；
6. 多匹配或 collision 返回 `invalid_task_identity`。

不建立 tracked identity index。active/archive artifacts 已是 durable authority；新增 index 只会形成第二
authority。运行期只构建调用期内存索引，不能持久化为 identity source。

## 7. Public handoff 规则

后续 contract 按 consumer 需求使用以下最小组合：

- 只需要稳定归属：TaskId；
- 需要读取当前 task artifact：TaskId + TaskRef；
- 需要区分 Reactivate 前后 lifecycle：TaskId + LifecycleIncarnation；
- 同时需要 artifact 与 lifecycle：TaskId + TaskRef + LifecycleIncarnation。

上述组合均处于已验证 repository context 内。跨 repository consumer 在此基础上额外携带并验证
RepositoryIdentity。

只传 TaskRef 的现有 lifecycle handoff 不足以证明稳定 identity，必须在迁移设计中增加 TaskId，consumer
必须验证二者一致。TaskId 不携带 checkout path、branch 或 HEAD。

Finish、Cleanup、Reactivate 与 receipt identity 不得再仅以 TaskRef 参与 hash 或 equality；否则 rename、
archive move 会把同一 task 解释成新 identity。它们必须以 TaskLifecycleKey 为归属，并把 TaskRef 仅作为
当前 locator。

## 8. Failure matrix

| 输入状态 | 结果 | 是否写入 |
| --- | --- | --- |
| 合法、未占用的 Create candidate | 建立新 TaskId | 首次 task write |
| Create candidate exact collision | `task_identity_conflict` | 否 |
| Create candidate case-fold collision | `task_identity_conflict` | 否 |
| TaskRef 存在且 metadata id 匹配 | resolution success | 否 |
| TaskRef 存在但 expected id 不匹配 | `invalid_task_identity` | 否 |
| 同一 id 出现在 active 与 archive | `invalid_task_identity` | 否 |
| rename | TaskRef 改变，TaskId 保持 | 仅 locator/display/back-reference |
| archive | active TaskRef 变为 archive TaskRef，TaskId 保持 | lifecycle/archive mutation |
| Reactivate | archive TaskRef 变为 active TaskRef，TaskId 保持 | lifecycle/reactivate mutation |
| legacy id 缺失或非法 | `identity_establishment_required` | 否 |
| 用户指定合法 legacy candidate | identity established | 仅 task identity establishment |
| 用户指定冲突 legacy candidate | `task_identity_conflict` | 否 |
| legacy task 存在无法归属的不可变远端结果 | `external_result_identity_conflict` | 否 |

## 9. 用户结果可行性检查

| 用户场景 | 为什么 TaskId 保持稳定 |
| --- | --- |
| rename | 只改变 TaskRef 与 display/name，identity 字段不再参与 rename。 |
| checkout move | TaskId 位于 tracked task artifact，不包含 checkout path。 |
| 跨 session | stored session 只引用 TaskId 与 generation；TaskRef 每次从 TaskId 重新解析。 |
| 跨机器 | task artifact 已进入显式 ref 可达的可传输 Git history 后，目标机器读取同一 TaskId；local-only artifact 不被宣称可恢复。 |
| branch rebind | branch association 引用 TaskLifecycleKey，不改 TaskId。 |
| archive | artifact locator 改变，metadata id 原样保留。 |
| Reactivate | 沿用 archived TaskId，只创建新 lifecycle incarnation。 |

跨机器恢复存在明确 portability boundary：未提交 task artifact、ignored control state 与本机 working tree
不会随 clone 自动出现。源机器必须先由`guru-checkpoint-task-state`，或普通Task Commit随后由Publication
传输，或Publication直接把exact task artifact放入目标机器可获取的显式ref。目标机器找不到该
artifact 时返回 `task_artifact_not_portable`，不得从 Issue、branch 或目录重建 identity。

因此，第一个用户结果在不引入 task/workspace mapping 的前提下可实现。该结论依赖后续问题满足三条
接口约束：branch/session/resource state 必须以 TaskId 或 TaskLifecycleKey 归属，checkout resolution 必须
把 TaskRef 验证回同一 TaskId，跨机器恢复必须先满足 portable checkpoint/sync 前置条件。

## 10. 当前设计结论与后续边界

本问题采用以下固定结论：

1. `task.json.id` 是 immutable TaskId；
2. directory 与 `task.json.name` 是可变 locator/display，不是 identity；
3. repository 内不新增 durable task identity index；
4. create 在 active、archive 和未终结责任记录间执行 uniqueness validation；
5. legacy 缺失或冲突 identity 通过用户显式 establishment 恢复，不自动猜测；
6. public lifecycle handoff 不再仅以 TaskRef 证明 identity；
7. rename、archive、Reactivate 必须保持 id 原字节不变。

本文件不决定 lifecycle incarnation schema、branch association store、session store、checkout resolver 或
resource ownership record；这些内容分别由后续独立问题设计。若后续设计要求修改 TaskId，说明该设计与
本问题冲突，必须返回这里重新审查，不能增加例外。
