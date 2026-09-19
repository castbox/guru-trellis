# #438 实施计划

## Ordered Steps

1. 在 canonical `guru-create-task-workspace` executor 中抽取/新增最小 session attach helper，复用 `common.active_task.resolve_context_key` 与 `set_active_task`，不调用 `task.py start`。
2. 将 attach 插入 task identity reread 之后、创建结果可返回之前，并把新 binding 纳入已有 rollback 记录。
3. 为 package runtime 增加成功、无 context、attach failure、rollback 和 cross-session isolation 测试。
4. 更新 canonical package 文档/fixtures（如 public contract 或 eval 需要反映创建后的 planning binding），然后通过 preset apply 同步 dogfood projection。
5. 运行定向 package tests、installed integration/transcript checks、Python compile、shell syntax、task validation 和 `git diff --check`。

## Expected Files

- `trellis/skills/guru-team/packages/guru-create-task-workspace/runtime/execute.py`：创建后 attach 与 rollback。
- `trellis/skills/guru-team/packages/guru-create-task-workspace/tests/test_contract.py` 或 `tests/test_runtime.py`：回归覆盖。
- `trellis/skills/guru-team/packages/guru-create-task-workspace/SKILL.md` / contract 或 preset fixtures：只在现有行为合同需要同步时修改。
- `.trellis/guru-team/...`：由 canonical preset projection 生成并校验 drift，不手工作为唯一源头修改。

## Validation

```bash
python3 -m unittest discover -s trellis/skills/guru-team/packages/guru-create-task-workspace/tests -p 'test_*.py'
python3 -m py_compile trellis/skills/guru-team/packages/guru-create-task-workspace/runtime/*.py
python3 trellis/presets/guru-team/scripts/python/test_workspace_invocation_integration.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/09-19-438-session-binding-attach
git diff --check
```

## Explicit Stop Points

- 不在本任务中提交或推送。
- 不创建 PR 或关闭 Issue #438。
- 若 current session identity contract 无法在官方 runtime 中可靠取得，先报告阻塞，不添加猜测式环境变量或跨平台别名。
