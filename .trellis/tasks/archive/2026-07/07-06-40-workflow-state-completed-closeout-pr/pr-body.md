## 变更摘要

- 扩展 `trellis/workflows/guru-team/workflow.md` 中的 `[workflow-state:completed]` closeout breadcrumb，使它覆盖 Branch Review Gate stale fallback、PR body/readiness、finish-work dry-run、metadata tail 以及禁止直接 `publish-pr` 的规则。
- 同步 dogfood 运行副本 `.trellis/workflow.md`，保证当前仓库运行时读取到的 completed breadcrumb 与 canonical workflow 一致。
- 为 `.codex/hooks/test_inject_workflow_state.py` 增加 completed breadcrumb 回归测试，验证 hook parser 会从 workflow Markdown 注入新的 closeout 关键文案。

## 影响范围

- 影响 Guru Team workflow 的 completed/fallback closeout 提示语义，不修改 Trellis 上游源码、全局 npm 包、`node_modules`、preset installer、marketplace index 或安装命令。
- 正常发布路径仍是 Branch Review Gate 通过后显式执行 `trellis-finish-work`；`[workflow-state:completed]` 仅作为 fallback/legacy breadcrumb，避免旧入口继续遗漏 PR body、dry-run 和 metadata tail 要求。
- 本次 diff 未修改 CI/CD、Docker、Compose、Kubernetes、数据库 migration、Makefile、runtime config 或部署脚本，不需要部署资产同步。

## 验证结果

- `python3 .codex/hooks/test_inject_workflow_state.py`：通过，7 tests。
- `python3 ./.trellis/scripts/get_context.py --mode phase`：通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`：通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.6`：通过。
- `python3 -m json.tool trellis/index.json`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .codex/hooks/inject-workflow-state.py .codex/hooks/test_inject_workflow_state.py`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-40-workflow-state-completed-closeout-pr`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `git diff --check`：通过。
- current-branch throwaway install 未完整验证：Trellis 0.6.5 不接受本地路径作为 `--workflow-source`，且审查时远端尚无该 slash branch 可采样。本 PR 未改 marketplace index、preset、installer 或安装命令；推送分支或合并后应补跑 marketplace smoke test，确认新安装可读取本次 completed breadcrumb。

## Review Gate

- Branch Review Gate 已由独立最终放行审查代理执行，reviewer `019f35ed-86fc-7a02-95cf-e6b268ef5aae`，reviewed HEAD `fb4a7b0275cbab3ca9f243c8cf2f850a9857c642`。
- 审查范围覆盖 `origin/main...HEAD` 的 workflow Markdown、dogfood workflow、hook 测试、task artifacts、相关 spec/README/overlay 文案和 changed-file list。
- 结论：0 个 P0/P1/P2/P3 finding，允许仅追加 Trellis metadata tail 后进入 finish-work。

## Issue 关闭范围

Closes #40

- #40 的验收点已覆盖：canonical workflow 与 dogfood workflow 的 completed breadcrumb 同步；breadcrumb 明确 gate stale/reviewer-only fallback、task-local PR body/readiness、先 dry-run 再正式 finish-work、禁止直接 `publish-pr`；hook 回归测试覆盖关键 closeout 文案。
- 无 related issue 或 follow-up issue 需要随本 PR 关闭。

## 安全说明

- 本次变更只包含公开 workflow 文案、hook 测试和 Trellis task metadata。
- 未新增或修改 token、secret、private key、`.env`、数据库 URL、客户数据或签名 URL。
