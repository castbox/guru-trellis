# 用 task-local finish-summary 替代 workspace journal/add_session

## 变更摘要

- Guru Team `finish-work` 不再调用官方 `add_session.py`，也不再读写 `.trellis/workspace/**`。
- 新增严格的 `finish-summary.json` schema、AI index 输入、recorder 与 Python validator，完成摘要随当前 task archive 保存。
- PR 发布采用初始空 URL 摘要和单 task metadata tail 两阶段写入；recovery 按 query-first 的 `0/1/>1` open PR 状态机执行。
- raw Git paths 先排序去重，再过滤 `.trellis/workspace/**` 与 `.trellis/.runtime/**`；安全集合同时写入两个 path 字段，过滤事实使用固定且不泄露路径的 contract record。
- Shared `trellis-start` 与 Codex/Cursor session-start 不再打开、枚举或输出 workspace journal；发布恢复输入由 task-local immutable `pr-readiness.json` 绑定。
- Git path snapshot 命令失败时两个 path 数组统一降级为空并记录固定、非披露 unavailable fact；throwaway update 后重新应用 marketplace workflow 与 preset，再执行最终 sidecar gate。
- 修复真实 formal finish 暴露的 path identity 冲突：合法 Git paths 按 exact string 去重，非路径语义文本继续按 normalized identity 检查。

## 影响范围

- Canonical workflow、companion scripts、finish-summary 与 marketplace verification schema。
- Guru Team preset installer、配置模板、ignore 策略、shared start、Codex/Cursor session hooks、Codex/Claude/Cursor continue/finish entries 和 dogfood 安装副本。
- Root/workflow/preset README、requirements 与 `.trellis/spec/` durable contracts。
- 本仓库三个 tracked workspace journal/index 文件从 Git tracking 删除；官方 Trellis workspace 能力和上游脚本保持不变。

## 验证结果

- Canonical tests：305 项通过，Python compile 后重跑仍为 305 项通过。
- Preset installer tests：36 项通过。
- PublishBoundary + FinishSummary 定向 tests：82 项通过。
- 无 site-packages finish-summary tests：34 项通过，1 项仅因 optional `jsonschema` 不存在而跳过。
- Python compile、Guru Team Bash syntax、251 个 tracked JSON 及 task-local JSON、task/planning/workspace boundary、overlay drift、6 组 canonical/dogfood byte equality、sidecar scan 与 `git diff --check` 全部通过。
- 真实 collision fixture 同时保留 `.trellis/guru-team/extension.json` 与 `trellis/guru-team-extension.json`，两个 summary path 字段通过 Python validator 与 JSON Schema 校验。
- Public-main sampling throwaway 完成 preview cleanup、initial workflow switch、`trellis update --force`、marketplace workflow reapply、preset reapply、shared-start workspace access audit 与最终 `.new/.bak` gate。
- Commit 后 `git ls-files '.trellis/workspace/**'` 为空，base-to-HEAD diff 保留三个预期删除记录。

## Review Gate

- Formal finish collision 修复后的 fresh 独立 Phase 2 check 已覆盖完整 `origin/main...HEAD` 与 4 个 tracked working paths；current-scope P0/P1/P2/P3 均为零。
- Branch Review Gate 必须继续以 `origin/main...HEAD` 为固定范围，覆盖文档、代码、测试、Trellis artifacts、配置、脚本、schema、preset/overlay、发布 readiness、CI/CD、容器、Kubernetes/Kustomize、数据库 migration 与 Makefile 影响。
- PR 只能在 `review-gate.json` 对当前 HEAD 有效、全部 P0/P1/P2/P3 finding 为零且 publish validators 通过后，由显式 `trellis-finish-work` 入口创建。
- 当前分支尚未 push；真实 current-ref remote marketplace verifier 必须在 `gh pr create` 前运行并把 pending ledger evidence 替换为 passed evidence。

## Issue 关闭范围

Closes #97

Related #53
Related #96
Related #100

后续 #98 和 #99 不由本 PR 关闭。

## 文档同步

- Docs SSOT strategy 为 `ssot_first`；canonical workflow、workflow/data/companion/preset specs、README 与 requirements 已先于最终实现同步。
- 方案 A 的 protected-path filtering、snapshot-unavailable 降级、immutable readiness、两阶段 publish、`0/1/>1` recovery、marketplace evidence reuse、no-workspace context 和 update/reapply sidecar gate 已写回 durable docs。
- Path identity 合同已写回 data contracts：所有 path-bearing arrays 使用 exact string identity，非路径语义数组继续使用 normalized text identity。
- Task artifact 仅保留规划审批、旧 blocker、sub-agent liveness、Phase 2 check 与临时 throwaway 证据等任务历史。
- 后续 / 当前 PR 限制：历史 task backfill、基于摘要的历史搜索和 developer identity 解耦不在本 PR；current-ref remote marketplace verifier 必须在正式 push 后完成。

## 安全说明

- 不包含 token、secret、private key、签名 URL、`.env`、数据库 URL、客户数据或 workspace journal 内容迁移。
- 不新增服务、API、后台任务、数据库 schema/migration、容器、Kubernetes/Kustomize、CI/CD 或 Makefile 运行入口，无业务部署步骤。
- 变更会影响 Guru Team workflow/preset 安装与发布元数据流程；remote marketplace verification 仍是创建 PR 前的 fail-closed 门禁。
- 默认 pinned `v0.6.5-guru.3` 尚未发布，本任务不创建 release tag；正式 publish 必须改用已 push current-ref 运行 remote marketplace verifier。
