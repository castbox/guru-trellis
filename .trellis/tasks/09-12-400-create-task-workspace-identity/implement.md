# 实施计划

1. 更新 readiness transition schema、change-request producer 和 workspace interface/contract，加入 discovery identity 的最小投影。
2. 更新 workspace plan preparation、executor、checker 和 task identity schema，写入并验证 `worktree_path` 与 session locator。
3. 更新 canonical package tests 与 installed integration fixtures，覆盖前置缺失、identity 冲突、合法恢复和 zero-write。
4. 同步 preset/dogfood/platform 投影，运行 drift、contract、runtime 和 installed 定向验证。
5. 运行 Phase 2 check；发现问题时只修改本 Issue 范围。

## 不变项

- 不改变 `invalid_task_state` 的唯一 stop consumer。
- 不新增第二个 workspace 创建 owner。
- 不持久化用户授权或 semantic gate 过程。
