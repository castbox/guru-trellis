# 设计：completed closeout breadcrumb 同步

## 现状复查

官方 Trellis 文档确认 `[workflow-state:STATUS]` 由 workflow Markdown 驱动，hook 每轮读取 `.trellis/workflow.md` 并生成 breadcrumb。仓库内 `inject-workflow-state.py` 也只解析 tag block，不内置 completed 文案 fallback。

当前主干已经具备完整 finish-work 规则：

- Phase 3.6 要求 gate 通过后创建或审查 task-local PR body；
- finish-work helper 支持 dry-run readiness preview；
- helper 只允许 Trellis metadata tail，拒绝非 metadata dirty；
- Phase 3.7 说明 publish 是 finish-work 后自动发生，direct `publish-pr` 不是正常路径；
- `trellis-finish-work` overlay 已要求中文 PR body 和 `--body-file` / `--body-artifact`。

唯一缺口是 `[workflow-state:completed]` 仍短到不足以作为 closeout breadcrumb。

## 改动边界

### Canonical workflow

更新 `trellis/workflows/guru-team/workflow.md` 中 `[workflow-state:completed]`。文案保持紧凑，但覆盖 issue #40 的关键顺序：

1. 说明 `completed` 是 fallback/legacy closeout breadcrumb。
2. 如果 `review-gate.json` 缺失、失败、stale 或 reviewer-only，回 Phase 3.5。
3. gate 通过后，生成或审查 task-local PR body/readiness。
4. 先 dry-run，再正式 `finish-work`。
5. 非 metadata dirty / drift 阻断，回 `trellis-continue` / Phase 2-3。
6. 不直接调用 `publish-pr`，正常 publish 只能由 `trellis-finish-work` 触发。

### Dogfood active workflow

同步 `.trellis/workflow.md`，确保本仓库当前 hook 立即读取同一文案。

### 测试

在 `.codex/hooks/test_inject_workflow_state.py` 新增 completed breadcrumb 测试：

- 读取当前 root 的 workflow breadcrumb；
- 构造 `build_breadcrumb("task", "completed", templates)`；
- 断言包含 `fallback/legacy closeout breadcrumb`、`review-gate.json`、`Phase 3.5`、`pr-body.md`、`--body-file`、`--dry-run`、`metadata`、`publish-pr` 等关键文本。

测试不需要改 hook parser，因为官方和本仓库规则都要求 workflow Markdown 是 SSOT。

## 兼容性

- 不改变 task status schema；`completed` 仍匹配默认 Trellis status。
- 不改变 `task.py archive` 或 `finish-work.sh` 行为。
- 不改变平台 overlay 文件，因为 finish-work overlay 已经完整覆盖 closeout；本次只补每轮 breadcrumb。
- 不改变 marketplace id、workflow id、preset path 或安装命令。

## 验证计划

- `python3 .codex/hooks/test_inject_workflow_state.py`
- `python3 ./.trellis/scripts/get_context.py --mode phase`
- `python3 ./.trellis/scripts/get_context.py --mode phase --step 3.5`
- `python3 ./.trellis/scripts/task.py validate .trellis/tasks/07-06-40-workflow-state-completed-closeout-pr`
- `git diff --check`

如 workflow/preset 改动触发 dogfood 同步要求，本任务还会运行 overlay drift check；若无 overlay 文件变更，则记录“不适用，未修改 overlays”。

## 风险

- 风险：breadcrumb 过长，违背官方建议的短提示。
  缓解：只放 closeout 决策和命令顺序，不复制完整 Phase 3.6/3.7。
- 风险：completed 被误解成日常主路径。
  缓解：首句明确它是 fallback/legacy closeout breadcrumb，日常路径仍是 Branch Review Gate 后显式 `trellis-finish-work`。
