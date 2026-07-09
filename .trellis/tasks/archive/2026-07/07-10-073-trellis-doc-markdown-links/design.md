# #73 设计：Trellis 官方文档链接改为 markdown 端点

## 设计目标

在不改变 Guru Team Trellis 流程语义的前提下，把仓库内仍指向 Trellis 官方 HTML 页的入口改为 markdown 端点，使 AI Agent 读取官方文档时直接获取低噪音 markdown 内容。

## 输入证据

- GitHub issue #73 要求项目内 Trellis 官方文档链接一步到位指向 markdown 格式。
- 仓库扫描命令：

```bash
rg -n "https://docs\\.trytrellis\\.app" .
```

- 当前命中：
  - `AGENTS.md:11` 首页 HTML 链接
  - `AGENTS.md:12` custom workflow HTML 链接
  - `AGENTS.md:13` custom spec template marketplace HTML 链接
  - `docs/requirements/guru-team-trellis-flow.md:419-422` 已为 `.md` 链接
- 官方索引 `https://docs.trytrellis.app/llms.txt` 已列出 markdown 文档端点。
- `curl -I -L -s` 已确认目标 markdown URL 返回 markdown 内容类型。

## 链接映射

| 文件 | 原链接 | 新链接 | 原因 |
| --- | --- | --- | --- |
| `AGENTS.md` | `https://docs.trytrellis.app/` | `https://docs.trytrellis.app/index.md` | 首页 markdown 端点返回 `text/markdown` |
| `AGENTS.md` | `https://docs.trytrellis.app/advanced/custom-workflow` | `https://docs.trytrellis.app/advanced/custom-workflow.md` | 官方 `llms.txt` 暴露该 markdown 文档 |
| `AGENTS.md` | `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace` | `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md` | 官方 `llms.txt` 暴露该 markdown 文档 |

## 变更边界

- 只编辑 `AGENTS.md` 的 3 个 URL 字面量。
- 不改变标题、段落、门禁规则、流程说明。
- 不触碰 `trellis/workflows/`、`trellis/presets/`、`.agents/skills/`、`.codex/`、`.trellis/spec/`。
- 不新增迁移脚本，因为目标是静态链接文本。

## Docs SSOT Plan

- docs state: `complete_docs`
- strategy: `ssot_first`
- durable docs source: `AGENTS.md`
- checked specs:
  - `.trellis/spec/docs/index.md`
  - `.trellis/spec/docs/public-docs.md`
  - `.trellis/spec/guides/index.md`
  - `.trellis/spec/guides/code-reuse-thinking-guide.md`
  - `.trellis/spec/guides/cross-layer-thinking-guide.md`
- affected durable docs:
  - `AGENTS.md`
- task artifact delta:
  - `prd.md` 记录 issue 范围、验收标准和官方 URL 证据。
  - `design.md` 记录 URL 映射和 docs SSOT 方案。
  - `implement.md` 记录执行顺序与验证命令。
- merge checkpoint: 实现阶段必须先更新 `AGENTS.md`，再记录 task artifact 验证证据。
- task-history-only content: 规划证据、扫描命令输出摘要、门禁记录保留在 task artifact 中，不复制到 `AGENTS.md`。

## Middle-platform Knowledge Gate

- 结论：不适用。
- 理由：本任务只修改 Trellis 官方文档链接文本，不涉及 go-guru、proto-guru、Unity3D Guru SDK、Flutter Guru SDK 或中台框架契约。

## 开箱即用与 upgrade/update 影响

- 本任务不修改 workflow、preset、marketplace、overlay、companion scripts、schema、安装器或平台入口。
- 因此不触发完整 throwaway 安装验收。
- 验证重点必须放在静态链接扫描、目标 URL markdown 内容类型、`git diff --check`。

## 风险与回滚

- 主要风险：错误推断首页 markdown 端点。缓解：用 `curl -I -L -s https://docs.trytrellis.app/index.md` 验证 `200` 和 `text/markdown`。
- 主要风险：漏改其他 HTML 链接。缓解：实现前后都运行 `rg -n "https://docs\\.trytrellis\\.app" .`。
- 回滚方式：还原 `AGENTS.md` 的 3 个 URL 字面量。
