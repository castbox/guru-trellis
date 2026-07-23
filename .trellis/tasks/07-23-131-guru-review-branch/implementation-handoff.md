# Issue #131 Implementation Handoff

## 1. 结论与边界

Issue #131 的实现边界已完成，当前工作区已具备交给独立 `trellis-check`
执行 Phase 2 语义检查的代码、合同、文档、分发与验证证据。

本结论不等同于 Phase 2 通过或 Branch Review 通过。本实现代理没有：

- 运行 `trellis-check`；
- 写入或验证 `phase2-check.json`；
- 创建 task work commit；
- 运行 `guru-review-branch` 对当前分支做真实 Branch Review；
- commit、push、创建或修改 PR、发布或归档。

## 2. Requirement / Design carryover

### 2.1 R1-R12

- R1-R2：新增 active `guru-review-branch` Interface 1.3 semantic package；固定
  `branch_review` 的 6 个必填字段、2 种 mode 与 3 种 review intent；#146
  committed output仍只提供 `task_ref`、`base_ref`、`committed_head`。
- R3：runtime entry checker绑定 task/worktree/base/current branch/current HEAD、
  `origin/<base>...HEAD`、planning、Phase 2、ledger、commit、Docs SSOT、
  assignment、raw reports、review lifecycle与 working tree。
- R4-R6：package拥有 independent-review handoff、qualification-first 五类
  scenario、finding owner/closure/replacement/fresh-final lifecycle；未修改 upstream
  check/review agent。
- R7-R8：实现四个独立 closed output schema/example；`passed` 只携带
  `task_ref`、`reviewed_head`、`review_ref` 到 planned #116 seed bridge；
  implementation、scope confirmation与 blocked各有唯一 consumer/stop。
- R9-R10：复用 `reviews/*.md`、`review.md`、`review-gate.json`、
  `agent-assignment.json`；AI拥有 semantic judgment，recorder/validator只处理确定性
  evidence；真实 wrapper与 7-case eval corpus已落地。
- R11：canonical workflow薄化为一次 mandatory invocation、四个 exits、两个
  routing targets、一个 planned consumer与一个 stop；production migration保持
  3 Skills / 11 exits，authoring-seed edges从 3 更新为 4；canonical、installed、
  dogfood与 selected-platform copies已同步。
- R12：实现只覆盖 honest-but-fallible 正常路径和普通 stale/mismatch/recovery；
  未扩展到恶意篡改、额外并发/原子性加固、#116发布、push/PR/archive或独立
  qualification wrapper。

### 2.2 AC1-AC17

- AC1-AC16已有实现、合同、测试或安装/update证据，待独立 Phase 2逐项语义复核。
- AC17尚未完成：它明确要求独立 Phase 2 与 Branch Review。实现代理没有代替这两个
  gate，也没有把本 handoff当作 pass evidence。

## 3. Files changed

### 3.1 Durable SSOT / public docs

- `.trellis/spec/workflow/{index,skill-package-contract,workflow-contract,data-contracts,companion-scripts,quality-guidelines}.md`
- `.trellis/spec/preset/{installer,overlay-guidelines,upstream-ownership}.md`
- `.trellis/spec/docs/public-docs.md`
- `docs/requirements/{README,requirement-main,guru-team-trellis-flow}.md`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

### 3.2 Canonical implementation

- `trellis/skills/guru-team/packages/guru-review-branch/**`
- `trellis/skills/guru-team/consumers/workflow/production/review-branch-*.schema.json`
- `trellis/skills/guru-team/packages/guru-create-task-commit/interface.json`
- `trellis/skills/guru-team/{registry.json,migrations/production-minimal-handoff.json}`
- `trellis/skills/guru-team/schemas/{skill-interface-1.3,production-migration-manifest}.schema.json`
- `trellis/skills/guru-team/{adapters/eval/native_adapter.py,tests/**}`
- `trellis/workflows/guru-team/{workflow.md,scripts/python/guru_team_trellis.py,scripts/python/test_guru_team_trellis.py}`
- `trellis/guru-team-extension.json`
- `trellis/presets/guru-team/ownership/upstream-ownership.json`
- `trellis/presets/guru-team/scripts/{bash/verify-throwaway-install.sh,python/**}`
- `trellis/presets/guru-team/overlays/**/trellis-continue*`

### 3.3 Generated / installed copies

- `.trellis/workflow.md`
- `.trellis/guru-team/**` 中对应 registry、schemas、migration、runtime、adapter、
  extension、consumer与 Skill package副本
- `.agents/skills/guru-review-branch/**`
- `.codex/skills/guru-review-branch/**`
- `.claude/skills/guru-review-branch/**`
- `.cursor/skills/guru-review-branch/**`
- `.agents`、`.codex`、`.claude`、`.cursor` 的 `trellis-continue` 薄入口副本

### 3.4 明确保持不变

以下 upstream check/review surfaces的 diff均为零：

- `.trellis/agents/check.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
- `.agents/skills/trellis-check/**`
- `.codex/agents/trellis-check.toml`
- `.claude/agents/trellis-check.md`
- `.cursor/agents/trellis-check.md`

## 4. Docs SSOT reconciliation

| Field | Result |
| --- | --- |
| Strategy | `ssot_first` |
| Durable-doc inputs | 先以更新后的 workflow/package/data/script/quality/preset/public-doc/requirement SSOT作为 package、runtime、workflow、distribution实现输入 |
| Task-delta inputs | Approved `prd.md`、`design.md`、`implement.md` 提供 Interface、qualification、artifact、router、lifecycle、eval与 upgrade delta |
| Updated durable paths | 第 3.1 节列出的全部 durable paths均已更新 |
| Task delta merged | Interface 1.3 planned seed、routing discriminator omission、13 entry preconditions、五类 qualification、四 exits、artifact lifecycle、runtime commands、10/39/23 closure、4 authoring edges、distribution与 upgrade合同均已合并 |
| Task-history-only | Intake/approval/context artifacts、agent assignment/liveness、原始命令输出、临时 throwaway路径、首次 apply 的 backup清理过程、本 handoff与后续 Phase 2/Branch Review evidence |
| No-change decisions | `design.md` 12.1列出的 durable authority均有 semantic delta，没有需要声明 no-change 的列出项；upstream check agent/Skill因 R4/R12明确禁止而保持不变 |
| Follow-up | #116继续为 planned publication Skill；#132继续保持 follow-up/open；本任务未实现两者 |
| Current PR limitation | 分支未获授权 push，因此当前 #131 exact feature-ref未通过远端 marketplace安装；throwaway以本地 unpublished canonical workflow sample验证当前改动，公开 marketplace discovery验证的是 public main |

Docs delta已合并到 durable docs；task artifacts只保留运行历史与 gate evidence，没有把
active task/private runtime内容发布到公共 Skill package。

## 5. Distribution / upgrade result

- Extension version更新为 `0.6.5-guru.21`，registry、extension inventory、
  ownership inventory及其固定 digest已同步。
- Preset apply已同步 all selected platforms；最终重复 apply与
  `check-dogfood-overlay-drift.sh`通过。
- 首次 apply生成的 11 个精确 `.bak` sidecars已逐一检查并清理；最终
  `.new/.bak`、conflict、removal均为 0。
- Full throwaway verifier覆盖 public marketplace discovery、fresh init、
  existing-project preview/switch、本地 unpublished current workflow sample、
  preset install、public wrapper/eval、selected platforms、`trellis update --force`、
  workflow/preset reapply、no-developer fixture与 pre-#146 upgrade fixture。
- 当前本机 Trellis CLI基线为 0.6.5；观察到 npm latest为 0.6.8，但本任务没有扩大
  已批准 baseline或宣称 0.6.8兼容性。

## 6. Tests and checks run

- `guru-review-branch` package contract：8/8 passed。
- Shared real-wrapper eval corpus：7/7 passed。
- Skill package full suite：166 tests，OK。
- Preset installer suite：45 tests，OK。
- Upstream ownership suite：6 tests，OK。
- Shared runtime full suite：557 tests，OK，13 skipped。
- Full throwaway install/update/reapply verifier：exit 0。
- Source package validator：passed，10 active Skills / 39 exits / 23 targets，
  planned `guru-review-task-publication`。
- Installed package validator：passed，同为 10 / 39 / 23；1903 managed files，
  sidecar/conflict/removal均为 0。
- `task.py validate`：passed。
- JSON parse：867 files passed。
- `bash -n`：throwaway verifier与 canonical/installed package wrappers passed。
- `py_compile`：updated Python passed。
- `git diff --check`：passed；index为空，没有 staged changes。
- Canonical/dogfood workflow、runtime及 canonical/shared/Codex/Claude/Cursor
  package tree一致性：passed。
- Recursive sidecar、`__pycache__`、public absolute path/credential pattern scan：
  clean。

## 7. Deployment and safety impact

- 修改影响 Guru Team workflow、Skill package、preset installer、platform overlays、
  installed extension与 upgrade/reapply行为。
- 没有 CI/CD、container、Kubernetes、database migration、Makefile或业务 service
  configuration变更，因此这些 surface不需要同步修改。
- 公共 package未包含 active task、workspace journal、本机绝对路径、secret、
  credential、signed URL或 private raw data。

## 8. Handoff to `trellis-check`

### 8.1 Required focus

1. 按 R1-R12、AC1-AC17审查 requirements/design/code/schema/tests/docs/distribution。
2. 验证 qualification-first语义所有权仍由 AI承担，runtime没有选择 scope、
   scenario、severity、finding disposition、route或 final pass。
3. 验证四个 output DTO与 consumers/projections；尤其是 planned #116 bridge只含三个
   seed fields且 package缺失时 fail closed。
4. 验证 finding closure、replacement、fresh final reviewer与 full-range/current-HEAD
   lifecycle。
5. 验证 active closure 10/39/23、production 3-Skill/11-exit与 4 authoring edges。
6. 验证 canonical workflow和各平台 `trellis-continue` 仅保留 invocation/route，
   没有重新复制 Branch Review内部合同。
7. 验证 clean install、update/reapply、pre-#146 migration fixture、sidecar cleanup与
   Docs SSOT reconciliation。
8. 复核第 3.4 节禁止修改的 upstream check/review paths仍为零 diff。
9. 复核 deployment/safety无遗漏，并明确当前远端 feature-ref未验证限制。

### 8.2 Gate blocker before Phase 2

最终重新运行 planning approval checker时得到：

```text
planning_approval_requirement_authority_stale
```

原因是批准的 `ssot_first` 实施按计划更新了 `docs/requirements/**` durable requirement
authority。`prd.md`、`design.md`、`implement.md` 本身没有被实现代理修改，初始
planning approval在实现开始前通过；但当前 gate按 requirement authority freshness
失败关闭。

实现代理没有重新记录或伪造批准。主会话必须先重新执行所需的 semantic planning
review/用户确认并恢复 current approval，之后才能 dispatch `trellis-check` 或记录
Phase 2。

## 9. Remaining risks / follow-ups

1. 先解决 `planning_approval_requirement_authority_stale`；这是当前唯一已知的
   Phase 2 entry blocker。
2. 独立 `trellis-check`、`phase2-check.json`、task work commit和真实
   `guru-review-branch` 尚未执行。
3. 未获 push授权，current #131 exact remote feature-ref marketplace install未验证。
4. #116 planned package与 #132 follow-up保持 open；不得在本任务中静默扩展。
5. Trellis CLI 0.6.8不在已批准/current tested baseline内。

## 10. Phase 2 finding-fix round（2026-07-23）

本节取代第 8.2 节关于“尚未执行 Phase 2 / planning stale”的旧状态描述，但保留旧文
作为实现历史。主会话已重新完成 planning review并取得用户确认，随后独立 Phase 2
返回 `implementation_required`，包含 `F-131-01`、`F-131-02`、`F-131-03`。本轮只修复
这三个 finding，没有运行 `trellis-check`、没有改写 `phase2-check.json`、没有创建
commit/push/PR。

### 10.1 Findings closure implementation

- `F-131-01`：public `guru-review-branch` invocation现在在读取 exact owner artifact后，
  重新验证 current workspace/task/base/HEAD、planning approval、Phase 2、ledger、
  Docs SSOT、working tree和 task-commit evidence。只有这一组显式 entry
  preconditions正常过期时才投影最小 `{"exit_id":"blocked"}`；任意未知 checker、
  locator或 schema错误仍按 invocation error失败关闭，不被降级成 `blocked`。
- `F-131-02`：Branch Review recorder和checker现在要求 exactly one
  `task-commit-plans/<seq>.json` 的 committed result绑定 current HEAD，并复验 plan
  digest、task/branch/base/parent/message/path/tree identity、planning/Phase 2/ledger/task
  evidence以及 candidate artifact自身已进入 commit。真实 `blocked-stale` eval改为先记录
  current passing gate，再通过普通 `prd.md`修订制造 planning stale，public wrapper实际
  返回 `blocked`。
- `F-131-03`：qualified finding的 `owner_round`必须绑定 assignment中真实产出 finding
  的 round、reviewed HEAD与raw report；`evidence_refs`支持精确 repo-relative或
  task-relative引用。Resolved finding的 `closure_evidence`必须绑定后续真实 closure
  round、current task-local report digest，以及 same-agent `reuse-for-closure`或显式
  replacement relation。该校验同时接入 recorder和 persisted gate checker。
- `no_docs_update_needed`的通用入口兼容性同时得到保留：非文档任务可以用具体
  `no_update_reason`满足 Docs SSOT outcome；其余三种 strategy仍要求
  `task_delta_merged=true`。

### 10.2 Finding-fix files

- Canonical runtime和tests：
  `trellis/workflows/guru-team/scripts/python/{guru_team_trellis.py,test_guru_team_trellis.py}`。
- Canonical eval adapter/corpus：
  `trellis/skills/guru-team/adapters/eval/native_adapter.py` 与
  `trellis/skills/guru-team/packages/guru-review-branch/evals/files/blocked-stale-facts.json`。
- Preset apply同步的 installed runtime、adapter、package以及
  `.agents` / `.codex` / `.claude` / `.cursor` package mirrors；installed extension
  inventory同步为current tree。
- 本节 implementation handoff。

禁止修改的 upstream check/review paths仍全部为零 diff。

### 10.3 Docs SSOT Plan reconciliation

| Field | Finding-fix result |
| --- | --- |
| Strategy | 延续批准的 `ssot_first` |
| Durable-doc implementation input | 第 4 节列出的 workflow/package/data/script/quality/preset/requirement SSOT仍是primary input |
| Task-delta input | Current PRD/design/implement与Phase 2三个 findings限定本轮修复边界 |
| Durable docs sync | 无新增 wording delta；durable SSOT原本已要求13项entry freshness、真实task commit handoff与finding lifecycle绑定，本轮是runtime/tests追平现有合同 |
| Task delta merged | 第 4 节已合并；本轮没有产生需要再次合并的新合同 |
| Task-history-only | Phase 2报告、负例复现过程、临时eval/throwaway路径、首次apply生成并清理的7个精确`.bak`、本finding-fix handoff |
| Current PR limitation | 仍未push；public marketplace只采样`main`，current unpublished workflow通过本地canonical sample验证 |

只更新了可执行 eval事实描述，没有为了修复代码缺陷重写 durable requirement或扩大
approved scope。

### 10.4 Finding-fix validation

- 新增负例先失败：普通 planning修订后旧 public wrapper仍返回 `passed`；缺失current
  task-commit handoff与错误 `owner_round` / `closure_evidence`均未被阻断。
- 新增focused tests通过；`ReviewGateReportTest` +
  `TaskCommitCandidateExecutorTest`共113 tests通过。
- Runtime full suite：560 tests，OK，13 skipped（原557 + 本轮3个回归）。
- `guru-review-branch` package：8 tests；Skill full suite：166 tests；
  installer：45 tests；ownership：6 tests，全部OK。
- Source与installed真实 shared eval各7/7 passed；`blocked-stale`实际
  `exit_id=blocked`，finding-fix与fresh-final均实际`passed`。
- Full throwaway install/update/reapply：默认public-main采样门禁先按预期失败关闭；
  显式允许public marketplace sample后exit 0，同时验证本地unpublished current
  workflow sample、fresh install、selected platforms、wrapper/eval、update/reapply、
  no-developer与pre-#146 fixtures。
- Source与installed package validator均passed：10 active Skills / 39 exits /
  23 targets；installed 1903 managed files，sidecar/conflict/removal均为0。
- `task.py validate`、2627个JSON parse、19个changed/new shell syntax、
  updated Python `py_compile`、`git diff --check`、empty index、dogfood drift、
  canonical/installed/all-platform package tree、recursive sidecar/cache、
  public package敏感路径/credential pattern scan全部通过。
- Final workspace boundary expected/actual均为本task worktree；planning checker
  `status=ok`、`typed_exit=approved`。

### 10.5 Handoff for the next independent `trellis-check`

下一轮检查应重新完整执行 Phase 2，不能只复用本节命令结果。除第 8.1 节原有focus外，
重点复核：

1. 正常 planning / Phase 2 / commit evidence stale时public wrapper只返回最小
   `blocked` DTO，而invalid invocation仍是错误。
2. current commit artifact的plan/result/object/evidence复验是否完整且未引入semantic
   route判断。
3. finding raw report的repo-relative/task-relative规范化仍是精确绑定，不退化为basename
   或任意文件匹配。
4. owner、closure、replacement与fresh-final assignment链在recorder和checker两处
   都失败关闭。
5. throwaway/update/reapply、10/39/23 closure和禁止修改路径继续保持当前结果。

有意留给后续gate的工作仅包括：独立Phase 2复审、Phase 2 artifact新结论、task work
commit与真实Branch Review。实现代理未执行这些职责。

### 10.6 Remaining risks / follow-ups after finding-fix

1. Current `phase2-check.json`仍诚实记录上一轮
   `typed_exit=implementation_required`；必须由新的独立检查轮次复核后才能更新。
2. Current branch未commit/push，feature-ref marketplace安装仍未验证。
3. #116、#132和Trellis CLI 0.6.8边界不变。

## 11. Phase 2 finding-fix round 2（2026-07-24）

本节取代第 10.3、10.4、10.5、10.6 节中与当前状态冲突的描述，但保留旧文作为实现
历史。独立 Phase 2 在上一轮修复后仍返回 `implementation_required`，新增
`F-131-04`（P1）与 `F-131-05`（P2）。本轮只修复这两个 finding，没有运行
`trellis-check`、没有修改或记录 `phase2-check.json`、没有创建 commit/push/PR。

### 11.1 Findings closure implementation

- `F-131-04`：public `guru-review-branch` owner invocation现在先把 owner gate的
  schema、facts digest与 task/mode/intent/base/HEAD identity错误保留为 invocation
  error；随后把 assignment、raw review report、final rollup和finding lifecycle作为
  entry precondition重新验证。只有这些客观的 missing/stale/digest/lifecycle错误才
  投影为最小 `{"exit_id":"blocked"}`，invalid locator/schema与未知 checker异常仍失败
  关闭为 invocation error，不存在 catch-all降级。
- `F-131-04`回归先构造真实通过的 finding-fix lifecycle，再以普通流程修改已登记的
  `round-002-closure.md`。修复前 public wrapper return code为2且没有stdout，
  stderr为 `owner_result_not_checked`；修复后 return code为0，语义DTO严格只有
  `exit_id=blocked`。finding-fix与fresh-final正向 corpus仍实际返回 `passed`。
- `F-131-05`：当前 durable authoring-seed合同统一为exactly four edges，新增/保留
  `guru-create-task-commit:committed -> guru-review-branch`；production migration
  membership继续独立保持exactly three Skills / eleven exits，没有把 authoring graph
  数量机械替换进 migration membership。
- 新增 durable-doc/graph回归，同时验证11个current-contract文档片段、4条
  authoring-seed edges、3个production migration Skills与11个migration exits。

### 11.2 Finding-fix files and distribution sync

- Canonical runtime：
  `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- Canonical eval adapter/corpus：
  `trellis/skills/guru-team/adapters/eval/native_adapter.py`、
  `trellis/skills/guru-team/packages/guru-review-branch/evals/files/blocked-stale-facts.json`
  与 `blocked-stale-input.json`。
- Graph/docs regression：
  `trellis/skills/guru-team/tests/test_skill_packages.py`。
- Durable docs：`README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`、`docs/requirements/README.md`、
  `docs/requirements/guru-team-trellis-flow.md`、
  `docs/requirements/requirement-main.md`、
  `.trellis/spec/workflow/skill-package-contract.md`、
  `.trellis/spec/workflow/companion-scripts.md`、
  `.trellis/spec/workflow/quality-guidelines.md`、
  `.trellis/spec/preset/installer.md` 与
  `.trellis/spec/preset/upstream-ownership.md`。
- Preset apply已同步 installed runtime、adapter、package与
  `.agents` / `.codex` / `.claude` / `.cursor` mirrors；canonical、installed和四个平台
  package tree最终一致。首次 apply产生的12个精确 `.bak`已逐项检查并删除，重复 apply
  为no-op，最终 sidecar/conflict/removal均为0。
- 第 3.4 节禁止修改的 upstream check/review paths仍全部为零 diff。

### 11.3 Docs SSOT Plan reconciliation

| Field | Finding-fix round 2 result |
| --- | --- |
| Strategy | 延续批准的 `ssot_first` |
| Durable-doc implementation input | Current workflow/package/data/script/quality/preset/public requirement SSOT继续作为实现主输入；本轮按Phase 2指出的current-contract不一致修正文档与graph test |
| Task-delta input | Current PRD/design/implement与`F-131-04`、`F-131-05`限定实现边界；没有扩大#116/#132或CLI baseline |
| Durable docs sync | 上述11个current-contract路径已统一为4条authoring-seed edges；production migration仍为3 Skills / 11 exits |
| Task delta merged | F05的durable graph合同已合并到当前SSOT并由回归固定；F04是runtime/eval追平既有entry freshness与blocked/invocation-error合同 |
| Task-history-only | 旧Phase 2报告、red/green临时eval路径、throwaway临时路径、12个preset backup的检查/清理过程和本handoff |
| Current PR limitation | 分支仍未push；公开marketplace discovery基于public main，current unpublished workflow由本地canonical sample验证 |

本轮有实际 durable wording delta，因此第 10.3 节“无新增 wording delta”的旧结论不再
适用。`.trellis/spec/preset/installer.md` 中“from three to four”的历史迁移叙述按原意
保留；它不是current edge-count断言。active task、raw gate evidence和本机路径没有进入
公共 Skill package。

### 11.4 Finding-fix validation

- `ReviewGateReportTest` + `Stage0MigrationManifestTests`：73 tests，OK。
- Runtime full suite：560 tests，OK，13 skipped。
- Skill full suite：167 tests，OK；`guru-review-branch` package：8 tests，OK。
- Preset installer：45 tests，OK；upstream ownership：6 tests，OK。
- Source与installed shared real-wrapper eval：各7/7 passed；`blocked-stale`实际只返回
  `exit_id=blocked`，finding-fix与fresh-final实际返回 `passed`。
- Source与installed package validator：10 active Skills / 39 exits / 23 targets，
  passed；installed inventory为1903 managed files，sidecar/conflict/removal均为0。
- Full throwaway install/update/reapply verifier：exit 0，覆盖public marketplace
  discovery、本地unpublished current workflow sample、fresh init、existing-project
  preview/switch、all-platform preset、wrapper/eval、`trellis update --force`、
  workflow/preset reapply、no-developer与pre-#146 fixtures。
- JSON parse：2630 files；`bash -n`：295 shell files；updated Python
  `py_compile`、`task.py validate`、`git diff --check`、empty index、
  dogfood overlay drift、canonical/installed/all-platform parity、
  recursive sidecar/cache与public path/secret/sensitive-filename scan全部通过。

### 11.5 Handoff for the next independent `trellis-check`

下一轮必须重新执行完整Phase 2；当前
`.trellis/tasks/07-23-131-guru-review-branch/phase2-check.json`仍诚实保留上一轮
`typed_exit=implementation_required`，实现代理没有触碰它。除第 8.1 与10.5节原有
focus外，重点复核：

1. 通过finding-fix fixture后普通修改registered assignment或raw review report时，
   public wrapper return code为0且输出DTO只有 `{"exit_id":"blocked"}`。
2. owner gate的invalid locator/schema、identity/facts错误与未知 checker异常仍是
   invocation error；只有明确的objective missing/stale/digest/lifecycle entry错误映射
   为 `blocked`。
3. 11个current durable docs、manifest和graph regression对“4 authoring edges”保持
   一致，且不破坏独立的“3 production migration Skills / 11 exits”合同。
4. Full throwaway/update/reapply、10/39/23 closure、1903-file inventory和禁止修改路径
   继续保持当前结果。

有意留给后续gate的工作仅包括：恢复current planning approval、独立Phase 2复审、
Phase 2 artifact新结论、task work commit与真实Branch Review。

### 11.6 Remaining risks / follow-ups after finding-fix round 2

1. `ssot_first`按计划更新durable requirement/docs authority后，最终planning checker
   已以exit 2和 `planning_approval_requirement_authority_stale`失败关闭。实现代理不会
   自行重批；必须由主会话重新展示/审查规划并取得fresh用户确认后才能dispatch下一轮
   `trellis-check`。
2. Current branch未commit/push，feature-ref marketplace安装仍未验证。
3. #116、#132和Trellis CLI 0.6.8边界不变。
