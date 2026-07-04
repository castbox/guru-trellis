# #26 设计：worktree developer identity 继承

## 边界

修改范围限定在 Guru Team canonical workflow/preset 资产：

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- 通过 preset apply 同步出的 `.trellis/guru-team/scripts/python/guru_team_trellis.py`

不修改官方 Trellis CLI 源码、全局 npm 包或业务仓库私有规则。

## 当前问题

`git worktree add` 只 materialize Git tracked files。`.trellis/.developer` 是 gitignored runtime identity，所以新 worktree 没有该文件。后续 Trellis local runtime 通过 `.trellis/scripts/common/developer.py` / `get_context.py` 读取 developer 时失败。

同一代码路径还存在 assignee 解析缺口：`infer_assignee()` 当前返回整个 `.trellis/.developer` 文本，导致 task assignee 可能包含 `initialized_at` 等多行内容。

## 目标合同

### Developer identity 文件解析

新增 helper：

- `developer_identity_path(root) -> Path`
- `read_developer_identity(root) -> dict[str, str] | None`
- `developer_name_from_identity(identity) -> str | None`
- `infer_assignee(root, explicit)` 改为：
  - 显式 `--assignee` 优先；
  - 否则读取 `.trellis/.developer`；
  - 若存在 `name=<value>`，返回 `<value>`；
  - 兼容旧格式：如果文件没有 `=` 且是单行非空文本，返回该文本；
  - 不返回整个多行 identity 文件。

### Worktree identity 确保

新增 deterministic helper `ensure_workspace_developer_identity(source_root, workspace_path, assignee=None)`：

1. 如果 workspace 是 source checkout，本身不做复制；但如果 source 缺 identity 且无 assignee，报错。
2. 如果目标 workspace 已有 `.trellis/.developer`，保留现状。
3. 如果 source checkout 有 `.trellis/.developer`，复制到 `workspace_path/.trellis/.developer`。
4. 如果 source checkout 缺 identity，但有可用 assignee，创建最小等价 identity：
   - `name=<assignee>`
   - `initialized_at=<UTC ISO timestamp>`
5. 如果两者都没有，抛 `WorkflowError(exit_code=2)`，payload 包含：
   - `missing_identity`
   - `source_identity_path`
   - `workspace_identity_path`
   - `recovery_command`: `python3 ./.trellis/scripts/init_developer.py <name>`

该 helper 是 executor，不做“谁应该是 developer”的智能判断；只有明确输入或源 checkout 事实可用时才写文件。

### 调用点

`cmd_prepare()` 保持 planner-only 无副作用。只有 `args.create_worktree` 或 `args.create_task` 时，在 `prepare_workspace()` 返回 ready 后调用 `ensure_workspace_developer_identity()`。

调用时机放在 `create_task()` 与 `write_handoff()` 前，确保：

- `--create-worktree` 只创建 worktree 时，目标 workspace 已能跑 Trellis context；
- `--create-task` 执行 `task.py create` 前，目标 workspace 已有 developer identity；
- existing worktree 被复用时也会补齐缺失 identity。

## 文档与兼容性

- README / workflow README 补充 executor 路径会继承或初始化 `.trellis/.developer`，缺失且无法推断时阻塞并提示恢复命令。
- `intake-handoff.schema.json` 维持 permissive，不需要新增 required 字段。
- 不改变 planner-only 输出语义，不在默认 `prepare-task.sh --json` 写 identity 文件。

## 风险与回滚

- 风险：把源 checkout 的 `.trellis/.developer` 复制到目标 worktree 是本机 runtime 状态，不应进入 Git。缓解：该文件已被 `.trellis/.gitignore` 忽略，验证 diff 时确认没有提交。
- 风险：显式 `--assignee` 可能不是本机 developer 名。缓解：只有源 identity 缺失时才用显式 assignee 初始化；这是用户/调用方明确输入。
- 回滚：删除新增 helper 和调用点，恢复 `prepare_workspace()` 原行为；测试会重新暴露 issue #26。

## Docs SSOT 决策

本任务改变 Guru Team workflow/preset 的长期行为合同，需要更新 durable README / workflow text；task artifact 只保留执行证据，不作为长期唯一来源。
