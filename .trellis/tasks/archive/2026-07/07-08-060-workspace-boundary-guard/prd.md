# #60 防止 task artifact 和 patch 误写到 source checkout

## 目标

建立 Guru Team worktree 模式下的 workspace boundary 机器事实层和流程合同，确保 issue-backed / task-like / file-changing 任务的 task artifact、review artifact、recorder 输入路径、sub-agent 状态证据和手工 patch 都只落在 intake 选定的 task worktree 中，而不是 source checkout。

## 背景证据

- Source issue: https://github.com/castbox/guru-trellis/issues/60
- Issue body 记录了四类历史误写：裸跑 `task.py create`、相对路径写 `review.md` / `review-gate.json` / `agent-assignment.json`、无显式 `workdir` 的编辑工具把 patch 打到 source checkout、旧 `prepare-task` planner 曾写 source checkout handoff。
- Issue comment 2026-07-08 补充了 sub-agent liveness 风险：如果主会话只观察 task worktree，而 source checkout 里仍有当前 task 相关进展，就会把 `workspace-boundary violation with progress` 误判为 stale。
- Issue comment 2026-07-08 明确 #76 是 heartbeat / liveness 后续工作；本任务先建立 workspace boundary 的事实快照和阻断能力，不关闭 #76。

## 需求

1. Workflow / skill / prompt 层必须明确：
   - `workspace_mode: worktree` 下，`prepare-task --create-worktree --create-task` 或等价 Guru Team executor 是创建 task/worktree 的合法路径。
   - 写任何 task artifact 前必须确认当前 repo root 是 intake handoff 的 `workspace_path`。
   - `apply_patch` 等无法显式传入 `workdir` 的编辑工具必须使用 task worktree 内绝对路径。
   - 相对 task artifact 路径只相对 task worktree，不相对 source checkout。
   - sub-agent 启动/等待/stale 判断要记录 expected workspace、actual cwd/repo root、source checkout 和 task worktree 双侧 evidence。
2. Companion scripts 只做 executor / validator / recorder，不做 AI 判断；但必须能客观阻断错误路径：
   - recorder / validator 调用时检查当前 repo root 是否等于 handoff `workspace_path`。
   - `--review-report`、`--agent-assignment`、`--checked-artifact`、`--task` 等 task artifact 输入必须解析到当前 task worktree 内。
   - source checkout 下存在同名 task artifact、handoff、review metadata 或相关 dirty path 时，输出可审计快照并 fail closed，除非该操作明确是 source checkout 允许的 planner-only 路径。
   - 增加轻量 `check-workspace-boundary` validator，输出 expected workspace、actual repo root、source checkout status、task worktree status、可疑 task artifact 副本和结论。
3. `prepare-task --json <issue>` planner-only 继续保持无写入：不得向 source checkout 写 `.trellis/tasks/` 或 `.trellis/guru-team/handoff.json`。
4. Guru Team 受控 `--create-task` 路径必须继续在目标 worktree 内运行 `task.py create`；不得引导 AI 在 source checkout 运行裸 `task.py create`。
5. 对裸 `task.py create` 的治理以 Guru Team 可复用边界为准：不 fork 官方 Trellis 或修改全局 npm 包；若无法安全改造官方 `task.py`，必须通过 Guru Team wrapper / validator / workflow 文案阻断并测试 source checkout 误用场景。
6. Durable docs 必须更新，说明 #60 建立的 workspace boundary 是 #76 heartbeat / liveness 的前置事实层。

## 非目标

- 不实现 #76 的 heartbeat、120s 心跳、180s observation window 或最终 stale 策略。
- 不修改 Trellis 上游源码、全局 npm 包、`node_modules` 或官方 `task.py` 发布包。
- 不把 AI 判断写入脚本：是否 stale、是否终止 sub-agent、是否迁移误写 patch、是否关闭 issue 仍由 AI/human 决定。
- 不静默清理 source checkout 的历史误写；本任务只阻断新流程和记录可疑状态。

## 验收标准

- [ ] `prepare-task --json <issue>` planner-only 在 source checkout 运行时不写 `.trellis/tasks/` 或 `.trellis/guru-team/handoff.json`。
- [ ] 在 worktree mode 且 handoff 指向目标 `workspace_path` 时，recorder / validator 从 source checkout 或其他 worktree 运行会 fail closed，并给出 expected / actual workspace evidence。
- [ ] `review-branch --review-report`、`record-agent-assignment --review-round-report`、`check-agent-assignment --agent-assignment`、`record-phase2-check --checked-artifact` 等 task artifact 参数拒绝 source checkout 路径或非当前 task worktree 路径。
- [ ] 新增 `check-workspace-boundary` validator，并能报告 source checkout status、task worktree status、可疑同名 task artifact 副本。
- [ ] workflow、trellis-start、trellis-continue、sub-agent overlay 和公开 docs 明确 `apply_patch` / 无显式 `workdir` 编辑工具必须使用 worktree 绝对路径。
- [ ] 回归测试覆盖 planner-only 无写入、错误 cwd、错误 review-report / agent-assignment / checked-artifact 路径、source checkout 可疑副本、受控 create_task 只在 worktree 中执行。
- [ ] durable docs `docs/requirements/**` 更新，#60 不关闭 #76。
- [ ] 修改 canonical overlay 后重新 apply dogfood 副本并通过 drift check；若产生 `.new` / `.bak`，逐个处理。
