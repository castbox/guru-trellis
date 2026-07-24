# #131 实施计划：guru-review-branch 闭环 Skill

## 1. 实现前门禁

- [ ] `guru-review-contract-wording:planning_artifacts` 对 current `prd.md`、
  `design.md`、`implement.md` 返回 checker-passed `pass`。
- [ ] `guru-approve-task-plan` 完成九个 entry preconditions、adequacy、provenance、
  unusual-scenario与 AI Review Gate。
- [ ] 用户查看三份 current planning links并给出独立 `post-planning-approval`。
- [ ] Main session记录 schema 2.0 `planning-approval.json`，checker验证
  `typed_exit=approved` 后运行 `task.py start`。
- [ ] Workspace boundary固定为
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/131-guru-review-branch`，
  branch固定为 `codex/131-guru-review-branch`，base固定为 `main`。
- [ ] `trellis-before-dev` 加载 current task `implement.jsonl` specs。
- [ ] Implementation由 `trellis-implement` sub-agent执行；Phase 2由独立
  `trellis-check` sub-agent执行；Branch Review由独立 review sub-agent执行。
- [ ] Docs strategy固定为 `ssot_first`；Middle-platform Knowledge Gate为“不适用”。

## 2. 有序实施步骤

### Step 1. Durable SSOT与active closure baseline

- [ ] 先更新 `design.md` 12.1 列出的 workflow/package/data/script/quality/preset/public-doc
  specs与 requirement/flow SSOT。
- [ ] 在 Skill package contract定义 `guru-review-branch` semantic owner、input、outputs、
  private artifacts、planned target与 routers。
- [ ] 定义 Interface 1.3 `planned_skill_input_seed` 的 closed schema、validation与
  future activation replacement规则。
- [ ] 把 `exit_id` omission从单一 hard-coded workflow edge收敛为通用 routing identity规则，
  省略范围限于 exact discriminator。
- [ ] 增加 source validator fixtures，证明 future complete active Interface 1.3 row使 closure
  从 9 Skills/35 exits增长到 10 Skills/39 exits，且 Stage 0/production migration sets不变。
- [ ] 更新 production migration manifest的 committed consumer/projection binding，并把
  authoring-seed edge清单从 current 3 条改为 4 条；3-Skill/11-exit集合与 activation
  identity保持不变。

Checkpoint：durable contracts与 source validator tests先通过。若 stable id、consumer
ownership或 product scope变化，停止并进入 Scope Change Gate。

### Step 2. Canonical package skeleton与 public I/O

- [ ] 新增 `trellis/skills/guru-team/packages/guru-review-branch/`。
- [ ] 编写 `SKILL.md` 与 `references/contract.md`，完整定义 semantic stages、entry
  preconditions、qualification-first、review lifecycle、confirmation、recorder/checker与
  four typed exits。
- [ ] 编写 Interface 1.3 `interface.json`，声明 workflow/standalone、13 个 preconditions、
  runtime dependency、artifacts、validators、reentry、platform destinations与
  public/private contracts。
- [ ] 新增 `branch_review` aggregate/profile schema与完整 input example。
- [ ] 新增 authoring example，只包含 `profile`、`mode`、`review_intent`。
- [ ] 新增四个 output schemas/examples与 invocation-error schema/example。
- [ ] 声明 #146 committed到本 profile的 target-owned authoring seed：
  seed固定 `task_ref`、`base_ref`、`committed_head`。
- [ ] 同步 `guru-create-task-commit/interface.json` 的 committed consumer contract与
  production migration manifest binding，producer output schema与 DTO bytes不变。
- [ ] 声明 `passed` planned #116 seed、implementation router、scope router、blocked stop与
  四个 projections。
- [ ] 负例覆盖 optional mega object、private artifact body、invalid intent、unknown field、
  unconsumed business field、planned target越权 schema与 wrong registry state。

Checkpoint：`discover-skill-contract` source mode返回 active minimal handoff，
input/output examples全部通过，private artifact字段不进入 DTO。

### Step 3. Qualification与 review artifact schema

- [ ] 定义五个 scenario classes与互斥 candidate dispositions。
- [ ] 为 qualified finding、scope proposal、observation、follow-up candidate定义 closed
  owner-result结构。
- [ ] Qualified finding必填 requirement refs、scope basis、scenario class、qualification、
  severity、owner round、reviewed HEAD与 closure evidence。
- [ ] Scope proposal禁止 severity与 implementation route。
- [ ] 演进 `review-gate.json` schema，区分 AI semantic fields与 deterministic bindings。
- [ ] 保留 `agent-assignment.json`、`reviews/*.md`、`review.md`现有 paths与生命周期语义。
- [ ] 增加 migration/reader回归，证明 current active artifacts可重验，archive artifacts
  保持只读。
- [ ] 增加 candidate未 qualification、互斥 disposition冲突、severity越权、scope proposal
  自动修复、out-of-scope阻塞 gate负例。

Checkpoint：artifact schema能表达 finding、proposal、observation、follow-up与 final pass，
且没有第二个 Branch Review pass artifact。

### Step 4. Recorder、checker与 public wrapper

- [ ] 在 shared runtime实现 review owner input materialization、recorder、checker与
  public output projection。
- [ ] Entry checker绑定 task/worktree/base/head/full range、planning、Phase 2、ledger、
  commit evidence、Docs SSOT、assignment、raw reports与 working tree。
- [ ] Recorder只在收到已完成 AI review payload后写 `review-gate.json`。
- [ ] Checker复验 schema、hash、HEAD、range、dirty allowlist、round lifecycle、
  closure-before-final、fresh final reviewer、review.md links与 artifact freshness。
- [ ] 保持现有 `review-branch`、`check-review-gate` CLI compatibility，使其委托同一
  owner recorder/checker。
- [ ] 新增 package `scripts/invoke.sh`，只接受 public input与 repo-local checker-passed
  owner result。
- [ ] Wrapper读取 actual exit后选择对应 output schema并序列化单一 DTO。
- [ ] Trace tests证明 runtime不选择 scope、scenario、severity、finding disposition、
  reviewer充分性、route或 pass。
- [ ] Regression证明 `expected_exit` 不进入 wrapper request、owner result或 route selector。

Checkpoint：四个 actual exits通过真实 wrapper；stdout每次只含一个 declared DTO。

### Step 5. Independent reviewer与 lifecycle闭环

- [ ] Package prompt明确 dispatch未修改 upstream check/review agent。
- [ ] 生成问题发现审查代理 handoff，覆盖 complete branch diff、requirements、planning、
  Docs SSOT、Phase 2、deployment/safety与 private-runtime禁读边界。
- [ ] 记录 raw report、assignment、liveness与 findings count。
- [ ] 实现 finding owner到 closure round的 same-agent、fresh-agent、replacement chain验证。
- [ ] 实现 closure agent不能成为 final reviewer、final agent id必须 fresh、final round必须
  last/current HEAD/zero findings。
- [ ] 增加 missing report、digest mismatch、round gap、stale head、unfinished replacement、
  closure仍有 finding、final reviewer复用负例。
- [ ] Upstream ownership测试断言 Step 2“明确禁止修改”路径全部无 diff。

Checkpoint：finding fix只能返回 implementation chain；全部 findings关闭后才能进入 fresh
final review。

### Step 6. Workflow薄化与 routers

- [ ] 将 `guru-create-task-commit:committed` consumer从
  `branch-review-or-finding-closure` workflow placeholder切换为 active
  `guru-review-branch` target profile。
- [ ] Phase 3.5替换为一个 mandatory invoke与四个 exact exit markers。
- [ ] 新增 `guru-branch-review-implementation-router`，消费
  `exit_id`、`task_ref`、`reviewed_head`、`finding_refs`，返回 implementation后强制经过
  check、commit、review。
- [ ] 新增 `guru-branch-review-scope-router`，消费 `exit_id`、`task_ref`、
  `proposal_refs`，要求 caller AI fresh编写 existing clarification profile input。
- [ ] 增加 `branch-review-blocked` stop target。
- [ ] 删除 workflow中已迁入 package的 review prompt、qualification、artifact与 recorder
  细节；保留 global phase transition与 fail-closed route。
- [ ] 更新 canonical workflow与 dogfood `.trellis/workflow.md`。
- [ ] Marker validator证明每个 exit只有一个 consumer，planned #116没有 invoke marker。

Checkpoint：workflow不含 step-local Branch Review checklist，unknown/multiple/unmapped/
missing planned package全部失败关闭。

### Step 7. Eval corpus、registry与 extension activation

- [ ] 新增 canonical `evals/evals.json` 与 repo-local semantic fixtures。
- [ ] 覆盖 `passed`、`implementation_required`、
  `scope_confirmation_required`、`blocked`。
- [ ] 覆盖 workflow、standalone、finding-fix review、fresh-final review。
- [ ] Shared native adapter复用 owner recorder/checker并真实执行 public wrapper；不新增
  generic fallback。
- [ ] 运行 shared eval runner，证明 actual exit决定 schema，grader只在返回后比较
  `expected_exit`。
- [ ] Registry新增 active #131 entry与 planned #116 entry；package roots只包含 active
  packages。
- [ ] Extension更新 active ids、public input/output/private schema inventories、
  managed assets与 runtime commands。
- [ ] Closure validator返回 10 active Skills、39 exits，全部 active profiles/exits有 current
  corpus binding。

Checkpoint：source active graph完整；planned #116只有 registry identity与 producer bridge，
没有 package、invoke marker或 exit marker。

### Step 8. Preset、dogfood与selected platforms同步

- [ ] 更新 preset managed assets、installer tests、throwaway assertions与 ownership
  registry。
- [ ] 运行 canonical preset apply同步 `.trellis/guru-team/`、`.agents/skills/`、
  `.codex/skills/`、`.claude/skills/`、`.cursor/skills/`。
- [ ] 逐个处理 `.new`、`.bak`，不静默覆盖用户文件。
- [ ] 比较 package Interface、schemas、examples、wrapper、evals在 canonical、installed与
  selected platform roots的 bytes及 executable mode。
- [ ] 运行 dogfood overlay drift、source/installed contract validation、recursive sidecar
  scan与 upstream ownership检查。
- [ ] 保持 issue #128 的 43-path historical `baseline_sha256` identity不变；仅为五个
  active `trellis-continue` entry登记 reviewed `current_payload_sha256`，并用
  schema/validator/negative regressions证明该字段不能扩到其它entry、不能随overlay
  bytes一起静默改写、也不提前执行 #132 removal。
- [ ] 更新 root README、workflow README、preset README中的 10/39、discovery、
  invocation、eval、install、update与 reapply命令。

Checkpoint：canonical与 dogfood无 drift，四平台 corpus一致，upstream check agent无修改。

### Step 9. Clean throwaway、update与reapply

- [ ] 在干净临时 repo验证 workflow marketplace index与 `guru-team` id/path/type。
- [ ] 验证新项目 init与已有项目 `--create-new` preview、正式 workflow switch。
- [ ] 安装 preset并运行 `guru-review-branch` contract discovery、wrapper smoke、
  10/39 closure与 selected-platform checks。
- [ ] 执行 normal commit-to-review input authoring-seed merge。
- [ ] 执行四个 exits、两种 mode、finding-fix review、fresh-final review corpus。
- [ ] 验证 `passed` 到 planned #116在 package缺失时 fail closed。
- [ ] 从 pre-#131 fixture运行 `trellis update`、preset reapply并重复 source/installed/
  closure/eval验证。
- [ ] 扫描零 unresolved `.new/.bak`、零 mixed graph、零 private runtime Agent import。

### Step 10. Docs reconciliation与 implementation handoff

- [ ] 对照 `design.md` 第12节记录实际 updated durable paths。
- [ ] 把 final Interface fields、schema ids、commands、qualification contract、closure规则、
  install/update结果合并到 durable docs。
- [ ] 记录 task-history-only内容、no-change理由与 follow-up界限。
- [ ] Implementation handoff列出所有修改路径、R/AC承接、validation、existing-state、
  deployment/safety与 distribution影响。
- [ ] 主会话复核 handoff后才进入独立 Phase 2。

### Step 11. 独立 Phase 2、commit与自举 Branch Review

- [ ] 独立 `trellis-check` sub-agent检查 requirements、design、code、API、schema、tests、
  runtime、workflow、docs、preset、install/update、CI/CD、container、K8s、migration、
  Makefile与 task artifacts。
- [ ] Main session只在完整 semantic check后 record/check `phase2-check.json`。
- [ ] `guru-create-task-commit` 创建 task work commit，精确 stage current task scope。
- [ ] 使用刚实现的 `guru-review-branch` dispatch独立问题发现审查代理。
- [ ] 若有 finding，按 implementation -> check -> commit -> closure review重入。
- [ ] 全部 findings关闭后 dispatch fresh final reviewer，覆盖
  `origin/main...HEAD`完整 diff。
- [ ] 记录并验证 `review.md`、`reviews/*.md`、`agent-assignment.json`、
  `review-gate.json`，消费 current `passed`。
- [ ] 因 #116仍 planned，`passed` 后在 missing-Skill gate停止，不执行 publish、push、
  PR mutation或 archive。

## 3. 预计修改面

### 3.1 Canonical source

- `.trellis/spec/workflow/{index,skill-package-contract,workflow-contract,data-contracts,companion-scripts,quality-guidelines}.md`
- `.trellis/spec/preset/{installer,overlay-guidelines,upstream-ownership}.md`
- `.trellis/spec/docs/public-docs.md`
- `docs/requirements/{README,requirement-main,guru-team-trellis-flow}.md`
- `trellis/skills/guru-team/packages/guru-review-branch/**`
- `trellis/skills/guru-team/packages/guru-create-task-commit/interface.json`
- `trellis/skills/guru-team/migrations/production-minimal-handoff.json`
- `trellis/skills/guru-team/schemas/skill-interface-1.3.schema.json`
- `trellis/skills/guru-team/registry.json`
- `trellis/skills/guru-team/tests/test_skill_packages.py`
- `trellis/skills/guru-team/adapters/eval/native_adapter.py` 及 tests
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及 tests
- `trellis/guru-team-extension.json`
- `trellis/presets/guru-team/**`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

### 3.2 Generated/installed copies

- `.trellis/workflow.md`
- `.trellis/guru-team/skills/**`
- `.trellis/guru-team/extension.json`
- `.agents/skills/guru-review-branch/**`
- `.codex/skills/guru-review-branch/**`
- `.claude/skills/guru-review-branch/**`
- `.cursor/skills/guru-review-branch/**`

这些路径只通过 canonical preset apply同步。

### 3.3 明确不修改

- `.trellis/agents/check.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
- `.agents/skills/trellis-check/**`
- `.codex/agents/trellis-check.toml`
- `.claude/agents/trellis-check.md`
- `.cursor/agents/trellis-check.md`

## 4. 验证命令族

实现阶段以仓库当前脚本 `--help` 与 durable docs为准，执行以下命令族：

```text
source Skill contract validation
installed Skill contract validation
guru-review-branch package contract tests
shared runtime unit tests
preset installer tests
upstream ownership tests
dogfood overlay drift check
public wrapper invocation probes
shared/Codex/Claude/Cursor eval corpus checks
clean throwaway install verification
trellis update plus preset reapply verification
recursive .new/.bak scan
git diff --check
```

每个命令记录 exit code、关键结果与未验证项。测试通过不能替代 Phase 2或 Branch Review
semantic gate。

## 5. 风险与停止条件

- Planned consumer bridge若需要定义 #116 input schema：停止并路由 scope clarification。
- #146 committed DTO若需要新增字段：停止；不得扩大 producer output。
- Qualification若无法保留 AI judgment owner：停止；不得把分类或 severity写入 script。
- Existing artifact演进若要求第二个 pass artifact：停止并修订 migration方案。
- Independent reviewer只能通过修改 upstream check agent获得 prompt：停止；改用 package
  handoff。
- Throwaway/update/reapply任一门禁未通过：不得声明开箱即用。
- 工作区出现无关 dirty paths：不得 stage、format、revert或提交这些路径。

## 6. Phase 2完成判定

仅在以下条件同时成立后创建 task work commit：

- R1-R12与 AC1-AC17均有 implementation/test/docs evidence；
- Docs SSOT Plan完成 reconciliation；
- Source、installed、dogfood、selected-platform与 clean throwaway门禁通过；
- Update/reapply无 unresolved sidecar；
- Upstream check agent diff为零；
- 独立 Phase 2报告无 current-scope finding；
- `phase2-check.json` 与 current HEAD/dirty scope匹配。

## 7. Docs SSOT checkpoint

Implementation handoff必须填写：

| Field | Required evidence |
| --- | --- |
| Strategy | `ssot_first` |
| Updated durable paths | 实际修改清单 |
| Task delta merged | Interface、qualification、artifact、workflow、runtime、distribution最终合同 |
| Task-history-only | Intake、approval、agent、raw command、review evidence |
| No-change decisions | 逐个列出未改 durable doc与理由 |
| Follow-up | #116、#132 |
| Deployment impact | CI/CD、container、K8s、migration、Makefile是否需要更新及理由 |

缺失任一项时，`guru-check-task` 返回 `implementation_required`。
