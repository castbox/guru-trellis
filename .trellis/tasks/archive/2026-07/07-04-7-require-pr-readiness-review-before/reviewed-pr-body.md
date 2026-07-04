## 变更摘要

### 发布门禁

- 收紧 Guru Team `publish-pr`：non-draft 发布必须使用 AI 审阅过的 `--body-file` 或 `--body-artifact`，脚本生成的 `generated` body 只保留为 draft/preview 辅助。
- 收紧 Guru Team `finish-work`：在 archive、journal、push 和 PR 创建前先校验 PR readiness source，缺少 reviewed source 时直接阻塞。
- 增加 archive 后 artifact 读取规则：如果 finish-work 前传入 active task 下的 body/readiness path，archive 后内部 publish 会重写到 archived task artifact path 再读取最终 PR body。

### Artifact 合同

- `--body-artifact` 现在必须包含 `ready: true`，并提供非空 `body` 或 `body_file`。
- readiness artifact 内的相对 `body_file` 以 artifact 所在目录解析，避免依赖 repo root 的隐式 fallback。
- `publish-pr --dry-run` 返回 `reviewed_source_required`、`reviewed_source_ok` 和 `reviewed_source_errors`，让 AI 在真实发布前能看到 non-draft source 门禁状态。

### 文档与入口同步

- 同步 canonical workflow、dogfood `.trellis/workflow.md`、top-level README、workflow README、preset README 和 workflow specs。
- 同步 `.agents`、`.codex`、`.claude`、`.cursor` finish-work overlays，明确 PR body/readiness 文件是 task metadata，并在 archive 后作为 publish SSOT。

## 影响范围

- Guru Team workflow marketplace：`trellis/workflows/guru-team/workflow.md`。
- Guru Team companion script：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 及 dogfood copy。
- Guru Team publish/finish tests：`trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
- Guru Team preset overlays：finish-work 技能、命令和提示入口。
- Durable docs/spec：README、workflow README、preset README、`.trellis/spec/workflow/*`。
- Trellis task metadata：#7 的 PRD、设计、实施计划、ledger、review gate 证据。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 通过，32 个测试。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh` 通过。
- `python3 -m json.tool trellis/index.json` 与 `python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json` 通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-7-require-pr-readiness-review-before` 通过，`implement.jsonl` / `check.jsonl` 各 5 条。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过，dogfood overlay copies match canonical。
- `git diff --check origin/main...HEAD` 通过。
- `python3 ./.trellis/scripts/get_context.py --mode phase`、`--step 3.5`、`--step 3.7` 通过。

## Review Gate

- Reviewed HEAD：`d5c333e160817857d1bc202668cafa110a6d9823`
- Diff range：`origin/main...HEAD`
- Review report：`.trellis/tasks/07-04-7-require-pr-readiness-review-before/review.md`
- Review gate：`.trellis/tasks/07-04-7-require-pr-readiness-review-before/review-gate.json`
- Findings：无 P0/P1/P2/P3。
- Gate 结论：已覆盖 canonical runtime、tests、workflow、README、spec、preset overlays、dogfood copies 和 task artifacts；Issue Scope Ledger 仅关闭 #7。

## Issue 关闭范围

- Closes #7

## 安全说明

- 本次变更不引入 secret、token、private key、数据库 URL、签名 URL、`.env` 输出或客户数据处理。
- 本次变更未修改 `.github/workflows/*`、Dockerfile、Docker Compose、Kubernetes/Kustomize、数据库 migration、Makefile 或 runtime config。
- 本次变更不新增服务、CLI 顶层入口、后台 worker、队列、migration 或运行时配置；无需同步部署资产。
- 发布行为的安全边界被收紧：non-draft PR 不能再依赖脚本生成 body 作为 readiness evidence，必须读取已审阅的 task metadata artifact。
