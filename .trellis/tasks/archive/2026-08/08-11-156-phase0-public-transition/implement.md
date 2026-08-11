# #156 实施计划：Phase 0 public transition 与 source-preserving freshness

## 1. Pre-Implementation Gates

- [ ] `guru-review-contract-wording:planning_artifacts`完整扫描三份 current规划并返回 `pass`。
- [ ] `guru-approve-task-plan`确认 PRD R1-R7、A1-A12、Design P1-P8与本计划一致。
- [ ] `task.py start`只在 planning approval后执行；bootstrap例外不代表实现授权。
- [ ] 使用 `trellis-before-dev`加载本 task的 `implement.jsonl`与其中列出的七份 Specs。
- [ ] 验证实际 repo root为本 task worktree、branch为
  `codex/156-phase0-public-transition`、base为 `main`，source checkout保持clean。
- [ ] Docs SSOT策略固定为 `ssot_first`。

## 2. Ordered Implementation

### Step 1. Durable SSOT

- [ ] 更新 `.trellis/spec/workflow/skill-package-contract.md`：阶段 transition family、call-local
  semantic transport、字段 consumer use与 compatibility边界。
- [ ] 更新 `workflow-contract.md`、`data-contracts.md`、`companion-scripts.md`、
  `quality-guidelines.md`、`index.md`：single sync、prepare provenance、真实 transcript门禁。
- [ ] 更新 `docs/requirements/{README.md,requirement-main.md,guru-team-trellis-flow.md}`。

Checkpoint：durable docs与 PRD/Design一致后才修改 runtime/schema。

### Step 2. Versioned Transition And Invocation Schemas

- [ ] 新增五个 closed stage schemas及 aggregate/version identity，放在 workflow-owned canonical
  consumer/transition root。
- [ ] 新增 call-local invocation envelope schemas，分别覆盖 deterministic sync、semantic
  owner invocation与 confirmed workspace mutation；禁止 optional mega object。
- [ ] 更新 Interface 1.3 declarations、stage0 migration manifest、registry/extension inventories与
  source validator，确保六包/全部 exits/consumers/projections/version集合完全匹配。
- [ ] 为每个 transition/output字段登记 direct consumer pointer；增加 private/unconsumed/unknown
  stage/operation/version负例。

Checkpoint：source schema/manifest validation通过，任何 mixed graph失败。

### Step 3. Shared Runtime Transport

- [ ] 为 dispatcher/public wrappers实现 `--invocation -` closed stdin envelope parsing；保持
  single typed stdout与 stable error object。
- [ ] 将 public input、transition、current owner result分别验证；owner checker仍由目标 Skill拥有。
- [ ] 移除 normal route对 `stage0_owner_path`、`--owner-prerequisites`、
  `--owner-change-request`、`--owner-plan`的依赖。
- [ ] 基于 repo consumer扫描决定 legacy locator删除或 compatibility-only保留；补充 removal condition
  和 normal-route零引用测试。

Checkpoint：六包 representative wrapper各自能无 repo-local owner文件执行一个 actual exit。

### Step 4. Six-Package Transition Graph

- [ ] Sync输出 `base_current`；Discovery以 transition + live Git验证 freshness并输出
  `context_current`。
- [ ] Clarification输出 `clarity_current`；保留 duplicate/authority/confirmation语义不变。
- [ ] Wording消费 clarity并输出 `wording_current`；content_changed完整重入并废弃旧 stage。
- [ ] Readiness改为消费 transition内 checker-bound clarity/wording projections，保持十维语义 gate。
- [ ] Workspace消费 `readiness_current`，通过 call-local plan/result完成确认后的 mutation/check，
  不持久化 prerequisite bundle。
- [ ] 更新每个 package的 SKILL/contract/interface/schema/example/eval/tests及 workflow router schemas。

Checkpoint：23个既有 Phase 0 typed exit ids和唯一 consumer保持不变，完整 graph validation通过
（`3 + 3 + 6 + 3 + 5 + 3 = 23`）。

### Step 5. Single Sync And Prepare Compatibility

- [ ] 删除 workflow/Skill/platform正常路径中的低层 resolve/execute/check AI编排文案；public wrapper
  内部只执行一次 deterministic loop。
- [ ] 实现 reviewed base provenance的 source-preserving reconstruction与 live validation。
- [ ] `prepare-task`显式接收 reviewed provenance；缺失时返回
  `missing_reviewed_base_provenance`并证明零 GitHub read/fetch/intake。
- [ ] 覆盖显式 main -> omitted CLI base的 provenance-preserving case、source/candidates变化、HEAD drift、dirty与真实
  content drift。

Checkpoint：normal workflow每个 sync/refresh只观察到一次 public sync invocation。

### Step 6. Public End-To-End Transcript

- [ ] 扩展 production eval/harness，使 producer actual stdout直接进入下一 consumer envelope。
- [ ] 在 clean installed throwaway运行 existing issue happy path直至真实 workspace/task creation。
- [ ] 覆盖 reviewed draft create/refresh、duplicate retain/retarget、wording content_changed、
  readiness reroute/ready、refresh与 stop families。
- [ ] 断言零 hidden prerequisite locator、零 runtime import、expected exit只在 actual output后比较、
  pre-task repo零写入。

### Step 7. Canonical Distribution And Dogfood

- [ ] 更新 canonical workflow/README、preset installer/README/overlays、extension/registry/manifest。
- [ ] 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`同步 dogfood。
- [ ] 逐个检查并处理 `.new`/`.bak`，不得覆盖用户未知修改。
- [ ] 验证 canonical/installed/Codex/Claude/Cursor及 manifest声明平台内容一致。

### Step 8. Verification And Semantic Check

- [ ] 运行六包 contract tests、shared runtime tests、Skill graph tests、preset installer tests。
- [ ] 运行 source/installed validation、ownership、overlay drift、clean throwaway与 update/reapply。
- [ ] 运行 `git diff --check`、task validation和 current-contract static scans。
- [ ] 调用 `guru-check-task`逐项审核 R1-R7、A1-A12、P1-P8、Docs SSOT和排除范围；修复全部
  P0-P3 findings并重跑受影响证据。

## 3. Primary Files

- Durable docs：`.trellis/spec/workflow/*.md`、`docs/requirements/*.md`。
- Canonical graph：`trellis/workflows/guru-team/workflow.md`、workflow consumers/transition schemas、
  `trellis/skills/guru-team/{registry.json,migrations/**,schemas/**}`。
- Six packages：`trellis/skills/guru-team/packages/guru-{sync-base,discover-change-context,
  clarify-requirements,review-contract-wording,review-change-request,create-task-workspace}/**`。
- Runtime/tests：`trellis/workflows/guru-team/scripts/{python,bash}/**`、
  `trellis/skills/guru-team/tests/**`。
- Distribution：`trellis/guru-team-extension.json`、`trellis/presets/guru-team/**`、根/workflow/
  preset README及 installer生成的 dogfood/platform copies。

## 4. Validation Commands

Targeted contracts：

```bash
python3 -m unittest trellis.skills.guru-team.packages.guru-sync-base.tests.test_contract
python3 -m unittest trellis.skills.guru-team.packages.guru-discover-change-context.tests.test_contract
python3 -m unittest trellis.skills.guru-team.packages.guru-clarify-requirements.tests.test_contract
python3 -m unittest trellis.skills.guru-team.packages.guru-review-contract-wording.tests.test_contract
python3 -m unittest trellis.skills.guru-team.packages.guru-review-change-request.tests.test_contract
python3 -m unittest trellis.skills.guru-team.packages.guru-create-task-workspace.tests.test_contract
python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis
```

Graph and distribution：

```bash
python3 -m unittest trellis.skills.guru-team.tests.test_skill_packages
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 trellis/presets/guru-team/scripts/python/test_upstream_ownership.py
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode source
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root . --json --mode installed
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/08-11-156-phase0-public-transition
git diff --check
```

Static scans必须证明 normal canonical/installed/workflow/platform files不要求 hidden
`--owner-result`、`--owner-prerequisites`、`--owner-change-request`或`--owner-plan` locator，且不把
low-level sync steps描述为 normal workflow。Compatibility-only命中必须有明确 allowlist和测试。

## 5. Acceptance Mapping

| Acceptance | Implementation steps |
| --- | --- |
| A1-A3 | Steps 2-4、call-local wrapper tests、normal-route static scan |
| A4-A6 | Steps 4-5、base/content freshness matrix |
| A7 | Step 5、single invocation trace |
| A8-A9 | Step 6、installed public transcript |
| A10 | Step 7、source/installed/ownership/throwaway/update gates |
| A11-A12 | Step 8、guru-check-task、Branch Review/PR readiness |

## 6. Rollback Points

| Point | Trigger | Action |
| --- | --- | --- |
| RP1 | Stage schemas无法保持最小/closed | 停止 runtime实现，修订 Design并重新 planning review |
| RP2 | Transport需要暴露完整 private owner evidence | 回退该 transport delta，重新划分 transition consumer fields |
| RP3 | Sync provenance掩盖真实 drift | 回退复用路径，保留 fail closed并补充 source/head regression |
| RP4 | Preset产生 mixed graph或未知 sidecar | 停止同步，保留旧安装，修复 canonical/staging后重跑 |
| RP5 | Semantic ownership或确认边界变化 | 停止实现，重新进入 requirements clarification |

## 7. Completion Checklist

- [ ] R1-R7、A1-A12、P1-P8全部有 code/test/docs证据。
- [ ] Planning wording/approval、Phase 2 semantic check与 Branch Review均绑定 current HEAD。
- [ ] Source/installed/dogfood/platform/throwaway/update-reapply一致且零 unresolved sidecar。
- [ ] Issue scope ledger只关闭 #156。
- [ ] 未经单独授权不 commit、push、创建 PR、merge、关闭 Issue或清理 worktree。
