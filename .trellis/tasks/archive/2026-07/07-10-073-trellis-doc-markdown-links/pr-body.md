## 变更摘要

将 `AGENTS.md` 中“官方 Trellis 优先”小节的 3 条 Trellis 官方文档链接改为 markdown 端点：

- `https://docs.trytrellis.app/` -> `https://docs.trytrellis.app/index.md`
- `https://docs.trytrellis.app/advanced/custom-workflow` -> `https://docs.trytrellis.app/advanced/custom-workflow.md`
- `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace` -> `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`

这样 AI Agent 读取本仓库指令里的 Trellis 官方文档时，可以直接访问低噪音 markdown 内容，不需要先抓 HTML 页面再切换到 markdown 文档。

## 影响范围

- 影响文件：`AGENTS.md`
- 影响行为：仅影响 AI Agent 读取官方 Trellis 文档链接时的入口 URL。
- 不影响范围：未修改 workflow、preset、marketplace、overlay、companion scripts、schema、平台入口、CI/CD、容器、K8s/Kustomize、数据库 migration、Makefile。

## 验证结果

- `rg -n "https://docs\\.trytrellis\\.app" .`：所有可见 Trellis 官方文档页面链接均为 `.md` 端点。
- `rg -n 'https://docs\.trytrellis\.app/($|[[:space:]])|https://docs\.trytrellis\.app/advanced/(custom-workflow|custom-spec-template-marketplace)([^.]|$)' AGENTS.md`：无输出，确认 `AGENTS.md` 不再保留本次范围内的 HTML 形式链接。
- `git diff --check`：通过。
- `curl -I -L -s`：`index.md`、`advanced/custom-workflow.md`、`advanced/custom-spec-template-marketplace.md` 均返回 `HTTP 200` 且 `content-type: text/markdown`。

## Review Gate

- Phase 2 check 已覆盖 requirements、design、code/docs、tests、spec sync、cross-layer、Docs SSOT、deployment，`findings=[]`。
- Branch Review Gate 已由独立最终放行审查代理审查 `origin/main...HEAD`，审查 HEAD 为 `04741e2b3fe6ef945cab933e642b7d8c167d6d6e`，`findings_count=0`。
- 已确认本次 committed diff 只有 `AGENTS.md`，内容为 3 个 URL 字面量替换。

## 文档同步

- docs_state：`complete_docs`
- strategy：`ssot_first`
- durable docs：`AGENTS.md`
- durable_docs：`AGENTS.md`
- durable_docs_updated：`AGENTS.md`
- task_delta_merged：3 条 Trellis 官方文档入口改为 markdown 端点。
- task-history-only：issue 范围、链接映射、验证命令、Phase 2 check、Branch Review Gate 证据。
- task_history：issue 范围、链接映射、验证命令、Phase 2 check、Branch Review Gate 证据。
- task_history_only：issue 范围、链接映射、验证命令、Phase 2 check、Branch Review Gate 证据。
- spec_update：未修改 `.trellis/spec/` 正文；因为没有新增工程约定、流程规则或可复用行为模式。
- followup_or_limitation：无当前 PR 必需 follow-up；本次不修改 workflow、preset、marketplace、overlay 或 installer，因此不触发完整 throwaway 安装验收。

## Issue 关闭范围

Closes #73

`issue-scope-ledger.json` 中 `close_issues` 仅包含 #73；没有 `related_issues` 或 `followup_issues`。

## 安全说明

本次 diff 只包含公开 Trellis 官方文档 URL，不包含 token、secret、private key、签名 URL、`.env`、数据库 URL 或客户数据。

## 开箱即用与 upgrade/update

本次没有修改 workflow、preset、marketplace、overlay、companion scripts 或安装器，因此不触发完整 throwaway 安装验收。已验证的是静态链接扫描与目标 markdown URL 可访问性；后续 `trellis upgrade` / `trellis update` 不需要为本次链接替换执行额外迁移。
