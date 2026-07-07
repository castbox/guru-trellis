# 官方 Trellis 文档依据

检查日期：2026-07-07

## Custom Workflow

来源：https://docs.trytrellis.app/advanced/custom-workflow

结论：

- `.trellis/workflow.md` 是 Trellis development workflow 的 Markdown 控制面。
- phase definitions、skill routing、per-turn reminders 和 task.py command catalog 都由 workflow markdown 描述。
- 修改 workflow 行为不需要改 Python、hook code 或重新发布 Trellis；运行时注入会读取 workflow markdown。

对本任务的含义：

- 业务项目中文文档规则属于 AI 运行时流程合同，应写入 `trellis/workflows/guru-team/workflow.md` 和 dogfood `.trellis/workflow.md`，并同步相关 overlay。

## Custom Spec Template Marketplace

来源：https://docs.trytrellis.app/advanced/custom-spec-template-marketplace

结论：

- spec template marketplace 是 Git-backed source，供 `trellis init --registry` 安装 `.trellis/spec/` 起点。
- spec template 应包含可复用工程约定、API/测试/错误处理规则、review checklist 和去敏例子。
- 不应包含 `.trellis/tasks/`、`.trellis/workspace/`、active task state、平台 prompt 文件或只属于一个仓库的 PRD。
- 发布前应在 throwaway repository 中测试 template 安装。

对本任务的含义：

- 本任务不能把业务私有规则塞入公共模板；只能记录 Guru Team 通用语言规则。
- 如果未来加入 Guru Team spec template marketplace，template id/path 属于公共 API，中文语言规则应作为可复用约定进入模板，而不是 active task state。
- 当前仓库没有独立 spec template marketplace 目录；本次主要通过 preset installer post-install 归一化和 workflow 规则覆盖官方默认模板里的英文语言行。
