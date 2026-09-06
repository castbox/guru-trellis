# #332 Release Authority Remap

## Goal

将本次正式发布的唯一 current target 从已存在但 smoke 失败且不可重建的
`v0.6.15-guru.5` 调整为新的 `v0.6.15-guru.6`，保持 Guru Team extension
`0.6.15-guru.40` 与官方 Trellis CLI `0.6.15` 不变。

## Requirements

- Issue #332、README、workflow/preset 文档和 Docs SSOT 使用一致的 `.6/.40/CLI .15` 映射。
- `v0.6.15-guru.5` 作为历史失败 tag 保留，不移动、删除或重建。
- 不修改运行时代码、公共接口、历史 Release 或其他 Issue。
- 提交前验证 release-facing 文本不存在误留的 `.5` current target。

## Acceptance Criteria

- Issue #332 保持 OPEN，标题和正文 current target 均为 `v0.6.15-guru.6`。
- 五个 canonical 文档的安装命令、版本表和 freshness 说明均为 `.6/.40/CLI .15`。
- `git diff --check`、版本引用扫描和文档定向检查通过。
