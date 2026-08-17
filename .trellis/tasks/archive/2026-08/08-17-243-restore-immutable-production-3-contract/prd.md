# #243 恢复 immutable production 3.0 contract 字节身份

## Goal

恢复 #237 意外改写的 production-current-3.0.json immutable 字节，完成相关 deterministic 验证、Branch Review，并发布 PR 关闭 #243。

## Requirements

- 恢复 `trellis/skills/guru-team/contracts/production-current-3.0.json` 在 #237 前的 immutable 字节身份，不修改测试中的 expected digest。
- 通过 canonical source 重新生成或同步 dogfood installed copy 与 managed extension manifest，保证 source/installed 字节相等。
- 仅处理 #237 引入的末尾空行删除回归；不吸收 #239、Trellis 0.7、多 workflow、多 consumer 或其它发布改造。
- 不运行 live GPT-5.6 Sol production matrix，不修改 #127、#220 或 #242 release-owned metadata。
- 用户明确免除 throwaway 安装验证；发布依据为相关 deterministic 验证、Phase 2 check 与独立 Branch Review。

## Acceptance Criteria

- [ ] canonical 与 installed `production-current-3.0.json` SHA-256 均为 `98f632f815351ae3f84af081613c1b4cde6eab7bc1341af00467755f2f4acacb`。
- [ ] immutable previous-contract、runtime、preset/package、managed inventory/ownership 与 overlay drift 相关验证全部通过，无 SKIP 冒充通过。
- [ ] canonical、installed 与 manifest 投影一致，递归检查无 `.new` / `.bak`。
- [ ] 初始与 postflight source snapshot 中 `.pyc` / `__pycache__` 为零；验证过程使用 `PYTHONDONTWRITEBYTECODE=1`。
- [ ] 完整 `origin/main...HEAD` Branch Review 无 P0-P3 finding。
- [ ] 中文 PR 准确披露未运行 throwaway 与 live model matrix，并使用 `Closes #243`；#237/#242 仅作为 related。

## Notes

- Issue authority: https://github.com/castbox/guru-trellis/issues/243
- Base authority at intake: `main@0e315fcf41c6fc918364927b93f4b84c9b944aba`.
