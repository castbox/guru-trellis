# 设计：planning approval 与 Phase 2 check evidence gate

## 设计原则

- AI 判断在前：planning approval 和 `trellis-check` 覆盖性由 AI/human 完成判断。
- 脚本在后：companion script 只记录、计算 hash、校验 stale、阻塞缺失证据，不替代 review / check 判断。
- Canonical 优先：修改 `trellis/workflows/guru-team/`、preset overlays 和 README，再同步 dogfood copy。
- Fail closed：缺证据、证据过期、基础分支过期、或 blocking finding 未处理时阻塞后续阶段。

## 新增 artifact

### `planning-approval.json`

默认路径：`{TASK_DIR}/planning-approval.json`。

建议结构：

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-07-04T00:00:00Z",
  "task_dir": ".trellis/tasks/<task>",
  "head": "<git sha>",
  "dirty_paths": [],
  "reviewer": "codex-main-session",
  "approval_summary": "用户已审阅 prd/design/implement，并确认进入实现。",
  "approved_artifacts": [
    {"path": ".trellis/tasks/<task>/prd.md", "sha256": "...", "size_bytes": 1, "modified_at": "..."}
  ],
  "notes": "record-planning-approval 是 recorder / validator，不替代 AI/human planning review。"
}
```

校验规则：

- 文件必须在当前 task 目录内。
- `prd.md` 必须存在；复杂任务需要 `design.md`、`implement.md`。
- artifact 中记录的 path/hash/size 必须匹配当前文件。
- artifact 记录的 `head` 必须等于当前 HEAD；允许 dirty_paths 记录 task metadata，但 planning 文件发生变化必须重新批准。
- `approval_summary` 必须非空。

### `phase2-check.json`

默认路径：`{TASK_DIR}/phase2-check.json`。

建议结构：

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-07-04T00:00:00Z",
  "task_dir": ".trellis/tasks/<task>",
  "base_branch": "main",
  "head": "<git sha>",
  "diff_range": "origin/main...HEAD",
  "dirty_paths": [],
  "checker": "codex-main-session",
  "check_summary": "已按完整 task scope 执行 trellis-check。",
  "checked_artifacts": [],
  "checked_specs": [],
  "coverage": {
    "requirements": true,
    "design": true,
    "code": true,
    "tests": true,
    "spec_sync": true,
    "cross_layer": true,
    "docs_ssot": true,
    "deployment": true
  },
  "validation_commands": [
    {"command": "python3 -m unittest ...", "result": "passed"}
  ],
  "findings": []
}
```

校验规则：

- `check_summary` 非空。
- required coverage key 必须存在且为 true；如某项不适用，AI 在 summary/evidence 中说明，但 artifact 中仍要显式记录为 true，含义为“已检查并判定不适用或无需修改”。
- P0/P1/P2 finding 必须不存在或状态为 resolved。
- 记录的 `head` 必须等于当前 HEAD。
- `dirty_paths` 与当前 dirty 状态不一致时判为 stale。
- 记录的 task/spec artifact hash 必须匹配当前文件。

## Helper 命令

新增 wrapper：

- `.trellis/guru-team/scripts/bash/record-planning-approval.sh`
- `.trellis/guru-team/scripts/bash/check-planning-approval.sh`
- `.trellis/guru-team/scripts/bash/record-phase2-check.sh`
- `.trellis/guru-team/scripts/bash/check-phase2-check.sh`

Bash 只转发到 Python：

```bash
python3 "$SCRIPT_DIR/../python/guru_team_trellis.py" <subcommand> "$@"
```

Python 新增 subcommand：

- `record-planning-approval`
- `check-planning-approval`
- `record-phase2-check`
- `check-phase2-check`

设计理由：保持与现有 `review-branch` 模式一致，脚本是 recorder/validator。`task.py` 是 Trellis 官方生成脚本，不作为本次长期扩展面修改。

## Branch Review Gate 独立来源校验

`review-branch --pass` 增加客观来源 metadata：

- `--review-source independent-agent`：声明该 passed gate 基于独立 Agent review。
- `--reviewer <identity>`：仍是身份 metadata，但 passed gate 会拒绝空值、`*-main-session` 和 `self-review` 形态。

`review-gate.json` 在 `verification_evidence.review_source` 中持久化来源。`validate_review_gate()` 对旧 artifact 也 fail closed：缺少 `review_source: independent-agent`、缺少 `review_report` digest、`review_report` 不是 task-local `review.md`，或 reviewer 是 main-session/self-review 时，`check-review-gate` / `finish-work` / `publish-pr` 都不能继续。

脚本只校验来源字段、reviewer 形态、`review.md` basename、digest、HEAD 和 finding 阻塞状态；“review 是否充分”仍由独立 Agent 的 `review.md` 和 findings 负责。当前主会话可以记录 P0/P1/P2 失败 gate，但不能写 passed gate。

`check-planning-approval` 默认仍严格要求批准 HEAD 等于当前 HEAD，用于进入实现前的 start gate。Branch Review Gate / post-commit audit 路径使用显式 `allow_committed_head`，允许 planning approval 记录的 HEAD 是当前提交祖先；这样不要求每次实现提交后重批规划，但仍要求规划文件 hash 未变。

`check-phase2-check` 默认仍严格要求 check HEAD 等于当前 HEAD，用于 commit 前 gate。Branch Review Gate / post-commit audit 路径允许 `phase2-check.json` 记录的 HEAD 是当前提交祖先，但只能接受该 HEAD 之后的 committed tail 全部属于 Trellis metadata，例如 task/review/journal artifact；如果 `recorded_head..HEAD` 含有 workflow、script、preset、README、schema、CI/CD、部署或其他非 metadata 文件，必须 fail closed。只检查当前 working tree dirty 状态不够，因为非 metadata 变更可能已经提交。

## Preflight Base Freshness

在 `cmd_prepare()` 内解析 base 后增加 freshness 检查：

- planner-only 路径：
  - 尝试读取 local/remote HEAD；
  - 不执行文件系统写入；
  - 输出 `preflight.base_freshness`，当无法确认 fresh 时给出 warning。
- executor 路径 `--create-worktree` / `--create-task`：
  - 执行 `git fetch <remote> <base>`；
  - 比较 local base 和 `origin/<base>`；
  - local 落后远端时，如果当前没有 dirty state 且可 fast-forward，则更新 local base；
  - local 和 remote 分叉或无法 fast-forward 时阻塞；
  - 从 refreshed base 创建 worktree。

`base_freshness` 进入 handoff，记录 remote、base、local_head_before/after、remote_head、fetch 执行情况、是否 fast-forward。

## Workflow / Overlay 更新

- `trellis/workflows/guru-team/workflow.md`：
  - Phase 1.4 增加 record/check planning approval 的步骤。
  - Phase 2.2 增加 record/check phase2 check report 的步骤。
  - Phase 3.4 commit 前要求 `check-phase2-check` 通过。
  - Phase 0 preflight 说明 base freshness。
- `.trellis/workflow.md` 与 canonical 同步。
- Continue overlay：
  - planning 状态提醒 start 前必须写入并检查 `planning-approval.json`。
  - in_progress 状态提醒 commit 前必须写入并检查 `phase2-check.json`。
  - after commit 状态要求独立 Agent review；无独立 review evidence 时停止在 Branch Review Gate pending。
- README 更新安装/日常入口说明。

Throwaway install 验证脚本默认使用当前 checkout 的 `trellis/` 作为 workflow marketplace source，同时验证 existing-project `trellis workflow --marketplace ... --create-new` 预览和 forced switch，避免只证明公开远端旧 workflow 可安装。

## Preset 同步

新增 helper 需要：

- 加入 `trellis/workflows/guru-team/scripts/bash/`。
- 加入 `trellis/presets/guru-team/scripts/python/apply_guru_team_trellis_preset.py` 的 `MANAGED_ASSET_PATHS`。
- 更新 `trellis/presets/guru-team/README.md` installed files。
- 运行 preset apply 同步 `.trellis/guru-team/` dogfood copy。

## 风险与回滚

- 风险：artifact stale 校验过严导致合法 metadata 变更被阻塞。缓解：规划 gate 只比较规划 artifact hash；Phase 2 gate 记录 dirty paths 并允许重新 record。
- 风险：base freshness 在本地 base 已被其他 worktree checkout 时无法 fast-forward。缓解：优先 fetch 和从 `origin/<base>` 创建 worktree；若必须更新 local base 且 Git 阻塞，输出明确错误。
- 回滚：撤销新增 helper、workflow/overlay 文案和 README 更新即可恢复旧流程。
