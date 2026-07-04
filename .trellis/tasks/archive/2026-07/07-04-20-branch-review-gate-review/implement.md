# 实施计划：强制 Branch Review Gate 产出 review.md

## 阶段 1：定位现有合同

- [x] 搜索 `review.md`、`--review-report`、`--reviewer`、`Branch Review Gate` 的所有引用。
- [x] 确认 canonical workflow、dogfood workflow、overlay skill/prompt、README、spec、Python companion 和测试的当前语义。

## 阶段 2：收紧脚本合同

- [x] 修改 `guru_team_trellis.py`：
  - [x] passed gate 必须提供有效 `--review-report`；
  - [x] `validate_review_gate()` 拒绝缺少 `review_report` 的 passed gate；
  - [x] 错误信息明确 `review.md` 是必需审查报告；
  - [x] 保留 `--reviewer` 身份记录。
- [x] 更新 `test_guru_team_trellis.py`：
  - [x] reviewer-only pass 失败；
  - [x] review-report pass 成功；
  - [x] 旧 reviewer-only gate validation 失败。

## 阶段 3：同步 AI-facing 流程合同

- [x] 修改 canonical `trellis/workflows/guru-team/workflow.md`。
- [x] 同步 `.trellis/workflow.md`。
- [x] 修改 preset overlay 的 `trellis-continue` skill/prompt/command 文案。
- [x] 运行 preset apply 同步 dogfood installed copies。

## 阶段 4：同步 docs/spec

- [x] 更新 `README.md`。
- [x] 更新 `trellis/workflows/guru-team/README.md`。
- [x] 更新 `trellis/presets/guru-team/README.md`。
- [x] 更新 `.trellis/spec/workflow/workflow-contract.md`。
- [x] 更新 `.trellis/spec/workflow/data-contracts.md`。
- [x] 更新 `.trellis/spec/workflow/quality-guidelines.md`。
- [x] 更新 `issue-scope-ledger.json` acceptance evidence。

## 阶段 5：验证

- [x] `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- [x] `python3 -m json.tool trellis/index.json`
- [x] `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`
- [x] `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- [x] `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- [x] `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-20-branch-review-gate-review`
- [x] `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- [x] reviewer-only dry-run fail-closed
- [x] review-report dry-run success
- [x] `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
- [x] `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- [x] `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- [x] `git diff --check`

## 阶段 6：提交与 Branch Review Gate

- [ ] 提交 issue #20 范围文件。
- [ ] 在 task worktree 下写入 `.trellis/tasks/07-04-20-branch-review-gate-review/review.md`。
- [ ] 用 `review-branch.sh --review-report ...` 写 `review-gate.json`。
- [ ] `check-review-gate.sh --json` 通过。

## 回滚

如果新合同阻塞合理的 finish-work 路径，回滚 Python companion 与 workflow/overlay/spec/docs 到 reviewer-or-report 语义，并保留 task artifact 说明本次收紧失败原因。
