# #39 收紧 review-branch findings 示例和脚本语义，避免 reviewer-only gate artifact

## Goal

收紧 Guru Team Branch Review Gate 的 recorder 语义，避免 findings 路径产生“只有 reviewer identity、缺少独立审查来源和 task-local review report”的 gate artifact。所有 Branch Review Gate 记录路径都必须明确承接已经发生的独立审查；脚本只负责记录和校验，不替代 reviewer 判断。

## Requirements

- canonical workflow `trellis/workflows/guru-team/workflow.md` 与 dogfood copy `.trellis/workflow.md` 中 pass path 和 findings path 的 `review-branch.sh` 示例都必须包含：
  - `--review-source independent-agent`
  - `--review-report ".trellis/tasks/<task>/review.md"`
  - task-local `--agent-assignment` 在 pass path 继续保留；findings path 继续允许记录 agent assignment digest。
- `trellis-continue` 相关平台入口必须同步语义：review 有 findings 时也必须携带独立审查来源和 task-local `review.md`，`--reviewer` 只是 identity metadata。
- 脚本层必须保证：
  - `passed=true` 只会在显式 `--pass` 且没有任何 finding 时出现；任何 `P0/P1/P2/P3` finding 都阻断 pass。
  - 非 pass findings artifact 清晰记录 `passed=false`。
  - findings 路径缺少 `--review-source independent-agent` 或缺少 task-local `review.md` 时 fail closed。
  - pass 和 findings 两类路径都不能把 main-session/self-review identity 当成独立审查证据。
- 回归测试覆盖 pass path、blocking finding path、missing review_source、missing review_report、non-pass artifact conclusion；其中 blocking finding path 使用 `P3` 验证用户修正后的“P0/P1/P2/P3 全阻断”语义。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`；长期源头在本仓库 canonical workflow / preset / overlay / companion scripts。

## Acceptance Criteria

- [ ] `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 中 findings 示例包含 `--review-source independent-agent` 与 `--review-report ".trellis/tasks/<task>/review.md"`。
- [ ] `trellis/presets/guru-team/overlays/` 中 `trellis-continue` 相关入口，以及 dogfood installed copies `.agents/skills/`、`.codex/prompts/`、`.codex/skills/`、`.claude/commands/`、`.cursor/commands/` 同步“findings path 也要独立来源 + review.md”的语义。
- [ ] `review-branch.sh` / `guru_team_trellis.py` 在未显式 `--pass` 时不会生成 `passed=true`。
- [ ] findings 路径缺少 `--review-source independent-agent` 或缺少 task-local `review.md` 会阻断。
- [ ] `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，且新增/更新测试覆盖上述路径。
- [ ] overlay 修改后运行 preset apply 同步 dogfood 副本，并通过 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
- [ ] 基础校验通过：`python3 -m json.tool trellis/index.json`、`bash -n ...`、`python3 -m py_compile ...`、`python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-39-review-branch-findings-reviewer-only`、`git diff --check`。
- [ ] 如未完成干净 throwaway install / marketplace update 验证，最终说明中明确未覆盖项和风险。

## Notes

- 用户对 issue 原文的修正：不再使用“没有 P0/P1/P2 blockers”作为 pass 条件；应为“没有任何 finding，包括 P0/P1/P2/P3”。
- 官方 Trellis 文档约束：workflow 行为通过 Markdown workflow/entrypoints 承载；脚本只做确定性 recorder / validator。本任务不改官方 Trellis 上游。
- Docs SSOT：本仓库 durable docs 包括 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` 和 workflow/preset specs。本任务先修改 workflow/overlay/script/test；如 README 已保持正确语义则不强制扩写，只在 review 中记录核对结果。
- Middle-platform Knowledge Gate：不适用。本任务不触及 go-guru/proto-guru/Flutter/Unity 等 Guru Team middle-platform SDK。
