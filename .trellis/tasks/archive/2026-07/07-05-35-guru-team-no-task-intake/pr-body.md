## 变更摘要

- 更新 Guru Team workflow 的 no_task triage、`[workflow-state:no_task]`、Phase 0.4 handoff review 和 Phase 1.0 task creation 文案，使 issue-backed、task-like、file-changing 请求优先进入 `check-env.sh --json` 与 `prepare-task.sh --json`，而不是在 source checkout 直接运行裸 `task.py create`。
- 同步 canonical `trellis-start` overlay、Codex prompt/skill 副本、dogfood `.trellis/workflow.md` 和 README/spec，明确 `workspace_mode: worktree` 下创建执行环境必须通过 `prepare-task --create-worktree --create-task` 或等价受控入口。
- 更新 Codex/Cursor no-task session fallback，并补充回归测试，覆盖 prepare/worktree 入口、`task creation consent` 不等于 current-checkout direct-edit consent，以及旧泛化 task consent 提示不再出现。

## 影响范围

- 影响 Guru Team workflow marketplace、preset overlay、dogfood 安装副本、Codex/Cursor session-start fallback，以及团队文档中的 no_task 入口说明。
- 普通 Trellis native workflow 的轻量任务 `task.py create` 行为没有在脚本层被改动；差异集中在 Guru Team overlay / workflow 启用场景。
- 对话型或非文件修改的小任务仍可只询问是否创建 Trellis task；issue-backed、明确开发任务或文件修改请求会被引导到 Guru Team intake/worktree 流程。

## 验证结果

- `python3 -m json.tool trellis/index.json` 与 `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json` 通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh` 通过；相关 Python hook/script `py_compile` 通过。
- `python3 .codex/hooks/test_inject_workflow_state.py` 通过，6 tests OK；`python3 .trellis/scripts/common/test_workflow_phase.py` 通过，4 tests OK。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-35-guru-team-no-task-intake`、`get_context.py --mode phase --step 0.4`、`get_context.py --mode phase --step 1.0`、`check-dogfood-overlay-drift.sh`、`git diff --check origin/main...HEAD` 均通过。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 通过，覆盖 public marketplace sample 与当前本地 preset installer。未合并分支远端 `gh:castbox/guru-trellis/trellis#codex/35-guru-team-no-task-intake` 未能获取 `index.json`，本 PR 不声称该远端 ref marketplace 验证已通过。

## Review Gate

- 独立 `trellis-check` agent 已按 `origin/main...HEAD` 完整 diff 复审 canonical workflow、dogfood workflow、trellis-start overlay、Codex/Cursor fallback、回归测试、README/spec、task artifacts、Docs SSOT reconciliation、preset installer 与 dogfood overlay drift evidence。
- Branch Review Gate 已通过，review report digest 已记录在 task-local `review-gate.json`，当前无 P0/P1/P2/P3 findings。
- Gate 同时记录本分支未触及 CI/CD、容器、Kubernetes/Kustomize/Helm、数据库 migration、Makefile 或运行部署资产，因此无需同步部署资产。

## Issue 关闭范围

- Closes #35。本分支完整覆盖 issue 中要求的 `trellis-start`、`workflow-state:no_task`、Phase 1.0、Codex/Cursor fallback 与回归测试修复。
- 本任务没有 related issues 或 followup issues。

## 安全说明

- 本次变更只涉及 workflow/prompt/docs/test/task metadata，不处理 secret、token、客户数据、签名 URL、`.env` 或数据库连接信息。
- 未修改发布流水线、容器镜像、运行时配置、数据库结构或业务服务入口；部署风险为低。
- PR body 关闭 issue 的语义仅限 `issue-scope-ledger.json` 中已记录验收证据且被 Review Gate 覆盖的 #35。
