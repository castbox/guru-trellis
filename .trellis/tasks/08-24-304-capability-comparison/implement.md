# Implementation Plan

## Steps

1. 校验 `/tmp/guru-304-task-intake.patch` 的 SHA-256 为
   `b355511c60a0616c557d25f7adaa8c9512fabb0ecb7e228973f9dc903271bf81`。
2. 将补丁应用到 task worktree；补丁只修改兼容性比较器和升级合同测试。
3. 检查 diff，确认 `distribution` 与 `skill_api` 仍被采集且仅从 capability
   blocking comparison 中移除。
4. 运行升级合同测试与 Python 编译检查。
5. 运行 upstream ownership、dogfood overlay drift 和 `git diff --check`。
6. 运行代表性本地 6-cell 兼容性矩阵，并明确记录 unpublished boundary。
7. 完成 Trellis check；若无 finding，再准备独立 commit 副作用计划供用户确认。

## Validation Commands

```bash
python3 trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py
python3 -m py_compile \
  trellis/presets/guru-team/scripts/python/verify_trellis_compatibility_matrix.py \
  trellis/presets/guru-team/scripts/python/test_verify_trellis_upgrade_contract.py
trellis/presets/guru-team/scripts/bash/check-upstream-ownership.sh --repo . --json
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

兼容性矩阵使用当前仓库既有命令和 `--allow-local-sample` 执行；该结果只证明本地
candidate 行为，不替代 remote/tag-pinned Release gate。

## Risk Controls

- 不修改 projection collector，避免掩盖安装或 package drift。
- 测试同时保留正向非阻断与 workflow marker 负向阻断断言。
- 不在本阶段执行任何远程 Git/GitHub 或 Release 副作用。
