# #60 详细设计：Workspace Boundary Guard

## 设计原则

1. Markdown / overlay 负责流程和判断：什么时候必须确认 worktree、什么时候算 stale、是否迁移误写 patch、是否终止 sub-agent，都由 AI/human 按 workflow 判断。
2. Companion script 只负责事实：解析 handoff、repo root、task dir、路径归属、Git status、文件是否存在、digest 是否匹配，并在机器可判定的边界 fail closed。
3. Canonical source 优先：长期改动放在 `trellis/workflows/guru-team/`、`trellis/presets/guru-team/overlays/` 和 `docs/requirements/`；dogfood `.trellis/workflow.md`、`.agents/skills/`、`.codex/**` 只作为安装副本同步。
4. 不改官方 Trellis upstream、全局 npm 包或 `node_modules`。对裸 `task.py create` 的可复用治理以 Guru Team executor、validator 和 workflow 文案为边界。

## 官方 Trellis 对齐

- 官方 custom workflow 文档说明 workflow 通过 Markdown 定义 AI 运行流程，本任务把 workspace boundary 判断写入 `workflow.md` / skill / prompt。
- 官方 spec template marketplace 文档将 marketplace 模板定位为可复用规范，不承载 active task state；本任务不把 `.trellis/tasks/` 或 handoff 实例放入 template。
- 官方扩展面允许 hooks、skills、commands、agents 协同；本任务只让脚本提供 deterministic guard，不把 reviewer / product owner 判断下沉到脚本。

## 现状

已存在能力：

- `prepare-task --json` 默认 planner-only，无 GitHub / filesystem 写入。
- executor path 在 `cmd_prepare()` 中先选择 workspace，再通过 `create_task()` 在 `workspace_path` 内运行 `task.py create`，随后把 handoff 写在 workspace 内。
- `resolve_task_local_path()` 已能要求若干 artifact 参数位于当前 `task_dir` 内。
- `review-branch.sh`、`record-agent-assignment.sh`、`record-phase2-check.sh` 都是 thin bash wrapper，核心逻辑在 `guru_team_trellis.py`。

缺口：

- recorder / validator 没有统一确认当前 repo root 是否就是 handoff `workspace_path`。
- `resolve_task_local_path()` 只能证明路径在当前 `task_dir` 内；如果当前 root 错在 source checkout 且那里有同名 task dir，就可能误通过。
- 还没有 source checkout + task worktree 双侧 status snapshot。
- workflow / overlay 虽已有禁止裸 `task.py create` 的文案，但对 `apply_patch` 绝对路径、sub-agent workspace 回报、liveness 双侧观察的要求不够系统。

## 数据流

```text
handoff.json
  -> workspace_path / preflight.current_checkout / task_dir
  -> workspace boundary validator
  -> recorder / gate / sub-agent status evidence
  -> review-gate.json / agent-assignment.json / phase2-check.json
```

关键字段：

- `handoff.workspace_mode`
- `handoff.workspace_path`
- `handoff.preflight.current_checkout`
- `handoff.task_dir`
- `task.json.branch`
- `task.json.base_branch`

## Companion Script 设计

### 1. Workspace boundary helper

在 `guru_team_trellis.py` 中增加共享 helper：

- `workspace_boundary_context(root, config, handoff, task_dir)`：构造 expected workspace、source checkout、actual root、task dir、relative task dir。
- `collect_workspace_boundary_snapshot(...)`：读取 task worktree 和 source checkout 的 `git status --short`、同名 task artifact 是否存在、source checkout handoff 是否存在、可疑 review metadata 是否存在。
- `workspace_boundary_errors(...)`：返回机器可判定错误：
  - `workspace_mode=worktree` 且 actual root 不等于 `workspace_path`。
  - 当前 task_dir 不在 actual root 的 `.trellis/tasks/` 下。
  - source checkout 下存在同名 active task artifact 或 review metadata。
  - task artifact 参数解析后不在当前 task_dir 内。

错误消息必须包含 expected workspace、actual repo root、source checkout 和 task dir，方便 AI 记录/修复。

### 2. 新增 validator subcommand

新增：

```bash
.trellis/guru-team/scripts/bash/check-workspace-boundary.sh --json [--task <task-dir>] [--allow-source-clean]
```

输出结构：

```json
{
  "status": "ok|blocked",
  "workspace_mode": "worktree",
  "expected_workspace": "...",
  "actual_repo_root": "...",
  "source_checkout": "...",
  "task_dir": "...",
  "source_checkout_status": [],
  "task_worktree_status": [],
  "suspicious_source_artifacts": [],
  "errors": []
}
```

该命令不决定 stale、不迁移 patch、不清理 source checkout，只输出事实并对可判定违规 fail closed。

### 3. Recorder / validator 集成

以下命令在解析 task 后调用 boundary helper：

- `record-planning-approval`
- `check-planning-approval`
- `record-phase2-check`
- `check-phase2-check`
- `record-agent-assignment`
- `check-agent-assignment`
- `review-branch`
- `check-review-gate`
- `finish-work` / `publish-pr` 只在 active/archived task path migration 后做只读校验，不阻止已 archive task 的合法读取。

路径参数处理：

- `review_report` 必须是 task-local `review.md`。
- `agent_assignment` 必须是 task-local `agent-assignment.json`。
- `review_round_report` 必须是 task-local `reviews/*.md`。
- `checked_artifact` 继续走 `resolve_task_local_path()`，但 helper 要在解析前确认 root 与 workspace 一致。
- 绝对路径允许，但必须在 expected task worktree 的 task dir 下。

### 4. Create path

`cmd_prepare(create_task=True)` 保持当前设计：

- source checkout 做 preflight 和 base freshness。
- `prepare_workspace()` 选定 / 创建 worktree。
- `create_task()` 用 `cwd=workspace_path` 运行 `task.py create`。
- `write_handoff()` 只写 workspace handoff。

测试覆盖 `create_task()` 的 cwd，而不是修改官方 `task.py` 语义。

### 5. Sub-agent status evidence

扩展 workflow / overlay 文案和 `record-agent-assignment` status event 示例：

- sub-agent 启动时回报 `pwd`、`git rev-parse --show-toplevel`、expected `workspace_path` 是否匹配。
- main session 在记录 `wait-timeout`、`progress-observed`、`stale-assessed`、`terminated-unfinished` 前先运行 `check-workspace-boundary --json` 或等价双侧 status 检查。
- 如果 source checkout 有当前 task 相关 dirty path，记录为 `workspace-boundary violation with progress` 事实，不把它直接当作 stale。

## Durable Docs

更新：

- `docs/requirements/README.md`：历史扫描 / active issue 索引纳入 #60。
- `docs/requirements/requirement-main.md`：P0 intake / worktree / gate 证据链补 workspace boundary 能力，#76 标为 follow-up。
- `docs/requirements/guru-team-trellis-flow.md`：在 Phase 0、Phase 2、Branch Review Gate 和 artifact 责任图中补 workspace boundary validator。

## 兼容性

- 旧安装仓库没有 `check-workspace-boundary.sh` 时不影响现有 `prepare-task` planner；preset apply 会安装新 helper。
- Handoff schema 保持 `additionalProperties: true`，新增 snapshot 字段只作为 additive evidence。
- 普通 Trellis native workflow 的 `task.py create` 不改变。
- 已 archived task 的 review gate / publish readiness 可能读取 archive path，boundary helper 必须区分 active task worktree 写入和 archived artifact 读取。

## 风险与控制

- 风险：source checkout 历史残留 handoff 造成误判。控制：snapshot 输出具体路径和 status，AI 只清理本轮明确创建的文件。
- 风险：过严校验阻塞合法 archive / publish。控制：active task 写入严格，archive 读取走既有 migration path。
- 风险：文案和 overlay 漂移。控制：修改 canonical overlay 后 apply dogfood 并跑 drift check。
- 风险：脚本开始判断 stale。控制：只记录 workspace/status facts，stale 决策仍留在 workflow。

## 验证设计

- Unit tests:
  - planner-only 不写 source checkout handoff/tasks。
  - `create_task()` 只以 workspace 为 cwd。
  - wrong cwd + handoff workspace mismatch fail closed。
  - source checkout 同名 task artifact / review metadata fail closed。
  - `--review-report` / `--agent-assignment` / `--review-round-report` / `--checked-artifact` 指向 source checkout 时 fail closed。
  - `check-workspace-boundary` 输出双侧 status snapshot。
- Integration / repo checks:
  - `bash -n` for shell wrappers。
  - `py_compile` for Python helpers。
  - `python3 -m unittest trellis/workflows/guru-team/scripts/python/test_guru_team_trellis.py`。
  - `python3 -m unittest trellis/presets/guru-team/scripts/python/test_apply_guru_team_trellis_preset.py` if managed asset list changes。
  - `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-08-060-workspace-boundary-guard`。
  - `trellis/presets/guru-team/scripts/bash/apply.sh --repo . --all-platforms` and drift check if overlays change。
  - Throwaway install verification if workflow / preset / managed assets change enough to affect new install readiness。
