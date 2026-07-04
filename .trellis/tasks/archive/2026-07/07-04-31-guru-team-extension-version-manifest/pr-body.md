## 变更摘要

- 为 Guru Team Trellis extension 增加独立于官方 Trellis CLI 的 canonical SemVer manifest：`trellis/guru-team-extension.json`，当前版本为 `0.1.0`。
- preset installer 现在会在目标仓库写入 `.trellis/guru-team/extension.json`，记录安装版本、workflow template、source repo/ref/commit/tree state、selected platforms、managed assets 和安装时间。
- `check-env --json` 与新增 `version.sh --json` 会暴露 `guru_team_extension` 节点，用户和 AI 排障时可以直接看到当前安装的 extension version 与 source provenance。
- README、preset/workflow README、需求文档和 `.trellis/spec/` 已同步说明 official Trellis CLI version、marketplace index schema version、canonical extension version、installed provenance 的边界。

## 影响范围

- 影响 Guru Team workflow / preset / companion scripts 的安装和排障面，不修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 影响目标仓库安装后的 `.trellis/guru-team/extension.json`、`.trellis/guru-team/scripts/bash/version.sh`、`check-env --json` 输出和 preset installer 输出。
- 影响本仓库 dogfood 安装副本：`.trellis/guru-team/extension.json` 与 `.trellis/guru-team/scripts/**` 已同步 canonical 版本。
- 不改变 workflow id、template id、preset 路径或现有 script CLI 的破坏性语义；缺少 installed manifest 的旧安装仍会 warning 并继续运行。

## 验证结果

- `python3 -m json.tool trellis/index.json && python3 -m json.tool trellis/guru-team-extension.json && python3 -m json.tool .trellis/guru-team/extension.json`：通过。
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过。
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过。
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：通过，83 tests。
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过。
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：通过，覆盖 public workflow sample 和当前本地 preset 的 installed manifest、`check-env --json`、`version.sh --json`。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-31-guru-team-extension-version-manifest && git diff --check`：通过。

## Review Gate

- 结论：独立 Branch Review Gate 复审通过，无 P0/P1/P2 finding。
- Reviewed HEAD：`5030cde306bf22962b729ef135d31186d532c893`
- Diff 范围：`origin/main...HEAD`
- Review 覆盖 docs、代码、测试、Trellis artifacts、config/scripts/schema、preset installer、dogfood installed copy、dogfood overlay drift、throwaway install、部署影响和安全边界。
- 前次 review 提出的 Phase 2 evidence stale 与 dogfood installed provenance 语义两个 P2 已修复并复审确认。

## Issue 关闭范围

- Closes #31 - Add Guru Team extension version manifest and installed provenance

### 仅引用或相关

- 无

### 后续范围

- 无

## 安全说明

- manifest/provenance 只记录 repo URL、ref、commit、tree state、selected platforms、managed asset list 和 install time；不记录 token、secret、private key、`.env`、signed URL、database URL 或 GitHub auth detail。
- `source_tree_state=dirty` 只是安装时 source tree 的客观状态，不包含 diff 内容。
- 本次未修改 CI/CD、Docker、Docker Compose、Kubernetes/Kustomize、Helm、数据库 migration/seed/backfill、Makefile 或 runtime entrypoint；不需要部署资产同步。
