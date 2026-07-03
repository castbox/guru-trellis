# 官方 Trellis 文档摘录

## Custom Workflow

来源：https://docs.trytrellis.app/advanced/custom-workflow.md

- `.trellis/workflow.md` 是 Trellis 运行开发流程的主定义，phase、skill routing、workflow-state prompt blocks 和 task command reference 都在该文件中维护。
- 修改 workflow 后，注入路径在运行时读取 `workflow.md`，不需要修改 hook 代码或重新发布 Trellis。
- 不应修改 workflow-state tag 格式、Phase/step heading 深度或 task.py 命令名这些脚本解析依赖的约定。

## Custom Spec Template Marketplace

来源：https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md

- spec template marketplace 用于复用工程约定、API 模式、测试规则、release 规则、review checklist 和脱敏示例。
- 不应把它当作远端 task store 或项目私有 runtime state。
- `index.json` 的 template `id` 是 CLI API，应稳定维护；破坏性改写需要新 id 或清晰迁移方式。
