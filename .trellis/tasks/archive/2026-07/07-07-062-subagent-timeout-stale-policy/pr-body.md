## 变更摘要

- 为 Guru Team workflow 增加 sub-agent wait timeout / stale / unfinished termination 合同：`wait_agent`、`trellis channel wait` 或等价等待命令 timeout 只表示等待窗口结束，不代表 agent 失败、卡死或可以采用半成品输出。
- 在 `agent-assignment.json` 中增加 additive `status_events[]` ledger，记录 wait timeout、progress observed、stale assessed、continue waiting、resume/replacement、terminated unfinished、completed、failed 等 AI/human 已做出的状态处理结论。
- 更新 Branch Review Gate 校验：若存在未闭环的 `terminated-unfinished`，必须先有 same-agent resume 或 replacement-started，并最终到达 `completed` 或明确 `failed`，否则 pass 路径 fail closed。
- 同步 Guru Team workflow、trellis-continue、Codex/Claude/Cursor/channel agent overlay、dogfood installed copies、README、requirements docs 和 `.trellis/spec/**`，让实现代理、阶段二检查代理和 review 代理都遵守同一策略。

## 影响范围

本次影响 Guru Team Trellis 扩展的 workflow 行为、companion script recorder/validator、preset overlay、dogfood 安装副本和公共/持久文档。变更保持在本仓库支持的扩展面内，没有修改 Trellis 官方 npm 包、`node_modules` 或上游源码。

`status_events[]` 是向后兼容的 additive 字段；旧 `agent-assignment.json` 缺少该字段时 loader 会补空数组。脚本只校验客观字段和恢复链完整性，不判断 agent 是否 stale、是否应该终止或是否应该替换。

## 验证结果

- `python3 -m json.tool trellis/index.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py .trellis/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`，136 tests passed
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-062-subagent-timeout-stale-policy`
- `python3 ./.trellis/scripts/get_context.py --mode phase` 以及 `--step 2.1`、`--step 2.2`、`--step 3.5`
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json --dry-run --status-event wait-timeout --decision continue-waiting`
- `git diff --check`

未执行完整 throwaway install、`trellis init`、`trellis workflow --marketplace` 或 upgrade/update 实跑；本 PR 不声称完成开箱即用全量验证。已覆盖 canonical/dogfood 同步、drift check、phase context 和当前仓库验证。

## Review Gate

Branch Review Gate 已由独立最终放行审查代理审查 `origin/main...413713cc8cf0ce4f04377e00609d0e6801b3b856` 完整 diff，结论 PASS，0 findings。Gate 证据覆盖 task artifacts、issue #62、canonical workflow/script/tests、dogfood copies、preset overlays、README、durable docs、`.trellis/spec/**` 与 `status_events[]` 合同。

Review Gate 同时记录：Phase 2 post-commit audit 中 50 个 non-metadata changed files 均被 `phase2-check.json.dirty_paths` 覆盖；当前只允许 Trellis metadata tail 进入 finish-work。

## Issue 关闭范围

Closes #62

本 PR 只关闭 #62。没有 related issues 或 follow-up issues 被本次 PR 关闭。

## 安全说明

本次未引入 token、secret、private key、签名 URL、`.env`、数据库 URL 或客户数据处理逻辑。变更不触碰 CI/CD、容器、Docker Compose、Kubernetes/Kustomize/Helm、数据库 migration、Makefile，也未新增服务、配置入口、数据库变更或部署形态，因此无需同步部署资产。
