# #454 C3 Checkout Acquisition Provenance Test Contribution

状态：`reviewed_promoted`。以下测试构成 `.61` provenance 增量的 current
acceptance authority，不替代后续 promotion-created diff gates。

- `T454-C3-11`（R454-C3-10/D454-C3-10）：transaction-created new/existing-branch worktree 写入 exact marker；existing-checkout reuse 不写 marker；marker payload 的 key、type 和 value 与 plan/result projection 一致。
- `T454-C3-12`（R454-C3-11/D454-C3-11）：正常 output-loss recovery 保持只读并恢复原 action/ownership/created flags；different-path replacement 与 same-path/same-branch/same-HEAD replacement 均 fail closed，replacement resource 保持存在且不被修改。
- `T454-C3-13`（R454-C3-11/D454-C3-11）：missing、invalid、extra/missing-field 与 mismatched marker 均返回 `acquisition_result_mismatch`，不得降级为 caller-owned success 或 Guru-owned recovery。
- `T454-C3-14`（R454-C3-12/D454-C3-12）：successful `post_acquire` 在 consumer invocation 前观察到 marker 已退休；marker retirement failure 与 callback failure 只回滚 transaction-created matching resource。
- `T454-C3-15`（R454-C3-10..12/D454-C3-10..12）：checkout substrate `27/27`、task lifecycle runtime `56/56`、compile/JSON/ownership/task/workspace/static/line/diff checks通过；package `19/20`、shared runtime `119/128`、lifecycle integration `38/44`、preset 272 with 2 errors/3 skips 与 Release matrix 如实保持未通过或未验证。

测试不得写真实 PR、merge、Issue closure、production activation 或 cleanup。
