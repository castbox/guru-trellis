# Issue #131 Branch Review Round 4 最终放行原始报告

## 检查完成

### 审查身份与固定范围

- 逻辑角色：`最终放行审查代理`，round 4。
- Technical agent：`/root/issue_131_branch_review_final`。
- Independence：本 agent 未参与实现、Phase 2、round 1 问题发现或 round 2/3
  问题闭环；assignment 中 round 3 → round 4 使用 `new-agent`。
- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Base：`origin/main`。
- Base HEAD / merge base：
  `ea132e350c4b6861fc955f17e590651a46e890ab`。
- Reviewed HEAD：`38a0e8dd2314b086378e0674f4bd377dc5e6f694`。
- 完整范围：
  `origin/main...38a0e8dd2314b086378e0674f4bd377dc5e6f694`。
- 完整 diff：315 files changed，33022 insertions，933 deletions。
- Commit history：
  - `cdf0fa47d3d6f508851b9c0e91260276d9fde8f5 feat(workflow): #131 建立分支审查闭环`
  - `0fdbb708f91296847b5812c3c1b9dd80b6e488a2 fix(workflow): #131 闭环分支审查问题`
  - `38a0e8dd2314b086378e0674f4bd377dc5e6f694 fix(workflow): #131 绑定精确闭环轮次`
- Workspace boundary：expected workspace 与 actual repo root 均为当前 task
  worktree；source checkout clean；suspicious source artifacts 为 0。

本轮只写本 raw report。未修改实现、测试、规划、durable docs、
`review.md`、`review-gate.json`、`agent-assignment.json`、
`phase2-check.json` 或 task commit evidence；未 commit、push、创建或修改 PR。

### 已检查文件

- Live authority：GitHub Issue `castbox/guru-trellis#131` 正文与 accepted-current
  comment `issuecomment-5045031945`。
- Planning 与 task artifacts：
  - `prd.md`
  - `design.md`
  - `implement.md`
  - `planning-approval.json`
  - `contract-wording-review.json`
  - `issue-scope-ledger.json`
  - `implementation-handoff.md`
  - `phase2-check.json` 与 Phase 2 raw reports
  - `task-commit-plans/001.json`、`002.json`、`003.json`
  - `agent-assignment.json`
  - `reviews/01-problem-discovery.md`
  - `reviews/02-finding-closure.md`
  - `reviews/03-finding-closure.md`
  - `review.md` 与 `review-gate.json`
- Canonical、installed 与 platform package：
  - `trellis/skills/guru-team/packages/guru-review-branch/**`
  - `.trellis/guru-team/skills/packages/guru-review-branch/**`
  - `.agents/skills/guru-review-branch/**`
  - `.codex/skills/guru-review-branch/**`
  - `.claude/skills/guru-review-branch/**`
  - `.cursor/skills/guru-review-branch/**`
- Runtime 与 eval：
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - `.trellis/guru-team/scripts/python/guru_team_trellis.py`
  - `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
  - canonical/installed `native_adapter.py`
  - shared wrapper、recorder、checker 与 package eval corpus
- Workflow、distribution 与 upgrade：
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
  - `trellis/presets/guru-team/**`
  - `.trellis/guru-team/extension.json`
  - canonical/installed registry、migration manifests、schemas、ownership inventory
  - Codex、Claude、Cursor 与 shared distribution copies
- Durable Docs SSOT：
  - `.trellis/spec/workflow/**`
  - `.trellis/spec/preset/**`
  - `.trellis/spec/docs/public-docs.md`
  - `README.md`
  - `docs/requirements/**`
- 完整 `origin/main...HEAD` 中的 task artifacts、代码、schema、config、脚本、测试、
  docs、preset、overlay、migration manifest 与 publish/finish 接口影响；禁止修改的
  upstream reviewer 六组路径保持零 diff。

### 历史问题闭环

| Finding | 历史严重度 | 闭环证据 | 当前结论 |
| --- | --- | --- | --- |
| `F-131-01..05` | P1/P2 | fresh Phase 2 对 planning freshness、13-entry、lifecycle、objective evidence route、4 authoring edges 完整复核 | closed |
| `F-131-BR-01` | P1 | round 2 真实 replacement recovery fixture | closed |
| `F-131-BR-02` | P2 | round 2 精确 task metadata/runtime input allowlist 回归 | closed |
| `F-131-BR-03` | P2 | round 2 current-scope no-defect `rejected_candidate` 回归 | closed |
| `F-131-BR-04` | P3 | round 2/3 `git diff --check` | closed |
| `F-131-BR2-01` | P2 | round 3 exact `expected_closure_round` 绑定与 6-case 回归 | closed |

Round 3 对 `F-131-BR2-01` 的闭环仍成立：per-finding lifecycle 传入 exact
`closure_number`，branch-global final validator 保留原全局语义；same-agent、
new-agent、replacement 与 final-review 路径均有回归。本轮没有重新打开任何历史
finding。

### 候选资格化

| Candidate | Scenario | Disposition | Severity | 结论 |
| --- | --- | --- | --- | --- |
| `C-131-BR4-01` | `normal_required_behavior` | `qualified_finding` | P2 | 全局 workflow 仍复制 Branch Review step-local 内部合同 |
| `C-131-BR4-02` | `out_of_scope` | `followup_candidate` | 无 | branch 未 push，exact remote feature-ref marketplace install 尚不可验证 |
| `C-131-BR4-03` | `out_of_scope` | `observation` | 无 | 仓库未配置且环境无 `ruff`、`shellcheck`、`mypy`、`pyright` |
| `C-131-BR4-04` | `out_of_scope` | `rejected_candidate` | 无 | hostile tamper、恶意伪造、TOCTOU、额外并发或原子性加固不属于当前批准范围 |
| `C-131-BR4-05` | `normal_required_behavior` | `rejected_candidate` | 无 | exact closure round、13-entry、public/private DTO、actual-exit、copy parity 与 upgrade/update evidence 未发现新缺陷 |

### 已修复问题

无。Branch Review 角色不得继续实现或首次修复 Docs SSOT 不一致；本轮未修改
implementation files。

### 未修复问题

#### `F-131-BR4-01` — P2：全局 workflow 仍复制 Branch Review step-local 内部合同

- Scenario class：`normal_required_behavior`。
- Disposition：`qualified_finding`。
- Affected paths：
  - `trellis/workflows/guru-team/workflow.md`
  - `.trellis/workflow.md`
- Requirement refs：
  - `prd.md:11-17`：`guru-review-branch` 是完整分支审查唯一 step-local
    SSOT；全局 workflow 只保留 mandatory invocation、四个 exits、consumer 与 stop。
  - `prd.md:196-199` / `prd.md:268-269`：R11 与 AC13 要求 workflow 不再复制
    Branch Review 内部合同。
  - `implement.md:121-137`：Phase 3.5 收敛 checkpoint 要求 workflow 不含
    step-local Branch Review checklist。
  - `.trellis/spec/workflow/workflow-contract.md:20-25`：workflow prose 不得复制
    package 的 step-local closed loop。
  - `.trellis/spec/workflow/workflow-contract.md:945-961`：reviewer prompt、
    qualification、severity、finding closure、final-review freshness、artifact
    construction 与 recovery 均属于 `guru-review-branch`，不得复制到 workflow。
- Normal-path evidence：
  - Phase 3.5 主段 `workflow.md:1170-1201` 已正确改为 mandatory invocation 与
    四个 exits。
  - 但同一全局 workflow 的 companion helper 示例
    `workflow.md:250-260` 仍给出直接调用
    `review-branch.sh --pass` / `check-review-gate.sh` 的可执行路径。
  - `workflow.md:302-366` 仍复制 reviewer role/independence、raw report、
    liveness/recovery、finding owner、fresh final review、post-commit Phase 2 audit、
    recorder/checker、artifact digest、`--finding`/`--observations` 等 Branch Review
    step-local 规则。
  - Canonical 与 dogfood workflow byte-identical，因此新安装和当前运行副本同时携带
    该重复合同。
- Qualification reason：
  这是普通 main-session 按当前 workflow prose 执行时可达的支持路径；不需要手工伪造
  artifact、恶意绕过、攻击 hash、TOCTOU 或并发压力。旧直调示例与重复的 reviewer /
  closure / recorder 规则会继续把 workflow 作为第二个 Branch Review 行为 SSOT，
  与 active Skill owner 形成双重权威，并可能引导调用方绕过 package mandatory
  invocation 直接进入 recorder。
- Impact：
  Issue #131 的核心 SSOT migration 未完整完成，AC13 不成立。Durable contract 已正确
  声明 step-local owner，但 canonical/dogfood workflow 仍与其不一致，因此当前
  `ssot_first` reconciliation 不能判为通过。
- Severity：
  P2。公共 workflow 的当前 normal path 与批准合同冲突，影响新安装和 dogfood
  运行时的流程权威；现有 validators 只验证 marker graph，无法用 green suite 消除该
  语义缺口。
- Required closure：
  删除或改写全局 workflow 中 Branch Review 专属的 helper 直调示例与 step-local
  reviewer/qualification/closure/final-review/artifact/recorder 细节，只保留真正跨 Skill
  的全局 sub-agent 原则与 Phase 3.5 typed routing。随后同步 dogfood workflow，执行完整
  Phase 2、fresh task commit、问题闭环审查，并由另一个未参与此前审查/闭环的 fresh
  最终放行代理复核完整新 HEAD。

### 验证结果

- Lint：通过（`git diff --check`、2631 个 tracked JSON、295 个 tracked Bash
  syntax 均通过；`ruff` / `shellcheck` 未配置且当前不可用）。
- TypeCheck：不适用/未配置（`mypy` / `pyright` 当前不可用；116 个 tracked Python
  文件 `py_compile` 通过，cache 写入 repo 外临时目录）。
- Tests：通过，但不能替代上述 semantic finding。

| 验证项 | 本轮 fresh final 结果 |
| --- | --- |
| `git diff --check origin/main...38a0e8dd...` | passed，exit 0 |
| `ReviewGateReportTest` focused matrix | 74/74 passed |
| `guru-review-branch/tests/test_contract.py` | 8/8 passed |
| `test_skill_packages.py` | 167/167 passed |
| `test_guru_team_trellis.py` | 566 passed，13 skipped |
| Preset installer tests | 45/45 passed |
| Upstream ownership tests | 6/6 passed |
| Source shared real-wrapper eval | 7/7 passed |
| Installed shared real-wrapper eval | 7/7 passed |
| Eval actual exits | `passed` / `implementation_required` / `scope_confirmation_required` / `blocked` |
| Source package validator | passed；10 active Skills / 39 exits / 23 targets / 1 planned |
| Installed package validator | passed；10/39/23；1903 managed files；0 sidecar/removal/conflict |
| Dogfood overlay drift | passed；43 active ownership paths，48 managed assets |
| Task context validation | passed；implement 11 / check 0 |
| Canonical/installed/platform package parity | passed；6 copies byte-identical |
| Canonical/installed runtime、adapter parity | passed |
| Canonical/dogfood workflow parity | passed；该 parity 同时证明 finding 影响两侧 |
| Forbidden upstream reviewer diff | 0 |
| Sensitive token / public local absolute path scan | 0 |
| Recursive `.new` / `.bak` / `.orig` / `__pycache__` / `.pyc` scan | 0 |
| Git index | empty |

### 未验证项

- Exact remote feature-ref marketplace install：未验证。远端
  `codex/131-guru-review-branch` 尚不存在且本轮无 push 授权，不能用 public `main`
  冒充当前 feature ref。
- Full throwaway install/update/reapply：本轮没有重复执行。Fresh Phase 2 已在组成当前
  commit 的同一 implementation tree 上以 Trellis 0.6.5 完成 full throwaway，覆盖
  clean init、existing preview/switch、real wrapper/eval、`trellis update --force`
  与 preset reapply；该证据是 fresh Phase 2 evidence，不表述为 round 4 独立重跑。
- `ruff`、`shellcheck`、`mypy`、`pyright`：仓库未声明 executable gate且当前环境不可用。
- Publication：`guru-review-task-publication` 仍为 planned/missing，PR/push/archive
  不在 #131 当前授权内，本轮未执行也不声称验证。

### 证据交接

- Branch Review range：
  `origin/main...38a0e8dd2314b086378e0674f4bd377dc5e6f694`，完整覆盖三个
  commits、315 个 changed files 与当前 task metadata tail。
- Historical closure：Phase 2 的 `F-131-01..05`、round 1 的
  `F-131-BR-01..04`、round 2 的 `F-131-BR2-01` 均保持 closed。
- Round 4 new findings：
  - P0：0
  - P1：0
  - P2：1
  - P3：0
- Scope proposals：0。
- Docs SSOT：plan strategy 为 `ssot_first`。Durable docs、package contract、
  runtime、schema、tests 与 distribution 的大部分 task delta 已合并；但
  `F-131-BR4-01` 证明 canonical/dogfood workflow 仍保留 step-local Branch Review
  内部合同，因此 current-scope Docs SSOT reconciliation 为 blocking inconsistent。
- Deployment impact：本 diff 不修改 `.github` CI/CD、Docker/Compose、Kubernetes /
  Kustomize、database migration、Makefile、业务 service、runtime config 或生产数据；
  `production-minimal-handoff.json` 是 Skill activation manifest，不是数据库
  migration。无需部署迁移或 rollback。
- Safety impact：未发现 secret、credential、private key、`.env`、签名 URL、客户数据
  或本机绝对路径进入公共 package；未执行外部写、生产写、push、PR 或 issue close。
- Observations：外部 lint/typecheck 工具与 exact remote feature-ref 验证限制已明确，
  均不用于降低或提高 current finding severity。
- Follow-up candidates：沿用 ledger 中 `#116` 与 `#132`；本轮没有新增 scope
  proposal，也没有把已排除的 hostile/concurrency 场景列为 required follow-up。
- Gate support：本报告可供 main session 记录 fresh final round 的
  `implementation_required` 结论及 `F-131-BR4-01`；不能支持
  `guru-review-branch:passed`、passing `review-gate.json` 或 Branch Review Gate
  放行。

### 结论

最终放行审查已完成，但当前 HEAD 不能放行。全部历史 findings 已关闭，round 4 在
normal supported path 中发现 1 个新 P2：全局 workflow 仍复制并暴露
`guru-review-branch` 已拥有的 step-local 内部合同，违反 Issue #131 的核心
SSOT migration 与 AC13。

建议 typed exit 为 `implementation_required`。必须先修复
`F-131-BR4-01`，重新执行完整 Phase 2 与 task commit，再完成 finding closure 和一个
全新的最终放行轮次；当前报告不支持 Branch Review Gate `passed`。
