# #220 恢复 Phase 1 规划人工审阅停点

## 背景

当前 `standard_intake` 在三份规划文档与 Docs SSOT Plan 通过
`guru-approve-task-plan` semantic review 后，会把 checked `approved` 直接路由到
`task.py start`。这保留了 AI 方案充分性门禁，却删除了用户在实现前审阅解决方向的窗口。

Issue #220 是 #52 的 corrective successor：恢复三文档可见的对话内 review pause，
但不恢复 #52 的授权 artifact、用户原话、确认时间、digest 或固定确认句式。

## 目标

1. 正常 `standard_intake` 在 Phase 1 semantic review 通过后固定暂停。
2. 主 Agent 展示 `prd.md`、`design.md`、`implement.md` 的可打开链接、AI 结论、关键方案选择、替代方案、取舍和未验证边界。
3. 只有展示后的当前对话出现清晰肯定，才执行 task activation 并进入 Phase 2。
4. 保留 AI-first 最小持久化原则，确认只存在于当前对话。

## 需求

### R1 Workflow 拥有 review pause

- `guru-approve-task-plan` 继续独占 planning adequacy、finding、revision、scope route 和四个 typed exits。
- `approved` 的 consumer id 继续是公共 API `phase-1-task-activation`；该 workflow target 先完成人类可见 plan presentation 和 pause，再执行既有 base pair guard、workspace boundary 与 `task.py start`。
- AI Gate 未通过、scope 未收敛或规划存在重大缺口时，不得展示可直接进入实现的确认提示。
- `guru-approve-task-plan` 在把验收场景、负例或 planning finding 纳入判断前，继续按现行合同调用
  `guru-qualify-normal-scenario:planning_scenario_set`；资格 Skill 只返回当前调用内的分类与 witness，
  不接管 planning adequacy、Phase 1 展示或用户确认。

### R2 清晰肯定与非确认输入

- 展示当前方案后，`确认继续`、`可以，继续实现`、`方案没问题，开始做` 这三种示例及相同语义的清晰肯定均有效。
- 提问、质疑、要求修改、只接受局部选择或语义不清的回复均不批准完整方案。
- 不要求用户复述 task、branch、SHA、digest、路径或固定句式。

### R3 修订与 autonomous execution

- 仅解释且计划不变时，回答后保持同一 review pause。
- 规划或 Docs SSOT Plan 实质变化时，重新执行 wording review 和 planning semantic review，再展示新方案；旧确认不可复用。
- scope 或 requirement authority 变化时，进入现有 clarification 路径并重做受影响的 Phase 1 链路。
- 仅当用户在当前请求中明确选择 autonomous execution 时，才可跳过普通 plan pause；scope、authority、重大方案或风险变化仍必须暂停。

### R4 零授权持久化

- 不新增 `human_confirmation`、`user_confirmation`、`approved_at`、confirmation ref/digest 或表达相同授权含义的字段。
- 不修改 recorder/validator 来判断用户是否确认。
- 不恢复 tracked 或 ignored `planning-approval.json` 授权审计；现有 schema 3.0 checkpoint 仍只承接 AI semantic result 和相邻 freshness。
- Phase 0 确认不能复用；Phase 1 确认也不授权 commit、push、PR、merge、release 或 cleanup。

### R5 Canonical、分发与文档一致

- Canonical workflow 与 dogfood `.trellis/workflow.md` 必须一致。
- `guru-approve-task-plan` canonical package 与 shared/Codex/Claude/Cursor managed copies 不得继续声称 checked `approved` 自动激活或“不增加 routine user stop”。
- 官方 Trellis 拥有的 `trellis-start`、`trellis-continue`、`trellis-finish-work`、hooks、agents 与 bundled skills 不改；各平台通过 live `.trellis/workflow.md` 和 managed Guru Skill package 获得一致语义。
- README、requirements 与 workflow/preset specs 必须同步新的确认预算、owner 边界和恢复规则。
- 当前 public graph 的 18 个 active Skills、17 个 business-task mandatory invokes、71 个 external exits、
  24 个 workflow targets 和 18 个 stop targets保持闭合；#220 只新增既有 profile 上的 confirmation
  boundary marker，不新增 Skill、exit、consumer 或 target id。

### R6 Semantic eval fixture composition 前置缺陷

- #220 的 source/installed Shared、Codex、Claude semantic eval 必须执行真实 public wrapper，
  不得以 contract test、静态 fixture 或另一 adapter 的结果替代。
- 当前 `origin/main` 的 native adapter 把 `guru-approve-task-plan/runtime/common.py` 直接当作
  production fixture runtime；该 common 不拥有 fixture 初始化所需的 `write_json`、`load_config`
  与 `write_runtime_mappings`，导致四个 typed-exit case 在进入 wrapper 前统一
  `execution_error`。仅补 `write_json` 会继续在 `write_runtime_mappings` 处失败。
- 在 canonical native adapter 增加一个受限的 production fixture composition：对缺少这些
  fixture-only 能力的 package runtime，复用现有 `guru-review-task-publication` owner 已定义的
  `write_json`、`load_config` 与 `write_runtime_mappings`，再创建 repo-external fixture。
- 把当前仅嵌套在 review-branch composition 中的 package wrapper command bindings 提取为独立
  production-owner command composition；在 owner staging 前按缺失能力注入现有 planning
  record/check bindings，使 `guru-approve-task-plan` 通过真实 wrapper 生成并检查 owner result。
- command composition 继续调用安装包自身的公开 shell wrapper，不导入其 recorder/checker
  Python 模块，不伪造 owner result，也不覆盖 runtime 已有 command capability。
- `guru-planning-approval-3.0` 已把 `semantic_review.scope_proposals` 定义为字符串引用列表，
  `public-clarify-scope-output` 也要求字符串 `proposal_refs`；当前 `invoke.py` 错误地把每项当对象
  读取 `id`。修复只把已校验字符串列表直接投影为 `proposal_refs`，不改变 schema、recorder、
  checker、exit 或 consumer。
- 不把 eval-only workspace/config 能力加入 `guru-approve-task-plan` production common，不复制
  mapping 实现，不改变 recorder/checker/invoke、public I/O 或业务 workflow。
- 回归必须证明 source/installed 的 Shared、Codex、Claude adapter 均越过 staging 并执行真实 wrapper；
  Cursor 缺少认证时仍按现有合同返回 `unsupported`，不进入交互会话。

## 验收标准

1. `standard_intake` 的 checked `approved` 进入用户可见 review pause，并展示三个现存规划 artifact 链接及 AI review 摘要。
2. 展示后没有清晰肯定时，task 仍为 `planning`，实现代理不派发，代码与 Phase 2 不开始。
3. 回归证据覆盖普通确认、同义肯定、提问非确认、要求修订、Phase 0 确认不可复用、规划变化后旧确认不可复用、AI finding 未关闭、明确 autonomous execution、autonomous 模式下 scope 变化暂停。
4. `guru-approve-task-plan` 的 public input、四 exits、consumer ids、schema 3.0 和 recorder/checker职责不变。
5. 任意 tracked、ignored runtime、checkpoint、gate、handoff、archive、schema 和 public DTO 新增授权字段数量为 0。
6. Phase 1 确认不授权后续 Git/GitHub 副作用；现有边界继续独立展示和确认。
7. `task_free` 行为保持不变。
8. Canonical workflow、dogfood、Guru Skill packages、声明支持的平台 managed copies 与公开文档语义一致。
9. Preset reapply、dogfood drift、无 `.new`/`.bak`、targeted contract tests 和 clean throwaway install/update 验证通过。
10. 九类对话回归先通过 `planning_scenario_set` 当前资格化，再由 planning owner 判断验收充分性；
    qualification 不产生 tracked、ignored runtime 或 public handoff artifact。
11. `guru-approve-task-plan` source/installed Shared、Codex、Claude semantic eval 的四个 exits
    均越过完整 fixture 与 owner-command composition，并执行真实 recorder/checker/public wrapper；
    不得再因缺少 `write_json`、`load_config`、`write_runtime_mappings`、
    `cmd_record_planning_approval`、`cmd_check_planning_approval` 或同一 composition 合同中的能力
    返回 `execution_error`；`clarify_scope` 必须把 schema-valid 字符串 proposal refs 原样投影，
    真实 wrapper exit/schema/assertion 结果按各 adapter 现行合同验证。

## 不在范围

- 不恢复 #52 的 `planning-approval.json` 用户授权模型。
- 不新增或重命名 Skill id、exit id、consumer id、schema id 或 script command。
- 不修改 Trellis upstream、全局 npm、`node_modules` 或 upstream-owned platform entry。
- 不让 Python/shell 判断自然语言确认、方案充分性或 route intent。
- 不向 `guru-approve-task-plan` production runtime 增加 eval-only workspace/config helper。
- 除 native adapter 的受限 fixture composition 及其直接回归外，不修改 adapter route、公开
  projection、native trace receipt、semantic grading 或 package runtime 行为。
- command composition 不增加新的 shell command 或 public API，只纠正现有 wrapper bindings 的
  安装位置；不把 recorder/checker Python 实现注入被评测 runtime。
- `invoke.py` 只修复 schema 3.0 到既有 public output 的字符串列表投影；不新增兼容分支、对象
  proposal 形态、默认值或 schema 迁移。
- 不处理恶意伪造、对抗性输入、TOCTOU、锁、并发压力、跨 OS 原子性或额外 fault injection。

## Docs SSOT Plan

- 状态：`stale_docs`。
- 策略：`ssot_first`。
- Durable authority：先更新 canonical workflow、`guru-approve-task-plan` package contract、workflow/preset specs 与 `docs/requirements/**`，再同步 dogfood和平台 managed copies。
- Task artifact 只记录 #220 的交付范围与实施顺序；不成为长期 workflow authority。

## Issue Scope

- Close：#220。
- Related：#52、#129、#161、#164。
- Follow-up：无。
