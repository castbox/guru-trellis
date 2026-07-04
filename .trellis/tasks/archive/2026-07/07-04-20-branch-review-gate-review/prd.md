# #20 强制 Branch Review Gate 每次产出 review

## 背景

当前 Guru Team Branch Review Gate 已经拆分为两层：

1. AI/human 在 code-review stance 下审查完整 `origin/<base>...HEAD` diff。
2. `review-branch.sh` 作为 recorder / validator，把既有审查结论固化为 `review-gate.json`。

现有合同允许两种通过路径：`--reviewer + --evidence` 或 `--review-report`。这导致有些任务会产出 `review.md` 并在 `review-gate.json` 中记录 digest，有些任务只记录 `reviewer` 和 evidence。两者都能通过 gate，但审计形态不一致，也给“脚本记录是否等同于 review 判断”留下解释空间。

## 目标

把 `review.md` 从“when practical / such as”的可选 artifact 提升为 Branch Review Gate 的必需审查报告：

- AI/human review 判断必须先落到 task-local `review.md`。
- `review-branch.sh` 的 passed gate 必须引用该 `review.md`，并记录 digest。
- `--reviewer` 只保留为身份字段，不能单独替代 review report。

## 需求

1. `trellis-continue` / Phase 3.5 必须明确 Branch Review Gate 的顺序：
   - 先完成 AI/human review；
   - 将审查结论写入 `{TASK_DIR}/review.md`；
   - 再调用 `review-branch.sh`，并传入 `--review-report <review.md>`。
2. `review-branch.sh --pass` 必须拒绝缺少有效 `--review-report` 的调用，即使传了 `--reviewer` 和 `--evidence`。
3. `check-review-gate.sh` / `finish-work.sh` 必须拒绝缺少 `review_report` digest 的 passed gate。
4. `review-gate.json` 必须继续记录：
   - `review_report.path`
   - `review_report.sha256`
   - `review_report.size_bytes`
   - `review_report.modified_at`
   - `reviewer` 身份字段（如果提供）
5. canonical workflow、dogfood workflow、overlay skill/prompt、README、spec、unit tests 和 preset installed copy 必须语义一致。
6. 本变更必须遵守官方 Trellis 最佳实践：workflow 行为写入 Markdown workflow/skills/prompts，脚本只做确定性 recorder / validator，不把 AI review 判断写入脚本。

## 非目标

- 不修改官方 Trellis upstream 源码、全局 npm 包或 `node_modules`。
- 不新增用户必须记忆的 `review-branch` 主流程；它仍是内部 companion script。
- 不让 Python/shell 自动生成 review 判断内容；`review.md` 内容由 AI/human review 写入，脚本只校验存在性和 digest。
- 不在本任务解决 PR body 质量问题，除非必须同步说明 Review Gate 证据。

## 验收标准

- [ ] `review-branch.sh --json --pass --reviewer ... --evidence ...` 不提供 `--review-report` 时失败，错误说明必须要求 `review.md` / `--review-report`。
- [ ] `review-branch.sh --json --pass --review-report .trellis/tasks/.../review.md ...` 成功，并在 `review-gate.json` 或 dry-run payload 中记录 digest。
- [ ] `check-review-gate.sh` 对缺少 `review_report` 的旧 passed gate 失败。
- [ ] workflow 和 overlay 文案明确 `review.md` 是必产物，不再使用 “when practical” 或 reviewer-only 示例作为 passing path。
- [ ] tests 覆盖 reviewer-only pass 被拒绝、review-report pass 成功、validation 缺 report 被拒绝。
- [ ] `apply.sh --repo .` 后 dogfood installed copies 与 canonical overlays 无漂移。
- [ ] throwaway install 验证通过，确认新安装项目也获得强制 `review.md` 语义。

## Docs SSOT

本仓库没有独立 `docs/` durable docs 目录；长期规则应同步到 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、canonical workflow、dogfood workflow 和 `.trellis/spec/workflow/*`。本 task artifact 只保留 issue #20 的执行证据。

## 中台知识依据

本任务修改 Trellis workflow/preset/companion scripts，不涉及 Guru Team middle-platform SDK 或框架；Middle-platform Knowledge Gate 不适用。
