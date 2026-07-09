# #92 Branch Review 汇总

## 审查轮次

| 轮次 | 角色 | Agent | Reviewed HEAD | findings | 原始报告 |
|---|---|---|---|---:|---|
| 1 | 最终放行审查代理 | `019f48dc-2e18-7db1-b50a-d794018502b1` | `1b42776abbc037d152fb350528c96b6e93ccbef2` | 1 | [round-001-final-release.md](reviews/round-001-final-release.md) |
| 2 | 问题闭环审查代理 | `019f48dc-2e18-7db1-b50a-d794018502b1` | `73a4985d07e4d2876c39a8ff53130cbdb1eb119e` | 0 | [round-002-closure.md](reviews/round-002-closure.md) |
| 3 | 最终放行审查代理 | `019f48fc-06cd-7983-8577-f8e1040dacff` | `73a4985d07e4d2876c39a8ff53130cbdb1eb119e` | 0 | [round-003-final-release.md](reviews/round-003-final-release.md) |

## 问题生命周期

- Round 001 在 `1b42776abbc037d152fb350528c96b6e93ccbef2` 发现 1 个 P2：`validate_commit_subject()` 未禁止 `Closes/Fixes/Resolves/Close/Fix/Resolve #xx` 出现在 commit subject，导致 commit message 与 PR body 的 issue close 语义分工不完整。
- 修复提交 `73a4985d07e4d2876c39a8ff53130cbdb1eb119e` 在 canonical/dogfood Python helper 中禁止 subject close keywords，并补充 work/merge subject 回归测试，且同步 workflow、README、preset README、spec 合同。
- Round 002 由 Round 001 finding owner 作为 `问题闭环审查代理` 复核该 P2，结论 `findings_count: 0`；`agent-assignment.json` 记录 `reuse-for-closure` 决策：`from_round=1`、`to_round=2`。
- Round 003 使用全新最终放行审查代理，覆盖最新 `origin/main...HEAD` 完整 diff，结论 `findings_count: 0`。

## 最终审查

最终 reviewed HEAD：`73a4985d07e4d2876c39a8ff53130cbdb1eb119e`

Diff 范围：`origin/main...HEAD`

最终结论：通过。Round 003 为全新最终放行审查，未发现 P0/P1/P2/P3 finding，可作为 Branch Review Gate 通过证据。

## 证据

- `check-workspace-boundary.sh --json --task .trellis/tasks/07-10-092-conventional-commits`：通过；当前 worktree 与 handoff workspace 一致，source checkout clean，当前工作区只剩 `.trellis/guru-team/handoff.json` 与 task metadata。
- `check-commit-messages.sh --task .trellis/tasks/07-10-092-conventional-commits --json`：通过；两个 work commit 均符合 #92 Conventional Commits 合同。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：通过，243 tests。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-10-092-conventional-commits`：通过。
- `git diff --check`：通过。
- `format-merge-commit.sh --task .trellis/tasks/07-10-092-conventional-commits --pull-request 91 --summary '中文 Conventional Commits 提交规范' --head-branch codex/092-conventional-commits --base-branch main --json`：通过，生成合规 `chore(merge)` payload。
- `python3 -m json.tool trellis/index.json`：通过。
- Phase 2 post-commit audit：`phase2-check.json.head` 为 `1b42776...`，是当前 HEAD `73a4985...` 的祖先；之后提交的非 metadata 路径均已由 `phase2-check.json.dirty_paths` 覆盖。

## 观察项

- 当前分支 marketplace install 在分支未 push/tag 前无法完成真实 `gh:` source 复验；task 与 Phase 2 证据已如实记录该限制。
- public marketplace sample / throwaway install 路径已覆盖新增 helper、manifest public API、preset installer 与 workflow preview/switch 行为。
- 当前工作区剩余 dirty paths 为 Trellis metadata，属于 finish-work/archive/journal/publish 阶段处理范围。

## 后续候选

- 分支 push 或 release tag 可解析后，使用 `TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#<ref>` 复验当前分支或 tag marketplace install。

## Docs SSOT

Docs SSOT strategy：`ssot_first`。

durable workflow、dogfood workflow、workflow README、preset README、top-level README、`.trellis/spec/workflow/{workflow-contract,data-contracts,quality-guidelines}.md` 已承接 issue #92 的 subject/body/metadata/merge/publish 合同。task artifacts 仅保留规划、Phase 2、review lifecycle 和未覆盖验证限制等过程证据。最终审查未发现 current-scope Docs SSOT inconsistency。

## 部署与安全影响

本分支修改 workflow/docs/spec、Python/bash companion scripts、preset installer、manifest、tests 和 dogfood installed copy。未涉及 CI/CD、Docker/K8s、DB migration、Makefile、runtime config 或 config template。未发现 `.new` / `.bak` 遗留；未发现 token、secret、private key、`.env`、数据库 URL、signed URL 或敏感原始数据风险。

## 结论

Branch Review 通过。Round 001 P2 已由 Round 002 闭合，Round 003 最终放行审查使用全新 agent 覆盖最新 HEAD，`findings_count: 0`。可以记录通过型 Branch Review Gate。
