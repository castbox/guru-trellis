# #9 实施计划

## 执行清单

1. 使用 existing preset installer 重新 apply 当前仓库。
2. 检查 apply 输出，确认是否有 `.new` / `.bak` 需要人工处理。
3. 新增 `check-dogfood-overlay-drift.sh` 只读验证脚本。
4. 更新 README、preset README、workflow 与 spec 维护说明。
5. 运行 drift check，确认 overlay installed copies 与 canonical overlay 对齐。
6. 运行 required validation。
7. 更新 issue-scope-ledger 的验收证据。
8. 提交本任务范围内文件。
9. 对 `origin/main...HEAD` 执行 Branch Review Gate。

## 验证命令

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-03-9-keep-dogfood-installed-overlays-in
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
git diff --check
```

## Docs SSOT Reconciliation

本任务没有 `docs/` 目录可更新；长期说明合并到 README、workflow README / workflow contract、preset README 与 `.trellis/spec/`。任务 artifact 只保留 issue #9 的执行证据。

## 回滚点

- 如果 preset apply 产生 `.new` / `.bak`，先检查原因再决定是否纳入。
- 如果 throwaway install 失败且原因与本任务改动无关，记录未验证项和风险；不能声称开箱即用已覆盖。
