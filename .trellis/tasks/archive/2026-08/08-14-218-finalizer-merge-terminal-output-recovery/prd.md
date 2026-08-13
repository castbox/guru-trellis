# Issue #218：Finalizer/Merge 终态输出与幂等恢复

## 目标

修复 `guru-finalize-task` 与 `guru-merge-task-pr` 已完成确定性远端事务后无法稳定向 workflow 物化终态结果的问题。所有成功 execute wrapper 必须在 stdout 恰好输出一个可解析 JSON object；同一计划已达到 Ready 或 merged terminal state 时，恢复路径直接消费经 live 复核的 terminal DTO，不重复 Git/GitHub mutation。

## 背景与事实

- Live Issue #218 是需求 SSOT，当前开放、无评论，唯一 assignee 为 `wesleywu`。
- #219 与 #217 已按固定顺序合并；当前基线为 `main@3bc80e83afe0f2a9c5b81b9c1746466f0e55acb3`，受管 Python runtime 支持 Draft 2020-12。
- #217 的真实 finalization 再次复现：executor 进程完成后 wrapper 无 stdout/exit result，workflow 只能重新读取 branch、remote、PR、archive 与 private transaction 判断停点。
- Finalizer current runtime 已能识别 `transaction_state=ready`，但 `trellis/skills/guru-team/packages/guru-finalize-task/runtime/owner.py:11860` 起的 execute 分支仍会在 `:11871` 调用 Draft-only `cmd_finish_work`；Merge owner 在 `trellis/skills/guru-team/packages/guru-merge-task-pr/runtime/owner.py:837` 已能读取 `terminal_output`，但 mutation 后 stdout/恢复消费链不完整。
- 无前缀 `task-finalization-gate.json` 与 `semantic-review-input.json` 仍指向 legacy schema/`verification_required`，与 #205 后的 current business Finalizer 不一致。

## 需求

### R1 Execute wrapper 单 JSON stdout

- `execute-finalization-transition.sh` 与 `execute-task-pr-merge.sh` 的每条成功路径 exit 0 且 stdout 恰好一个 JSON object。
- 输出由 package handler 返回 dict，经统一 dispatcher 序列化；不得在 bash wrapper 中补 `printf`，不得输出诊断日志或多个 JSON。
- stderr 只用于诊断；terminal DTO 必须符合 command/interface 声明与唯一 consumer 合同。

### R2 Finalizer Ready 同计划恢复

- 当 plan/task/repo/base/branch/archive/summary/PR/head/close scope 均经 current live facts 证明一致，`transaction_state=ready` 直接物化 `ready_for_merge` DTO。
- 不再调用 Draft-only `cmd_finish_work`，不重复 push、PR create/update/ready、archive 或 commit。
- 成功消费后按 current contract 退休 transaction、gate/request 与 superseded owner-private state。
- 任一 identity 或内容不匹配继续 fail closed，不追认 arbitrary out-of-order state。

### R3 Merge terminal 恢复

- expected-head merge 与 closure 验证完成后，先持久化最小 terminal output，再交给 dispatcher 输出单 JSON。
- 同一 gate 的精确 PR 已 merged 时，重新验证 merge commit 与 Issue closure，消费既有 terminal output并退休 gate，不再次 merge。
- closure mismatch 保留现有 typed exit，不静默转为 `merged`。

### R4 Current/legacy examples 收敛

- 无前缀 current Finalizer gate/semantic-review examples 使用 current gate schema、`ready_for_merge` executor marker 与 Merge consumer。
- immutable legacy examples/schema 显式使用 legacy 文件名、artifact/interface id 或文档说明。
- current package tests拒绝 `verification_required` 成为 business Finalizer current route。

### R5 投影与安装一致性

- 同步 canonical source、installed package、Shared/Codex/Claude/Cursor projections、schemas、examples、Interface、README 与 managed inventory。
- preset targeted apply/reapply 后 dogfood drift 为零，未知 `.new`/`.bak`/sidecar 为零。

## 验收标准

1. 真实 shell wrapper fixture 覆盖 Finalizer 与 Merge fresh success：exit 0，stdout 可被一次 `json.loads` 完整解析且无额外字节。
2. 覆盖 mutation 成功但首次输出丢失后的同计划恢复；恢复不重复任何 Git/GitHub mutation。
3. Finalizer `ready` recovery 不调用 Draft-only finish path，并输出 current `ready_for_merge` DTO。
4. Merge terminal recovery 重新验证 exact PR/head/merge commit/closure，输出 `merged` 或现有 `closure_mismatch`。
5. 覆盖 plan/task/repo/base/branch/PR/head/summary/close-scope stale/mismatch 的关键 fail-closed 矩阵。
6. current examples 不再使用业务 `verification_required`；legacy 资产保留但显式标识。
7. Finalizer/Merge package/runtime/integration tests、source-installed equality、targeted apply/reapply、managed inventory、dogfood drift 与零未知 sidecar通过。

## 范围边界

- 不实现 #208 的跨 task existing Ready PR adoption。
- 不实现 #223 的 required CI、Ready 时序或自动合并策略。
- 不恢复业务 `verification_required`，不调用 `guru-verify-extension-installation`。
- 不执行 #222 的完整 marketplace、official update、全平台 throwaway、业务仓库 upgrade smoke或 Release/tag。
- 不处理恶意伪造、并发竞态、锁、TOCTOU、额外 crash consistency。
- PR 只关闭 #218；#208、#222、#223 保持独立。

## Docs SSOT Plan

- `trellis/skills/guru-team/packages/guru-finalize-task/{SKILL.md,references/contract.md}`：拥有 Finalizer ready terminal 物化、恢复与退休语义。
- `trellis/skills/guru-team/packages/guru-merge-task-pr/{SKILL.md,references/contract.md}`：拥有 Merge terminal checkpoint、live 重验、恢复与退休语义。
- `.trellis/spec/workflow/{companion-scripts.md,skill-package-contract.md}`：仅在实现确认存在可复用的 dispatcher single-JSON/terminal-result 不变量时更新。
- `.trellis/spec/preset/installer.md` 与 `trellis/presets/guru-team/README.md`：仅在受管投影/验证入口发生可见变化时更新。
- global workflow phase/typed-exit graph不变；不新增 workflow route。
