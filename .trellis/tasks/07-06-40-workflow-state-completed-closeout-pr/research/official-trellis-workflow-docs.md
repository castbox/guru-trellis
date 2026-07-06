# 官方 Trellis workflow 依据

## 来源

- <https://docs.trytrellis.app/advanced/custom-workflow.md>
- <https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md>

## 摘要

`custom-workflow` 文档说明 `.trellis/workflow.md` 是 workflow 行为的集中定义，包含 phase、skill routing、per-turn reminder 和 task.py 命令目录。`[workflow-state:STATUS]` 块由 `inject-workflow-state.py` 在每次 `UserPromptSubmit` 时读取，用于生成 `<workflow-state>` breadcrumb。文档也明确 hook 脚本是 parser-only，不内置 fallback 内容；breadcrumb 文案改动应直接编辑 workflow Markdown。

`custom-spec-template-marketplace` 文档说明 spec template marketplace 用于可复用工程约定、测试规则、review checklist 与去敏示例，不应放 `.trellis/tasks/`、`.trellis/workspace/`、active task state 或平台 prompt 文件。本任务不修改 spec template marketplace，因此只需确认没有把 issue #40 的 active task 内容写进 marketplace/spec 模板。

## 对 issue #40 的结论

近期主干已经在 Phase 3.6/3.7 与 `trellis-finish-work` 入口里覆盖 PR body、dry-run、metadata-only tail、direct `publish-pr` 非正常入口和 non-draft publish readiness 规则。但 `workflow-state:completed` 仍是一句话，缺少这些 closeout breadcrumb 要点，所以问题仍存在。

解决方案没有过时，但应收窄为：

- 只扩展 canonical `trellis/workflows/guru-team/workflow.md` 和 dogfood `.trellis/workflow.md` 中的 `[workflow-state:completed]`；
- 不改 hook Python 的解析逻辑；
- 用 hook 单元测试断言 completed breadcrumb 包含 gate stale fallback、PR body/readiness、dry-run、metadata-only tail 和 direct publish 禁止；
- 文案说明 `completed` 是 active task 被标为 completed 但尚未 finish/archive/publish 时的 fallback/legacy closeout breadcrumb，日常路径仍是 `trellis-continue` 在 Branch Review Gate 后停止，用户/session 显式调用 `trellis-finish-work`。
