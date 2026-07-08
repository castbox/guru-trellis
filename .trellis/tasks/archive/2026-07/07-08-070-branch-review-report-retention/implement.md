# #70 实施计划

## 实施顺序

1. 更新 companion script 数据合同：
   - 增加 `reviews/` raw report digest helper。
   - `record-agent-assignment --review-round` 增加 `--review-round-report`。
   - 校验 `review_rounds[]` raw report flat digest fields。
   - `review-branch` pass/findings 两条路径都要求 task-local `agent-assignment.json`，并把 raw `review_reports[]` 写入 `review-gate.json`。
   - `check-review-gate` / archive migration 支持 nested `reviews/*.md` digest。

2. 更新测试：
   - raw report 缺失时 `record-agent-assignment --review-round` fail closed。
   - `review-branch` pass 写入 `verification_evidence.review_reports[]`。
   - findings path 缺少 raw report / current round mismatch 时 fail closed。
   - archive migration 可迁移 `reviews/*.md` raw report digest。
   - metadata-only tail 接受 `reviews/*.md`。

3. 更新 workflow / README / overlay 文案：
   - canonical workflow 与 dogfood `.trellis/workflow.md`。
   - workflow README、preset README、top-level README 中 Branch Review Gate 说明。
   - continue/finish overlays和 dogfood installed copies。
   - 如涉及 preset overlays，运行 apply 同步 dogfood 并跑 drift check。

4. 检查 durable docs：
   - 对照 `docs/requirements/guru-team-trellis-flow.md` 判断是否需要同步。
   - 若不更新，必须在 Phase 2 check 和 Review Gate evidence 中说明理由。

5. 运行验证：
   - `python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis` 或可执行的等价 targeted test。
   - `python3 -m json.tool trellis/index.json`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-070-branch-review-report-retention`
   - `python3 ./.trellis/scripts/get_context.py --mode phase`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `git diff --check`

## Phase 2 check 重点

- 验证脚本仍只做 recorder / validator，没有引入 review 语义判断。
- 验证所有 changed workflow surfaces 一致。
- 验证 raw report digest 在 `agent-assignment.json`、`review-gate.json`、archive migration 中可追溯。
- 验证 #61 展示层边界未被扩大。

## Commit 边界

`trellis-continue` 阶段只提交代码、docs、workflow、overlay、测试和非 gate task planning/check evidence。最终 `review.md`、`review-gate.json`、`pr-body.md` 等 release metadata 由 finish-work 阶段处理。
