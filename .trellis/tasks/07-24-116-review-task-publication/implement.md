# #116 实施计划：guru-review-task-publication 闭环 Skill

## 1. 实施前门禁

- [ ] `guru-review-contract-wording:planning_artifacts` 对 current `prd.md`、
  `design.md`、`implement.md` 返回 checker-passed `pass`。
- [ ] `guru-approve-task-plan` 完成九个 entry preconditions、adequacy、provenance、
  unusual-scenario 与 AI Review Gate。
- [ ] 用户查看三份 current planning links 并给出独立
  `post-planning-approval`。
- [ ] 主会话记录 schema 2.0 `planning-approval.json`，checker验证
  `typed_exit=approved` 后运行 `task.py start`。
- [ ] Worktree 固定为
  `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`，
  branch固定为 `codex/116-review-task-publication`，base固定为 `main`。
- [ ] `trellis-before-dev` 加载 current `implement.jsonl` specs。
- [ ] Implementation、Phase 2 与 Branch Review 按 `trellis-continue` 分别使用独立
  implement/check/review agent；main session拥有Gate与最终决定。
- [ ] Docs strategy固定为 `ssot_first`；Middle-platform Knowledge Gate不适用。

## 2. 有序实施步骤

### Step 1. Durable SSOT 与 contract baseline

- [ ] 先更新 `design.md` 第17节列出的 workflow/package/data/script/quality/preset/
  public-doc authorities。
- [ ] 在 Skill package contract定义 publication semantic owner、双入口、三 exits、
  private evidence、metadata revision loop与唯一gate。
- [ ] 在 data contracts定义 `pr-readiness.json` semantic/deterministic/
  finalization-owned三层及legacy migration。
- [ ] 在 companion scripts定义 recorder/checker/wrapper边界，明确禁止deterministic
  `ready=true`冒充AI review。
- [ ] 更新 workflow/quality docs中的十维review、freshness、return/re-entry与fail-closed。
- [ ] 更新 preset/upstream ownership docs，保留finish family边界。

Checkpoint：durable contracts先通过文档/contract scanner；若stable public identity或
Issue authority需要变化，停止并进入Scope Change Gate。

### Step 2. Canonical package与public I/O

- [ ] 新增
  `trellis/skills/guru-team/packages/guru-review-task-publication/`。
- [ ] 编写 `SKILL.md` 与 `references/contract.md`，声明
  `judgment_mode=semantic`和完整closed loop。
- [ ] 编写Interface 1.3 `interface.json`，包含两个input profiles、十二个entry
  preconditions、artifacts、validators、re-entry、platform destinations与consumers。
- [ ] 新增aggregate schema、两个profile schemas、两个complete input examples与两个
  authoring examples。
- [ ] 新增`ready`、`return_to_task_work`、`blocked`独立output schemas/examples及
  invocation-error schema/example。
- [ ] `publication_ref`保持opaque，private evidence/body/index/hash bundle不进入DTO。
- [ ] 负例覆盖mega object、unknown/optional字段、wrong enum、private字段泄漏、
  seed/authoring overlap/incomplete/overwrite。

Checkpoint：source contract discovery能解析两个profiles、三个exits及唯一consumer。

### Step 3. Producer/consumer bridges与registry

- [ ] 把`guru-review-branch:passed`的`planned_skill_input_seed`替换为指向
  `publication_review`的target-owned`skill_input_authoring_seed`。
- [ ] Seed固定`task_ref/reviewed_head/review_ref`，authoring固定
  `profile/mode/review_intent`。
- [ ] 证明#131 output schema/example/bytes不变。
- [ ] Registry将#116 planned row激活为Interface 1.3 active。
- [ ] Registry新增planned `guru-finalize-task` stable identity。
- [ ] Ready seed固定`task_ref/reviewed_head/publication_ref`；不定义#118 target schema。
- [ ] 为stale profile发布target-owned schema/example/fixture，但不激活future producer。
- [ ] Source closure更新为11 active Skills/42 exits。
- [ ] `production-minimal-handoff-v1`保持3 Skills/11 exits及原activation identity。

Checkpoint：active graph、planned identity、producer partitions与consumer projections全部
通过source validator。

### Step 4. Private gate schema与facts materialization

- [ ] 定义或演进`pr-readiness.json` private schema，包含semantic dimensions、
  findings/closure、scope/docs/safety/deployment、revision history、AI conclusion、
  deterministic bindings与optional publish inputs。
- [ ] 定义十维closed ids、finding route classes、reason codes、exit/consumer union。
- [ ] Facts materializer读取task/workspace/base/head/planning/Phase2/ledger/Docs/
  Branch Review/body/index/current diff/working tree。
- [ ] Re-entry读取current readiness identity并要求replacement/current binding。
- [ ] Allowlist只接受contract明确的publication metadata paths。
- [ ] Legacy snapshot reader能识别旧shape，但new checker拒绝把它当semantic pass。
- [ ] 负例覆盖missing/failed/stale/wrong task/head/hash/scope/workspace/non-allowlisted tail。

Checkpoint：private schema能表达pass、return、blocked与revision history，且只有一个gate。

### Step 5. Recorder、checker与compatibility migration

- [ ] 实现`record-task-publication-review`，只消费AI已审查payload并重建objective facts。
- [ ] 实现`check-task-publication-review`，复验schema、hash、HEAD、review ref、
  ledger/body/index/docs/tail、exit/consumer与facts digest。
- [ ] Trace测试证明recorder/checker不决定dimension pass、finding、route、issue closure、
  PR body充分性、安全/部署或ready。
- [ ] 演进`build_pr_readiness_snapshot()`：只有checker-passed ready gate才能追加或校验
  deterministic `publish_inputs`。
- [ ] Compatibility helper保留semantic sections、typed conclusion与publication ref；
  不覆盖gate、不写第二artifact。
- [ ] 增加legacy/active/replacement reader regression。

Checkpoint：无AI owner result无法生成ready；existing finalization reader仍可读取合法
publish inputs。

### Step 6. Public wrapper与metadata revision runtime

- [ ] 新增dispatcher-only `scripts/invoke.sh`。
- [ ] Wrapper验证public input并定位repo-local checker-passed owner result。
- [ ] 根据actual `exit_id`选择output schema并做minimal projection。
- [ ] `expected_exit`只在wrapper完成后由grader断言。
- [ ] 实现metadata-only reread/rescan支持，但AI仍负责修订与fresh十维review。
- [ ] Metadata-only pass输出ready；non-metadata drift输出return；外部blocker输出blocked。
- [ ] stdout每次只含一个declared DTO；unknown/multiple/unmapped result失败关闭。

Checkpoint：三个actual exits均通过真实wrapper，route trace中没有grader输入或脚本判断。

### Step 7. Canonical workflow薄化

- [ ] 在Branch Review passed后增加一个mandatory
  `guru-review-task-publication` invocation。
- [ ] 增加ready到planned finalization、return到task-work loop、blocked到stop的唯一route。
- [ ] Return router强制重新经过implementation、Phase2、commit、Branch Review。
- [ ] Stale re-entry必须使用`publication_review_stale`并执行完整Skill。
- [ ] 删除/改写workflow中无条件构建`ready=true`或复制step-local checklist的旧表述。
- [ ] 更新canonical workflow与dogfood `.trellis/workflow.md`。
- [ ] Marker tests覆盖missing/unknown/multiple/unmapped/no-consumer fail closed。

Checkpoint：workflow只含global invocation/transition，不拥有十维review、finding loop或
artifact字段。

### Step 8. Eval corpus与平台适配

- [ ] 新增canonical `evals/evals.json`与repo-local semantic fixtures。
- [ ] 覆盖workflow/standalone initial ready、return、blocked、stale re-entry、
  metadata fix fresh ready、metadata fix发现durable drift return。
- [ ] 每个semantic case真实执行public wrapper。
- [ ] Shared native adapter复用owner recorder/checker，不新增generic fallback。
- [ ] 同步Codex/Claude/Cursor corpus，并做byte-identical断言。
- [ ] 覆盖Codex trusted Git root、Claude input protocol、Cursor unavailable/
  unsupported与shared parsing。
- [ ] 断言eval corpus/private runtime source不会进入Agent request。
- [ ] 确认每个active profile/exit有current eval binding。

Checkpoint：actual exit决定schema；grader无法影响Agent、owner result或route。

### Step 9. Extension、preset与dogfood同步

- [ ] 更新`trellis/guru-team-extension.json` commands、managed assets、active ids、
  public input/output/private schema inventory。
- [ ] 更新preset installer、ownership registry、throwaway assertions与tests。
- [ ] 运行
  `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
  同步installed shared与四平台copies。
- [ ] 比较Interface、schemas、examples、contract、wrapper、evals bytes与executable mode。
- [ ] 逐项处理`.new`/`.bak`，不覆盖无关用户改动。
- [ ] 运行source/installed validators、recursive sidecar scan、
  upstream ownership与dogfood overlay drift。
- [ ] 确认finish-work upstream assets无diff。

Checkpoint：canonical与所有安装副本无drift，extension inventory完整。

### Step 10. README与Docs reconciliation

- [ ] 更新root、workflow、preset README的11/42、discover、invoke、install、update/
  reapply命令。
- [ ] 更新requirements SSOT中的publication/finalization boundary与flow。
- [ ] 对照`design.md`第17节记录实际updated durable paths。
- [ ] 把最终fields/schema ids/commands/closure/compatibility合并到durable docs。
- [ ] 记录task-history-only与no-change decisions。
- [ ] 明确remote marketplace verifier未在本task执行，保留给finish/publish。

Checkpoint：Docs delta完成合并，durable docs与code/schema/runtime一致。

### Step 11. Clean throwaway、update与reapply

- [ ] 在干净临时repo验证`trellis/index.json`的guru-team id/path/type。
- [ ] 验证新项目init与已有项目`--create-new` preview/正式switch。
- [ ] 安装preset并运行contract discovery、11/42 closure、wrapper smoke与platform checks。
- [ ] 执行#131 passed到#116 input的authoring-seed merge。
- [ ] 执行两个profiles、两个modes、三个exits与metadata/stale corpus。
- [ ] 验证ready到planned#118在package缺失时fail closed。
- [ ] 从pre-#116 fixture运行`trellis update`、preset reapply并重复验证。
- [ ] 扫描零unresolved `.new/.bak`、零mixed graph、零private runtime Agent import。
- [ ] README命令必须在throwaway中真实可执行。

Checkpoint：开箱即用与upgrade/update抗漂移门禁有命令证据。

### Step 12. Implementation handoff与独立Phase 2

- [ ] Implementation agent输出完整handoff：修改路径、R/AC映射、validation、
  existing-state、distribution、compatibility、安全与部署影响。
- [ ] Main session复核handoff及Docs checkpoint。
- [ ] 独立check agent检查requirements/design/code/API/schema/runtime/workflow/eval/
  docs/preset/install/update/CI/CD/container/K8s/migration/Makefile与task artifacts。
- [ ] Current-scope finding返回implementation agent修复并重跑受影响验证。
- [ ] Main session只在完整semantic check后record/check `phase2-check.json`。

Checkpoint：Phase 2证据fresh、scope-complete、finding为零。

### Step 13. Task commit与Branch Review

- [ ] `guru-create-task-commit`精确stage当前task范围并创建reviewed task work commit。
- [ ] 独立review agent覆盖`origin/main...HEAD`完整diff。
- [ ] Findings按implementation -> check -> commit -> closure review闭环。
- [ ] 全部finding关闭后由fresh final reviewer完成最终pass。
- [ ] 记录/校验`review.md`、raw reports、`agent-assignment.json`、
  `review-gate.json`。
- [ ] 消费current `guru-review-branch:passed` seed进入本任务实现的publication review。
- [ ] 因#118仍planned，publication `ready`后在missing consumer gate停止；不push、不创建
  PR、不archive、不finalize。

## 3. 预计修改面

### 3.1 Canonical

- `trellis/skills/guru-team/packages/guru-review-task-publication/**`
- `trellis/skills/guru-team/packages/guru-review-branch/interface.json`
- `trellis/skills/guru-team/registry.json`
- `trellis/workflows/guru-team/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/guru-team-extension.json`
- `trellis/presets/guru-team/**`

### 3.2 Tests/evals

- `trellis/skills/guru-team/tests/**`
- `trellis/workflows/guru-team/tests/**`
- `trellis/presets/guru-team/tests/**`
- package-local `tests/**`、`evals/**`与fixtures。

### 3.3 Durable docs

- `design.md`第17.2节列出的`.trellis/spec/**`与`docs/requirements/**`。
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`

### 3.4 Generated dogfood/platform copies

- `.trellis/guru-team/**`
- `.trellis/workflow.md`
- `.agents/skills/guru-review-task-publication/**`
- `.codex/skills/guru-review-task-publication/**`
- `.claude/skills/guru-review-task-publication/**`
- `.cursor/skills/guru-review-task-publication/**`

这些路径必须由preset apply生成，不手工分叉。

## 4. 验证命令计划

实际命令名以current scripts/tests为准；实施时先用`rg`定位现有入口，不凭记忆发明。

```bash
python3 -m unittest discover -s trellis/skills/guru-team/tests
python3 -m unittest discover -s trellis/workflows/guru-team/tests
python3 -m unittest discover -s trellis/presets/guru-team/tests
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-review-task-publication/tests
```

```bash
python3 trellis/workflows/guru-team/scripts/python/guru_team_trellis.py validate-skill-contracts
python3 trellis/workflows/guru-team/scripts/python/guru_team_trellis.py validate-installed-skill-contracts
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

还必须执行：

- registry/closure与production manifest validator；
- real-wrapper eval runner与platform parity；
- upstream ownership、managed assets、executable mode、sidecar scan；
- clean throwaway init/preview/switch/install/update/reapply；
- workspace boundary与source checkout cleanliness；
- task-local contract wording、planning/Phase2/commit/review gate checkers。

若仓库实际命令参数不同，沿用current测试调用方式，并在handoff记录真实命令/结果。

## 5. AC承接

| AC | 实施步骤 |
| --- | --- |
| AC1-AC3 | Step 2-3 |
| AC4 | Step 4-5 |
| AC5 | Step 4-6 |
| AC6-AC7 | Step 4-5 |
| AC8 | Step 6-7 |
| AC9-AC11 | Step 2-4、Step 7 |
| AC12-AC13 | Step 8 |
| AC14 | Step 3、Step 7 |
| AC15-AC17 | Step 9、Step 11 |
| AC18 | Step 1、Step 10 |
| AC19 | Step 12-13 |

## 6. 风险与停止条件

- Public API/consumer需要超出Issue权威的破坏性变化：停止，回Scope Change Gate。
- #118 target schema或finalization transaction成为实现前提：停止，保留planned bridge。
- Existing legacy readiness无法安全迁移：不得创建第二gate；先修订设计并重新审批。
- Runtime开始决定semantic dimension/finding/route：拒绝实现，调整回AI owner。
- Preset同步覆盖用户文件或产生未决`.new/.bak`：停止并逐项处置。
- Clean throwaway依赖本机已安装副本或隐藏状态：验证失败，不得声称开箱即用。
- Current base/task/workspace/planning evidence stale：重新进入对应freshness/gate。
- 出现恶意actor、并发锁、TOCTOU、fault injection及其它未授权范围：排除，不实施。

## 7. 安全、部署与回滚

- 不记录secret、token、private URL或客户数据；fixtures只用去敏合成内容。
- 预计无DB migration、K8s、container与生产部署变更；Phase 2仍按changed files复验。
- 有CLI/schema/workflow/preset兼容影响，必须通过source/installed与throwaway验证。
- 回滚以单一task commit/revision commit为边界；不使用破坏性git命令。
- 未完成remote marketplace verification必须在最终说明中明确，不以本地throwaway替代。

## 8. 完成判定

只有以下全部成立才可进入task work commit：

1. AC1-AC18有current实现与命令证据。
2. Docs SSOT delta已合并且与current实现一致。
3. Canonical/installed/platform copies无drift。
4. Clean install/update/reapply通过，零未决`.new/.bak`。
5. Implementation handoff完整。
6. 独立Phase 2通过且current-scope finding为零。

随后必须再通过task commit与完整Branch Review；#116 task自身不授权push、PR mutation、
archive或finalization。
