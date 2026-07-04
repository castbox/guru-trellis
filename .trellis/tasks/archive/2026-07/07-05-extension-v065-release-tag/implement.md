# #33 实施计划

## 实现步骤

1. 完成 planning gate：
   - 更新 `prd.md`、`design.md`、`implement.md`；
   - 填充 `implement.jsonl`、`check.jsonl`；
   - 记录 `planning-approval.json`；
   - 运行 `check-planning-approval.sh`；
   - `task.py start` 进入实现。
2. 修改 canonical version：
   - `trellis/guru-team-extension.json.version` 改为 `0.6.5`；
   - `tested.trellis_cli` 记录 `0.6.5`。
3. 修改 public docs：
   - `README.md` 中安装、升级 prompt 和版本章节改成稳定 tag-pinned 示例；
   - `trellis/workflows/guru-team/README.md` 同步 marketplace source；
   - `trellis/presets/guru-team/README.md` 同步 throwaway / marketplace 说明；
   - `docs/requirements/requirement-main.md` 增加 #33 能力和 release tag contract。
4. 修改 reusable specs：
   - 在 `.trellis/spec/workflow/data-contracts.md` 和/或
     `.trellis/spec/preset/installer.md` 写入 release tag 与 manifest version 对齐规则。
5. 同步 dogfood installed manifest：
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms`；
   - 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`；
   - 如产生 `.new` / `.bak`，逐个检查并处理。
6. 验证：
   - `python3 -m json.tool trellis/guru-team-extension.json .trellis/guru-team/extension.json trellis/index.json`；
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`；
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`；
   - `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py`；
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-05-extension-v065-release-tag`；
   - `git diff --check`；
   - `rg "guru-team/v0\\.6\\.5|gh:castbox/guru-trellis/trellis(?!#v0\\.6\\.5)" ...` 做文档抽查。
7. 记录 Phase 2 check：
   - 手动完成完整 `trellis-check` 判断；
   - 调用 `record-phase2-check.sh --pass` 并运行 `check-phase2-check.sh`。
8. Commit：
   - 只 stage #33 相关文件；
   - commit message 采用 `chore: align guru team extension release version`。
9. Branch Review Gate：
   - 获取独立 Agent 对 `origin/main...HEAD` 的完整 diff review；
   - 写入 task-local `review.md`；
   - 调用 `review-branch.sh --review-source independent-agent --review-report ...`；
   - `trellis-continue` 到此停止，等待 `trellis-finish-work`。

## 验证边界

本 PR 可以验证：

- JSON / scripts / Python tests；
- docs 与 spec 一致性；
- dogfood installed manifest 与 overlay drift；
- Trellis CLI 对 marketplace `#ref` 的能力已由前置实测确认。

本 PR 不能在 merge 前验证：

- `gh:castbox/guru-trellis/trellis#v0.6.5` 的远程安装，因为 tag 还不存在；
- 删除旧 `guru-team/v0.6.5` tag 后的远程状态。

这些必须作为 post-merge / post-tag 操作记录在 PR body 和最终报告中。

## 回滚点

- 如果 docs 与 manifest 不一致，回退文档或 manifest 后重新运行验证。
- 如果 dogfood apply 产生不可接受的 `.new` / `.bak`，停止并检查 overlay/installer 输入。
- 如果测试失败，不进入 commit；先修复或调整实现范围。
