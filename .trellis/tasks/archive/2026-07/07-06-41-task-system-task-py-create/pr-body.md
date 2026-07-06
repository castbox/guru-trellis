## 变更摘要

在 Guru Team workflow 的 `### Task System` 命令目录前增加 reference-only 提示，明确该命令块只是 Trellis task CLI 参考，不是 Guru Team issue-backed / task-like / file-changing work 的入口。

新增说明覆盖：

- Guru Team durable、issue-backed、task-like、file-changing work 必须先走 Phase 0 `check-env` + `prepare-task`。
- `workspace_mode: worktree` 下不能从 source checkout 直接运行裸 `task.py create`。
- 裸 `task.py create` 只允许作为 Phase 1.0 controlled follow-up，且 shell/editor 已位于 `prepare-task` 返回或写入的 `workspace_path`。

同步修改了 canonical workflow 与本仓库 dogfood active copy：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`

## 影响范围

影响 Guru Team marketplace workflow 和本仓库 dogfood workflow 的 AI 运行时提示。该变更不修改 `task.py`、`prepare-task.sh`、installer、schema、overlay、hook 或 Trellis upstream。

普通 Trellis native workflow 的 `task.py create` 行为不变；本 PR 只调整 Guru Team workflow 文案，降低 AI 被前部 CLI command catalog 误导、绕过 Phase 0 intake/preflight 的风险。

## 验证结果

已完成以下验证：

- `rg` 检查两份 workflow 均出现 reference-only、Phase 0 prepare-first、source checkout 禁止和 `workspace_path` controlled follow-up 语义。
- `python3 ./.trellis/scripts/get_context.py --mode phase`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.0`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-41-task-system-task-py-create`
- `python3 -m json.tool trellis/index.json`
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
- `git diff --check`
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`
- `TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#codex/41-task-system-task-py-create trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`

已发布 release tag 的 throwaway install 验证通过；PR publish 后已补跑当前分支 marketplace 安装验证，`gh:castbox/guru-trellis/trellis#codex/41-task-system-task-py-create` 能完成 `trellis init`、preset apply、`check-env`、`version.sh`、finish/publish direct-call guard、workflow preview 与 forced switch 验证。

## Review Gate

Branch Review Gate 已通过。独立最终放行审查代理审查了 `origin/main...HEAD` 完整 diff，结论为 `findings: []`。

Review Gate 覆盖：

- issue #41 验收标准；
- canonical workflow 与 dogfood workflow 同步；
- task artifacts、Issue Scope Ledger、planning approval、Phase 2 check；
- Docs SSOT reconciliation；
- CI/CD、Docker、Compose、K8s/Kustomize/Helm、DB migration、Makefile、runtime config 部署影响判断。

## Issue 关闭范围

Closes #41

本 PR 只关闭 issue #41。无 related issues，无 follow-up issues。

## 安全说明

本 PR 不包含 token、secret、private key、`.env`、数据库 URL、签名 URL、客户数据或敏感原始记录。变更只涉及 workflow Markdown 文案和 Trellis task metadata，不改变脚本执行路径、权限模型、部署配置或运行时凭据处理。
