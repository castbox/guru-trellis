## 变更摘要

本 PR 收紧 Guru Team Branch Review Gate 的 `review-branch` 记录语义，避免 findings 路径产生只有 `--reviewer` identity、缺少独立审查来源和 task-local `review.md` 的 gate artifact。

核心行为调整：

- `review-branch` 的 pass 和 findings 记录路径都必须提供 `--review-source independent-agent`，且不能使用 main-session/self-review identity 冒充独立审查。
- `--review-report` 必须指向当前 task-local `review.md`；`--reviewer` 只保留为 reviewer identity metadata。
- `conclusion.passed=true` 只会在显式 `--pass` 且没有任何 finding 时出现；P0/P1/P2/P3 任意 finding 都会阻断 pass。
- workflow、Codex/Claude/Cursor/agents continue 入口、dogfood installed copies 和 `.trellis/spec/workflow/*` 已同步 failed findings artifact 也必须承接独立审查证据的规则。

## 影响范围

- canonical workflow：`trellis/workflows/guru-team/workflow.md`
- canonical companion script：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- regression tests：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- Guru Team preset overlays：`trellis/presets/guru-team/overlays/**/trellis-continue*`
- dogfood installed copies：`.trellis/workflow.md`、`.trellis/guru-team/scripts/python/guru_team_trellis.py`、`.agents/.codex/.claude/.cursor` continue entries
- durable specs：`.trellis/spec/workflow/companion-scripts.md`、`.trellis/spec/workflow/data-contracts.md`

本 PR 不修改 Trellis upstream、全局 npm 包或 `node_modules`。本 PR 不涉及 CI/CD workflow、Docker、Docker Compose、Kubernetes/Kustomize/Helm、数据库 migration/seed/backfill、Makefile，也不新增运行时服务或部署入口。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：114 tests OK
- `python3 -m json.tool trellis/index.json`：通过
- `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json`：通过
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`：通过
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-39-review-branch-findings-reviewer-only`：通过
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`：通过
- `git diff --check`：通过
- `check-phase2-check.sh --json`：通过
- `check-review-gate.sh --json --allow-metadata-after-gate`：通过

未执行完整 throwaway repo install / marketplace update 验证；本 PR 已覆盖 dogfood overlay apply/drift 和 installed copy 一致性，但不声称完整新仓库开箱即用门禁已覆盖。

## Review Gate

Branch Review Gate 已由独立最终放行审查代理 `019f35c6-da2d-7b71-b637-fd8a111839ef` 审查 `origin/main...HEAD` 的完整 diff，并记录在 task-local `review.md` 与 `review-gate.json`。

Gate 结论：

- `passed=true`
- `findings_count=0`
- `blocking_findings_count=0`
- 审查覆盖代码、测试、workflow、dogfood workflow、preset overlays、installed copies、spec、task artifacts、Issue Scope Ledger、Docs SSOT 和部署影响判断。

## Issue 关闭范围

Closes #39

`issue-scope-ledger.json` 仅将 #39 放入 `close_issues`。本 PR 没有关联 issue 或 follow-up issue 需要引用或关闭。

## 安全说明

本 PR 不处理 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。变更内容是本仓库内 Guru Team workflow、companion script、overlay、spec 和 task metadata；没有新增日志输出敏感信息，也没有扩大外部系统权限。
