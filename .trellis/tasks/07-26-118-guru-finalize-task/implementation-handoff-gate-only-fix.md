# Gate-only finalization freshness 修复 handoff

## 1. 现场复现与根因

在已确认的 immutable closeout plan 上，`record-finalization-gate` 正常写入
`task-finalization-gate.json` 后，真实 public checker 返回：

- `task finalization gate plan identity mismatch`
- `task finalization gate current facts mismatch`
- `Task finalization route output plan_ref does not match current facts.`

因果链已定位到
`check_task_publication_for_finalization_augmentation()`：首次 formal transition 前，
task-local `closeout-plan.json` 尚未落盘，唯一新增 finalizer-owned tracked delta 是
`task-finalization-gate.json`。函数已正确构造 `finalization_paths=[gate_relative]`，并用它
完成 repository exact-delta 判断；但消除 entry-precondition stale 时又把 owner allowlist
硬编码为 `[plan_relative]`。因此 gate-only 正常路径被 publication owner 误判 stale，
finalization preview 失去 current plan，最终外显为上述三项 mismatch。

该复现来自 recorder -> checker 的正常 honest workflow，不依赖伪造、并发、锁、TOCTOU
或额外 fault injection。

## 2. 实现改动

- Canonical runtime：二次
  `task_publication_entry_precondition_bindings()` 重算直接复用同一已验证的
  `finalization_paths`。
- Canonical tests：新增 gate-only exact delta 正向回归，并新增 gate-only unexpected
  metadata 与 `require_plan=True` 缺 plan 两条 fail-closed 回归。
- Dogfood runtime：通过官方 preset `apply.sh --repo .` 同步，canonical 与 installed
  runtime byte-identical。

该改动没有增加新状态、DTO、exit、route 或脚本判断；只修正同一 validator 内 exact
allowlist 的传递。Plan-only、gate+plan、unexpected path 与 plan-required 语义保持不变。

## 3. 验证结果

- 聚焦 augmentation 回归：5/5 passed。
- `TaskPublicationMetadataAllowlistTest` + `CloseoutTransactionContractTest`：
  100/100 passed。
- Runtime 全量：620 passed，13 skipped。
- `guru-finalize-task` package：5/5 passed。
- Skill package / production eval：179/179 passed。
- Preset installer：45/45 passed。
- Upstream ownership：9/9 passed。
- Canonical/dogfood runtime `cmp`：byte-identical。
- `check-dogfood-overlay-drift.sh`：passed。
- `py_compile` 与 `git diff --check`：passed。

Preset apply 首次按当前 selected platforms 运行时产生 523 个 Claude managed removal；
随后用官方 `--all-platforms` 重新应用，恢复全部 Claude 分发并取得
`removal_count=0`。Installer 生成的 extension 运行记录已恢复为 apply 前的 exact Git
blob；runtime `.bak` 与本轮 cache 已移到
`/tmp/guru-issue118-gate-only-cleanup.1VYNM1`，不进入 task diff。

## 4. Docs SSOT 判定

不需要修改 durable Docs SSOT。现有 contract 已要求 finalizer-owned exact metadata
delta、owner-private gate、formal checker freshness 与 unexpected-path fail closed；本次是
runtime 偏离既有合同的 correctness 修复，不改变公共 I/O、事务顺序、recovery matrix、
安装命令或用户可见语义。

## 5. 明确未改边界

- 未修改 global workflow 或 Finish family routing。
- 未修改 upstream `trellis-finish-work` Skill/Command/Prompt 或官方 `task.py`。
- 未修改 preset overlay ownership、#119 集成或 #132 cleanup。
- 未改变 #105 已完成的事务顺序、PR/archive/ready 语义。
- 未修改 main-owned `phase2-check.json`、Branch Review Gate、publication gate 或
  finalization gate。
- 未 commit、push、创建 PR、archive 或修改 Issue。

## 6. 后续与剩余风险

本修复新增 runtime/test/handoff 路径后，之前绑定 `4f254b70...` 的 Phase 2、Branch
Review、Publication Review、immutable closeout plan 与 confirmation 均需由主会话按 owner
workflow 重新生成、复审并取得必要确认。当前真实 checker 仍会因为并行更新的
`agent-assignment.json` 使既有 publication evidence stale 而返回外层 finalization
mismatch；这属于预期 freshness 阻断，不能由实现子代理越权刷新或忽略。

除上述 mandatory re-review/reprepare 外，未发现本实现范围内 remaining correctness
blocker。
