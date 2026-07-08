## 变更摘要

- Guru Team workflow 新增显式 post-planning review gate：`prd.md`、`design.md`、`implement.md` 三份规划文档生成后，主会话必须向用户展示三个 task-local 链接，并在用户明确确认后才允许进入实现。
- `planning-approval.json` 升级为 `schema_version=1.1`，强制 `user_confirmation.source=explicit-post-planning-review`，记录三份规划文档的 digest/size/mtime、approval HEAD 和 dirty paths。
- `check-planning-approval` 会拒绝 Phase 0 handoff / generic workflow confirmation、旧 schema、缺少三文档、digest/mtime 漂移、HEAD 漂移，以及 dirty paths freshness 不匹配。
- Codex / Claude / Cursor / shared `.agents` overlay、channel runtime agent、durable docs 和 `.trellis/spec` 已同步三文档显式审核门禁，避免 fresh install 或 dogfood copy 继续看到旧的 PRD-only / optional planning 提示。

## 影响范围

影响 Guru Team workflow marketplace、preset overlays、dogfood installed copies、companion scripts、tests、durable requirement docs 和 `.trellis/spec` 规范。主要文件包括：

- `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 与 `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- Codex / Claude / Cursor / shared `.agents` overlay 与 channel runtime agent 文案
- `trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `docs/requirements/guru-team-trellis-flow.md`、`docs/requirements/requirement-main.md` 与 `.trellis/spec/**`

本 PR 不修改官方 Trellis npm 包、`node_modules`、全局安装目录或 Trellis upstream 源码。

## 验证结果

- `PYTHONDONTWRITEBYTECODE=1 python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：146 tests OK
- `PYTHONDONTWRITEBYTECODE=1 python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：27 tests OK
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：OK
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`：OK
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms --json`：OK，dogfood installed copy 已同步，无 `.new` / `.bak` 遗留
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh --repo .`：OK
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-052-explicit-planning-review`：OK
- `git diff --check`：OK

完整 public throwaway install 仍需在本分支 push、合并并发布新 release tag 后重跑。当前 public tag `v0.6.5-guru.1` 不包含本 PR，本地分支在发布前也不是可用的 public marketplace ref，因此本 PR 不声称 public marketplace fresh install 已通过。

## Review Gate

Branch Review Gate 已在 `16c240ba890e6997f7ea131ecaa528db84607705` 通过。审查覆盖 `origin/main...HEAD` 完整 diff、workflow / overlay / scripts / tests / docs / specs / task artifacts / deployment impact。

审查流程中发现的 round 1、3、5、7 findings 均已由同一 finding owner 完成 closure review；最终 fresh reviewer `019f3e85-f072-7400-b620-79d6b408a357` 返回 `findings_count=0`。`review-gate.json` 记录了 task-local `review.md` 与 `agent-assignment.json` digest evidence。

## Issue 关闭范围

Closes #52。

Refs #72。#72 仅作为 #52 issue body 中的复现背景和历史 artifact 证据引用，本 PR 不关闭 #72。

## 安全说明

本 PR 不涉及 secret、token、private key、`.env`、数据库 URL、signed URL 或客户数据。变更未引入外部服务调用、运行时 credential、数据库 migration、容器/K8s/Compose/Helm/Makefile 或 CI/CD 行为调整。脚本新增逻辑仅校验本地 artifact source、digest、HEAD 和 dirty-state freshness，不把 AI/user 对规划内容充分性的判断写进 Python 或 shell。
