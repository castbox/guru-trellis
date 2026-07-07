# 实现计划：planner base freshness 刷新

## 执行顺序

1. 代码定位
   - 复查 `inspect_base_freshness()`、`ensure_base_freshness()` 和 `cmd_prepare()` 调用关系。
   - 确认 tests 中 prepare planner/executor 路径断言。

2. 实现
   - 新增或改造 planner-only freshness helper，使默认 `prepare-task` 也执行 `git fetch origin <base>`。
   - Planner-only 不 fast-forward 本地 base，只刷新 remote-tracking ref 并输出 `fresh/stale/diverged/remote_ref_missing` 等状态。
   - Executor 路径继续使用 `ensure_base_freshness()`，保持创建前强刷新与 fail closed。

3. 测试
   - 增加 mock 单元测试：planner-only 调用刷新 helper，不再调用纯缓存 inspect。
   - 增加本地临时 git 仓库复现测试：local `main` 落后 remote 后，planner-only 输出 `fetch_performed: true`、`fresh: false`、`status: stale`，且本地 `main` 不被 fast-forward。
   - 回归 executor 测试，确保创建 worktree 前仍安全快进或 fail closed。

4. 文档与 schema
   - 更新 workflow README、preset README、workflow.md、schema description，说明 planner-only 也必须刷新/确认 base freshness。
   - 同步 `.trellis/workflow.md` 与 `.trellis/guru-team/` dogfood 安装副本。

5. 验证
   - `python3 -m unittest trellis.workflows.guru-team.scripts.python.test_guru_team_trellis` 的可运行形式按仓库实际导入方式执行。
   - `python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py`
   - `bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh`
   - `python3 -m json.tool trellis/index.json`
   - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-07-059-refresh-base-freshness`
   - `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh`
   - `git diff --check`

## 上下文清单

- 需求来源：GitHub issue #59。
- 项目规范：`.trellis/spec/workflow/*`、`.trellis/spec/preset/*`、`.trellis/spec/guides/*`。
- 官方 Trellis 约束：自定义 workflow / marketplace 采用官方扩展面，不修改上游 Trellis 或全局 npm 包。

## 回退点

- 如果 planner-only 刷新导致不可接受的副作用，只保留 fail-closed unknown 状态而不报告 fresh；不得恢复未刷新却 `fresh: true` 的行为。
