# #267 post-merge lifecycle authority evidence 修复设计

## Current Defect

`a41b8a34` 上唯一 active `.42` Test authority 与 Architecture current evidence 仍将
promotion-created lifecycle 写为尚待 fresh Phase 2、task commit 与 independent Branch
Review。Live PR #315 已记录上述步骤完成后合并，因此 current authority 与 live merged
history 不一致。

## Change Model

本任务使用 `ssot_first` 文档策略：

- `docs/architecture/evidence/current-evidence.md` 拥有 current Architecture evidence；
- `docs/test/versions/current-main-0.6.5-guru.42/test-plan.md` 拥有 active `.42` Test
  lifecycle evidence；
- 两个 owner 同步记录已完成 history 与尚未完成 Release gates；
- archived task 只读，不承担 current authority 修复。

目标文本不写自引用 recovery commit SHA。它只记录当前已存在的 immutable lifecycle
identity，并将本 task 的 commit、review、merge 与之后的 candidate freeze 保持为 future gate。

## Architecture Impact

本任务不改变 Architecture decision、owner、single-writer、runtime boundary、GAP lifecycle、
compatibility exit 或设计原则权衡。它只修正 current evidence 对已发生 Git/GitHub lifecycle
的表述。

Architecture owner 在 Planning、Phase 2 和 Branch Review 分别进行 fresh judgment：

- Planning 预期 `architecture_impact / target_native / reviewed_promoted`，复用现有已晋升
  #267 contribution，不创建 successor contribution；
- Phase 2 验证 before/after evidence 一致性；
- Branch Review 从完整 committed range 独立复核。

`ADR required=false`，不创建 Architecture contribution，不执行 shared-current promotion。

## Implementation

1. 从旧 finding-fix worktree 读取两个文件的精确 diff。
2. 在本 task worktree 对相同 repo-relative path 应用相同语义修改。
3. 不复制或修改旧 task 的 archived planning/checklist。
4. 执行 exact-path、archive identity、live authority、ancestor、structured docs 与定向测试。
5. Phase 2 通过后，只提交两个 authority 文件与本 active task 的 tracked planning/ledger
   文件；提交前由 `guru-create-task-commit` 精确分类全部 dirty paths。
6. 创建 committed-range Branch Review；通过后才展示 push 与 PR 计划。

## Validation Design

- Git：branch/base/dirty/index/untracked、`git diff --check`、exact paths、ancestor checks。
- Docs：Markdown links、YAML/JSON parse、`.42` unique-active 与 `.39/.41` superseded scan。
- Architecture：fresh `task_impact_sync` Planning、Phase 2 与 Branch Review stage。
- Tests：preset `81/81`、canonical verifier `17/17`、installed verifier `17/17`。
- Live authority：Issue #267 r19、PR #315 merge、main SHA、`.3` tag/Release absence、#311 OPEN。

## Failure Routing

- authority 或 scope 变化：返回 Planning。
- 两文件外出现实现 dirty path：停止并进入 scope review。
- archive byte 变化：返回 implementation，恢复 archive 原始 bytes。
- test、Architecture 或 Phase 2 failure：停止 commit。
- committed Branch Review finding：返回 implementation，修复后重跑完整 Phase 2。
