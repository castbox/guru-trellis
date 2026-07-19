# #130 实施计划：`guru-check-task`

## 1. 执行边界

- Active task：`.trellis/tasks/07-19-130-guru-check-task`
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/130-guru-check-task`
- Branch：`feat/130-guru-check-task`
- Base：`origin/main@edbd762a93d2a06c8624b13681689e57106acda0`
- Close：#130
- Related：#127
- Follow-up：#81、#108、#131、#132
- Dispatch mode：`sub-agent`
- 主会话只负责planning、artifact、spec reconciliation、semantic gates、commit与finish编排；实现和Phase 2 check分别由Trellis sub-agent承担。

## 2. 实现前门禁

- [ ] `check-workspace-boundary.sh`返回`status=ok`，source checkout无suspicious artifact。
- [ ] `prd.md`、`design.md`、`implement.md`与Docs SSOT Plan完整。
- [ ] `implement.jsonl`、`check.jsonl`只含真实spec/research路径。
- [ ] `guru-review-contract-wording:planning_artifacts` AI review和checker返回`pass`。
- [ ] `guru-approve-task-plan`完成adequacy/provenance/unusual-scenario review。
- [ ] 主会话展示三份planning文档链接，用户给出fresh post-planning confirmation。
- [ ] Schema 2.0 `planning-approval.json` checker通过，随后`task.py start`。
- [ ] Middle-platform Knowledge Gate标记不适用：本任务只改Trellis extension仓库自身，不依赖业务middle-platform SDK/framework。
- [ ] 未完成上述门禁前不派发实现代理、不改canonical source、不写`phase2-check.json`。

## 3. 实施顺序

### Step 1：Durable SSOT First

- [ ] 更新`docs/requirements/requirement-main.md`，加入Phase 2 semantic owner、scope-before-severity、four exits和artifact v2合同。
- [ ] 更新`docs/requirements/guru-team-trellis-flow.md`的Phase 2 sequence、ownership、artifact和migration说明。
- [ ] 更新`docs/requirements/README.md`的active flow索引。
- [ ] 更新`.trellis/spec/workflow/skill-package-contract.md`，定义package、entry parity、AI/script boundary、typed exits和re-entry。
- [ ] 更新`.trellis/spec/workflow/workflow-contract.md`，把Phase 2 check收敛为mandatory invocation与global route。
- [ ] 更新`.trellis/spec/workflow/data-contracts.md`，定义`guru-phase2-check-2.0` closed union、scope qualification、findings、unverified items、digests和freshness。
- [ ] 更新`.trellis/spec/workflow/companion-scripts.md`，定义executor/recorder/checker objective boundary与legacy migration。
- [ ] 更新`.trellis/spec/workflow/quality-guidelines.md`，加入full-rerun、scope order、agent recovery、install/update测试合同。
- [ ] 更新`.trellis/spec/workflow/index.md`、`.trellis/spec/docs/public-docs.md`、`.trellis/spec/preset/overlay-guidelines.md`、`.trellis/spec/preset/upstream-ownership.md`。
- [ ] 更新root/workflow/preset README，保证安装、升级和Phase 2说明真实。

Checkpoint：durable docs/spec先表达最终合同；implementation agent随后以这些SSOT为primary input。

### Step 2：Canonical Package 与 Registry

- [ ] 新建`trellis/skills/guru-team/packages/guru-check-task/`完整package。
- [ ] 编写短`SKILL.md`和step-local SSOT `references/contract.md`。
- [ ] 编写schema 1.2 `interface.json`，声明11项entry、semantic五阶段、runtime commands和四出口。
- [ ] 编写closed `schemas/phase2-check.schema.json`，schema id固定`guru-phase2-check-2.0`。
- [ ] 编写去敏`examples/phase2-check.json`，禁止active task和本机绝对路径。
- [ ] 编写dispatcher-only wrappers并设置executable mode。
- [ ] 编写package contract tests。
- [ ] 在registry注册active package并更新extension manifest的active ids、artifact schema ids、runtime commands和version。

### Step 3：Shared Deterministic Runtime

- [ ] 升级`guru_team_trellis.py`的Phase 2 schema loader、input reader、projection、recorder和checker。
- [ ] 复用current planning、workspace、ledger、agent recovery、dirty snapshot、post-commit coverage helpers。
- [ ] 添加command result、implementation handoff、worker evidence、reviewed path digest和full-round identity projection。
- [ ] 验证scope candidate先qualification后severity；non-current candidate必须severity=null。
- [ ] 验证finding反向引用current-scope candidate和adequacy dimension。
- [ ] 验证unverified item、Gate、four-exit/route/consumer closed union。
- [ ] `passed`要求current evidence、complete dimensions、zero blocking finding/unverified item和closed agent recovery。
- [ ] Legacy schema 1.0 active artifact返回稳定migration error；archive保持不变。
- [ ] 保留post-commit ancestor/dirty-path coverage语义。
- [ ] Static audit证明runtime不生成scope、severity、adequacy、Docs consistency或pass。

### Step 4：Workflow Thin Route

- [ ] Canonical workflow mandatory invoke`guru-check-task`。
- [ ] 添加`passed`、`implementation_required`、`planning_stale`、`blocked`唯一mapping和target/stop marker。
- [ ] `planning_stale`router只消费checker-validated discriminator，不重新判断scope。
- [ ] 删除Phase 2区旧semantic checklist、finding规则、recorder invocation和step-local recovery算法。
- [ ] 保留implement/check worker dispatch、task activation和commit transition的global orchestration。
- [ ] 同步dogfood`.trellis/workflow.md`。

### Step 5：Preset Distribution 与 Installed Copies

- [ ] 更新source package validator和registry/interface tests。
- [ ] 更新preset installer/manifest tests，安装shared、Codex、Claude、Cursor package copies。
- [ ] 更新throwaway脚本，覆盖installed package、runtime commands、v2 artifact和four-exit fixture。
- [ ] 不编辑`trellis/presets/guru-team/overlays/**`中的upstream-owned asset。
- [ ] 执行preset apply同步`.trellis/guru-team/skills/**`和四平台`guru-check-task` copies。
- [ ] 检查并处理`.new`/`.bak`，最终必须为零。

### Step 6：Tests

- [ ] Package/interface/schema/example/wrapper/runtime dependency测试。
- [ ] Workflow/standalone parity和missing/stale/legacy evidence matrix。
- [ ] Official worker evidence不能独立pass fixture。
- [ ] Scope qualification order：current、scope-change、followup、out-of-scope和illegal severity组合。
- [ ] Unusual scenario：无approved trigger时只能proposal/out-of-scope，不能P0-P3。
- [ ] Adequacy dimensions、findings、unverified items和Gate引用完整性。
- [ ] Four exits、planning discriminator、consumer和Gate双向invariant。
- [ ] Finding fix必须full rerun，partial rerun、latest-chunk-only和stale round失败。
- [ ] Agent failed/unfinished/stale/replacement/completed recovery matrix。
- [ ] Dirty snapshot、reviewed path、planning/docs/ledger/authority/HEAD freshness和post-commit coverage。
- [ ] Legacy schema/CLI migration、archive unchanged和single artifact owner。

### Step 7：Dogfood、Ownership 与 Throwaway

- [ ] Source package validator通过。
- [ ] Preset apply `--all-platforms`同步dogfood，installed validator通过。
- [ ] Canonical/shared/Codex/Claude/Cursor package bytes一致。
- [ ] `check-upstream-ownership.sh`证明43条inventory不变且diff无upstream-owned mutation。
- [ ] `check-dogfood-overlay-drift.sh`通过。
- [ ] Clean throwaway完成marketplace init、preview、switch、initial preset、installed invocation和reapply。
- [ ] Throwaway执行`trellis update --force`后重新应用workflow/preset，package/runtime/route保持可用。
- [ ] Final sidecar scan为空，README命令在throwaway中执行成功。

### Step 8：当前 Task Bootstrap 与 Phase 2 Handoff

- [ ] 新package/runtime就绪后确认当前三份planning文档digest未变。
- [ ] 若new Skill不接受旧Phase 2 artifact，不修改旧artifact；当前task直接执行新`guru-check-task`完整round。
- [ ] Implementation handoff记录`ssot_first`执行、durable docs更新、task-history-only内容、tests和deferred validation。
- [ ] Check agent按new Skill contract形成raw evidence；主会话完成scope/adequacy Gate并调用recorder/checker。
- [ ] 任一current-scope finding返回implementation agent；修复后重新执行完整check。

## 4. Phase 2 Check Focus

阶段二检查代理必须覆盖：

- PRD R1-R10与AC1-AC16；
- package/interface/schema/example/wrappers/tests；
- scope qualification先于severity；
- unusual scenario和normal-operation boundary；
- requirements/design/implementation/tests/Docs SSOT adequacy；
- finding fix full rerun和agent recovery；
- workflow thin route与four-exit uniqueness；
- runtime AI/script boundary；
- legacy artifact/CLI migration和post-commit coverage；
- source/shared/Codex/Claude/Cursor distribution；
- dogfood、ownership、throwaway、update/reapply、sidecar；
- CI/CD、container、K8s/Kustomize、DB migration、Makefile影响。预期均无业务部署修改，必须基于diff确认。

命令exit 0、coverage flags或recorder success不能替代semantic check。

## 5. 验证命令

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json \
  --task .trellis/tasks/07-19-130-guru-check-task

python3 -m unittest \
  trellis.skills.guru-team.packages.guru-check-task.tests.test_contract \
  trellis.skills.guru-team.tests.test_skill_packages \
  trellis.workflows.guru-team.scripts.python.test_guru_team_trellis \
  trellis.presets.guru-team.scripts.python.test_apply_guru_team_trellis_preset \
  trellis.presets.guru-team.scripts.python.test_upstream_ownership

python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py \
  trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py

bash -n trellis/skills/guru-team/packages/guru-check-task/scripts/record-phase2-check.sh
bash -n trellis/skills/guru-team/packages/guru-check-task/scripts/check-phase2-check.sh
bash -n trellis/presets/guru-team/scripts/bash/apply.sh
bash -n trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#feat/130-guru-check-task \
  TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 \
  trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/07-19-130-guru-check-task
git diff --check
git status --short --branch
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

## 6. Commit 与 Branch Review Boundary

- [ ] Fresh `guru-check-task:passed`后mandatory invoke`guru-create-task-commit`。
- [ ] 只stage #130 durable docs、canonical package/schema/runtime/workflow/preset、Guru-owned installed copies、tests和task evidence。
- [ ] 不stage source checkout、其它worktree、ignored runtime、workspace journal、unresolved sidecar或用户无关改动。
- [ ] Commit后#131未实现前仍按当前独立Branch Review Gate覆盖`origin/main...HEAD`完整diff；不得把Phase 2 pass当作post-commit review。
- [ ] Branch Review Gate pass后停止；push、PR、archive与issue close由显式`trellis-finish-work`入口处理。

## 7. 回滚点

| 失败 | 回滚动作 |
| --- | --- |
| V2 schema无法表达four exits | 停止activation，修订planning/schema，不新建第二artifact |
| Scope/severity只能由script推断 | 删除推断逻辑，把判断交回AI Gate |
| Planning stale无法唯一路由 | 修订closed discriminator，不扩展第五exit，不接受multi-consumer |
| Workflow仍保存step-local算法 | 继续收敛workflow，不复制到平台入口 |
| Legacy CLI静默产生新pass | 改为稳定migration failure或AI-authored input path |
| Installer触碰upstream-owned overlay | 回滚该改动并修订additive package distribution |
| Dogfood/update/throwaway出现drift或sidecar | 禁止commit/publish，修复canonical/installer/managed hash |
| Review提出排除场景 | 无current requirement trigger时记录proposal/out-of-scope，不进入P0-P3或implementation |

## 8. 完成条件

- [ ] `guru-check-task`是`phase2-check.json`唯一semantic owner。
- [ ] Scope qualification、adequacy、four exits、full rerun、stale evidence和agent recovery均有production path与fixtures。
- [ ] Official unchanged worker只能提供evidence，upstream-owned files保持不变。
- [ ] Workflow、package、runtime、durable docs、tests、manifest和installed copies语义一致。
- [ ] Docs SSOT、dogfood、ownership、throwaway、update/reapply和sidecar门禁全部通过。
- [ ] Task work commit与Branch Review Gate完成后才进入后续finish/publish流程。
