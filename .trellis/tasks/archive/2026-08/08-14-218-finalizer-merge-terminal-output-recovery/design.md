# 技术设计

## 1. 根因模型

问题不是单纯“缺少打印”，而是确定性 transaction 与 public command 结果物化之间缺少稳定的 terminal 边界：

```text
mutation owner
  -> 持久化最小 terminal facts
  -> live/objective revalidation
  -> handler return dict
  -> shared dispatcher exactly-once JSON serialization
  -> public invoke 消费并退休 owner state
```

当前缺口分别表现为：

- Finalizer：`ready` context 已存在，但 execute 仍可进入 `cmd_finish_work` 的 Draft-only 路径。
- Merge：merge/closure 完成后 terminal facts 没有形成可恢复的“先持久化、后输出”闭环。
- Dispatcher 边界：真实 shell wrapper 的成功 mutation path 没有稳定证明 handler dict 被序列化为单 JSON stdout。

## 2. Finalizer 设计

### 2.1 Ready terminal context

复用 current `finalization_current_terminal_gate`、`finalization_current_terminal_context` 与 `finalization_gate_with_ready_for_merge_output`，收敛为唯一 terminal materializer。其输入必须绑定：

- current task/archive locator 与 summary；
- exact plan、repo、base/head branch、reviewed/publication HEAD；
- local/remote/PR head 与 Ready PR identity；
- pre-merge close Issue facts。

### 2.2 Execute state dispatch

`execute-finalization-transition` 根据 checker-passed transaction state显式分流，修改入口以 `trellis/skills/guru-team/packages/guru-finalize-task/runtime/execute.py:7` 和 `runtime/owner.py:11860` 为主：

- pre-terminal states：执行现有 push/Draft/archive/Ready transaction；
- `ready`：只做 terminal live revalidation并物化 `ready_for_merge`；
- mismatch：返回现有 fail-closed route/error，不回退到 Draft-only finish。

terminal 成功后由 public invoke 按 current lifecycle退休 transaction、gate/request/private publication input；terminal DTO仍是交给 `guru-merge-task-pr` 的最小 output。

## 3. Merge 设计

### 3.1 Terminal output checkpoint

Merge gate 内只保留 current contract 已允许的最小 `terminal_output`；读取/写入入口分别锚定 `trellis/skills/guru-team/packages/guru-merge-task-pr/runtime/owner.py:837` 与 `:924`。内容限于 exit、repo/PR identity、expected head、merge commit、closure result与直接 consumer必需字段。写入顺序为：

1. expected-head merge；
2. live PR merged/merge commit重验；
3. close Issue逐项验证；
4. 持久化 terminal output；
5. handler 返回同一 dict，由 dispatcher序列化。

若第 5 步输出丢失，同一 gate恢复从第 2 步开始只读复核，不再次调用 merge。

### 3.2 Closure mismatch

closure mismatch 是既有 terminal typed exit。它同样先持久化，再输出；恢复时重新读取 closure facts并保持 `closure_mismatch`，不得因为 PR 已 merged而改写为 `merged`。

## 4. Dispatcher 与 stdout

- package bash scripts保持纯 launcher，不增加 Skill-specific输出逻辑。
- runtime handler所有成功分支返回 dict；shared dispatcher只序列化一次。
- 真实 wrapper测试同时检查 exit code、完整 stdout bytes、单 object解析和 stderr边界。
- 直接 Python unit test仅作补充，不能替代 shell launcher + managed dispatcher fixture。

## 5. Current/legacy 迁移

- current无前缀 examples迁移到 current schema/route。
- legacy schema 3.0与 `verification_required` 示例重命名或通过 interface artifact id明确标记 legacy，保持 immutable compatibility读取但不进入 current package route/eval。
- Interface、eval facts、README与测试使用 current `ready_for_merge` consumer；current registry/graph不新增 `verification_required`。

## 6. 受管投影

canonical source位于 `trellis/skills/guru-team/packages/`。修改后通过 preset installer同步：

- `.trellis/guru-team/skills/packages/` installed copies；
- `.agents/skills/`、`.codex/skills/`、`.claude/skills/`、`.cursor/skills/` discovery projections；
- extension manifest/managed inventory。

不直接把 installed/dogfood副本当作 SSOT。

## 7. 失败与恢复不变量

- 任何 repo/task/plan/base/branch/PR/head/summary/close-scope mismatch fail closed。
- recovery只接受同 plan、同 gate、同 terminal identity。
- terminal recovery的 mutation计数必须为零。
- terminal output写入失败不得声称成功；output丢失不得导致重复 mutation。
- 不增加 lock、TOCTOU或恶意篡改防御。

## 8. 回滚

变更集中于两个 package及其投影。回滚为恢复 canonical package到基线并重新 apply preset；不得只回退 installed副本。任何 schema/interface breaking change必须保留显式 legacy identity，不能静默复用 current id。
