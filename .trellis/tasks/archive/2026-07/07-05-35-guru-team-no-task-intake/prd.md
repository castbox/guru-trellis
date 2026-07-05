# Issue 35：Guru Team no_task intake 防绕过 worktree

## 目标

修复 Guru Team workflow / overlay 在 `no_task` 和 Phase 1.0 下的提示缺陷，确保 issue-backed、task-like 或需要文件修改的开发请求不会只凭通用 task creation consent 在 source checkout 直接运行裸 `task.py create`。

## 背景与证据

- 用户在 `chengtuo-resume` 复现：`.trellis/guru-team/config.yml` 配置 `workspace_mode: worktree`、`branch_prefix: codex/` 和默认 worktree root，输入“解决 issue #50”后 Codex 收到 `workflow-state:no_task`。
- 旧提示只强调“classify current turn / ask task-creation consent”，后续 Phase 1.0 又展示裸 `python3 ./.trellis/scripts/task.py create ...`，AI 被带到 source checkout 的 `main` 下直接创建 `.trellis/tasks/...`。
- Guru Team 正确流程必须先运行：
  - `.trellis/guru-team/scripts/bash/check-env.sh --json`
  - `.trellis/guru-team/scripts/bash/prepare-task.sh --json "<user request or issue URL>"`
- 本任务已按 Guru Team intake 执行：source issue 为 <https://github.com/castbox/guru-trellis/issues/35>，base branch 为 `main`，task worktree 为 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/35-guru-team-no-task-intake`，branch 为 `codex/35-guru-team-no-task-intake`。

## 需求

1. `workflow-state:no_task` 必须把 issue-backed / task-like / file-changing 请求的第一优先级写成 Guru Team Phase 0 intake，而不是裸 `task.py create`。
2. `workflow-state:no_task` 必须直接列出 `check-env.sh --json` 和 `prepare-task.sh --json` 命令。
3. Phase 1.0 必须明确：
   - `task creation consent` 不等于 current checkout direct-edit consent。
   - 默认 `prepare-task` 只做 intake/preflight/handoff planning。
   - `workspace_mode: worktree` 时，创建执行环境必须通过 `prepare-task --create-worktree --create-task` 或等价受控 executor 入口。
   - 裸 `task.py create` 只能在已进入 prepare 选定的 `workspace_path` 且 handoff 已写入后作为 follow-up，不得在 source checkout 运行。
4. `trellis-start` overlay 与 Codex/Cursor session-start 类提示不得再只提示“ask task-creation consent”，必须指向 Guru Team prepare/worktree 流程。
5. 回归测试必须证明 workflow-state / generated workflow 提示包含 Guru Team prepare/worktree 流程，不再只有泛化 task consent。
6. 不修改 Trellis upstream、全局 npm 包或 `node_modules`；不破坏普通 Trellis native workflow 中轻量任务的 `task.py create` 行为。

## 范围

### 必须检查和更新

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/presets/guru-team/overlays/.agents/skills/trellis-start/SKILL.md`
- `trellis/presets/guru-team/overlays/.codex/prompts/trellis-start.md`
- `trellis/presets/guru-team/overlays/.codex/skills/trellis-start/SKILL.md`
- dogfood installed copies under `.agents/` and `.codex/`
- Codex/Cursor session-start no-task fallback text if it can conflict with Guru Team workflow-state
- Tests around workflow-state injection / workflow phase parsing

### 可选更新

- `README.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `.trellis/spec/` workflow/preset guideline if this bug exposes a reusable review rule

### 不在范围

- 不改 `task.py create` 的普通 Trellis native 语义。
- 不新增脚本判断 AI 应该如何规划；脚本只可记录或校验客观事实。
- 不改业务仓库 `chengtuo-resume` 的生成文件。

## 验收标准

- [ ] 新生成的 guru-team 项目中，`trellis-start`、`workflow-state:no_task`、Phase 1.0 均明确阻止 issue-backed 任务直接在 source checkout 运行 `task.py create`。
- [ ] 文案明确列出 `check-env.sh --json` 和 `prepare-task.sh --json` 作为 no_task issue-backed 入口。
- [ ] `workspace_mode: worktree` 时，提示要求使用 `prepare-task --create-worktree --create-task` 或等价受控入口创建执行 worktree。
- [ ] 测试或快照证明 workflow-state / generated workflow 不再只提示“ask whether create Trellis task”，而是提示 Guru Team prepare/worktree 流程。
- [ ] `trellis/presets/guru-team/scripts/bash/check-dogfood-overlay-drift.sh` 通过，确认 canonical overlay 与 dogfood 副本同步。
- [ ] 普通 Trellis native workflow 的轻量 `task.py create` 行为未被脚本层改动。

## Docs SSOT 与中台知识门禁

- 本仓库有 `docs/requirements/`，但本任务修改的是 Guru Team workflow/preset 的可复用运行合同；长期 SSOT 主要在 `README.md`、`trellis/workflows/guru-team/README.md`、`trellis/presets/guru-team/README.md` 与 `.trellis/spec/`。
- 本任务不涉及 Guru Team 中台 SDK / framework，因此 Middle-platform Knowledge Gate 不适用。

## 当前开放问题

无阻塞开放问题。用户已确认采用 Guru Team worktree + task 通道，并要求实现修复。
