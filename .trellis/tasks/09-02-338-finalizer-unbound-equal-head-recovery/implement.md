# #338 实施计划

## 1. Pre-Implementation Gates

- [ ] `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan 通过 planning wording review。
- [ ] `planning_scenario_set` 对 acceptance 与负向候选返回 `classified`，仅 qualified 场景进入 planning
  approval。
- [ ] Architecture `task_impact_sync(stage=planning)` 返回 fresh
  `baseline_current/no_architecture_impact`。
- [ ] `guru-approve-task-plan` 返回 `approved`。
- [ ] 用户在最新 planning summary 后明确批准实施；此前不运行 `task.py start`，不修改 product/docs
  implementation surface。
- [ ] 激活后运行 `trellis-before-dev`，读取本 task 的 curated `implement.jsonl` 与 current specs。

## 2. Phase A: Task-Owned RDT Delta

1. 创建 `docs/requirements-design-test-contributions/338-finalizer-unbound-equal-head-recovery/`。
2. 定义 requirement/behavior、design responsibility/contract、test strategy/scenario/case 与 traceability。
3. 绑定 current `.43` RDT 与 Architecture identity，不直接改写 shared current。
4. 在最终 Phase 2 check 前完成 RDT owner review、serialized promotion 与 promotion-diff recheck。

## 3. Phase B: Focused Regression First

1. 保留 fresh equality 无 transaction 的 rejection regression。
2. 增加 #333 / PR #337 去敏 fixture：ordinary transaction、`push_content`、未绑定 PR、三方一致 HEAD、
   Ready PR、body 多一个末尾 LF。
3. 固定当前失败：preview 未报告 recovery，executor 返回 existing Open PR block。
4. 为 Git/GitHub/archive mutation 建立精确 call-count assertions。

## 4. Phase C: Equality Recovery Classification

1. 在 Finalizer canonical runtime 增加 ordinary transaction equality predicate。
2. 复用 current plan/transaction identity validation、PR resolver、scope parser 与 metadata comparator。
3. 调整 `finalization_existing_pr_recovery_context()` 的分支顺序，不放宽无 transaction 的 fresh equality。
4. Preview 投影 `existing_pr_recovery`、exact PR、equal ancestry、no push、metadata decision 与 Ready action。
5. 为 stage/binding/identity/head/scope drift 增加稳定负向覆盖。

## 5. Phase D: Transaction Conversion And Execution

1. 在首个剩余 mutation 前把 exact ordinary transaction 转换为 current existing recovery transaction。
2. 绑定 PR identity、一致 HEAD、initial Draft/Ready、原始 live title/body comparison、
   `metadata_update_required`、Publication payload、scope 与 plan digest。
3. 跳过 publication push 和 PR create，复用 bind、metadata convergence、archive、push_archive、Ready
   handling 与 terminal projection。
4. 验证 metadata equal 路径零 edit，末尾 LF 路径一次 edit 和 post-update exact reread。
5. 验证 equal-HEAD `bind_pr` 恢复对缺失/不一致原始 metadata decision 和 live drift fail closed；推进到
   `archive` 后 retry 不重复 edit、archive move/commit/push 或 Ready mutation。

## 6. Phase E: Contracts, Durable Docs, Projection

1. 更新 canonical Finalizer `SKILL.md`/contract 与命中的 data/companion/quality specs。
2. 完成 task-owned RDT contribution promotion；无公共 schema/API变化时保持 Interface、registry、schema 和
   extension version 不变。
3. 运行 preset apply 同步 dogfood installed 与 Shared/Codex/Claude/Cursor copies。
4. 逐项处理 `.new`/`.bak`，运行 ownership/parity、overlay drift 与 sidecar-zero。

## 7. Validation Matrix

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root .
python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/09-02-338-finalizer-unbound-equal-head-recovery
git diff --check
find . -name '*.new' -o -name '*.bak'
```

实现后补充 installed Finalizer focused runner 与命中的 workflow integration tests。完整多平台 Throwaway、
tag-pinned 与 Release Gate matrix 不执行。

## 8. Phase 2 And Review

1. Implement Agent 仅修改 approved scope 内的 canonical Finalizer、tests、task-owned RDT contribution、
   durable specs 与 generated projection；不 commit、push、PR、merge、close、release 或 cleanup。
2. Check Agent 独立读取 live #338、planning、current diff、current RDT/Architecture 与 tests，运行 complete
   `guru-check-task`；不得把未运行的 Release matrix标为 pass。
3. 新增 scope/risk/owner/public schema 场景先进入 `implementation_discovery` normal-scenario qualification 与
   fresh Architecture impact。
4. Findings 修复后重跑受影响测试、Phase 2 semantic check 与完整 committed diff review。

## 9. Stop Conditions

- Live #338 authority、task close scope 或 selected base 发生 material drift。
- 实现要求新增 public typed exit、transaction schema、跨 package owner 或 parallel recovery authority。
- Equality recovery 无法在不放宽 arbitrary Open PR adoption 的前提下成立。
- Canonical、installed、platform projection 或 sidecar 无法收敛。
- 需要修改 #333、PR #337、#208、#249、#251 或执行 Release Gate。

## 10. Completion Boundary

本地实现、RDT/Architecture/Phase 2、task commit 与 independent Branch Review 属于后续独立阶段。Commit、
push、PR、merge、Issue closure、release 和 cleanup 均要求各自精确副作用计划与新授权。
