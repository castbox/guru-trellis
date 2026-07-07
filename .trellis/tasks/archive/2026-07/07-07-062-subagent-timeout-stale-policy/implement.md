# #62 subagent timeout / stale 策略实现计划

## 执行顺序

1. 更新 task-local context manifest：`implement.jsonl` / `check.jsonl` 引用本任务读取过的 workflow、preset、docs spec 与官方文档 research。
2. 修改 companion script 数据合同：
   - `default_agent_assignment_payload()` 增加 `status_events: []`。
   - `load_agent_assignment()` 对旧 artifact 补 `status_events`。
   - `record-agent-assignment` 增加 status event 记录模式。
   - `check-agent-assignment` 校验 `status_events[]` 结构和高风险事件必填证据。
   - Branch Review Gate pass 校验未闭环 `terminated-unfinished` 状态事件。
3. 增加/更新 unit tests：
   - 记录 status event。
   - 校验非法 status event 枚举或缺失 reason 被拒绝。
   - `terminated-unfinished` 缺少后续恢复/继任/完成/失败事件时，passing review gate 被拒绝。
   - 有 `resume-same-agent` 或 `replacement-started` / `completed` 后允许通过 status event ledger 校验。
4. 更新 canonical workflow：
   - `trellis/workflows/guru-team/workflow.md`
   - `.trellis/workflow.md`
5. 更新 preset overlay：
   - shared / Codex `trellis-continue`
   - Codex prompt `trellis-continue`
   - Claude / Cursor continue command
   - Codex / Cursor / Claude implement/check agents
   - channel runtime implement/check agents
6. 更新 public / durable docs：
   - `README.md`
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
   - `docs/requirements/requirement-main.md`
   - `docs/requirements/guru-team-trellis-flow.md`
7. 若改动 overlay 或 managed assets，运行：
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
   - 处理 `.new` / `.bak`（如有）
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
8. 运行验证与检查，记录 Phase 2 check 后再 commit。

## 预期修改文件范围

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `.trellis/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- preset overlay 下的 continue / agent 文件
- dogfood installed overlay copy：`.agents/skills/`、`.codex/prompts/`、`.codex/skills/`、`.codex/agents/`、`.cursor/agents/`、`.claude/agents/`、`.trellis/agents/`
- public/durable docs 与本 task artifacts

## 验证计划

基础验证：

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-062-subagent-timeout-stale-policy
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.2
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

目标行为验证：

```bash
.trellis/guru-team/scripts/bash/record-agent-assignment.sh --json \
  --logical-role "实现代理" \
  --agent-id "agent-timeout-demo" \
  --platform-nickname "Implement Agent" \
  --status-event wait-timeout \
  --decision continue-waiting \
  --reason "等待窗口 timeout，但最近仍有输出和工作区变化，继续等待。" \
  --last-observed-progress-at "2026-07-07T00:00:00Z" \
  --workspace-evidence "git diff 仍在变化。" \
  --running-command-evidence "验证命令仍在运行。"
.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json
```

如果实际实现采用不同参数名，以实现后的 `--help` 为准，验证目标保持不变。

## Docs SSOT 与 spec 更新

- 本任务必须更新 durable docs，因为它改变长期 workflow 合同。
- 本任务也需要更新 `.trellis/spec/workflow/data-contracts.md` 或相关 workflow spec，记录 `agent-assignment.json.status_events[]` 合同，供后续任务读取。

## 开箱即用 / upgrade-update 验证

最低覆盖：

- dogfood overlay apply + drift check 必须通过。
- managed companion script 同步到 `.trellis/guru-team/`。
- phase context 能读到新规则。

如果时间不足以跑完整 throwaway install / `trellis init` / `trellis workflow --marketplace` 预览，最终报告必须明确未覆盖该项，不能声称已完成开箱即用全量验证。

## Gate 计划

规划审批后：

1. 记录 `planning-approval.json`。
2. `task.py start`。
3. 进入实现，优先使用 Trellis sub-agent；主会话保留协调、artifact、commit 和最终 gate。
4. 完成实现后记录 `phase2-check.json`。
5. commit 前展示 commit plan 并等待确认。
6. commit 后执行独立 Branch Review Gate，停在 `trellis-continue` 允许的边界。
