# #342 实施计划

## 1. Pre-Implementation Gates

- [ ] `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan 通过 planning wording review。
- [ ] `planning_scenario_set` 只保留 Issue 正文中的 supported normal scenarios。
- [ ] Architecture `task_impact_sync(stage=planning)` 返回 fresh
  `baseline_current/no_architecture_impact`，或按其真实 route 修订规划。
- [ ] `guru-approve-task-plan` 返回 `approved`。
- [ ] 向用户展示最终规划摘要并在后续消息取得明确实施批准；此前不运行 `task.py start`。
- [ ] 激活后运行 `trellis-before-dev`，读取 curated `implement.jsonl` 与 current specs。

## 2. Phase A: Focused Regression First

1. 增加 #333 / PR #337 去敏 fixture：旧 ordinary/push_content/unbound transaction、旧 publication HEAD、
   current reviewed/publication 的单个 direct-child provenance tail、唯一 Ready PR 和 metadata LF 差异。
2. 固定当前失败：plan validation 后误入 current-transaction supersession，并返回
   `provenance_reprepare_base_evolution_mismatch`。
3. 增加 owner transaction write、push、PR create/edit、archive move/commit/push 和 Ready mutation 的顺序及次数断言。

## 3. Phase B: Rebind Classification

1. 在 canonical Finalizer runtime 增加 provenance-tail transaction rebind predicate/projection。
2. 复用 `provenance_tail_commit_errors()`、current plan/transaction identity、PR resolver、scope parser 与
   metadata comparator。
3. 调整 plan-mismatch 分支顺序，仅对 ordinary/push_content/unbound predecessor 尝试该路径。
4. 调用现有 strict-ancestor classifier，并生成 current-plan bound recovery transaction candidate 形成 preview。
5. 为非法 tail、业务 diff、stage/binding/identity/head/scope/archive drift 增加稳定负向覆盖。

## 4. Phase C: Rebind Execution And Existing Recovery

1. 执行前重新读取 preview 所有 live facts并比较 projection。
2. 在首个外部 mutation前一次性持久化 current-plan bound strict-ancestor recovery transaction。
3. 恰好推送一次新的 current publication HEAD；不重复旧 publication push，也不创建 PR。
4. 验证 metadata equal 零 edit、LF convergence 一次 edit 和 post-update exact reread。
5. 验证 Ready 保持、Draft-to-Ready、archive、push_archive 与 terminal `ready_for_merge`。
6. 对每个 transition 的中断重试验证 current publication push 与其余已完成副作用均不重复。

## 5. Phase D: Contracts And RDT

1. 创建 `docs/requirements-design-test-contributions/342-finalizer-provenance-tail-rebind/`。
2. 更新 canonical Finalizer `SKILL.md`/contract 与直接命中的 workflow durable specs。
3. 保持 public Skill I/O、typed exits、transaction stages 和 schema id 不变；若无法保持则停止并重新评审。
4. 完成 RDT owner review/promotion；promotion diff 重新进入 Phase 2、task commit 与 Branch Review。

## 6. Phase E: Projection

1. 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
2. 核对 canonical、dogfood installed、Shared/Codex/Claude/Cursor contract/runtime/test bytes。
3. 处理并确认递归 `.new`/`.bak`/`.rej`/`.orig` 为零。

## 7. Validation Matrix

```bash
PYTHONDONTWRITEBYTECODE=1 .trellis/guru-team/runtime/resolve-python.sh \
  . trellis/skills/guru-team/runtime \
  trellis/skills/guru-team/packages/guru-finalize-task/tests/test_contract.py
PYTHONPATH=.trellis/guru-team PYTHONDONTWRITEBYTECODE=1 \
  .trellis/guru-team/runtime/resolve-python.sh \
  . .trellis/guru-team/runtime \
  .trellis/guru-team/skills/packages/guru-finalize-task/tests/test_contract.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
.trellis/guru-team/scripts/bash/check-skill-packages.sh --root .
python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/09-03-342-finalizer-provenance-tail-rebind
git diff --check
find . \( -name '*.new' -o -name '*.bak' -o -name '*.rej' -o -name '*.orig' \)
```

补充命中的 finish-family/workflow integration tests。完整多平台 Throwaway、tag-pinned 与 Release Gate matrix
不执行，并在最终结果中明确记录。

## 8. Phase 2 And Review

1. Implement Agent 只修改 approved canonical Finalizer、tests、task-owned RDT contribution、durable specs 和
   generated projection；不 commit、push、PR、merge、close、release 或 cleanup。
2. Check Agent 独立读取 live #342、planning、current diff、current RDT/Architecture 与 tests，执行完整
   `guru-check-task`。
3. 新发现的 scope/risk/owner/public schema 场景先进入 `implementation_discovery` normal-scenario qualification
   与 fresh Architecture impact，不直接吸收。
4. Findings 修复后重跑受影响测试、Phase 2 semantic check 和完整 committed diff review。

## 9. Stop Conditions

- Live #342 authority、close scope 或 selected base 发生 material drift。
- 实现要求新增 public typed exit、transaction stage/schema、跨 package owner 或双路径 authority。
- Rebind 无法在只接受 manifest-only provenance tail 的前提下成立。
- 需要修改 #333、PR #337、#249，或执行 Release/production mutation。
- Canonical、installed 或平台 projection 无法无 sidecar 收敛。

## 10. Completion Boundary

本次实施批准只授权本地实现和验证。Commit、push、PR、merge、Issue closure、Release 和 cleanup 均需要各自的
精确副作用计划与新授权。
