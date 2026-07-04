# #26 实施计划

## 当前状态

- Phase 0 intake / worktree / branch / task 已完成。
- worktree: `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/26-worktree-trellis-developer-identity`
- branch: `codex/26-worktree-trellis-developer-identity`
- close issue: #26
- 首次 `get_context.py` 已复现 `.trellis/.developer` 缺失；为继续本 task，已手动从源 checkout 复制 gitignored identity 到当前 worktree。

## 执行步骤

1. 修改 canonical companion script：
   - 增加 `.trellis/.developer` 解析 helper。
   - 修复 `infer_assignee()` 只返回 developer 名字。
   - 增加 `ensure_workspace_developer_identity()`。
   - 在 `cmd_prepare()` executor path、`create_task()` 前调用 identity ensure。
2. 更新 canonical 单测：
   - 目标 worktree 从 source identity 复制 `.trellis/.developer`。
   - source 缺 identity 且显式 `--assignee` 时初始化目标 identity。
   - source 缺 identity 且无 assignee 时阻塞并给恢复命令。
   - `infer_assignee()` 正确解析 `name=`。
3. 更新 durable 文档：
   - `trellis/workflows/guru-team/README.md`
   - `trellis/presets/guru-team/README.md`
   - 必要时更新 `.trellis/spec/workflow/data-contracts.md` 或 companion script spec。
4. 同步 dogfood 安装副本：
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo .`
   - 运行 `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
5. 验证：
   - `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `python3 -m json.tool trellis/index.json`
   - throwaway 或等价安装验证 `prepare-task --create-worktree` 后目标 worktree 有 `.trellis/.developer`
6. 执行完整 `trellis-check` 口径：
   - requirements / design / code / tests / spec_sync / cross_layer / docs_ssot / deployment 全覆盖。
   - 记录 `phase2-check.json`。
7. Phase 3：
   - 判断是否需要更新 `.trellis/spec/`；若本次新增长期脚本合同，更新相关 spec。
   - 提交 task work 与规划/验证 artifact。
   - 取得独立 review，写 task-local `review.md`，记录 Branch Review Gate。
   - `trellis-continue` 到 Branch Review Gate 后停止，不调用 finish-work / publish。

## 验证注意事项

- 检查 `.trellis/.developer` 不进入 Git diff。
- 如果 throwaway 完整 marketplace 安装因为远端分支限制或网络失败无法完成，最终报告要列出未覆盖的开箱即用验证项。
- 本任务不涉及 CI/CD、容器、K8s、数据库 migration 或 Makefile 部署资产；review gate 仍需记录这些资产无需同步的理由。
