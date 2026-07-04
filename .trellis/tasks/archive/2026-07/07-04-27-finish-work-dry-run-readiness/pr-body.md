## 变更摘要

- 修复 Guru Team `finish-work` 的 dry-run 语义：`finish-work --dry-run --from-trellis-finish-work` 现在只执行 readiness 校验并输出将要执行的 archive、journal、metadata commit、push、PR 发布计划，不再移动 task、写 journal、创建 metadata commit、push 或创建 PR。
- 修正 Codex 平台默认运行方式：缺省或非法 `codex.dispatch_mode` 现在会回落到 `sub-agent`，避免新安装项目默认 inline 导致 Branch Review Gate 无法获得独立 Agent review。
- 保留显式 `codex.dispatch_mode: inline`，作为调试或降级模式；preset installer 会为缺省项目 materialize `.trellis/config.yaml` 中的 `codex.dispatch_mode: sub-agent`。

## 影响范围

受影响的运行面包括 Guru Team workflow helper、dogfood 安装副本、Codex hook、workflow phase 解析、preset installer、throwaway install 验证脚本，以及 README / workflow / preset 文档。

本次同步了 canonical 与 dogfood 入口：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 和 `.trellis/guru-team/scripts/python/guru_team_trellis.py` 保持一致，`trellis/workflows/guru-team/workflow.md` 和 `.trellis/workflow.md` 保持一致。preset installer 会为缺省项目 materialize `.trellis/config.yaml` 中的 `codex.dispatch_mode: sub-agent`，并保留显式 inline。

本 diff 未修改 GitHub Actions、Docker / Compose、Kubernetes / Kustomize / Helm、数据库 migration、Makefile 或运行服务入口，不需要同步部署资产。

## 验证结果

已通过以下验证：

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：62 个测试通过。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：4 个测试通过。
- `python3 .trellis/scripts/common/test_workflow_phase.py`：4 个测试通过。
- `python3 .codex/hooks/test_inject_workflow_state.py`：3 个测试通过。
- `python3 -m json.tool trellis/index.json`、`intake-handoff.schema.json` 和 task `issue-scope-ledger.json`：通过。
- `bash -n` 覆盖 workflow、preset、dogfood bash scripts：通过。
- `python3 -m py_compile` 覆盖 workflow helper、dogfood helper、preset installer、Codex hook 和 workflow phase parser：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `python3 ./.trellis/scripts/task.py validate 07-04-27-finish-work-dry-run-readiness`：通过。
- `git diff --check`：通过。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`：确认 `codex_dispatch unchanged sub-agent`，无 `.new` / `.bak`。

未完整实跑当前分支作为 public marketplace source 的 throwaway install。`verify-throwaway-install.sh` 对此按设计 fail-closed，避免把 public `main` 的 marketplace 验证误认为当前分支验证。

## Review Gate

Branch Review Gate 已由独立 `trellis-check-agent Popper` 审查 `origin/main...HEAD` 并通过。审查覆盖 dry-run readiness preview、Codex 默认 sub-agent dispatch、显式 inline 降级、preset installer、dogfood overlay、README / workflow 文档、测试、任务 artifacts、部署影响和安全风险。

Review Gate 未发现 P0/P1/P2 阻塞问题。记录的 P3 风险为：当前分支完整 throwaway install 未实际执行；dry-run 无副作用主要由 mock/unit test 覆盖，后续可沉淀真实 task fixture 端到端验证。

## Issue 关闭范围

Closes #27

本 PR 完整覆盖 issue #27：`finish-work --dry-run` 不再产生 archive、journal、metadata commit、push 或 PR 副作用，并补齐 Codex 默认 sub-agent dispatch，使 Branch Review Gate 在新安装项目中具备可执行的独立 review 路径。

## 安全说明

本次变更未引入 token、secret、private key、签名 URL、`.env`、数据库 URL 或客户数据处理逻辑。变更集中在本地 Trellis workflow / preset / helper / hook / 文档 / 测试，不改变线上运行服务、数据库 schema、网络访问策略或部署权限边界。
