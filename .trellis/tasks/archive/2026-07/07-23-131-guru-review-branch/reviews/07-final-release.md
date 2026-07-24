# Issue #131 Branch Review Round 7 最终放行原始报告

## 检查完成

### 审查身份与固定范围

- 逻辑角色：`最终放行审查代理`，round 7。
- Technical agent：`/root/issue_131_branch_review_final2`。
- 独立性：本 agent 未参与实现、Phase 2、round 1-6 审查或历史 finding
  修复；assignment 将其登记为当前 HEAD 上的新鲜最终审查代理。
- Task：`.trellis/tasks/07-23-131-guru-review-branch`。
- Base：`origin/main`。
- Base HEAD / merge base：
  `ea132e350c4b6861fc955f17e590651a46e890ab`。
- Reviewed HEAD：
  `f4e2a62b8264dceb5078fd3ceb2caa3e46c97a53`。
- 完整审查范围：
  `origin/main...f4e2a62b8264dceb5078fd3ceb2caa3e46c97a53`。
- 完整 diff：320 files changed，35007 insertions，1068 deletions。
- Branch：`codex/131-guru-review-branch`。
- Workspace boundary：expected workspace 与 actual repo root 均为当前 task
  worktree；source checkout clean；task worktree 状态符合 Branch Review metadata
  tail；suspicious source artifacts 为 0。

本轮开始时已存在 main-session 管理的 metadata 变化：

- modified
  `.trellis/tasks/07-23-131-guru-review-branch/agent-assignment.json`
- modified
  `.trellis/tasks/07-23-131-guru-review-branch/task-commit-plans/004.json`
- untracked
  `.trellis/tasks/07-23-131-guru-review-branch/reviews/06-finding-closure.md`

本 agent 只新增本 raw report。未修改实现、测试、规划、durable docs、
`phase2-check.json`、`review.md`、`review-gate.json`、assignment 或 task commit
plan；未执行 Guru Team recorder/gate validator，未 commit、push、创建或修改 PR。

### 前置证据

- GitHub Issue `castbox/guru-trellis#131` 当前仍为 open；accepted-current
  authority 继续要求 active `guru-review-branch` 独占 Branch Review step-local
  closed loop，global workflow 与平台入口只负责加载、调用和 typed routing。
- 官方 Trellis 当前文档继续确认 `.trellis/workflow.md` 是运行时读取的 workflow
  合同；本仓库扩展应在官方 marketplace/workflow/preset 面上实现。
- `planning-approval.json` 为 schema 2.0、`typed_exit=approved`，
  `ambiguity_review.status=passed`，fixed-scope scanner 没有 unchecked
  normative hit，confirmation 来自显式 post-planning review。
- 当前 planning 内容 digest 与 approval 精确匹配：
  - `prd.md`：
    `6ad8c1137377203441afacc4bd2a1db03e2564cd6f47b1a23c16e1ba612902ec`
  - `design.md`：
    `9b7db338b6c34ed261db10a22b07803fa4950929fbdfecf7dc741da980c5efce`
  - `implement.md`：
    `fa902098b919fa30d8d5a9fee028eb9074f2e40b0cb1a42e4c6530efc2ec53cc`
- `phase2-check.json` 为 schema 2.0、`typed_exit=passed`，记录
  `full_rerun=true`；历史 `F-131-BR4-01` 与 `F-131-P2-R5-01` 均被标记为
  resolved。
- `task-commit-plans/004.json` 绑定当前 commit、parent 与 tree；当前 commit
  tree 与计划中的 expected/actual tree 一致。
- `check.jsonl` 只有 seed row，因此按 reviewer fallback 读取了完整 task
  artifacts，并用 `get_context.py --mode packages` 选择 workflow、preset、
  layers 与 docs specs。

这些证据使 round 7 具备 fresh final review 的 entry qualification，但不预先决定
semantic pass。

### 已检查文件

- Live Issue #131、accepted-current comment、官方 Trellis workflow 与
  marketplace 文档。
- `.trellis/tasks/07-23-131-guru-review-branch/{prd.md,design.md,implement.md}`。
- `.trellis/tasks/07-23-131-guru-review-branch/{planning-approval.json,implementation-handoff.md,phase2-check.json,review.md,agent-assignment.json}`。
- `.trellis/tasks/07-23-131-guru-review-branch/task-commit-plans/004.json`。
- `.trellis/tasks/07-23-131-guru-review-branch/reviews/01-problem-discovery.md`。
- `.trellis/tasks/07-23-131-guru-review-branch/reviews/02-finding-closure.md`。
- `.trellis/tasks/07-23-131-guru-review-branch/reviews/03-finding-closure.md`。
- `.trellis/tasks/07-23-131-guru-review-branch/reviews/04-final-release.md`。
- `.trellis/tasks/07-23-131-guru-review-branch/reviews/05-problem-discovery.md`。
- `.trellis/tasks/07-23-131-guru-review-branch/reviews/06-finding-closure.md`。
- `.trellis/spec/workflow/{index.md,workflow-contract.md,skill-package-contract.md}`。
- `.trellis/spec/docs/public-docs.md`。
- `.trellis/spec/preset/{installer-contract.md,upgrade-update-contract.md}` 及相关
  layers specs。
- `trellis/workflows/guru-team/{workflow.md,README.md}` 与 dogfood
  `.trellis/workflow.md`。
- `trellis/skills/guru-team/registry.json`、interface/schema/migration manifests、
  active packages、wrappers、eval corpus 与 tests。
- Canonical `trellis/presets/guru-team/` installer、ownership、README、overlays
  与 platform entry copies。
- Installed `.trellis/guru-team/` packages/scripts/schema/config 及
  `.agents/`、`.codex/`、`.claude/`、`.cursor/` selected-platform copies。
- 完整 committed diff
  `origin/main...f4e2a62b8264dceb5078fd3ceb2caa3e46c97a53`，不是只检查
  latest commit。

### 历史 finding 闭环复核

- Phase 2 `F-131-01..05`：closed。
- Round 1 `F-131-BR-01..04`：closed。
- Round 2 `F-131-BR2-01`：closed。
- Round 4/5 `F-131-BR4-01`：round 6 closure 在当前 HEAD 上有效；canonical
  与 dogfood global workflow 已 byte-identical 且 Phase 3.5 routing-only。
- Phase 2 `F-131-P2-R5-01`：round 6 closure 在当前 HEAD 上有效；throwaway
  public sample 与 exact/current source preview 已分开验证。

本轮没有重开上述历史 finding。下述两项是 fresh full-range review 新发现的
current-scope finding。

### 候选资格化

- `C-131-BR7-01`：平台 continue entry 在普通任务继续路径中必然被加载，无需
  伪造 artifact 或 hostile input 即可观察到相互矛盾的 Branch Review ownership
  文案；分类为 `normal_required_behavior`，进入 finding。
- `C-131-BR7-02`：public/durable docs 在正常阅读、安装和 upgrade/update
  指引路径中直接给出相互矛盾的 active package 状态；分类为
  `normal_required_behavior`，进入 finding。
- Exact remote feature-ref marketplace install：当前 feature branch 未获 push
  授权且远端 ref 不存在；这是 publication 前的验证限制，不证明本地实现缺陷，
  不赋 severity，也不是 scope proposal。
- 独立 `ruff` / `shellcheck`、`mypy` / `pyright`：仓库未声明这些 gate；
  保留为未配置项，不伪装成通过，也不赋 severity。
- 恶意 artifact/hash/state 篡改、对抗输入、TOCTOU、锁、并发压力、fault
  injection、crash consistency 与跨 OS atomicity：无法在批准的 supported
  normal path 中复现，按明确 authority 为 `out_of_scope`。

### 已修复问题

- 无。Branch Review 为 review-only；本轮发现不能由最终审查代理修改。

### 未修复问题

#### F-131-BR7-01 — P2 — Platform continue entries 仍复制 Branch Review step-local 合同

- 分类：`normal_required_behavior`。
- 影响：current acceptance blocker；不是 scope proposal。
- 主要路径：
  - `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
  - `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md`
  - `trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md`
  - `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md`
  - `trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md`
  - 对应 installed `.agents/`、`.codex/`、`.claude/`、`.cursor/` copies。
- 当前证据：
  - `.agents/skills/trellis-continue/SKILL.md:21` 正确声明 active
    `guru-review-branch` 独占 reviewer dispatch、qualification、artifacts、
    finding closure、fresh final、recorder/checker、freshness 与 re-entry，并明确
    “entry must not reproduce or reconstruct those rules”。
  - 同文件 `:40-43` 又声明 entry 不应直接调用 Branch Review recorder/checker。
  - 但同文件 `:47` 仍完整规定 `review-branch.sh` 的 post-commit audit、
    Branch Review metadata 白名单、何时返回 Phase 2、review evidence 缺失时的
    fail-closed 等 step-local 行为。
  - `.codex/prompts/trellis-continue.md:15` 与 `:34-37` 有同样的新 ownership
    声明，`:41` 仍保留同样的 legacy Branch Review paragraph。
  - canonical overlay 与 installed entry copies 通过 drift 检查保持一致，所以
    该重复不是单个 dogfood 文件偶然漂移，而是由 preset 正常分发的公共入口行为。
- 违反合同：
  - AGENTS §3.1 要求 platform entry 只加载、调用和路由，不复制 step-local skill
    内部步骤。
  - PRD R4/R11、AC13/AC15/AC16，Design §2/§9，Implement Step 6/8 均要求
    `guru-review-branch` 成为唯一 Branch Review 行为 SSOT，并要求 command/prompt/
    entry 保持 dispatcher-only。
  - 同一个 entry 自身的新句与旧段落也直接矛盾，使 agent 无法只按一个权威合同
    执行 normal continue path。
- 测试缺口：
  - `test_branch_review_workflow_is_routing_only_in_source_and_dogfood` 只扫描
    global workflow，没有扫描 platform continue entries。
  - 当前 platform-entry routing regression 只覆盖 task-commit ownership，未固定
    Branch Review 禁止词与 thin-entry 合同。
- 建议闭环：
  - 从 canonical overlay entry 中删除 Branch Review 专属 legacy paragraph，或收敛
    为 active package invocation、typed exits 与唯一 consumer route。
  - 重新应用 preset 同步 installed copies，确认无 `.new` / `.bak`。
  - 新增 canonical/installed/platform entry regression，禁止
    `review-branch.sh`、Branch Review artifact schema、closure/final-review
    细则在 entry 中复现，同时保留一次 package invocation 与四个 typed routes。

#### F-131-BR7-02 — P3 — Docs SSOT 仍把当前 10 个 active packages 写成 9 个且未完整公开新 owner

- 分类：`normal_required_behavior`。
- 影响：current-scope Docs SSOT blocker；不是 scope proposal。
- 当前证据：
  - `.trellis/spec/workflow/skill-package-contract.md:107-109` 写
    “All nine current production packages”，`:123` 再写
    “all nine active production packages”。
  - `.trellis/spec/workflow/index.md:39-44` 写 interface 1.3 对全部 9 个
    workflow packages active。
  - `README.md:964-965` 写 9 个 production packages 却同时写全部 39 exits；
    当前 validator 的真实状态是 10 active packages / 39 exits。
  - `trellis/presets/guru-team/README.md:225-232` 相邻内容先写 active closure
    10/39，再写 transaction 只安装 9 包 public contracts。
  - 同 README `:342-346` 的 active registry 列表遗漏
    `guru-approve-task-plan`、`guru-check-task` 与 `guru-review-branch`。
  - `trellis/workflows/guru-team/README.md` 与
    `trellis/presets/guru-team/README.md` 没有 exact `guru-review-branch` 名称；
    preset README `:636-672` 仍直接叙述旧的 Branch Review script、finding
    closure、fresh final 与 gate lifecycle，却没有说明 active package 是唯一
    semantic owner。
  - `.trellis/spec/docs/public-docs.md:342-354` 明确要求三个 public README
    表述 10 active packages / 39 exits，并命名 active `guru-review-branch`
    consumer；`:372-376` 再要求 #131 后三个 README 都识别它为 Phase 3.5
    semantic owner。
- 违反合同：
  - Approved Docs SSOT strategy 为 `ssot_first`，Design §12.1 将这些 durable
    specs 与三个 public README 都列入当前任务同步范围。
  - implementation handoff 与 `phase2-check.json` 声明 task delta 已合并且
    `docs_ssot_plan.task_delta_merged=true`；当前内容证明该结论不完整。
  - Branch Review 规则要求 current-scope Docs SSOT inconsistency 作为 blocking
    finding 返回，reviewer 不得在本轮首次替实现合并 durable docs。
- 建议闭环：
  - 把所有 current-state package 数量统一为 10 active / 39 exits，并明确
    `production-minimal-handoff-v1` 自身三包/11 exits 身份没有因 #131 改写。
  - 更新三个 public README 的 active registry/owner/upgrade-update 描述，命名
    `guru-review-branch` 为 Phase 3.5 semantic owner，并把 script 说明降为
    package-owned recorder/validator implementation detail。
  - 添加 public docs regression，验证三个 README 都包含 10/39 与 exact active
    owner，且不存在 current-state “nine active/production packages”。

### 验证结果

| 验证项 | 终态 |
| --- | --- |
| Live Issue #131 与 accepted-current authority | open/current；无新增 scope |
| Workspace boundary | passed；expected=actual task worktree；source clean |
| Planning approval digests | passed；prd/design/implement 精确匹配 |
| `git diff --check origin/main...HEAD` | passed |
| `git diff --check origin/main` | passed |
| Runtime full suite | 566 tests passed，13 skipped，151.320s |
| Skill package full suite | 169/169 passed，194.525s |
| Preset installer suite | 45/45 passed，78.122s |
| Upstream ownership suite | 6/6 passed |
| `guru-review-branch` package contract | 8/8 passed |
| Source shared real-wrapper eval | 7/7 passed；四类 actual exits 符合合同 |
| Installed shared real-wrapper eval | 7/7 passed；与 source 一致 |
| Source package validator | passed；10 active / 39 exits / 23 targets |
| Installed package validator | passed；10 active / 39 exits / 23 targets；1903 managed files；0 sidecar/removal/conflict |
| Dogfood overlay drift | passed；43 frozen/active paths；0 removed |
| JSON parse | 所有 tracked JSON 通过 |
| Shell syntax | 所有 tracked shell files 通过 `bash -n` |
| Python in-memory compile | 116 files passed |
| Task validation | passed；`implement.jsonl` 11 entries，`check.jsonl` 0 entries |

Lint：

- `git diff --check`、JSON parse、shell syntax、package/preset/ownership/drift
  validators 均通过。
- 仓库未配置独立 `ruff` / `shellcheck` gate，故不表述为通过。

TypeCheck：

- 仓库未配置 `mypy` / `pyright` gate；116 个 Python 文件 compile 与 runtime
  tests 通过，但不能替代独立 type-check。

Tests：

- 全部已运行 test suites 与 source/installed real-wrapper eval 终态通过。
- 这些机械结果证明 package/runtime/preset 当前可执行，但不能消除
  `F-131-BR7-01` 的第二份行为权威或 `F-131-BR7-02` 的 Docs SSOT
  current-state 矛盾。

开箱即用 / upgrade-update：

- 本轮 fresh 重跑 preset suite、ownership suite、source/installed validators、
  source/installed shared eval 与 dogfood drift，全部通过。
- 完整 throwaway 没有在 round 7 再次重复执行；同一 implementation tree 的
  fresh Phase 2 已覆盖 fresh init、existing preview/switch、update/reapply 与
  sidecar 清理。本报告只引用该同树证据，不冒充本轮独立重跑。
- Exact remote feature-ref install 仍需获得 push 授权且远端 ref 存在后复验；
  当前没有因此扩大授权、push 或发布。

### 证据交接

- 阶段二：planning、implementation handoff、Phase 2、commit tree 与历史 finding
  closure 均能与 current HEAD 连续绑定；验证命令终态为 green。但 round 7 fresh
  semantic review 发现两个 Phase 2 未覆盖的 current-scope issue，因此现有
  `phase2-check.json` 不能支持当前 Branch Review pass；修复后需要 fresh
  implementation、Phase 2、commit 与 review 闭环。
- Docs SSOT：plan strategy 是 `ssot_first`。代码/registry/validators 的真实状态为
  10 active packages / 39 exits，task artifact 却把 docs merge 记为完成；durable
  contract 和 public README 仍有 9-package/current-owner 漂移。结论为
  `task_delta_merged` 尚未真实满足，`F-131-BR7-02` 阻塞。
- Branch Review：
  - diff 范围：
    `origin/main...f4e2a62b8264dceb5078fd3ceb2caa3e46c97a53`
  - reviewed HEAD：
    `f4e2a62b8264dceb5078fd3ceb2caa3e46c97a53`
  - P0=0，P1=0，P2=1，P3=1
  - observations/follow-up candidates：exact remote feature-ref install 待发布授权后
    复验；不赋 severity。
  - scope proposals：0。
  - typed exit 建议：`implementation_required`。
  - 本 raw report 不能支持 passing `review.md` 或 Branch Review Gate；main
    session 应先路由实现闭环，不能运行 pass recorder。

### 部署与安全影响

- 完整 range 没有 GitHub Actions、Docker/Compose、Kubernetes/Kustomize、
  业务数据库 migration、Makefile 或生产配置变化。
- `production-minimal-handoff.json` 是 Skill API migration manifest，不是数据库
  migration。
- 未观察到 secret、credential、private key、`.env`、客户数据或签名 URL
  泄露。
- 本轮没有生产写、部署、archive、push、PR mutation 或 issue close。

### 结论

Round 7 fresh final review 未放行。

- `F-131-BR7-01`：P2，platform continue entries 在 normal path 中继续复制
  `guru-review-branch` 的 Branch Review step-local 合同。
- `F-131-BR7-02`：P3，Docs SSOT 与 public README 没有真实完成 10/39 和 active
  owner 同步。

当前共有 P2 1 项、P3 1 项未闭环；没有 P0/P1，没有 scope proposal。虽然 lint-like
checks、tests、validators 与 eval 全部通过，semantic ownership 与 Docs SSOT
finding 仍使 Branch Review Gate 必须 fail closed。建议唯一 typed exit 为
`implementation_required`；修复后重新执行 fresh Phase 2、commit、finding closure
与独立最终审查。
