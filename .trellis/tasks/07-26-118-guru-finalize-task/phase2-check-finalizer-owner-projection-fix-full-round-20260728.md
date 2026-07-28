# Issue #118 finalizer owner evidence 兼容投影修复 Phase 2 全量检查

## 检查完成

### 检查身份与边界

- 角色：独立 Phase 2 `trellis-check` reviewer。
- Reviewer：`/root/issue118_phase2_owner_projection_fix_check`；未参与本轮
  implementation。
- Task：`.trellis/tasks/07-26-118-guru-finalize-task`。
- Worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task`。
- Branch：`feat/118-guru-finalize-task`。
- Base：`origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c`。
- Checked HEAD：`d7308d4aeaa3228d7650b93821ac7b4269ec5b38` 加 current working
  tree。
- Remote feature ref：
  `d7308d4aeaa3228d7650b93821ac7b4269ec5b38`；当前 runtime fix 尚未提交或
  push。
- Current implementation-owned delta：canonical/dogfood runtime、canonical runtime
  tests 与 task-local handoff 共 4 paths；runtime/test 为 509 insertions、16 deletions。
- Finding inventory：P0=`0`、P1=`0`、P2=`0`、P3=`0`。
- 建议 typed exit：assignment linkage 补录并 fresh validation 通过后为 `passed`，
  consumer=`skill:guru-create-task-commit`。

Workspace boundary 通过：expected workspace 与 actual repo root 均为上述 task
worktree；source checkout
`/Users/wumengye/Documents/GoProjects/guru-trellis` clean，
`suspicious_source_artifacts=[]`。Planning approval 在检查前通过：
`typed_exit=approved`、provenance=`explicit-post-planning-review`，
`ambiguity_review=passed`，fixed-scope scan passed，
`unchecked_normative_hits=[]`，批准的 `prd.md`、`design.md`、`implement.md`
content digests current。

`check.jsonl` 只有 seed row，因此按合同 fallback 读取完整 planning artifacts、
implementation handoff chain、finalizer/#105/#117 contracts、durable specs、完整 current
diff、task metadata 与 tests。Live authority 已复核：Issue #118 OPEN，accepted-current
comment 为 `5045036678`；#105 CLOSED，#115/#119/#132 OPEN；close scope 只有 #118，
#115 为 related，#119/#132 为 follow-up。

本 reviewer 未调用 Phase 2 recorder/checker semantic gate，未修改 implementation、tests、
durable docs、planning、ledger、review/publication/finalization artifact，也未 commit、stage、
push、创建或修改 PR、archive、Ready、merge、deploy、production write 或修改 Issue。本轮
tracked writes 只有本报告与同轮 command evidence JSON。

Assignment terminal linkage 当前未闭合：`agent-assignment.json` 对本 checker 只记录
`evt-0540-eb9ef2299a` assigned event，没有 completed event；文件中没有
`/root/issue118_finalizer_owner_projection_fix` agent/event，因此也没有其 completed event。
本 reviewer按合同不自行修改 assignment。主会话必须依据真实派发/完成事实，通过
`record-subagent-liveness-event.sh` 补录 implementation assigned/completed lineage与本 checker
completed event，再运行 fresh current-HEAD assignment/linkage validation；在此之前不得调用
Phase 2 recorder。

### 已检查文件

- Planning 与 authority：`prd.md`、`design.md`、`implement.md`、
  `planning-approval.json`、`issue-scope-ledger.json`、live Issue/comment 与 dependency
  Issue 状态。
- Current fix：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`、
  `.trellis/guru-team/scripts/python/guru_team_trellis.py`、
  `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`、
  `implementation-handoff-finalizer-owner-projection-fix.md`。
- Transaction 与 owner contracts：#105 closeout transaction、
  `guru-finalize-task` Interface/contract/private gate、#117
  `guru-verify-extension-installation` recorder/checker/execution inventory、#116
  publication producer edge。
- Active/archive recovery：finalizer task locator、exact augmentation、standalone
  `not_required` task/plan/HEAD/ref binding、archived committed plan/evidence recovery 与
  #117 local/remote HEAD drift rejection。
- Package/distribution：canonical、installed、shared、Agents、Codex、Claude、Cursor
  finalizer package copies；preset installer、extension manifest、source/installed package
  validators、ownership inventory、overlay drift 与 clean throwaway。
- Durable docs：finalizer package contract、`.trellis/spec/workflow/**`、
  `.trellis/spec/preset/**`、repository/workflow/preset README 与 approved Docs SSOT
  Plan。
- Protected surfaces：global workflow、upstream `trellis-finish-work`
  Skill/Command/Prompt、official `.trellis/scripts/task.py`、preset overlay、CI/CD、
  container、Kubernetes、DB migration、Terraform、Makefile 与 deploy paths。
- Lifecycle evidence：旧 `phase2-check.json`、Round 17 Branch Review、
  `review-gate.json`、`pr-readiness.json`、finalization checkpoint absence与 main-session
  metadata tail。

### 实现语义复核

原 normal-path defect 已复现并与 handoff 一致：#117 owner checker 接受 current
Interface 1.3 `verified` evidence 后，`cmd_execute_finalization_transition()` 仍把 owner
artifact 原样传入 #105 legacy `closeout_passed_marketplace_evidence()`。后者要求 schema
1.0 `status/verified_head/remote_head/steps/assets`，因此 remaining finalization 在 evidence
commit、Draft PR 与 archive 前被 `Cannot record invalid marketplace verification.`
阻断。

Current implementation 新增 finalizer-private deterministic compatibility projection：

1. 输入只能是 finalizer 已通过 owner checker 取得的 `(owner payload, checker result)`。
2. Checker 必须为 `status=ok`、`typed_exit=verified`、workflow mode，且
   `verification_ref`、owner digest 与可选 finalization plan ref 精确匹配。
3. Owner artifact path 必须是 non-symlink regular file，重读 JSON 必须等于 checked
   payload；task、immutable plan、repo、remote、branch ref、reviewed HEAD、remote HEAD 与
   `execution.status=passed` 必须全部 current。
4. `execution.commands` 只投影为 legacy `steps`；workflow 与三个 legacy schema digest
   只能从 checker-bound `asset_expectations` 各取唯一一项。
5. 投影必须继续通过未修改的
   `marketplace_verification_contract_errors()`；任何缺失、重复、类型错误或 binding drift
   都 exit 2。
6. 只有 `marketplace.required=true` 的 `published` transition 使用该 private
   compatibility payload；`not_required` 不制造 legacy verification evidence。
7. #105 ledger evidence 的 `artifact_sha256` 仍从真实 Interface 1.3 owner artifact path
   bytes 计算，不从临时 projection 计算。

五个 legacy boolean flag 没有形成未验证的放宽。既有 #105
`execute_marketplace_verification()` 本来就以同一 monolithic result 的 `passed` 值派生
`runtime_gitignore_present`、`workspace_gitignore_present`、
`session_auto_commit_false`、`legacy_handoff_absent`、
`legacy_intake_schema_absent`。Current #117 `verified` evidence 同时绑定：

- `execution.status=passed`；
- `verify_throwaway_installation` capability；
- 六条 capability command 与完整 stdout/stderr identity；
- 完整匹配的 installed asset expectation/digest inventory；
- workflow 与三个 schema 的 exact source path/digest；
- 同一 task、plan、repo、ref、reviewed HEAD 与 remote HEAD。

因此把五项 flag 设为 true 是对既有 #105 accepted executor 规则的兼容投影，不是仅依赖
`typed_exit=verified` 的空断言。实现没有修改 generic #117 checker/schema、#105
transaction order、public finalizer DTO/schema/exit、global workflow route、preset
inventory 或 #119/#132 ownership。

### Active/archive 与 stale gate 判断

六项 focused active/archive regression 全部通过，明确覆盖：

- Real `verified` owner recorder/checker 到 remaining finalization 的 `published`
  transition。
- Exact finalizer verification augmentation 只接受 plan-bound owner evidence。
- Standalone `not_required` owner 必须绑定 task、plan、HEAD 与 ref。
- Active-to-archive locator 只能采用 immutable plan 的 archive projection。
- Archived recovery 读取 committed plan 与 committed owner evidence。
- #117 checker 拒绝 local/remote HEAD drift。

旧 active `marketplace-verification.json`、`closeout-plan.json` 与
`task-finalization-gate.json` 当前均不存在；这是前序 stale-checkpoint cleanup 的预期结果。
本轮正向证明来自真实 recorder/checker test reconstruction，不复用已删除 artifact。

三项 downstream gate 均如预期 fail closed：

- 旧 Phase 2 exit 2：
  `phase2_check_agent_assignment_stale`、`phase2_check_head_stale`、
  `phase2_check_dirty_snapshot_stale`、`phase2_check_repository_snapshot_stale`。
- 旧 Branch Review exit 2：Phase 2、ledger、assignment 与 current implementation paths
  stale。
- 旧 publication readiness exit 2：Branch Review、Phase 2、assignment、repository 与
  current non-metadata implementation paths stale。

这些 expected nonzero 证明 current fix 正确重入 Phase 2；旧 Round 17、publication 与
finalization evidence 不得作为 current acceptance 使用。

### 已修复问题

- 文件：canonical/dogfood `guru_team_trellis.py` 与 canonical runtime tests。
- 问题：Current #117 Interface 1.3 owner artifact 通过 strict checker 后，remaining
  #105 engine 仍接收错误 payload shape，verified re-entry normal path 必然阻断。
- 修复：Implementation agent 增加 plan-bound private compatibility projection、real
  published transition regression 与 ledger owner-artifact identity assertions。
- Reviewer处理：本 reviewer 未修改 implementation；独立 semantic review、完整 runtime、
  focused positive/negative 与 #105 transaction matrix确认该 finding 已关闭。

本轮没有 reviewer self-fix，也没有 open current-scope finding。唯一初始
`package-parity` 非零来自 canonical test 运行生成的
`tests/__pycache__/test_contract.cpython-312.pyc`；精确删除该 cache 后，以
`--exclude=__pycache__ --exclude=*.pyc` 重跑六树 parity exit 0。它不是受管内容缺陷。

### 未修复问题

- Agent recovery gate 尚未闭合：implementation agent
  `/root/issue118_finalizer_owner_projection_fix` 的真实 assigned/completed lineage缺失，本
  checker completed event也尚未由主会话记录。该缺口不要求修改 implementation，但会阻塞正式
  `phase2-check.json` recorder；主会话补录后必须 fresh recheck。
- Current runtime fix 尚未 commit/push；remote feature ref仍为 `d7308d4...`。Pushed-ref
  marketplace verification 必须在 fresh commit/push 后由 #117 owner gate执行，本轮 clean
  throwaway不能替代该 future gate。
- Claude/Cursor external native availability不是本 runtime-only correction 的新增行为；
  本轮不把外部认证/unsupported 状态描述为 semantic pass。
- 完整 committed range 的 `git diff --check` 仍只命中
  `reviews/round-009-finding-closure.md:203` 的历史 raw report trailing whitespace。Current
  dirty diff check为 exit 0；该 assignment-bound historical observation不影响当前代码或
  contract，本轮不改写其字节。
- #119 继续拥有 global Finish-family integration 与 #115 closure；#132 继续拥有 upstream
  overlay cleanup。本轮不扩大范围。

以上均不是 open P0-P3 finding。

### 验证结果

- Lint：通过。Current `git diff --check`、changed JSON parse、Python compile、Bash
  syntax、source/installed package validators、ownership、overlay drift、protected/deploy
  path scan、sensitive material scan与 managed-tree cache/sidecar inventory均符合预期。
- TypeCheck：通过适用检查。仓库无 configured mypy/pyright/ruff gate；changed Python
  compile、closed schemas、package validators与完整 runtime tests提供适用覆盖。
- Runtime full：628 tests，13 skipped，exit 0。
- #105 `CloseoutTransactionContractTest`：106 tests，exit 0。
- Owner projection focused：6 tests，exit 0。
- Active/archive focused：6 tests，exit 0。
- Skill/package/eval graph：180 tests，exit 0。
- Finalizer + #116 + #117 package contracts：33 tests，exit 0。
- Preset installer：45 tests，exit 0。
- Upstream ownership：9 tests，exit 0。
- Four-platform focused protocol：5 tests，exit 0。
- Wrapper/actual-exit boundary：5 tests，exit 0。
- Source/installed shared real wrapper：各 8/8；覆盖六个 exits及
  `verified`/`not_required` re-entry。
- Source package validator：13 active、0 planned、0 legacy，workflow markers
  `12/46/27`。
- Installed package validator：2659 managed files，
  sidecar/removal/conflict=`0/0/0`。
- Ownership validator：frozen/active/overlay=`43/43/43`，
  facts SHA-256=`b99e67e59cb2e14679917bd31494f5ed32a87c72425f65b4fa41bd27470fc072`。
- Package parity：canonical、installed、shared、Codex、Claude、Cursor
  byte-identical；canonical/dogfood runtime一致。
- All-platform preset apply：exit 0；无 sidecar/conflict/removal。Apply只瞬时刷新
  installed manifest 的 `installed_at` 与 source commit provenance；两项已机械恢复，未留下
  manifest diff。
- Clean throwaway：exit 0；stdout明确输出
  `Verified throwaway Guru Team Trellis install`。覆盖 current local preset/runtime、
  remote unchanged workflow source、init、official update、workflow/preset reapply、
  no-developer project、installed eval、managed hashes、`.new/.bak` recovery、三平台
  distribution与 terminal validator。
- Official Trellis docs：`index.md`、`custom-workflow.md`、
  `custom-spec-template-marketplace.md` 均 live HTTP 200；current fix仍位于 canonical
  companion runtime/test，未修改 upstream source、global workflow或 spec marketplace
  content。
- Terminal hygiene：受管 source/package/platform trees 无 `.new`、`.bak`、`.pyc`；
  source checkout clean。

同轮 command evidence：
`.trellis/tasks/07-26-118-guru-finalize-task/phase2-command-evidence-finalizer-owner-projection-fix-full-round-20260728.json`。
它对可精确恢复的命令记录 exact argv；聚合 suite 明确使用 `suite_scope`，不把重建描述冒充
argv；每项记录 expected nonzero rationale、exit code与可用的 stdout/stderr SHA-256、字节数。
原始临时 streams 只用于生成该持久证据。

### 证据交接

- 阶段二：覆盖 planning/provenance、live authority、完整 current dirty scope、handoff、
  owner-check binding、private compatibility projection、真实 owner artifact ledger identity、
  active/archive recovery、runtime/#105/package/eval、distribution、Docs SSOT、安全/部署与
  terminal hygiene。P0/P1/P2/P3=`0/0/0/0`；implementation与verification adequacy passed，
  agent recovery pending。本报告与同轮 JSON在主会话补录真实 assignment completion lineage并
  fresh linkage validation通过后，可支撑 fresh `phase2-check.json`；本 reviewer没有调用
  recorder。
- Docs SSOT：strategy=`ssot_first`；durable finalizer/#105/#117 compatibility contract
  已是 primary input且 current。当前修复只恢复既有 documented behavior，
  `no_docs_update_needed`成立；handoff/report/evidence为 task-history-only，不构成第二份
  behavior SSOT。
- Branch Review：本轮不是 Branch Review。Fresh task commit后必须对完整
  `origin/main...HEAD` 重新执行 independent Branch Review，再执行 publication review与新的
  immutable finalization plan/digest confirmation。
- 部署/安全：current delta无 dependency、CI/CD、container、Kubernetes、DB migration、
  Terraform、Makefile、deploy或 production write影响；未发现 token、private key、signed
  URL、`.env`、database URL、customer data或 sensitive raw provider payload。
- 外部限制：未执行 commit、push、PR、archive、Ready、merge或 Issue mutation；旧
  Phase 2/Branch Review/publication/finalization evidence全部 stale，必须按流程重建；
  assignment linkage在主会话补录与 fresh validation前仍是 gate blocker。

### 结论

Current finalizer-private compatibility projection关闭了支持的 `verified` re-entry normal
path defect：strict #117 owner evidence在绑定 task、immutable plan、repo/ref、reviewed/remote
HEAD、checker result、execution status、完整 asset inventory与真实 artifact path后，才被投影为
#105 legacy schema；ledger继续记录真实 Interface 1.3 owner artifact identity。Public
Skill I/O、typed exits、workflow、#105 transaction、#117 generic checker、distribution与
#119/#132边界均未放宽。

完整检查未发现 current-scope P0-P3 implementation finding。主会话下一步必须先补录
`/root/issue118_finalizer_owner_projection_fix` 的真实 assigned/completed lineage与本 checker
completed event，并 fresh验证 assignment/linkage；通过后建议唯一 typed exit=`passed`，再运行
Phase 2 recorder/checker与 fresh task commit；
之后必须执行 independent Branch Review、publication review、pushed-ref #117 verification与新的
immutable plan digest confirmation，旧 evidence不得复用。
