# PRD：扩展 completed closeout breadcrumb

## 背景

Issue #40 要求复查 `[workflow-state:completed]` 的提示是否仍不足，并判断原方案是否因近期大量 PR 合并而过时。当前主干已经在 Phase 3.6/3.7、`trellis-finish-work` skill / prompt / command overlay、README 和 companion script 中补齐了 PR body、dry-run、metadata-only tail 与 direct publish 限制。但 canonical workflow 和 dogfood active workflow 的 `[workflow-state:completed]` 仍然只有一句：

```text
Code committed. Before `/trellis:finish-work`, confirm `review-gate.json` passed for the current HEAD. If missing or stale, run Branch Review Gate in Phase 3.5.
```

因此问题仍存在，但需求范围应收窄为同步 closeout breadcrumb，而不是重复改 finish-work 入口或 companion script。

## 目标

- 扩展 `[workflow-state:completed]`，使其覆盖 gate stale fallback、PR body readiness、dry-run、正式 finish-work、metadata-only tail 和 direct `publish-pr` 禁止。
- 说明 `completed` 状态的定位：它是 active task 处于 completed status 但还需要 closeout 的 fallback/legacy breadcrumb；当前日常路径仍由 `trellis-continue` 在 Branch Review Gate 后停止，并等待显式 `trellis-finish-work`。
- 保持官方 Trellis 扩展方式：Markdown workflow 定义判断流程，hook 脚本只解析 `[workflow-state:STATUS]`。
- 增加或更新测试，确保 Codex workflow-state hook 可以读到新的 completed breadcrumb 关键内容。

## 非目标

- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不修改 `finish-work.sh`、`publish-pr.sh`、`review-branch.sh` 的执行语义。
- 不新增新的用户日常 publish 命令或 workflow phase。
- 不把 issue #40 的任务状态写入 spec template marketplace。

## 验收标准

- `trellis/workflows/guru-team/workflow.md` 和 `.trellis/workflow.md` 的 `[workflow-state:completed]` 内容一致。
- completed breadcrumb 明确：gate 缺失、失败、stale 或 reviewer-only 时返回 Phase 3.5。
- completed breadcrumb 明确：gate 通过后创建或审查 task-local PR body，并通过 `--body-file "{TASK_DIR}/pr-body.md"` 或 `--body-artifact` 提供 readiness。
- completed breadcrumb 明确：先运行 `finish-work.sh --json --from-trellis-finish-work --body-file "{TASK_DIR}/pr-body.md" --dry-run`，审查 dry-run 后再运行去掉 `--dry-run` 的正式命令。
- completed breadcrumb 明确：finish-work 只允许 `review.md`、`review-gate.json`、PR body/readiness 等 Trellis metadata tail；非 metadata dirty 或非 metadata committed drift 要回 `trellis-continue` / Phase 2-3。
- completed breadcrumb 明确：`trellis-finish-work` 是唯一正常 publish 入口，不直接调用 `publish-pr`。
- 回归测试断言 hook parser 能注入 updated completed breadcrumb。

## Docs SSOT

本任务修改的是 workflow 行为定义本身，长效 SSOT 是 canonical `trellis/workflows/guru-team/workflow.md`，dogfood active copy 是 `.trellis/workflow.md`。公开 README 已经包含完整 finish-work closeout 规则，本任务不改变安装命令或对外命令语义；如实现后发现 README 仍有旧 completed breadcrumb 文案再补充更新。

## 中台知识门禁

不适用。本任务不涉及 Guru Team middle-platform SDK、go-guru、proto-guru、Unity3D Guru SDK 或 Flutter Guru SDK。

## 安全约束

只修改公开 workflow 文案、hook 测试和 task artifacts。不得写入 token、secret、`.env`、私有 URL 或敏感运行数据。
