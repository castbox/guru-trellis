# 官方 Trellis 文档核对

## 读取来源

- `https://docs.trytrellis.app/index.md`
- `https://docs.trytrellis.app/advanced/custom-workflow.md`
- `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`

## 结论

- workflow 行为应通过 `.trellis/workflow.md` 这类 Markdown workflow 合同表达。
- workflow phase、skill routing、per-turn state block 均由 AI runtime 读取 Markdown。
- spec template marketplace 承载可复用工程约定和 checklist，不承载 active task state。
- 本任务的提交规范属于 `guru-team` workflow / preset companion 范围，不需要修改 Trellis 上游 npm 包。
