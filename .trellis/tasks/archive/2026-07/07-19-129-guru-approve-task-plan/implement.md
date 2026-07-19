# #129 实施计划：`guru-approve-task-plan`

## 1. 执行边界

- Active task：`.trellis/tasks/07-19-129-guru-approve-task-plan`
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/129-guru-approve-task-plan`
- Branch：`feat/129-guru-approve-task-plan`
- Base：`origin/main@56e32836376ae31d6e07862ca988c24f5654886d`
- Close scope：#129
- Related：#127、#128、#114、#112
- Follow-up：#130、#131、#132
- Dispatch mode：`sub-agent`
- 主会话不直接实现，也不直接执行 Phase 2 semantic check；实现与检查分别交给 Trellis sub-agent，主会话只负责边界、artifact、spec reconciliation、commit gate 与后续 Branch Review 编排。

## 2. 实现前门禁

- [ ] 运行 `check-workspace-boundary.sh`，结果必须是 `status=ok`，且 source checkout 无 suspicious artifact。
- [ ] `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan 完整。
- [ ] `implement.jsonl` / `check.jsonl` 只含真实 spec/research 路径，无 `_example` 行。
- [ ] `guru-review-contract-wording:planning_artifacts` AI review 与 checker 返回 `pass`。
- [ ] 主会话展示三份 planning 文档链接，用户在看到链接后给出 fresh post-planning confirmation。
- [ ] Current runtime 写入并校验 schema 1.2 `planning-approval.json`，再执行 `task.py start`。
- [ ] Middle-platform Knowledge Gate 已标记不适用。
- [ ] 未取得 post-planning confirmation 前，不派发实现代理、不写 `phase2-check.json`、不改 canonical source。

## 3. 实施顺序

### Step 1：Durable SSOT first

- [ ] 更新 `docs/requirements/requirement-main.md`，加入 #129 semantic owner、provenance、unusual confirmation、v2 artifact 与四出口合同。
- [ ] 更新 `docs/requirements/guru-team-trellis-flow.md` 的 Phase 1 sequence、ownership table、artifact table 与 migration contract。
- [ ] 更新 `docs/requirements/README.md` 的 active issue/flow 索引。
- [ ] 更新 `.trellis/spec/workflow/skill-package-contract.md`，定义 package、mode parity、entry、AI/script boundary、exit、re-entry。
- [ ] 更新 `.trellis/spec/workflow/workflow-contract.md`，把 Phase 1 approval收敛为 mandatory invocation 与typed routing。
- [ ] 更新 `.trellis/spec/workflow/data-contracts.md`，定义 `guru-planning-approval-2.0` closed union、digests、legacy migration与downstream freshness。
- [ ] 更新 `.trellis/spec/workflow/companion-scripts.md`，定义 recorder/checker objective scope与AI字段输入边界。
- [ ] 更新 `.trellis/spec/workflow/quality-guidelines.md`，加入 provenance、unusual proposal、exit matrix、bootstrap、install/update测试合同。
- [ ] 更新 `.trellis/spec/docs/public-docs.md`、`.trellis/spec/preset/overlay-guidelines.md` 与 `.trellis/spec/preset/upstream-ownership.md`，记录 public install与 additive ownership。
- [ ] 更新 `trellis/workflows/guru-team/README.md` 与 `trellis/presets/guru-team/README.md`。

Checkpoint：durable docs/spec必须先表达最终稳定合同；task artifact只保留task delta与evidence。

### Step 2：Canonical package 与 schema

- [ ] 新建 `trellis/skills/guru-team/packages/guru-approve-task-plan/`。
- [ ] 编写 `SKILL.md`，固定semantic闭环、provenance、unusual confirmation、wording调用、final Gate、recorder/checker与四出口。
- [ ] 编写 `interface.json`，使用schema 1.2、`judgment_mode=semantic`、mode parity、九项entry precondition、两个runtime command、四出口唯一consumer。
- [ ] 编写 `references/contract.md`，使其成为step-local semantic SSOT，不复制#113/#114合同。
- [ ] 新建closed `schemas/planning-approval.schema.json`，schema id为`guru-planning-approval-2.0`。
- [ ] 新建去敏 `examples/planning-approval.json`，不得出现active task、本机绝对路径或私有状态。
- [ ] 新建dispatcher-only `scripts/record-planning-approval.sh`与`check-planning-approval.sh`，设置executable bit。
- [ ] 新建package `tests/test_contract.py`，覆盖interface/schema/example/wrapper/runtime dependency与contract markers。
- [ ] 在`trellis/skills/guru-team/registry.json`注册active package。
- [ ] 更新`trellis/guru-team-extension.json`版本与必要inventory metadata。

### Step 3：Shared deterministic runtime

- [ ] 在`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`新增v2 schema loader、payload builder、facts digest与closed-union validator。
- [ ] Recorder改为消费AI-reviewed input JSON，重建task/workspace、authorities、planning file、Docs SSOT、wording、base/HEAD与dirty facts后写唯一artifact。
- [ ] Checker重建current facts并验证statement locator/digest、provenance field组合、choice refs、proposal confirmation、AI Gate、user confirmation、typed exit/consumer与facts digest。
- [ ] `approved` task activation checker必须拒绝任何非approved artifact。
- [ ] Legacy schema 1.2 active artifact必须返回稳定migration error；archive不改写。
- [ ] Downstream planning validation保留“planning content/authority改变才stale”的语义，不能只因task activation后的HEAD变化失败。
- [ ] 保持既有runtime command名；top-level compatibility wrappers与package wrappers共用同一实现。
- [ ] 运行static audit，确认runtime未生成provenance class、choice必要性、unusual scenario必要性、confirmation充分性或semantic pass。

### Step 4：Workflow thin route

- [ ] 在`trellis/workflows/guru-team/workflow.md`添加mandatory `guru-approve-task-plan` invocation与四exit mapping。
- [ ] 删除Phase 1 approval区内属于新Skill的adequacy checklist、provenance、confirmation、recorder/checker command与revision algorithm正文。
- [ ] 保留global task activation transition及其唯一`approved`入口。
- [ ] Missing package、unknown/multiple/unmapped exit与consumer冲突必须fail closed。
- [ ] 先改canonical workflow，随后同步dogfood `.trellis/workflow.md`。

### Step 5：Package validation 与 preset distribution

- [ ] 更新`trellis/skills/guru-team/tests/test_skill_packages.py`的active package、marker、exit、runtime command、schema、platform destination与copy equality检查。
- [ ] 更新`trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`及其tests，使registry-driven install包含新package与四平台discovery copy。
- [ ] 更新`trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`，加入installed package discovery、v2 approval与update/reapply链路。
- [ ] 不编辑`trellis/presets/guru-team/overlays/**`。若实现需要upstream-owned overlay变更，立即停止并返回Phase 1，不能绕过#128。
- [ ] 运行preset apply同步`.trellis/guru-team/skills/**`、`.agents/skills/**`、`.codex/skills/**`、`.claude/skills/**`、`.cursor/skills/**`dogfood副本。
- [ ] 逐个处理apply产生的`.new`/`.bak`，不得静默覆盖用户内容。

### Step 6：Runtime与package tests

- [ ] Positive：workflow/standalone各自产生`approved`，输入与输出schema/current digest一致。
- [ ] Provenance matrix：四类class各有valid fixture，缺失entry、重复id、unknown class、空authority、stale statement digest均失败。
- [ ] Choice matrix：缺alternatives、selected id、reason或no-scope-expansion字段均失败。
- [ ] Unusual matrix：explicit requirement、dedicated confirmation、general confirmation misuse、refusal、clarification route、out-of-scope均有fixture。
- [ ] Mechanism fixture：非必要lock/atomic mechanism引发风险时先返回`revision_required`，删除或替换后通过，不生成scope expansion。
- [ ] Exit matrix：四出口与Gate/consumer双向invariant；unknown/multiple/unmapped均失败。
- [ ] Freshness：requirements、wording、Docs SSOT locator、planning content、base/HEAD invocation snapshot、artifact digest stale均失败。
- [ ] Migration：schema 1.2 active artifact要求完整新review；archive bytes不变；当前#129 bootstrap可在docs digest相同下重录v2。
- [ ] Boundary：script不决定semantic字段，package不复制wording或clarification owner。

### Step 7：Dogfood、ownership 与 throwaway

- [ ] Source package validator通过。
- [ ] Preset apply `--all-platforms`同步dogfood，installed package validator通过。
- [ ] `check-dogfood-overlay-drift.sh`通过。
- [ ] `check-upstream-ownership.sh`通过，diff中无new upstream patch、baseline rewrite或unclassified asset。
- [ ] Clean throwaway完成workflow marketplace init/preview/switch、preset initial apply、package discovery、v2 approval、reapply。
- [ ] Throwaway执行`trellis update --force`，随后workflow与preset reapply，package/runtime/route保持可用。
- [ ] Final sidecar scan为空，script executable mode与manifest inventory通过。

### Step 8：当前task v2 bootstrap与Phase 2 handoff

- [ ] 新package/runtime安装后，确认本task三份planning文档digests与用户审阅版本完全相同。
- [ ] 主会话按新Skill contract重新检查adequacy/provenance/unusual scenario与current wording evidence。
- [ ] 复用本轮用户对同一三文档的post-planning confirmation录制v2 `planning-approval.json`；若digest变化则重新展示链接并请求fresh confirmation。
- [ ] 新`check-planning-approval`通过后，Phase 2检查代理方可形成final semantic report。
- [ ] 实现代理handoff必须写明`ssot_first`结果、durable docs merge、task-history-only内容、v2 bootstrap、验证状态与未覆盖项。

## 4. Phase 2 语义检查

独立 Trellis check代理必须覆盖：

- PRD R1-R10与AC1-AC15；
- package/interface/schema/example/wrappers/tests；
- provenance coverage与implementation choice分类；
- unusual scenario专用确认与mechanism removal fixture；
- workflow thin route与typed-exit uniqueness；
- shared runtime AI/script boundary；
- schema 1.2 -> v2 migration与当前task bootstrap；
- durable docs/spec/package/runtime/tests的一致性；
- shared/Codex/Claude/Cursor distribution；
- dogfood、ownership、throwaway、update/reapply、sidecar；
- CI/CD、容器、K8s/Kustomize、DB migration、Makefile影响。预期均无修改，check代理必须基于diff确认。

任一current-scope finding返回实现代理修复，再由检查代理完整复验。命令退出码为0不能替代semantic check。

## 5. 验证命令

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json \
  --task .trellis/tasks/07-19-129-guru-approve-task-plan

python3 -m unittest \
  trellis/skills/guru-team/packages/guru-approve-task-plan/tests/test_contract.py \
  trellis/skills/guru-team/tests/test_skill_packages.py \
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py \
  trellis/presets/guru-team/scripts/python/test_upstream_ownership.py

python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py \
  trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py

bash -n trellis/skills/guru-team/packages/guru-approve-task-plan/scripts/record-planning-approval.sh
bash -n trellis/skills/guru-team/packages/guru-approve-task-plan/scripts/check-planning-approval.sh
bash -n trellis/presets/guru-team/scripts/bash/apply.sh
bash -n trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

.trellis/guru-team/scripts/bash/check-planning-approval.sh --json \
  --task .trellis/tasks/07-19-129-guru-approve-task-plan
python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/07-19-129-guru-approve-task-plan
git diff --check
git status --short --branch
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

## 6. Docs SSOT checkpoint

- [ ] `docs/requirements/**`已承接用户可见流程与artifact owner。
- [ ] `.trellis/spec/workflow/**`已承接Skill/interface/runtime/schema/test合同。
- [ ] canonical package `references/contract.md`是step-local semantic SSOT。
- [ ] workflow只保留global invocation/routing。
- [ ] preset/workflow README描述真实install/update行为。
- [ ] task artifact中的稳定delta全部合并到durable docs；bootstrap过程、handoff和review证据保留为task history。

## 7. Commit 与 Branch Review边界

- [ ] Phase 2 semantic pass后，主会话记录并检查`phase2-check.json`。
- [ ] Mandatory invoke `guru-create-task-commit`；只stage #129 durable docs、canonical package/schema/runtime/workflow/preset、Guru-owned dogfood copies、tests与task work evidence。
- [ ] 不stage source checkout、其它worktree、ignored runtime/workspace、unresolved sidecar、legacy overlay drift或用户无关改动。
- [ ] Commit后独立Branch Review覆盖`origin/main...HEAD`完整diff；current-scope finding必须回到implementation + full Phase 2。
- [ ] Branch Review Gate pass后停止；push、PR、archive、remote verification与issue close只由显式`trellis-finish-work`入口执行。

## 8. 回滚点

| 失败 | 回滚动作 |
| --- | --- |
| V2 schema无法表达四出口 | 停止activation，修订schema与planning，不新建第二artifact |
| Provenance coverage只能靠script推断 | 删除推断逻辑，把coverage交回AI Gate |
| Dedicated confirmation与general confirmation无法区分 | 阻断approved，修订closed union与fixture |
| Workflow仍有step-local正文 | 继续收敛workflow，不把该正文复制到平台入口 |
| Current task bootstrap失败 | 停止Phase 2 check，重新展示三文档并请求fresh confirmation |
| Installer触碰upstream-owned overlay | 回滚该改动并修订additive distribution路径 |
| Dogfood/update/throwaway出现drift或sidecar | 禁止commit/publish，修复canonical/installer/managed hash |
| Review提出排除场景 | 无current requirement basis时不进入finding或implementation |

## 9. 完成条件

- [ ] 四typed exits、四provenance classes、unusual proposal dispositions、mode parity与migration均有production path和fixture。
- [ ] `planning-approval.json`只有`guru-approve-task-plan`一个semantic owner。
- [ ] Workflow、package、runtime、durable docs、tests、installed copies语义一致。
- [ ] Docs SSOT、dogfood、ownership、throwaway、update/reapply和sidecar门禁全部通过。
- [ ] Task work commit与Branch Review Gate完成后，才进入后续`trellis-finish-work`发布流程。
