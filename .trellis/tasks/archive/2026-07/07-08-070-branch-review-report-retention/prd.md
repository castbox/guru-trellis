# #70 保留多轮 Branch Review 原始报告并生成最终 review.md 汇总

## 背景

当前 Guru Team Branch Review Gate 已要求独立审查后产出 task-local `review.md`，并在 `review-gate.json` 中记录该文件 digest。这个规则能避免 reviewer-only gate，但多轮 review / 修复 / 复核时，前序独立审查报告仍可能被最终 `review.md` 覆盖或手工压缩，导致 findings、修复闭环、复核结论和阶段性 evidence 难以追溯。

本任务 anchored by GitHub issue #70，属于 Guru Team workflow / companion script / preset overlay 的证据模型 hardening，不修改 Trellis upstream、全局 npm 包或 `node_modules`。

## 需求范围

- 每一轮 Branch Review 独立审查必须保留一份 task-local raw Markdown report，路径稳定、可读、不会覆盖既有轮次，建议位于 `{TASK_DIR}/reviews/*.md`。
- 顶层 `{TASK_DIR}/review.md` 继续作为最终人类入口和 rollup report，汇总 review rounds、findings lifecycle、关键结论、最终放行结论，并链接每轮 raw report。
- `agent-assignment.json.review_rounds[]` 需要记录每轮 raw review report 的 path、sha256、size、modified_at，并保留 round、logical_role、agent_id、reviewed_head、findings_count、reuse_policy、reuse_decision。
- `review-gate.json.verification_evidence` 需要继续记录最终 `review.md` digest，并增加可追溯的 raw `review_reports[]` 汇总。
- `review-branch` findings path 和 pass path 都必须要求 independent review source、task-local `review.md`、task-local `agent-assignment.json` 和本轮 raw report evidence，避免 failed review evidence 被后续 pass 覆盖丢失。
- `check-review-gate` / `finish-work` / archive migration 需要把 raw reports 视为 Trellis task metadata，并在归档后仍能校验 active task path 到 archived task path 的 digest 迁移。
- Workflow、README、preset README、overlay continue/finish 文案需要同步说明 raw reports 是 metadata，`trellis-continue` 不提交这些 review metadata，`finish-work` 处理 metadata tail。
- #61 的标准 Markdown artifact 表边界不在本任务内：默认仍只列顶层 human artifacts，raw reports 通过 `review.md` 链接或调试证据访问。

## 非目标

- 不让脚本判断 review 语义是否充分；脚本只做 recorder / validator。
- 不要求阶段回复表格列出每一轮 raw review report。
- 不把 `review-gate.json`、`agent-assignment.json` 等 JSON 放入标准人类 review 表。
- 不改变 official Trellis upstream、全局 npm package、`node_modules`。
- 不关闭或重新打开 #20、#39、#61；它们只作为相关背景。

## Durable Docs / SSOT

本仓库已有 durable requirements docs：`docs/requirements/README.md`、`docs/requirements/requirement-main.md`、`docs/requirements/guru-team-trellis-flow.md`。本任务会检查是否需要更新 `docs/requirements/guru-team-trellis-flow.md`；如果 workflow 行为变更只在 marketplace/preset README 中足够表达，也必须在最终 Review Gate 说明为什么不更新 durable requirements。

## Middle-platform Knowledge Gate

本任务不涉及 go-guru、proto-guru、Unity/Flutter Guru SDK 或其他 middle-platform SDK/framework；Middle-platform Knowledge Gate 不适用。

## 验收标准

- [ ] 多轮 Branch Review 不再覆盖唯一 `review.md`；每轮 raw Markdown review report 都有 task-local 稳定路径。
- [ ] 最终 `{TASK_DIR}/review.md` 是汇总入口，包含 review rounds summary、findings lifecycle、最终放行结论，并链接 raw reports。
- [ ] `agent-assignment.json.review_rounds[]` 记录每轮 review report 的 path/digest/HEAD/agent 信息。
- [ ] `review-gate.json` 记录最终 `review.md` digest，并能追溯参与 gate 的 raw review reports。
- [ ] findings path 和 pass path 都保留本轮 review report；failed review evidence 不会被最终 pass report 覆盖丢失。
- [ ] `trellis-continue` 明确 raw review reports 是 task metadata，不在 continue 阶段 stage/commit。
- [ ] `finish-work` archive 后 raw reports 和最终 `review.md` 均可从 archived task 目录访问并通过 digest 校验。
- [ ] #61 的标准 Markdown artifact 表仍只默认列顶层 human artifacts，不要求列出每一轮 raw review report。
- [ ] 测试覆盖多轮 review report digest、最终 rollup、archive path migration、metadata-only tail。
