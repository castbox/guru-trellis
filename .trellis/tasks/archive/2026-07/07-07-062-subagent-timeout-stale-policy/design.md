# #62 subagent timeout / stale 策略设计

## 目标与边界

本任务把 sub-agent 等待与终止策略提升为 Guru Team workflow 的显式合同：等待窗口 timeout 不是失败证据；只有无进展达到 stale 条件且记录证据后，主会话才可以 interrupt / terminate；未完成 agent 必须恢复或由继任 agent 接手；未闭环的中间输出不能成为 gate pass 证据。

实现边界保持在本仓库可维护扩展面内：

- Markdown workflow / skill / prompt / agent overlay 负责 AI 判断流程。
- companion script 只记录和校验客观字段。
- 不改 Trellis 官方包或 `node_modules`。
- 不把 active task state 放进 spec template marketplace。

## 官方文档承接

- 官方 custom workflow 文档说明 `.trellis/workflow.md` 控制 phase、skill routing、per-turn reminder，修改后 runtime 读取 Markdown 生效。因此 timeout/stale 判断规则应进入 `workflow.md` 与 overlay 入口。
- 官方 custom sub-agents 文档说明 shipped agents 为 `trellis-implement`、`trellis-check`、`trellis-research`，不同平台 agent 文件格式不同，缺少 hook 注入的平台通过 pull-based prelude 读取 JSONL 与 task artifacts。因此继任规则必须同步到 Codex/Cursor/Claude/channel runtime agent overlay，而不是只改一个平台。
- 官方 spec template marketplace 文档说明 spec template 只放可复用工程规范，不放 `.trellis/tasks/`、workspace 或平台 prompt 文件。本任务不修改 spec template marketplace 内容。

## Durable Docs SSOT

本任务影响长期 workflow 合同，需要同步 durable docs：

- `README.md`：日常使用与 sub-agent 规则摘要。
- `trellis/workflows/guru-team/README.md`：marketplace workflow 行为说明。
- `trellis/presets/guru-team/README.md`：preset 安装后的 agent / script 文件说明。
- `docs/requirements/requirement-main.md`：需求 SSOT 的能力矩阵与 issue 状态。
- `docs/requirements/guru-team-trellis-flow.md`：流程图与 artifact 说明。

## 数据合同

在 `agent-assignment.json` 增加 `status_events[]`，作为 task-local sub-agent 状态处理事件 ledger。它记录 AI/human 已做出的观察和处理决策，不替代判断。

建议事件结构：

```json
{
  "event": "wait-timeout",
  "logical_role": "实现代理",
  "agent_id": "technical-agent-id",
  "platform_nickname": "display-only",
  "head": "<git-head>",
  "observed_at": "2026-07-07T00:00:00Z",
  "last_observed_progress_at": "2026-07-07T00:00:00Z",
  "workspace_evidence": "中文说明 git status / diff / channel event / output 观察",
  "running_command_evidence": "中文说明仍在运行、已卡住或不适用",
  "decision": "continue-waiting",
  "reason": "中文 AI/human 判断依据",
  "supersedes_agent_id": "",
  "handoff_summary": ""
}
```

候选 `event`：

- `wait-timeout`：等待窗口超时，默认不代表失败。
- `progress-observed`：观察到输出、diff、验证命令或 channel event 仍在推进。
- `stale-assessed`：完成 stale 评估，记录最近进展与工作区证据。
- `continue-waiting`：决定继续等待当前 agent。
- `resume-same-agent`：恢复同一 technical agent / session。
- `replacement-started`：启动继任 agent。
- `terminated-unfinished`：终止了未完成 agent。
- `completed`：agent 完成当前逻辑角色。
- `failed`：agent 明确失败且无法继续。

候选 `decision`：

- `continue-waiting`
- `resume-same-agent`
- `start-replacement`
- `terminate-unfinished`
- `mark-completed`
- `mark-failed`

校验边界：

- recorder 校验 JSON root、枚举、`logical_role`、HEAD、`reason`、`head`、`status_events[]` 数组结构。
- 对 `terminated-unfinished` 这类高风险事件，validator 可客观要求事件包含 `last_observed_progress_at`、`workspace_evidence`、`running_command_evidence`、`handoff_summary`。
- Branch Review Gate pass 前，若 `status_events[]` 中存在未被后续 `resume-same-agent`、`replacement-started`、`completed` 或 `failed` 解释的 `terminated-unfinished`，脚本应 fail closed。该判断是客观 ledger 完整性校验，不判断是否应该终止。

## Workflow 规则

在 `Sub-agent Boundary` 与 Phase 2 / Phase 3 规则中增加：

1. `wait_agent` / `trellis channel wait` timeout 只是等待窗口结束。
2. stale 判断默认至少需要 5 分钟无可观察进展；有输出、diff、验证命令、channel event 或合理工作区变化时继续等待。
3. interrupt / terminate 前记录 status event。
4. replacement 必须接收：
   - `Active task: <task path>`
   - 前任输出或 channel log 摘要
   - 当前 git diff / dirty paths
   - `prd.md` / `design.md` / `implement.md`
   - `implement.jsonl` 或 `check.jsonl`
   - 剩余 checklist 与阻塞 gate
5. Phase 2 pass 与 Branch Review Gate pass 必须确认没有未完成/被终止且未继任闭环的 sub-agent 输出被当成完成证据。

## Overlay 同步

需要同步：

- shared skill: `trellis-continue`
- Codex skill/prompt: `.codex/skills/trellis-continue/SKILL.md`、`.codex/prompts/trellis-continue.md`
- Claude/Cursor continue commands
- Codex/Cursor/Claude implement/check agent overlay
- channel runtime `.trellis/agents/implement.md` / `check.md`

原则：overlay 不复制完整 workflow，只保留短规则并指向 `.trellis/workflow.md`；agent 文件强调“完成前不要报告 complete；被中断/失败时列出剩余工作、当前 diff 和继任 handoff 所需信息”。

## 兼容性

- `agent-assignment.json` schema 采用 additive 字段；旧 artifact 缺少 `status_events` 时 loader 补空数组。
- 对没有 sub-agent 状态事件的普通任务，现有 assignment / review round 规则不变。
- 对已安装目标仓库，preset apply 会更新 managed companion script 和 overlay；本仓库 dogfood copy 通过 apply 同步。

## 风险与回滚

- 风险：过度脚本化 stale 判断会违反“脚本不做 reviewer/planner 判断”边界。
  - 缓解：脚本只校验事件是否存在、字段是否完整、未完成终止是否有后续闭环事件。
- 风险：只更新 canonical workflow 不更新 overlay，导致新项目或平台入口仍沿用旧规则。
  - 缓解：修改 canonical 后运行 preset apply 和 dogfood overlay drift check。
- 风险：新 status event 参数过复杂，主会话不愿记录。
  - 缓解：保留单一 `record-agent-assignment` 子命令，新增 status-event 模式，字段使用文本 evidence，不引入复杂外部状态采集。

## 非适用项

- 不涉及部署资产、CI/CD、容器、Kubernetes、DB migration 或 Makefile 运行形态变化。
- 不涉及 middle-platform SDK。
