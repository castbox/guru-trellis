# 设计：强制 Branch Review Gate 产出 review.md

## 设计原则

1. **Markdown 定义流程**：Branch Review Gate 的 AI 行为、顺序和平台入口文案写在 canonical workflow、dogfood workflow、overlay skill/prompt、README 和 spec 中。
2. **脚本只做确定性校验**：Python companion 不判断 diff 是否合格，只校验 `review.md` 文件存在、可读、非空、digest 已记录，以及 passed gate 不缺必需字段。
3. **review.md 是主证据**：`review-gate.json` 是 gate recorder artifact；`review.md` 是 AI/human review 判断报告。passed gate 必须引用 review report digest。
4. **身份字段不等于报告**：`--reviewer` 仍可记录 reviewer identity，但不能作为 passed gate 的唯一 review evidence。

## 当前行为

`validate_review_gate()` 目前通过 `has_review_identity(reviewer, review_report)` 判定 reviewer 或 review report 二选一即可。workflow Phase 3.5 也写着 “when practical” 持久化 `review.md`，并给出了只传 `--reviewer` 的 pass 示例。

## 目标行为

### AI 流程

Phase 3.5 固定为：

1. AI/human review 完整 `origin/<base>...HEAD` diff。
2. 在 task worktree 下写入 `{TASK_DIR}/review.md`。
3. `review.md` 至少包含：
   - 审查范围与 diff range；
   - Reviewed HEAD；
   - summary；
   - evidence / validation；
   - findings，空 findings 也要明确写出；
   - Docs SSOT 和部署影响判断；
   - issue close/ref/followup 覆盖判断。
4. 调用 `review-branch.sh --review-report <review.md>` 写 `review-gate.json`。

### Python companion

1. 新增或收紧校验函数：
   - passed gate 必须有有效 `review_report`；
   - `review_report.path`、`sha256`、`size_bytes` 必填；
   - `size_bytes` 必须大于 0；
   - `reviewer` 不再参与 passed gate 必需证据判定，只作为可选身份字段记录。
2. `cmd_review_branch` 在 `--pass` 时：
   - 如果缺少 `--review-report`，抛出 `WorkflowError(exit_code=2)`；
   - 如果 report 文件不存在、为空、不能读，抛出 `WorkflowError(exit_code=2)`；
   - 如果传入 `--reviewer`，仍写入 `verification_evidence.reviewer`。
3. `validate_review_gate()` 在 `check-review-gate` 和 `finish-work` 路径拒绝缺少 `review_report` 的 passed gate。

### Backward Compatibility

这是有意的安全收紧：旧的 reviewer-only passed gate 会在新的 `check-review-gate.sh` / `finish-work.sh` 中失败，要求重新生成 `review.md` 并重跑 Branch Review Gate。由于 gate 是发布前证据，不应 silently grandfather。

## 修改范围

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `trellis/presets/guru-team/overlays/**/trellis-continue*`
- dogfood installed copies：`.agents/skills/trellis-continue/SKILL.md`、`.codex/prompts/trellis-continue.md`、`.codex/skills/trellis-continue/SKILL.md` 等由 preset apply 同步
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/data-contracts.md`
- `.trellis/spec/workflow/quality-guidelines.md`

## 风险与缓解

- **风险：旧 task 的 reviewer-only gate 被阻塞。**
  - 缓解：这是预期安全收紧；错误信息应明确要求先写 `review.md` 再重跑 gate。
- **风险：AI 误以为脚本会生成 review.md。**
  - 缓解：workflow/skill/prompt 明确 `review.md` 由 AI/human review 写入，脚本只 record/validate。
- **风险：多 worktree 写错 review.md。**
  - 缓解：保留并强化现有 worktree-local artifact 规则；示例使用 `{TASK_DIR}/review.md`，并提醒无 workdir 编辑工具使用绝对路径。
- **风险：平台 overlay 文案漂移。**
  - 缓解：改 canonical overlay 后运行 `apply.sh --repo .` 和 `check-dogfood-overlay-drift.sh`。

## 验证设计

1. 单元测试覆盖：
   - reviewer-only pass 被拒绝；
   - review-report pass 成功并记录 digest；
   - validate passed gate 缺 `review_report` 被拒绝；
   - report 文件为空或不存在被拒绝。
2. 脚本 dry-run：
   - 真实 task 下不带 `--review-report` 的 dry-run 失败；
   - 带 `review.md` 的 dry-run 成功。
3. 标准验证：
   - JSON 校验；
   - bash syntax；
   - py_compile；
   - task validate；
   - get_context phase reads；
   - dogfood overlay drift；
   - throwaway install；
   - git diff check。
