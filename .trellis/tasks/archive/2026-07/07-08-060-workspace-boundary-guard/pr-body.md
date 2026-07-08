## 变更摘要

- 为 Guru Team workflow 增加 workspace boundary guard：在 worktree 模式下，任务创建、handoff、review/report artifact、agent assignment、Branch Review Gate 等关键入口都会校验当前写入位置属于任务 `workspace_path`，避免把 `.trellis/tasks/`、`.trellis/guru-team/handoff.json`、review artifact 或 patch 误写到 source checkout。
- 新增并同步 `check-workspace-boundary` validator、相关 Python 记录/校验逻辑、bash wrapper、回归测试、workflow/spec/README 文档、Codex/Claude/Cursor overlay 与 dogfood installed copy。
- 将 Guru Team extension 版本提升到 `0.6.5-guru.2`，同步 canonical manifest、dogfood manifest、preset README、workflow README 和 `verify-throwaway-install.sh` 默认 source，确保这次 workspace boundary 能力有独立 release revision。
- 为 Branch Review Gate validator 增加 replacement closure chain 的机器校验：当原 finding-owner review agent 失败或中断时，要求存在 predecessor failed/unfinished 状态、`replacement-started` 事件、`reuse_decisions[] decision=replace`、闭环轮 `findings_count=0` 与 `reuse_decision=replace`，并禁止 replacement closure reviewer 直接成为 final reviewer。

## 影响范围

- 影响 Guru Team Trellis workflow、preset installer、platform overlay、dogfood 安装副本、workflow/spec 文档和 companion scripts。
- 不修改 Trellis 上游源码、全局 npm 包、`node_modules`、业务项目私有规则或官方模板机制。
- 不修改 CI/CD workflow、Docker / Compose、Kubernetes / Helm / Kustomize、数据库 migration、Makefile、runtime config template 或生产服务代码。
- #76 的 heartbeat / workspace-aware liveness 策略仍是后续能力，本 PR 只收敛 #60 的 workspace boundary fact layer 与 artifact 写入边界。

## 验证结果

- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：161 个测试通过。
- `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：27 个测试通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`：通过。
- JSON 校验覆盖 `trellis/index.json`、`trellis/guru-team-extension.json`、`.trellis/guru-team/extension.json` 与 intake schema：通过。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-060-workspace-boundary-guard`：通过。
- `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`：通过；再次执行无新增 `.new` / `.bak`。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `git diff --check` 与 `git diff --check origin/main...HEAD`：通过。
- tag-pinned throwaway install 仍需在本 PR 合并并创建 annotated tag `v0.6.5-guru.2` 后执行；当前 PR 不声明公开 tag 安装链路已完成验证。

## Review Gate

- Branch Review Gate 覆盖 `origin/main...HEAD` 完整 diff，reviewed head 为 `3af6ee1d99fcbae862ef993efa851111c9874a96`。
- 第 004 轮 fresh final reviewer `019f4212-acdc-7492-849c-f7c5efe7d72e` 复核 workspace boundary guard、release/version bump、replacement closure validator、tests、workflow/spec/docs、preset installer、canonical overlays 与 dogfood installed copies，`findings_count=0`。
- `review-gate.json` 已通过 `.trellis/guru-team/scripts/bash/check-review-gate.sh --json --allow-metadata-after-gate` 校验，当前非代码 dirty 状态仅为允许的 Trellis metadata。
- Issue scope ledger 记录 #60 为 close scope，#76 为 follow-up only。

## Issue 关闭范围

Closes #60.

Refs #76，但不关闭 #76。

## 安全说明

- 本 PR 不新增 token、secret、private key、签名 URL、数据库 URL、`.env` 内容或客户数据。
- 敏感词扫描只命中安全规则文字、literal token 文案、tokenization 代码和环境变量读取逻辑，没有发现实际凭据。
- Companion scripts 仍只承担 executor / validator / recorder 角色；workspace boundary 与 replacement closure 的判断性流程仍由 workflow、skill 和 AI/human review gate 执行。
