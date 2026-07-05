# #44 收紧 Branch Review Gate：任何 finding 阻断并要求 fresh 最终放行审查

## 目标

把 Guru Team Branch Review Gate 从“P0/P1/P2 finding 阻断、P3 可记录放行”收紧为“任何 finding 都阻断”。当某轮 review 发现 finding 后，该 review agent 后续只能承担问题闭环确认；最终放行必须来自 fresh `最终放行审查代理`，并且该代理要在当前 HEAD 上完整审查 `origin/<base>...HEAD` 后给出 0 findings。

## 背景与确认事实

- GitHub issue: https://github.com/castbox/guru-trellis/issues/44。
- 当前 worktree: `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/44-branch-review-gate-finding-fresh`。
- Base branch: `main`，创建 worktree 时已刷新到 `67df7ff0cefbfa0dbdb6db7b213f8b34b56e5841`。
- 当前 `trellis/workflows/guru-team/workflow.md` 与 `.trellis/workflow.md` 仍写有 “P3 record but does not block”。
- 当前 `guru_team_trellis.py` 的 `DEFAULTS.review_gate.block_priorities` 为 `["P0", "P1", "P2"]`，`review-branch --pass` 只在 P0/P1/P2 blocker 存在时拒绝。
- 当前 `agent-assignment.json` 已支持中文逻辑角色、`review_rounds[]`、`findings_count` 和 reuse decision，但 `review-branch --pass` 尚未强制校验 fresh final reviewer 与完整 diff 0 findings 的关系。
- 官方 Trellis 扩展边界：workflow 行为通过 marketplace workflow / `.trellis/workflow.md` 的 Markdown 合同表达；脚本只做 deterministic recorder / validator，不替代 AI review 判断。

## 需求

1. Branch Review Gate passing path 必须在存在任意 `finding` 时阻断，包括 P3。
2. Review artifact / CLI 语义要区分：
   - `finding`: 当前 diff 已知问题，任何级别都阻断 gate。
   - `observation`: 非阻断观察，不代表当前 PR 有缺陷。
   - `followup_candidate`: 当前 scope 外后续候选，应进入 follow-up issue 或 `issue-scope-ledger.json`，不作为当前 PR finding。
3. `review-gate.json` 必须记录 findings、observations、followup candidates，并在 conclusion 中体现 blocking finding 计数和 observation/followup 计数。
4. 有 findings 的 review round 不能直接 pass gate；修复后可由同 agent 做 `问题闭环审查代理` 确认，但最终 pass 需要 fresh `最终放行审查代理`。
5. `review-branch --pass` 在传入 `--agent-assignment` 时必须校验最终放行 review round：
   - 最终 review round 的 `logical_role` 是 `最终放行审查代理`。
   - `reviewed_head` 等于当前 HEAD。
   - `findings_count` 为 0。
   - 最终 reviewer 的 `agent_id` 不能等于任何之前 `findings_count > 0` 的 review round 的 `agent_id`。
   - 最终 round 的 `reuse_decision` 应表达 fresh/new final reviewer，而不是 `reuse` 或 `reuse-for-closure`。
6. Workflow、continue entry、overlay、dogfood 副本、spec 与 durable docs 必须同步，避免 AI 继续把 P3 当作非阻断，或把问题闭环确认误当最终放行。
7. 脚本只能校验客观字段，不判断 review 质量、observation 是否合理、follow-up 是否应创建 issue；这些判断仍由 AI/human review 和 Markdown workflow 执行。

## 验收标准

- [ ] `review-branch --pass` 在存在任意 finding 时失败，包括 P3。
- [ ] `--observation` 和 `--followup-candidate` 可进入 `review-gate.json`，但不计入 finding blocker。
- [ ] `review-gate.json` 记录 observation / followup candidate 计数，且 conclusion 的通过与否只由 findings 是否为 0 决定。
- [ ] 带有 findings 的 review agent 不能作为最终放行审查代理；修复后必须由 fresh final reviewer 对当前 HEAD 完整 diff 做 0 findings review。
- [ ] reviewed HEAD stale 时仍阻断。
- [ ] 单元测试覆盖任意 finding 阻断、observation 非阻断、followup candidate 非阻断、finding owner closure review 不能 pass、fresh final reviewer 可 pass、reviewed HEAD stale 阻断。
- [ ] canonical workflow、dogfood `.trellis/workflow.md`、preset overlay、`.agents` / `.codex` / `.cursor` 安装副本文案保持一致。
- [ ] `.trellis/spec/workflow/*` 与 `docs/requirements/requirement-main.md` 更新 durable contract。
- [ ] 运行 preset apply 与 dogfood overlay drift check；如未完成完整 throwaway install，最终报告明确未覆盖项。

## 非目标

- 不改变 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不把 AI review 充分性判断写入脚本。
- 不新增 GitHub issue，不关闭 issue #44 以外的 issue。
- 不改变 Phase 2 `trellis-check` finding 语义，除非为了文案一致需要说明 Branch Review Gate 与 Phase 2 的差异。

## Docs SSOT 与知识门禁

- Durable docs 存在于 `docs/requirements/requirement-main.md`，本任务会同步 Branch Review Gate 能力描述。
- Reusable workflow contract 存在于 `.trellis/spec/workflow/`，本任务会同步 companion script 与 workflow contract 规则。
- Middle-platform Knowledge Gate 不适用：本任务不涉及 go-guru、proto-guru、Unity、Flutter 等中台 SDK。
