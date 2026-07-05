## 变更摘要

- 新增 Trellis subagent assignment ledger：通过 `agent-assignment.json` 记录中文 `logical_role`、稳定 `agent_id`、平台展示昵称、HEAD/digest、审查轮次和复用决策。
- 新增 `record-agent-assignment.sh` 与 `check-agent-assignment.sh`，并让 `review-branch --agent-assignment` 把 assignment ledger digest 固化到 Branch Review Gate。
- 同步 canonical workflow/preset overlay 与 dogfood 安装副本，让 Codex、Cursor、Claude 和 `.trellis/agents` 的 UI 描述、角色标题和工作流文案使用中文逻辑角色。
- 保留技术调度 ID 的稳定性：`trellis-implement`、`trellis-check`、`trellis-research` 和 channel `implement/check` 继续使用英文；Codex `nickname_candidates` 的 ASCII 限制已写入文档，中文名称通过 `description` 与 ledger `logical_role` 表达。

## 影响范围

- 影响 Trellis guru-team workflow、preset installer、平台 overlay、task metadata schema、review gate recorder/validator、README 和 `.trellis/spec/` 规范文档。
- 不改变官方 Trellis 上游源码、全局 npm 包或 `node_modules`；流程判断仍由 Markdown workflow/skill 承载，脚本只执行记录、校验和确定性文件操作。
- preset overlay 已重新应用到 dogfood 副本，`check-dogfood-overlay-drift.sh` 确认 canonical overlay 与当前安装副本一致。
- 未修改 `.github/workflows`、Docker/Compose、K8s/Helm/Kustomize、数据库 migration、Makefile 或 runtime config。

## 验证结果

- `python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：80 tests passed。
- `python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`：18 tests passed。
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-43-trellis-subagent`：通过。
- `check-agent-assignment.sh --require-current-head`、`check-planning-approval.sh --allow-committed-head`、Phase 2 check relaxed validation、`check-dogfood-overlay-drift.sh`、`git diff --check origin/main...HEAD`：均通过。
- 开箱即用抽样验证已覆盖 public marketplace workflow sample 与 local preset apply；未用远端 `gh:castbox/guru-trellis/trellis` 验证本分支内容，因为该实现尚未发布到远端默认分支。

## Review Gate

- Branch Review Gate 已按 `origin/main...HEAD` 审查，reviewed HEAD 为 `26185a6b3098c0fa7e6e4051043ca3829f07e9ea`。
- 独立 `trellis-check` 审查代理 Volta 覆盖 workflow、dogfood workflow、companion scripts、assignment ledger、review gate digest、post-commit metadata audit、Codex/Cursor/Claude/.trellis overlay、README/docs/spec/task artifacts。
- 审查结论：P0/P1/P2/P3 findings 均为无；Docs SSOT、部署影响和 preset/overlay drift 证据已记录在 `review.md` 与 `review-gate.json`。

## Issue 关闭范围

- Closes #43：本 PR 完成“规范 Trellis subagent 中文逻辑角色与复用记录”的范围，包含中文 UI 展示名、复用记录、审查证据固化和文档同步。
- 本次没有关联 issue 或 follow-up issue；不关闭其他 issue。

## 安全说明

- 本次不处理 token、secret、private key、签名 URL、`.env`、数据库 URL 或客户数据。
- 新增 artifact 只记录 subagent 身份、逻辑角色、HEAD/digest、审查轮次与复用决策，不包含敏感凭据。
- PR 不引入部署资产、运行时配置或数据库变更；发布影响集中在 Trellis workflow/preset/overlay 与 companion scripts。
