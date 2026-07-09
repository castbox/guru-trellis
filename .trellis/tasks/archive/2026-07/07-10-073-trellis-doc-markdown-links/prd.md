# #73 将项目里的 trellis 官方文档链接的 html 地址替换为 markdown 格式的地址

## 目标

将仓库内仍指向 Trellis 官方 HTML 页面的文档链接替换为对应 markdown 端点，减少 AI Agent 先访问 HTML、再访问 markdown 的重复读取。

## 需求来源

- GitHub issue: https://github.com/castbox/guru-trellis/issues/73
- issue 标题：将项目里的 trellis 官方文档链接的 html 地址替换为 markdown 格式的地址
- issue 内容：HTML 内容噪音过多，AI Agent 访问 HTML 页面后还要再访问 markdown 文档，本任务必须让项目内 Trellis 官方文档入口一步到位指向 markdown。

## 当前证据

- `rg -n "https://docs\\.trytrellis\\.app" .` 显示 `AGENTS.md` 仍有 3 条 HTML 形式链接：
  - `https://docs.trytrellis.app/`
  - `https://docs.trytrellis.app/advanced/custom-workflow`
  - `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace`
- `docs/requirements/guru-team-trellis-flow.md` 的 Trellis 官方文档链接已经使用 `.md` 端点，必须保持不变。
- 官方 `https://docs.trytrellis.app/llms.txt` 列出 Trellis 文档 markdown 端点，其中包含 `advanced/custom-workflow.md` 和 `advanced/custom-spec-template-marketplace.md`。
- `curl -I -L -s` 已确认以下目标 URL 返回 `200` 且 `content-type: text/markdown`：
  - `https://docs.trytrellis.app/index.md`
  - `https://docs.trytrellis.app/advanced/custom-workflow.md`
  - `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`

## 范围

### 必须修改

- `AGENTS.md` 中“官方 Trellis 优先”小节的 3 条 Trellis 官方文档链接：
  - 首页链接必须改为 `https://docs.trytrellis.app/index.md`
  - custom workflow 链接必须改为 `https://docs.trytrellis.app/advanced/custom-workflow.md`
  - custom spec template marketplace 链接必须改为 `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`

### 不在范围

- 不修改 Trellis workflow、preset、overlay、companion scripts、schema、平台入口、`.trellis/spec/` 规范正文。
- 不修改已经使用 `.md` 端点的链接。
- 不重写 `AGENTS.md` 的流程规则、门禁规则、发布规则。
- 不新增脚本或自动重写工具。

## 约束

- 修改前必须基于当前 worktree 里的实际文件扫描结果，不得凭记忆批量替换。
- 链接显示文字和周围中文说明必须保持语义不变。
- 本任务只处理 `https://docs.trytrellis.app` 官方文档链接；其他域名不得变更。
- 任务完成后必须重新扫描仓库，确认没有新增或遗漏的 Trellis 官方 HTML 形式链接。
- 安全边界：不得输出 token、secret、private key、签名 URL、`.env`、数据库 URL 或敏感数据。

## 验收标准

- [ ] `AGENTS.md` 的 3 条 Trellis 官方文档链接全部指向 markdown 端点。
- [ ] `rg -n "https://docs\\.trytrellis\\.app" .` 输出中，所有 Trellis 官方文档页链接均以 `.md` 结尾，`llms.txt` 若出现则作为索引端点处理。
- [ ] 针对 `AGENTS.md` 的 HTML 形式链接检查命令无命中：

```bash
rg -n 'https://docs\.trytrellis\.app/($|[[:space:]])|https://docs\.trytrellis\.app/advanced/(custom-workflow|custom-spec-template-marketplace)([^.]|$)' AGENTS.md
```

- [ ] 目标 markdown URL 可访问性验证返回 `200` 和 `content-type: text/markdown`。
- [ ] `git diff --check` 通过。

## Docs SSOT 状态

- 状态：`complete_docs`
- 证据：`AGENTS.md` 是本仓库 AI Agent 通用指令入口；`.trellis/spec/docs/public-docs.md` 定义公开文档语言、SSOT 与验证要求；本任务不改变 workflow 行为合同。
- 需求影响：本任务直接更新 durable instruction source `AGENTS.md`，task artifact 只记录范围、证据与验收，不作为长期文档来源。
