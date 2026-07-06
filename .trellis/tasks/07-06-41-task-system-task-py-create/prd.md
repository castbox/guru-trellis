# #41 在 Task System 命令目录前标注 task.py create 为 reference-only，避免绕过 Phase 0

## 目标

在 Guru Team workflow 前部 `### Task System` 命令目录之前补充明确提示，防止 AI 在 issue-backed、task-like 或 file-changing Guru Team worktree 任务中被早期 `task.py create` 命令示例锚定，从 source checkout 直接创建 Trellis task 并绕过 Phase 0 intake/preflight。

## 背景与证据

- GitHub issue: https://github.com/castbox/guru-trellis/issues/41
- 官方 Trellis `Customizing the Workflow` 文档说明：`/.trellis/workflow.md` 控制 Phase definitions、skill routing、per-turn reminders 和 `task.py` command catalog；修改 workflow 行为应编辑 Markdown workflow，不需要改 Python、hook code 或重新发布 Trellis。
- 官方 `Custom Spec Template Marketplace` 文档说明 spec template marketplace 只适合可复用工程约定、测试规则、review checklist 与去敏例子，不应用作 active task state 或项目私有运行状态；本需求不改 spec template。
- 本仓库 live grep 结果确认 `trellis/workflows/guru-team/workflow.md` 与 dogfood `.trellis/workflow.md` 的 `### Task System` 章节在命令列表前缺少 issue 要求的 reference-only 提示。

## 需求

1. 在 `trellis/workflows/guru-team/workflow.md` 的 `### Task System` 命令块前增加明确说明：
   - `Task System` 命令列表是 Trellis task CLI reference only。
   - Guru Team durable、issue-backed、task-like、file-changing work 必须先进入 Phase 0 `check-env` + `prepare-task`。
   - `workspace_mode: worktree` 下不能从 source checkout 直接运行裸 `task.py create`。
   - 裸 `task.py create` 只适用于 Phase 1.0 明确允许的 controlled follow-up，并且 shell/editor 已位于 `prepare-task` 返回的 `workspace_path`。
2. 将同样说明同步到 dogfood `.trellis/workflow.md`，保证本仓库运行副本与 canonical workflow 一致。
3. 不改 `.trellis/scripts/task.py`、companion scripts、hooks 或 Trellis upstream；本次只调整 Guru Team workflow 文案。
4. 保持普通 Trellis native workflow 的 `task.py create` 行为不变；差异只存在于 Guru Team workflow contract。

## 范围外

- 不修改 `task.py` 命令实现。
- 不修改 `prepare-task.sh` / `guru_team_trellis.py` 执行逻辑。
- 不修改 spec template marketplace 内容。
- 不创建或调整新的 workflow id、template id 或 preset API。

## Docs SSOT 与 Knowledge Gate

- Durable docs: 本仓库存在 `docs/requirements/` 作为需求类 durable docs，但本次是 issue #41 的 workflow 文案修复，不改变长期产品/API/部署/数据合同；task artifact 记录本次需求即可，无需新增 durable docs。
- Middle-platform Knowledge Gate: 不适用。本次不涉及 `go-guru`、`proto-guru`、Unity、Flutter 或 Guru Team middle-platform SDK/framework。

## 验收标准

- [ ] `trellis/workflows/guru-team/workflow.md` 的 `### Task System` 命令目录前出现 reference-only / Phase 0 prepare-first / source checkout 禁止说明。
- [ ] `.trellis/workflow.md` 同步出现相同说明。
- [ ] grep 能定位到 Task System command list 附近的 `Reference only`、`Phase 0`、`prepare-task`、`source checkout`、`workspace_path` 语义。
- [ ] `python3 ./.trellis/scripts/get_context.py --mode phase` 仍可读取 workflow phase 内容。
- [ ] `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-41-task-system-task-py-create` 通过。
- [ ] `git diff --check` 通过。
