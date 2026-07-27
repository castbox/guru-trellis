# #118 Branch Review 第 2 轮问题发现审查原始报告

## 检查完成

### 审查身份与目的

- Logical role：`问题发现审查代理`
- 技术 `agent_id`：`/root/issue118_branch_review_final`
- 审查轮次：`round-002-problem-discovery`
- 审查意图：`initial_review` 的 finding-owner binding；本轮不是 `问题闭环审查代理`、`最终放行审查代理`、实现代理或 Phase 2 检查代理。
- 唯一任务：复核并资格化 `F-FINAL-LEGACY-01`，把 candidate、scenario、requirement、scope、qualification、severity、owner round 与正常路径证据绑定到同一 committed HEAD。
- 结论：`implementation_required`。

### 完整分支背景

- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Reviewed HEAD：`5695f7aab15b5d40660b535948c11c0ef55300f5`。
- 完整审查范围：`origin/main...5695f7aab15b5d40660b535948c11c0ef55300f5`。
- 变更规模：459 files，48175 insertions，4791 deletions；单一 commit `5695f7a feat(workflow): #118 新增任务终结闭环`。
- 覆盖背景：planning approval、Phase 2 evidence、Docs SSOT、完整 committed diff、finalizer package/runtime/eval、preset/distribution/install/update 与部署/安全影响均沿用并复核同一 HEAD 的 Round 1 完整审查证据。
- 本轮范围目的：上述完整 diff 是 candidate qualification 的上下文和排他性检查边界；本轮不重新声明 final pass，只负责把唯一 current-scope finding 绑定到 owner round。
- Workspace boundary：expected workspace 与 actual repo root 均为指定 task worktree；source checkout clean；`suspicious_source_artifacts=[]`。

### Finding Owner Binding

#### Candidate

- Candidate ref：`C-FINAL-LEGACY-01`。
- Affected behavior：`guru-finalize-task` 接管由现有 #105 closeout engine 合法持久化的同月 partial closeout plan，并从 standalone active/partially-finalized 状态继续 recorder、checker 与 transition。
- Affected paths：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:27538`、`:27560`、`:27900`、`:30467`、`:31050`。
- Candidate fact：existing projection 分支原样复用旧 `move_paths`、`tracked_move_paths` 与 `untracked_archive_outputs`；`include_finalization_gate=True` 只在没有 existing projection 时加入 `task-finalization-gate.json`。

#### Scenario

- Scenario class：`normal_required_behavior`。
- 正常性说明：旧 #105 engine 正常生成和持久化同月 immutable partial plan；新 finalizer 正常读取该 plan；semantic recorder 正常写入自身合同要求的 private gate；transition checker 正常重建 objective state。该顺序不依赖手工篡改、伪造、恶意 actor、对抗性输入、并发、TOCTOU、lock、fault injection、crash consistency 或跨 OS 原子性。

#### Requirement

- `prd.md` R2：finalizer 必须复用现有 #105 closeout transaction engine，不得形成破坏既有恢复状态的第二套收尾事务。
- `prd.md` R11：standalone/recovery 路径必须覆盖 active、partially-finalized 与 archived 的合法恢复状态。
- `prd.md` AC8：中断 closeout 必须能通过同一 finalizer contract 恢复，而不是被新增 private artifact 自身阻断。
- `design.md`：standalone active/partial/archived recovery profile、immutable plan ownership、exact allowlist 与 finalizer-only augmentation 必须同时成立。
- Accepted-current issue requirement：Interface 1.3、target-owned re-entry authoring 与 #119/#132 ownership 边界均未排除同月 legacy partial plan takeover。

#### Scope

- Scope basis：Issue #118 current acceptance。该行为属于新增 `guru-finalize-task` package 对现有 closeout transaction 的兼容接管，不是 #119 的 global Finish-family integration，也不是 #132 的 upstream overlay cleanup。
- Scope ledger：#118 为 close issue；#115 保持 related；#119/#132 保持 follow-up。本 finding 不扩张或改写 ledger。
- Docs SSOT：批准策略为 `ssot_first`；durable contract 已声明 #105 transaction compatibility 与 standalone partial-state recovery。当前实现未兑现该 current-scope 合同。

#### Qualification

- Qualification：`qualified_finding`。
- Qualification reason：正常支持路径可稳定重现 contract violation；通过项只覆盖 fresh finalizer plan，没有覆盖 legacy partial plan -> finalizer takeover 的状态迁移，因此无法反证 candidate。
- Rejected-candidate 判定：不适用。当前代码与独立 probe 都确认 violation 存在。
- Scope-proposal 判定：不适用。该行为已有明确 requirement 与 accepted-current scope，不需要额外 scope confirmation。

#### Severity And Ownership

- Finding ref：`F-FINAL-LEGACY-01`。
- Severity：`P1`。
- Severity reason：合法 partial closeout 在 semantic review/confirmation 和 recorder 写 gate 后无法进入 checker/transition，阻断 finalizer standalone recovery 主流程；这不是降级、提示或边缘输出差异。
- Owner round：`round-002-problem-discovery`。
- Reviewed HEAD：`5695f7aab15b5d40660b535948c11c0ef55300f5`。
- Status：`open`。
- Required consumer：返回 implementation / Phase 2 修复；修复后必须完成 fresh Phase 2、task commit、finding closure round 与新的 fresh final review。

### 正常路径复现

1. 使用仓库现有 `CloseoutTransactionContractTest` fixture，以 `include_finalization_gate=False` 调用现有 #105 engine，生成并持久化合法同月 `closeout-plan.json`。
2. 由新 finalizer 以 `include_finalization_gate=True` 重建同一 plan。因为存在 `projection`，代码不会把新 gate 加入 `move_paths` 或 `untracked_archive_outputs`。
3. 该步实际输出：

   ```text
   {'same_digest': True,
    'gate_in_move_paths': False,
    'legacy_untracked_outputs': ['finish-summary.json'],
    'resumed_untracked_outputs': ['finish-summary.json']}
   ```

4. semantic recorder 按 `guru-finalize-task` 合同正常写入 `task-finalization-gate.json`。
5. transition 通过 `check_finalization_gate_result()` 重建 finalization context；`build_closeout_plan()` 在 `observed_task_files - move_paths` 中发现 recorder 自己写入的 gate。
6. 该步实际输出：

   ```text
   {'blocked': True,
    'message': 'Persisted closeout plan does not own newly added task artifacts.',
    'unexpected_task_files': ['task-finalization-gate.json']}
   ```

7. 即使跳过该 rebuild，`commit_closeout_evidence_metadata(..., finalizer_mode=True)` 的 exact dirty-path allowlist 同样不拥有 gate，仍会阻断 evidence commit。

### 修复与闭环要求

- 为 existing projection 增加 deterministic、plan-bound 的 finalizer takeover/migration，使 `task-finalization-gate.json` 被 plan ownership、dirty staging、evidence commit 与 archive move 一致拥有。
- 不得放宽 generic #105 unexpected-artifact fail-closed；除 exact finalizer-owned gate 外的新增 artifact 必须继续阻断。
- 增加同月 legacy partial plan 的 preview -> recorder -> checker -> transition 生产级回归，并保留 negative control。
- 修复属于 implementation/Phase 2，不由本问题发现审查代理执行。

### 其它 Candidate

- 其它 current-scope candidate：无。
- actual-exit-first eval、六 exit schema/consumer projection、terminal published materialization、archive locator、repo identity、legal resume state、source/installed distribution 与 throwaway install/update 均已有通过证据，未发现第二个 current-scope violation。
- #119 global integration、#132 overlay cleanup 以及 hostile/concurrency/TOCTOU 扩张均为明确排除项，不得提升为本轮 finding。

### 已检查文件

- `reviews/round-001-final-release.md` 与 current `review.md`：只读，用于确认 finding provenance、完整 diff 背景和当前 open 状态。
- `prd.md`、`design.md`、`implement.md`、planning approval、Phase 2 evidence、issue scope ledger、implementation handoff 与 durable Docs SSOT：同一 HEAD 的既有完整证据已复核。
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`：复核 existing projection ownership、finalizer preview/checker、evidence commit 与 published transition 调用链。
- 完整 `origin/main...HEAD`：沿用 Round 1 对 459 paths 的背景审查，以确认 candidate 属于 current scope 且不存在第二个 current-scope candidate。

### 已修复问题

- 无。本轮是问题发现与 owner binding，不是实现或闭环轮次。

### 未修复问题

- `F-FINAL-LEGACY-01`：open P1，交回 implementation / Phase 2。

### 验证结果

- Normal-path reproduction：通过；在 exact reviewed HEAD 上稳定得到 `unexpected_task_files=['task-finalization-gate.json']`。
- 既有 fresh validation：runtime 611 passed/13 skipped、Skill packages 178 passed、preset 45 passed、finalizer package 4 passed、installed shared eval 8/8 passed、fresh throwaway exit 0。
- 覆盖判断：上述通过项没有 legacy partial plan takeover 用例，因此不关闭或降级本 finding。
- Lint/TypeCheck：本轮未重跑；Round 1 同一 HEAD 的 `git diff --check`、Bash syntax、Python compile 均通过，仓库无独立 configured type checker。

### 操作边界

- 未修改 implementation、docs、spec、code、schema 或 tests。
- 未修改 `reviews/round-001-final-release.md`、`review.md`、`agent-assignment.json`、`task-commit-plans/001.json` 或 `.trellis/.runtime/guru-team/**` inputs。
- 未调用 `review-branch.sh`、`check-review-gate.sh`、任何 `record-*`、Phase 2 recorder/checker 或其它 Guru Team gate recorder/validator。
- 未执行 commit、push、PR、GitHub mutation、archive、finish-work、deploy 或 production write。
- 本轮唯一写入为当前 `reviews/round-002-problem-discovery.md`。

### 证据交接

- Branch Review finding owner：`round-002-problem-discovery` 拥有 `F-FINAL-LEGACY-01` 的 qualification 与 severity binding。
- 完整范围：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c...5695f7aab15b5d40660b535948c11c0ef55300f5`，459 paths。
- Finding inventory：P0=0、P1=1、P2=0、P3=0；无其它 current-scope candidate 或 scope proposal。
- Typed route：`implementation_required`，finding refs 仅为 `F-FINAL-LEGACY-01`。
- 本报告是 problem-discovery raw evidence，不是 closure evidence 或 final-pass evidence。

### 结论

`C-FINAL-LEGACY-01` 属于 `normal_required_behavior`，由 R2/R11/AC8 与 standalone partial recovery 明确覆盖，已资格化并绑定为 open P1 `F-FINAL-LEGACY-01`。当前必须返回 implementation / Phase 2；在 fresh fix、Phase 2、task commit、closure 与 final review 完成前，Branch Review 不得通过。
