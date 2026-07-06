# #38 实现计划

## 执行步骤

1. 更新 `trellis/workflows/guru-team/workflow.md` 和 `.trellis/workflow.md` 中 finish-work helper 示例，加入 `--body-file` 与 `--dry-run` 顺序。
2. 更新 `trellis/presets/guru-team/overlays/` 下所有 finish-work 入口，保持 Codex、Claude、Cursor、通用 `.agents` 文案一致。
3. 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`，同步 dogfood `.agents`、`.codex`、`.claude`、`.cursor` 副本。
4. 添加 Python 单测，读取 overlay 文件并断言：
   - 至少一个 reviewed body source 示例：`--body-file` 或 `--body-artifact`；
   - 存在 `--dry-run` readiness preview 示例；
   - 不存在只包含 `.trellis/guru-team/scripts/bash/finish-work.sh --json --from-trellis-finish-work` 的孤立主示例。
5. 运行验证命令并记录 Phase 2 check。

## 验证计划

```bash
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-38-trellis-finish-work-pr-body
python3 ./.trellis/scripts/get_context.py --mode phase
python3 ./.trellis/scripts/get_context.py --mode phase --step 3.6
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
git diff --check
```

## Docs SSOT 与 spec 判断

- `docs/requirements/requirement-main.md` 已有 reviewed PR body、dry-run readiness 和唯一 finish-work 入口要求；本任务预计不需要更新 durable docs。
- `.trellis/spec/` 当前规则已经覆盖本任务，不预计新增 reusable spec。

## 出口条件

- Phase 2 check 覆盖 requirements、design、code、tests、spec_sync、cross_layer、docs_ssot、deployment。
- 工作提交后执行独立 Branch Review Gate。
- `trellis-continue` 到 Branch Review Gate 后停止，不在本入口调用 `trellis-finish-work`、push 或创建 PR。
