# Branch Review Gate 审查报告

## 审查范围

- Task：`.trellis/tasks/archive/2026-07/07-04-20-branch-review-gate-review`
- Issue：#20 强制 Branch Review Gate 每次产出 review，并修复 metadata 提交边界
- Diff range：`origin/main...HEAD`
- Reviewed HEAD：`afe1afb`
- 审查者：`codex-main-session`

本次审查覆盖完整分支 diff，包括 canonical workflow、dogfood workflow、Guru Team companion Python、单元测试、preset overlays、dogfood installed copies、README、workflow specs、Trellis task artifacts、Issue Scope Ledger、throwaway install 验证、Branch Review Gate dry-run 证据，以及本次 follow-up 对 metadata-only tail 的处理。

## 结论

Branch Review Gate 通过：本分支已强制 passed gate 引用 task-local `review.md`，并进一步明确 `trellis-continue` 只产出 review/gate metadata、不提交不发布；`finish-work` 是剩余 Trellis metadata commit 与 publish 的唯一正常入口。未发现 P0/P1/P2/P3 finding。

## 关键审查证据

- Python companion 已要求 `review-branch --pass` 必须提供 task-local `--review-report`，`validate_review_gate()` 拒绝缺少 `review_report` digest 的 passed gate。
- `cmd_finish_work()` 入口改为 `validate_review_gate(..., allow_metadata_after_gate=True)`，与 publish 路径一致，只接受 reviewed HEAD 后的 Trellis metadata-only tail。
- 单元测试新增并通过：reviewer-only pass 失败、review-report pass 成功、旧 reviewer-only gate validation 失败、metadata-only tail 可通过、非 metadata tail 会阻塞、finish-work 入口使用 `allow_metadata_after_gate=True`。
- Canonical workflow、dogfood workflow、continue/finish overlays、README 和 workflow specs 已同步：`trellis-continue` 写完 `review.md` / `review-gate.json` 后停止，不 stage/commit/push/PR；`finish-work` 负责 archive、journal、remaining metadata commit 与 publish。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .` 已同步 dogfood installed copies，`check-dogfood-overlay-drift.sh` 通过，没有遗留 `.new` 或 `.bak`。

## 验证结果

- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：通过，12 tests OK。
- `python3 -m json.tool trellis/index.json`：通过。
- `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`：通过，输出包含 continue 停止、不提交 gate metadata 的规则。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.6`：通过，输出包含 `--allow-metadata-after-gate` 和 finish-work metadata ownership。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：通过。
- `python3 -m json.tool .trellis/tasks/archive/2026-07/07-04-20-branch-review-gate-review/issue-scope-ledger.json`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/archive/2026-07/07-04-20-branch-review-gate-review`：通过。
- `git diff --check`：通过。

## Docs SSOT

本仓库没有独立 `docs/` durable docs 目录。本次长期规则已同步到 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、canonical workflow、dogfood workflow、overlay skill/prompt/commands 和 `.trellis/spec/workflow/*`。Task artifact 仅保留 issue #20 的执行与审查证据。

## 部署影响

本次仅修改 Trellis workflow/preset/overlay/companion scripts/docs/task artifacts，不新增或变更 API service、CLI runtime entrypoint、background worker、scheduled job、queue consumer、runtime config、CI/CD workflow、Dockerfile、Docker Compose、Kubernetes/Kustomize、database migration、Makefile 或生产部署资产。无需部署资产更新。

## Issue 关闭范围

- `close_issues`：#20。Issue Scope Ledger 已记录 review report 强制产物和 metadata 提交边界两部分验收证据，Branch Review Gate 覆盖本 issue。
- `related_issues`：无。
- `followup_issues`：无。

## Findings

无 P0/P1/P2/P3 finding。
