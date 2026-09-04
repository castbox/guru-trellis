# #327 修复 Standard intake 实现阶段 task/worktree 身份绑定

## Goal

确保 Standard intake 和 active-task 实现仅能在已验证的 task worktree 中写入；补齐 stale fallback、并行 worktree 与身份漂移阻断及回归测试。

## Requirements

- Standard intake 只有在 `guru-create-task-workspace:created` 被当前调用链消费后，才能进入规划、实现、测试写入或 task artifact 写入。
- worktree 模式的每次源码、测试和 task artifact 写入前，必须重新读取并验证 repository root、cwd、branch、task.json、task branch、ignored runtime workspace/task mapping、`git worktree list` 以及当前请求与 task/workspace identity 的匹配关系。
- 缺少 created 结果、当前 checkout 无 active task/worktree identity、task/worktree/branch/runtime mapping 不一致或身份已过期时，必须 fail closed，且不得自动切换、stash、复制、迁移、清理或继续编辑。
- 实现阶段启动后新增的 worktree、dirty 修改或同一可写 checkout 的重复绑定，必须在下一次写入前被识别并阻断。
- 已有 dirty `main` checkout 不得被覆盖、清理或迁移；恢复必须进入明确的 recovery 或重新选择 workspace 路由。
- task-free current-checkout 仍按其独立合同运行，不被本需求禁止。

## Acceptance Criteria

- [ ] Standard intake 在 workspace 创建前失败或缺少 `created` typed exit 时，不产生源码、测试或 task artifact 写入。
- [ ] 当前 cwd 为 `main` 而 mapping 指向 task worktree、或 branch/task/runtime/worktree 任一身份不一致时，下一次写入被阻断。
- [ ] 运行期间新增并行 worktree、dirty 修改或重复 checkout 绑定能被下一次写入前检测。
- [ ] 正确 task worktree 中的正常实现仍可继续，task-free current-checkout 不受影响。
- [ ] 已有 dirty `main` 的场景保持原内容不变，不触发自动 stash、迁移或清理。
- [ ] canonical package、workflow/spec 与声明的平台投影保持一致，并通过针对性回归测试。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
