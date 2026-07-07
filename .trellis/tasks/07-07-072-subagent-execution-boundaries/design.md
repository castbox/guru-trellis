# #72 设计

## 边界

本任务是 workflow / preset / overlay / docs 级别变更，不改变官方 Trellis CLI、不修改 `node_modules`，也不把 AI 判断写进 companion scripts。

长期源头：

- `trellis/workflows/guru-team/workflow.md`
- `trellis/presets/guru-team/overlays/`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `README.md`
- `docs/requirements/`

运行副本：

- `.trellis/workflow.md`
- `.agents/skills/`
- `.codex/prompts/` 与 `.codex/skills/`
- `.codex/agents/`
- `.cursor/agents/` 与 `.cursor/commands/`
- `.claude/agents/` 与 `.claude/commands/`
- `.trellis/agents/`

## 设计原则

1. Markdown workflow / prompt / agent overlay 负责流程判断。
2. Python / shell 继续只负责 executor / recorder / validator。
3. `trellis-implement`、`trellis-check`、review subagent 是默认 `sub-agent` mode 的强制执行边界。
4. `agent-assignment.json` 记录 subagent 身份、status events、review rounds，但不让脚本决定复用或 stale。
5. `phase2-check.json` 只固化 `trellis-check` 完成后的 AI check evidence；不把命令通过或 recorder 通过当作 check 本身。
6. Branch Review pass 语义只引用 #44；本任务只加强“必须真实由 review subagent 执行”。
7. #62 的 timeout / stale / unfinished termination 合同继续适用于 implement、check 和 branch review subagent。

## 预期修改面

- `workflow.md`：
  - 在 Sub-agent Boundary 和 Phase 2/3 中明确默认 sub-agent mode 的强制执行边界。
  - 明确主 agent 不得把自己的实现、check、自审或脚本校验冒充 subagent evidence。
  - 明确 inline/self-exemption 需要 artifact evidence。
- Continue overlay / prompts：
  - 强化 `in_progress` 路径：dispatch `trellis-implement` -> dispatch `trellis-check` -> record `phase2-check.json`。
  - 强化 commit 后路径：dispatch branch review subagent，review 完成后主 agent 才运行 recorder。
- Agent overlays：
  - Implement agent 输出实现 handoff，包括修改范围、设计承接、验证、剩余风险、给 check 的关注点。
  - Check agent 输出可支撑 `phase2-check.json` 的 evidence，并明确它是 Phase 2 check，不替 Branch Review。
  - Check/review agent 在 Branch Review 角色下只审查完整 committed diff，不继续实现。
- Durable docs / README：
  - 同步说明三个 subagent 边界和脚本边界。

## 兼容性

- 技术 dispatch id 不变：`trellis-implement`、`trellis-check`、`trellis-research`、channel `implement`、channel `check`。
- `agent-assignment.json` schema 和 allowed logical roles 不变。
- `review-branch.sh` pass 条件不在本任务复制实现，继续以 #44 现有脚本/文档为 SSOT。
- `status_events[]` 合同不变，只在文档中明确新 subagent 边界同样受 #62 约束。

## Docs SSOT

本任务会更新 durable docs，因为它改变长期 workflow 执行合同。Task artifacts 仅记录本轮规划与证据，不作为长期唯一来源。

## 验证策略

- 静态语法 / JSON：
  - `python3 -m json.tool trellis/index.json`
  - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
  - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
- Workflow parsing：
  - `python3 ./.trellis/scripts/get_context.py --mode phase`
  - `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1`
  - `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.2`
  - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- Task / overlay：
  - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-072-subagent-execution-boundaries`
  - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
  - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
  - `git diff --check`

## 风险

- 多平台 overlay 文案容易漂移；实现必须以 canonical overlay 为源头，再 apply 到 dogfood 副本。
- Durable docs、README 与 workflow 文案可能形成重复但语义不一致；实现后需要 grep 关键短语确认一致。
- 开箱即用验证可能耗时；若无法完成 throwaway install / upgrade 验证，最终报告必须明确。
