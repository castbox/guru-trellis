## 变更摘要

本 PR 为 Guru Team workflow 增加 `resolve-human-artifacts` companion helper，用于在阶段回复中确定性解析当前 task 的人类 review Markdown 产物。

- 新增 `resolve-human-artifacts` 子命令和 thin Bash wrapper，面向阶段回复提供 task Markdown 产物的路径、存在性、active/archive 状态事实。
- 将 `Markdown 产物 review 表` 写入 Guru Team workflow、continue / finish-work overlay 和公开文档，确保用户从最近一次阶段回复即可打开当前 task 的关键 Markdown 产物。
- 把新 wrapper 纳入 preset managed assets、installed dogfood copy、extension manifest、throwaway install verifier 和回归测试，避免新仓库安装时缺少脚本入口。

标准阶段产物表只包含 `prd.md`、`design.md`、`implement.md`、`review.md`、`pr-body.md` 五个 Markdown 文件。缺失文件返回空 `link`，AI 回复不得生成死链；`planning-approval.json`、`phase2-check.json`、`review-gate.json`、`pr-readiness.json`、`issue-scope-ledger.json`、`agent-assignment.json` 等 JSON 证据不进入默认人类 review 表。

同时同步了 canonical workflow、dogfood `.trellis/workflow.md`、shared / Codex / Claude / Cursor 的 continue 与 finish-work overlay，要求 planning stop、Phase 2 完成、Branch Review Gate、finish-work dry-run、正式 archive/publish 回复都运行 resolver 并输出 `Markdown 产物 review 表`。正式 finish-work archive 后必须重新 resolve archive path，不能复用 archive 前 active task 链接。

## 影响范围

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 与 installed dogfood copy：新增 `resolve-human-artifacts` 子命令。
- `trellis/workflows/guru-team/scripts/bash/resolve-human-artifacts.sh` 与 installed dogfood wrapper：新增可执行 wrapper。
- `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`、preset README、extension manifest、throwaway verifier：把新 wrapper 纳入 managed assets / public API / 安装验证。
- `trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`、`.agents`、`.codex`、`.claude`、`.cursor` overlays：补充阶段回复必须输出 Markdown 产物 review 表的运行规则。
- README、workflow README、preset README 与相关 specs：同步 resolver 合同、finish-work archive 后重新 resolve 的要求、JSON artifact 不进默认表的边界。

本次未修改 CI/CD、Docker / Compose、K8s / Helm / Kustomize、DB migration、Makefile 或运行部署资产。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：186 tests OK。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：27 tests OK。
- `python3 -m json.tool trellis/index.json`、`trellis/guru-team-extension.json`、`.trellis/guru-team/extension.json`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过。
- canonical 与 dogfood `resolve-human-artifacts.sh --json` smoke：返回五个 Markdown artifact，缺失 `review.md` / `pr-body.md` 时 `link` 为空。
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.4/2.2/3.5/3.6/3.7`：阶段上下文包含 resolver / review 表规则。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-061-task-markdown-review-table`：通过。
- `git diff --check`：通过。

未执行完整 current-branch throwaway install。当前分支尚未作为远端 marketplace ref 发布，默认 verifier 会采样已发布 `v0.6.5-guru.3`，不能证明当前未提交 diff 的完整开箱即用安装链路；该限制已记录在 task ledger 与 Review Gate observation。

## Review Gate

Branch Review Gate 已通过。最终放行审查代理审查了 `origin/main...HEAD` 完整 diff，覆盖 resolver Python、Bash wrapper、installed dogfood copy、preset installer、throwaway verifier、unit tests、workflow / README / preset README、extension manifests、shared / Codex / Claude / Cursor overlays，以及 task artifacts 与相关 specs。

Review Gate 结论：无 P0/P1/P2/P3 finding。观察项为完整 current-branch throwaway install 未执行，需要在发布说明中如实披露。

## Issue 关闭范围

Closes #61

`issue-scope-ledger.json` 将 #61 记录为 `close_issues`。本 PR 完整承接 #61 的标准阶段产物表需求：新增 deterministic resolver、同步 workflow / overlay / docs，并验证 JSON artifact 不进入默认表、missing artifact 不生成死链、finish-work archive 后重新 resolve archive path。

## 安全说明

本次变更不包含 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。变更范围是 Trellis workflow / preset / overlay / docs / companion scripts / tests，不改变业务运行服务、数据库 schema、容器镜像或部署拓扑。
