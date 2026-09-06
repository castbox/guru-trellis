# Design

## Boundary

这是 release authority/documentation-only 变更。Issue #332 是远端 current
authority；仓库 canonical 文档是本地发布入口 authority。`.5` tag 和历史
Release 属于 immutable history，不参与替换。

## Mapping

| Axis | Target |
| --- | --- |
| Repository tag | `v0.6.15-guru.6` |
| Guru Team extension | `0.6.15-guru.40` |
| Official Trellis CLI | `0.6.15` |
| Predecessor | `v0.6.15-guru.5` |

所有稳定安装命令 pin 同一个 `.6` tag；扩展 revision 和 CLI 版本保持独立
但必须与 manifest 一致。Issue 更新与本地文档修改分开验证，避免把远端 authority
变更误当作代码提交证据。

## Validation

读取 Issue live body/title，扫描五个 canonical 文档的 `.5`/`.6` 引用，执行
`git diff --check`，再运行文档和版本 manifest 的定向校验。
