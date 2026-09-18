# #430 修复 release candidate 幂等重投影与 bytecode residue

## Goal

修复 #410 Stage 2 exact candidate 的 preset reapply provenance mutation 与 Python bytecode residue，确保修复合并后可从新 main 重新冻结并完成正式发布。

## Requirements

- R1. `apply.sh --repo . --all-platforms` 在完整 managed projection 没有变化时必须保持
  `.trellis/guru-team/extension.json` 字节不变，包括原有 `installed_at` 与 `source`。
- R2. 当 canonical manifest、managed asset、platform projection、overlay、sidecar、配置或
  package inventory 的有效安装结果发生变化时，installer 仍必须写入本次 apply 的新
  `installed_at` 与 source provenance，不能把 no-op 规则泛化为永不刷新 provenance。
- R3. 用户修改、无效旧 provenance、`.new` / `.bak` 冲突和现有 fail-closed 行为保持不变。
- R4. 原始 `apply.sh` 入口以及 Stage 2 validator 共享的 managed Python resolver 不得在
  source 或 target checkout 生成 `__pycache__`、`.pyc` 或 `.pyo`。
- R5. 修复只修改 preset installer、必要 durable contract/public README、同步 dogfood
  projection 和回归测试；不修改 extension schema、public Skill API 或 release route。
- R6. #410 的失败 candidate 和所有旧 worktree/branch/runtime mapping 不得修改、复位、清理
  或复用；修复合并后必须从新 `origin/main` 重新冻结 candidate 并从零执行 Stage 2。

## Acceptance Criteria

- [ ] AC1. 单元测试证明等价 reapply 保留 installed manifest 原始 bytes，即使当前 source
  `HEAD` 与 manifest 中记录的安装来源不同。
- [ ] AC2. 单元测试证明 managed delivery bytes 变化后 reapply 会刷新 provenance，并记录新
  source identity。
- [ ] AC3. raw `apply.sh --repo . --all-platforms` clean-checkout 回归结束后
  `git status --short`、`git diff --check` 和递归 residue scan 均为空。
- [ ] AC4. source/installed validators、Shared/Codex/Claude/Cursor parity、upstream ownership、
  dogfood drift 与 preset installer tests 全部通过。
- [ ] AC5. 文档明确 no-op provenance retention 与 Python bytecode 禁止规则，canonical 和
  installed/dogfood copies 一致。
- [ ] AC6. PR 合并后 #410 使用新 candidate 完整重跑发布门禁，不复用当前修复或旧 candidate
  的验证结论。

## Out Of Scope

- 不变更 Trellis upstream、全局 Python/npm、npm package、业务仓库或生产基础设施。
- 不扩张为任意历史版本兼容或完整累计 Release Gate matrix。
- 不新增 release-state、动态 checklist、Release body handoff 或新的持久化状态。
