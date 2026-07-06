## 变更摘要

- 完成 #38：`trellis-finish-work` 的主示例改为先准备 task-local `pr-body.md`，再执行 `--body-file ... --dry-run`，dry-run 通过后再正式执行 `--body-file ...`。
- 同步 canonical `guru-team` workflow、preset overlay、dogfood workflow，以及 Codex、Claude、Cursor、`.agents` 等 finish-work 入口，避免某个平台仍展示裸 `finish-work.sh` 调用。
- 补充回归测试，防止 runtime entrypoint 或 public docs 再次出现缺少 reviewed PR body 与 dry-run 的 finish-work 示例。

## 影响范围

- Workflow 文案：`trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md`。
- Finish-work 入口：`trellis/presets/guru-team/overlays/**/trellis-finish-work*` 及 dogfood 副本 `.agents/skills/trellis-finish-work/SKILL.md`、`.codex/prompts/trellis-finish-work.md`、`.codex/skills/trellis-finish-work/SKILL.md`、`.claude/commands/trellis/finish-work.md`、`.cursor/commands/trellis-finish-work.md`。
- Public docs 与规范：`trellis/workflows/guru-team/README.md`、`.trellis/spec/workflow/quality-guidelines.md`。
- 测试：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 增加 finish-work entrypoint contract 覆盖。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，112 tests。
- `python3 -m json.tool trellis/index.json` 通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh` 通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-38-trellis-finish-work-pr-body` 通过。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过，dogfood copies 与 canonical overlays 一致。
- `trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh` 通过，已覆盖 throwaway install 与 preset overlay 安装检查。
- `git diff --check` 通过。

## Review Gate

- Branch Review Gate 已通过，reviewed HEAD：`156fcf43bb90b7dcc801f989c1871eb640b71c80`。
- Diff 范围：`origin/main...HEAD`。
- 最终放行审查代理：`019f357b-04c5-72d0-b6bc-c4d4a087ac05`，`findings_count=0`。
- 审查覆盖 workflow SSOT、canonical overlays、dogfood copies、public README、spec、tests、task artifacts、部署影响和 Issue Scope Ledger。

## Issue 关闭范围

Closes #38

### 仅引用或相关

- 无。

### 后续范围

- 无。

## 安全说明

- 未改动 token、secret、签名 URL、`.env`、数据库 URL 或客户数据处理逻辑。
- 未修改 CI/CD workflow、Dockerfile、Docker Compose、Kubernetes/Kustomize、数据库 migration 或 Makefile。
- 本次变更只影响 Guru Team Trellis workflow / overlay / 文档示例 / 测试，不改变部署资产和运行部署形态。
