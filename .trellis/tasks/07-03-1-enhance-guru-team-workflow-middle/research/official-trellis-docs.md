# 官方 Trellis 文档核对

## 来源

- Customizing the Workflow: <https://docs.trytrellis.app/advanced/custom-workflow.md>
- Configuration: <https://docs.trytrellis.app/advanced/configuration.md>
- Custom Hooks: <https://docs.trytrellis.app/advanced/custom-hooks.md>
- Everyday Use: <https://docs.trytrellis.app/start/everyday-use.md>

## 对本任务的约束

- `workflow.md` 是 workflow phase、skill routing、task command catalog 和 `[workflow-state:STATUS]` breadcrumb 的主控制面。修改 workflow 行为应优先修改 marketplace workflow markdown，而不是新增分散脚本逻辑。
- `[workflow-state:STATUS]` block 会按 task status 注入每轮提示；它适合短提醒，不适合承载长篇门禁细节。
- `.trellis/config.yaml` 的 absent key 走默认值。对应到 Guru Team 自有 `.trellis/guru-team/config.yml`，新增 `middle_platform_knowledge.mode` 时也应保持“缺失即默认”的兼容语义。
- hooks 用于 SessionStart、UserPromptSubmit、PreToolUse、PostToolUse 等上下文注入或提醒；官方文档说明 task lifecycle hook failure 只打印 warning，不应把核心阻塞门禁放在非阻塞 hook。
- Trellis 当前是 skill-first 日常入口，用户主要通过自然语言、`continue`、`finish-work` 推进；Guru Team overlay 应保持入口轻量，并把详细合同指向 `.trellis/workflow.md`。

## 设计结论

- 中台知识门禁和 docs SSOT reconciliation 的长期规则放在 `trellis/workflows/guru-team/workflow.md`。
- 配置默认放在 `trellis/workflows/guru-team/config-template.yml`，并保持 preset installer 对已有 `.trellis/guru-team/config.yml` 的 preserve 语义。
- Platform overlay 只增加“按 workflow 执行 knowledge gate / docs SSOT reconciliation”的入口提醒，不复制完整规则。
- 不新增 shell companion script 来检测 MCP availability，因为 MCP availability 是 AI 平台运行时工具能力，不是稳定 shell 环境事实。
