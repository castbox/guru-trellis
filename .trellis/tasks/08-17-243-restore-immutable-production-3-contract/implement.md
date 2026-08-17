# Implementation Plan

1. 记录初始 Git 状态、目标文件 SHA、bytecode 与 sidecar snapshot。
2. 精确恢复 canonical immutable asset 的历史字节。
3. 运行 Guru preset apply，同步 installed copy 与 extension manifest，处理任何 `.new` / `.bak`。
4. 执行 targeted immutable test、相关 runtime/preset/package tests与 managed inventory/ownership/drift 检查。
5. 执行完整 Phase 2 semantic check；修复 findings 后全量重跑受影响验证。
6. 创建 reviewed task commit，随后对完整 `origin/main...HEAD` 执行独立 Branch Review。
7. Branch Review 通过后完成 publication readiness，推送并创建中文 PR，`Closes #243`。

## Explicitly Skipped

- throwaway 安装验证（用户明确免除）。
- 160x5、160x1 或其它 live GPT-5.6 Sol production matrix。
