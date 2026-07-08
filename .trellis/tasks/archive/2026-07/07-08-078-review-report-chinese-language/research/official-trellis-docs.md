# 官方 Trellis 文档核对

## 来源

- `https://docs.trytrellis.app/advanced/custom-workflow.md`
- `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`

## 结论

- workflow 行为应写在 `.trellis/workflow.md` 这类 Markdown 合同中。官方文档说明
  phase definitions、skill routing、per-turn reminders 和 task command catalog 都由
  workflow Markdown 承载，运行时读取后生效；fork workflow 不需要改 Python、hook code
  或重新发布 Trellis。
- spec template marketplace 用于跨仓库复用工程约定、API / testing / release
  规则和 review checklist。它不是 remote task store，不应包含 `.trellis/tasks/`、
  `.trellis/workspace/`、active task state 或平台 prompt 文件。

## 对本任务的影响

- 本任务的长期流程语义应进入 `trellis/workflows/guru-team/workflow.md` 和
  `.trellis/workflow.md`，并通过 preset overlay 分发到平台入口。
- `.trellis/spec/**` 可记录可复用规范和 checklist，但不能存放 task runtime state。
- companion script 只增加确定性 validator：扫描明显英文模板标题，不替代 AI review
  或判断中文语义充分性。
