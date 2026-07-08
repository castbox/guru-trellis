# #78 实施计划

## 执行顺序

1. 更新 workflow 合同
   - 修改 `trellis/workflows/guru-team/workflow.md`。
   - 同步 `.trellis/workflow.md`。
   - 明确 `reviews/*.md` 和 `review.md` 的中文 human-readable artifact 规则。

2. 更新 Branch Review 生成入口
   - 修改 canonical continue overlays。
   - 修改 canonical check agent overlays 的报告模板。
   - 如 finish-work 文案消费 review evidence，同步说明中文规则。

3. 更新 durable docs / spec
   - 修改 `.trellis/spec/workflow/workflow-contract.md`。
   - 修改 `.trellis/spec/workflow/quality-guidelines.md`。
   - 修改 `.trellis/spec/preset/overlay-guidelines.md`。
   - 修改 `docs/requirements/requirement-main.md` 和
     `docs/requirements/guru-team-trellis-flow.md`。
   - 检查 README / workflow README / preset README 是否需要同步。

4. 增加客观模板痕迹校验
   - 在 `guru_team_trellis.py` 增加 forbidden heading 常量和读取/扫描函数。
   - 在 `cmd_review_branch` 与 `validate_review_gate` 相关路径调用。
   - 错误信息中文，指出命中的 report path 和 heading。

5. 补充测试
   - final `review.md` 英文模板标题失败。
   - raw `reviews/*.md` 英文模板标题失败。
   - 中文 report 正常通过。
   - 覆盖 issue 指定的五个 forbidden headings。

6. 同步 dogfood 安装副本
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`。
   - 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`。
   - 处理所有 `.new` / `.bak`。

7. 验证与提交前检查
   - JSON / shell / Python compile。
   - targeted unittest。
   - task validate。
   - dogfood drift check。
   - `git diff --check`。

## 重点文件

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-continue/SKILL.md`
- `trellis/presets/guru-team/overlays/.claude/commands/trellis/continue.md`
- `trellis/presets/guru-team/overlays/.cursor/commands/trellis-continue.md`
- `trellis/presets/guru-team/overlays/.trellis/agents/check.md`
- `trellis/presets/guru-team/overlays/.codex/agents/trellis-check.toml`
- `trellis/presets/guru-team/overlays/.claude/agents/trellis-check.md`
- `trellis/presets/guru-team/overlays/.cursor/agents/trellis-check.md`
- `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
- `.trellis/spec/workflow/workflow-contract.md`
- `.trellis/spec/workflow/quality-guidelines.md`
- `.trellis/spec/preset/overlay-guidelines.md`
- `docs/requirements/requirement-main.md`
- `docs/requirements/guru-team-trellis-flow.md`

## 验证命令

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-078-review-report-chinese-language
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

可选开箱即用验证：

```bash
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

## Review Gate 关注点

- Branch Review raw report 和 rollup 是否真正被中文规则覆盖。
- Script 校验是否只做客观模板痕迹检查，没有替代 AI reviewer。
- Canonical overlay 与 dogfood 安装副本是否无漂移。
- Durable docs SSOT 是否反映本任务的长期规则。
- 是否明确未改变 #70 digest / archive migration 数据模型。
