# Branch Review Gate Review

## 审查范围

- Review source: independent agent `trellis-check-agent`
- Diff range: `origin/main...HEAD`
- Reviewed commit: `59832b1 feat(preset): filter platform overlays`
- Task: `.trellis/tasks/07-04-11-let-preset-installer-apply-only`

## 结论

无 P0/P1/P2/P3 findings。实现满足 issue #11 的验收范围，可以记录 Branch Review Gate。

## 审查覆盖

- 已审查 `README.md`、`trellis/presets/guru-team/README.md`、preset installer Python、installer 单测、throwaway 验证脚本、preset spec、Trellis task artifacts 和 handoff。
- 平台过滤合同符合规划：共享 `.agents/` 始终安装；默认安装 `.codex/` + `.cursor/`；默认不会创建 `.claude/`；`--all-platforms` 会安装 `.claude/`；`--platform` 与 `--all-platforms` 互斥由 argparse 阻塞。
- Docs SSOT reconciliation：本仓库无 `docs/`；长期公开文档为 `README.md` 与 `trellis/presets/guru-team/README.md`，本次已同步命令和平台语义。
- 部署影响：仅改本地 preset installer、公开文档、测试和 task evidence；不涉及 CI/CD、容器、K8s、DB、Makefile 或运行服务。
- 安全检查：未发现 token、私钥、`.env`、签名 URL 或本机-only 文件；无 `.new` / `.bak` / untracked 产物遗留。
- 官方扩展边界：对照 Trellis custom workflow 文档，未发现通过脚本实现 AI 判断流程分叉；本次脚本改动属于确定性 preset installer 行为。

## 验证结果

- `git diff --check origin/main...HEAD`：通过。
- `bash -n trellis/presets/guru-team/scripts/bash/apply.sh trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：通过。
- `python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：12 tests OK。
- `python3 -m json.tool trellis/index.json`：通过。
- `python3 -m json.tool .trellis/tasks/07-04-11-let-preset-installer-apply-only/phase2-check.json`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-11-let-preset-installer-apply-only`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- 临时 repo 行为抽样：默认 apply 安装 `.agents/.codex/.cursor` 且不创建 `.claude`；`--all-platforms` 创建 `.claude`。

## 已处理问题

- 独立 review 初始发现 `phase2-check.json` 的 `head` 仍为提交前 base HEAD，且 `checked_specs` 为空；已修正为当前 commit `59832b1d19b232a5dc5cffd59dba70294aa81238`，并补充相关 spec digest 与 `git diff --check origin/main...HEAD` 证据。
