# #52 prd/design/implement 文档显式用户审核

## 目标

在默认 Guru Team workflow 下，`prd.md`、`design.md`、`implement.md` 生成后必须停在用户可见的规划审核门禁。只有用户在看到这三个具体文档链接后明确确认，主会话才能记录 `planning-approval.json`、执行 `task.py start`，并在默认 `sub-agent` mode 下派发 `trellis-implement`。

## 背景证据

- Source issue: https://github.com/castbox/guru-trellis/issues/52
- 复现证据来自 issue #72：历史 `planning-approval.json` 把 Phase 0 handoff 的“确认创建 worktree / branch / task 并继续”记录成 planning approval，35 秒后即派发 `trellis-implement`，缺少用户审核三份规划文档的可审计节点。
- 当前仓库 durable docs 已有 `docs/requirements/requirement-main.md` 和 `docs/requirements/guru-team-trellis-flow.md`，本任务改变 Guru Team 长期 workflow contract，因此需要同步 durable docs。
- 官方 Trellis 扩展面依据：`workflow.md`/marketplace workflow 是流程合同入口；spec template marketplace 不应承载 active task 状态。本任务必须通过 canonical workflow / preset overlay / companion recorder-validator 实现，不改 Trellis upstream、全局 npm 包或 `node_modules`。

## 需求

1. 规划阶段完成后，主 agent 必须向用户展示 task-local 三个规划文档的可打开链接：
   - `prd.md`
   - `design.md`
   - `implement.md`
2. 展示文案必须明确说明：用户未确认前不会进入实现，不会派发 `trellis-implement`，也不会记录 Phase 2 check。
3. Phase 0 handoff 确认不得作为 planning approval 使用；planning approval 的确认必须发生在三份规划文档生成并展示之后。
4. `planning-approval.json` 必须记录并校验三份规划文档的路径、digest、size、mtime、approval 时的 HEAD 和 dirty paths。
5. `user_confirmation.source` 必须能区分 post-planning explicit review，不能继续写成泛化 `workflow`。
6. `check-planning-approval` 必须在以下情况 fail closed：
   - 缺少 `prd.md` / `design.md` / `implement.md` 任一文档；
   - 缺少对应 digest/size/mtime；
   - digest 与当前文件不一致；
   - `user_confirmation.source` 不是规划文档展示后的显式确认；
   - artifact 只有 Phase 0 handoff confirmation 或旧 schema。
7. 默认 `sub-agent` mode 下，缺少有效 planning approval evidence 时必须 fail closed，不得派发 `trellis-implement`、不得记录 Phase 2 check、不得 commit、不得 finish-work。
8. Canonical 与 dogfood installed copies 必须一致：
   - `trellis/workflows/guru-team/workflow.md`
   - `.trellis/workflow.md`
   - `trellis/presets/guru-team/overlays/**/trellis-continue*`
   - `.agents/skills/**`
   - `.codex/**`
   - `.claude/**`
   - `.cursor/**`
9. Script 仍只能做 recorder / validator，不判断规划内容是否充分。

## 非目标

- 不改变 Phase 0 GitHub issue / worktree / branch / task 创建 handoff 流程。
- 不要求用户审核实现后的每一次普通文档小改；只覆盖进入实现前的规划门禁，以及用户批准后规划文档又变化时的重新确认。
- 不把规划内容充分性判断写进 Python / shell。
- 不修改 Trellis 官方 npm 包、`node_modules` 或上游源码。

## 验收标准

- 生成三份规划文档后，`trellis-continue` / Codex / Claude / Cursor 入口固定停在用户审核节点并展示三个链接。
- 用户未确认前，不会派发 `trellis-implement`，不会进入实现，不会记录 `phase2-check.json`。
- Phase 0 handoff 的确认无法通过 `record-planning-approval` / `check-planning-approval`。
- `planning-approval.json` 包含 `review_prompt_presented_at`、`reviewed_artifacts[]`、`user_confirmation.source = explicit-post-planning-review`、`user_confirmation.message`、`approved_at`、`head`、`dirty_paths`。
- 修改任一规划文档后，旧 approval 因 digest mismatch 失效。
- 新增或更新测试覆盖有效 post-planning approval、Phase 0 confirmation 误用、缺少三文档或 digest、文档修改后失效。
- 改 canonical overlay 后，运行 preset apply 同步 dogfood installed copies，并通过 dogfood overlay drift check。
- 完整验证覆盖脚本测试、overlay drift、必要的 throwaway install；若无法覆盖 upgrade/update 或 throwaway install，在 PR body 和最终说明中明确风险。

## Docs SSOT 与知识门禁

- Durable docs: 需要更新 `docs/requirements/requirement-main.md` 和 `docs/requirements/guru-team-trellis-flow.md` 中关于 Phase 1 planning gate 的描述。
- Middle-platform Knowledge Gate: 本任务不涉及 Guru Team 中台 SDK / framework，判定为不适用。
- Spec update: 本任务会强化 workflow/spec contract，若实现中形成可复用规则，需要更新 `.trellis/spec/workflow/*` 或 `.trellis/spec/preset/overlay-guidelines.md`。

## Issue Scope Ledger

- `close_issues`: #52。
- `related_issues`: #72 作为复现背景，只引用，不关闭。
- `followup_issues`: 当前无；若实现中发现更大范围的 Trellis upstream 行为变化或 upgrade 机制缺口，另行提出 follow-up。
