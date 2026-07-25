# #116 Phase 2 Round 9 独立检查报告

## 检查完成

### 审查身份与权威

- Reviewer：`/root/issue116_phase2_round9`
- Role：`trellis-check` Phase 2 fresh reviewer
- Active task：`.trellis/tasks/07-24-116-review-task-publication`
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`
- Workspace boundary 初检：`status=ok`；expected workspace 与 actual repo root 均为上述 task worktree；source checkout 初检为 clean，`suspicious_source_artifacts=[]`。
- Planning approval 初检：`status=ok`、`typed_exit=approved`；批准证据包含 passed `ambiguity_review`、fixed-scope scanner、`explicit-post-planning-review` provenance 与当前规划文档 digest。
- Live authority：
  - GitHub Issue `castbox/guru-trellis#116` 仍为 `OPEN`；
  - accepted-current authority 为 comment `5045033833`（`2026-07-22T11:04:57Z`）；
  - 当前实现继续遵守 Interface 1.3、stable `exit_id`、两个 target-owned profiles、real-wrapper eval、以及不实现 #118/#119/#132 的边界。
- 官方 Trellis 交叉核对：
  - `https://docs.trytrellis.app/advanced/custom-workflow` 继续把 `.trellis/workflow.md` 定义为 workflow 行为 SSOT；
  - `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace` 继续要求 stable template id、可复用 spec 内容与 throwaway 安装验证。

### 审查范围与候选身份

- Base：`origin/main` = `bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- Merge base：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- Reviewed HEAD：`1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`
- Committed range：`origin/main...HEAD`
  - commits：
    - `aacb6e0 feat(workflow): #116 实现 task publication 审查闭环`
    - `1dd2ef8 fix(workflow): #116 收紧 publication 状态校验`
  - `337 files changed, 44698 insertions(+), 590 deletions(-)`
- Round 9 报告写入前的 dirty implementation/task-evidence snapshot：
  - `27 files changed, 2803 insertions(+), 103 deletions(-)`
  - `27` 个 tracked dirty path；
  - `5` 个 untracked path；
  - 本报告写入后只额外增加本文件这一条 task-local evidence path。
- 审查覆盖完整 committed range、当前 dirty finding-fix candidate、canonical/installed/shared/四平台副本、preset 与 extension manifest、task evidence；没有把审查缩窄到最新一行修复。

### 已检查文件

- Task authority 与规划：
  - `.trellis/tasks/07-24-116-review-task-publication/prd.md`
  - `.trellis/tasks/07-24-116-review-task-publication/design.md`
  - `.trellis/tasks/07-24-116-review-task-publication/implement.md`
  - `.trellis/tasks/07-24-116-review-task-publication/planning-approval.json`
  - `.trellis/tasks/07-24-116-review-task-publication/check.jsonl`
  - `.trellis/tasks/07-24-116-review-task-publication/implement.jsonl`
  - `.trellis/tasks/07-24-116-review-task-publication/issue-scope-ledger.json`
- Curated specs：
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/upstream-ownership.md`
  - `.trellis/spec/docs/public-docs.md`
- 实现与 durable contract：
  - `trellis/skills/guru-team/packages/guru-review-task-publication/**`
  - `.trellis/guru-team/skills/packages/guru-review-task-publication/**`
  - `.agents/skills/guru-review-task-publication/**`
  - `.codex/skills/guru-review-task-publication/**`
  - `.claude/skills/guru-review-task-publication/**`
  - `.cursor/skills/guru-review-task-publication/**`
  - `trellis/workflows/guru-team/scripts/bash/record-task-publication-review.sh`
  - `trellis/workflows/guru-team/scripts/bash/check-task-publication-review.sh`
  - `.trellis/guru-team/scripts/bash/record-task-publication-review.sh`
  - `.trellis/guru-team/scripts/bash/check-task-publication-review.sh`
  - `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
  - `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
  - `trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
  - `trellis/presets/guru-team/ownership/**`
  - `.trellis/guru-team/extension.json`
- 历史 finding 与实现交接：
  - `.trellis/tasks/07-24-116-review-task-publication/implementation-handoff.md`
  - `.trellis/tasks/07-24-116-review-task-publication/review.md`
  - `.trellis/tasks/07-24-116-review-task-publication/reviews/round-03-problem-closure.md`
  - `.trellis/tasks/07-24-116-review-task-publication/reviews/round-04-final-release.md`
  - `.trellis/tasks/07-24-116-review-task-publication/phase2-worker-report-round8.md`

### 先前问题闭环

#### `BR116-R04-P1-01`：通过

- 原问题：publication recorder/checker 只剥离 canonical source suffix，导致 installed shared 与 `.agents`、`.codex`、`.claude`、`.cursor` 四平台 package 错把 package root 当 repo root，无法定位 shared dispatcher。
- 当前闭环：
  - recorder/checker 采用与 public `invoke.sh` 对齐的六布局 exact resolver；
  - unknown layout fail closed；
  - 未设置 `GURU_TEAM_DISPATCHER` override 时，canonical audited layout 的 recorder/checker `2/2` 均到达 dispatcher 并按合同返回 `rc=2`；
  - installed shared 与四平台 recorder/checker 共 `10/10` 均返回 `rc=0` 并显示 mapped runtime help；
  - canonical 与 installed publication contract 各 `18/18` 通过，包含从 `interface.json` 读取 exact command 的真实六布局覆盖；
  - 两条 workflow runtime wrapper 已进入 preset managed assets 与 executable inventory；
  - fresh install、`trellis update --force`、preset reapply 三阶段分别得到 `10/10` wrapper help；
  - source/installed actual public-wrapper eval 各 `7/7` passed。
- 语义边界：
  - dirty finding-fix 没有修改 `SKILL.md`、`interface.json`、public schemas、step-local contract 或 global workflow；
  - `guru-review-task-publication` 仍为 `judgment_mode=semantic`；
  - AI owner 继续负责十维 publication review、finding、充分性、human confirmation 与 route；
  - recorder/checker 只在 AI gate 后执行 deterministic recording/validation，不选择 dimension status、finding 或 typed exit。

#### `PH2-116-R8-P2-01`：通过

- 原问题：throwaway verifier 的 authoritative source assertion 已从 `92` 更新为 `94`，但 preset exact-source regression test 仍断言旧 literal `92`。
- 当前闭环：
  - `trellis/presets/guru-team/**` 内 exact `assert len(assets) == 92` occurrence = `0`；
  - verifier 与 regression test 内 exact `assert len(assets) == 94` occurrence = `2`，各一处；
  - exact selector `PlatformOverlayInstallerTest.test_throwaway_verifier_cleans_preview_and_scans_sidecars_after_reapply`：`1/1 OK`；
  - preset full suite：`45/45 OK`；
  - installed manifest：`managed_assets=94`、Skill managed files=`2100`；
  - ownership validator：`managed_asset_count=50`；
  - sidecar/new/backup/removal/conflict 均为 `0`。
- 该修复只纠正 source-contract expectation，没有改变 installer、runtime、public I/O 或 publication semantic contract。

### P0–P3 Findings

- P0：`0`
- P1：`0`
- P2：`0`
- P3：`0`
- Round 9 新 finding：无。

### 已修复问题

- Reviewer 未修改实现文件。
- 本轮唯一写入是本报告；上述两个 finding 均由进入 Round 9 的候选实现闭合，并由本轮 fresh evidence 独立复验。

### 未修复问题

- 无 current-scope 未修复问题。
- #81、#117、#118、#119、#132 保持 `followup_issues`，未被本 task 越权实现或关闭。
- #115、#131、#144、#146 保持 `related_issues`；`close_issues` 仍只有 #116。

### 验证结果

- Lint：通过
  - `bash -n`：canonical/installed/platform publication package scripts、两条 workflow runtime wrapper、preset apply 与 throwaway verifier 全部通过。
  - `python3 -m py_compile`：runtime、runtime tests、Skill tests、publication contract tests、preset apply/tests、ownership validator/tests 全部通过。
  - `git diff --check origin/main...HEAD` 与 dirty `git diff --check`：通过。
- TypeCheck：不适用
  - 当前 Python/Shell 范围没有独立静态类型检查入口；已执行 compile、schema/contract validator 与完整测试。
- Tests：通过
  - Runtime full suite：`Ran 572 tests in 198.485s — OK (skipped=13)`。
  - Skill package full suite：`Ran 174 tests in 280.151s — OK`。
  - Preset full suite：`Ran 45 tests in 93.679s — OK`。
  - Upstream ownership full suite：`Ran 9 tests in 0.803s — OK`。
  - Canonical publication contract：`Ran 18 tests in 11.566s — OK`。
  - Installed publication contract：`Ran 18 tests in 11.554s — OK`。
  - P2 exact selector：`Ran 1 test — OK`。
  - Source publication actual-wrapper eval：`7/7 passed`。
  - Installed publication actual-wrapper eval：`7/7 passed`。
  - Source package validator：passed，`11 active / 42 exits / 25 targets`。
  - Installed package validator：passed，`2100` managed files，sidecar/removal/conflict 全为 `0`。
  - Ownership validator：`status=ok`，`50` managed assets，facts digest `738ffab55b80bfec2b5e482d6d25591d30e46d2d5264590b5be61ee56a43f801`。
  - Dogfood overlay drift：passed。
  - Task context validation：passed，`implement.jsonl=9`、`check.jsonl=8`。
  - Final planning approval：`status=ok`、`typed_exit=approved`、current HEAD=`1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`。
  - Final workspace boundary：`status=ok`；expected workspace 等于 actual repo root；source checkout status 为空；`suspicious_source_artifacts=[]`。
  - Final candidate status：HEAD 未变化；`27` 个 tracked dirty path、`6` 个 untracked path（包含本 Round 9 报告）。

#### Fresh throwaway / update / reapply

- 命令：
  - `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 ./trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- 结果：
  - exit code `0`；
  - fresh install：`10/10 publication validator wrappers reached shared help`；
  - after `trellis update --force`：`10/10`；
  - after preset reapply：`10/10`；
  - 完成 existing closeout/eval、ownership、drift、absence、no-developer 与 marketplace discovery 子场景；
  - 终态：`Verified public marketplace discovery plus local unpublished workflow sample`。

#### Parity、manifest 与 sidecar

- Canonical publication package 与 installed shared、`.agents`、`.codex`、`.claude`、`.cursor` 五副本：
  - tracked/package bytes parity：通过；
  - mode mismatch：`0`。
- 两条 canonical workflow runtime wrapper 与 installed `.trellis/guru-team/scripts/bash/` 副本：
  - bytes parity：通过；
  - executable mode：通过。
- `.trellis/guru-team/extension.json`：
  - managed assets：`94`
  - Skill managed files：`2100`
  - new copies：`0`
  - managed backups：`0`
  - sidecars：`0`
  - removals：`0`
  - conflicts：`0`
- Repository recursive `.new/.bak/.orig` scan：`0`。
- 注：`python3 -m py_compile` 会在本机生成 gitignored `__pycache__`；byte parity 命令明确排除该 runtime cache 后比较全部 package source files。它不属于 tracked candidate、installer asset 或 release payload。

### 关键命令证据

- 核心 suites：
  - `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - `python3 trellis/skills/guru-team/tests/test_skill_packages.py`
  - `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
  - `python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
- Publication：
  - `python3 trellis/skills/guru-team/packages/guru-review-task-publication/tests/test_contract.py`
  - `python3 .trellis/guru-team/skills/packages/guru-review-task-publication/tests/test_contract.py`
  - `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode source --skill guru-review-task-publication --adapter shared ... --json`
  - `.trellis/guru-team/scripts/bash/run-skill-evals.sh --root . --mode installed --skill guru-review-task-publication --adapter shared ... --json`
  - 在 `GURU_TEAM_DISPATCHER` unset 条件下直接执行 canonical/installed/platform recorder/checker `--help`。
- Package / ownership：
  - `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode source --json`
  - `.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --mode installed --json`
  - `trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json`
  - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- Context / boundary：
  - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-24-116-review-task-publication`
  - `./.trellis/guru-team/scripts/bash/check-planning-approval.sh --json --task .trellis/tasks/07-24-116-review-task-publication`
  - `./.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json --task .trellis/tasks/07-24-116-review-task-publication`

### 证据交接

- 阶段二：
  - 已覆盖 Issue #116 current authority、approved planning、全部 curated specs、完整 committed diff、当前 dirty finding-fix candidate、canonical/installed/platform copies、runtime、schemas/API、registry、workflow、preset、ownership、durable docs、task evidence 与 tests。
  - `BR116-R04-P1-01` 与 `PH2-116-R8-P2-01` 均以 ordinary supported path 的 fresh evidence 闭合。
  - 当前 P0/P1/P2/P3 findings 全为 `0`。
  - 本报告可支撑后续 `phase2-check.json` recorder；recorder 应绑定当前 HEAD、最终 dirty path set、本报告 digest 和 fresh validation summary。Reviewer 未调用 recorder/checker。
- Docs SSOT：
  - plan strategy：`ssot_first`。
  - committed #116 contract 已由 durable specs 作为 primary input；task delta 已在此前实现轮完成合并。
  - Round 9 dirty fixes只修 resolver、preset-managed runtime wrappers 与过期测试 literal，不修改 `SKILL.md`、Interface 1.3、public schemas、step-local contract、workflow route 或 durable semantics。
  - `implementation-handoff.md` 对 P1/P2 的 no-new-durable-delta 判断成立；当前代码、tests、installed copies、task evidence 与 durable docs 一致。
- 安全：
  - committed 与 dirty added lines 的 credential-shaped scan 均为 `0`；
  - 无 secret、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始记录进入候选；
  - 未执行 GitHub issue/PR mutation、push、publication、archive、finish 或 production write。
- 部署：
  - 完整 committed+dirty path scan 未命中 `.github`、Docker、K8s、DB migration、Makefile、Go/npm lockfile 等部署敏感路径；
  - 本次影响是 workflow Skill/preset/platform 安装资产，不包含生产服务部署或数据迁移；
  - throwaway 对 install/update/reapply 的 OOTB 与 upgrade/update 抗漂移门禁已实际覆盖。
- 限制：
  - 当前 candidate branch 尚未 push，无法验证 exact remote candidate-branch marketplace source；
  - throwaway 按批准方式使用 public marketplace sample 与 local unpublished workflow sample；
  - 该限制已诚实披露，不影响当前本地 Phase 2 finding-fix 的语义与 OOTB 验证，但远端 exact ref 验证仍属于 publication 前的后续门禁。
  - 按正常 honest-but-fallible 边界，本轮未扩张到恶意 artifact/hash 篡改、攻击模型、竞态、TOCTOU、锁、fault injection 或跨 OS 原子性。

### 结论

- Semantic conclusion：`passed`
- Findings count：`0`
- `BR116-R04-P1-01`：closed
- `PH2-116-R8-P2-01`：closed
- 当前候选满足 approved task scope、Public Skill I/O / semantic boundary、preset OOTB、upgrade/update、Docs SSOT、测试与安全/部署要求。
- 本报告仅支持主会话继续记录新的 Phase 2 gate；不授权 commit、push、PR、issue close、archive、finalize 或 publication。
