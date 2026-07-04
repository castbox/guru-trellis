## 变更摘要

- 修复 Guru Team `prepare-task --create-worktree` / `--create-task` 创建或复用 task worktree 后缺少 Trellis developer identity 的问题。
- executor 路径现在会优先从 source checkout 复制 gitignored `.trellis/.developer`，source 缺失但调用方提供 `--assignee` 时初始化目标 worktree identity，两者都不可用时 fail closed 并提示 `init_developer.py` 恢复命令。
- `infer_assignee()` 改为解析 `.trellis/.developer` 的 `name=` 字段，避免把整个多行 identity 文件写入 `task.py create --assignee`。

## 影响范围

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 与 dogfood 安装副本 `.trellis/guru-team/scripts/python/guru_team_trellis.py`。
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 新增 identity 继承、初始化、缺失阻塞和 assignee 解析测试。
- `trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`、`.trellis/spec/workflow/data-contracts.md` 已同步记录新的 executor 合同。
- 不改变 planner-only `prepare-task --json` 的无副作用语义，不修改 Trellis upstream、全局 npm 包或 `node_modules`。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，61 tests。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh` 通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 通过。
- `python3 -m json.tool trellis/index.json` 和 `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json` 通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过，dogfood overlay copies match canonical。
- disposable repo 验证 `prepare --create-worktree` 后目标 worktree 的 `preflight.developer_identity.status=copied`，且 `.trellis/.developer` 存在。
- `git diff --check` 通过。

## Review Gate

- Branch Review Gate 已由独立 Agent 按 `origin/main...0e628860dad7bdc3a34ec7e68e168a7e9812d5b9` 审查通过，并纳入 `review.md` / `phase2-check.json` metadata tail。
- Review 覆盖 source identity 复制、显式 `--assignee` 初始化、缺 identity fail closed、`infer_assignee name=` 解析、planner-only 无副作用、canonical/dogfood 同步、Docs SSOT 与部署影响。
- 未发现 P0/P1/P2/P3 finding。

## Issue 关闭范围

- Closes #26 - worktree 创建后应继承 Trellis developer identity。
- 本 PR 不关闭其他 issue；`issue-scope-ledger.json` 中 `related_issues` 与 `followup_issues` 均为空。

## 安全说明

- `.trellis/.developer` 仍是 gitignored 本地 runtime identity，未进入 tracked diff；未提交 `.bak` / `.new` 临时文件。
- 未涉及 token、secret、签名 URL、`.env` 内容、数据库 URL 或客户数据。
- 未修改 CI/CD、Docker/Compose、K8s/Kustomize、database migration、Makefile 或部署配置；本次变更只影响 Guru Team workflow/preset companion script、测试、README/spec 与 Trellis task metadata。
