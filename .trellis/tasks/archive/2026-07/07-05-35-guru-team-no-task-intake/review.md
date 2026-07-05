# Branch Review Gate 复审报告

## 审查结论

通过。已按 `.trellis/workflow.md` Phase 3.5 对 `origin/main...HEAD` 完整 diff 进行独立复审；当前未发现 P0/P1/P2/P3 findings。

前次两个问题已复核消除：

- P1 `phase2-check.json` stale：报告写入前运行 `.trellis/guru-team/scripts/bash/check-phase2-check.sh --json --task .trellis/tasks/07-05-35-guru-team-no-task-intake`，返回 `status: ok`，`checked_head` 为 `ef72b424bfdf159863ed5606787e4b7dac6c2028`。
- P3 Cursor fallback test：`.codex/hooks/test_inject_workflow_state.py` 已包含 `CursorSessionStartNoTaskTest`；`PYTHONDONTWRITEBYTECODE=1 python3 .codex/hooks/test_inject_workflow_state.py` 运行 6 tests OK。

## Diff Range

- Base：`origin/main`
- Merge base：`059f8f9fe2b377f37a03b9b533dba3121458cd3e`
- Reviewed HEAD：`ef72b424bfdf159863ed5606787e4b7dac6c2028`
- Diff range：`origin/main...HEAD`
- 当前分支：`codex/35-guru-team-no-task-intake`

说明：当前工作区仍有 task metadata 改动 `.trellis/tasks/07-05-35-guru-team-no-task-intake/phase2-check.json`，这是前次 P1 修复后的 gate evidence 更新；本复审按用户指定 HEAD 审查代码/文档 diff，并读取当前 task artifact 证据。

## 审查范围

覆盖的变更文件包括：

- canonical workflow 与 dogfood active workflow：`trellis/workflows/guru-team/workflow.md`、`.trellis/workflow.md`
- trellis-start canonical overlay 与 dogfood 副本：`trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`、`trellis/presets/guru-team/overlays/.codex/prompts/trellis-start.md`、`trellis/presets/guru-team/overlays/.codex/skills/trellis-start/SKILL.md`、`.agents/skills/trellis-start/SKILL.md`、`.codex/prompts/trellis-start.md`、`.codex/skills/trellis-start/SKILL.md`
- session fallback 与测试：`.codex/hooks/session-start.py`、`.cursor/hooks/session-start.py`、`.codex/hooks/test_inject_workflow_state.py`
- docs/spec：`README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/workflow/quality-guidelines.md`
- Guru Team dogfood artifact 与 task artifacts：`.trellis/guru-team/extension.json`、`.trellis/guru-team/handoff.json`、本任务 `prd.md` / `design.md` / `implement.md` / `planning-approval.json` / `phase2-check.json` / `issue-scope-ledger.json` / `check.jsonl` / `implement.jsonl` / `task.json`

## 验证与证据

- Source issue：`gh issue view 35 --repo castbox/guru-trellis --json ...` 显示 issue #35 目标为修复 Guru Team `no_task` intake，验收标准要求 `trellis-start`、`workflow-state:no_task`、Phase 1.0 均阻止 issue-backed 任务直接裸 `task.py create`，并要求 `check-env.sh --json`、`prepare-task.sh --json`、`prepare-task --create-worktree --create-task` 证据。
- Handoff evidence：`.trellis/guru-team/handoff.json` 指向 issue #35，`workspace_mode: worktree`，`workspace_path` 为当前 worktree，`base_branch` 为 `main`，`preflight.base_freshness.status` 为 `fresh`。
- Phase 2 evidence：当前 `phase2-check.json` 记录 `head: ef72b424bfdf159863ed5606787e4b7dac6c2028`、`diff_range: origin/main...HEAD`、`coverage.requirements/design/code/tests/spec_sync/cross_layer/docs_ssot/deployment` 均为 true；`check-phase2-check.sh --json` 返回 ok。
- Workflow evidence：`trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 的 `[workflow-state:no_task]` 直接列出 `check-env.sh --json` 与 `prepare-task.sh --json`，并写明 `prepare-task --create-worktree --create-task` 是 worktree mode 下创建执行环境的受控入口；Phase 0.4 与 Phase 1.0 均明确禁止 issue-backed/file-changing Guru Team worktree 任务在 source checkout 运行裸 `task.py create`。
- Session fallback evidence：Codex 与 Cursor no-task fallback 均改为指向 per-turn workflow-state、`check-env.sh --json`、`prepare-task.sh --json`，并写明 task creation consent 不是 current-checkout direct-edit consent。
- Test evidence：`PYTHONDONTWRITEBYTECODE=1 python3 .codex/hooks/test_inject_workflow_state.py` 通过，6 tests OK；`PYTHONDONTWRITEBYTECODE=1 python3 .trellis/scripts/common/test_workflow_phase.py` 通过，4 tests OK。
- Parser/phase evidence：`python3 ./.trellis/scripts/get_context.py --mode phase --step 0.4` 与 `--step 1.0` 输出均包含受控 `prepare-task --create-worktree --create-task` 路径与 source checkout 禁止语义。
- Overlay drift evidence：`trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 返回 `Dogfood overlay copies match canonical Guru Team overlays.`；未发现 `.new` / `.bak` 残留。
- Syntax/schema evidence：`python3 -m json.tool trellis/index.json` 与 task JSON artifacts 通过；`python3 -m py_compile ...` 覆盖相关 Python hook/script；`bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh` 通过；`python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-35-guru-team-no-task-intake` 通过；`git diff --check origin/main...HEAD` 通过。
- Official docs evidence：已用 `curl -k -L` 读取 Trellis 官方 custom workflow 与 custom spec template marketplace 文档。官方 custom workflow 文档确认 `workflow.md` 是 phase、skill routing、per-turn reminder 与 task.py catalog 的运行合同，workflow-state hook 解析 `[workflow-state:STATUS]`；spec marketplace 文档确认 template marketplace 用于可复用工程约定，不应放 `.trellis/tasks/`、workspace 或 active task state。本分支改动符合这些边界。
- Installer/marketplace evidence：`phase2-check.json` 记录 `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 通过，覆盖 public marketplace sample + 当前本地 preset installer。该脚本包含 throwaway `trellis init`、preset apply、`get_context.py`、`check-env`、`version`、finish/publish 直调阻塞、`trellis workflow --create-new` 预览和实际 workflow 切换验证。当前未合并分支的远端 `TRELLIS_WORKFLOW_SOURCE=gh:castbox/guru-trellis/trellis#codex/35-guru-team-no-task-intake` 未获取到 `index.json`，本报告不声称该远端 ref marketplace 验证已通过；这是未合并分支验证限制，不影响本地 canonical/preset 复审结论。

## Docs SSOT Reconciliation

本任务修改的是 Guru Team workflow/preset 的长期运行合同，已同步 durable docs / spec：

- `README.md` 增补日常入口说明：issue-backed/task-like/file-changing 的第一跳是 `check-env` + `prepare-task`，`prepare-task` 默认 planner-only，worktree mode 创建执行环境必须走受控 executor，direct-edit 只能是显式 override。
- `trellis/workflows/guru-team/README.md` 与 `trellis/presets/guru-team/README.md` 同步 no_task/worktree/task creation consent 语义。
- `.trellis/spec/workflow/quality-guidelines.md` 增补复用 review 规则，防止后续 workflow/preset 修改回退到裸 `task.py create`。
- Task artifacts 保留任务级需求、设计、实施和验证证据；未把 active task state 放入 spec template marketplace。

Docs SSOT 结论：已完成需要的 README/spec 同步；无需新增 `docs/requirements/` 或其它长期产品需求文档。

## 部署影响判断

本分支未触及 CI/CD、容器、Docker/Compose、Kubernetes/Kustomize/Helm、数据库 migration、Makefile 或运行部署资产。`git diff --name-only origin/main...HEAD` 的命中范围仅为 workflow、overlay、hook、README/spec、Guru Team task/metadata artifacts。结论：无需部署、CI/CD、容器、K8s/Kustomize、DB migration 或 Makefile 更新。

## Findings

无 findings。
