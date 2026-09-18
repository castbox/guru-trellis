# Design

## Current defect

`_run_cell(..., scenario="existing")` 在安装前序 preset 后把 installed extension 与固定字符串 `0.6.5-guru.36` 比较。该检查既不绑定 `--before-tag`，也无法验证 #410 指定的两个正式 predecessor。

## Design

1. 在导出 `--before-tag` 后，从 `before-source/trellis/guru-team-extension.json` 读取完整 canonical extension manifest。
2. 将安装目标 `.trellis/guru-team/extension.json` 的 `extension` 对象与该 manifest 精确比较，并同时验证 manifest 的 Trellis CLI 轴等于 `--before-cli`。
3. 在 cell summary 中记录前序 tag、extension version 和 CLI identity。
4. 增加 `mode=existing`：验证 candidate Fork source 与 predecessor source，解析 annotated before tag，只构造选定平台的一个 existing cell，检查 source 在执行期间无漂移，并输出独立 summary。
5. official update 后先计算 active workflow 的精确 managed identity：retirement migration 的 `--force --migrate` 路径绑定 pinned candidate Trellis 的 native workflow template；普通 `--skip-all` 路径绑定 immutable predecessor workflow。preview/switch helper 在任何 `--create-new` 或 `--force` 前逐字节拒绝未知状态。
6. shell wrapper 增加 `--before-tag`、`--before-cli`、`--platform` 转发；默认值保持现有 full/focused 行为。

## Compatibility

这是现有 validator 的直接修正和一个窄化执行 profile。`full` 仍运行原六 cell catalog，`focused` 仍只证明 current-source clean/update/reapply；不增加 fallback、双写、旧硬编码或长期兼容层。

## Docs and architecture

不改变公共 Guru Skill、workflow、schema、manifest 或 Architecture/RDT authority。仅更新 maintainer-facing preset verifier 文档以列出新的定向模式。
