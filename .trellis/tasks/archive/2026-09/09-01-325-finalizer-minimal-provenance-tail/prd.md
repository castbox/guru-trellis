# PRD: Finalizer 最小 Provenance Tail

## 1. 背景

正常业务 task 在 Finalizer 的 `reprepare_required` 路径中，为生成
`extension.json` 的 provenance metadata tail 调用了完整 preset apply。完整
installer 会重建安装清单并写入新的 `installed_at`，使业务仓库产生与业务
代码无关的 tracked diff。两个并行业务 PR 从同一 base 收尾时，该字段会在
合并 `origin/main` 时形成内容冲突。

Live 证据来自两个 Codex task：业务 PR #297 的唯一冲突文件是
`.trellis/guru-team/extension.json`，唯一冲突字段是 `installed_at`；另一条
正常业务 task 也走过同一标准 Finalizer 流程。Issue #325 已记录完整日志和
时间戳证据。

## 2. 目标

- Finalizer provenance reprepare 不再调用完整 preset apply 作为 metadata-tail
  producer。
- 新增或复用独立的最小 producer，仅更新允许的 `source` provenance 字段。
- 保留首次安装生成的 `installed_at`、安装清单和其它 manifest inventory。
- 保持现有 source/target 绑定、managed asset、sidecar、dirty/mutable/
  mismatch、reviewed HEAD 与越界 diff 的 fail-closed 约束。
- 完整 preset 初装、reapply 和 Trellis update 后 reapply 继续由 installer
  负责，语义不被 Finalizer 复制。

## 3. 非目标

- 不修改业务仓库中的 task、branch、PR 或 Issue。
- 不放宽 provenance source identity 或 manifest allowlist。
- 不把并发锁、TOCTOU、防攻击伪造等非常规机制加入本 Issue。
- 不执行完整多平台 Release/升级矩阵；该职责仍归专门兼容性 Issue。

## 4. 用户可见验收

1. 正常 Finalizer publication/reprepare 不改变 `installed_at`。
2. reprepare metadata tail 不执行 `apply_guru_team_trellis_preset.py`。
3. tail 只包含允许的 `source` 字段变化，并保留原 `installed_at` 与 inventory。
4. 两个并行任务不会因安装时间戳产生 `extension.json` 冲突。
5. 初装、完整 reapply、Trellis update 后 reapply 的 installer 行为保持不变。
6. canonical、dogfood、installed projection 与相关测试同步；现有 drift 检查
   通过。

## 5. 验证边界

本任务覆盖 Finalizer、provenance reprepare、installer 回归、业务并行 PR
冲突回归以及 canonical/dogfood/installed 投影。完整跨平台 throwaway 矩阵、
Release candidate 和长期升级兼容性结论不在本任务内宣称完成。
