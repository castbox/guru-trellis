# 设计：Branch Review Gate finding 全阻断与 fresh final reviewer

## 总体设计

本任务保留现有 Guru Team 架构边界：Markdown workflow 决定 AI 流程与判断，`guru_team_trellis.py` 只作为 companion recorder / validator。实现分三层：

1. **Workflow 合同层**：把 Branch Review Gate 改为任何 finding 阻断；明确 `finding`、`observation`、`followup_candidate` 的语义；要求 finding owner 必须先做同 agent 闭环确认到 0 findings，最终放行必须来自之后启动的 fresh `最终放行审查代理`。
2. **Artifact / CLI 层**：`review-branch` 支持记录 observations 和 followup candidates；`review-gate.json` 记录三类条目与计数；passing path 校验任意 finding、final review round、current HEAD 和 fresh reviewer 客观字段。
3. **安装/运行副本层**：canonical workflow、preset overlay、dogfood installed copies、spec 和 durable docs 同步，避免安装新仓库或 dogfood 仓库读取旧语义。

## Artifact 合同

`review-gate.json` 保持 `schema_version: "1.0"`，在现有结构上追加字段以兼容旧 artifact：

- `findings`: 仍为数组，但任何非空 finding 都使 `conclusion.passed=false`。
- `observations`: 新增数组，记录非阻断观察。
- `followup_candidates`: 新增数组，记录 scope 外后续候选。
- `conclusion.blocking_findings_count`: 改为任意 finding 数量。
- `conclusion.findings_count`: 新增任意 finding 数量。
- `conclusion.observations_count`: 新增 observation 数量。
- `conclusion.followup_candidates_count`: 新增 followup candidate 数量。
- `verification_evidence.agent_assignment`: 继续记录 digest 和 review round summary；`--pass` 必须提供该 artifact，脚本校验 closure-before-final 和 fresh final reviewer 客观条件。

`agent-assignment.json` 暂不升级 schema，复用现有 `review_rounds[]` 字段：

- `round`: 必须唯一，并按记录顺序严格递增，确保最终放行 round 可被唯一判定为最后一轮。
- `logical_role`: `问题闭环审查代理` 表示 finding owner 闭环确认 round，`最终放行审查代理` 表示最终放行 round。
- `reviewed_head`: 必须等于当前 HEAD。
- `findings_count`: 闭环和最终放行必须为 0。
- `agent_id`: 最终 agent 不能出现在 earlier finding rounds 中。
- `reuse_decision`: 闭环使用 `reuse-for-closure`，最终放行使用 `new-agent`，不接受 `reuse`。

## CLI 设计

新增/调整参数：

- `review-branch --observation "message[|path]"`
- `review-branch --observations-file <json>`
- `review-branch --followup-candidate "message[|path]"`
- `review-branch --followup-candidates-file <json>`
- `--finding` 与 `--findings-file` 保持不变。

解析规则：

- `finding` 必须带 `priority`，支持 P0/P1/P2/P3。
- `observation` 和 `followup_candidate` 不带 priority，不进入 blocking count。
- JSON file 可为数组，或对象中的 `observations[]` / `followup_candidates[]`。

Passing 校验：

- `args.pass_gate and findings` 直接失败，错误文案使用“any findings”。
- `not args.pass_gate and not findings` 仍要求显式 result；observation/followup candidate 不是 failed gate 的替代结果。
- `--pass` 必须传入 `--agent-assignment`，先校验 `review_rounds[].round` 唯一且严格递增，再校验每个 finding owner 都先完成同 agent 闭环 round，最后校验最新/最高 round 的 `最终放行审查代理` 满足 fresh final reviewer 条件。

## Workflow 与平台同步

需要同步以下 canonical 与 dogfood 文件：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/**/trellis-continue*`
- `.agents/skills/trellis-continue/SKILL.md`
- `.codex/prompts/trellis-continue.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.cursor/commands/trellis-continue.md`
- `.trellis/spec/workflow/companion-scripts.md`
- `.trellis/spec/workflow/workflow-contract.md`
- `docs/requirements/requirement-main.md`

如 overlay canonical 改动后，运行 preset apply 同步 dogfood 副本，再运行 drift check。

## 风险与兼容性

- 旧 `review-gate.json` 没有 observations / followup fields 时，`check-review-gate` 不应因缺字段失败。
- 默认配置中的 `block_priorities` 可能仍存在于用户配置。为避免配置漂移削弱 gate，Branch Review Gate 通过逻辑不再依赖该配置；保留字段只作为旧 artifact/配置兼容信息。
- `observation` 与 `followup_candidate` 是否合理属于 AI review 判断，脚本只能记录和校验格式。
- Full throwaway install 耗时较高；如未执行，最终报告必须说明未覆盖。

## 回滚

若实现导致 gate 误阻断，可回滚脚本与 workflow 文案到 base branch；artifact 新增字段为 additive，不会破坏旧 artifact 读取。
