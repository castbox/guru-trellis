# #55 github issue intake 的过程需要与时俱进

## 目标

让 Guru Team issue intake 在用户输入、GitHub issue、任务执行中需求发生变化时保持“与时俱进”：AI 必须先判断需求是否清晰，必要时进入 `trellis-brainstorm` 与用户澄清，并把澄清或增补结论同步到合适的 GitHub issue 记录，而不是只把最初的 issue body 当成固定事实。

## 背景与证据

- Source issue: https://github.com/castbox/guru-trellis/issues/55。
- Issue 55 明确指出两类缺口：
  - 初始 issue body 或自然语言任务可能模糊，流程应按需进入 brainstorming，多轮确定完整范围。
  - 当前 task 进行过程中可能新增需求或引用其他 issue，流程应询问用户是在当前 task 内完成还是另开 issue，并留下需求增补痕迹。
- 当前 canonical workflow 已要求读取 issue body/comments、Phase 1 加载 `trellis-brainstorm`、维护 `issue-scope-ledger.json`，但没有把“需求模糊度判定、GitHub issue 记录更新、任务中 scope 变化留痕”写成强制合同。
- 官方 Trellis custom workflow 文档支持通过 marketplace workflow 的 Markdown 定义团队流程；本任务应优先修改 `trellis/workflows/guru-team/workflow.md` 及其 dogfood/overlay 入口，不把智能判断写进 companion script。

## 需求

### R1: 初始 intake 必须做需求清晰度判定

- 当用户提供 GitHub issue URL/number 时，AI 读取 issue body 和 comments 后必须判断当前 issue 是否足以进入 Trellis planning。
- 当用户没有提供 issue、只给自然语言任务时，AI 必须判断请求是否足以生成 reviewed issue body。
- 如果需求模糊、验收标准不足、范围边界不清、关闭语义不清，AI 必须进入 `trellis-brainstorm` 式澄清；能从仓库、docs、历史 task、issue comments 回答的问题先查证，不能直接问用户。

### R2: 澄清结果必须同步回 GitHub issue 记录

- 已有 source issue 时，AI 需判断澄清结果应追加 issue comment 还是建议更新原 issue body。
- 新建 issue 前，proposed issue title/body 必须吸收已澄清结论，而不是保留通用占位。
- 同步 GitHub issue body/comment 是 AI/human 判断和 GitHub 副作用；companion script 只能执行确定性 `gh` 写入或记录证据，不能决定澄清是否充分、该改 body 还是 comment。

### R3: 任务中新增需求或引用其他 issue 必须走 scope-change gate

- 在 task 进行过程中出现新增需求、引用其他 issue、发现新 bug、扩大交付边界时，AI 必须暂停当前实现路径并询问用户：纳入当前 task、作为 related reference、还是创建 follow-up issue / 新 Trellis task。
- 结论必须同时留下两类记录：
  - GitHub 侧：当前 issue comment、相关 issue comment，或新 issue。
  - Task 侧：更新 `prd.md` / `design.md` / `implement.md`（如适用）和 `issue-scope-ledger.json` 的 `close_issues` / `related_issues` / `followup_issues`。

### R4: close/ref/follow-up 语义必须保持发布可审计

- `Closes #xx` 只能来自 `issue-scope-ledger.json.close_issues`。
- 新增 close issue 必须满足同一交付单元、不显著扩大边界/风险/测试范围、规划 artifact 已更新、用户明确确认、Branch Review Gate 后续覆盖。
- related/follow-up issue 只能在 PR body 中使用 reference 语义，不能被 publish 自动关闭。

### R5: canonical 与 dogfood/overlay 必须一致

- 长期源头是 `trellis/workflows/guru-team/workflow.md` 和 `trellis/presets/guru-team/overlays/`。
- 本仓库 dogfood 副本 `.trellis/workflow.md`、`.agents/skills/`、`.codex/prompts/`、`.codex/skills/` 需要通过 preset apply 同步或显式保持一致。
- Durable docs 需要更新 `docs/requirements/requirement-main.md` 或 `docs/requirements/guru-team-trellis-flow.md` 中对应能力说明。

## 不做范围

- 不把需求清晰度、body/comment 选择、scope 是否纳入当前 task 的判断写进 Python/shell。
- 不修改 Trellis 上游源码、全局 npm 包或 `node_modules`。
- 不引入新的用户可见主阶段；仍通过 Phase 0 intake、Phase 1 planning、Phase 2 execute/check 和 Phase 3 finish/publish 表达。
- 不要求每个模糊输入都自动创建 issue；创建 GitHub issue 仍需 AI/human reviewed body 和用户确认。

## 验收标准

- [ ] `trellis/workflows/guru-team/workflow.md` 明确写入 intake clarity / brainstorming gate、GitHub issue body/comment 同步规则、task 中 scope-change gate。
- [ ] `.trellis/workflow.md` 与 canonical workflow 在新增规则上保持一致。
- [ ] `trellis/presets/guru-team/overlays/` 的 start/continue 入口对新增规则有足够提示，且不重复粘贴整份 workflow。
- [ ] dogfood overlay drift check 通过，或最终报告明确 `.new` / `.bak` 处理情况。
- [ ] Durable docs 记录该能力，task artifact 不成为唯一长期说明。
- [ ] 相关测试或文本验证覆盖新增规则，至少包含 workflow 文案、overlay 同步、脚本语法/单测和 dogfood drift。
- [ ] Issue 55 的 close 语义只在 acceptance evidence、Phase 2 check 和 Branch Review Gate 覆盖后进入 PR `Closes #55`。

## Docs SSOT 与知识门禁

- Durable docs SSOT: 本仓库有 `docs/requirements/`，本任务会更新 `docs/requirements/guru-team-trellis-flow.md` 或 `docs/requirements/requirement-main.md`，避免只把长期规则留在 task artifact。
- Middle-platform Knowledge Gate: 不适用。本任务修改 Trellis workflow/preset/companion 流程，不涉及 Guru Team middle-platform SDK/framework。

## 当前开放问题

无。Issue 55 的 product intent 已足够进入设计：新增规则应强制 AI 判断与留痕，而不是新增脚本 Planner/Reviewer 行为。
