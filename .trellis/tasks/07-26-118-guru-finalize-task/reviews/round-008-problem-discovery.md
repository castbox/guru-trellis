# Issue #118 Branch Review 第 8 轮问题发现审查原始报告

## 检查完成

### 审查身份与目的

- Logical role：`问题发现审查代理`。
- 技术 `agent_id`：`/root/issue118_branch_review_round7`。
- 审查轮次：`round-008-problem-discovery`。
- Reuse：同一 independent reviewer 从 Round 7 `reuse`，在完全相同的 HEAD 与 range 上建立
  finding-owner binding；assignment 中的 `from_round=7`、`to_round=8`、`decision=reuse` 已记录。
- 审查意图：只对 Round 7 已资格化的 `F-NOT-REQUIRED-EDGE-01` 建立正式 finding owner
  evidence。本轮不是实现代理、Phase 2 检查代理、问题闭环审查代理或最终放行审查代理。
- 结论：`implementation_required`。

### 完整分支背景

- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Reviewed HEAD：`925007cb6f9b8101360db8fb93f92ef6b35a5b77`。
- Exact range：
  `7820a9eeec2a2a75fb52fba156a7211d9f9fb09c...925007cb6f9b8101360db8fb93f92ef6b35a5b77`。
- Diff 规模：476 paths，59242 insertions，4879 deletions。
- Round 7 raw evidence：`round-007-final-release.md`，251 lines，16731 bytes，SHA-256
  `c0bcafd48378f141fe51ecbcaa28d8ee32a26c6937235b95e54924af42c1007e`。
- 覆盖背景：Round 7 已 fresh 覆盖 planning、Phase 2、Docs SSOT、完整 committed diff、runtime、
  packages、schemas、eval、distribution、install/update、安全与部署影响。本轮沿用并复核该同
  HEAD 证据，只负责 finding qualification/ownership，不重复宣称 final review。
- Workspace boundary：expected workspace 与 actual repo root 都是上述 task worktree；source
  checkout clean，`suspicious_source_artifacts=[]`。

### Finding Owner Binding

#### Candidate

- Candidate ref：`C-R7-NOTREQ-02`。
- Finding ref：`F-NOT-REQUIRED-EDGE-01`。
- Affected behavior：不包含 installable extension surface 的正常 task 在
  `marketplace.required=false` 时，通过 standalone `guru-finalize-task` 完成 publication、
  verification decision、evidence、draft、archive 与 terminal `published` closeout。
- Affected paths：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18970`：#117 workflow
    invocation 拒绝 `not_required`。
  - `trellis/skills/guru-team/packages/guru-verify-extension-installation/schemas/public-not-required-output.schema.json:17`：
    standalone branch 只发布 `repo_ref/resolved_head/verification_ref`。
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:30954`：
    `marketplace.required=false` 拒绝 `verification_required`。
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:30995`：缺少 current
    same-plan #117 evidence 时拒绝 archive 前 `published`。
  - `trellis/skills/guru-team/adapters/eval/native_adapter.py:2737`、`:2808`：现有
    not-required eval 直接注入 terminal transaction/context 与 verification facts，未执行 producer。

#### Scenario

- Scenario class：`normal_required_behavior`。
- 正常性说明：finalizer 对普通非 extension task 正常生成
  `marketplace.required=false` plan，并推进到正常 `evidence_pushed` state。AI/recorder/checker、
  #117 与 #118 均按公开合同正常调用；该路径不依赖手工篡改、伪造、恶意 actor、hostile input、
  并发、TOCTOU、lock、fault injection、crash consistency 或 cross-OS atomicity。

#### Requirement

- `prd.md` R5：六个 closed profiles 明确包括 `not_required` re-entry 与 standalone
  finalization。
- `prd.md` R6：#118 必须消费 #117
  `not_required(exit_id,task_ref,plan_ref,reviewed_head)` 的最小业务 seed，且 target authoring
  与 producer seed 互斥、完整、无 runtime 合成。
- `prd.md` R10：finalizer 必须通过 #117 owner checker 消费同 plan/ref/HEAD 的 current
  verification decision，保持 verification 在 content push 后、PR/archive 前。
- `prd.md` AC3：#117 `verified|not_required` producer projection 与 #118 target profile 必须
  closed、无 missing/extra/overlap/overwrite。
- Approved design 与 active durable contracts：`verification_not_required`、standalone
  finalization 和完整 task closeout loop 都是 #118 current acceptance，不是 planned future behavior。

#### Scope

- Scope basis：Issue #118 current acceptance。该行为属于 active `guru-finalize-task` package
  内部的 #117 producer -> projection -> #118 consumer/standalone closeout edge。
- Scope ledger：只关闭 #118；#81/#115 保持 related，#119/#132 保持 follow-up。本 finding 不
  修改 ledger，也不承接 #119 global Finish-family invocation/order 或 #132 overlay cleanup。
- #105：本 finding 不改变已完成的 deterministic transaction engine 或历史 takeover fix；它只
  证明正常 non-required edge 无法到达该 engine 的 terminal archive path。
- Docs SSOT：approved strategy 为 `ssot_first`。Durable docs 同时声明 workflow
  `not_required` 不可产生、其唯一 active consumer 是 finalizer、finalizer 消费 workflow-shaped
  seed 并拥有完整 standalone loop；当前 code/schema 无法同时兑现这些声明。

#### Reproduction And Qualification

- #117 owner checker 对 workflow `not_required` 返回：
  `workflow verification_required cannot silently exit not_required.`。
- #117 standalone `not_required` output 不含 `task_ref/plan_ref/reviewed_head`，无法投影
  finalizer `verification_not_required` profile。
- 对同一正常 `marketplace.required=false`、`evidence_pushed` facts 的 Round 7 deterministic
  route probe：

```json
{
  "published": "blocked: published requires current same-plan verification owner evidence before archive.",
  "reprepare_required": "blocked: reprepare_required is not compatible with the current transaction state.",
  "resume_finalization": "accepted",
  "verification_required": "blocked: verification_required is not compatible with the completed plan transition."
}
```

- `resume_finalization` 只形成 same-plan self re-entry，不能补出不存在的 #117 producer evidence，
  因而不是 terminal closure route。
- Existing `not-required-reentry-published` eval 直接构造
  `transaction_state=ready`、`marketplace_required=false` 与 verification context；8/8 green 只证明
  注入后的 target wrapper behavior，未覆盖 producer -> projection -> finalizer edge。
- Qualification：`qualified_finding`。正常支持路径稳定违反 R5/R6/R10/AC3 与 active durable
  contract；passing tests 没有执行被破坏的 edge，不能反证 candidate。
- Scope-proposal：不适用。该行为已有 approved current requirement，无需额外 scope confirmation。

#### Severity And Ownership

- Severity：`P1`。
- Severity reason：所有 `marketplace.required=false` 的正常 standalone task closeout 都不能到达
  terminal `published`，而只能 blocked 或非终态 self re-entry，阻断 #118 声明的核心完整闭环。
  该问题可在 current code/contract/test 范围内修复，未发现数据破坏或安全边界突破，故不是 P0。
- Owner round：`round-008-problem-discovery`。
- Owner agent：`/root/issue118_branch_review_round7`，从 Round 7 same-agent `reuse`。
- Reviewed HEAD：`925007cb6f9b8101360db8fb93f92ef6b35a5b77`。
- Status：`open`。
- Required consumer：返回 implementation / Phase 2；不得进入 publication、finalization 或
  Branch Review pass。

### Required Closure

- 统一 #117 `not_required` producer contract 与 #118 finalizer consumer contract，为正常
  non-extension task 提供可达、same-plan、current 且 terminal 的 closeout path。
- 保持 public DTO 最小化、producer/target authoring partition、#117 semantic ownership 与 #118
  verification ordering；不得由 runtime 伪造 AI intent/context 或 owner evidence。
- 新增真正执行 #117 producer -> thin projection -> #118 finalizer 的正常 standalone regression；
  不得用 adapter 直接注入 terminal state/verification facts替代该 acceptance path。
- 按 `ssot_first` 同步 package contracts 与 durable workflow/package SSOT，消除
  `not_required` reachability 矛盾。
- 修复后必须完成 fresh Phase 2、task commit、由合格 closure reviewer 执行 finding closure，
  再由 fresh final reviewer 覆盖完整新 HEAD range。
- 修复属于 implementation/Phase 2，不由本问题发现审查代理执行。

### 其它 Candidate

- `C-R7-PRECONDITION-01` 保持 `rejected_candidate`：missing/stale publication owner facts 可以
  正常路由 `publication_review_stale`，未证明受支持路径违反 approved contract；不附 severity。
- 其它 current-scope candidate：无。
- 历史 `F-FINAL-LEGACY-01` 保持 closed；本轮不重新打开或改写其 owner/closure evidence。
- #119、#132 与 hostile/forgery/concurrency/locks/TOCTOU/fault/crash/cross-OS 扩张保持
  `out_of_scope`，不得提升为本轮 finding。
- Finding inventory：P0=0、P1=1、P2=0、P3=0；无 scope proposal。

### 已检查文件

- `reviews/round-001-final-release.md`、`round-002-problem-discovery.md`：只读，用于确认
  final-review finding 到 same-agent discovery-owner 的既有 reuse 模式。
- `reviews/round-007-final-release.md`、current `review.md`、`agent-assignment.json`：只读，用于
  绑定 Round 7 provenance、current open status、same HEAD 与 Round 7 -> 8 reuse decision。
- `prd.md`、`design.md`、`implement.md` 与匹配 workflow package/workflow durable contracts：
  复核 R5/R6/R10/AC3、scope 与 Docs SSOT basis。
- 完整 `origin/main...HEAD`：沿用 Round 7 对 476 paths 的 fresh full-range evidence，确认本轮只
  绑定唯一 finding，未出现额外 candidate。

### 已修复问题

- 无。本轮是问题发现与 owner binding，不是 implementation、Phase 2 或 closure。

### 未修复问题

- `F-NOT-REQUIRED-EDGE-01`：open P1，route=`implementation_required`。

### 验证结果

- Fresh binding：HEAD 仍为 `925007cb6f9b8101360db8fb93f92ef6b35a5b77`，Round 7 report digest/
  size/lines 与 assignment/current review 一致。
- Round 7 fresh validation：`git diff --check`、39 changed Bash syntax、17 changed Python AST、
  runtime 615 passed/13 skipped、Skill packages 178/178、preset 54/54、finalizer 4/4、verifier
  9/9、focused edge 4/4、installed eval 8/8、source/installed validators、2644-file inventory、
  overlay/ownership/platform identity/no-write checks均通过。
- Coverage judgment：上述通过项未执行 #117 `not_required` producer -> projection -> #118
  finalizer edge，因此不关闭或降级本 finding。
- Lint/TypeCheck/Tests：本轮按同 HEAD reuse 约束不重跑长测试；Round 7 同一 HEAD evidence current，
  仓库没有独立 configured type checker。

### 操作边界

- 未修改 implementation、planning、durable docs、spec、code、schema、tests、`review.md`、
  `review-gate.json`、`agent-assignment.json` 或 task commit plan。
- 未调用 `review-branch.sh`、`check-review-gate.sh`、任何 Branch Review/Guru recorder、validator
  或 `record-*`。
- 未执行 commit、push、PR、GitHub mutation、archive、finish-work、deploy 或 production write。
- 本轮唯一写入为 `reviews/round-008-problem-discovery.md`。

### 证据交接

- Branch Review finding owner：`round-008-problem-discovery` 正式拥有
  `F-NOT-REQUIRED-EDGE-01` 的 qualification、severity、scope 与 required-closure binding。
- Reuse relation：technical agent `/root/issue118_branch_review_round7` 从 Round 7 到 Round 8
  same-agent `reuse`；HEAD/range 完全相同，本轮不承担 implementation、closure 或 final pass。
- Exact range：
  `7820a9eeec2a2a75fb52fba156a7211d9f9fb09c...925007cb6f9b8101360db8fb93f92ef6b35a5b77`，
  476 paths。
- Finding inventory：P0=0、P1=1、P2=0、P3=0；finding ref 仅为
  `F-NOT-REQUIRED-EDGE-01`；`C-R7-PRECONDITION-01` 为 `rejected_candidate`；无额外 finding
  或 scope proposal。
- Typed route：`implementation_required`。
- Docs SSOT：当前 `ssot_first` reconciliation 在 `not_required` reachability 上不成立，必须随
  implementation 修复后由新 Phase 2 复核。
- 本报告是 problem-discovery raw owner evidence，不是 finding closure 或 final-pass evidence。

### 结论

`C-R7-NOTREQ-02` 属于 `normal_required_behavior`，由 R5/R6/R10/AC3 与 active standalone
finalization contract 明确覆盖，已正式绑定为 open P1 `F-NOT-REQUIRED-EDGE-01`。Round 8 owner
为 `/root/issue118_branch_review_round7`，以 same-agent `reuse` 从 Round 7 在同一
`925007cb` HEAD/range 上建立 lifecycle evidence；没有第二个 finding，
`C-R7-PRECONDITION-01` 保持 rejected。

当前必须返回 implementation / Phase 2。修复、Docs SSOT、fresh Phase 2、task commit、finding
closure 与 fresh final review 完成前，Branch Review 不得通过，也不得进入 publication 或
finalization。
