# Branch Review Gate 复审报告

## 结论

本次独立 Branch Review Gate 复审范围为 `origin/main...HEAD`，当前 HEAD 为 `5030cde306bf22962b729ef135d31186d532c893`，任务为 issue #31 `Add Guru Team extension version manifest and installed provenance`。

复审覆盖 docs、代码、测试、Trellis artifacts、config/scripts/schema、preset installer、dogfood installed copy、dogfood overlay drift、throwaway install、部署影响和安全边界。前次两个 P2 均已解决，未发现新的 P0/P1/P2 finding。

**Gate 可通过。无 P0/P1/P2 finding。**

## Scope

- Diff range：`origin/main...HEAD`
- Base branch：`main`
- Head：`5030cde306bf22962b729ef135d31186d532c893`
- GitHub issue：#31
- Worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/31-guru-team-extension-version-manifest`
- 已读取任务 artifacts：
  - `.trellis/tasks/07-04-31-guru-team-extension-version-manifest/prd.md`
  - `.trellis/tasks/07-04-31-guru-team-extension-version-manifest/design.md`
  - `.trellis/tasks/07-04-31-guru-team-extension-version-manifest/implement.md`
  - `.trellis/tasks/07-04-31-guru-team-extension-version-manifest/phase2-check.json`
  - `.trellis/tasks/07-04-31-guru-team-extension-version-manifest/issue-scope-ledger.json`
- 主要变更面：
  - canonical manifest：`trellis/guru-team-extension.json`
  - installed provenance：`.trellis/guru-team/extension.json`
  - preset installer：`trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
  - workflow helper：`trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
  - user entrypoint：`version.sh` canonical copy + dogfood copy
  - tests：两个 Python unittest 文件
  - docs/spec：`README.md`、preset/workflow README、`docs/requirements/requirement-main.md`、`.trellis/spec/preset/installer.md`、`.trellis/spec/workflow/data-contracts.md`
  - verification：throwaway install script、Phase 2 check artifact、Issue Scope Ledger

## 验证证据

- `.trellis/guru-team/scripts/bash/check-phase2-check.sh --json`：通过，`checked_head=5030cde306bf22962b729ef135d31186d532c893`
- `python3 -m json.tool trellis/index.json && python3 -m json.tool trellis/guru-team-extension.json && python3 -m json.tool .trellis/guru-team/extension.json`：通过
- `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh .trellis/guru-team/scripts/bash/*.sh`：通过
- `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .trellis/guru-team/scripts/python/guru_team_trellis.py`：通过
- `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：通过，83 tests
- `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过，dogfood overlay copies match canonical Guru Team overlays
- `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1 trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh`：通过，覆盖 public workflow sample + 当前本地 preset；验证 installed manifest、`check-env --json`、`version.sh --json`、默认 Codex/Cursor 平台、`.claude/` 未创建、existing project workflow preview/switch
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-31-guru-team-extension-version-manifest && git diff --check`：通过
- `.trellis/guru-team/scripts/bash/version.sh --json`：通过，输出 installed Guru Team extension version/provenance
- `.trellis/guru-team/scripts/bash/check-env.sh --json`：通过，输出 `guru_team_extension` 节点

说明：复审未再次执行 `apply.sh --repo . --all-platforms`，避免改写 dogfood installed manifest 的 `installed_at`。`phase2-check.json` 记录该命令已在修复阶段通过，并且 dogfood drift check 当前通过。throwaway install 会在临时 repo 中应用当前本地 preset，输出显示本次临时安装观测到 `source_commit=5030cde306bf22962b729ef135d31186d532c893`、`source_tree_state=dirty`。

## 前次 P2 处理确认

### 已解决：`phase2-check.json` stale

前次 finding：`phase2-check.json` 记录的 HEAD 是 `7a715753f19dc55124493dbed33f945eb30a0de2`，与 review HEAD 不一致。

本次确认：

- 当前 `phase2-check.json` 记录 `head=5030cde306bf22962b729ef135d31186d532c893`
- `.trellis/guru-team/scripts/bash/check-phase2-check.sh --json` 返回 `status=ok`
- artifact 的 `dirty_paths` 只包含 task-local `review.md` metadata，符合复审阶段允许的 metadata tail

### 已解决：dogfood installed manifest provenance 语义不清

前次 finding：已提交 `.trellis/guru-team/extension.json` 的 `source.commit` 指向 apply 前提交，容易被误读为当前 reviewed HEAD 的自指 provenance。

本次确认：

- `.trellis/guru-team/extension.json` 已更新为 apply-time provenance：`source.commit=b94c4fb4e74ba032511fa9f5aa5b6bac6899737c`、`source.tree_state=dirty`
- installed manifest `notes` 明确说明 `source.commit` / `source.tree_state` 描述的是 apply 时观测到的 extension source，不声明该 installed manifest 被包含在同一 commit 中
- `README.md`、`.trellis/spec/workflow/data-contracts.md`、`design.md` 均同步说明 dogfood installed copy 是“上一次 apply 的安装事实”，canonical version 仍以 `trellis/guru-team-extension.json` 为准
- 该语义符合 installer recorder 边界：脚本记录事实，升级/回滚判断仍由 AI/human review 执行

## Docs SSOT

本任务改变 Guru Team extension 的长期安装、升级、排障和 provenance contract，已同步 durable docs 和用户入口文档：

- `README.md`：新增 Guru Team extension version 章节，区分 official Trellis CLI version、`.trellis/.version`、`trellis/index.json.version`、canonical extension version 和 installed manifest；安装/升级 prompt 要求报告 extension version/source provenance
- `trellis/presets/guru-team/README.md`：说明 installed manifest、`version.sh`、throwaway install 验证范围和当前分支 marketplace 限制
- `trellis/workflows/guru-team/README.md`：说明 workflow marketplace id 与 extension version/provenance 的关系
- `docs/requirements/requirement-main.md`：记录 #31 作为版本治理/安装可观测能力
- `.trellis/spec/preset/installer.md` 与 `.trellis/spec/workflow/data-contracts.md`：沉淀 reusable installer/data contract 规则，包括 installed manifest backward compatibility 和 apply-time provenance 语义

Docs SSOT reconciliation 结论：长期 contract 已回写 durable docs 和 `.trellis/spec/`，task artifact 仅保留本次执行和 gate evidence。

## Deployment Impact

本次 diff 未修改 `.github/workflows/*`、Dockerfile、Docker Compose、Kubernetes/Kustomize、Helm、数据库 migration/seed/backfill、Makefile 或应用 runtime entrypoint。

变更影响面是本仓库 Trellis extension marketplace/preset/companion scripts/docs。它会影响后续目标 repo 安装/升级时写入的 `.trellis/guru-team/extension.json` 和 `check-env` / `version.sh` 输出，不引入服务进程、API、worker、定时任务、队列消费者、数据库 schema 或部署配置变更。因此不需要同步部署资产。

## 安全判断

- manifest/provenance 记录 repo URL、ref、commit、tree state、selected platforms、managed asset list 和 install time；未记录 token、secret、private key、`.env`、signed URL、database URL、GitHub auth detail 或本机绝对 source path
- `source_tree_state=dirty` 是客观事实，不含 diff 内容
- `check-env --json` 会输出 repo root 和 worktree 列表，这是既有本地诊断行为；本任务新增的 `guru_team_extension` 节点不扩大 secret 暴露面
- public docs 仅包含安全检查提示和公开 repo/path 示例，未写入敏感凭据

## Findings

无 P0/P1/P2 finding。

## 非阻塞观察

- `verify-throwaway-install.sh` 在默认 public marketplace source 且当前分支非 `main` 时仍会 fail closed；本次使用 `TRELLIS_ALLOW_PUBLIC_MARKETPLACE_SAMPLE=1` 明确表示 public workflow sample + 当前本地 preset 验证，避免把未合并分支 marketplace 能力误报为已验证。
- `check.jsonl` / `implement.jsonl` 仍只有 seed 行；本次复审按 workflow fallback 读取 task artifacts 和相关 `.trellis/spec/`，未因此阻塞 gate。
- `review.md` 本身是 task metadata，当前工作区只需后续由主 session 记录/提交 gate metadata。

