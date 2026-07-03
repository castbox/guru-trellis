# #5 Require AI review prompt before Branch Review Gate artifact

## Goal

TBD.

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
# PRD：Branch Review Gate 前强制 AI Review 证据

## 背景

GitHub issue #5 指出：当前 `guru-team` workflow 虽然有 Branch Review Gate 和 `review-branch.sh` artifact，但实际执行时 Agent 容易把 `review-branch.sh --pass` 当成“完成 review”，导致没有独立的文档 + 代码 review 判断，仍可写入 passed 的 `review-gate.json` 并进入 `finish-work` / publish。

本任务要修正这个流程边界：AI/human review 是判断步骤，`review-branch.sh` 只能是 recorder / validator。

## 需求范围

1. `trellis/workflows/guru-team/workflow.md` 和 dogfood `.trellis/workflow.md` 必须明确 Branch Review Gate 拆成两个步骤：
   - 先执行 AI review prompt / code-review stance，审查 `origin/<base>...HEAD` 完整 diff。
   - 再调用 `review-branch.sh` 固化 review 结论到 gate artifact。
2. `trellis-continue` 相关 overlay 必须同步说明：先 review prompt，后 artifact recorder。
3. `trellis-finish-work` 相关入口不得暗示脚本本身完成 review；它只验证已有 gate、归档、journal、publish。
4. `review-branch.sh` / `check-review-gate.sh` 背后的 Python companion 至少新增一种机器可验证机制，避免空 `reviewer` + 自填 `--pass` 成为可发布 gate。
5. 文档必须说明 `review-branch.sh` 是 recorder / validator，不是 reviewer。
6. 必须用 dry-run 或测试任务验证：缺少 reviewer / review report / findings evidence 时，不能形成可发布 gate。

## 非目标

- 不新增用户必须手动记忆的新发布阶段。
- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不把 active task 状态写入 workflow marketplace 或 spec template。
- 不改变 `finish-work.sh` 自动 publish PR 的总体顺序。

## 验收标准

- [ ] `trellis-continue` / `.trellis/workflow.md` 明确要求先执行 AI review prompt，再调用 `review-branch.sh` 写 gate artifact。
- [ ] `trellis-finish-work` 入口说明不再暗示脚本本身完成 review。
- [ ] preset overlay 中 Codex / Claude / Cursor / shared `.agents` 入口同步更新。
- [ ] `review-branch` 或 `check-review-gate` 会阻止缺少 reviewer / review report 的 pass gate 进入 publish 路径。
- [ ] README / workflow docs 说明 `review-branch.sh` 是 recorder / validator，不是 reviewer。
- [ ] dry-run 或测试任务证明缺少 review 身份/报告证据时 gate 被阻塞。

## 文档 SSOT 与研究记录

- 本仓库目前没有独立 `docs/` durable docs 目录；长期说明分散在 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、canonical workflow 和 `.trellis/spec/`。
- 本任务会更新上述长期 workflow/preset 文档，不把 task artifact 当作唯一长期来源。
- 已核对 Trellis 官方 custom workflow 文档：流程行为应通过 `workflow.md` 等 Markdown 控制面表达；脚本只做确定性 recorder / validator。
- Middle-platform Knowledge Gate 不适用：本任务不涉及 go-guru、proto-guru、Unity/Flutter Guru SDK 或中台框架实现。
