# 官方 Trellis 文档核对

## 核对来源

- https://docs.trytrellis.app/
- https://docs.trytrellis.app/advanced/custom-workflow
- https://docs.trytrellis.app/advanced/custom-spec-template-marketplace

## 抓取方式

- Python `urllib.request` 访问官方站点时触发本机证书校验失败：`CERTIFICATE_VERIFY_FAILED`。
- 随后使用 `curl -L` 抓取页面；HTML 中存在 Markdown alternate 链接：
  - `/advanced/custom-workflow.md`
  - `/advanced/custom-spec-template-marketplace.md`
- 使用上述 Markdown URL 读取正文作为规划依据。

## 结论

- `custom-workflow` 文档确认 `.trellis/workflow.md` 是 Trellis workflow 行为的集中定义；phase、skill routing、per-turn reminders 和 `task.py` command catalog 都在这个 Markdown 文件中。
- `[workflow-state:STATUS]` block 由 hook 在用户提示时解析，hook 是 parser-only；因此本任务的阶段回复要求应写入 workflow / skill / prompt Markdown，不应通过改 hook 或 Trellis upstream 代码实现。
- 官方文档还要求 workflow 修改后 AI 下次 session / turn 通过读取 Markdown 生效，不需要重新发布 Trellis。
- `custom-spec-template-marketplace` 文档确认 spec template marketplace 适合 reusable engineering conventions、testing rules、release rules、review checklists 和去敏例子；不应用作 remote task store，也不应放 `.trellis/tasks/`、workspace、active task state 或平台 prompt 文件。

## 对本任务的设计影响

- 路径解析和存在性检查可以落在 companion script，因为这是 deterministic fact。
- “每个阶段结束回复必须输出 Markdown review 表”属于 AI workflow 行为，必须写入 canonical workflow 和平台 overlay。
- 本任务不改 spec template marketplace；只需确保不会把 task artifact 或平台 prompt 规则误放进 spec template。
