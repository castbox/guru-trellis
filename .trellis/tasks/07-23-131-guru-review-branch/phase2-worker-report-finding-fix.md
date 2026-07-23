# Issue #131 finding-fix 独立阶段二复检

## 检查完成

### 检查身份与范围

- 检查角色：`trellis-check` 阶段二独立检查代理。
- Issue：`castbox/guru-trellis#131`。
- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/131-guru-review-branch`。
- Branch：`codex/131-guru-review-branch`。
- Intake base：`main` @ `ea132e350c4b6861fc955f17e590651a46e890ab`。
- 检查 HEAD：`ea132e350c4b6861fc955f17e590651a46e890ab`。
- Diff 范围：该 HEAD 上相对 `origin/main` 的完整未提交实现 diff；检查开始时为 56 个 tracked changed files，约 5146 insertions / 814 deletions，index 为空。
- Planning approval：确定性 validator 通过，来源为 `explicit-post-planning-review`，`typed_exit=approved`。
- Docs SSOT strategy：`ssot_first`。
- `check.jsonl` 仅含 seed row，因此按协议回退到 task planning artifacts 与 `implement.jsonl` 的 11 个 curated specs。
- 本轮只执行独立检查与写入本报告；未修改实现、durable docs、schema、配置、测试，未写 `phase2-check.json`，未 commit、push 或创建 PR。

### 已检查文件

- Task artifacts：`prd.md`、`design.md`、`implement.md`、`planning-approval.json`、`implementation-handoff.md`、`issue-scope-ledger.json`、`agent-assignment.json`、原 `phase2-worker-report.md` 与 `phase2-check.json`。
- Curated specs：`.trellis/spec/workflow/{workflow-contract,skill-package-contract,companion-scripts,data-contracts,quality-guidelines}.md`、`.trellis/spec/preset/{installer,upstream-ownership,overlay-guidelines}.md`、`.trellis/spec/docs/public-docs.md`、`.trellis/spec/guides/{cross-layer-thinking-guide,code-reuse-thinking-guide}.md`。
- Durable docs：`README.md`、`docs/requirements/**`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- Canonical implementation：`trellis/skills/guru-team/packages/guru-review-branch/**`、production migration manifest、registry、shared consumers、Interface 1.3 schema、native eval adapter、runtime recorder/checker/public projection。
- Distribution copies：`.trellis/guru-team/skills/packages/guru-review-branch/**`、`.agents/skills/guru-review-branch/**`、`.codex/skills/guru-review-branch/**`、`.claude/skills/guru-review-branch/**`、`.cursor/skills/guru-review-branch/**`。
- Workflow / preset / overlay / installer / ownership / tests 的当前完整 dirty diff。
- GitHub Issue #131 正文与 accepted-current 评论，以及 Trellis 官方 `index.md`、custom workflow、custom spec template marketplace 文档的当前在线版本。

禁止改动的现有 Phase 2 reviewer 路径保持零 diff：

- `.trellis/agents/check.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
- `.agents/skills/trellis-check/**`
- `.codex/agents/trellis-check.toml`
- `.claude/agents/trellis-check.md`
- `.cursor/agents/trellis-check.md`

### 历史 findings 复验

#### F-131-01：已验证修复

在 fresh `workflow-passed` fixture 中先确认 public wrapper 返回 `passed`，随后对 `prd.md` 做一次正常规划修订：

- `check-planning-approval.sh` 退出 2，报告 `contract_wording_scope_stale`、planning artifact digest/size/provenance/authority stale。
- public wrapper 随后返回且只返回 `{"exit_id":"blocked"}`。

结论：planning freshness 已进入 public invocation 的真实 fail-closed 路径。

#### F-131-02：已验证原 finding 的两部分均修复

在 fresh `standalone-passed` fixture 中将当前 task 的 `task-commit-plans/001.json` 移出 task：

- recorder dry-run 退出 2，报告 `review entry task commit evidence is missing`。
- public wrapper 返回且只返回 `{"exit_id":"blocked"}`。

在另一 fresh fixture 中正常制造 task-commit artifact 的 `message_sha256` mismatch，public wrapper 同样返回最小 `blocked`。

结论：缺失或 stale task-commit evidence 已被入口重验，原 F-131-02 的 task-commit 缺口已修复。与 reviewer assignment / raw report 有关的剩余协议缺口另列为 F-131-04。

#### F-131-03：已验证修复

在 fresh `finding-fix-passed` fixture 中：

- 正确 owner input 与真实 closure report 的 recorder dry-run 通过。
- `owner_round=99` 被 recorder 拒绝，报告 unknown assignment review round。
- 不存在的 `closure_evidence` 被 recorder 拒绝。
- 在 gate 后对登记的 closure raw report 做一次正常内容修订，checker 退出 2，报告 assignment / gate / closure digest stale。

结论：finding 的 owner round、closure evidence、assignment membership 与 report digest 已建立可重验绑定，原 F-131-03 已修复。

### 候选问题资格判定

| ID | 正常支持路径可复现 | 当前 scope 依据 | 处置 | 严重级别 |
| --- | --- | --- | --- | --- |
| C-004 | 是；通过态 finding-fix fixture 的已登记 raw closure report 发生普通内容修订后，checker 正确判 stale，但 public wrapper 返回 invocation error `owner_result_not_checked`，不是声明的最小 `blocked` | Issue #131 Entry Preconditions / Closed Loop；PRD R3、R7；design §5、§6.1、§10.2 | `qualified_finding` | P1 |
| C-005 | 是；当前 durable docs 同时把 production authoring-seed edge inventory 描述为 3 和 4，而 manifest / Interface / validator 实际为 4 | PRD R11、AC14、AC16；design §11.1、§12；`.trellis/spec/docs/public-docs.md` | `qualified_finding` | P2 |

下列项目未升级为 finding：

- 当前 feature branch 未推送，因此 throwaway 脚本默认拒绝把公开 marketplace `main` 当作当前 branch。使用显式允许的 public-marketplace sample 后，完整 clean init / existing switch / update / reapply 验证通过；精确 feature-ref marketplace 验证仍受当前未发布状态限制。
- npm 当前提示 Trellis CLI `0.6.8`，但本任务批准、manifest 声明与完整验证 baseline 是 `0.6.5`；未把未授权的新版兼容性扩张为当前 scope。
- 需要恶意伪造、攻击 artifact、TOCTOU 或并发压力才能构造的案例均未用于 finding。

### 已修复问题

- 本独立 reviewer 未修改实现。
- 历史 F-131-01、F-131-02、F-131-03 已由 implementation owner 修复，并由本轮使用真实 wrapper / recorder / checker fixture 独立复验。
- 测试产生的 7 个 repo-local `__pycache__` 目录已在检查后精确清理；这不是实现变更。

### 未修复问题

#### F-131-04 — P1：13 项入口合同仍未把 assignment / raw report stale 映射为稳定 `blocked`

事实：

- `design.md` §5 声明 workflow 与 standalone 共用 13 个 ordered preconditions，其中第 11 项是 `reviewer_assignment`、第 12 项是 `review_evidence`；PRD R3 要求 assignment、全部 task-local raw reports 与 recovery chain 的缺失、stale、digest mismatch 或 lifecycle 未闭合均失败关闭。
- `review_branch_entry_precondition_errors()` 当前重验 runtime、workspace/task、range、public input identity、task commit、planning、Phase 2、ledger、Docs SSOT 与 working tree，但没有重验第 11、12 项。
- Assignment / raw report 的 digest 绑定在后续 review-gate checker 中才执行。

正常复现：

1. 使用 fresh `finding-fix-passed` fixture，确认 gate 与 public wrapper 处于通过态。
2. 对已登记的 `.trellis/tasks/current/reviews/round-002-closure.md` 追加一次普通 review 修订。
3. `check-review-gate.sh` 正确退出 2，并报告 assignment / gate / closure report digest stale。
4. public wrapper 退出 2，返回 invocation error，错误码为 `owner_result_not_checked`；没有返回接口声明的 `{"exit_id":"blocked"}`。

影响：

- 13 项入口前置条件仅实现了 11 项到稳定 `blocked` route 的映射。
- 正常 reviewer report 修订或 assignment/report freshness 失效时，workflow consumer 无法依赖声明的 typed exit 进行稳定恢复。
- `blocked-stale` corpus 仍未覆盖 assignment / raw report 在通过后变 stale 的真实 public-wrapper 路径。

建议修复：

- 将 current assignment、全部 raw reports 与 lifecycle evidence 纳入显式 entry precondition 重验，或把仅属于这些客观 stale/missing 条件的 checker 结果确定性映射为最小 `blocked`。
- 保留 invalid locator、schema、unknown checker failure 等真正 invocation error 的独立语义。
- 增加“先通过、再普通修订 assignment 或 raw report、随后 public wrapper 必须只返回 `blocked`”的真实回归测试。

#### F-131-05 — P2：`ssot_first` durable docs 对 authoring-seed edge 数量自相矛盾

实现与新段落的正确当前事实是 4 条 authoring-seed edges：

- `.trellis/spec/workflow/skill-package-contract.md` 的 Issue #131 段落写明 `Exactly four semantic handoffs`。
- `.trellis/spec/preset/overlay-guidelines.md` 写明 4 个 target-owned authoring examples。
- `.trellis/spec/docs/public-docs.md` 与 `.trellis/spec/preset/installer.md` 写明 inventory 从 3 增长到 4。
- production manifest、Interface、consumer binding 与 validator 实际均实现 4 条；production migration membership 仍正确保持 3 Skills / 11 exits。

但以下 current-contract 文字仍声明只有 3 条：

- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `docs/requirements/README.md`
- `docs/requirements/guru-team-trellis-flow.md`
- `.trellis/spec/workflow/skill-package-contract.md` 的通用 production semantic edge 段落
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/installer.md` 的前置合同段落
- `.trellis/spec/preset/upstream-ownership.md`

影响：

- Approved Docs SSOT Plan 使用 `ssot_first`，实现必须以已修订的 durable docs 为主输入；当前 handoff 的“durable SSOT 已 current / 无 wording delta”结论不成立。
- 三个公开 README 没有满足 `.trellis/spec/docs/public-docs.md` 对当前 inventory 的同步要求。
- 新安装用户会从公开合同读到 3 条，但实际 package graph 为 4 条。

建议修复：

- 将所有描述“authoring-seed edge / authoring example inventory”的 current-contract 文字同步为 4。
- 保留“production migration membership 为 3 Skills / 11 exits”这一不同维度的正确事实，避免机械替换。
- 更新 implementation handoff 的 Docs SSOT reconciliation，并复跑公开文档、source / installed graph 与 throwaway 验证。

### 十维充分性结论

| 维度 | 结论 | 证据摘要 |
| --- | --- | --- |
| `requirements` | 通过 | Live issue、accepted-current、PRD 与 scope ledger 权威一致；两项开放问题均有当前 scope 依据 |
| `design` | 失败 | 设计声明 13 项入口条件统一 fail-closed，但 assignment / raw report stale 未进入稳定 `blocked` route |
| `implementation` | 失败 | F-131-04 的真实 public wrapper 行为不满足接口；F-131-05 的 durable docs 未完成实现前置同步 |
| `tests` | 失败 | 全量自动化通过，但没有覆盖“passing report 后变 stale 必须返回 blocked”与 durable-doc edge count 一致性 |
| `docs_ssot` | 失败 | `ssot_first` current-scope 文档同时声明 3 和 4 条 authoring edges |
| `cross_layer` | 失败 | Interface / manifest / validator 为 4，公开 README 与部分 spec 为 3；entry contract 与 wrapper route 不一致 |
| `compatibility` | 失败 | 声明的 stable `blocked` exit 对 assignment / report stale 场景仍不可达 |
| `deployment_and_operations` | 通过 | 无 CI/CD、container、Kubernetes、DB migration、Makefile 或业务 runtime infrastructure 变更 |
| `agent_recovery` | 通过 | 当前 implementation / finding-fix / check assignment chain 完整，无未闭合 recovery blocker |
| `verification_completeness` | 失败 | 已完成要求的全量命令与手工负例，但 1 个 P1、1 个 P2 仍开放 |

### 验证结果

| 验证项 | 结果 |
| --- | --- |
| `guru-review-branch` package tests | 通过，8 tests |
| source shared eval | 通过，7/7；actual exits 为 `passed, passed, implementation_required, scope_confirmation_required, blocked, passed, passed` |
| installed shared eval | 通过，7/7；actual exits 与 source 一致 |
| source package validator | 通过，10 active Skills / 39 exits / 23 targets |
| installed package validator | 通过，10 active Skills / 39 exits / 23 targets，1903 managed files，0 sidecar/removal/conflict |
| Skill full suite | 通过，166 tests |
| production runtime suite | 通过，560 tests，13 skipped |
| preset installer suite | 通过，45 tests |
| upstream ownership suite | 通过，6 tests |
| dogfood overlay drift | 通过，frozen 43 paths 未漂移 |
| canonical / installed / shared / Codex / Claude / Cursor package parity | 通过，内容 byte-identical；三条 wrapper executable mode 一致 |
| repo tracked JSON parse | 通过，419 files |
| repo tracked Bash syntax | 通过，89 files |
| Python compile | 通过，使用 repo 外部 cache root |
| `git diff --check` | 通过 |
| forbidden reviewer path diff | 通过，零差异 |
| source checkout | 通过，clean；无 suspicious task/worktree artifacts |
| strict secret / sensitive filename / absolute machine path scan | 通过，零命中 |
| `.new` / `.bak` / repo-local cache scan | 通过，零遗留 |
| full throwaway install / update / reapply | 通过，Trellis 0.6.5；public marketplace discovery + local unpublished workflow sample，覆盖 clean init、existing switch、`update --force`、preset 重放、43-path ownership、10/39/23 graph、1903 installed files、零 unresolved sidecar |

Lint：

- `git diff --check`、JSON parse、Bash syntax、Python compile、package validators 与 repo-defined tests 均通过。
- 当前环境未安装 `ruff`、`shellcheck`，仓库也未提供统一替代 lint 命令；不能把这些外部工具标记为“通过”。

TypeCheck：

- 当前环境未安装 `mypy`、`pyright`，仓库没有可执行的统一 type-check gate；记为“不适用/未提供”。
- Python compile 与 560 个 runtime tests 通过，但不替代 F-131-04 的 semantic contract 失败。

Tests：

- Repo-defined relevant suites、source/installed eval 与完整 throwaway 均通过。
- 语义充分性仍失败，因为 green suite 未覆盖 F-131-04 和 F-131-05。

### 证据交接

- 阶段二覆盖：完整当前 dirty diff、task artifacts、11 个 curated specs、live issue / accepted-current、官方 Trellis 文档、durable docs、canonical / installed / platform copies、runtime、schema、manifest、registry、config、installer、ownership 与 tests。
- 历史 findings：F-131-01、F-131-02、F-131-03 均已使用 fresh fixture 和真实 wrapper / recorder / checker 独立复验修复。
- 开放风险：F-131-04（P1）与 F-131-05（P2）均可在 honest-but-fallible 正常路径复现，属于 current acceptance，不是 hostile-input、TOCTOU 或范围扩张。
- Docs SSOT：strategy 为 `ssot_first`；package graph、copy parity 和 installer 一致，但 durable docs 对 3/4 authoring-edge inventory 自相矛盾，task delta merge 不能判完成。
- Upgrade / update：完整 throwaway 已覆盖官方 0.6.5 clean init、existing switch、update、workflow / preset 重应用与零 sidecar。因 feature branch 尚未推送，未验证精确远端 feature ref；脚本显式记录的是 public `main` marketplace sample 加本地未发布 workflow。
- 部署 / 安全：`production-minimal-handoff.json` 是 Skill activation manifest，不是 DB migration；无 runtime infrastructure、secret、credential、signed URL 或敏感样本影响。
- 当前旧 `phase2-check.json` 的 `implementation_required` 结论与本轮方向一致，但它不是本轮 passing evidence；本 reviewer 未写新 artifact。
- 本报告足以支撑 `guru-check-task:implementation_required`，不能支撑 `guru-check-task:passed` 或 passing `phase2-check.json`。

### 结论

历史三项 finding 的实现修复均已独立验证，但当前仍有 1 个 P1 和 1 个 P2：

1. assignment / raw report stale 没有按 13 项入口合同返回稳定最小 `blocked`。
2. `ssot_first` durable docs 对 authoring-seed edge inventory 同时声明 3 和 4。

因此本轮阶段二检查结论为 `implementation_required`。应由 implementation owner 修复 runtime / regression test 与 durable Docs SSOT，随后重新执行完整 Phase 2 check；当前不得进入 commit 或 Branch Review。
