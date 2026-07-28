# Issue #118 final projection compatibility chain Phase 2 全量检查

## 检查完成

### 检查身份与边界

- 角色：独立 Phase 2 trellis-check reviewer。
- Reviewer：/root/issue118_phase2_final_projection_chain。
- Implementation agent：/root/issue118_final_projection_chain_fix。
- Task：.trellis/tasks/07-26-118-guru-finalize-task。
- Worktree：/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/118-guru-finalize-task。
- Branch：feat/118-guru-finalize-task。
- Base：origin/main@7820a9eeec2a2a75fb52fba156a7211d9f9fb09c。
- Checked HEAD：85ab42837a44968d892f520614ab611becf5b8d5 加 current task-local working tree。
- Finding inventory：P0=0、P1=0、P2=0、P3=0。
- Scope proposal inventory：0。
- 建议 typed exit：passed，consumer=skill:guru-create-task-commit。

Workspace boundary 通过：expected workspace 与 actual repo root 均为上述 task
worktree；source checkout 为
/Users/wumengye/Documents/GoProjects/guru-trellis，状态 clean；task worktree
包含本轮 runtime/test/task metadata dirty scope；没有 suspicious source artifacts。

Planning approval checker 返回 typed_exit=approved，当前
guru-planning-approval-2.0 仍绑定经 explicit-post-planning-review 审核的
prd.md、design.md、implement.md、authority、provenance、ambiguity review、
fixed-scope scanner 与 Docs SSOT Plan。Implementation HEAD/dirty drift没有改变
planning/authority/docs plan identity。

check.jsonl 只有 seed row，因此本轮按 fallback 完整读取 planning 三件套，并读取
.trellis/spec/workflow/skill-package-contract.md、workflow-contract.md、
companion-scripts.md、data-contracts.md、quality-guidelines.md，以及适用的
preset/install/ownership/public-docs SSOT。guru-check-task Skill 与完整 contract
也已加载。

本 reviewer 未修改 runtime、tests、public contract、API、schema、workflow、preset、
overlay、README、平台分发、agent-assignment.json 或 phase2-check.json；未执行
commit、push、PR mutation、archive、Ready、merge、deploy 或 GitHub Issue mutation。
本轮只新增本报告与配套 command evidence JSON。

### 已检查文件

- Planning 与 authority：prd.md、design.md、implement.md、
  planning-approval.json、Issue #118 body/accepted-current comment。
- Implementation handoff：
  implementation-handoff-final-projection-chain-fix.md。
- Canonical runtime：
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py。
- Dogfood runtime：
  .trellis/guru-team/scripts/python/guru_team_trellis.py。
- Regression tests：
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py。
- Task checkpoint cleanup：删除的 closeout-plan.json、
  marketplace-verification.json、未跟踪的 task-finalization-gate.json，
  以及 issue-scope-ledger.json 中旧 remote verification evidence。
- Agent/recovery evidence：agent-assignment.json 当前 implementation/check
  lineage、status/liveness events 与 current-HEAD validator。
- Existing task gates：phase2-check.json、review-gate.json、
  pr-readiness.json、pr-body.md、finish-summary-index.json。
- Durable Docs SSOT：.trellis/spec/workflow/**、.trellis/spec/preset/**、
  .trellis/spec/docs/** 与 repository/workflow/preset README。
- Full branch context：origin/main...HEAD 的 562 paths / 11 commits，以及
  current 7 tracked dirty paths和本轮 task-local untracked handoff/report/evidence。
- Protected/deploy surfaces：global workflow、upstream trellis-finish-work
  family、official .trellis/scripts/task.py、preset overlays、CI/CD、container、
  K8s/Kustomize/Helm、DB migration、Terraform、Makefile、deploy path 与
  sensitive material patterns。

### 语义检查结论

实现正确修复了正常路径中的 compatibility gap：

    #117 checker-passed owner result
    -> finalizer-private compatibility projection
    -> cmd_execute_finalization_transition
    -> cmd_finish_work
    -> build_final_archive_projection
    -> validate_closeout_active_projection
    -> execute_archive_metadata_transaction

active interrupted archive recovery 也从 resume_active_archive_move() 将同一
projection 传入 active projection 与 archive transaction。所有新增
_verification_projection 只在内存中传递，不进入 public input/output、
Interface、schema、ledger、task finalization gate 或 persisted recovery state。

validate_closeout_marketplace_artifact() 在 projection 存在时用它校验 #105 legacy
字段；artifact locator、existence 与 artifact_sha256 仍从真实 task-local
marketplace-verification.json owner bytes 取得。Ledger primary/close issue evidence
继续与真实 owner bytes SHA 绑定。无 projection 的 #105 compatibility path 保持读取
legacy on-disk artifact，未改变既有行为。

Owner bytes 变化、reviewed HEAD mismatch 与 plan digest mismatch 均 fail closed。
Canonical 与 dogfood runtime byte-identical。未修改 #117 generic checker、#105
transaction ordering、public Skill graph、Finish global route 或 #119/#132 ownership。

Production regression 不再 mock 整个 cmd_finish_work()，真实执行 public finalizer
transition、cmd_finish_work()、ledger evidence update、draft identity validation、
build_final_archive_projection() 与 active projection consumer。该 regression 仍
mock publication/current-state fixture setup（包括 prepare_closeout 的既有 fixture
路径）以及 Git/GitHub/archive/Ready side effects；这些 mocks 没有替代本次目标
projection consumers。故本报告不把它描述为“只 mock 外部 side effects”。

### 已修复问题

- 文件：trellis/workflows/guru-team/scripts/python/guru_team_trellis.py、
  .trellis/guru-team/scripts/python/guru_team_trellis.py。
- 问题：finalizer 在 #117 owner result 首次转换后，Draft 后的 final/active/archive
  consumers 又把 Interface 1.3 owner artifact 当作 #105 legacy schema 1.0 读取，
  正常 verified happy path会在 final projection 稳定失败。
- 修复：Implementation agent 增加 owner-private in-memory projection 参数，并贯穿
  final projection、existing-summary active projection、archive transaction 与 active
  interrupted-archive recovery；legacy 无 projection 路径保持不变。

- 文件：trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py。
- 问题：原 production regression mock 整个 cmd_finish_work()，没有执行到真实
  final/active consumer；owner bytes/HEAD/plan mismatch 缺少针对性回归。
- 修复：Regression 真实执行目标 consumer 链，并增加 owner bytes、HEAD、plan
  mismatch fail-closed、legacy default 与 active recovery private keyword 覆盖。

- 文件：task-local stale checkpoints 与 issue-scope-ledger.json。
- 问题：旧 closeout-plan.json、marketplace-verification.json、
  task-finalization-gate.json 和 ledger remote evidence 绑定旧 plan/HEAD，不能作为
  current implementation 的 Phase 2/publication/finalization 输入。
- 修复：Implementation agent 保留 provenance 后删除 active stale copies，并只移除
  ledger primary/#118 的旧 remote evidence；后续必须按 current task-work 重建全部
  downstream evidence。

本 reviewer 没有新增 implementation self-fix。

### 未修复问题

没有 open current-scope P0-P3 finding，implementation_required=false。

以下是下游门禁，不是当前实现缺陷：

- current dirty fix 尚未形成新 task commit，pushed-ref #117 remote marketplace
  verification 尚不能针对该新 commit执行；
- 旧 phase2-check.json、review-gate.json 与 pr-readiness.json 均预期 stale，
  validator exit 2，证明旧 evidence 未被复用；
- 主会话必须先记录本 reviewer 的 completed event，再运行 fresh
  guru-check-task recorder/checker、task commit、独立 Branch Review、publication
  review、side-effect-free finalization preview 与 exact digest confirmation。

### Historical observation

git diff --check origin/main...HEAD exit 2，只命中 immutable raw report
.trellis/tasks/07-26-118-guru-finalize-task/reviews/round-009-finding-closure.md:203
的 trailing whitespace。该 path 曾被 reviewer 临时机械删除空格，但按主会话要求已恢复
HEAD exact bytes；git diff --exit-code HEAD -- <path> 与
git diff --check HEAD 均通过。它是历史 evidence observation，不是 current finding。

Raw cmp 比较两份 closeout schema exit 1，仅因格式不同；canonical JSON comparison
exit 0。首次 ledger zero probe 因 reviewer shell quoting error exit 1，corrected jq
probe exit 0。combined-branch-dirty-diff-hygiene 运行于上述临时历史报告修改期间，
不作为终态证据。

### Docs SSOT

Approved strategy=ssot_first。Issue #118 主实现已把 finalizer ownership、
Interface 1.3、#105 transaction、#117 private compatibility、production eval、
安装状态与 #119/#132 边界写入 durable package/spec/README SSOT。

本轮 runtime/test fix 结论为 no_docs_update_needed：

- durable contracts 已要求 finalizer-only compatibility 绑定 exact task/plan/HEAD、
  repository、owner bytes、ledger digest 与 transaction；
- 本轮只让 runtime 正确承接既有 contract，不改变 public DTO、Interface、schema、
  route、transaction ordering、install inventory、platform distribution 或 user-facing
  behavior contract；
- handoff、本报告与 command evidence 只保存 task history，不成为第二份 behavior
  SSOT；
- global workflow、upstream Finish assets、preset、overlay、README 与 durable docs
  无 current dirty delta。

因此 durable docs、planning/task artifacts、runtime 与 tests 对 approved Docs SSOT
Plan 一致；ssot_first + no_docs_update_needed 在 final diff 上仍成立。

### 验证结果

- Lint：通过。Current dirty candidate git diff --check HEAD、Bash syntax、
  source/installed validators、ownership、overlay drift、protected/deploy no-diff、
  sidecar 与 sensitive scan 均通过；full branch 仅有上述 immutable historical
  observation。
- TypeCheck：通过适用检查。仓库没有 configured ruff/mypy/pyright gate；
  canonical/dogfood/test py_compile 与 closed schema/interface validators 通过。
- Tests：通过。
- Focused production/negative/legacy regressions：5 passed。
- CloseoutTransactionContractTest：107 passed。
- Full runtime：629 passed, 13 skipped。
- Skill/package/interface/eval：180 passed。
- Finalizer contract：5 passed。
- #116 publication contract：18 passed。
- #117 verification contract：10 passed。
- Preset installer：45 passed。
- Upstream ownership：9 passed。
- Task、planning、assignment/current-HEAD、workspace validators：通过。
- Canonical/dogfood runtime、canonical/installed/shared/Codex/Claude/Cursor package
  parity：通过。
- Closeout schema canonical JSON semantic parity：通过。
- Clean throwaway：通过，终态 marker 为
  Verified throwaway Guru Team Trellis install；覆盖 workflow marketplace、
  preset initial install/reapply、Trellis update、managed hash、.new/.bak、
  platform copies、contract discovery 与 OOTB。该运行从 remote feature ref取得
  本轮未变的 workflow marketplace，并从 local preset/runtime取得 current dirty
  candidate；它不替代 dirty fix commit 后的 real pushed-ref #117 verification。
- 未观察 GitHub 401。Cursor unsupported/unavailable 与 standalone remote-unavailable
  仅为 test corpus 覆盖，不是外部失败。
- Final state：stale closeout/verification/gate/finish-summary absent；task
  in_progress；ledger remote evidence count=0；PR body只含 Closes #118。
- Live state at retained capture：local/remote/PR #160 head均为
  85ab42837a44968d892f520614ab611becf5b8d5；PR #160 OPEN/Draft；Issue #118
  OPEN。本轮没有 mutation。
- Security/deploy：未发现 secret/credential/customer data/raw provider payload；
  无 CI/CD、container、K8s、DB migration、Terraform、Makefile、deploy 或
  production-write 影响。

### Command evidence

配套 artifact：

phase2-command-evidence-final-projection-chain-fix-full-round.json

- SHA-256：d1bbb1f6d7e18155fac376a46d30fbf8728a19ddf3ebff1ad1f68af386201ec1
- Bytes：26712
- Lines：149
- Commands：53
- 原始 commands.jsonl SHA-256：
  a1881560002959e942cfd36e5482487d30ff6bedbb6d5f89841c4f1b21c13ca0
- 每条保留 exact argv[]、exit code、stdout/stderr SHA-256 与 byte size。
- Evidence JSON 中 53 个 command object 与 raw JSONL 逐条 canonical JSON
  readback相等。
- Raw stream temporary root
  /tmp/guru118-final-projection-phase2.5EKsM0 已在 artifact readback 后删除并验证
  absent。

### 证据交接

- 阶段二：覆盖 planning/provenance/workspace、完整 562-path branch context、
  current final/active/archive projection chain、legacy #105、owner-byte/HEAD/plan
  mismatch、stale checkpoint cleanup、629/13 runtime、107 transaction、180 Skill
  graph、#116/#117、preset/ownership、canonical/dogfood/platform parity、clean
  throwaway、protected/deploy/sensitive scope与 live GitHub identity。
  P0/P1/P2/P3=0/0/0/0，scope proposals=0，本报告可支撑 fresh
  phase2-check.json 的 AI-authored semantic input。
- Guru boundary：本 reviewer 未写 phase2-check.json，未调用 recorder/checker。
  主会话需记录本 checker completed event，再由 guru-check-task owner构建并验证唯一
  schema 2.0 artifact。
- Docs SSOT：strategy=ssot_first；current fix result=no_docs_update_needed；
  durable docs、task artifacts、runtime、tests一致；handoff/report/evidence 为
  task-history-only。
- Branch Review：本轮不是 Branch Review。Fresh task commit 后必须由独立 reviewer
  覆盖完整 origin/main...HEAD，不得复用本 Phase 2 身份。
- 发布限制：dirty fix commit/push 前不能运行 current pushed-ref #117 verification；
  fresh publication review 与新的 immutable plan/digest confirmation 前禁止 PR
  mutation、archive、Ready、merge 或 Issue mutation。
- 安全与部署：无 sensitive data 或 deployment/production-write 影响。

### 结论

Final projection compatibility chain 修复满足 Issue #118、approved planning、
Docs SSOT、Interface 1.3 private-state boundary、#105 transaction semantics、
#116/#117 ownership与 #119/#132 scope 边界。真实 final/active/archive consumers
收到同一 owner-private projection，owner artifact bytes/ledger SHA authority 与 legacy
default path均保持不变。

未发现 open current-scope finding；Lint、适用 TypeCheck、完整 tests、package/eval、
distribution/OOTB 与 retained command identity均通过。建议 Phase 2
typed exit=passed，implementation_required=false。

下一步由主会话记录本 reviewer completed event，运行 fresh guru-check-task
recorder/checker，然后创建 task commit并进入独立 Branch Review。新 publication
readiness、immutable plan/digest confirmation 与 #117 pushed-ref evidence完成前，不得
继续 closeout external side effects。
