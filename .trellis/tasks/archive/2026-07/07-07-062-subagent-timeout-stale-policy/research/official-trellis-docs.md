# 官方 Trellis 文档核对

核对时间：2026-07-07

## 已核对页面

- `https://docs.trytrellis.app/index.md`
- `https://docs.trytrellis.app/advanced/custom-workflow.md`
- `https://docs.trytrellis.app/advanced/custom-agents.md`
- `https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md`
- `https://docs.trytrellis.app/llms.txt`

## 结论

- Trellis 的核心概念包括 Spec、Workspace、Task、Skill、Sub-agent、Command、Hook、Journal；本任务属于 workflow / sub-agent / command overlay 扩展，不属于业务代码改动。
- custom workflow 文档明确 `.trellis/workflow.md` 是 phase、skill routing 与 per-turn workflow-state 的 Markdown 控制面；修改 workflow 行为不需要改 Python hook 逻辑或重新发布 Trellis 官方包。
- custom sub-agents 文档明确 shipped sub-agent 包括 `trellis-implement`、`trellis-check`、`trellis-research`，不同平台 agent 文件格式不同；缺少 hook 注入的平台通过 pull-based prelude 读取 JSONL、`prd.md`、`design.md`、`implement.md`。因此本任务需要同步各平台 agent overlay 与 continue 入口。
- custom spec template marketplace 文档明确 spec template marketplace 适合复用工程规范、API/测试/发布规则和 review checklist，不应作为 remote task store，也不应包含 `.trellis/tasks/`、workspace 或平台 prompt 文件。本任务不会把 timeout/stale active task 状态写入 spec marketplace。

## 对本任务的约束

- AI 判断流程写入 `workflow.md`、skills/prompts/commands/agent overlay。
- companion script 只记录和校验 status event artifact，不判断是否卡死。
- `agent-assignment.json` 的新增状态事件属于 task-local runtime evidence，不属于 spec template marketplace。
