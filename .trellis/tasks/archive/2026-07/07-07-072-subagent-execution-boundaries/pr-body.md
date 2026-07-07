## 变更摘要

- 在 Guru Team workflow 与 dogfood workflow 中明确默认 `sub-agent` mode 的三段强制执行边界：实现必须由 `trellis-implement` 执行，Phase 2 check 必须由 `trellis-check` 执行，commit 后 Branch Review 必须由独立 review subagent 执行。
- 更新 Codex、Claude、Cursor 与 channel runtime 的 continue / implement / check overlay，明确主 agent 只负责规划、调度、等待、恢复、替换、记录 evidence、commit 与 finish，不得用主 agent 自己的实现、自检、自审或脚本校验替代 subagent 工作。
- 同步 README、workflow README、preset README、durable requirements 与 `.trellis/spec/**`，明确 `phase2-check.json` 是固化 `trellis-check` AI check 结论和验证证据的 Guru Team artifact，不是脚本替代 AI check 的入口。
- 保持 #43 agent identity、#44 Branch Review Gate pass 语义、#62 wait timeout / stale / unfinished termination 合同为引用关系，没有复制、改写或弱化既有规则。

## 影响范围

- 修改 canonical workflow：`trellis/workflows/guru-team/workflow.md`。
- 修改 canonical preset overlays：`trellis/presets/guru-team/overlays/**`，并通过 preset apply 同步 dogfood installed copies。
- 修改 dogfood 运行副本：`.trellis/workflow.md`、`.agents/skills/**`、`.codex/**`、`.claude/**`、`.cursor/**`、`.trellis/agents/**`。
- 修改公共说明与 durable docs：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`docs/requirements/**`、`.trellis/spec/**`。
- 未修改 Trellis 官方 npm 包、`node_modules`、GitHub Actions、Docker/Compose、Kubernetes/Helm/Kustomize、DB migration、Makefile 或运行时配置。

## 验证结果

- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` 通过，dogfood installed copies 已按 canonical overlay 同步。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过，canonical overlay 与 dogfood copies 无漂移。
- `python3 -m json.tool trellis/index.json .trellis/guru-team/handoff.json .trellis/guru-team/extension.json trellis/guru-team-extension.json` 通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh` 通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py` 通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-072-subagent-execution-boundaries` 通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase` 以及 `--step 1.1`、`--step 2.1`、`--step 2.2`、`--step 3.5` 通过。
- Codex canonical/dogfood `trellis-implement`、`trellis-check` TOML 解析通过。
- `git diff --check` 通过。
- `.new` / `.bak` 扫描无输出。
- tag-pinned throwaway install 样本通过：使用 `gh:castbox/guru-trellis/trellis#v0.6.5-guru.1` 初始化干净项目，并应用当前 worktree preset overlay，覆盖 overlay、channel runtime agents、check-env/version、finish/publish direct-call 阻断、workflow preview 与 switch。
- 当前分支 marketplace source 未覆盖：分支尚未 push，无法用 `gh:castbox/guru-trellis/trellis#codex/072-subagent-execution-boundaries` 验证当前分支 workflow source。
- 完整 upgrade/update throwaway 场景未重跑；本轮验证覆盖 preset apply、dogfood drift 与 tag-pinned throwaway install 样本。

## Review Gate

- 实现代理 `019f3d27-f5e6-70f3-bb67-b9c55b748eee` 已完成实现 handoff。
- 阶段二检查代理 `019f3d3b-8cdd-7d02-a474-2b5d845a74dc` 已完成 Phase 2 check，`phase2-check.json` 记录当前 scope 无未修复 findings。
- 初始最终放行审查代理超时后已按 #62 记录 stale 与 `terminated-unfinished`，replacement review agent `019f3d72-1657-7153-b0e3-2efbe6918ecf` 已独立审查 `origin/main...HEAD` 完整 diff。
- Branch Review Gate 对 `80ef050bd27f6556b3896b23a59447957225baab` 通过，`review-gate.json` 记录 `findings_count: 0`。

## Issue 关闭范围

Closes #72

`issue-scope-ledger.json` 中 `close_issues` 只包含 #72，无 `related_issues` 或 `followup_issues`。本 PR 只关闭默认 `sub-agent` mode 下强制 implement、check 与 branch review 均由 subagent 执行的 workflow / overlay / docs 合同问题。

## 安全说明

- 本次变更不包含 token、secret、private key、签名 URL、`.env`、客户数据或敏感原始记录。
- 未新增网络调用、权限扩大、部署脚本、数据库迁移或运行时配置。
- Companion scripts 仍只承担 executor / recorder / validator 角色；实现充分性、check 充分性、review 充分性继续由 AI review evidence 承担。
