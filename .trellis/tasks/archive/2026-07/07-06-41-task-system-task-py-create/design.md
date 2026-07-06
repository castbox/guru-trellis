# 设计：Task System 命令目录 reference-only 提示

## 设计边界

本次变更只修改 Guru Team workflow contract 的 Markdown 文案：

- canonical source: `trellis/workflows/guru-team/workflow.md`
- dogfood active copy: `.trellis/workflow.md`

不修改 companion scripts、installer、schema、task lifecycle Python 或官方 Trellis upstream。原因是官方 Trellis 文档明确 `workflow.md` 承载 phase、routing、per-turn reminder 和 `task.py` command catalog，workflow 行为提示应由 Markdown workflow 负责。

## 方案

在 `### Task System` 标题和命令目录正文之间插入一段短说明，位置要早于 `python3 ./.trellis/scripts/task.py create "<title>" --slug <name>`。文案采用英文，因为 surrounding workflow 章节主体为英文，并且 issue 给出的建议文本也是英文；命令名和 workflow 关键字保持 literal。

文案表达四个合同点：

1. 该命令列表是 Trellis task CLI reference only。
2. Guru Team durable / issue-backed / task-like / file-changing work 必须 Phase 0 prepare-first。
3. `workspace_mode: worktree` 禁止从 source checkout 直接运行裸 `task.py create`。
4. 裸 `task.py create` 只可作为 Phase 1.0 controlled follow-up，且 shell/editor 已在 `prepare-task` 返回的 `workspace_path`。

## 兼容性

- 对普通 Trellis native workflow 无影响，因为本仓库只修改 `guru-team` marketplace workflow。
- 对 `task.py` CLI 无影响，因为命令本身和命令列表仍保留。
- 对 installer 无新增 managed asset；但 dogfood active copy 必须与 canonical workflow 同步。

## 验证策略

- 文案验证：`rg` 检查 reference-only / prepare-first / source checkout / workspace_path 在两个 workflow 文件中出现。
- 解析验证：运行 `python3 ./.trellis/scripts/get_context.py --mode phase`，确认 workflow Markdown 改动未破坏 phase 解析。
- task artifact 验证：运行 `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-41-task-system-task-py-create`。
- diff 验证：运行 `git diff --check`。

## 风险与回滚

风险较低。若文案过长或位置不当影响 AI 注意力，可回滚插入段落或压缩为更短的 reference-only 说明；不会影响脚本执行行为。
