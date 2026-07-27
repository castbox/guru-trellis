# #118 Branch Review 第 1 轮最终放行审查原始报告

## 检查完成

### 审查身份与结论

- 审查角色：独立 `最终放行审查代理`
- 技术 `agent_id`：`/root/issue118_branch_review_final`
- 审查轮次：`round-001-final-release`
- 结论：`blocked`
- 问题数量：`1`（P0=`0`，P1=`1`，P2=`0`，P3=`0`）
- 门禁判断：当前报告不能作为 Branch Review Gate 的 pass evidence。`F-FINAL-LEGACY-01` 必须回到 Phase 2 修复、补充回归测试并形成新 commit，随后由新的完整 Branch Review 复验。

### 审查绑定

- GitHub issue：`castbox/guru-trellis#118`，现场复核状态为 `OPEN`。
- Accepted-current requirement：issue comment `#issuecomment-5045036678`，绑定 Interface 1.3、`exit_id`、target-owned reprepare seed、actual-exit-first eval，以及 #119/#132 的 ownership 边界。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Reviewed HEAD：`5695f7aab15b5d40660b535948c11c0ef55300f5`。
- 完整 diff：`origin/main...5695f7aab15b5d40660b535948c11c0ef55300f5`。
- 变更规模：459 files，48175 insertions，4791 deletions；单一 task commit `5695f7a feat(workflow): #118 新增任务终结闭环`。
- Workspace boundary：expected workspace 与 actual repo root 均为上述 task worktree；source checkout clean；`suspicious_source_artifacts=[]`。
- 审查开始前既有 dirty paths 仅为主会话维护的 `agent-assignment.json` 与 `task-commit-plans/001.json`，不属于 reviewed committed diff。本代理未修改它们。
- Assignment：现场验证 fresh final-release assignment `evt-0230-6e51bbda54` 绑定本代理、上述 exact HEAD 与最终放行意图；此前没有 Branch Review round。

### 问题清单

#### P0

无。

#### P1 `F-FINAL-LEGACY-01`：finalizer 无法接管由现有 #105 engine 生成的同月 partial closeout plan

- 位置：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:27538`、`:27560`、`:27900`、`:30467`、`:31050`。
- 合同：Issue #118 R2 要求复用现有 #105 closeout transaction，而不是破坏其已持久化恢复状态；R11、AC8 与 standalone `active/partially-finalized/archived` profile 要求合法的中断状态可以由 `guru-finalize-task` 接管并恢复。当前 accepted requirement 也没有把同月 legacy partial plan 排除在外。
- 正常路径前提：现有 #105 engine 在 finalizer package 激活前可以合法持久化同月 partial `closeout-plan.json`。该 plan 的 `projection.untracked_archive_outputs` 仅包含 `finish-summary.json`，`move_paths` 与 `evidence_paths` 均不知道后来新增的 `task-finalization-gate.json`。
- 实现行为：finalizer preview 在 active task 上设置 `include_finalization_gate=True` 并调用 `prepare_closeout()`。但 `build_closeout_plan()` 只在没有 `existing_projection` 时才把 `task-finalization-gate.json` 加入 `task_files` 与 `untracked_archive_outputs`；有旧 projection 时原样复用旧集合。semantic recorder 随后按新 Skill 合同正常写入 tracked `task-finalization-gate.json`。transition checker 再次重建 plan 时，`observed_task_files - move_paths` 立即把该 gate 判为未拥有的新 artifact 并 fail closed；即使绕过重建，`commit_closeout_evidence_metadata(..., finalizer_mode=True)` 的 exact dirty-path gate 也不会允许该路径。
- 独立复现：使用仓库现有 `CloseoutTransactionContractTest` fixture，先以 `include_finalization_gate=False` 生成并持久化合法 plan，再以 `True` 重建，得到：

  ```text
  {'same_digest': True,
   'gate_in_move_paths': False,
   'legacy_untracked_outputs': ['finish-summary.json'],
   'resumed_untracked_outputs': ['finish-summary.json']}
  ```

  随后模拟 semantic recorder 正常写入 `task-finalization-gate.json`，再次执行相同 finalizer rebuild，得到：

  ```text
  {'blocked': True,
   'message': 'Persisted closeout plan does not own newly added task artifacts.',
   'unexpected_task_files': ['task-finalization-gate.json']}
  ```

- 资格判定：`normal_required_behavior`。复现不依赖伪造、恶意篡改、对抗性输入、并发、TOCTOU 或 fault injection；它由旧版本正常持久化的 partial plan 与新 finalizer 正常 recorder 顺序直接触发。
- 影响：standalone finalization 不能恢复一类现有、合法、同月的 partial closeout state，用户会在已完成 semantic review/confirmation 并写入 gate 后被自身新增 artifact 阻断。该路径正是本 issue 引入 finalizer 后必须承接的 closeout compatibility/recovery 主流程，因此为 P1。
- 测试缺口：现有 full suite 覆盖了从一开始就以 `include_finalization_gate=True` 构建的 plan，但没有覆盖“先由兼容 #105 engine 生成 partial plan，再由 finalizer 接管并写 gate”的同月 takeover。全套测试与 8-case eval 因此均未触发该状态迁移。
- 修复要求：为 existing projection 定义 deterministic、plan-bound 的 finalizer takeover/migration 合同，使新 private gate 在不放宽其它 exact allowlist 的前提下被 plan ownership、dirty-path staging、evidence commit 与 archive move 一致拥有；保留 generic #105 strictness；新增同月 legacy partial plan takeover 的 preview -> recorder -> checker -> transition 回归，并验证既有 plan 的其它新增 artifact 仍 fail closed。
- 状态：`unresolved`。

#### P2

无。

#### P3

无。

### 已检查文件

- Planning/scope：`prd.md`、`design.md`、`implement.md`、planning approval、issue review、issue scope ledger、task metadata、implementation handoff Round 2/3、Phase 2 Round 2/3/4 reports 与 current `phase2-check.json`。
- Canonical package：`trellis/skills/guru-team/packages/guru-finalize-task/**`，包括 Skill、step-local contract、Interface 1.3、六个 input profiles、六个 typed exits、consumer/projection、两个 private artifacts、五个 wrapper、八个 eval cases 与 package tests。
- Runtime：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 中 finalizer public input、publication/verification owner augmentation、preview、route validation、private gate recorder/checker、transition executor、#105 plan/evidence/archive transaction 与 public invocation。
- Eval：`trellis/skills/guru-team/adapters/eval/native_adapter.py`、eval request/response schemas、production consumer schemas、actual-exit-first runner ordering与 production staging。
- Distribution：canonical/installed registry、extension manifest、preset installer/verifier、canonical 与 `.trellis/guru-team`、Agents、Codex、Claude、Cursor copies。
- Durable Docs SSOT：根/workflow/preset README；`.trellis/spec/workflow/**` 的 skill package、workflow、companion scripts 与 quality contracts；preset installer/upstream ownership 与 public docs。
- Explicit no-write scope：global workflow Markdown、upstream `trellis-finish-work` family、official `.trellis/scripts/task.py`、preset overlays、CI/CD、dependency、container、K8s/Helm、DB migration、Makefile 与 deploy assets。
- 官方 Trellis live docs：`index.md`、`advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md`。

### 已修复问题

- 无。Branch Review 模式禁止继续实现或首次合并 Docs SSOT，本代理没有修改 implementation、durable docs、spec、schema、tests、task planning artifacts 或 gate evidence。

### 未修复问题

- `F-FINAL-LEGACY-01` 未修复。该问题需要修改 closeout plan compatibility/recovery 语义并补测试，属于 Phase 2 实现返工，不是本轮可机械自修复项。

### 验证结果

- Lint：通过。`git diff --check origin/main...HEAD`、changed Bash syntax 与 Python compile 均 exit 0。
- TypeCheck：不适用。仓库没有独立 configured type checker；Python compile、JSON schema validator 与 unittest 为当前适用静态/合同检查。
- Tests：通过，但未覆盖上述 finding。
  - Runtime full：611 passed，13 skipped。
  - Skill package full：178 passed。
  - Preset full：45 passed。
  - Finalizer package：4 passed。
  - Installed shared real public wrapper eval：8/8 passed，六个 actual exits 均先按实际 `exit_id` 选择 schema，再比较 expected exit。
  - Source/installed package validation：13 active、0 planned、0 legacy；global markers 12 invokes / 46 exits / 27 targets；installed 2644 managed files、0 conflict/removal/sidecar。
  - Contract discovery：6 profiles、6 exits、2 private artifacts；eval discovery：8 cases、4 adapters。
  - Dogfood overlay drift、task artifact validation：通过。
  - Fresh clean throwaway：exit 0；覆盖 public marketplace discovery、local unpublished canonical workflow sample、initial install/reapply、official `trellis update`、managed hash、`.new/.bak` recovery、developer/no-developer fixtures、all-platform distribution、real wrappers/evals 与 installed closeout recovery。
- Finding reproduction：通过，稳定重现旧 plan 不拥有 finalization gate，且 recorder 写 gate 后 transition rebuild 被 `unexpected_task_files` 阻断。

### Planning 与 Phase 2 Evidence

- Planning approval 为 schema 2.0、`typed_exit=approved`，来源 `explicit-post-planning-review`；ambiguity/provenance/unusual-scenario review 与 fixed-scope scanner 均 passed，且当前 `prd.md`、`design.md`、`implement.md` digests 与 approval 绑定一致。
- 独立重算 digest 与记录一致：`prd.md=770e2752...`、`design.md=a9d8777a...`、`implement.md=d26bb613...`、planning approval `1bcc7712...`、Phase 2 `02b2142e...`、ledger `10495918...`、task `44c9c3c...`。
- Current Phase 2 artifact 为 schema 2.0、`typed_exit=passed`，Round 4 报告零 open findings；但本轮 fresh normal-path reproduction 证明 Phase 2 的 compatibility/recovery 覆盖不完整。该 evidence 对当前 committed HEAD 的 semantic pass 结论不足，必须在修复后重录。
- Scope ledger 仅关闭 #118；#115 为 related，#119/#132 为 follow-up。当前 finding 不改变该 ownership ledger，但在其关闭前不得进入 issue close。

### Docs SSOT

- 批准策略：`ssot_first`。
- Implementation handoff 记录 durable docs 已作为 primary input，task delta 已合并，task-history-only 内容保留在 task artifacts，并将 global Finish activation 与 overlay cleanup 分别留给 #119/#132。
- Durable docs、README 与 package inventory 对 active 13 Skills / 52 exits、global 12/46/27 markers、finalizer-only #117 augmentation、private gate、terminal public DTO materialization、archive locator、repo binding 与 legal resume states 的描述一致。
- 但 current code 不能承接 durable contract 声明的 existing #105 transaction compatibility 与 standalone partial-state recovery，构成 current-scope Docs SSOT/implementation 不一致。Branch Review 不在本轮首次修正文档或代码；应优先修实现并复核 durable wording，除非 Phase 2 发现合同本身需要经批准修订。

### 安全与部署影响

- 安全：新增 preset-managed runtime、schemas 与 platform package copies，扩大安装资产但没有引入 credential、token、private key、`.env`、签名 URL、客户数据或敏感原始记录。复现与 finding 不依赖 hostile-input security model。
- 部署：无 dependency、CI/CD、container、Compose、K8s/Helm/Kustomize、DB migration、Makefile、服务部署或 production data-write 变化。存在 extension/preset/package/schema/runtime 的安装与升级影响，fresh throwaway 已验证本地发布链路。
- 外部副作用：本轮未执行真实 GitHub draft PR create/ready、commit/push、issue mutation、archive、finish-work 或 production write；这些操作不在最终审查代理授权范围内。

### 观察项、后续候选与排除项

- 观察项：actual-exit-first eval、六 exit schema/consumer projection、terminal published materialization、archive locator、repo identity 与 legal resume states 均通过当前 tests/eval；未形成第二个 finding。
- 后续候选：修复 `F-FINAL-LEGACY-01` 时，应增加 legacy same-month partial plan takeover 的生产级回归，且测试需证明 generic unexpected artifact 仍被拒绝；该测试属于 finding closure，不是独立 follow-up issue。
- 排除项：#119 的 global Finish-family invocation/order 与 #132 的 upstream overlay cleanup 明确不属于 #118 current scope，未提升为 finding。
- 排除项：仅通过手工篡改 artifact/hash/state、恶意伪造、对抗输入、并发竞态或非常规 fault injection 才能成立的候选均为 `out_of_scope`；本报告没有用这些场景支撑 severity。

### 证据交接

- Branch Review：已覆盖完整 `origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c...5695f7aab15b5d40660b535948c11c0ef55300f5` committed diff、459 paths、planning/Phase 2/Docs SSOT、package/runtime/eval/distribution/install/update 与安全/部署影响。
- Finding：一个 open P1，ref=`F-FINAL-LEGACY-01`；P0/P2/P3 均为 0。没有未定级 current-scope candidate。
- Gate：本报告可作为 Branch Review Gate 的 blocking evidence，不可作为 pass evidence。Consumer 必须路由回 task implementation/Phase 2；修复 commit、fresh Phase 2 与新的独立 Branch Review 缺一不可。
- Docs SSOT：`ssot_first` 的 durable docs/task artifacts 基本完整，但实现与 current partial-state recovery contract 不一致；禁止在未修复前宣称 reconciliation 完成。
- 部署/安全：无服务部署或生产写影响；有 extension/preset 安装与 upgrade/update 影响，local clean throwaway 已验证；未发现敏感信息泄漏。

### 结论

完整 committed diff 存在一个可由受支持正常恢复路径稳定复现的 P1。Issue #118 的 finalizer package 在 fresh path 工作，但无法接管现有 #105 engine 已合法持久化的同月 partial closeout plan；因此 R2/R11/AC8 与 standalone recovery 尚未闭环。当前 Branch Review 必须 fail closed，禁止进入 pass、finish-work、push、PR ready 或 issue close。
