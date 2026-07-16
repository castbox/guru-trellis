# #113 实现计划：guru-clarify-requirements

## 1. 执行前置

- [ ] 用户审查并确认 `prd.md`、`design.md`、`implement.md`。
- [ ] Main session 完成 ambiguity review与 controlled-wording classification，写入并验证 `planning-approval.json`。
- [ ] `task.py start` 把 task状态切换为 `in_progress`。
- [ ] `trellis-before-dev` 注入 workflow/preset/docs specs与共享 guides。
- [ ] Main session为 `trellis-implement` sub-agent生成 current `implement.jsonl`，并验证 workspace boundary。
- [ ] Middle-platform Knowledge Gate记录为 not applicable。

## 2. Phase A：Durable SSOT

- [ ] 更新 `.trellis/spec/workflow/workflow-contract.md`：#113 mandatory route、五个 exits、staged consumer migration、active-task re-entry。
- [ ] 更新 `.trellis/spec/workflow/skill-package-contract.md`：modes、preconditions、question loop、AI Gate、confirmation、result schema与stdout-only artifact边界。
- [ ] 更新 `.trellis/spec/workflow/companion-scripts.md`：executor/recorder/checker命令、输入、输出、zero-side-effect stale path。
- [ ] 更新 `.trellis/spec/workflow/data-contracts.md`：`guru-requirements-clarification-1.0`、scope proposal、source action、content identity与active-task evidence linkage。
- [ ] 更新 `.trellis/spec/preset/installer.md`、`.trellis/spec/preset/upstream-ownership.md`：additive package/runtime/discovery assets和no-new-overlay约束。
- [ ] 更新 `.trellis/spec/docs/public-docs.md`：公开说明、version matrix与staged dependency措辞。
- [ ] 更新 `docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`：把 #55旧行为升级为 active #113 closed-loop Skill。
- [ ] 运行 docs/contract focused text checks与 `git diff --check`。

## 3. Phase B：Canonical package 与schema

- [ ] 新建 `trellis/skills/guru-team/packages/guru-clarify-requirements/`完整 package。
- [ ] 编写短 `SKILL.md`与详细 `references/contract.md`，保持 step-local SSOT且不复制 global workflow。
- [ ] 编写 `interface.json`：semantic stage profile、两种 mode parity、preconditions、runtime dependency、commands与五个 exits。
- [ ] 编写 closed Draft 2020-12 `requirements-clarification.schema.json`。
- [ ] 编写去敏 `examples/requirements-clarification.json`。
- [ ] 编写两个 dispatcher-only wrappers并设置 executable mode。
- [ ] 编写 package `tests/test_contract.py`，覆盖frontmatter/interface/contract/schema/wrapper边界。

## 4. Phase C：Shared deterministic runtime

- [ ] 在 `guru_team_trellis.py` 增加 schema loader、canonical digest、question/scope/action/result pure validators。
- [ ] 实现 `record-requirements-clarification`：仅记录AI/human结论并计算derived content/result identity。
- [ ] 实现 `check-requirements-clarification`：schema、shape、digest、GitHub freshness、task-local hash/linkage和typed exit校验。
- [ ] 证明shared runtime和package wrappers均不调用GitHub write；mutation由AI在exact confirmation后使用现有connector/`gh`执行。
- [ ] 增加 Bash runtime wrappers与 parser command registration。
- [ ] 保持 canonical workflow runtime、preset distributed runtime和dogfood runtime字节一致。

## 5. Phase D：Registry、workflow、extension 与installer

- [ ] 激活 registry entry `guru-clarify-requirements`，保持 stable id/public API。
- [ ] 迁移 #111 `context_ready` consumer到 active #113 Skill，并同步 predecessor interfaces/contracts/tests。
- [ ] 在 canonical workflow增加 #113 mandatory invocation、五个 exit mappings、workflow/stop targets和fail-closed规则。
- [ ] 同步 dogfood `.trellis/workflow.md`，不得修改 upstream-owned overlay payload。
- [ ] 更新 `trellis/guru-team-extension.json`：version、artifact schema id、active skill ids、companion command ids和managed public API。
- [ ] 更新 preset `MANAGED_ASSET_PATHS`与installer assertions，安装新增 runtime wrappers。
- [ ] 更新 representative active fixtures与 registry/interface source validation tests。

## 6. Phase E：Behavior 与回归测试

- [ ] Initial existing issue：clear、comment、body edit。
- [ ] No-issue request：proposed draft update与new issue draft。
- [ ] Standalone：context current、needs_context、refresh_context、blocked。
- [ ] Question loop：single、atomic group、partial answer、refusal、open question blocking。
- [ ] Active task：current inclusion、related、followup、new task、out-of-scope、task-local path/hash/re-entry owner。
- [ ] #127 scope proposal：exact proposal confirmation、generic confirmation rejection、refusal/defer、optional mechanism removal/replacement。
- [ ] Mutation evidence：stale preimage禁止write、exact confirmation/payload、post-mutation hash/facts。
- [ ] Exit mapping：missing/unknown/multiple/unmapped consumer全部fail closed。
- [ ] 运行package、shared runtime、preset installer、ownership validator与public API focused suites。

## 7. Phase F：Dogfood、public docs 与开箱验证

- [ ] 更新 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
- [ ] 运行 canonical preset apply同步 `.trellis/guru-team/**`、`.agents/skills/guru-*`、`.codex/skills/guru-*`、`.cursor/skills/guru-*`、`.claude/skills/guru-*`。
- [ ] 逐个处理 `.new`/`.bak`，不得覆盖未知本地修改。
- [ ] 运行 `check-upstream-ownership`、source/installed `check-skill-packages`与dogfood overlay drift。
- [ ] 运行clean throwaway workflow marketplace + preset initial install。
- [ ] 运行throwaway standalone invocation、完整五-exit fixtures、`trellis update`、workflow switch、preset reapply、all-platform discovery与recursive sidecar checks。
- [ ] 验证README安装/升级命令不依赖本机隐藏状态。

## 8. Phase G：Trellis Check 与提交门禁

- [ ] Main session更新 `check.jsonl`并派发独立 `trellis-check` sub-agent。
- [ ] Phase 2 check覆盖PRD、design、实现、tests、durable docs、public docs、canonical/dogfood copies、throwaway/update与issue scope。
- [ ] 修复finding后重复完整 check，写入fresh `phase2-check.json`。
- [ ] 评估 `.trellis/spec/`更新完整性与Docs SSOT reconciliation。
- [ ] 使用 `guru-create-task-commit`完成AI commit review、用户确认、exact staging与commit。
- [ ] Branch Review Gate覆盖`origin/main...HEAD`完整diff；finding fix后重复Phase 2与commit/review。
- [ ] 本阶段停止在通过的Branch Review Gate；`trellis-finish-work`和PR发布由后续显式入口执行。

## 9. 验证命令基线

```bash
python3 trellis/skills/guru-team/packages/guru-clarify-requirements/tests/test_contract.py
python3 trellis/skills/guru-team/tests/test_skill_packages.py
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --json --mode installed
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-16-113-guru-clarify-requirements
python3 ./.trellis/scripts/get_context.py --mode phase
git diff --check
```

实际执行时必须使用各脚本当前 `--help`和测试入口；命令名或参数发生变化时，先更新本计划与durable contract，再继续实现。

## 10. 回滚点

- Durable SSOT完成后形成首个检查点；runtime实现不得先于该检查点。
- Canonical package/runtime通过focused tests后再修改registry/workflow/manifest。
- Preset apply前记录dogfood dirty paths和managed sidecar状态。
- Throwaway失败只修正canonical source，不手工patch临时安装副本。
- 任何upstream ownership gate失败必须停止installer与后续发布验证。
