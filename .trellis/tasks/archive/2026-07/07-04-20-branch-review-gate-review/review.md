# Branch Review Gate 审查报告

## 审查范围

- Task：`.trellis/tasks/07-04-20-branch-review-gate-review`
- Issue：#20 强制 Branch Review Gate 每次产出 review
- Diff range：`origin/main...HEAD`
- Reviewed HEAD：`6277464`
- 审查者：`codex-main-session`

本次审查覆盖完整分支 diff，包括 canonical workflow、dogfood workflow、Guru Team companion Python、单元测试、preset overlays、dogfood installed copies、README、workflow specs、Trellis task artifacts、Issue Scope Ledger、throwaway install 验证和 Branch Review Gate dry-run 证据。当前 HEAD `6277464` 相比工作提交 `3ada1c4` 只新增 review/gate metadata commit 和 task archive metadata commit，本次恢复 gate 用于让 finish-work 的严格 HEAD 校验匹配当前已归档 HEAD。

## 结论

Branch Review Gate 通过：本分支将 `review.md` 从可选 artifact 收紧为 passed gate 的必需 review report，`review-gate.json` 必须引用其 digest；未发现 P0/P1/P2/P3 finding。

## 关键审查证据

- Python companion 已从 reviewer-or-report 二选一改为 passed gate 必须有有效 `review_report`，`--reviewer` 只保留身份记录。
- `validate_review_gate()` 会拒绝缺少 `review_report.path`、`sha256` 或 `size_bytes` 的 passed gate；`finish-work` 和 `publish-pr` 复用该校验路径。
- `cmd_review_branch()` 在 `--pass` 且缺少 task-local `--review-report` 时返回 exit 2，错误明确说明 reviewer 不能替代 review report。
- 单元测试新增 reviewer-only pass 失败、review-report pass 成功、旧 reviewer-only gate validation 失败三类覆盖。
- Canonical workflow、dogfood workflow、continue/finish overlays、README 和 workflow specs 已同步 `review.md` 必产物语义。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 已同步 dogfood installed copies，`check-dogfood-overlay-drift.sh` 通过。

## 验证结果

- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：通过，9 tests OK。
- `python3 -m json.tool trellis/index.json`：通过。
- `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-20-branch-review-gate-review`：通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`：通过，输出已包含 `review.md` 必产物和 `--review-report` 规则。
- reviewer-only dry-run：按预期 exit 2，错误为必须提供 `--review-report`。
- review-report dry-run：通过，记录 `.trellis/tasks/07-04-20-branch-review-gate-review/review-dry-run.md` 的 64 位 sha256 与 `size_bytes`。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：通过。
- `git diff --check origin/main...HEAD`：通过。

## Docs SSOT

本仓库没有独立 `docs/` durable docs 目录。本次长期规则已同步到 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、canonical workflow、dogfood workflow、overlay skill/prompt/commands 和 `.trellis/spec/workflow/*`。Task artifact 仅保留 issue #20 的执行证据。

## 部署影响

本次仅修改 Trellis workflow/preset/overlay/companion scripts/docs/task artifacts，不新增或变更 API service、CLI runtime entrypoint、background worker、scheduled job、queue consumer、runtime config、CI/CD workflow、Dockerfile、Docker Compose、Kubernetes/Kustomize、database migration、Makefile 或生产部署资产。无需部署资产更新。

## Issue 关闭范围

- `close_issues`：#20。Issue Scope Ledger 已记录验收证据，Branch Review Gate 覆盖本 issue。
- `related_issues`：无。
- `followup_issues`：无。

## Findings

无 P0/P1/P2/P3 finding。
