# Branch Review Gate Dry-run Review Report

本文件用于验证 issue #20 的强制 `--review-report` 合同。

这不是最终 Branch Review Gate 审查报告；最终报告应写入同目录的 `review.md`，并在任务工作提交之后由 `review-branch.sh --review-report` 引用。

Dry-run 覆盖：

- reviewer-only passed gate 必须失败；
- 带 task-local review report 的 passed gate 必须成功并记录 `sha256`、`size_bytes`、`modified_at`；
- `--reviewer` 只作为身份字段，不替代 review report。
