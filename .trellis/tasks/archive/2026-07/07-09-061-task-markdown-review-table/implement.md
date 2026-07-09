# #61 实施计划

## 执行顺序

1. 新增 resolver fact layer。
   - 在 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py` 增加 `HUMAN_MARKDOWN_ARTIFACTS` 常量、resolver helper、`cmd_resolve_human_artifacts()` 和 parser dispatch。
   - 新增 Bash wrapper `trellis/workflows/guru-team/scripts/bash/resolve-human-artifacts.sh`。
   - 更新 `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 的 `MANAGED_ASSET_PATHS`。

2. 增加回归测试。
   - 新建或扩展 Python unit test，构造临时 `.trellis/tasks` active/archive 目录。
   - 验证 Markdown-only、archive path、missing link、JSON exclusion。

3. 更新 workflow 合同。
   - 更新 `trellis/workflows/guru-team/workflow.md` 的 planning / in_progress / completed breadcrumb、Phase 1.4、Phase 2.2、Phase 3.5、Phase 3.6、Phase 3.7。
   - 同步 `.trellis/workflow.md`。

4. 更新 platform overlay。
   - 更新 canonical overlay 下 `trellis-continue` 和 `trellis-finish-work` 的 shared skill、Codex prompt/skill、Claude command、Cursor command。
   - 运行 preset apply 同步 dogfood installed copies。

5. 更新公开/安装文档与 manifest。
   - 更新 `trellis/presets/guru-team/README.md` installed files。
   - 必要时更新 `README.md` / `trellis/workflows/guru-team/README.md`，说明阶段回复 Markdown review 表和 resolver。
   - Additive 更新 `trellis/guru-team-extension.json` 和 installed manifest 的 script/capability 列表。

6. 验证。
   - `python3 -m json.tool trellis/index.json`
   - `python3 -m json.tool trellis/guru-team-extension.json`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - resolver unit test。
   - resolver manual active/archive smoke tests。
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 1.4`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 2.2`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
   - `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.6`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-09-061-task-markdown-review-table`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `git diff --check`

7. 开箱即用 / upgrade-update 验证。
   - 修改 overlay 后必须运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`。
   - 如时间允许，运行 throwaway install verifier；若无法完整跑，最终报告明确未覆盖项。

## Sub-agent / inline 说明

当前 Codex 会话在主 session 中完成 planning 和协调。进入实现前需先获得用户对 `prd.md` / `design.md` / `implement.md` 的显式 post-planning 确认，再记录 `planning-approval.json` 并 `task.py start`。

## Docs SSOT

本任务改动长期 workflow / companion script 行为，需同步公开 README / workflow README / preset README 中与日常阶段输出和 installed files 相关的内容。任务 artifacts 只是历史证据。

## 回滚点

- Resolver 代码和 wrapper 是独立新增，可单独回滚。
- Workflow / overlay 文案可通过 git revert 或重新 apply preset 还原。
- 不改变已有 archive、review gate、publish 语义。
