# Implementation Plan

1. 在 `guru-check-task/runtime/common.py` 增加 index/commit Gitlink identity、
   initialized-state 验证与稳定 entry 构造，保留现有非 Gitlink digest。
2. 在 `guru-check-task/tests/test_runtime.py` 增加真实 Gitlink fixture，覆盖：
   uninitialized-clean、initialized-clean、dirty、HEAD drift、pointer drift、
   deletion、replacement、root mismatch，以及普通 identity 兼容性。
3. 增加正常 record/check wrapper 回归，证明未初始化 Gitlink 可通过 Phase 2，
   并核对 Task Commit 的 Gitlink staging 合同未被放宽。
4. 更新 `.trellis/spec/workflow/data-contracts.md`、
   `.trellis/spec/workflow/quality-guidelines.md` 及 canonical preset spec，明确
   Phase 2 Gitlink 算法兼容策略与测试矩阵；保持 canonical/dogfood 一致。
5. 运行定向 package tests、相关 integration/eval、Python compile、preset
   reapply、dogfood drift、ownership、installed parity 与 sidecar 检查。
6. 执行完整 Phase 2 semantic check；任何 finding 返回实现修复，不创建 commit。

## Risk And Rollback

- 风险集中在 Git status/index 语义判断；使用真实 Git fixture而非字符串 mock。
- 若 scope 触及共享 `guru-reviewed-content-1.0`、public schema 或 Task Commit
  executor，视为规划边界扩大，先停止并重新审批。
- 未提交状态下可通过移除本 task 的 runtime/spec/test delta 回退，不影响
  submodule 或远程状态。
