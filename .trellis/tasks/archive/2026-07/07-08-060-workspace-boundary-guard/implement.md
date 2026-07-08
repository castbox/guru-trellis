# #60 实施计划：Workspace Boundary Guard

## Phase 1 前置

1. 已完成 Phase 0 intake：
   - issue: https://github.com/castbox/guru-trellis/issues/60
   - workspace: `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/060-workspace-boundary-guard`
   - branch: `codex/060-workspace-boundary-guard`
   - base: `main`，executor 已 fast-forward 到 `origin/main`
2. Middle-platform Knowledge Gate：不适用。本任务修改 Trellis workflow / preset / companion scripts，不涉及 Guru Team 中台 SDK 或 framework。
3. Docs SSOT：存在 `docs/requirements/`，本任务需要更新 durable docs。

## 实施顺序

1. **补充 workspace boundary helper**
   - 修改 `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`。
   - 先搜索并复用现有 `repo_relative()`、`resolve_task_local_path()`、`git_status_paths()`、`load_handoff()`、`resolve_task_dir()`、`file_digest()`，避免重复路径解析逻辑。
   - 增加 context / snapshot / error helpers。

2. **新增 `check-workspace-boundary` 子命令**
   - 在 Python argparse 增加 subcommand。
   - 新增 thin wrapper `trellis/workflows/guru-team/scripts/bash/check-workspace-boundary.sh`。
   - 如果加入 managed asset，更新 preset installer 的 managed file list、README installed files、extension manifest installed assets。

3. **接入 recorder / validator**
   - 在 `record-planning-approval` / `check-planning-approval` / `record-phase2-check` / `check-phase2-check` / `record-agent-assignment` / `check-agent-assignment` / `review-branch` / `check-review-gate` 中解析 task 后调用 boundary 校验。
   - 对 `review_report`、`agent_assignment`、`review_round_report`、`checked_artifact` 的错误路径加测试。
   - 保留 archive / finish-work 的合法 path migration。

4. **同步 workflow / overlay**
   - 修改 `trellis/workflows/guru-team/workflow.md`。
   - 修改 `trellis/presets/guru-team/overlays/` 中相关 start / continue / agent / meta reference overlay。
   - 运行 `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` 同步 dogfood `.trellis/workflow.md`、`.agents/skills/`、`.codex/**`、`.cursor/**`、`.claude/**` 等安装副本。
   - 运行 drift check，处理 `.new` / `.bak`。

5. **更新 durable docs / spec**
   - 更新 `docs/requirements/README.md`、`docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`。
   - 如 workspace boundary 规则应长期保留，更新 `.trellis/spec/workflow/companion-scripts.md`、`workflow-contract.md`、`quality-guidelines.md`。

6. **回归测试**
   - 更新 `trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
   - 若 preset managed asset list 变化，更新 `test_apply_guru_team_trellis_preset.py`。

## Sub-agent 派发计划

规划确认后，按默认 sub-agent 模式执行：

1. 主会话记录 planning approval 并运行 `check-planning-approval.sh --json`。
2. 主会话运行 `task.py start`。
3. 派发 `trellis-implement` 实现代理：
   - Active task: `.trellis/tasks/07-08-060-workspace-boundary-guard`
   - 写入范围：`trellis/workflows/guru-team/**`、`trellis/presets/guru-team/**`、`docs/requirements/**`、`.trellis/spec/workflow/**`、安装副本同步后产生的 dogfood overlay paths。
   - 要求开始时回报 `pwd`、`git rev-parse --show-toplevel`、expected workspace 是否匹配。
4. 派发 `trellis-check` 阶段二检查代理：
   - 覆盖 requirements、design、code、tests、spec sync、cross-layer、docs SSOT、deployment。
   - 输出可记录到 `phase2-check.json` 的中文报告。
5. 主会话记录 `phase2-check.json`，提交非 metadata task work。
6. 提交后派发独立 Branch Review sub-agent，写中文 `reviews/*.md` 和 `review.md`，再由主会话记录 Branch Review Gate。

## 验证命令

最小必跑：

```bash
python3 -m json.tool trellis/index.json
bash -n trellis/workflows/guru-team/scripts/bash/*.sh trellis/presets/guru-team/scripts/bash/*.sh
python3 -m py_compile trellis/workflows/guru-team/scripts/python/guru_team_trellis.py trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py
python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py
python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-060-workspace-boundary-guard
git diff --check
```

如新增 managed asset 或 overlay：

```bash
python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py
trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms
trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh
```

开箱即用验证：

```bash
trellis/presets/guru-team/scripts/bash/verify-throwaway-install.sh
```

如果时间或远端限制导致 throwaway install 不能完整跑通，最终报告必须明确未覆盖项和风险。

## 回滚

- 脚本变更可通过回退 `guru_team_trellis.py`、新增 wrapper 和 managed asset list 回滚。
- Workflow / overlay 文案回滚后必须重新 apply dogfood 并跑 drift check。
- Docs/spec 变更可单独回滚，不影响 runtime。
