# Issue #116 Phase 2 Round 8 独立检查报告

- Reviewer：`/root/issue116_phase2_round8`
- Role：fresh Phase 2 check / finding-fix verification
- Active task：`.trellis/tasks/07-24-116-review-task-publication`
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`
- Base range：`origin/main...HEAD`
- Base / merge-base：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- Reviewed HEAD：`1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`
- Committed diff：337 files，44,698 insertions，590 deletions
- Candidate scope：上述完整 committed diff，加本轮开始时已有的 27 个 dirty implementation / installed-copy / test / task-evidence 路径
- Scope authority：GitHub Issue #116 当前正文及 2026-07-22 accepted-current comment、批准的 `prd.md` / `design.md` / `implement.md`
- Overall typed conclusion：`implementation_required`
- Findings：P0=0，P1=0，P2=1，P3=0

## 检查完成

本轮已独立审查完整 `origin/main...HEAD` committed range 与当前 dirty candidate，并针对 Branch Review finding `BR116-R04-P1-01` 重新执行真实 package wrapper、source/installed package、preset 安装、`trellis update` 和 preset reapply 验证。该 P1 所描述的六种 package layout dispatcher 定位缺陷已经获得行为闭环证据；但本轮发现一个新的、正常支持路径可复现的 P2 测试一致性遗漏，因此当前候选不能通过 Phase 2。

### 已检查文件

- 需求与授权：
  - GitHub Issue #116 当前正文及 accepted-current comment
  - `.trellis/tasks/07-24-116-review-task-publication/prd.md`
  - `.trellis/tasks/07-24-116-review-task-publication/design.md`
  - `.trellis/tasks/07-24-116-review-task-publication/implement.md`
  - `.trellis/tasks/07-24-116-review-task-publication/planning-approval.json`
  - `.trellis/tasks/07-24-116-review-task-publication/check.jsonl`
  - `.trellis/tasks/07-24-116-review-task-publication/implement.jsonl`
- 本 task 的实现与审查证据：
  - `.trellis/tasks/07-24-116-review-task-publication/implementation-handoff.md`
  - `.trellis/tasks/07-24-116-review-task-publication/issue-scope-ledger.json`
  - `.trellis/tasks/07-24-116-review-task-publication/phase2-check.json`
  - `.trellis/tasks/07-24-116-review-task-publication/review.md`
  - `.trellis/tasks/07-24-116-review-task-publication/review-gate.json`
  - `.trellis/tasks/07-24-116-review-task-publication/reviews/round-04-final-release.md`
  - `origin/main...HEAD` 的 337-file committed diff
  - Round 8 开始时的 27-path dirty candidate
- Durable Specs：
  - `.trellis/spec/workflow/quality-guidelines.md`
  - `.trellis/spec/workflow/skill-package-contract.md`
  - `.trellis/spec/workflow/workflow-contract.md`
  - `.trellis/spec/workflow/data-contracts.md`
  - `.trellis/spec/workflow/companion-scripts.md`
  - `.trellis/spec/preset/installer.md`
  - `.trellis/spec/preset/upstream-ownership.md`
  - `.trellis/spec/preset/overlay-guidelines.md`
  - `.trellis/spec/docs/public-docs.md`
- Publication Skill canonical contract：
  - `trellis/skills/guru-team/packages/guru-review-task-publication/SKILL.md`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/interface.json`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/references/contract.md`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/schemas/*.json`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/examples/*.json`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/evals/**`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/scripts/*.sh`
  - `trellis/skills/guru-team/packages/guru-review-task-publication/tests/test_contract.py`
- Publication Skill installed/discovery copies：
  - `.trellis/guru-team/skills/packages/guru-review-task-publication/**`
  - `.agents/skills/guru-review-task-publication/**`
  - `.codex/skills/guru-review-task-publication/**`
  - `.cursor/skills/guru-review-task-publication/**`
  - `.claude/skills/guru-review-task-publication/**`
- Runtime、workflow 与 registry：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `trellis/skills/guru-team/registry.json`
  - `trellis/skills/guru-team/migrations/production-minimal-handoff.json`
  - `.trellis/guru-team/scripts/bash/record-task-publication-review.sh`
  - `.trellis/guru-team/scripts/bash/check-task-publication-review.sh`
- Preset、installer 与 ownership：
  - `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
  - `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
  - `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
  - `trellis/presets/guru-team/scripts/python/test_upstream_ownership.py`
  - `trellis/presets/guru-team/ownership/upstream-ownership.json`
  - `.trellis/guru-team/extension.json`
  - `trellis/presets/guru-team/README.md`
  - `trellis/workflows/guru-team/README.md`

### 已修复问题

- 无。本轮 handoff 明确只允许写本报告，未授权修改 implementation、spec、planning、gate、assignment、review 或 commit-plan 文件。

### 未修复问题

#### `PH2-116-R8-P2-01` — preset 全量测试仍断言旧的 92-file managed asset inventory

- Severity：P2
- Status：open
- 文件：`trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py:1051`
- 触发路径：正常运行 required preset full suite，无需篡改 artifact、hash 或 state。
- 现象：
  - 本轮为修复 `BR116-R04-P1-01`，installer 新增两条 public runtime wrapper：
    - `.trellis/guru-team/scripts/bash/record-task-publication-review.sh`
    - `.trellis/guru-team/scripts/bash/check-task-publication-review.sh`
  - `verify-throwaway-install.sh:1502`、installer、extension manifest 与 ownership 证据均已使用 `94`。
  - 但 `test_throwaway_verifier_cleans_preview_and_scans_sidecars_after_reapply` 仍检查 verifier 包含字面量 `assert len(assets) == 92`。
- 独立复现：

  ```text
  python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py \
    PlatformOverlayInstallerTest.test_throwaway_verifier_cleans_preview_and_scans_sidecars_after_reapply

  Ran 1 test in 0.003s
  FAILED (failures=1)
  AssertionError: 'assert len(assets) == 92' not found
  ```

- 全套影响：

  ```text
  Ran 45 tests in 85.193s
  FAILED (failures=1)
  ```

- 修复建议：把该测试的 expected literal 从 `92` 更新为 `94`，然后至少重跑单方法、完整 preset suite、source/installed validator、ownership/drift 与 throwaway install。
- 未自修复原因：超出本轮唯一写权限；需要返回 implementation owner 处理。

### `BR116-R04-P1-01` 闭环判断

- Status：closed for the reported behavior
- 六种受支持 package layout 的 recorder/checker wrapper 都采用 exact root resolver：
  - canonical：`trellis/skills/guru-team/packages/<skill>`
  - installed shared：`.trellis/guru-team/skills/packages/<skill>`
  - `.agents/skills/<skill>`
  - `.codex/skills/<skill>`
  - `.cursor/skills/<skill>`
  - `.claude/skills/<skill>`
- 未设置 `GURU_TEAM_DISPATCHER` 的独立真实调用：
  - canonical recorder/checker：2/2 以 rc=2 在业务动作前 fail closed，错误包含 `not an audited installed or discovery layout`。
  - installed shared 与四个平台 recorder/checker：10/10 rc=0，且实际进入 interface 声明的 shared dispatcher runtime help。
- 六布局的 recorder/checker/test bytes 与 mode 一致；两个 installed runtime wrapper 和 canonical runtime wrapper 等字节且均为 `0755`。
- installed manifest：`managed_assets=94`、`skill_files=2100`、`sidecars=0`、`conflicts=0`、`removals=0`。
- throwaway：
  - `fresh-install: 10/10 publication validator wrappers reached shared help`
  - `after-trellis-update: 10/10 publication validator wrappers reached shared help`
  - `after-preset-reapply: 10/10 publication validator wrappers reached shared help`
  - 最终 exit 0，尾行：`Verified public marketplace discovery plus local unpublished workflow sample ...`
- 因此 R04 的“installed/platform wrapper 无 override 时错误落到 `<repo>/<runtime>`”行为缺陷已经修复；当前阻塞来自独立的新 P2 测试 expectation 漂移，不是该 P1 行为仍可复现。

### 语义与合同核对

- `guru-review-task-publication` 为 active `judgment_mode=semantic` Skill；global workflow 只 mandatory invoke 并路由三个 exit，没有复制 step-local 审查。
- AI owner 负责十个 publication dimensions、findings、结论、revision history、human confirmation 与 AI Review Gate；recorder/checker 不选择 route、dimension status 或 typed exit。
- recorder/checker 重建 12 个 entry preconditions；`ready` 对 entry error、artifact/status/diff/HEAD/review binding/Docs SSOT/content freshness 失败关闭。
- 当前 public input 为两个 closed profile：
  - `publication_review`
  - `publication_review_stale`
- 实际 owner `typed_exit` 驱动三个 closed minimal outputs：
  - `ready`
  - `return_to_task_work`
  - `blocked`
- `expected_exit` 只用于 checker / eval grading，不决定真实 public output。
- Registry closure 为 11 active Skills / 42 exits；仅 `guru-finalize-task` 保持 planned missing-Skill boundary。
- `production-minimal-handoff-v1` 仍严格保持 planning/check/commit 三包与 11 exits，没有把 publication Skill 错纳入既有 production manifest。
- Issue Scope Ledger 的 `close_issues` 仅含 #116；#115/#131/#144/#146 为 related，#81/#117/#118/#119/#132 为 follow-up，不会被本 task 误关闭。

### 验证结果

- Lint：通过
  - `bash -n`：canonical publication wrappers、installed runtime wrappers、preset apply 与 throwaway verifier 全部通过。
  - `python3 -m py_compile`：runtime、runtime tests、Skill tests、publication contract tests、preset tests、ownership tests 全部通过。
  - `git diff --check origin/main...HEAD` 与 dirty `git diff --check`：通过，无 whitespace error。
- TypeCheck：不适用
  - 本仓库当前相关 Python/Shell 范围无独立静态类型检查命令；已执行 Python compile、contract/schema validator 和完整测试。
- Tests：失败
  - Runtime full suite：`Ran 572 tests in 146.029s — OK (skipped=13)`。
  - Skill full suite：`Ran 174 tests in 263.777s — OK`。
  - Preset full suite：`Ran 45 tests in 85.193s — FAILED (failures=1)`，对应 `PH2-116-R8-P2-01`。
  - Ownership full suite：`Ran 9 tests in 0.710s — OK`。
  - Canonical publication package：`Ran 18 tests — OK`。
  - Installed publication package：`Ran 18 tests — OK`。
  - Source publication actual-wrapper eval：7/7 passed。
  - Installed publication actual-wrapper eval：7/7 passed。
  - Source package validator：passed，11 active / 42 exits。
  - Installed package validator：passed，managed files 2100，sidecar/removal/conflict 均为 0。
  - Upstream ownership validator：passed，43 frozen / 43 active overlays，5 reviewed current payloads，50 managed assets。
  - Dogfood overlay drift：passed。
  - Throwaway fresh install / update / reapply：exit 0；三阶段 publication wrappers 各 10/10。
  - Task context validation：passed，`implement.jsonl=9`、`check.jsonl=8`。
  - Final workspace boundary：passed；expected workspace 等于 actual repo root，source checkout clean，suspicious source artifacts 为空。
  - Final planning approval check：passed，`typed_exit=approved`，current HEAD=`1dd2ef8af1cf583eeaf302a11c4770a07922b0b2`。

### 证据交接

- 阶段二：
  - 覆盖了 Issue #116 当前 authority、批准规划、全部 curated specs、完整 committed diff、dirty finding-fix candidate、canonical/installed/platform copies、runtime、schema/API、registry、workflow、preset、ownership、durable docs 与 task artifacts。
  - `BR116-R04-P1-01` 的原始行为已经闭环。
  - 新发现 `PH2-116-R8-P2-01`，使 required full preset suite 失败。
  - 本报告可作为 `guru-check-task` 后续 semantic owner 记录 `implementation_required` 的 raw reviewer evidence；它不能支撑 `passed`，且本轮没有调用 Phase 2 recorder/checker。
- Docs SSOT：
  - 批准策略：`ssot_first`。
  - 当前 committed durable specs 已定义 public runtime wrapper、完整 preset 分发、installed/shared/platform 可运行、upgrade/update/reapply 与 OOTB 验收责任。
  - R04 修复遵从这些既有 durable contracts；本轮 resolver/inventory finding-fix 没有新增或改变语义合同，因此不需要新的 durable-doc delta。
  - `implementation-handoff.md` Section 11 和 Round 4 raw report 属于 task-history-only 证据。
  - 当前分支仍是 unpublished mutable ref；throwaway 只证明 public marketplace discovery 加 local unpublished workflow sample，不能冒充 merge/tag 后 exact remote branch 验证。该限制已在 durable docs 与 handoff 中明确。
  - `PH2-116-R8-P2-01` 是测试 expectation 漂移，不要求 durable spec 变更。
- Branch Review：
  - 本轮为 Phase 2 fresh check，不写 `review.md`、不调用 Branch Review recorder/validator，也不替代后续完整 committed Branch Review Gate。
  - 当前 dirty candidate 修复后必须重新通过 Phase 2、创建受审 commit，并由 Branch Review 对新的完整 `origin/<base>...HEAD` 与新 HEAD 独立复审。
- 部署与安全：
  - 变更影响 workflow/Skill/preset/CLI runtime distribution 与安装/更新链路。
  - 未发现 dependency、DB migration、container、Kubernetes、Makefile 或 CI/CD 变更。
  - 检查范围内未发现 credential、token、`.env`、签名 URL 或客户数据进入 task/public artifacts。
  - 本轮未执行 publish、push、PR、Issue close、archive、finish 或生产写入。

### 结论

`BR116-R04-P1-01` 已按真实六布局 wrapper 与 fresh/update/reapply 行为证据关闭，但当前候选仍有一个开放的正常路径 P2：preset 测试保留 92-file 旧断言，导致 required full preset suite 失败。

因此 Round 8 结论为：

```text
implementation_required
findings_count=1
open_findings=PH2-116-R8-P2-01
```

实现 owner 应先把 `test_apply_guru_team_trellis_preset.py:1051` 的 92 更新为 94，重跑相关验证，再发起 fresh Phase 2 check。当前不能记录 `phase2-check.json:passed`，也不能进入 task commit 或 Branch Review。
