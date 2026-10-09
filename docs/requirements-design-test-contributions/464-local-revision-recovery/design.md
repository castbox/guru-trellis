# #464 原 owner 合同设计贡献

`DES-464-CHECK` 承接 `BEH-464-CHECK`，实现 locator 为 `trellis/skills/guru-team/packages/guru-check-task/references/contract.md` 的 Dependency-Scoped Validation。`DES-464-RECOVERY` 承接 `BEH-464-RECOVERY`，实现 locator 为 `trellis/skills/guru-team/packages/guru-review-task-delivery/references/contract.md` 的 Public Entry。

全局 routing 仍由 `trellis/workflows/guru-team/workflow.md` 唯一 continuation 编排；spec 保留跨 owner 边界与验证策略，README 只导航。当前 Architecture 为 `docs/architecture/README.md / current-main-0.6.17-guru.77 / active`；本次为 existing-boundary refinement，无新增 writer、存储、schema、exit、public DTO 或跨 Skill private-state consumer。

现有 Phase2→TaskCommit checkpoint consumer、capture ancestry、exact-tree校验和 mutation receipts 保留。旧执行事实只能由原 owner 复核后形成当前结果；result 更新不循环改变 candidate。无事实则局部重跑，不新增缓存、ledger、Generation、Freeze 或授权持久化。shared promotion 继续独立 expected-current 边界，新增 committed diff 仍走 fresh Phase2/commit/完整 Branch Review。
