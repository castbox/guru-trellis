# #251 实施计划

## 1. 实施原则

- 只在 `fix/251-finalizer-post-bind-recovery` 专用 worktree 实施。
- 先 canonical，后 preset apply 生成 installed/platform copies。
- 保持 Finalizer public input、六个 typed exits 与 Merge DTO 不变。
- Post-bind recovery 使用现有 transaction identity，不新增 tracked handoff。
- Legacy `closeout-plan.json` 采用受控 projection 退休，不 materialize current plan。
- 跳过完整 Throwaway installer；只运行 Issue #251 要求的 focused clean installed-package recovery smoke。

## 2. Phase A：Focused regression fixture

1. 在 canonical `guru-finalize-task` tests 中构造真实 Git topology：业务 reviewed HEAD 与 extension source commit 不同。
2. 构造 schema 3.0 `existing_pr_recovery` transaction，绑定唯一 Draft PR，remote/PR HEAD 等于 publication HEAD，`next_transition=archive`。
3. 构造历史 tracked schema 1.x/2.x `closeout-plan.json`，工作树删除但 index/transaction parent 仍含旧 blob。
4. 先固定当前失败：preview 误返 `reprepare_required`，archive projection 缺 plan。

## 3. Phase B：Post-bind stage ownership

1. 新增/收敛 post-bind transaction predicate 与 exact validation helper。
2. 调整 `finalization_preview_context` 顺序：匹配的 post-bind current transaction 先恢复，再决定是否适用 pre-PR provenance。
3. 保持 fresh existing PR adoption 与 pre-PR provenance 原路径不变。
4. 确保 preview 输出保留 publication mode、PR identity、initial state、HEAD、remaining actions。
5. 增加 plan/payload/scope/PR/HEAD drift 与 arbitrary Open PR 负向覆盖。

## 4. Phase C：Legacy plan projection 退休

1. 修改 `build_closeout_plan`/projection 分类，使 current Finalizer 将历史 tracked-deleted plan 从 move/retained/required 集合中退休。
2. 为 archive transaction 增加唯一的 retired tracked deletion ownership，并更新 path equality、pre-move continuity、commit/archive validation。
3. 更新 `build_final_archive_projection`，不再要求 current plan 文件存在。
4. 更新 current archived/terminal recovery，使规范 archive 缺少 plan 可恢复，且重新出现/identity drift fail closed。
5. 覆盖首次 archive、archive commit/push、Draft-to-Ready、terminal `ready_for_merge` 与 owner-private cleanup。

## 5. Phase D：Contract、spec 与生成副本

1. 更新 canonical Finalizer `SKILL.md`/contract、tests/evals 和必要 schemas/examples。
2. 更新 workflow/preset durable specs 与 README 中的 current recovery/legacy retirement/验证分工。
3. 运行 canonical preset apply 同步 dogfood、installed、shared/Codex/Claude/Cursor copies。
4. 检查 ownership、byte/mode parity、overlay drift、零 `.new/.bak`。

## 6. Validation Matrix

### 6.1 Targeted source/package

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  trellis.skills.guru-team.packages.guru-finalize-task.tests.test_contract
```

实际命令按 package 的可导入路径或现有 test runner 调整，并完整覆盖 canonical Finalizer package、installed Finalizer package、shared runtime integration、preset installer 与 ownership 中受影响的 tests。

### 6.2 Focused installed-package recovery smoke

- 创建 disposable fixture repo/目录；
- 通过 managed installation projection 放入 current canonical Finalizer package/runtime；
- 从 installed public wrapper 运行本 Issue 的 same-plan post-bind recovery；
- 断言 preview、archive、archive push、Ready、三方 HEAD、terminal output 与 cleanup；
- 不调用 README 完整 throwaway verifier，不执行 initial install、workflow preview/switch、official update、preset reapply 或 tag-pinned smoke。

### 6.3 Canonical/dogfood

```bash
trellis/presets/guru-team/scripts/bash/apply.sh --repo .
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
git diff --check
find . -name '*.new' -o -name '*.bak'
```

### 6.4 Task gate

- `guru-check-task` 覆盖完整 Issue #251 scope，而不是以 targeted tests 替代。
- Findings 修复后重跑受影响完整集合。
- 明确记录完整 Throwaway installer 与 #254 Release Gate 未执行。

## 7. 实施/检查子 Agent 分工

- Implement Agent：仅修改 approved plan 范围内的 canonical Finalizer、tests/evals、durable docs，并运行 targeted tests；不得 commit、push、PR、merge、cleanup 或完整 throwaway installer。
- Check Agent：独立读取 Issue、planning、current diff 与 tests，执行 Phase 2 semantic check；不得把 skipped Release Gate 写成 pass，不得自行扩张到 #254。
- 主会话：处理 planning approval、spec reconciliation、finding 修复协调、commit/finish 的后续独立副作用边界。

## 8. Stop Conditions

- Live Issue #251 authority、base 或 task scope material drift。
- 需要改变 public typed exits、进入 verifier、修改真实业务仓或吸收 #254 Release Gate。
- Post-bind predicate 无法在不放宽 arbitrary PR/HEAD recovery 的情况下成立。
- Legacy plan 退休无法通过 exact path-set/parent-blob continuity 证明。
- Canonical/installed/platform 副本或 sidecar 无法收敛。
