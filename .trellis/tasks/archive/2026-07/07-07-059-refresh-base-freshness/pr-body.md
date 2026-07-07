## 变更摘要

- 修复 `prepare-task` 在 planner-only 阶段使用过期 `origin/<base>` 判断 base freshness 的问题。
- planner 阶段现在会先执行 `git fetch origin <base>` 刷新远端 base 引用，再输出 `preflight.base_freshness` 结论。
- planner-only 路径只做远端刷新和状态报告，不 fast-forward 本地 base，不写 handoff，不创建 worktree/task。
- executor 路径继续在真正创建 task/worktree 前独立调用强刷新逻辑，避免 planner 结果被当作执行阶段的 freshness 保证。

## 影响范围

- 更新 canonical Guru Team workflow companion script：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
- 同步 dogfood 安装副本：`.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- 扩展 `intake-handoff.schema.json` 的 base freshness 证据字段，覆盖 canonical 与 dogfood schema。
- 更新 workflow、workflow README、preset README，明确 planner-only refresh 行为和 executor 仍需重刷的边界。
- 更新 `.trellis/spec/workflow/data-contracts.md`，把 planner-only freshness 刷新合同固化到 Docs SSOT。
- 新增/更新单元测试，覆盖 planner-only stale、diverged、fetch_failed 以及 executor 分离语义。

## 验证结果

- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，127 tests OK。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` 通过，18 tests OK。
- `python3 -m py_compile` 覆盖本次 Python 脚本。
- `python3 -m json.tool` 覆盖本次 JSON/schema artifact。
- `bash -n` 覆盖本次相关 shell 脚本。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-059-refresh-base-freshness` 通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过，无 `.new` / `.bak` 漂移残留。
- `git diff --check` 通过。
- dogfood `prepare-task` planner-only smoke 验证输出包含 `fetch_attempted=true`、`fetch_performed=true`、`fast_forwarded=false`、`remote_head_source=fetched`、`handoff_written=false`、`workspace_ready=false`。

远端 marketplace 全链路安装未在本 PR 发布前完整验证：未跑 `trellis init --workflow-source gh:castbox/guru-trellis/trellis` 和 `trellis workflow --marketplace gh:castbox/guru-trellis/trellis` 的远端安装链路。本次覆盖的是本地 dogfood apply、managed asset 同步、overlay drift、以及 Phase 2 temp preset install 证据。

## Review Gate

Branch Review Gate 已由独立最终放行审查代理 `019f3bb9-e1ce-7e32-8de5-68ab9b059e74` 审查 `origin/main...HEAD`，reviewed HEAD 为 `548a24f8e9709b1a720088ae053e8c80d6b8cf98`，结论通过，0 findings。

gate 证据覆盖代码、测试、workflow/docs/schema、Trellis artifacts、配置、脚本、preset installer、CI/CD、Docker、K8s、数据库 migration、Makefile 影响面；结论记录在 task-local `review.md` 与 `review-gate.json`。

## Issue 关闭范围

Closes #59

#62 是本任务执行过程中暴露的 subagent timeout/终止策略 follow-up，仅登记为后续问题，不在本 PR 关闭范围内。

## 安全说明

本 PR 未引入 `.env`、token、secret、private key、签名 URL、数据库 URL 或敏感原始记录。未修改 CI/CD、Docker、K8s/Kustomize/Helm、数据库 migration、seed/backfill、Makefile 或部署资产，因此无额外部署步骤。
