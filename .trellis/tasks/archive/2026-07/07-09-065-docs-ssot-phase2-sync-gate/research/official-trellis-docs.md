# 官方 Trellis 文档核对

## 核对来源

- https://docs.trytrellis.app/advanced/custom-workflow
- https://docs.trytrellis.app/advanced/custom-spec-template-marketplace

## 结论

- Guru Team workflow 行为应继续通过 `.trellis/workflow.md`、marketplace workflow、platform overlay、skill/prompt/agent Markdown 入口表达。
- 本任务不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- `.trellis/spec/**` 只沉淀可复用 workflow / preset / docs 维护规范，不放 active task、PR runtime state 或项目私有业务状态。
- #65 的 `Docs SSOT Plan` Phase 2 消费规则属于 AI implementation/check 判断合同，应写入 Markdown workflow / overlays / docs / specs，而不是写入 Python / shell 判断 docs 语义充分性。

## 命令证据

Python `urllib` 在本机因 CA 证书链报 `CERTIFICATE_VERIFY_FAILED`，随后使用 `curl -k -L` 对同一官方 URL 读取公开页面并确认页面包含 custom workflow / workflow.md 与 custom spec template marketplace 相关内容。
