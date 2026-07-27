# Issue #118 Branch Review 第 12 轮问题发现审查原始报告

## 检查完成

### 审查身份与目的

- Logical role：`问题发现审查代理`。
- 技术 `agent_id`：`/root/issue118_branch_final_review_round11`。
- 审查轮次：`round-012-problem-discovery`。
- Reuse：同一 independent reviewer 从 Round 11 在完全相同的 HEAD/range 上切换 logical role，
  只为 Round 11 已资格化的两项 finding 建立正式 discovery-owner binding。
- 本轮不是 implementation、Phase 2、问题闭环审查或 fresh 最终放行审查；不重新执行完整
  branch review，也不复用 Round 11 的 final-release role 作为 closure/pass 身份。
- 结论：`implementation_required`。
- 唯一写入：
  `.trellis/tasks/07-26-118-guru-finalize-task/reviews/round-012-problem-discovery.md`。

### 完整分支背景与 Objective Identity

- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Reviewed HEAD：`77ad13f0a65f652e68e655afbe11917aa659df5c`。
- Exact range：
  `origin/main...77ad13f0a65f652e68e655afbe11917aa659df5c`。
- Diff 规模：526 paths，70807 insertions，4753 deletions。
- Workspace boundary：`status=ok`；expected workspace 与 actual repo root 相同；source checkout
  clean；`suspicious_source_artifacts=[]`。
- Round 11 source evidence：`reviews/round-011-final-release.md`，235 lines，15283 bytes，
  SHA-256 `bbd4d927574b69ea4d8d5deb6c2103e317a714e8db78f24b1a92a2193b2ff56f`。
- Round 11 已在同一 HEAD fresh 覆盖完整 diff、planning、Phase 2、Docs SSOT、runtime、packages、
  tests、eval、throwaway install/update、distribution、安全与部署影响。本轮复核其 digest 与
  objective identity 后复用终态验证，不重复运行高成本 suites。
- 写报告前 main-session-owned `agent-assignment.json`、`review.md`、executor-owned
  `task-commit-plans/005.json` result tail 与 Round 11 raw report 出现在 task-local working tree；
  它们未改变 committed HEAD，本 reviewer 未读取或修改 main-owned `review.md`。

### Finding Owner Binding 1

#### Candidate

- Candidate ref：`C-R11-VERIFICATION-METADATA-REENTRY-01`。
- Finding ref：`F-VERIFICATION-METADATA-REENTRY-01`。
- Affected behavior：#105/#118 content push 后，#117 workflow `verified` 或 reachable
  task-bearing standalone `not_required` 按合同写入 current task-local evidence，再由
  `guru-finalize-task` 重新进入同一 plan/ref/HEAD transaction并继续 PR/archive。
- Affected paths：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:14175-14212`：publication
    finalization-owned status allowlist 只接受 plan/gate。
  - 同文件 `:15269-15306`：finalization augmentation 构造 closed `finalization_paths`。
  - 同文件 `:26223-26374,26402-26410`：#117 recorder 写唯一 task-local
    `marketplace-verification.json`。
  - 同文件 `:30098-30143`：publication owner 在 plan/gate 存在时调用 augmentation。
  - 同文件 `:30588-30655,30847-30879`：eval staging 可提前返回，而真实 preview 先检查
    publication、后检查 verification owner。

#### Scenario

- Scenario class：`normal_required_behavior`。
- 正常性说明：finalizer 正常建立 immutable plan 并 content push；#117 正常执行 semantic
  review、recorder 与 checker，写入合同唯一 task-local artifact；#118 正常使用 public re-entry
  调用。该顺序不依赖手工篡改、伪造、恶意 actor、hostile input、并发、lock、TOCTOU、fault
  injection、crash consistency 或 cross-OS atomicity。

#### Current Requirement

- `prd.md` R6：#118 必须消费 #117 `verified` 与 `not_required` 的最小 current owner seed。
- `prd.md` R10：verification 必须位于 content push 后、PR/archive 前，finalizer 必须通过 #117
  owner checker 验证同一 plan/ref/HEAD evidence。
- `prd.md` AC3：producer projection 与 target authoring 必须 closed、最小、无 overwrite。
- `prd.md` AC6：current verified/not-required re-entry 只接受 same plan/ref/HEAD，并继续正常
  transaction。
- Approved design 与 current durable SSOT 同样要求 finalizer-only compatibility augmentation
  接受正常 #117 metadata tail；相关 current definitions 位于
  `.trellis/spec/workflow/workflow-contract.md:1045-1067`、
  `.trellis/spec/workflow/skill-package-contract.md:1532-1546,1564-1574`、
  `.trellis/spec/workflow/companion-scripts.md:1545-1550` 与 finalizer package contract
  `:34-49,78-85,119-136`。

#### Scope And Qualification

- Scope basis：Issue #118 current acceptance；该行为属于 active `guru-finalize-task` 对 #117
  owner evidence 的正常消费，不是 #119 global Finish integration 或 #132 overlay cleanup。
- Docs SSOT strategy=`ssot_first`；durable docs 已声明要求，当前 code/test 没有兑现，因此不是
  scope proposal或缺少首次 docs merge。
- Independent reproduction：plan、gate 与 verification 三个正常 status paths 进入 current
  allowlist 时得到：

  ```text
  unexpected_status_paths=['.trellis/tasks/07-26-118-guru-finalize-task/marketplace-verification.json']
  ```

- Real result：publication augmentation 在 verification owner checker 运行前失败，并被转换为
  `publication_review_stale`；workflow `verified` 与 reachable task-bearing standalone
  `not_required` 的正常 re-entry 都不可达。
- Eval limitation：source/installed shared 8/8 staged eval 通过，但
  `GURU_TEAM_EVAL_STAGING=1` 在 real publication owner checker 前返回 terminal facts，只证明
  wrapper/schema/distribution，不覆盖 recorder -> real preview edge。
- Qualification：`qualified_finding`。
- Qualification class：`normal_required_behavior`。
- Scope proposal：不适用；current approved requirement 已明确覆盖。

#### Severity And Ownership

- Severity：`P1`。
- Severity reason：R6/R10 主发布链在 content push 后稳定阻断，正常 finalization 无法继续；
  不是提示、日志或低影响边缘行为，也未发现数据破坏或安全边界突破，故不是 P0。
- `owner_round=12`。
- Owner report：`round-012-problem-discovery`。
- Owner agent：`/root/issue118_branch_final_review_round11`，从 Round 11 same-agent logical-role
  reuse。
- Reviewed HEAD：`77ad13f0a65f652e68e655afbe11917aa659df5c`。
- Source evidence：Round 11 SHA-256
  `bbd4d927574b69ea4d8d5deb6c2103e317a714e8db78f24b1a92a2193b2ff56f`。
- Status：`open`。
- Required consumer：返回 implementation / Phase 2；不得进入 publication、finalization 或
  Branch Review pass。

#### Required Closure

- 在不放宽 arbitrary metadata 的前提下，使 finalizer 精确识别并严格验证 current、
  plan-bound `marketplace-verification.json`，或以等价 owner-check 顺序建立相同 closed binding。
- 增加不使用 eval staging、实际通过 #117 recorder 写 task-local evidence 后调用 real #118
  wrapper 的 workflow `verified` 与 reachable standalone `not_required` regression。
- 保持 generic unexpected-metadata fail-closed、#117 semantic ownership、same plan/ref/HEAD、
  minimal public DTO 与 #119/#132 scope boundary。
- 修复后 fresh Phase 2、Docs SSOT reconciliation、task commit、finding closure 与 fresh final
  review必须由后续不同 logical/technical identities完成。

### Finding Owner Binding 2

#### Candidate

- Candidate ref：`C-R11-ROUND9-TRAILING-WHITESPACE-01`。
- Finding ref：`F-ROUND9-TRAILING-WHITESPACE-01`。
- Affected behavior：完整 committed range 必须通过 required Git diff hygiene/lint。
- Affected path：
  `.trellis/tasks/07-26-118-guru-finalize-task/reviews/round-009-finding-closure.md:203`。

#### Scenario

- Scenario class：`normal_required_behavior`。
- 正常性说明：reviewer 对完整 committed range 正常执行 `git diff --check` 即可稳定重现；不
  依赖 artifact 伪造、恶意输入、并发、TOCTOU 或其它排除场景。

#### Current Requirement

- Approved implementation/Phase 2/Branch Review validation strategy要求完整 diff lint/hygiene
  通过；仓库 review checklist 同样要求 lint 与 changed artifact 质量可验证。
- 该 path 属于 Issue #118 当前 committed diff，不是外部历史文件或 follow-up scope。

#### Scope And Qualification

- Fresh Round 11 command：

  ```text
  .trellis/tasks/07-26-118-guru-finalize-task/reviews/round-009-finding-closure.md:203: trailing whitespace.
  ```

- `git diff --check origin/main...77ad13f0a65f652e68e655afbe11917aa659df5c`
  terminal exit=`2`。
- Qualification：`qualified_finding`。
- Qualification class：`normal_required_behavior`。
- Scope proposal：不适用；required lint 与 current diff 已覆盖。

#### Severity And Ownership

- Severity：`P3`。
- Severity reason：不改变 runtime、data 或 security behavior，但使 required lint/hygiene
  失败，属于 current committed artifact 的机械质量缺陷。
- `owner_round=12`。
- Owner report：`round-012-problem-discovery`。
- Owner agent：`/root/issue118_branch_final_review_round11`，从 Round 11 same-agent logical-role
  reuse。
- Reviewed HEAD：`77ad13f0a65f652e68e655afbe11917aa659df5c`。
- Source evidence：Round 11 SHA-256
  `bbd4d927574b69ea4d8d5deb6c2103e317a714e8db78f24b1a92a2193b2ff56f`。
- Status：`open`。
- Required consumer：由 implementation/finding-fix owner 删除行尾空格，随 P1 修复一起进入
  fresh Phase 2 与 task commit。

#### Required Closure

- 精确删除 Round 9 line 203 行尾空格，不改写其历史 finding narrative。
- 重跑完整 `git diff --check origin/main...<new-head>` 并在 fresh Phase 2/closure evidence中记录。

### 其它 Candidate 与 Scope Boundary

- Gate-only exact-delta fix 保持 accepted：exact gate-only path 可重建 entry preconditions；
  `require_plan=true` 与 arbitrary unexpected metadata 仍 fail closed。P1 只要求消费合同已声明且
  owner-validated 的 #117 artifact。
- Main-owned assignment/review metadata、executor-owned task commit result tail、staged eval pass、
  Claude `401 Invalid API key` 与 unpushed exact feature ref均不是新增 source finding。
- #119 global integration、#132 overlay cleanup 与 hostile/forgery/concurrency/locks/TOCTOU/fault/
  crash/cross-OS 扩张保持 out of scope。
- Finding inventory：P0=0、P1=1、P2=0、P3=1；无额外 finding 或 scope proposal。

### 已检查文件

- `reviews/round-011-final-release.md`：只读并复核 SHA-256/bytes/lines，用于两项 finding 的
  candidate、requirement、qualification、severity、reproduction 与 verification provenance。
- `reviews/round-002-problem-discovery.md`、`round-008-problem-discovery.md`：只读，用于复核
  final-review finding 到 same-agent discovery-owner binding 的既有 lifecycle 模式。
- Current HEAD、workspace boundary、task-local working-tree identity：只读，用于确认 Round 12
  与 Round 11 完全相同的 committed candidate。
- `prd.md` R6/R10/AC3/AC6 与匹配 durable finalizer/workflow/runtime SSOT：沿用并复核 Round 11
  同 HEAD evidence，确认两个 findings 都属于 current requirements。

### 已修复问题

- 无。本轮是 finding discovery-owner binding，不是 implementation、Phase 2 或 closure。

### 未修复问题

- `F-VERIFICATION-METADATA-REENTRY-01`：open P1。
- `F-ROUND9-TRAILING-WHITESPACE-01`：open P3。

### 验证结果

- Objective identity：HEAD=`77ad13f0a65f652e68e655afbe11917aa659df5c`；boundary
  `status=ok`；source checkout clean；Round 11 digest/size/lines完全匹配。
- Reused Round 11 terminal validation：runtime 620 passed/13 skipped；skill packages 179 passed；
  preset/ownership 54 passed；finalizer+verifier 15 passed；focused publication/closeout 100 passed；
  source/installed shared eval 各 8/8；fresh throwaway terminal exit 0；source/installed validators、
  ownership、overlay drift、platform distribution与 protected/deploy-surface scans通过。
- Lint：失败；唯一 current failure 为
  `F-ROUND9-TRAILING-WHITESPACE-01`。
- TypeCheck：仓库无独立 configured static type checker；Round 11 changed Python AST/compile
  validation通过。
- Coverage judgment：通过的 focused/full tests 与 staged eval 未执行 normal #117 recorder ->
  real publication owner -> verification owner sequence，因此不关闭或降级 P1。
- 本轮按 unchanged HEAD owner-binding 约束未重跑高成本 suites。

### 操作边界

- 未修改 implementation、tests、planning、Phase 2、durable docs、spec、`review.md`、
  `review-gate.json`、assignment、commit plans、ledger、publication/finalization artifacts。
- 未调用 `review-branch.sh`、`check-review-gate.sh`、Guru Team recorder/validator 或任何
  `record-*`。
- 未执行 commit、push、PR、archive、Issue mutation、deploy 或 production write。
- 本轮唯一写入为 `reviews/round-012-problem-discovery.md`。

### 证据交接

- Round 12 正式拥有 `F-VERIFICATION-METADATA-REENTRY-01` 与
  `F-ROUND9-TRAILING-WHITESPACE-01` 的 qualification、severity、scope、requirements、
  `normal_required_behavior` 与 required-closure binding。
- Owner fields：两个 findings 均为 `owner_round=12`、owner agent
  `/root/issue118_branch_final_review_round11`、HEAD
  `77ad13f0a65f652e68e655afbe11917aa659df5c`、status=`open`。
- Provenance：Round 11 raw evidence SHA-256
  `bbd4d927574b69ea4d8d5deb6c2103e317a714e8db78f24b1a92a2193b2ff56f`。
- Exact range：
  `origin/main...77ad13f0a65f652e68e655afbe11917aa659df5c`，526 paths。
- Finding inventory：P0/P1/P2/P3=`0/1/0/1`；无 scope proposal。
- Typed route：`implementation_required`。
- Docs SSOT：strategy=`ssot_first`；P1 是 code/test 与 current durable SSOT 分歧，修复后必须
  fresh reconciliation。
- 本报告仅为 problem-discovery raw owner evidence，不是 finding closure、fresh final review 或
  Branch Review pass evidence。
- 后续 implementation/Phase 2、closure 与 fresh final review 必须由符合 lifecycle separation 的
  不同 identities执行；本 reviewer 不承担后续 closure/pass。

### 结论

Round 11 在同一 `77ad13f0` HEAD/range 上资格化的 P1
`F-VERIFICATION-METADATA-REENTRY-01` 与 P3
`F-ROUND9-TRAILING-WHITESPACE-01` 均属于 Issue #118 current
`normal_required_behavior`，现已由 Round 12 正式绑定 discovery owner、requirements、scope、
severity、source evidence、open status 与 required closure。

当前必须返回 implementation / Phase 2，typed route=`implementation_required`。本 Round 12
只提供 owner evidence；修复后的 finding closure 与 fresh final review 必须由不同 identities
完成。两项 finding 闭合前不得进入 publication、finalization、push/PR/archive 或 Issue closure。
