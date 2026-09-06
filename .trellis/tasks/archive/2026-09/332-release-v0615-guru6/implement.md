# Implementation Plan

1. 更新 README、public-docs SSOT、Requirements/Design/Test freshness、preset README 和 workflow README 的 current target 为 `.6`。
2. 回读 Issue #332，确认标题/正文为 `.6/.40/CLI .15` 且 Issue 保持 OPEN。
3. 运行 release-facing 引用扫描、manifest/version 检查、`git diff --check` 和相关文档校验。
4. 通过 task check 后，按独立确认创建 task commit；本任务不执行 push、Tag、GitHub Release 或 Issue close。

## Docs SSOT Plan

- `README.md`：用户安装与更新入口的版本主表和命令。
- `.trellis/spec/docs/public-docs.md`：公共文档版本映射合同。
- `.trellis/spec/docs/requirements-design-test-ssot.md`：knowledge identity 与 publication identity freshness 说明。
- `trellis/presets/guru-team/README.md`：preset 安装、reapply 和 stable source。
- `trellis/workflows/guru-team/README.md`：workflow marketplace stable source。
