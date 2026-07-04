# 实施计划：#7 PR readiness source 门禁

## 执行顺序

1. **基线确认**
   - 读取 #7 live issue、#17 背景、workflow/preset/docs specs。
   - 搜索 `resolve_pr_body`、`cmd_finish_work`、`cmd_publish_pr`、`body_source`、`body_file`、`body_artifact` 的全部引用。

2. **脚本实现**
   - 增加 reviewed source 判断 helper：non-draft 只接受 `body-file:*` / `body-artifact:*`。
   - 增加 active task path 到 archived task path 的映射 helper。
   - 在 `cmd_finish_work()` archive 前做 readiness preflight。
   - archive 后重写 `body_file` / `body_artifact` 到 archived task path，再调用 `cmd_publish_pr()`。
   - 在 `cmd_publish_pr()` 中阻塞 non-draft generated body，并让 dry-run payload 显示门禁状态。

3. **测试更新**
   - 更新现有 generated body 测试，使 non-draft generated 被拒绝。
   - 增加 draft generated 允许的测试。
   - 增加 finish-work 缺少 reviewed source 被拒绝测试。
   - 增加 active task path archive 后映射测试。
   - 增加 body artifact 内相对 body_file 解析测试。

4. **文案同步**
   - 更新 canonical workflow 与 dogfood workflow。
   - 更新 workflow README、preset README、top-level README。
   - 更新 finish-work overlays：`.agents`、`.codex`、`.claude`、`.cursor` canonical copies。
   - 运行 preset apply 同步 dogfood copies，再跑 drift check。

5. **验证**
   - `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m json.tool trellis/index.json`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-04-7-require-pr-readiness-review-before`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `git diff --check`

6. **收尾**
   - 更新 issue-scope-ledger acceptance evidence。
   - 运行 `trellis-update-spec` 判断是否需要 spec 更新。
   - 提交任务变更。
   - 执行 Branch Review Gate，写 `review.md` / `review-gate.json` 后停止，等待 `trellis-finish-work`。

## 回滚点

- 如果脚本路径重写影响 publish recovery，回滚 helper 并保留 non-draft generated 阻塞的最小改动。
- 如果 overlay 同步产生 `.new` / `.bak`，逐个检查，不带未处理 sidecar 提交。

## 验证记录

- [x] `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`：通过，32 个测试。
- [x] `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`：通过，dogfood overlay copies match canonical。
- [x] 完整静态验证已执行：py_compile、bash -n、json.tool、task.py validate、phase context reads、dogfood overlay drift check、git diff --check 均通过。
- [x] 2026-07-04 14:05 CST 复验通过：单测 32 个、py_compile、bash -n、`trellis/index.json` 与 intake schema JSON、task.py validate、phase context reads、dogfood overlay drift check、git diff --check 均通过；dry-run payload 已包含 `reviewed_source_errors`，可说明 non-draft generated body 的阻塞原因。
