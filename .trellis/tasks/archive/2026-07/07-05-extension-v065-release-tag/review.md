# Branch Review Gate Review

## 审查范围

- 仓库：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/extension-v065-release-tag`
- 分支：`codex/extension-v065-release-tag`
- Diff range：`origin/main...HEAD`
- Base：`dfc16d735e0ddc9ba74d3e83fdd746a8e2030e6e`
- HEAD：`1e498a01804684aa2cf7d5275c5b12c09d5755d9`
- 范围：20 files changed，647 insertions，39 deletions
- Reviewer：独立 `trellis-check` Agent `Beauvoir`
- 只读审查：未修改文件

注意：当前 worktree 有一个未提交 dirty 文件 `.trellis/guru-team/handoff.json`，不属于
`origin/main...HEAD` diff。本报告只审查已提交分支 diff；后续 stage/commit 时不要误带入
该 dirty 文件，除非主会话明确决定纳入。

## 验证命令结果

- `git diff --stat origin/main...HEAD`：通过，确认 20 个变更文件。
- `git diff --name-only origin/main...HEAD`：通过，覆盖 manifest、docs、spec、task artifacts、verify script、测试。
- `python3 -m json.tool trellis/guru-team-extension.json`：通过。
- `python3 -m json.tool .trellis/guru-team/extension.json`：通过。
- `python3 -m json.tool trellis/index.json`：通过，`version` 仍为 `1`。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile ...`：通过。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：通过，83 tests OK。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-extension-v065-release-tag`：通过。
- `./trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `git diff --check origin/main...HEAD`：通过。
- `.trellis/guru-team/scripts/bash/version.sh --json`：通过，installed version 为 `0.6.5`。
- `.trellis/guru-team/scripts/bash/check-env.sh --json`：通过，status ok，extension version 为 `0.6.5`。
- `verify-throwaway-install.sh` 默认远程 tag 验证：未运行；`gh:castbox/guru-trellis/trellis#v0.6.5` 依赖 PR merge 后创建 tag，必须 post-merge/post-tag 执行。

## Docs SSOT 结论

通过。`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、
`docs/requirements/requirement-main.md`、`.trellis/spec/workflow/data-contracts.md`、
`.trellis/spec/preset/installer.md` 已一致表达：

- stable source 使用 `gh:castbox/guru-trellis/trellis#v0.6.5` 或泛化 `#vX.Y.Z`。
- unpinned `gh:castbox/guru-trellis/trellis` 是 latest/canary。
- repo release tag 使用 `vX.Y.Z`，不使用长期 namespaced `guru-team/v0.6.5`。
- PR merge 后创建 annotated tag `v0.6.5`，验证后再退休旧 `guru-team/v0.6.5`。
- `guru-team` workflow id 不变。
- `trellis/index.json.version` 仍是 marketplace schema version `1`，未误改成 extension version。

## 需求结论

#33 的 PR 前可完成部分满足：canonical manifest 为 `0.6.5`，`tested.trellis_cli` 记录
`0.6.5`；dogfood installed manifest 为 `0.6.5`，source provenance 指向当前 dirty branch，
这符合 installed provenance 记录 apply-time source 的语义，不是 release-readiness 声明。

远程 `v0.6.5` tag 未创建，符合“PR merge 前不创建 v0.6.5”的要求。当前远端仍只有旧
`guru-team/v0.6.5` tag，未提前退休，符合“新 tag 验证后再退休”的要求。

## Issue 关闭范围

通过。`issue-scope-ledger.json` 中：

- `close_issues: []`
- `related_issues` 包含 #33
- 明确要求 PR body 使用 `Refs #33`，不能使用 `Closes #33`

结论：本 PR 不应关闭 #33，因为 tag 创建、tag-pinned throwaway install / workflow 验证、旧
tag 退休都必须 post-merge/post-tag 执行。

## 部署影响

通过。本 diff 是 Trellis extension manifest、文档、spec、脚本验证默认值、测试和 task
artifacts 变更；本 repo 无 app runtime。未发现需要同步 CI/CD、Docker、K8s/Kustomize/Helm、
DB migration、Makefile 或运行时部署资产的变更。

## 安全结论

通过。对分支变更文件执行敏感信息搜索，未发现 token、secret、private key、signed URL、
`.env` 内容、数据库 URL 或客户敏感数据。命中的 `.env`、token、secret 仅为文档/spec 中的
安全检查说明。

## Findings

- P0：无
- P1：无
- P2：无
- P3：无

## Branch Review Gate

结论：可通过 Branch Review Gate。

前提说明：本 gate 覆盖 `origin/main...HEAD` 的已提交 diff。当前未提交的
`.trellis/guru-team/handoff.json` 不在本次 diff 范围内，后续主会话记录 gate 或发布前应避免
误提交未审查 dirty 文件。
