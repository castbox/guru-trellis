# #332 Merge eval trace 合同修复

## 目标

修复 `v0.6.15-guru.5` exact-candidate Release Gate 中阻断单仓 throwaway
验证的 Merge Skill eval 合同错误，使当前候选能够重新通过 schema 校验，并在合并后从
fresh `origin/main` 重新执行完整 pre-tag Release Gate。

## 背景与已确认事实

- 发布 authority 为 GitHub Issue #332，目标版本仍为外部 tag
  `v0.6.15-guru.5`、Guru Team extension `0.6.15-guru.40`、Trellis CLI
  `0.6.15`。
- 当前修复基线为 `origin/main@0a5f52572755dbf28f2dd3b47d7d6e0d1829738b`。
- exact-SHA 单仓 throwaway 连续两次在
  `guru-merge-task-pr/evals/evals.json` 的
  `workflow-task-work-phase2-reentry` case 失败，错误为
  `schema_mismatch`，定位到 assertion invariant `no_github_write`。
- `trellis/skills/guru-team/schemas/skill-evals.schema.json` 与
  `trellis/skills/guru-team/runtime/eval_runner.py` 仅定义
  `public_invocation_only`、`evals_not_loaded_by_skill` 和
  `private_runtime_not_read_by_agent` 三种 trace invariant。
- `no_github_write` 只出现在该 Merge eval case，runner 没有对应语义。
- `test_phase2_reentry_route_is_bound_and_requires_no_merge_mutation` 已通过
  `mutation.assert_not_called()` 独立验证 Phase 2 re-entry 不执行 Merge mutation。
- Issue #332 已规定任何 Release Gate failure 都阻断 tag，因此无需修改 Issue 正文或创建
  follow-up Issue。

## 范围

1. 删除 Merge Phase 2 re-entry eval 中未声明且不可执行的
   `no_github_write` trace assertion。
2. 保留该 eval 的 `expected_exit=phase2_reentry_required` JSON-path assertion，继续验证
   public route 与 DTO schema。
3. 通过现有单元测试继续证明 Phase 2 re-entry 不调用 Merge mutation。
4. 同步 canonical、dogfood installed、Shared、Codex、Claude、Cursor 管理副本。
5. 完成 task 级验证和标准 workflow；合并后重新冻结 fresh `origin/main` candidate，并从零
   重跑 #332 完整 Release Gate。

## 验收标准

- `guru-merge-task-pr/evals/evals.json` 可通过当前
  `guru-team-skill-evals-1.0` schema 校验。
- canonical 与所有声明平台投影中的 Merge eval bytes 一致。
- Merge package tests 通过，且无 mutation 单元测试仍实际执行并通过。
- source/installed Skill package validator、projection、preset reapply 和 dogfood drift 检查通过。
- exact-SHA 单仓 throwaway 不再因该 schema mismatch 失败。
- 不修改 Merge runtime 路由、公共 Skill I/O、trace invariant 公共枚举或 Issue #332 正文。
- 在修复 PR 合并并生成新 candidate 前，不创建或推送 tag，不创建 GitHub Release，不关闭
  Issue #332。

## 范围外

- 不新增通用 `no_github_write` trace 能力。
- 不重构 eval runner、Merge runtime 或 archived-task recovery 行为。
- 不移动本地 `main`，不清理既有 worktree/task/runtime residue。
- 不在本 task 内声称正式版本已经发布。

## 风险与约束

- 仅删除 eval assertion 不能替代 runtime 行为测试；因此必须保留并运行现有
  `mutation.assert_not_called()` 测试。
- canonical 变更必须通过 preset apply 同步所有管理副本，不能手工只改 dogfood 文件。
- task 通过并不代表 Release Gate 通过；合并后必须从新 candidate 从零验证。
