# Issue #118 finalization gate re-entry 修复交接

## 1. 身份、边界与 lifecycle

- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- 当前 HEAD：`c04ed1d7a816ac80217953bcf52f7a2a44b645d2`。
- Technical agent id：`/root/issue118_finalization_gate_reentry_fix`。
- Logical role：`实现代理`。
- Finding：`F-FINALIZATION-GATE-REENTRY-01`。
- 本轮入口：主会话显式派发 active task 后，workspace boundary 与 planning approval
  checker 均通过；expected workspace 与 actual repo root 完全一致。
- 本轮终态：implementation completed；无运行中命令，无实现 blocker。主会话负责把本
  handoff 与 lifecycle 状态写入 `agent-assignment.json`，实现代理未写该 artifact。

本 handoff 只证明本 finding 的 implementation 与验证状态，不替代 fresh Phase 2、task
commit、独立 Branch Review、publication review 或 finalization gate，也不授权远端副作用。

## 2. 正常路径根因

`record-finalization-gate` 在第一次 formal transition 前会写入唯一 task-local
`task-finalization-gate.json`。此时 immutable plan 尚未 materialize，publication readiness
仍没有 `publish_inputs`。随后 checker 通过 `resolve_closeout_pre_draft_state()` 识别
`prepared` 状态时，仍调用 generic publication checker。Generic checker 不拥有也不接受
刚写入的 finalizer-private gate，于是把正常 recorder delta 误报为 repository/entry binding
stale，导致 recorder 无法重入自身 checker。

该缺陷可由 honest workflow 的真实 recorder -> checker 顺序直接触发，不依赖人为伪造、
恶意输入、并发 finalizer、锁、TOCTOU、额外 fault injection、crash consistency 或跨 OS
原子性。

## 3. 实现

在 `resolve_closeout_pre_draft_state()` 的精确 prepared 分支中：

1. 当 plan 尚未 materialize、readiness 尚无 `publish_inputs`，且 direct task-local
   `task-finalization-gate.json` 是 regular non-symlink file 时，调用既有
   `check_task_publication_for_finalization_augmentation()`。
2. 显式传入唯一 owner-owned gate locator，`require_plan=False`；augmentation 继续执行
   exact repository/entry binding 校验。
3. Gate 不存在时保持原 generic publication checker 路径。
4. 任意额外/unowned metadata 仍因 exact status delta 不匹配而 fail closed。

新增 regression 通过真实 `cmd_record_finalization_gate()` 先写 gate，再调用
`cmd_check_finalization_gate()`：

- exact gate-only prepared path 返回 `transaction_state=prepared` 与
  `typed_exit=verification_required`；
- 同一路径加入 arbitrary task metadata 后，checker 必须抛出 `WorkflowError`。

该改动没有新增 public DTO、profile、schema、typed exit、consumer、transaction state 或
route，没有修改 generic publication checker、#117 checker、global workflow、preset overlay、
upstream Finish family、official `task.py` 或 #105 transaction ordering。

## 4. 精确 owned paths

本实现代理拥有以下最终 delta：

1. `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
2. `.trellis/guru-team/scripts/python/guru_team_trellis.py`
3. `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
4. `.trellis/tasks/07-26-118-guru-finalize-task/implementation-handoff-finalization-gate-reentry-fix.md`

Canonical 与 dogfood runtime 已通过 official preset apply 同步并保持 byte-identical。
`.trellis/guru-team/extension.json` 的 installer action/provenance churn 已精确收敛，当前相对
HEAD byte-for-byte no-diff；递归 `.new`/`.bak` 为零，manifest conflict/sidecar 为零。

工作树中现有 `agent-assignment.json`、`finish-summary-index.json`、
`issue-scope-ledger.json`、`pr-body.md`、`pr-readiness.json`、`review-gate.json`、
`review.md`、`task-commit-plans/006.json`、`task-finalization-gate.json` 与 Round 13/14 raw
reports 属于主会话/独立 review/旧 closeout evidence；本实现代理未回退、覆盖或声明拥有。

## 5. Docs SSOT reconciliation

Approved strategy 保持 `ssot_first`。本修复以 durable
`.trellis/spec/workflow/skill-package-contract.md`、
`.trellis/spec/workflow/companion-scripts.md` 与
`guru-finalize-task/references/contract.md` 为主要实现输入；task planning artifacts 只提供
Issue #118 delta 与验收边界。

Docs outcome 为 `no_docs_update_needed`：现有 durable contract 已明确 finalizer-owned exact
metadata augmentation、owner-private gate、generic checker strictness、prepared route 与
unexpected-path fail closed。本修复只让 runtime 对齐既有 SSOT，不改变公共 I/O、recovery
matrix、transaction order、安装方式或用户可见语义。

- Durable docs sync：无需新 delta，既有 SSOT 与实现一致。
- Task delta merge：没有待合并到 durable docs 的新语义。
- Task-history-only content：本 handoff 的复现、finding closure 输入与验证记录。
- Follow-up/current PR limitation：无 docs follow-up；当前 PR 仍必须完成 fresh Phase 2 与后续
  owner gates，#119/#132 边界保持不变。

## 6. 验证终态

- 新增 focused regressions：2/2，`OK`。
- `guru-finalize-task` package contract：5/5，`OK`。
- Full runtime / #105 recovery matrix：626 tests，`OK (skipped=13)`。
- Full Skill package graph：179 tests，`OK`。
- Preset installer：45 tests，`OK`。
- Upstream ownership tests：9 tests，`OK`。
- Upstream ownership validator：`status=ok`；frozen/active overlay 均为 43，active Skill 为
  13，planned Skill 为 0。
- All-platform preset reapply：`status=ok`，2659 managed files 最终均为 `unchanged`，
  `removal_count=0`、`conflict_count=0`、`sidecar_count=0`。
- Dogfood overlay drift：passed。
- Canonical/dogfood runtime `cmp`：passed。
- Canonical runtime 与 preset installer `py_compile`：passed。
- `.trellis/guru-team/extension.json` no-diff：passed。
- Recursive `.new/.bak` scan：零结果。

最终 `git diff --check`、owned-path inventory、runtime/test/handoff SHA-256 与 size 由本
handoff 写入后再执行并在实现代理 final 中交给主会话，避免在文件内记录自引用 digest。

## 7. 旧 gate freshness 与 Phase 2 交接

本轮 runtime/test/handoff delta 使此前绑定旧 working tree 的 Phase 2、task commit、Branch
Review、publication review、immutable closeout plan 与 finalization gate 自然 stale。当前
真实 checker 已越过原 publication-stale root cause，随后对旧 evidence 报告 plan/current
facts/route `plan_ref` mismatch 是预期 fail-closed，不应放宽、修补或复用旧 confirmation。

Fresh `trellis-check` 应重点复核：

- recorder 写入 exact gate 后，prepared checker 正常 re-entry；
- arbitrary/unowned metadata 仍 fail closed；
- `require_plan=False` 只用于 plan 尚未 materialize 的 exact gate-only path；
- gate 缺失时 generic publication checker 行为不变；
- public Interface 1.3、六 exits、private-state boundary 与 production eval 无变化；
- canonical/dogfood parity、package graph、preset/ownership/sidecar/no-diff 证据 current；
- Docs SSOT `ssot_first` 与 `no_docs_update_needed` 判定成立；
- #119 global integration、#132 overlay cleanup 与 #105 transaction semantics 未进入 diff。

## 8. 副作用与剩余风险

未 commit、push、创建/更新 PR、archive、draft-to-ready、修改 Issue、deploy、production
write、tag/release、修改全局 npm 或 `node_modules`。Preset 验证只在本 worktree 与测试临时
repo 执行；最终 extension manifest 与 sidecar 均无遗留 delta。

本实现范围内未发现 remaining correctness blocker。剩余工作是由主会话按 owner workflow
重新完成 Phase 2、task commit、独立 review、publication review 与新的 exact closeout
confirmation；实现代理不得自行执行这些门禁。
