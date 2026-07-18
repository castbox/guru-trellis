# #112 `guru-create-task-workspace` 实现计划

## 1. 实现前门禁

- [ ] 主会话完成 `guru-review-contract-wording:planning_artifacts`，checker 返回 `pass`。
- [ ] 主会话展示 `prd.md`、`design.md`、`implement.md` 的 task-worktree 链接，并取得用户阅读后的
  明确实现确认。
- [ ] 主会话记录 schema 1.2 `planning-approval.json`；`ambiguity_review.status=passed`，
  `unchecked_normative_hits=[]`，七个 planning dimensions 全部为 `true`。
- [ ] `check-workspace-boundary.sh` 与 `check-planning-approval.sh` 通过后运行 `task.py start`。
- [ ] 实现阶段加载 `trellis-before-dev`，再派发 Trellis 实现角色；主会话不直接实现。
- [ ] 中台知识门禁记为 `not_applicable`：本 task 不使用 Guru Team 中台 SDK/framework。

## 2. Scope 与旧路径清理

- [ ] 以 live #112、#99、#54 和 current task artifacts 为唯一当前需求权威；禁止读取或复用旧
  #112 worktree 的 planning、代码、approval、check、review 或测试 evidence。
- [ ] 审计 current `prepare-task` mutation、developer identity helper、workflow inline route、README
  install command 与 tests，形成删除/迁移清单。
- [ ] 选择 `guru-create-task-workspace` 作为唯一 mutation owner；`prepare-task` 只保留 query mode，
  legacy mutation flags 零写入返回 migration error。
- [ ] 不改 upstream-owned overlay，不新增 compatibility overlay；#132 的移除范围保持独立。
- [ ] 所有 finding 先绑定 current requirement、approved planning 或普通 correctness，再分配 severity；
  排除场景不得进入实现。

## 3. Durable Docs SSOT checkpoint

执行 `design.md` 第 17 节 `stale_docs + ssot_first`：

- [ ] 更新 `docs/requirements/README.md`、`requirement-main.md`、
  `guru-team-trellis-flow.md`，把 planned consumer/prepare/handoff/developer identity 替换为 active
  workspace Skill、assignee route、四 artifacts 与 thin Intake chain。
- [ ] 更新 `.trellis/spec/workflow/index.md`、`workflow-contract.md`、
  `skill-package-contract.md`、`data-contracts.md`、`companion-scripts.md`、
  `quality-guidelines.md`。
- [ ] 更新 `.trellis/spec/preset/installer.md`、`overlay-guidelines.md`、
  `upstream-ownership.md` 与 `.trellis/spec/docs/public-docs.md`。
- [ ] 更新 `README.md`、`trellis/workflows/guru-team/README.md`、
  `trellis/presets/guru-team/README.md`，删除 developer name/TRELLIS_USER/`-u` Guru 安装要求。
- [ ] Public docs 明确：official Trellis clean init 的 identity/workspace 行为仍存在；Guru preset 与
  task executor 不读取、不创建、不恢复这些路径。
- [ ] Durable docs 写明两类 confirmation、created issue refresh、assignee 顺序、ordinary recovery、
  A/B merge fixture、update/reapply 与排除项。
- [ ] 在 package/runtime 改动前执行一次 docs 交叉复核；不一致时停在本 checkpoint。

## 4. Registry、package 与 interface

- [ ] 把 production registry 的 `guru-create-task-workspace` 从 `planned` 提升为 `active`，登记 package、
  interface、shared/Codex/Cursor/Claude destinations 与 workflow route id。
- [ ] 创建短 `SKILL.md` 与 `references/contract.md`，完整承接 semantic 五阶段、两类 mode、
  confirmation、re-entry、ordinary recovery 与四出口。
- [ ] 创建 interface schema 1.2 instance；workflow/standalone precondition ids 必须完全一致。
- [ ] 创建 `guru-task-workspace-plan-1.0` 与 `guru-task-workspace-result-1.0` closed schemas 和
  去身份化 examples。
- [ ] 创建三个 thin wrappers：`record-task-workspace-plan.sh`、`create-task-workspace.sh`、
  `check-task-workspace-result.sh`。
- [ ] 增加 package contract tests，证明 package 依赖完整 preset/runtime，不能独立复制运行。

## 5. Semantic forward behavior 与 plan recorder

- [ ] 实现五个 prerequisite payload 的完整 current validation；旧 schema、missing、stale、wrong exit、
  target/content/linkage mismatch 返回 `refresh_review`。
- [ ] 投影 #139 target disposition、duplicate decisions、authority impact/source action 与 readiness
  scope conclusion；workspace Skill 禁止修改这些投影。
- [ ] 实现 AI-authored naming、existing-object disposition 与 assignee route 输入合同。
- [ ] 记录 exact plan：repo、target、scope、base、branch/worktree/task、assignee、artifacts、runtime、
  command argv、confirmation scopes、AI Gate、freshness 与 plan digest。
- [ ] Recorder stdout-only，执行前后 repo snapshot一致；它只派生 canonical digest和结构校验，不生成
  naming、scope、Gate 或 route。
- [ ] 用户 target/disposition 变更与取消生成 `no_side_effect` result，并通过 zero-write checker。

## 6. Reviewed draft 与 created issue refresh

- [ ] Executor 只接受 `github_issue_mutation` confirmation 已绑定的 exact plan。
- [ ] 创建前重验 base、reviewed draft、title/body/labels、clarity/wording/readiness digests 与 live
  duplicate facts。
- [ ] 使用 exact reviewed payload 创建 issue，立即重读 live title/body/state/updated_at。
- [ ] 构造并校验 `created_issue_binding`；result 固定 `typed_exit=refresh_review`。
- [ ] 断言同一调用未创建 branch/worktree/task/runtime mapping。
- [ ] 覆盖 session interruption recovery：current live duplicate/target facts识别同一 issue，完整 Intake
  重跑后 workspace invocation 不会再次创建 issue。
- [ ] Binding missing、state 非 open、live title/body drift、draft digest mismatch 全部 fail closed。

## 7. Assignee 与 no-developer runtime

- [ ] 实现 explicit、single issue assignee、zero issue assignee -> current GitHub login 的客观候选 facts。
- [ ] Multiple/unresolved 只返回 AI question state；用户选择后 plan 记录专用 source enum 与 evidence。
- [ ] Workspace executor 始终向 `task.py create` 传 `--assignee`，删除 `.developer` fallback。
- [ ] 删除 Guru `ensure_workspace_developer_identity()` 调用、identity copy/init/recovery command 与对应
  mutation tests。
- [ ] Source/target 缺失 `.trellis/.developer` 与 `.trellis/workspace/**` 时 create/reuse成功；执行后仍
  保持缺失。
- [ ] Runtime mapping 只写 `.trellis/.runtime/guru-team/workspaces/` 与 `tasks/`，JSON actor 字段不
  参与目录层级。

## 8. Workspace/task executor 与 artifacts

- [ ] 重构现有 base/naming/GitHub/worktree/task helper，供唯一 `create-task-workspace` executor 复用；
  禁止复制第二套 creator。
- [ ] 每个 mutation boundary 重验 plan digest、base、live target、branch/worktree/task facts 与当前
  prerequisite bytes。
- [ ] 实现 `create_new`、`reuse_exact`、`conflict_blocked` object disposition。
- [ ] 运行 official `task.py create --assignee`，再设置 branch/base/scope；不得修改 official scripts。
- [ ] 从 readiness scope conclusion 写 `issue-scope-ledger.json`。
- [ ] 扩展 task-start-context schema 1.0 的 `intake_summary`，新增 optional schema properties；新 executor
  强制写 `final_source_issue_binding` 与 `prerequisite_evidence`，old tasks 保持兼容。
- [ ] 以 exact checker-passed bytes 写 `context-discovery.json` 与 `issue-review.json`。
- [ ] 写后校验 artifact schema/hash/size/mode/trackability、runtime ignore 与 workspace boundary。
- [ ] 已存在 artifact bytes 不同、task locator/branch/base/issue/status mismatch 时 `blocked`，不覆盖现有内容。

## 9. Workflow、extension、distribution 与 dogfood

- [ ] Canonical workflow 新增一次 mandatory invoke 与四个 unique exit markers；`created` 唯一进入
  Phase 1，`refresh_review` 回到 `guru-sync-base`，两个 stop各有唯一 target。
- [ ] 移除 active workflow 的 0.5-0.8 inline `check-env`/`prepare-task`/handoff route正文，保留 thin
  transition；Scope Change `retarget_context` 继续完整重跑。
- [ ] 更新 `trellis/guru-team-extension.json` patch version、active/planned ids、artifact schema ids、
  companion commands、managed paths 与 public API。
- [ ] 扩展 runtime dispatcher/parser、Bash wrapper inventory、executable assertions 与 source/installed
  package validation。
- [ ] 运行 preset apply 同步 `.trellis/workflow.md`、`.trellis/guru-team/**` 与
  shared/Codex/Cursor/Claude `guru-*` copies。
- [ ] 审计 legacy overlay baseline不变；ownership validator必须通过。
- [ ] 逐项处理 `.new/.bak`，最终 sidecar集合为空。

## 10. Installer 与 no-name throwaway

- [ ] README 与 workflow/preset README 的 Guru install command 省略 `TRELLIS_USER` 和 `-u`。
- [ ] Throwaway 记录 official `trellis 0.6.5` init baseline；在 identity/workspace 已缺失的 initialized
  repo 输入上应用 Guru preset。
- [ ] 断言 apply、`trellis update`、workflow reapply、preset reapply 均不创建 `.trellis/.developer`
  或 `.trellis/workspace/**`。
- [ ] 断言 preset 不删除 existing official identity/workspace；既有用户数据 bytes 保持不变。
- [ ] 验证新安装 repo 可发现六个 upstream Intake Skills 加 `guru-create-task-workspace`，并运行
  source/installed validators。
- [ ] 验证 shared/Codex/Cursor/Claude 声明平台的 discovery copy、interface、schema 与 wrappers一致。

## 11. A/B merge fixture

- [ ] 从同一 clean base 创建独立 A/B worktree 与 branch。
- [ ] 通过 production recorder/executor/checker创建 A/B task 与四类 task-local Intake artifacts。
- [ ] 分别生成去身份化 `finish-summary.json`，使用 production closeout helper 和 official
  `task.py archive` 完成 task-local active -> archive。
- [ ] 分别提交完整 tracked diff，记录 branch HEAD、base..HEAD、changed paths 与 forbidden paths。
- [ ] 执行 integration-ab 的 A -> B merge，第二次 merge exit 为成功且 conflict files为空。
- [ ] 执行 integration-ba 的 B -> A merge，第二次 merge exit为成功且 conflict files为空。
- [ ] 断言 A/B tracked Guru metadata path交集为空；两个 final trees 的 metadata projection一致。
- [ ] 断言 diff不含 fixed handoff、workspace、developer identity、shared runtime/index/cache。
- [ ] AI Review report记录两个顺序、完整命令/result与 no-shared-write结论。

## 12. 自动化测试与开箱门禁

- [ ] 在 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 增加 plan/result、
  prerequisite freshness、draft refresh、assignee matrix、object recovery、artifacts、no-developer 与
  A/B merge tests。
- [ ] 在 `trellis/skills/guru-team/tests/test_skill_packages.py` 增加 active package、mode parity、
  runtime commands、schemas、markers/exits、legacy no-bypass 与 platform copy tests。
- [ ] 在 package `tests/test_contract.py` 增加 wrapper/interface/schema/example/runtime dependency tests。
- [ ] 在 preset tests 增加 active package distribution、managed hash upgrade/conflict、manifest inventory、
  no-name/no-developer input、existing official identity preservation 与 no-overlay-drift tests。
- [ ] 扩展 `verify-throwaway-install.sh`，覆盖 marketplace install/preview/switch、preset apply、direct Skill
  discovery、workspace creation、update/reapply、zero sidecar 与 runtime executable mode。
- [ ] 运行 ownership fixture，证明没有 new upstream patch、baseline rewrite 或 unclassified asset。
- [ ] 增加 scope regression audit，拒绝 malicious-input、threat、TOCTOU、lock、stress、cross-OS、
  fault-injection 合同或用例。

## 13. Phase 2 验证命令

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json \
  --task .trellis/tasks/07-18-112-create-task-workspace

python3 -m unittest \
  trellis/skills/guru-team/packages/guru-create-task-workspace/tests/test_contract.py \
  trellis/skills/guru-team/tests/test_skill_packages.py \
  trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py \
  trellis/presets/guru-team/scripts/python/test_upstream_ownership.py

python3 -m py_compile \
  trellis/workflows/guru-team/scripts/python/guru_team_trellis.py \
  trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py \
  trellis/presets/guru-team/scripts/python/validate_upstream_ownership.py

bash -n trellis/workflows/guru-team/scripts/bash/record-task-workspace-plan.sh
bash -n trellis/workflows/guru-team/scripts/bash/create-task-workspace.sh
bash -n trellis/workflows/guru-team/scripts/bash/check-task-workspace-result.sh
bash -n trellis/presets/guru-team/scripts/bash/apply.sh
bash -n trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh

python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/07-18-112-create-task-workspace
git diff --check
git status --short --branch
find . -type f \( -name '*.new' -o -name '*.bak' \) -print
```

## 14. Phase 2 check 与提交边界

- [ ] 实现角色交付 handoff，说明 `ssot_first` 结果、durable docs更新、task delta merge、
  task-history-only内容、验证状态与未覆盖风险。
- [ ] 独立 Trellis check角色覆盖 PRD R1-R12、AC1-AC17、Docs SSOT、AI/script boundary、schema、
  runtime、tests、preset、dogfood、upgrade/update、A/B merge 与场景范围。
- [ ] 任一 current-scope finding 返回实现角色修复，再由 check角色完整复验；命令通过不能替代 AI check。
- [ ] Phase 2 pass 后记录并校验 `phase2-check.json`，再 mandatory invoke
  `guru-create-task-commit`。
- [ ] 只 stage #112 的 durable docs、canonical package/schema/runtime/workflow/preset、Guru-owned dogfood
  copies、tests 与 task evidence。
- [ ] 不 stage source checkout、其它 worktree、ignored runtime/workspace、legacy overlay drift、未处理
  sidecar 或用户无关改动。
- [ ] Commit 后独立 Branch Review覆盖 `origin/main...HEAD` 全 diff；current-scope finding 必须返回
  implementation + full Phase 2。
- [ ] Branch Review Gate pass 后停止；push、PR、archive、remote verifier 与 issue close只由后续
  `trellis-finish-work` 入口执行。

## 15. 风险与回滚点

| 风险 | 阻断或回滚点 |
| --- | --- |
| Workspace Skill重新决定 target | prerequisite projection test失败即删除该判断，返回 clarification owner |
| Draft创建后继续创建 task | transaction test失败即回滚 executor分支，固定 `refresh_review` |
| Legacy prepare仍能绕过 review | no-bypass test失败即阻断 registry activation |
| Assignee回退到 developer identity | no-developer matrix失败即删除 fallback |
| Existing object被覆盖 | reuse identity test失败即固定 `conflict_blocked` |
| Task context含本机 path | schema/recursive scan失败即阻断写入 |
| Script生成 AI Gate或 route | contract test发现即回滚 deterministic逻辑 |
| Official identity被 preset删除 | preservation fixture失败即回滚 installer改动 |
| Preset在缺失状态重建 identity/workspace | no-developer fixture失败即禁止 publish |
| A/B metadata path交叉 | 任一 merge顺序冲突即回滚 shared tracked write |
| Legacy overlay发生 drift | ownership/dogfood drift失败即回滚本 task引入的 overlay change |
| Update后 package丢失或产生 sidecar | throwaway/update gate失败即禁止 publish |
| Review引入排除场景 | 没有 current requirement basis时不得赋 severity或派发修复 |

## 16. 完成条件

- [ ] 三份 planning artifact 的每条合同均有 durable docs、package、runtime、schema、test 或 fixture承接。
- [ ] 四个 typed exits、两类 confirmation、assignee matrix、created issue refresh 与 ordinary recovery均有
  production path evidence。
- [ ] A/B merge fixture、throwaway、dogfood、source/installed、update/reapply与 ownership gates全部通过。
- [ ] Issue scope ledger只有 #112、#99、#54 位于 `close_issues`。
- [ ] Full diff与 working tree不含排除机制、upstream overlay扩张或 shared tracked runtime。
- [ ] Task work commit、Branch Review Gate 与后续 finish-work遵守 Guru Team workflow。
