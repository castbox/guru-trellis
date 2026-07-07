# #57 实施计划

## 前置核对

- [x] 读取 issue #57 body 和 comment。
- [x] 读取官方 Trellis custom workflow / custom spec template marketplace 文档。
- [x] 读取 `trellis-meta`、`trellis-before-dev`、preset / workflow / docs specs。
- [x] Docs SSOT：本任务会更新 durable docs 与 `.trellis/spec/`。
- [x] Middle-platform Knowledge Gate：不适用。

## 实施步骤

1. [x] 修改 installer：
   - 在 `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 增加确定性语言规则归一化函数。
   - 把结果写入 installer JSON payload。
2. [x] 补充 installer 单测：
   - 覆盖 `.trellis/spec/backend/index.md`、`.trellis/workspace/index.md`、无目标句文件和 payload。
   - 覆盖 `.trellis/tasks/00-bootstrap-guidelines/prd.md` 中已知英文语言规则的确定性替换。
3. [x] 修改 throwaway install 验证：
   - 增加 `.trellis/spec/**`、workspace index、`00-bootstrap-guidelines` 相关英文语言规则 grep。
4. [x] 修改 workflow / overlay：
   - canonical `trellis/workflows/guru-team/workflow.md`。
   - dogfood `.trellis/workflow.md`。
   - 必要的 start/continue overlay canonical 副本。
5. [x] 运行 preset apply 同步 dogfood：
   - `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`
   - 处理 `.new` / `.bak`。
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
6. [x] 修改 durable docs / spec：
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
   - `docs/requirements/requirement-main.md`
   - `docs/requirements/README.md`
   - `.trellis/spec/workflow/workflow-contract.md`
   - `.trellis/spec/preset/installer.md`
   - `.trellis/spec/docs/public-docs.md`
7. [ ] 运行验证并记录 Phase 2 check。

## 验证命令计划

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-057-chinese-doc-language
git diff --check
```

如环境允许，再运行：

```bash
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

若该命令只能采样 public tag 而不能验证当前分支 marketplace，最终报告会明确说明。

## 提交与 Review Gate

- Phase 2 check 通过后只 stage 本任务文件。
- commit 前运行 `check-phase2-check.sh --json`。
- commit 后获取独立 Agent review，写入 task-local `review.md`，再由 main session 记录 Branch Review Gate。
- `trellis-continue` 到 Branch Review Gate 后停止，不运行 `finish-work`、不 push、不创建 PR。
