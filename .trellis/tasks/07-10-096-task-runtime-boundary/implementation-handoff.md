# 实现代理交接

## 身份与范围

- 实现代理：`019f4b63-b84b-7091-90a0-e108488589ec`（Build Agent）
- 工作区：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/096-task-runtime-boundary`
- 任务：`.trellis/tasks/07-10-096-task-runtime-boundary`
- 执行边界：完成 Issue #96 实现与实现期验证；未执行 `trellis-check`、Phase 2 recorder、commit、push、PR 或 Branch Review Gate。

## Docs SSOT 承接

- Strategy：`ssot_first`。
- Durable primary inputs：`trellis/workflows/guru-team/workflow.md`、`trellis/workflows/guru-team/schemas/task-start-context.schema.json`。
- Durable sync result：已同步 `.trellis/spec/workflow/**`、`docs/requirements/**`、仓库/marketplace/preset README、canonical overlays 和 dogfood installed copies。
- Task delta merged：任务启动上下文、本机运行态、workspace boundary、obsolete managed artifact 清理合同已合并到 durable workflow/schema/spec/docs。
- Task-history-only：`prd.md`、`design.md`、`implement.md`、`research/*.md`、planning approval、agent assignment 和本交接记录仅作为任务审计历史，不复制到公共 marketplace/spec template。
- Follow-up / limitation：实现代理报告固定 tag `v0.6.5-guru.3` 不存在，当前分支远端 marketplace 内容在 commit/push 前无法通过该 tag 验证；本地 canonical preset 与公开 main marketplace 组合验证通过，但不能替代当前分支远端 marketplace 验证。

## 实现完成项

- 新增严格 portable `task-start-context.json` writer/loader/validator 和 schema。
- 新增 `.trellis/.runtime/guru-team/workspaces|tasks/*.json` local-only mappings。
- 迁移 workspace boundary、planning/check/review/finish/publish 下游读取路径。
- 删除旧 `.trellis/guru-team/handoff.json`、`intake-handoff.schema.json`、`handoff_path` config/public API。
- preset installer 增加 obsolete managed file 安全清理：未修改 managed copy 删除；用户修改副本保留并报告冲突。
- preset installer 管理 `.trellis/.runtime/` ignore，canonical overlays 已 apply 到 dogfood。

## 实现期验证

- canonical unit tests：227 项通过（含 Round 1 SHA/verifier 回归）。
- preset installer tests：30 项通过；obsolete clean fixture 不依赖 Git history。
- JSON、shell syntax、Python compile、task validation、phase context、workspace boundary、dogfood drift、`git diff --check` 通过。
- throwaway preset 安装通过，新安装含 runtime ignore、不含旧 handoff/schema、包含新 schema。
- 无遗留 `.new` / `.bak`。

## Phase 2 检查重点

- portable context forbidden-key / absolute-path 扫描。
- cache 删除后的 `git worktree list` 重建。
- finish/publish workspace boundary 执行顺序。
- 普通 task 写入 allowlist 与并行 task 隔离。
- obsolete cleanup 的未修改删除和用户修改 fail-safe 双路径。
- canonical/dogfood/docs/overlay 一致性及 marketplace 当前分支验证限制。

## Branch Review Round 1 修复

- Finding 1：`build_task_start_context()` 改读 producer 的 `local_head_after` / `remote_head`；writer 对 `fresh`、`remote_only`、`fetch_failed` 状态执行 fail-closed SHA 约束，并新增三类数据流测试。
- Finding 2：obsolete schema 内容固化为 `trellis/presets/guru-team/scripts/python/fixtures/intake-handoff.schema.json`，测试不再读取 `git show HEAD:`，clean clone 当前 commit 可独立复现。
- Finding 3：新增 `verify-marketplace` companion command、`marketplace-verification.schema.json` 与 publish fail-closed 数据流。公共 marketplace/preset 变更发布时执行：push reviewed content HEAD → remote branch init → preview → switch → clone 已 push 的 remote branch → 从该 clone 执行 canonical preset reapply → 记录命令结果与 digest → metadata-only commit/push verification artifact → 校验 artifact/current HEAD/remote HEAD → `gh pr create`。任何步骤失败、artifact 缺失或 stale 都在创建 PR 前阻断；不创建 tag。AI 继续负责 PR readiness 判断，脚本只执行/记录/校验确定性事实。
- Finding 4：`issue-scope-ledger.json` 已按 Issue #96 十项验收写入真实文件/命令/结果。远端 marketplace 项明确要求由真实 push 后 `marketplace-verification.json` 补齐并由 publish validator 校验，当前未写 passed。

## Round 1 后验证计划

- core/preset unit tests、JSON/schema、shell syntax、Python compile。
- `apply.sh --repo . --all-platforms`、dogfood drift、`.new/.bak`、task validation、workspace boundary、`git diff --check`。
- 不执行真实 push；远端 verifier 的真实执行点保留在 formal `finish-work` / `publish-pr`，届时缺失或失败会阻止 PR 创建。
