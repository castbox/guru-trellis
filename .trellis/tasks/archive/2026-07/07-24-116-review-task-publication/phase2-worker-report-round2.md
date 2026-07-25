## 检查完成

### 检查身份与边界

- 角色：finding-fix 后 fresh Phase 2 `trellis-check` 独立复审。
- Agent：`/root/issue116_phase2_rerun`。
- Task：`.trellis/tasks/07-24-116-review-task-publication`。
- Worktree：
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`。
- Branch：`codex/116-review-task-publication`。
- 当前 HEAD：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940`。
- Base：`main`；当前任务分支尚无相对 base 的 committed implementation commit，
  本轮审查对象为该 worktree 的完整 uncommitted current diff 与全部新增文件。
- `check-workspace-boundary.sh --json`：通过。expected workspace 与 actual repo
  root 相同；source checkout
  `/Users/wumengye/Documents/GoProjects/guru-trellis` 干净；没有 suspicious
  same-task source artifact。
- `check-planning-approval.sh --json`：通过。当前
  `planning-approval.json` 为 `approved`、fresh、content digest current，且包含
  passed ambiguity review、fixed-scope scanner 与
  `explicit-post-planning-review` provenance。
- 本 reviewer 未调用 Phase 2 recorder/checker、Branch Review recorder、commit、
  push、PR、archive 或 finalization。

### 已检查文件

- Task 与 gate：
  - `.trellis/tasks/07-24-116-review-task-publication/check.jsonl`
  - `.trellis/tasks/07-24-116-review-task-publication/prd.md`
  - `.trellis/tasks/07-24-116-review-task-publication/design.md`
  - `.trellis/tasks/07-24-116-review-task-publication/implement.md`
  - `.trellis/tasks/07-24-116-review-task-publication/planning-approval.json`
  - `.trellis/tasks/07-24-116-review-task-publication/issue-scope-ledger.json`
  - `.trellis/tasks/07-24-116-review-task-publication/implementation-handoff.md`
  - `.trellis/tasks/07-24-116-review-task-publication/phase2-worker-report.md`
  - `.trellis/tasks/07-24-116-review-task-publication/phase2-check.json`
  - `.trellis/tasks/07-24-116-review-task-publication/agent-assignment.json`
- Curated specs：
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/upstream-ownership.md`
  - `.trellis/spec/docs/public-docs.md`
- Canonical publication package：
  - `trellis/skills/guru-team/packages/guru-review-task-publication/SKILL.md`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/interface.json`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/references/contract.md`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/schemas/*.json`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/examples/*.json`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/evals/**`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/scripts/*.sh`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/tests/test_contract.py`
- Runtime / wrapper / eval：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - `trellis/workflows/guru-team/scripts/bash/record-task-publication-review.sh`
  - `trellis/workflows/guru-team/scripts/bash/check-task-publication-review.sh`
  - `trellis/skills/guru-team/adapters/eval/native_adapter.py`
- Registry / workflow / consumer：
  - `trellis/skills/guru-team/registry.json`
  - `trellis/skills/guru-team/migrations/stage0-minimal-handoff.json`
  - `trellis/skills/guru-team/migrations/production-minimal-handoff.json`
  - `trellis/skills/guru-team/packages/guru-review-branch/interface.json`
  - publication workflow/stop consumer schemas
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
- Installed/platform copies：
  - `.trellis/guru-team/skills/packages/guru-review-task-publication/**`
  - `.agents/skills/guru-review-task-publication/**`
  - `.codex/skills/guru-review-task-publication/**`
  - `.claude/skills/guru-review-task-publication/**`
  - `.cursor/skills/guru-review-task-publication/**`
  - `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - `.trellis/guru-team/skills/adapters/eval/native_adapter.py`
  - `.trellis/guru-team/extension.json`
- Preset / installer / upgrade：
  - `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
  - `trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
  - `trellis/presets/guru-team/scripts/python/verify_installed_closeout.py`
  - `trellis/presets/guru-team/ownership/upstream-ownership.json`
  - `trellis/presets/guru-team/overlays/**`
- Durable/public docs：
  - approved Docs SSOT Plan 列出的 16 个 durable paths，包括 workflow/preset/docs
    specs、三份 requirements 文档、root/workflow/preset README。

### Scope qualification

#### SQ-001：F-001 stale/current invocation 修复

- Scenario class：`normal_required_behavior`。
- Scope：current task。
- 结论：未发现 F-001 仍开放的独立实现缺口。
- 实际代码证据：
  - stale recorder 读取现有 current `pr-readiness.json`，要求
    `supersedes_publication_ref` 精确等于 prior artifact 的 current
    `publication_ref`；
  - stale artifact 持久化 `stale_reason`、`reentry_context` 与
    `supersedes_publication_ref`；
  - recorder/checker 每轮重建十二项 entry bindings，`ready` 对任一 objective
    entry error fail closed；
  - checker 比较 stored/current 十二项 bindings、artifact bindings、repository
    binding、review identity、opaque publication identity 与 facts digest；
  - public wrapper 重跑 owner checker，并把 stale public input 的
    `stale_reason`、`reentry_context` 与 checked owner result 精确比较；
  - finalization augmentation 只接受 exact `closeout-plan.json` 引入的 repository
    status delta 与派生 `review_range_and_working_tree` binding 变化。
- Fresh 证据：
  - source actual-wrapper eval `stale-reentry-ready`：passed，actual exit=`ready`；
  - source/installed publication package contract 各 11 tests passed；
  - exact closeout-plan augmentation 与 extra metadata delta negative 共 2 tests
    passed。
- 限制：installed actual-wrapper stale eval 被下述 F-003 的 installed package
  provenance gate 在执行前阻断；因此 F-001 的 installed end-to-end 仍需在 F-003
  修复后重跑，不能仅凭 source 结果宣告完整安装链路通过。

#### SQ-002：F-002 private gate closed semantics 修复

- Scenario class：`normal_required_behavior` / `explicit_requirement`。
- Scope：current task。
- 结论：F-002 仅部分修复，仍为开放 P1 finding。
- 已确认修复：
  - `semantic_review`、`deterministic_bindings`、consumer 与 optional
    `publish_inputs` 已从开放 object 收敛为 nested closed schema；
  - finding 的 summary/scope/evidence/affected/closure 已要求非空；
  - duplicate finding refs、ready failed entry、缺 stale replacement fields
    已有 negative coverage；
  - ready consumer、十二项 passed bindings、AI Gate 与 ten dimensions 已有
    conditional schema/runtime检查。
- 仍可复现的 normal authored payload：
  1. 以 package 的 schema/runtime-valid ready example 为基线，只把
     `semantic_review.conclusions.issue_scope.status` 改为 `blocked`；
     JSON Schema errors=`0`，`task_publication_semantic_errors(...)`=`[]`。
  2. 选择 `return_to_task_work`，保留十个 dimensions 全部 `passed`，加入一个
     open `task_work` finding 并让 AI Gate/consumer 匹配；
     JSON Schema errors=`0`，runtime semantic errors=`[]`。
  3. 选择 `blocked`，保留十个 dimensions 与 scope/Docs/safety conclusions
     全部 `passed`、findings 为空，只补 reason/remediation；
     JSON Schema errors=`0`，runtime semantic errors=`[]`。
- 这些 payload 不需要伪造 digest、篡改 artifact 或绕过脚本；它们可作为正常
  AI-authored recorder input，recorder 会重算 deterministic bindings/facts。
- Contract impact：
  - `ready` 可以与 blocked scope/Docs/safety conclusion 同时成立；
  - `return_to_task_work` 可以没有任何 failed/finding dimension；
  - `blocked` 可以没有 blocked dimension 或 external-blocker finding；
  - 因此 closed exit/semantic union 仍未实现 PRD R4/R6、design §7/§8/§10 与
    durable Docs SSOT 所声明的 current semantic consistency。
- Required implementation：
  - 在 private schema 与 runtime semantic checker 同时增加 exit-conditional
    cross-consistency；
  - `ready` 至少要求三项 conclusions 全部 `passed`、十维全 pass、findings
    全 closed，且无 open/blocking evidence；
  - `return_to_task_work` 要求至少一个 `finding` dimension 与一个 open
    `task_work` finding，finding.dimension 必须指向非-passed dimension；
  - `blocked` 要求 blocked dimension 与 open external-blocker evidence；如果产品
    决策希望 reason-only blocked，则必须先修订 planning/durable contract，不得由
    runtime静默接受两种语义；
  - 增加 source/installed schema、semantic checker、recorder/checker 与 actual
    wrapper negative tests/evals，并重新同步所有安装/platform copies。

#### SQ-003：installed package provenance / sidecar inventory

- Scenario class：`normal_upgrade_update_path`。
- Scope：current task 的 preset/dogfood installed state。
- Severity：P1（阻断 installed package validator 与 installed actual wrapper）。
- Fresh reproduction：
  - source `check-skill-packages --mode source`：passed，11 active Skills /
    42 exits / 25 targets；
  - installed `check-skill-packages --mode installed`：exit 2，failed；
  - `.trellis/guru-team/extension.json` 的 `skill_packages.sidecars` 仍登记五个
    `guru-review-task-publication/references/contract.md.bak`；
  - recursive actual `.new/.bak/.orig` scan 为 0，这五个声明文件均不存在；
  - validator errors 包括：
    - `installed skill package provenance is invalid or conflicted`
    - `installed skill package has unresolved sidecars`
    - 五条 `missing installed skill sidecar ...contract.md.bak`
    - `installed skill sidecar inventory is incomplete`
  - installed stale actual-wrapper eval 因此在执行前以
    `contract_asset_invalid` 失败。
- Impact：
  - handoff 的“installed validator passed / sidecar=0”与 current installed
    manifest不一致；
  - dogfood installed contract 当前不是可被 runtime接受的 complete compatible
    preset；
  - update/reapply/open-box acceptance不能以当前 state 通过。
- Required implementation：
  - 不要手工掩盖 validator；通过 canonical preset apply/upgrade 路径重新生成
    current installed manifest，使 sidecar inventory 与实际 resolved state 一致；
  - 重跑 installed validator、installed publication 11 tests、installed
    `stale-reentry-ready` 与完整 7-case shared eval、dogfood drift、recursive
    sidecar scan以及 clean update/reapply；
  - 更新 implementation handoff 中的 current 结果，不能沿用删除 sidecar 前的
    manifest证据。

### 已修复问题

- 无。
- 原因：本轮 handoff 明确要求 finding-fix 后独立全量复审；发现任何剩余 gap 时返回
  `implementation_required`，不得继续实现。F-002 需要 schema/runtime/tests/
  installed copies 联动，F-003 需要 canonical preset reapply/manifest 重建，均不属于
  reviewer 可安全执行的单文件机械修复。

### 未修复问题

- F-002（P1，blocking）：publication exit 与 dimensions/findings/conclusions 的
  closed cross-consistency 仍可被 normal authored payload绕过。
- F-003（P1，blocking）：installed extension manifest 保留五个已删除 sidecar 的
  stale provenance inventory，installed validator 与 installed actual wrapper
  fail closed。
- F-001 本轮未重开；但 installed end-to-end 复验依赖 F-003 先闭环。

### 十维充分性结论

1. Requirements：失败。F-002 违反 R4/R6/R9 与 AC6/AC8；F-003 违反
   installation/update/open-box acceptance。
2. Design：失败。§7/§8/§10 closed semantic union 与当前 schema/runtime
   cross-consistency 不一致；installed state也不满足 package provenance设计。
3. Implementation：失败。核心 package/runtime 大部分修复已落地，但上述两条
   normal-path gap仍开放。
4. Tests：失败。现有 green contract suite没有覆盖 non-passed conclusions 与
   typed-exit cross-consistency；installed validator fresh失败。
5. Docs SSOT：失败。approved strategy=`ssot_first`，16 个 durable paths已作为实现
   输入并有 task delta；但 durable docs声称 closed semantic gate 与 resolved
   installed sidecar state，current implementation/state不满足，不能标记
   task delta merged。
6. Cross-layer：失败。private schema/runtime/recorder exit consistency以及
   installed extension manifest/actual filesystem不一致。
7. Compatibility：失败。legacy reader与 finalization augmentation targeted tests
   通过，但 installed compatible preset当前无效。
8. Deployment and operations：通过。完整 changed/untracked path scan没有发现
   GitHub Actions、Docker/Compose、Kubernetes/Helm、DB migration、`.env`、
   Makefile 或 production deployment surface变更；未执行远端写入或发布。
9. Agent recovery：通过。initial implementation、initial Phase 2、finding-fix
   implementation 与本 fresh check身份、顺序和状态均可从
   `agent-assignment.json` 恢复；没有把旧 Phase 2 pass证据复用成新结论。
10. Verification completeness：通过（足以安全路由实现）。fresh probes和 installed
    validator已足以确认两个 current-scope blocking findings；未验证项不妨碍
    `implementation_required`。

### 验证结果

- Lint：部分通过。
  - `git diff --check`：通过。
  - dogfood overlay drift：通过。
  - 仓库无独立 ruff/flake8/shellcheck lint配置。
  - installed package validator失败，因此不能给任务级 lint/package gate
    `passed`。
- TypeCheck：不适用。仓库未配置 mypy、pyright 或等价 type-check command；未用
  Python import或单测冒充静态类型检查。
- Tests：任务级失败。
  - publication source contract：11 passed。
  - publication installed contract：11 passed（直接执行 installed copy）。
  - finalization augmentation targeted：2 passed。
  - source actual-wrapper `stale-reentry-ready`：passed。
  - source package validator：passed，11/42/25。
  - installed package validator：failed，sidecar_count=5 且实际 sidecar=0。
  - installed actual-wrapper `stale-reentry-ready`：
    `contract_asset_invalid`，未进入 owner round。
  - F-002 三个 fresh mutation probes：均被 schema/runtime错误接受，任务级失败。
- Reused fresh heavy evidence：
  - finding-fix handoff记录 current implementation files上的 skill package suite
    171 passed、runtime 570 passed/13 skipped、preset 45 passed、source/installed
    publication 11+11、source/installed shared eval 7+7、throwaway
    install/update/reapply双 closeout通过；
  - 本 reviewer通过 current file parity、targeted tests与 current HEAD/mtime
    确认代码主体未在 handoff 后改变；
  - 但 current fresh installed validator推翻了 handoff中的 installed
    provenance/sidecar终态，因此不复用该部分作为通过证据。
- Finalization：
  - exact closeout-plan augmentation positive：passed；
  - extra metadata delta negative：passed；
  - 没有执行真实 finalization。
- Closure / frozen invariants：
  - source closure：11 Skills / 42 exits / 25 targets，passed；
  - production migration manifest：3 Skills / 11 exits，保持；
  - Stage 0 migration manifest：6 Skills / 24 exits，保持；
  - upstream ownership：43 frozen/active paths、5 reviewed current payloads、
    11 active + 1 planned，passed；
  - dogfood overlay copies match canonical overlays；
  - current diff没有触及 production manifest、#131 output schema/examples、
    五个 continue overlays、overlay tree或 finish-work assets。
- Distribution parity：
  - canonical、installed、Agents、Codex、Claude、Cursor publication package
    bytes一致（忽略 Python cache）；
  - canonical/installed runtime与 native adapter bytes一致；
  - parity通过不消除 installed manifest provenance F-003。
- Sidecars：
  - actual recursive `.new/.bak/.orig` scan：0；
  - declared installed sidecars：5；
  - 声明/实际不一致，failed。

### 安全、部署与开箱即用

- 本轮没有读取或输出 secret、credential、`.env`、signed URL、客户数据或私有原始
  payload。
- 没有执行 commit、push、PR、archive、GitHub写入、production deployment或
  finalization。
- Full throwaway install/update/reapply 结果只作为 finding-fix handoff evidence
  读取；当前 installed manifest fresh失败后，不能再声称 current dogfood/open-box
  链路完整通过。
- Exact current branch remote marketplace verification仍需分支 push授权后执行；
  public-marketplace sample不等于 exact-branch verification。该限制本身不是本轮
  finding，但必须继续在后续 publication readiness中显式披露。
- 真实 Codex/Claude/Cursor CLI在线 invocation、#118 finalization、remote
  marketplace、commit/push/PR/archive均未验证。

### 证据交接

- 阶段二：
  - 覆盖完整 current uncommitted diff、全部新增 publication package、
    canonical/installed/platform copies、runtime/schema/wrapper/eval/test、
    registry/workflow/consumer、preset/manifest/ownership、Docs SSOT 与
    safety/deployment。
  - F-001 source current path与 exact finalization边界通过，未重开。
  - F-002 仍为 current-scope P1，F-003 为新的 current-scope P1。
  - 本报告可支撑新的 `phase2-check.json` 使用
    `typed_exit=implementation_required`；不能支撑 `passed`。
  - 必须在两个 finding修复后重新执行完整 Phase 2 round，不能只做 finding
    delta check。
- Docs SSOT：
  - plan strategy=`ssot_first`；
  - durable docs、task artifacts、code/test大部分已同步；
  - F-002 使 closed readiness contract与实现不一致，F-003 使
    installer/provenance contract与 current dogfood state不一致；
  - `task_delta_merged` 当前应为 false，修复后重新核对全部 16 durable paths；
  - exact remote branch marketplace保留为授权 push后的明确限制，不得冒充已验证。
- Branch Review：
  - 不适用。本轮不是 Branch Review，没有审查 committed
    `origin/<base>...HEAD` diff，也没有写 `review.md` / review gate。
- Agent evidence：
  - initial implementation：`/root/issue116_implement` completed；
  - initial check：`/root/issue116_phase2_check` completed，
    `implementation_required`；
  - finding fix：`/root/issue116_fix_round1` completed；
  - fresh rerun：`/root/issue116_phase2_rerun`，本 raw report；
  - 旧 `phase2-check.json` 仍是 initial `implementation_required` artifact，
    不能被解释为当前 fresh round的 recorder结果。

### 结论

`implementation_required`。

F-001 的 stale identity、十二项 entry binding、wrapper reason/context 与 exact
finalization augmentation 在本轮未发现新的独立缺口；但 F-002 的 closed semantic
union仍可接受互相矛盾的 ready/return/blocked evidence，且 current installed
extension manifest 与实际 sidecar state不一致，导致 installed validator和 actual
wrapper fail closed。必须先按上述 implementation work修复 F-002、F-003，更新 current
handoff，并重新运行完整 Phase 2 check；当前不能进入 task commit 或 Branch Review。
