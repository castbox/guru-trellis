# #43 实施计划

## 前置确认

- Source issue：GitHub #43。
- Base branch：`main`。
- Task worktree：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/43-trellis-subagent`。
- 中台知识门禁：不适用。
- Durable docs：存在 `docs/requirements/`，本任务需要更新。
- 官方 Trellis 文档依据：`custom-workflow.md`、`custom-agents.md`、`custom-hooks.md`、`custom-spec-template-marketplace.md`。

## 实施步骤

1. 更新 workflow 合同。
   - 修改 `trellis/workflows/guru-team/workflow.md`。
   - 同步 `.trellis/workflow.md`。
   - 增加 `agent-assignment.json` 任务 artifact、中文逻辑角色、身份边界、Phase 2/3 记录要求。

2. 增加 companion recorder / validator。
   - 在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 增加 assignment 常量、读写、校验、digest 摘要。
   - 新增 bash wrapper：`record-agent-assignment.sh`、`check-agent-assignment.sh`。
   - 更新 argument parser。
   - 让 `review-branch` 支持 `--agent-assignment` 并在 `review-gate.json` 中固化摘要。
   - 添加或更新 Python tests。

3. 更新 docs。
   - 更新 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md`。
   - 更新 `docs/requirements/requirement-main.md`。
   - 必要时更新 `.trellis/spec/workflow/data-contracts.md` / `workflow-contract.md` / `quality-guidelines.md`，把新 artifact 作为可复用合同记录。

4. 更新 platform overlay。
   - 修改 `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`。
   - 增加/更新 `trellis/presets/guru-team/overlays/.trellis/agents/{implement,check}.md`，保留 channel runtime 技术 `name`，使用中文 UI 展示说明。
   - 增加/更新 `trellis/presets/guru-team/overlays/.codex/agents/trellis-{implement,check,research}.toml`，保留技术 `name`，使用中文 `description` 和 ASCII `nickname_candidates`，避免 Codex 忽略 agent 文件。
   - 增加/更新 `trellis/presets/guru-team/overlays/.cursor/agents/trellis-{implement,check,research}.md` 和 `.claude/agents/trellis-{implement,check,research}.md`，保留技术 `name`，使用中文 `description` / 标题。
   - 修改 `.codex/prompts/trellis-continue.md`、`.codex/skills/trellis-continue/SKILL.md`。
   - 修改 `.claude/commands/trellis/continue.md`。
   - 修改 `.cursor/commands/trellis-continue.md`。
   - 仅在需要时小幅更新 finish/start overlay，避免重复整套 workflow。

5. 同步 dogfood installed copies。
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
   - 处理 `.new` / `.bak`。
   - 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。

6. 自测与质量检查。
   - 运行 JSON / bash / Python 静态验证。
   - 运行 companion unit tests。
   - 运行 task validate 和 phase context reads。
   - 若时间允许，运行 throwaway install 验证。

7. Phase 2 check 记录。
   - 调度或运行完整 `trellis-check`，覆盖 requirements、design、code、tests、spec_sync、cross_layer、docs_ssot、deployment。
   - 写入并校验 `phase2-check.json`。

8. Phase 3 commit 与 review gate。
   - 先检查 dirty state 和 commit plan，等待提交确认。
   - commit task work。
   - 获取独立 Agent review，写 `review.md`。
   - 用 `review-branch.sh --review-source independent-agent --review-report ...` 写 `review-gate.json`。
   - `trellis-continue` 在 Branch Review Gate 后停止，不直接 finish/publish。

## 验证命令清单

```bash
python3 -m json.tool trellis/index.json
python3 -m json.tool trellis/workflows/guru-team/schemas/intake-handoff.schema.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
python3 -m json.tool .trellis/tasks/07-05-43-trellis-subagent/agent-assignment.json
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-43-trellis-subagent
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 2.1
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5
.trellis/guru-team/scripts/bash/check-agent-assignment.sh --json --task .trellis/tasks/07-05-43-trellis-subagent --require-current-head
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

可选开箱验证：

```bash
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

## 风险文件与回滚点

- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`：新增 artifact 读写和 review gate 集成，必须有测试覆盖。
- `trellis/presets/guru-team/overlays/`：改后必须 apply dogfood 并 drift check；agent overlay 要同时覆盖 `.trellis/agents`、Codex、Cursor、Claude，且不能把技术 `name` 改成中文。
- `.trellis/workflow.md` 与 dogfood overlay 副本：只能由 canonical 同步，不要手工产生语义漂移。
- `docs/requirements/requirement-main.md`：作为 durable docs，需保持历史矩阵和当前状态一致。

## Docs SSOT 收敛计划

本任务改变长期 workflow / gate artifact 合同，因此 task artifact 内容需要合并回 durable docs：

- 合并到 `docs/requirements/requirement-main.md`：#43 的能力说明、历史矩阵、当前边界。
- 保留在 task history：具体实现 checklist、命令输出、review gate evidence。

## 开始实现前条件

- `prd.md`、`design.md`、`implement.md` 已完成并经用户确认。
- `implement.jsonl` / `check.jsonl` 已替换为真实 spec/research entries。
- `planning-approval.json` 已记录且 `check-planning-approval.sh --json` 通过。
- `task.py start` 已执行。
