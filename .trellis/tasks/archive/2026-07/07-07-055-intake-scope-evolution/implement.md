# #55 实施计划：Issue Intake Scope Evolution

## 实施顺序

1. 修改 canonical workflow：
   - `trellis/workflows/guru-team/workflow.md`
   - 增加 Intake Clarity Gate、Issue Evidence Update Rule、Scope Change Gate。
2. 修改 canonical overlay：
   - `trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`
   - `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
   - 同步 `.codex/prompts` / `.codex/skills` / `.claude` / `.cursor` 对应入口的简短提示。
3. 更新 durable docs：
   - `docs/requirements/guru-team-trellis-flow.md`
   - 必要时更新 `docs/requirements/requirement-main.md`。
4. 运行 preset apply 同步 dogfood 安装副本：
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
5. 处理 `.new` / `.bak`：
   - 逐个检查，不静默丢弃未知本地改动。
6. 运行验证：
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `git diff --check`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - 相关 Python unittest。
7. Phase 2 check：
   - 按 `trellis-check` 覆盖 requirements、design、docs、workflow、overlay、script boundary、tests、deployment impact。
   - 记录 `phase2-check.json`。
8. Commit 与 Branch Review Gate：
   - 只 stage 本任务范围文件。
   - commit 后获得独立 review，写 `review.md` 和 `review-gate.json`。

## 预期修改文件

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/**/trellis-start*`
- `trellis/presets/guru-team/overlays/**/trellis-continue*`
- dogfood installed overlay copies under `.agents/`, `.codex/`, `.claude/`, `.cursor/`
- `docs/requirements/guru-team-trellis-flow.md`
- 可能补充 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py` 的文本合同测试

## 风险文件与回滚点

- Workflow/overlay 文案是公共运行合同，必须保持 canonical 与 dogfood 一致。
- 若 preset apply 产生 `.new`，先 diff 后决定合并或保留，不能直接删除。
- 若 tests 暴露脚本行为与新 workflow 不一致，优先调整 Markdown 判断合同；只有确定性验证缺失才改脚本。

## Docs SSOT 责任

本任务会更新 durable docs，至少记录以下长期能力：

- Phase 0 intake clarity / brainstorming。
- Planning/ongoing task scope change gate。
- GitHub issue comment/body/new issue 留痕策略。

## Middle-platform Knowledge Gate

不适用；本任务不涉及 Guru Team middle-platform SDK/framework。

## 完成标准

- 规划 artifact 已审查并记录 `planning-approval.json` 后再 `task.py start`。
- Phase 2 check 通过并记录。
- commit 后 Branch Review Gate 通过。
- 若未跑完整 throwaway install，最终报告明确未验证项和风险。
