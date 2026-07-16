# #113 按 Skill-first 重实现 #55：guru-clarify-requirements

## 1. 目标

实现可独立调用的 semantic closed-loop Skill `guru-clarify-requirements`，把 #55 的 initial intake clarity 与 active-task scope change 统一收敛到一个 step-local SSOT。该 Skill 必须在仓库证据不足时返回缺失证据，在需求需要用户产品意图时按单问题循环收敛，在任何 source-of-truth mutation 前取得针对 exact action 的确认，并以 current content/scope digest 返回唯一 typed exit。

## 2. 来源与已确认事实

- 主需求来源为 [GitHub issue #113](https://github.com/castbox/guru-trellis/issues/113)。
- #113 重新实现 closed #55 的 initial clarity 与 active-task scope evolution，不重新打开或关闭 #55。
- #109 已确立 Global workflow SSOT、Step-local Skill SSOT、semantic stage profile、typed exits 与 script boundary。
- #111 已交付 `guru-discover-change-context`、fresh evidence snapshot、shared dispatcher、canonical package 分发和 throwaway/update 验证基础。
- #125 已确认 `standalone` 仅移除 global workflow routing 依赖；完整 Guru Team preset/runtime 依赖保持不变。
- #128 已冻结 upstream-owned overlay 集合；本任务只能 additive 新增 Guru namespace package、runtime command 和 discovery copies。
- #98 定义 initial intake 全局顺序：`guru-sync-base -> guru-discover-change-context -> guru-clarify-requirements -> guru-review-contract-wording -> guru-review-change-request -> guru-create-task-workspace`。
- #127 指定本 Skill 是未确认 scope expansion 的唯一 requirements/human-confirmation owner。
- 官方 Trellis 文档确认 `.trellis/workflow.md` 拥有 phase/routing，Skill 承载可复用 capability，脚本不得拥有 AI 语义判断。
- 2026-07-16 用户确认 Branch Review Round 1 的 F-001 不纳入 #113：调用方恶意伪造 pre-task/standalone clarification artifact 不属于本任务威胁模型；GitHub-visible 决策见 [issue comment](https://github.com/castbox/guru-trellis/issues/113#issuecomment-4990373622)。

## 3. 功能需求

### R1. Public Skill package 与运行模式

- 新增 stable public Skill id `guru-clarify-requirements`，状态为 `active`。
- `workflow` 与 `standalone` 两种 mode 必须声明完全相同的 entry preconditions、semantic stage profile、runtime dependency 与 freshness 语义。
- Frontmatter description 必须同时覆盖 initial intake、active-task scope change 与用户显式 clarification review。
- Package 必须通过 canonical registry、interface schema 1.2、shared dispatcher 和 preset managed distribution 安装；单独复制 package 必须 fail closed。

### R2. Evidence-first 输入分类

Skill 必须把输入分成以下互斥集合：

1. `confirmed_facts`：已经由 source issue/draft、current repo evidence 或用户明确答案证明的事实。
2. `repository_answerable_questions`：必须先读取 current Docs/code/tests/history/GitHub/Git evidence，不得直接询问用户。
3. `product_intent_questions`：只有用户能决定的目标、优先级或产品语义。
4. `scope_risk_decisions`：current/related/followup/new task/out-of-scope 以及 exact scope proposal。
5. `out_of_scope`：已明确排除且不得进入 current acceptance 或 implementation 的事项。

Workflow mode 必须消费 #111 current snapshot，不得重复搜索已经 current 的 context evidence。Standalone mode 缺少 load-bearing context 时必须返回 `needs_context`。

### R3. 单问题 clarification loop

- Skill 必须加载 `trellis-brainstorm` 作为问答方法，但问题选择、收敛与 pass/block 判断只属于 `guru-clarify-requirements`。
- 每轮只能询问一个最高价值问题。
- 当且仅当多个子问题构成不可分割的同一产品选择时，使用一个 `atomic_group`；该轮必须记录不可分割理由。
- 每轮必须记录 `question_id`、问题类别、答案摘要、affected contracts、opened questions 与 closed questions。
- `answer_status=partial` 不得关闭 open question。
- `clear` 必须满足 open questions 为空、source authority current、content/scope digest current。

### R4. Source-of-truth action 与确认

AI 必须在收敛后选择一个 action plan：

- `none`
- `issue_comment`
- `issue_body_edit`
- `proposed_draft_update`
- `new_issue_draft`
- `active_task_scope_update`

选择规则：

- additive evidence、确认或原 body 不误导 future intake时使用 issue comment。
- problem/scope/acceptance/non-goals/close authority 已误导 future intake时使用 body edit。
- 无 source issue 时更新 side-effect-free proposed draft。
- 独立 delivery unit 时返回 side-effect-free new issue draft；真正创建 issue 由 `guru-create-task-workspace` 执行。
- Active task scope decision 必须同步 GitHub-visible evidence、planning artifacts 与 `issue-scope-ledger.json`。

任何 mutation 前必须展示 exact target、payload、scope delta、受影响 contracts 与 executor command，并取得 action-digest-bound 用户确认。普通 task 创建确认、planning approval 或单独的“继续”不得替代该确认。

### R5. Active-task Scope Change Gate

Active task 出现新增需求、引用其它 issue、新 bug 或 scope expansion 时必须暂停 implementation/check/commit/review progression。

AI 必须提出并收敛以下唯一分类之一：

- 纳入 current `close_issues`
- `related_issues`
- `followup_issues`
- new task
- out-of-scope

Current-task inclusion 当且仅当属于同一 delivery unit、边界/风险/测试未实质扩张、planning 可完整更新并且用户确认 inclusion。纳入 current 后必须更新 `prd.md`、`design.md`、`implement.md`、ledger 与 GitHub-visible authority；既有 planning approval、Phase 2 check 与 Branch Review evidence 必须视为 stale，并重新执行其 owner Skill。

### R6. 未确认 scope expansion 专用合同

- #129/#130/#131 或其它 caller 提交非常规 scope proposal 时，输入必须包含 exact scenario、触发证据、拟新增合同、成本、替代方案和不实施后果。
- 安全、威胁、攻击、恶意 actor、TOCTOU、并发 race、fault injection、跨 OS 原子性在原 requirement 未声明时，必须取得 proposal-digest-bound 专用确认。
- 未确认 proposal 不得进入 issue body、planning execution contract、acceptance、P0-P3 findings 或 implementation。
- 用户拒绝或选择后续处理时，必须分类为 related/followup/new task/out-of-scope；当前已确认 scope 不得因此被阻塞。
- 风险只由非必要实现机制产生时，必须删除或替换该机制，不得通过扩大 requirement 为该机制增加加固 scope。

### R7. Typed exits 与唯一 consumer

- `clear`：requirements 完整且 authority/hash current；唯一 workflow consumer 为 `guru-requirements-clear-router`。Router 校验 `invocation_context.resume_target`：initial issue/draft 进入 staged `guru-review-contract-wording` target，standalone 返回 `guru-standalone-caller`，accepted-current active scope 进入 `guru-active-task-planning-review`，non-current active classification 恢复 exact interrupted progression。
- `needs_context`：缺少 repo/current/history evidence；consumer 为 `guru-discover-change-context`。
- `refresh_context`：comment/body/draft/source/scope/query 已 mutation或 current binding stale；consumer 为 `guru-sync-base`，随后重跑 context 与 clarification。
- `new_task`：独立 delivery unit 已形成 reviewed draft/scope；consumer 为完整 task intake route。
- `blocked`：用户拒绝当前 scope 的 load-bearing 决策、必要 evidence 不可取得或存在无法收敛冲突；consumer 为 fail-closed stop。

Unknown、multiple、unmapped exit 或缺少 consumer 必须 fail closed。

### R8. Deterministic runtime 边界

- AI 必须负责 question selection、clarity、scope classification、action selection、AI Review Gate、confirmation necessity、pass/block 与 typed route。
- AI 在 exact confirmation 后只能通过现有 GitHub connector或审查过的 `gh` 命令执行 issue comment/body mutation，并在 mutation 后重读 live facts。
- `record-requirements-clarification` 只能规范化并记录 AI/human 已完成的结论、hash、scope delta、mutation facts 与 typed exit。
- `check-requirements-clarification` 只能校验 schema、closed shape、digest、live GitHub/source freshness、task-local evidence linkage 与 exit invariants。
- Script 不得生成问题、选择 comment/body/new issue、决定 current/followup、判断 finding severity 或制造 semantic pass。

### R9. Artifact 与状态边界

- 发布 artifact schema `guru-requirements-clarification-1.0`。
- Pre-task result 必须保持 stdout-only，不得写 repo-level clarification cache、workspace journal 或 tracked fixed handoff。
- Initial chain 的 passing result 由后续 `guru-review-change-request` 消费；task 创建后由其 `issue-review.json` 绑定 clarity result digest。
- Active-task scope change 必须把最终 decision trail 写入当前 task 的 ledger/planning/review evidence；不得写其它 task directory。
- Public package、schema、fixtures 与 example 不得包含 active task、workspace journal、secret、本机绝对路径或业务私有数据。

### R10. Canonical、dogfood、安装与文档

- Canonical source 必须位于 `trellis/skills/guru-team/packages/guru-clarify-requirements/`、`trellis/skills/guru-team/registry.json`、`trellis/workflows/guru-team/` 和 `trellis/guru-team-extension.json`。
- Workflow 必须把 #111 `context_ready` consumer 从 placeholder route迁移到 active `guru-clarify-requirements`，并新增本 Skill mandatory invocation 与 exits。
- Preset 必须 additive 安装 shared、Codex、Cursor、Claude 声明目标的 `guru-*` discovery copies；不得新增或修改 upstream-owned overlay。
- Canonical 修改后必须执行 preset apply、source/installed package validation、dogfood drift、clean throwaway initial/update/reapply 与 standalone probes。
- Durable requirements、workflow/preset/docs specs 和三份 public README 必须同步新行为与升级边界。

## 4. Issue Scope

### Close

- #113：本任务必须完整实现并验证全部 acceptance。

### Related

- #55：历史行为来源，已关闭，不重复关闭。
- #98：Intake Skill family umbrella。
- #109：Skill-first architecture prerequisite。
- #111：上游 context discovery producer。
- #114：`clear` 的下游 wording review owner。
- #101：clarity passing evidence consumer。
- #112：最终 task workspace 与 intake integration consumer。
- #127：scope qualification 与 upstream ownership umbrella。

### Follow-up

- 无。本任务不代替上述 open issues 的独立交付。

## 5. 非目标

- 不实现 `guru-review-contract-wording`、`guru-review-change-request` 或 `guru-create-task-workspace`。
- 不创建 repo-level clarification cache、共享 tracked handoff、workspace journal 或全局 index。
- 不修改 Trellis upstream 源码、全局 npm package 或 `node_modules`。
- 不新增或扩大 upstream-owned overlay。
- 不把未声明的威胁、竞态、fault injection、跨 OS 原子性纳入 current scope。
- 不为防止调用方恶意伪造 pre-task/standalone clarification artifact，新增 draft/context 可解引用正文或 locator；F-001 固定分类为 `out-of-scope`。该排除不影响 F-002 至 F-006，也不削弱正常流程的 evidence-first、问题收敛、repository evidence、exact confirmed mutation payload、caller-aware resume 与 ownership 验证。
- 不让 recorder/validator 替代 semantic review 或用户确认。
- 不追溯修改 archived task artifact。

## 6. Acceptance Criteria

- [ ] AC1：`guru-clarify-requirements` 作为 active public Skill 安装并可从 workflow/standalone 两种 mode 调用，两种 mode 使用相同 preconditions 与 semantic stage profile。
- [ ] AC2：Initial issue、无 issue draft、active-task scope change、standalone request 四类入口均有 fixtures。
- [ ] AC3：Repository-answerable question 先取证；单问题、atomic group、`answer_status=partial`、收敛与拒绝路径均有测试。
- [ ] AC4：Comment、body edit、proposed draft、new issue draft、active-task scope update action 全覆盖；mutation 前 exact confirmation，mutation 后 live hash binding。
- [ ] AC5：非常规 scope proposal 的 exact proposal、专用确认、拒绝/后续分类与 optional-mechanism removal 规则有正反测试。
- [ ] AC6：`clear/needs_context/refresh_context/new_task/blocked` 均有唯一 consumer，unknown/multiple/unmapped exit fail closed。
- [ ] AC7：Recorder/validator 不能生成问题、选择 action、分类 scope、执行 mutation 或决定 semantic pass；GitHub mutation 只能在 exact confirmation 后由 AI 调用现有 connector/`gh`。
- [ ] AC8：Pre-task 无 repo/task/runtime tracked write；active-task 只修改当前 task-local ledger/planning/review evidence与明确 GitHub target。
- [ ] AC9：#111 consumer、registry、interface、schema、runtime commands、extension manifest、installer inventory、platform copies 与 public docs 同步。
- [ ] AC10：Source/installed skill validation、package tests、runtime tests、preset installer tests、dogfood apply/drift、clean throwaway initial/update/reapply/standalone 全部通过，无未处理 `.new`/`.bak`。
- [ ] AC11：Branch Review Round 1 的 F-001 以用户确认和 GitHub-visible evidence 记录为 `out-of-scope`；实现不得保留仅为防止该伪造场景新增的 draft/context 正文或 locator 合同，F-002 至 F-006 必须继续闭环。

## 7. Docs SSOT 与知识门禁

- Docs state：`partial_docs`。现有 durable docs 记录 #55 旧行为和 #111 placeholder route，但尚未定义 #113 package、result schema、confirmation/mutation contract 和 active-task scope proposal state machine。
- Docs strategy：`ssot_first`。详细 Docs SSOT Plan 由 `design.md` 单点定义。
- Middle-platform Knowledge Gate：not applicable。本任务只修改 Trellis workflow extension，不涉及 go-guru、proto-guru、Unity3D Guru SDK 或 Flutter Guru SDK。

## 8. 开放问题

无。#98/#101/#112/#114 live issue 已确定 consumers、artifact linkage 和分阶段迁移边界。
