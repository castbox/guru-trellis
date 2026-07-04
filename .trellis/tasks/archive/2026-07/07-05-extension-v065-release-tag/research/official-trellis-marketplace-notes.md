# 官方 Trellis marketplace 依据

检索时间：2026-07-05

## Customizing the Workflow

来源：https://docs.trytrellis.app/advanced/custom-workflow.md

结论：

- Trellis workflow 行为由 `.trellis/workflow.md` Markdown 定义；
- Phase、skill routing、workflow-state breadcrumb 都属于 workflow markdown 控制面；
- 修改 workflow 不需要改 Python、hook code 或重新发布 Trellis upstream。

对本任务的影响：

- Guru Team 扩展继续通过官方 workflow marketplace 发布 `guru-team` workflow；
- release tag 只决定安装来源 ref，不改变 workflow template id。

## Custom Spec Template Marketplace

来源：https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md

结论：

- Git source 格式是 `provider:user/repo[/subdir][#ref]`；
- 官方示例使用 `#v1` pin branch 或 tag；
- template id 是团队公共 API，breaking rewrite 应新建 id 或 pin old behavior。

对本任务的影响：

- 稳定安装命令使用 `gh:castbox/guru-trellis/trellis#v0.6.5` 符合官方 source 格式；
- `guru-team` template id 继续保持稳定，不把版本号写进 id；
- mutable `main` 只适合作为 latest/canary，不作为可复现 release 坐标。
