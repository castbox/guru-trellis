## 变更摘要

本 PR 解决 GitHub issue intake 在需求不清晰或执行中范围变化时缺少显式判断与留痕的问题。

- 在 Guru Team workflow 中加入 intake clarity check：当 GitHub issue 或用户请求存在范围模糊、验收标准不清、涉及多个 issue 或可能需要拆分时，必须先使用 `trellis-brainstorm` 澄清，不能直接创建 task 或进入实现。
- 要求澄清后的 scope 回写到 GitHub issue body/comment，或在新 issue 创建前给出已审查的 proposed issue body，保证 Trellis task 的依据对 GitHub 可见。
- 新增任务执行中的 Scope Change Gate：当用户提出新增需求、引用其他 issue 或要求扩 scope 时，必须判断 current task / related issue / follow-up issue 的归属，并同步更新 `issue-scope-ledger.json`。
- 收紧 `issue-scope-ledger.json` 语义：只有被当前 task 完整验收且被 Branch Review Gate 覆盖的 issue 才能进入 `close_issues` 并在 PR 中使用 `Closes #xx`。
- 同步 canonical workflow、dogfood workflow、preset overlay、Codex/Claude/Cursor 入口文案、长期需求文档和回归测试。

## 影响范围

影响 Guru Team Trellis 的 issue intake、scope 变化处理、finish/publish 前的 issue 关闭判断，以及各平台 start/continue 入口提示。

本次修改覆盖：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/`
- 已安装 dogfood 副本：`.agents/`、`.codex/`、`.cursor/`、`.claude/`
- `docs/requirements/guru-team-trellis-flow.md`
- `docs/requirements/requirement-main.md`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`

未修改 CI/CD、容器、K8s/Kustomize、数据库 migration、SQL 或 Makefile，不需要部署侧配置变更。

## 验证结果

已通过以下验证：

- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：131 tests passed
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：18 tests passed
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：通过，覆盖新仓库 throwaway 安装验证
- `git diff --check origin/main...HEAD`：通过
- `bash -n`、`python3 -m py_compile`、`python3 -m json.tool`：通过
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-055-intake-scope-evolution`：通过
- `.trellis/guru-team/scripts/bash/check-review-gate.sh --json --allow-metadata-after-gate`：通过

## Review Gate

Branch Review Gate 已由独立审查代理完成并通过。

- Diff range：`origin/main...HEAD`
- Reviewed HEAD：`ecfa4c51f5da93f2672a28913f50450406408307`
- 审查代理：`019f3c0b-f959-7233-b215-bef77849195b`（Release Agent）
- 结论：0 个 P0/P1/P2/P3 finding
- 审查覆盖：issue #55 live scope、官方 Trellis 扩展边界、canonical/dogfood workflow 同步、overlay/installed copy 漂移、长期文档 SSOT、回归测试、开箱即用验证和部署影响判断

## Issue 关闭范围

Closes #55

`issue-scope-ledger.json` 仅将 #55 列入 `close_issues`，`related_issues` 和 `followup_issues` 为空。本 PR 不关闭其他 issue。

## 安全说明

本次变更不涉及 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或敏感原始记录。

变更内容集中在 workflow Markdown、平台入口 overlay、需求文档、回归测试和 Trellis task artifact；未引入新的外部服务调用、凭据读取、部署配置或数据迁移。
