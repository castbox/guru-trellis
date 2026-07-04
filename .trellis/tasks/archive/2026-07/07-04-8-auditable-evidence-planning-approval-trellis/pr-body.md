## 变更摘要

- 为 Guru Team workflow 增加 `planning-approval.json` 和 `phase2-check.json` 两个可审计 gate artifact，明确 `task.py start` 只是状态写入，验证命令只是 `trellis-check` 证据的一部分。
- 强化 Branch Review Gate：通过状态必须来自独立 Agent review，`review-branch --pass` 要求 `--review-source independent-agent`、非 main-session reviewer、task-local `review.md` digest，并拒绝 `prd.md` 等其他 artifact 冒充 review report。
- 修复 worktree preflight：`prepare-task --create-worktree` / `--create-task` 在创建 worktree 或 task 前刷新并校验 base branch freshness，handoff 记录 local/remote HEAD、fetch 和 fast-forward evidence。
- 更新 Guru Team workflow、platform overlays、README、spec、preset installer 与 dogfood copy，并补充 focused 单元测试覆盖 gate 缺失、stale、通过路径和 base freshness 关键分支。

## 影响范围

- 影响 Guru Team marketplace workflow、preset installer、overlay 入口、dogfood `.trellis/guru-team` helper、Trellis task evidence 和项目规范文档。
- 对使用 Guru Team preset 的项目，进入实现、提交前检查、Branch Review Gate 和 finish/publish 前置校验会更严格；缺少或过期的 planning/check/review evidence 会 fail closed。
- 未修改 Trellis 官方 CLI 源码、全局 npm 包或 `node_modules`。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：57 tests OK。
- `python3 -m json.tool trellis/index.json` 与 handoff schema / gate artifact JSON 校验通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh` 通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py` 通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-8-auditable-evidence-planning-approval-trellis` 通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过。
- `git diff --check` 通过。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 在 feature branch 上按预期 fail-closed，防止把公开 `main` marketplace 样本误当当前分支验证。

## Review Gate

- 独立 reviewer：`independent-review-agent`。
- Review source：`independent-agent`。
- 审查范围：`origin/main...HEAD`，reviewed HEAD `fbf0dc49f33cc104243e95772e623b634ec10eda`。
- 第三次独立复审未发现 P0/P1/P2/P3 finding。
- 复审确认上一轮 P1 已修复：`phase2-check.json` 的 post-commit audit 会检查 recorded HEAD 到当前 HEAD 的 committed tail，只允许 Trellis metadata；非 metadata committed tail 会阻塞 Branch Review Gate。

## Issue 关闭范围

Closes #8

本 PR 仅关闭 issue #8。没有 related 或 follow-up issue 会被关闭。

## 安全说明

- 本次变更不涉及 token、secret、private key、`.env`、数据库 URL、签名 URL 或客户数据。
- 未修改 CI/CD workflow、Dockerfile、Docker Compose、Kubernetes/Kustomize、数据库 migration、seed/backfill 或 Makefile。
- 完整 current-branch marketplace throwaway install 仍受当前 Trellis CLI `gh:` source 不支持 branch ref 的限制；脚本已 fail-closed，避免把公开远端样本误报为当前分支开箱验证。
