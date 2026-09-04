# #358 实施计划

## 1. Pre-Implementation Gates

- [ ] `prd.md`、`design.md`、`implement.md` 通过 planning wording review。
- [ ] `planning_scenario_set` 的正向/负向候选通过 normal-scenario qualification。
- [ ] task-introduced direct reviewed-descendant predicate 通过 solution-mechanism qualification。
- [ ] Architecture `task_impact_sync(stage=planning)` 返回 fresh
  `baseline_current/no_architecture_impact`，或按其真实 route 修订规划。
- [ ] `guru-approve-task-plan` 返回 `approved`。
- [ ] 向用户展示最终规划、精确编辑范围与验证范围，并取得独立 implementation 确认。
- [ ] 激活 task 后执行 `trellis-before-dev`，重新读取 current specs 和 task context。

## 2. Phase A: Regression First

1. 在 canonical Finalizer `tests/test_contract.py` 增加真实 Git topology：旧未绑定
   transaction、evolved selected base、fresh reviewed task commit 直接作为 current Publication
   HEAD、unique existing PR/remote 停在严格祖先。
2. 固定当前失败为 `provenance_tail_transaction_rebind_invalid`，并断言 PR resolver 未被错误
   提前调用或外部 mutation 为零。
3. 增加 task/repo/base/head/scope/archive/Publication、reviewed/publication mismatch 与 ancestry
   drift 负例，并覆盖只修改已审 source path 的合法 Task Commit 与 sibling remote ancestor。

## 3. Phase B: Narrow Classifier Change

1. 调整 `provenance_tail_transaction_rebind_is_reviewed_base_descendant()` 或增加同 owner helper，
   直接校验 current reviewed/Publication HEAD，不要求额外 provenance tail parent。
2. 在 `classify_provenance_tail_transaction_rebind()` 中只对限定 error set 启用该路径。
3. 复用 existing selected-base resolution、`is_ancestor()`、transaction exact checks 和
   `classify_existing_pr_recovery()`；要求 remote 位于 predecessor-to-current lineage，不新增
   changed-path classifier、PR resolver 或状态机。
4. 保持 direct-tail、pure-base、base-plus-tail 与 reprepare 优先级和行为不变。

## 4. Phase C: Preview, Execute And Retry

1. 扩展 #333 / PR #337 去敏 preview/execute fixture，断言准确 PR、HEAD、metadata comparison、
   `strict_ancestor` 和 `push_required=true`。
2. 断言 current-plan recovery transaction 在首个外部 mutation 前写入。
3. 覆盖 Ready/Draft、metadata equal/convergence、archive 和 terminal retry；验证 push/create/edit/
   Ready/archive 的精确次数。
4. 验证 drift 在 mutation 前 fail closed，且不会删除或改写 predecessor 作为 workaround。

## 5. Phase D: Contracts And RDT

1. 创建
   `docs/requirements-design-test-contributions/358-finalizer-fresh-reviewed-rebind/` 的 manifest、
   requirements、design、test 和 traceability。
2. 更新 canonical Finalizer `references/contract.md` 及直接命中的 workflow
   `data-contracts.md`、`companion-scripts.md`、`quality-guidelines.md`；仅当实际语义受影响时更新
   `SKILL.md`。
3. 保持 public I/O、typed exits、transaction schema/mode/stage 和 registry/interface 不变；若无法
   保持则停止并重新评审。

## 6. Phase E: Projection

1. 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
2. 核对 canonical、dogfood installed、Shared/Codex/Claude/Cursor runtime/test/contract bytes。
3. 处理并确认递归 `.new`、`.bak`、`.rej`、`.orig` 为零。

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
python3 ./.trellis/scripts/task.py validate \
  .trellis/tasks/09-04-358-finalizer-fresh-reviewed-rebind
git diff --check
find . -type f \( -name '*.new' -o -name '*.bak' -o -name '*.rej' -o -name '*.orig' \)
```

补充运行 Finalizer/finish-family targeted integration、package ownership、installed projection 和
task/RDT validation。普通 Issue 不执行完整 Release/多平台 Throwaway matrix；该边界在最终报告中明确。

## 8. Stop Conditions

- 必须改变 public DTO、typed exit、transaction schema/mode/stage 或跨 Skill owner。
- 正向场景要求删除/手改 predecessor transaction、放宽 provenance 或绕过 fresh review identity。
- 需要修改 #333、PR #337 或其它外部 Issue/PR 状态。
- canonical 到 installed/platform projection 无法收敛，或出现未处理 sidecar。
- live base、Issue authority 或 accepted scope 发生 material drift。

## 9. Publication Boundaries

本次 implementation 授权不包含 commit、push、PR 创建/更新、Finalizer、merge、Issue closure 或
worktree cleanup；这些动作继续按各自 owner 和独立确认执行。
