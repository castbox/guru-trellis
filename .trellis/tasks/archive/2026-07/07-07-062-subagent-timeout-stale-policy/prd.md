# #62 subagent 超时/终止策略不能把 wait 超时当作未完成工作可接受结果

## Goal

修正 Guru Team workflow 与 preset overlay 中的 sub-agent 协作规则，明确等待窗口超时、长时间无产出、人工终止、恢复/继任和完成证据之间的边界，避免主会话把仍在推进的 sub-agent 提前收口，或把未完成 sub-agent 的部分输出当作 Phase 2 / Branch Review Gate 通过证据。

## Requirements

- `wait_agent`、`trellis channel wait` 或等价等待命令的 timeout 只能表示本次等待窗口未等到最终完成事件，不能单独证明 sub-agent 卡死、失败或应该停止。
- 主会话必须区分“总运行时间长”和“长时间无可观察进展”。只要 sub-agent 仍在输出、改动工作区、运行验证、产出 channel event，或有其他可观察进展，主会话不得要求它收尾或终止。
- 真正的 stale / 卡死判断必须基于最近一段时间无输出、无工作区变化、无有意义命令进展或无状态变化；默认判断窗口至少 5 分钟，不能用固定总运行时长替代。
- 终止、soft interrupt、hard stop、恢复同一 agent 或启动 replacement agent 前，主会话必须留下证据：`agent_id` / logical role、最近一次输出或变化时间、工作区变化证据、等待窗口 timeout 次数或观察方式、是否有长时间卡住的命令、处理决策和原因。
- 如果 sub-agent 未完成即被中断或终止，必须恢复同一会话或启动继任 sub-agent，并传递前任输出、任务上下文、当前 diff、剩余工作和 gate 阻塞点；直到工作完成或明确失败。
- 未完成、被提前终止、未继任闭环的 sub-agent 输出只能作为中间证据，不能作为实现完成、Phase 2 check 通过或 Branch Review Gate 通过依据。
- 规则必须覆盖实现代理、阶段二检查代理、问题发现审查代理、问题闭环审查代理和最终放行审查代理。
- 伴随脚本如需改动，只能作为 recorder / validator：记录 AI/human 已做出的状态处理判断，并校验客观 artifact 字段；脚本不得决定 agent 是否卡死、是否应该终止或是否应该更换。

## Out of Scope

- 不修改 Trellis 官方 npm 包、`node_modules` 或上游 Trellis 源码。
- 不调整 Codex / Claude / Cursor 底层 `wait_agent` 或 channel runtime 的真实超时时长实现。
- 不把业务仓库私有规则写进公共 spec template marketplace。
- 不把 active task runtime state 放进 spec template marketplace。

## Source Evidence

- GitHub issue: https://github.com/castbox/guru-trellis/issues/62
- 官方文档核对：`https://docs.trytrellis.app/advanced/custom-workflow.md` 明确 workflow 行为由 `.trellis/workflow.md` 控制；`https://docs.trytrellis.app/advanced/custom-agents.md` 明确 shipped sub-agent 与平台差异；`https://docs.trytrellis.app/advanced/custom-spec-template-marketplace.md` 明确 spec marketplace 不承载 task/runtime state。
- 本仓库当前证据：`trellis/workflows/guru-team/workflow.md` 已有 sub-agent 身份、review reuse 与 Branch Review Gate 规则，但缺少等待窗口 timeout / stale / 未完成继任策略。

## Docs SSOT

本仓库存在 durable docs SSOT：`docs/requirements/`。本任务会改变 Guru Team workflow 和 sub-agent 协作长期合同，因此需要同步更新：

- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`

Task artifact 只保存本次执行证据，不作为长期唯一来源。

## Middle-Platform Knowledge Gate

不适用。本任务修改 Trellis workflow / preset / companion script / docs，不涉及 Guru Team middle-platform SDK、go-guru、proto-guru、Unity3D Guru SDK 或 Flutter Guru SDK。

## Acceptance Criteria

- [ ] workflow 文档明确区分等待窗口 timeout、长时间无产出、人工终止、恢复/继任和正常完成。
- [ ] 主会话规则明确禁止因为总运行时间长就终止仍有可观察进展的 sub-agent。
- [ ] `agent-assignment.json` 或等价 task artifact 有明确状态事件合同，可记录 timeout/stale 判断依据、继续等待/恢复/替换/终止决策和继任上下文。
- [ ] 未完成即被终止的 sub-agent 必须有恢复同一 agent 或 replacement agent 继续完成的证据；未闭环状态不得通过后续 gate。
- [ ] Phase 2 check / Branch Review Gate 规则明确不能把被终止且未完成的 sub-agent 输出作为通过依据。
- [ ] 相关 prompt / skill / agent overlay 覆盖实现代理、阶段二检查代理、问题发现/闭环/最终放行审查代理。
- [ ] canonical source 与 dogfood installed copy 同步：`trellis/workflows/guru-team/`、`trellis/presets/guru-team/overlays/`、`.trellis/workflow.md`、`.agents/skills/`、`.codex/prompts/`、`.codex/skills/`、`.trellis/guru-team/`。
- [ ] 验证覆盖 JSON/schema、bash、Python 编译/单测、phase context、task validate、dogfood overlay drift、`git diff --check`。
- [ ] 若无法完成 throwaway install / upgrade-update 全量验证，最终报告必须明确未覆盖项和风险。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- 本任务为复杂 workflow/preset/script/docs 变更，需要 `design.md` 与 `implement.md` 审批后才能 `task.py start`。
