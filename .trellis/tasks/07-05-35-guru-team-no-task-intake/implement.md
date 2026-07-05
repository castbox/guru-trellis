# Issue 35 实施计划

## 执行顺序

1. 读取并确认当前真实模板、overlay、hook 和测试。
   - 搜索 `workflow-state:no_task`、`task-creation consent`、`task.py create`、`prepare-task`。
   - 对比 canonical workflow 与 dogfood active copy。
2. 修改 workflow 合同。
   - 更新 `trellis/workflows/guru-team/workflow.md`。
   - 同步 `.trellis/workflow.md`。
3. 修改 overlay / 平台提示。
   - 更新 canonical `trellis-start` overlay。
   - 更新 Codex / Cursor session-start no-task fallback 文案。
   - 运行 preset apply 同步 dogfood installed copies。
4. 补回归测试。
   - 增加 workflow-state no_task 内容断言。
   - 增加 session-start no-task fallback 不再停留旧 task consent 文案的断言。
5. 更新 docs/spec。
   - README / workflow README / preset README 补充 no_task issue-backed prepare/worktree 入口。
   - 如有必要，更新 `.trellis/spec/workflow/quality-guidelines.md` 或 workflow contract，防止后续回退。
6. 验证。
   - `python3 -m unittest .codex/hooks/test_inject_workflow_state.py .trellis/scripts/common/test_workflow_phase.py`
   - `python3 -m json.tool trellis/index.json`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py .codex/hooks/inject-workflow-state.py .codex/hooks/session-start.py .cursor/hooks/session-start.py`
   - `python3 ./.trellis/scripts/get_context.py --mode phase`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `git diff --check`
   - 尽力运行 throwaway install / preset 验证；若完整远端 marketplace 验证无法覆盖当前未合并分支，最终报告明确说明。

## 需要重点检查的文件

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-start.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-start/SKILL.md`
- `.agents/skills/trellis-start/SKILL.md`
- `.codex/prompts/trellis-start.md`
- `.codex/skills/trellis-start/SKILL.md`
- `.codex/hooks/session-start.py`
- `.cursor/hooks/session-start.py`
- `.codex/hooks/test_inject_workflow_state.py`
- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/workflow/quality-guidelines.md`

## 验证关注点

- no_task breadcrumb 直接包含 Guru Team intake 命令。
- Phase 1.0 不再把裸 `task.py create` 表达成可在 source checkout 直接运行的主路径。
- overlay 与 dogfood 副本无 drift。
- README 的日常入口说明和 workflow 合同一致。
- 没有修改普通 Trellis native workflow 或 upstream CLI 行为。

## 回滚点

如果测试发现 hook/session-start 变化影响非 Guru Team 平台，优先回滚 hook fallback 文案，只保留 canonical workflow/overlay 修复；因为 workflow-state parser 已经以 `.trellis/workflow.md` 为 SSOT。
