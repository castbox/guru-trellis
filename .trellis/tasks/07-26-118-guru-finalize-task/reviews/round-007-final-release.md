# Issue #118 Branch Review 第 7 轮最终放行审查原始报告

## 检查完成

### 审查身份与独立性

- 逻辑角色：全新独立“最终放行审查代理”。
- 技术 `agent_id`：`/root/issue118_branch_review_round7`。
- 审查轮次：`round-007-final-release`。
- 审查意图：`fresh_final_review`。
- Assignment：`evt-0284-a5fb06eeae` 把本代理绑定到
  `925007cb6f9b8101360db8fb93f92ef6b35a5b77` 的完整 Branch Review 和本报告唯一写入权限。
- 独立性：本代理未参与 Issue #118 implementation、Phase 2、task commit、Round 1/2 finding
  discovery、历史 finding 修复或 Round 3-6 closure/final review。
- 本代理未调用 `review-branch.sh`、`check-review-gate.sh`、Branch Review recorder/checker 或
  `record-*`；未修改 implementation、planning、durable docs、spec、runtime、schema、config、
  installer、tests、`review.md` 或 `review-gate.json`。唯一写入是本 raw report。

### 完整审查范围

- Worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Reviewed HEAD：`925007cb6f9b8101360db8fb93f92ef6b35a5b77`。
- Exact range：
  `7820a9eeec2a2a75fb52fba156a7211d9f9fb09c...925007cb6f9b8101360db8fb93f92ef6b35a5b77`。
- Diff 规模：476 paths，59242 insertions，4879 deletions。审查覆盖从 base 到 HEAD 的完整
  committed range，不限于 `925007c` 的 task-local metadata tail。
- Commit graph：`7820a9e -> 5695f7a -> 4847bfb -> 925007c`；commit plan 003 的 parent、
  commit、committed paths 与 expected/actual tree 均匹配。
- Workspace boundary：expected workspace 与 actual repo root 都是上述 issue #118 worktree；
  source checkout 与 task worktree 状态符合 validator 报告，`suspicious_source_artifacts=[]`。
- 审查期间仅主会话维护的 `agent-assignment.json`、`task-commit-plans/003.json` 为 dirty；本代理
  未触碰或覆盖它们。

### Lifecycle、Planning、Scope、Commit 与 Phase 2 Evidence

- Planning approval 为 schema 2.0、`typed_exit=approved`，包含 passed semantic、provenance、
  ambiguity 与 unusual-scenario review；fixed-scope scanner 无 unchecked normative hit；
  `prd.md`、`design.md`、`implement.md` 的 approved digests 保持 current。
- Scope ledger 只把 #118 列入 `close_issues`；#81/#115 为 `related_issues`，#119/#132 为
  `followup_issues`。本分支不关闭或承接 #81/#115/#119/#132。
- Current `phase2-check.json` 为 schema 2.0、`typed_exit=passed`，记录 Round 5 fresh full-scope
  check、`ssot_first` reconciliation、task delta merge、implementation handoff、validation matrix
  与当时零 open P0-P3。
- Round 1/2 的历史 P1 `F-FINAL-LEGACY-01` 已由 `4847bfb` 修复，Round 5 direct
  `new-agent` closure relations 完整，Round 6 是 `4847bfb` 的独立 zero-finding final review。
- `925007c` 随后固化 stable handoff、Phase 2、Round 3-6、scope、publication candidates 与 commit
  evidence，使 Round 6 成为历史证据；本 Round 7 对新 HEAD 重新执行 qualification-first review。

### Qualification 与 Findings

#### `F-NOT-REQUIRED-EDGE-01`，P1，`implementation_required`

- Candidate：`C-R7-NOTREQ-02`。
- Scenario class：`normal_required_behavior`。
- Requirement basis：`prd.md` R5、R6、R10、AC3，以及 active package/durable contracts 对
  `verification_not_required` re-entry、standalone finalization 与完整 task closeout loop 的声明。
- 正常触发：对不包含 installable extension surface 的 task 执行 standalone finalization。现有 plan
  builder 会合法产生 `marketplace.required=false`；该场景不需要伪造 artifact、恶意输入、并发、
  crash、TOCTOU 或未授权 mutation。
- Producer violation：#117 workflow mode 在
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:18970` 明确拒绝
  `not_required`，错误为 `workflow verification_required cannot silently exit not_required.`。
  #117 standalone `not_required` output schema 只发布
  `repo_ref/resolved_head/verification_ref`，不含 finalizer
  `verification_not_required` profile 必需的 `task_ref/plan_ref/reviewed_head`。因此不存在正常的
  producer -> projection -> consumer edge。
- Finalizer violation：当 `marketplace.required=false` 时，
  `guru_team_trellis.py:30954` 拒绝 `verification_required`；在没有 current same-plan #117
  `verified|not_required` evidence 时，`guru_team_trellis.py:30995` 又拒绝进入 archive 前的
  `published`。`reprepare_required` 与当前 state 不兼容，`resume_finalization` 只产生 self re-entry，
  不能形成 terminal closeout。
- 确定性 route probe 对同一正常 `marketplace.required=false`、`evidence_pushed` facts 的结果：

```json
{
  "published": "blocked: published requires current same-plan verification owner evidence before archive.",
  "reprepare_required": "blocked: reprepare_required is not compatible with the current transaction state.",
  "resume_finalization": "accepted",
  "verification_required": "blocked: verification_required is not compatible with the completed plan transition."
}
```

- Test gap：现有 `not-required-reentry-published` installed real-wrapper eval 不能反证该问题。
  `trellis/skills/guru-team/adapters/eval/native_adapter.py:2737` 直接选定 terminal `published`、
  `ready` 与 `marketplace_required=false`，并在 `:2808` 直接注入 verification ref/context；它没有
  执行 #117 producer、projection 或从正常 active task 推进该 edge。
- Observable impact：所有 `marketplace.required=false` 的正常 standalone task closeout 都无法通过
  package 声明的完整闭环到达 `published`，只能 blocked 或非终态自循环。影响核心用户工作流，
  但可在本地代码/合同/测试范围内修复，未观察到数据破坏或安全边界突破，因此 severity 为 P1。
- Required closure：实现者必须统一 #117 producer contract 与 finalizer consumer contract，为
  non-extension task 提供可达、same-plan、current 的 terminal path；同时补充真正执行
  producer -> projection -> finalizer 的正常 standalone regression，并同步当前 durable Docs SSOT。

#### `C-R7-PRECONDITION-01`

- Candidate concern：step-local contract 的 publication precondition 文案可被宽泛解读为缺失任何
  publication evidence 都应在入口阶段直接阻断。
- Current code path：runtime 明确保留 missing/stale owner fact，并允许 AI 选择
  `publication_review_stale`，与 durable contract 的 active recovery 语义一致。
- Qualification：`rejected_candidate`。未证明受支持正常路径违反批准需求，不附 severity、
  `finding_ref` 或 finding-only closure 字段。

#### Current inventory

- Qualified findings：1。
- Scope proposals：0。
- P0=`0`，P1=`1`，P2=`0`，P3=`0`。
- 历史 `F-FINAL-LEGACY-01` 保持 closed；本轮没有重新打开它。
- #119 global Finish-family invocation/order/combined acceptance 与 #132 upstream overlay cleanup
  保持 `out_of_scope`；本 finding 位于 #118 已声明 active 的 standalone finalizer/package edge，
  不是把 #119 或 #132 拉回当前范围。
- 恶意 actor、artifact/hash/state 伪造、hostile input、并发 finalizer、锁、TOCTOU、额外 fault
  injection、偶发 crash consistency 与 cross-OS atomicity 均未用于资格化本 finding。

### 已检查文件

- Planning/scope：`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、
  `issue-scope-ledger.json`、`task.json`、implementation handoffs、Phase 2 artifacts 与 task commit
  plans 001/002/003。
- Branch Review lifecycle：`reviews/round-001-final-release.md` 至
  `round-006-final-release.md`、`agent-assignment.json`、`review.md`、`review-gate.json`。
- Canonical package：`trellis/skills/guru-team/packages/guru-finalize-task/**` 与
  `guru-verify-extension-installation/**`，包括 Skill、contract、Interface 1.3 profiles、schemas、
  examples、projections、private artifacts、wrappers、eval cases 与 package tests。
- Runtime：canonical 与 dogfood `guru_team_trellis.py` 的 finalizer preview、plan builder、private
  gate、route validation、transition executor、#117 recorder/checker/projection、#105 transaction
  engine、recovery、archive与 terminal DTO materialization。
- Eval/tests：finalizer native adapter、installed shared real-wrapper corpus、runtime route/transaction
  tests、finalizer/verifier package tests、source/installed discovery 与四平台 protocol tests。
- Distribution：canonical/installed registry、extension manifest、preset installer/verifier、managed
  hashes、canonical/dogfood/Agents/Codex/Claude/Cursor package copies与 executable wrappers。
- Durable Docs SSOT：finalizer/verifier step-local contracts；`.trellis/spec/workflow/skill-package-contract.md`、
  `workflow-contract.md`、`companion-scripts.md`、`quality-guidelines.md`；preset ownership/installer、
  repository/workflow/preset README 与 public docs。
- Explicit no-write scope：canonical/dogfood global workflow、upstream `trellis-finish-work` family、
  official `.trellis/scripts/task.py`、preset overlays、dependency/CI/CD/container/Compose/Kubernetes/
  Helm/Kustomize/DB migration/Makefile/deploy surfaces。

### 已修复问题

- 无。Branch Review 模式禁止继续 implementation 或首次 Docs SSOT merge；本 finding 不是可由
  reviewer 机械修复的小问题。

### 未修复问题

- `F-NOT-REQUIRED-EDGE-01` 保持 open，route 为 `implementation_required`。它需要实现者决定并
  落实 #117 producer 与 finalizer consumer 的一致合同、runtime path、真实跨 owner eval 和 durable
  docs 同步；本 reviewer 不越权修改。
- 真实 GitHub Draft PR、archive commit/push、three-way remote/PR HEAD、draft-to-ready 与 Issue
  mutation 是后续 gated side effects；本轮 P1 未闭环前不得进入 publication/finalization。

### 验证结果

- Lint：通过。
  - `git diff --check 7820a9e...925007c`：exit 0。
  - 完整 diff 中 39 个 changed Bash 文件 `bash -n`：通过。
  - 17 个 changed Python 文件 AST parse：通过。
  - Canonical/dogfood runtime、finalizer/verifier packages 与 Agents/Codex/Claude/Cursor copies 的
    byte/mode equality：通过。
  - Full-range deploy/dependency/CI/container/migration/Makefile query：zero-hit。
- TypeCheck：不适用。仓库没有独立 configured type checker；Python AST、schema/contract validators
  与 unittest 是当前适用静态/合同检查。
- Tests：通过，但这些 green tests 不覆盖已资格化的 producer edge。
  - Runtime full suite：615 passed，13 skipped。
  - Skill package full suite：178/178 passed，388.876s。
  - Preset suite：54/54 passed。
  - Finalizer package：4/4 passed；verifier package：9/9 passed。
  - Focused finalizer edge tests：4/4 passed。
  - Installed shared finalizer real-wrapper eval：8/8 passed；其中 not-required case 存在上述
    producer bypass。
  - Source/installed package validation：passed；13 active，global markers 12 invokes / 46 exits /
    27 targets。
  - Installed inventory：2644 managed files，0 sidecar/conflict/removal；overlay drift、ownership、
    canonical/dogfood/platform package identity、runtime identity 与 wrapper executable checks 通过。
  - Upstream Finish、global workflow、official `task.py`、preset overlays no-write checks：通过。

### Docs SSOT

- Approved strategy：`ssot_first`。
- Initial implementation handoff 声明 durable docs 已拥有 active finalizer、六 profiles/六 exits、
  #117 verification re-entry、standalone finalization、完整 closeout loop、task delta merge 与
  #119/#132 boundary。
- Current durable docs 同时声明：
  - #117 workflow-required invocation 不能选择 `not_required`；
  - #117 `not_required` 的唯一 active consumer 是 `guru-finalize-task`；
  - finalizer 消费 workflow-shaped `not_required` seed，并拥有完整 standalone closeout loop。
- 代码与 schema 又只允许 #117 standalone `not_required` 输出无 task/plan identity 的 standalone
  DTO。上述三项无法同时成立，且正常 non-extension standalone closeout 已由 probe 证明无法
  terminal completion。因此最终 diff 上的 `ssot_first` reconciliation / no-update judgment 不再
  成立，存在 current-scope Docs SSOT inconsistency。
- Finding 修复必须先同步 durable docs 与 package contracts，再由新的 Phase 2 check 复核 code、
  schema、projection、eval、installed copies 与 task handoff；本 reviewer 不执行首次 docs merge。

### 安全、部署、安装升级与 Scope 边界

- 安全：完整 diff 与 task evidence 未发现 credential、token、private key、`.env`、signed URL、
  database URL、客户数据或敏感原始 payload 泄漏。Public DTO/private evidence 分层未发现独立
  security finding。
- 部署：没有 dependency、CI/CD、container、Compose、Kubernetes、Helm/Kustomize、DB
  migration、Makefile、服务部署或 production data-write 变化。
- 安装/升级：#118 有 additive Skill/package/schema/runtime/preset distribution 影响；当前
  source/installed validation、2644-file managed inventory、canonical/platform identity、overlay
  drift 与既有 clean install/update/reapply evidence均通过。`F-NOT-REQUIRED-EDGE-01` 是安装后
  仍存在的 semantic/runtime edge 缺口，不能由 distribution checks 抵消。
- #105：本 finding 不改变其 deterministic transaction engine 与历史 takeover fix；问题是
  finalizer 在正常 non-required verification edge 上无法到达该 engine 的 terminal archive path。
- #119：global Finish activation/order/combined acceptance仍由 #119 承担；本 finding 只要求 #118
  已承诺的 active package/standalone path内部自洽。
- #132：upstream overlay cleanup 保持 follow-up；本轮未修改或要求修改 upstream
  `trellis-finish-work` assets。
- Issue close recommendation：当前不关闭 #118；#81/#115 不关闭，#119/#132 保持 follow-up。

### 证据交接

- Branch Review：本报告 fresh 覆盖 exact
  `7820a9eeec2a2a75fb52fba156a7211d9f9fb09c...925007cb6f9b8101360db8fb93f92ef6b35a5b77`
  的 476-path 完整 committed range，reviewer 为 `/root/issue118_branch_review_round7`，intent 为
  `fresh_final_review`。
- Findings：`F-NOT-REQUIRED-EDGE-01` 是 current-scope P1、scenario
  `normal_required_behavior`、route `implementation_required`；P0=0、P1=1、P2=0、P3=0。
  `C-R7-PRECONDITION-01` 为 `rejected_candidate`。
- Test gap：installed `not-required-reentry-published` eval 直接注入 finalizer terminal context 与
  verification facts，没有执行 #117 producer/projection；8/8 green 不构成该 edge 的闭环证据。
- Docs SSOT：`ssot_first` 的 durable docs / task artifacts / code / schema / eval 在
  `not_required` reachability 上不一致；必须由 implementation owner 修复并重新执行 Docs merge、
  Phase 2、commit 与完整 Branch Review。
- 部署/安全：无服务部署、production write 或敏感信息泄漏 finding；存在 additive install/update
  surface，但 distribution checks 已通过。#105 不扩 scope，#119/#132 保持 follow-up。
- Gate 使用：本报告可作为 Round 7 raw semantic evidence供主会话记录
  `implementation_required`。它不能支持 `passed` Branch Review Gate，也不授权 push、PR、archive、
  finish-work、issue close、deploy 或 production write。
- AI recommendation：`implementation_required`。

### 结论

对
`7820a9eeec2a2a75fb52fba156a7211d9f9fb09c...925007cb6f9b8101360db8fb93f92ef6b35a5b77`
的 fresh final Branch Review 已完成。静态检查、全量 runtime/Skill/preset tests、package validators、
installed inventory、overlay/ownership 与 no-write checks 均通过，但它们没有覆盖 #117
`not_required` producer 到 finalizer 的真实 edge。

正常 non-extension standalone task 会产生 `marketplace.required=false`；#117 workflow mode 拒绝
`not_required`，#117 standalone DTO 又无法提供 finalizer 所需的 task/plan/HEAD seed，finalizer 同时
拒绝 `verification_required` 与无 owner evidence 的 `published`。该正常路径无法完成 closeout，
资格化为 P1 `F-NOT-REQUIRED-EDGE-01`。最终 AI recommendation 为
`implementation_required`；修复并重新完成 Docs SSOT、Phase 2、commit 与 fresh full-range Branch
Review 前，不得放行 #118。
