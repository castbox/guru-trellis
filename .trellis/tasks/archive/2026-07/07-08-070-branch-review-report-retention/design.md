# #70 设计：Branch Review raw report retention

## 设计目标

建立“raw reports + rollup + gate digest”的双层证据合同：

- `{TASK_DIR}/reviews/*.md` 是每轮独立 review 的不可变 raw report。
- `{TASK_DIR}/review.md` 是最终人类入口和 rollup，不再承担唯一原始证据职责。
- `agent-assignment.json.review_rounds[]` 是每轮 review 身份、HEAD、finding 数量和 raw report digest 的结构化 ledger。
- `review-gate.json.verification_evidence` 绑定最终 rollup digest 和参与 gate 的 raw report digest 汇总。

脚本只校验客观事实：路径、文件存在、非空、digest、HEAD、round 顺序、finding count、final reviewer freshness、archive path migration、metadata-only tail。review 充分性、findings lifecycle 的语义总结仍由独立 AI/human review 完成。

## 数据合同

### Raw report 路径

每轮 raw report 使用 task-local Markdown 路径：

```text
{TASK_DIR}/reviews/round-001-<purpose>.md
{TASK_DIR}/reviews/round-002-<purpose>.md
{TASK_DIR}/reviews/round-003-final-release.md
```

约束：

- 必须在当前 task directory 内。
- 必须在 `reviews/` 子目录内，避免和顶层 `review.md` 混淆。
- 必须是 `.md` 文件且内容非空。
- 路径由 AI/human review 流程选择；脚本只校验稳定路径和 digest。

### `agent-assignment.json.review_rounds[]`

在现有字段基础上，每个 review round 增加 flat digest fields：

```json
{
  "round": 1,
  "logical_role": "问题发现审查代理",
  "agent_id": "trellis-review-a",
  "platform_nickname": "review-a",
  "reviewed_head": "<git-sha>",
  "findings_count": 2,
  "reuse_policy": "发现 finding 的 agent 只能复用为闭环审查代理。",
  "reuse_decision": "new-agent",
  "review_report_path": ".trellis/tasks/.../reviews/round-001-problem-finding.md",
  "review_report_sha256": "...",
  "review_report_size_bytes": 1234,
  "review_report_modified_at": "2026-07-08T00:00:00+00:00"
}
```

`record-agent-assignment --review-round` 新增 `--review-round-report <path>`。记录 review round 时必须传入 raw report；recorder 计算 digest 并写入 flat fields。

### `review-gate.json`

`review-gate.json.verification_evidence` 保持现有字段：

- `review_report`: 顶层 `{TASK_DIR}/review.md` digest。
- `agent_assignment`: task-local `agent-assignment.json` digest and summary。

新增：

- `review_reports[]`: 从 `agent-assignment.json.review_rounds[]` 汇总而来的 raw report digest list，每项含 `round`、`logical_role`、`agent_id`、`reviewed_head`、`findings_count` 和 digest。

`review-branch` pass path 校验：

- `--review-source independent-agent`。
- `--review-report` 指向 task-local top-level `review.md`。
- `--agent-assignment` 指向 task-local `agent-assignment.json`。
- `agent-assignment.json` 所有 review rounds 都有有效 raw report digest。
- final `最终放行审查代理` 为最后一轮、0 findings、fresh `agent_id`、reviewed_head 等于当前 HEAD。
- 顶层 `review.md` 内容包含每个 raw report 的 repo-relative path 或 `reviews/<file>.md` 相对链接，保证 rollup 能引导人类追溯 raw evidence。

`review-branch` findings path 校验：

- 同样要求 independent source、top-level `review.md`、task-local `agent-assignment.json`。
- 当前 HEAD 必须有一轮 review round，`findings_count` 与本次 CLI findings 数量一致，并绑定 raw report digest。
- 不执行 final reviewer freshness / closure-before-final pass 条件，因为 failed gate 本身记录阻塞状态。

### Archive migration

归档后，active task path 会迁移到 `.trellis/tasks/archive/<month>/<task>`。validator 需要接受并可迁移：

- `verification_evidence.review_report`
- `verification_evidence.agent_assignment`
- `verification_evidence.review_reports[]`

迁移只重写路径和 digest metadata，不改变 review conclusion、reviewed HEAD 或 AI judgment。

## Workflow / overlay 合同

需要同步以下 canonical 和 dogfood surfaces：

- `trellis/workflows/guru-team/workflow.md`
- `.trellis/workflow.md`
- `trellis/workflows/guru-team/README.md`
- `trellis/presets/guru-team/README.md`
- `trellis/presets/guru-team/overlays/*continue*`
- `.agents/skills/trellis-continue/SKILL.md`
- `.codex/skills/trellis-continue/SKILL.md`
- `.codex/prompts/trellis-continue.md`
- finish-work entry overlays中关于 metadata tail 的说明

Overlay 仍只指回 `.trellis/workflow.md` 和 companion scripts，不复制完整 workflow。

## 兼容性与风险

- 新增字段是 additive，但新的 pass/finding gate 会要求新 review rounds 包含 raw report digest；旧任务如果已经处于 Branch Review 阶段，升级后需要补录 raw report evidence。
- `reviews/*.md` 是 task metadata，不应由 `trellis-continue` stage/commit；`finish-work` 可以在 archive/journal/publish 阶段处理 metadata tail。
- `review.md` 链接 raw report 的检查是客观字符串检查，只证明可追溯入口存在，不证明摘要语义充分；语义充分性仍由 independent review 负责。

## 官方 Trellis 扩展面对齐

本任务遵守官方 Trellis 自定义 workflow / marketplace 思路：流程判断写入 workflow/skill/prompt Markdown；脚本只作为 executor/validator/recorder；不修改 upstream CLI 或全局 npm 包。
