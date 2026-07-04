## 变更摘要

为 Guru Team preset installer 增加平台 overlay 选择能力，解决 `trellis init --codex --cursor` 后 preset 仍恢复 `.claude/` 入口的问题。

- 新增可重复 `--platform {codex,cursor,claude}` 参数。
- 默认安装共享 `.agents/skills`、Codex overlay、Cursor overlay，不再默认创建 `.claude/`。
- 新增 `--all-platforms`，用于需要保留历史全量 overlay 安装行为的维护场景。
- `--platform` 与 `--all-platforms` 互斥，未知平台由 argparse fail closed。
- 同步更新顶层 `README.md`、preset README、throwaway 验证脚本和 preset installer spec。

## 影响范围

- 影响 `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 的 overlay 复制逻辑。
- 影响 `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 的默认验证路径，明确验证 Codex + Cursor 不创建 `.claude/`。
- 影响公开安装/升级文档中的 preset apply 命令，默认文案从“安装后清理未选择平台”调整为“installer 不创建未选择平台 overlay”。
- 不修改 canonical overlay 文件本身；Claude overlay 仍保留在仓库中，只有显式 `--platform claude` 或 `--all-platforms` 时安装。

## 验证结果

- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：通过，12 个测试覆盖默认平台、重复 apply、Claude 显式选择、全量平台、互斥参数和非法平台。
- `python3 -m py_compile trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过。
- `bash -n trellis/presets/guru-team/scripts/bash/apply.sh trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：通过。
- `python3 -m json.tool trellis/index.json`：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-11-let-preset-installer-apply-only`：通过。
- `git diff --check origin/main...HEAD`：通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- 临时 repo 行为抽样：默认 apply 安装 `.agents/.codex/.cursor` 且不创建 `.claude`；`--all-platforms` 创建 `.claude`。

未运行完整 `verify-throwaway-install.sh`，因为该脚本在非 `main` 分支会 fail closed，避免把公开 marketplace 采样误报为当前分支验证。本 PR 对 issue #11 的关键行为已由单测和临时 repo 抽样覆盖。

## Review Gate

Branch Review Gate 已由独立 `trellis-check-agent` 审查 `origin/main...HEAD` 完整 diff 并通过。审查覆盖 README、preset README、installer Python、installer 单测、throwaway 验证脚本、preset spec、Trellis task artifacts、handoff 和 Issue Scope Ledger，结论为无 P0/P1/P2/P3 findings。

Docs SSOT reconciliation：本仓库没有 `docs/` 目录；长期公开文档为 `README.md` 与 `trellis/presets/guru-team/README.md`，本次已同步更新。

## Issue 关闭范围

Closes #11

本 PR 完整处理 issue #11：Codex + Cursor 默认安装不再创建 `.claude/`，重复 apply 不会恢复未选择平台目录，README/preset README 与 installer 参数一致，并保留 `--all-platforms` 全量安装方式。

## 安全说明

本次变更不涉及 token、secret、`.env`、私钥、签名 URL 或客户数据。变更只影响本地 preset installer、公开文档、测试脚本和 Trellis task evidence；不涉及 CI/CD、容器、Kubernetes、数据库 migration、Makefile 或线上运行服务。
