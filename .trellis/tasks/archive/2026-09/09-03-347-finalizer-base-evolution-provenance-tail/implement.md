# #347 实施计划

## 1. Pre-Implementation Gates

- [x] `prd.md`、`design.md`、`implement.md` 与 Docs SSOT Plan 通过 planning wording review。
- [x] `planning_scenario_set` 只保留 live #347 定义的 supported normal scenarios。
- [x] solution mechanism qualification 接受“验证 single tail 后以 direct parent 执行现有 base-delta comparison”的单一路径。
- [x] Architecture `task_impact_sync(stage=planning)` 返回 fresh `baseline_current/no_architecture_impact`，或按真实 exit
  修订规划。
- [x] `guru-approve-task-plan` 返回 `approved`。
- [x] 向用户展示最终规划摘要；只在后续消息取得明确实施批准后运行 `task.py start`。
- [x] 激活后读取 curated `implement.jsonl`、planning、live Issue 与 current specs。

## 2. Phase A: Regression First

1. 在 canonical Finalizer tests 增加真实 Git topology：old Publication、两个 base commits、merge、single legal
   manifest-only tail。
2. 固定当前失败为 `provenance_tail_transaction_rebind_invalid` 与 `provenance_tail_parent_mismatch`。
3. 断言 tail validator 单独通过，但现有完整 binary-delta comparison 因 tail delta 返回 false。
4. 扩展 execution fixture，记录 transaction write、push、PR create/edit、archive move/commit/push 与 Ready mutation
   的顺序和次数。

## 3. Phase B: Composition Classification

1. 在 canonical `runtime/owner.py` 提取可复用的 exact base-evolution endpoint comparison。
2. 保留 pure #344 current-head endpoint。
3. 增加 #347 endpoint 解析：读取 current Publication 的唯一 parent，通过
   `provenance_tail_commit_errors()` 完整验证 tail，再以 parent 运行相同 binary-delta comparison。
4. 只在现有 provenance-shape inapplicability error set 内尝试该路径；其它 error 继续 fail closed。
5. 组合通过后复用现有 PR resolver 与 `classify_existing_pr_recovery()`，不增加 recovery mode/stage/schema。

## 4. Phase C: Execution And Idempotence

1. 执行前重读 transaction、plan、Git topology、remote、PR、scope、metadata 与 Draft/Ready state。
2. 在首个 external mutation 前写入 current-plan-bound existing-PR recovery transaction。
3. push current Publication HEAD 一次，PR create 计数为 0。
4. 验证 metadata equal 零 edit、metadata convergence 一次 edit、Ready preserve 与 Draft-to-Ready。
5. 验证 archive、archive push、terminal `ready_for_merge`。
6. 对 push、metadata、archive、archive push、Ready transition 的中断重试断言零重复 mutation。

## 5. Phase D: Negative And Compatibility Coverage

1. 覆盖额外文件、非法 manifest 字段、错误 parent、merge tail、多 tail 链与 post-base business drift。
2. 覆盖 task/repo/base/head/title/body/scope/archive/transaction 与 remote/PR drift。
3. 重跑 #342 direct tail、#344 pure merge/multiple commits、#338 equal HEAD 与现有 terminal/fork/multiple PR tests。
4. 新发现的 planning 外场景先返回 coordinator，完成 fresh normal-scenario 与 mechanism qualification；在此之前不写
   code 或 test。

## 6. Phase E: Contracts And Docs SSOT

1. 创建 `docs/requirements-design-test-contributions/347-finalizer-base-evolution-provenance-tail/`。
2. 更新 canonical Finalizer `SKILL.md` 与 `references/contract.md` 的组合恢复合同。
3. 更新 `.trellis/spec/workflow/data-contracts.md`、`companion-scripts.md`、`quality-guidelines.md` 中直接命中的 recovery
   与 validation 语义。
4. 保持 public I/O、typed exits、transaction stages 与 schema identity；出现不兼容需求时停止并返回 Phase 1。
5. 完成 task-owned RDT review；shared current promotion 走其独立 owner，不在本地实现批准中静默执行。

## 7. Phase F: Projection

1. 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
2. 检查 canonical、dogfood installed、Shared/Codex/Claude/Cursor runtime/contract/test bytes。
3. 验证 recursive `.new/.bak/.rej/.orig` 计数为 0，并通过 ownership 与 drift checks。

## 8. Validation Matrix

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
  .trellis/tasks/09-03-347-finalizer-base-evolution-provenance-tail
git diff --check
find . \( -name '*.new' -o -name '*.bak' -o -name '*.rej' -o -name '*.orig' \)
```

补充命中的 finish-family integration tests。完整 Throwaway、tag-pinned 与 Release Gate matrix 不执行，并在交付结果
中明确记录未验证边界。

## 9. Phase 2 And Review

1. Implement Agent 只修改 approved canonical Finalizer、tests、task-owned RDT、命中的 durable specs 与 generated
   projection；不执行 commit、push、PR、merge、Issue closure、release 或 cleanup。
2. Check Agent 独立读取 live #347、planning、current diff、current RDT/Architecture 与 tests，执行完整
   `guru-check-task`。
3. implementation discovery 引入 scope、risk、owner、state authority、persistence 或 dependency boundary 变化时，
   停止写入并重跑 Architecture impact。
4. Finding 修复后重跑受影响 tests、Phase 2 semantic check 与后续完整 committed-diff review。

## 10. Stop Conditions

- Live #347 authority、close scope 或 selected base 发生 material drift。
- 实现需要新增 public typed exit、transaction mode/stage/schema、跨 package owner 或 parallel classifier authority。
- 组合恢复无法在 single validated provenance tail 与 exact base binary delta 前提下成立。
- 需要 mutation #333 transaction、PR #337、#249，或执行 Release/production action。
- canonical、installed 或平台 projection 无法无 sidecar 收敛。

## 11. Completion Boundary

后续实施批准只覆盖本 worktree 内的本地实现和验证。Commit、push、PR、merge、Issue closure、Release 与 cleanup 均
需要独立的精确副作用计划与新授权。
