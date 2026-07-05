# Issue 35 技术设计

## 设计原则

1. Markdown 控制面优先：AI 判断流程写在 `workflow.md`、skill、prompt、README 和 spec 中。
2. 脚本只做事实注入或测试校验：不把“是否创建 task / worktree”的智能判断写入 Python / Bash。
3. Guru Team 差异隔离：修复只作用于 Guru Team workflow / overlay / hook fallback 文案，不改变普通 Trellis native workflow 或 `task.py create` 本身。
4. Canonical source 优先：先改 `trellis/workflows/guru-team/` 与 `trellis/presets/guru-team/overlays/`，再通过 preset apply 同步 dogfood 副本。

## 改动边界

### Workflow

`trellis/workflows/guru-team/workflow.md` 和 `.trellis/workflow.md` 同步更新：

- Request Triage：把 issue-backed/task-like/file-changing 请求的“第一动作”写成 `check-env` + `prepare-task`。
- `[workflow-state:no_task]`：直接列命令，并明确禁止把 task creation consent 当作 direct-edit consent。
- Phase 1.0：把 `prepare-task --create-task` 作为 worktree mode 的推荐受控入口；裸 `task.py create` 只保留为已经位于 prepare 选定 `workspace_path` 且 handoff 已写入后的 follow-up。

### Overlay / Platform Prompt

`trellis-start` overlay 只做入口提示，不复制完整 workflow：

- 保留 fallback orientation 语义。
- no active task 的 issue-backed 请求直接指向 `check-env` + `prepare-task`。
- 说明 `--create-worktree --create-task` 是用户确认后的 executor 路径。
- 说明 `task creation consent` 不等于 current checkout direct-edit consent。

Codex / Cursor session-start 的 no-task fallback 文案改为与 Guru Team workflow-state 不冲突，避免启动提示先把 AI 带到“只问 task creation consent”。

### Tests

测试重点放在 parser / generated breadcrumb：

- `inject-workflow-state.py` 读取 workflow-state block 后，no_task breadcrumb 必须包含 `check-env.sh --json`、`prepare-task.sh --json`、`--create-worktree --create-task`、`task creation consent is not current-checkout direct-edit consent`。
- session-start no-task fallback 不得只包含旧的 `ask for task-creation consent before creating any Trellis task`。

## 兼容性

- 普通 Trellis native workflow 不使用 Guru Team workflow / preset overlay，本任务不修改 upstream template 或 `task.py`。
- 已安装 Guru Team 项目需要重新应用 preset 才能获得 overlay 更新；workflow marketplace 更新后新项目或切换 workflow 的项目会获得新 `workflow.md`。
- `.trellis/workflow.md` 是本仓库 dogfood active copy，需要和 canonical workflow 同步。

## Docs SSOT

本任务会影响长期 workflow 行为，应在 README / workflow README / preset README 中补充“no_task issue-backed 入口必须先 prepare/worktree”的日常入口说明，避免安装文档仍强化旧心智模型。

## 风险与回滚

- 风险：文案过长导致 workflow-state 噪声增加。控制方式：no_task block 保持短命令 + 硬边界，详细说明留在 Phase 0 / Phase 1.0。
- 风险：过度禁止轻量 task。控制方式：明确差异仅限 Guru Team + issue-backed/task-like/file-changing 请求；普通 native `task.py create` 不变。
- 回滚：回退 workflow/overlay/test/doc/spec 改动并重新 apply preset，dogfood drift check 可确认副本同步状态。
