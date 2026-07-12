# #109 建立 Guru Team Skill-first 闭环流程模块化强制规范

## 目标

仅修改仓库根 `AGENTS.md`，增加稳定、简洁、强制的 Skill-first 闭环流程模块化规则，使后续 AI Agent 能明确区分 global workflow SSOT、step-local skill SSOT、AI judgment、human confirmation、deterministic script 和 typed exit 的责任边界。

## 用户确认范围

- 2026-07-12 用户明确把当前 task 收缩为只修改根 `AGENTS.md`。
- 2026-07-12 用户要求把 #109 原有的通用闭环 Skill 合同、Canonical package、平台分发、managed hash、结构 validator 和 throwaway 验收迁移到独立 foundation issue。
- 当前 task 不修改 workflow、preset、overlay、skill package、companion script、schema、README、durable requirements/spec 或测试代码。
- 当前 task 不承接、引用或实现其它 issue 的任务范围。

## GitHub Source-of-Truth Action

- 用户已确认 proposed foundation issue 标题/正文，并明确新 issue 不需要写成某两个 umbrella 的共享前置。
- 已创建 #120 承接通用闭环 Skill 合同、Canonical package、平台分发、managed hash、结构 validator 和 throwaway 验收。
- 必须把 #109 正文收敛为根 `AGENTS.md` 原则任务，并链接 #120 作为被迁移内容的唯一 owner。
- 当前 task 不批量修改其它 issue dependency；完成 #109 后按用户顺序直接执行 #120。

## Requirements

### R1. 全局与局部 SSOT

- `AGENTS.md` 必须明确：`.trellis/workflow.md` 只拥有全局 phase 顺序、mandatory skill invocation、跨 skill transition 和 fail-closed stop。
- `AGENTS.md` 必须明确：每个可独立命名的完整步骤由一个 step-local skill 承担内部行为 SSOT；workflow、command、prompt、breadcrumb 和平台 launcher 不得复制 skill 内部步骤。
- Mandatory workflow step 必须由 workflow 按 stable skill id 显式加载，不能只依赖 frontmatter auto-match。

### R2. 闭环 Skill 合同

- Skill 内部顺序必须固定为：正向行为、AI Review Gate、命中条件时的 human confirmation、recorder/validator、typed exit。
- Workflow 只能消费稳定外部出口；每个外部出口必须有唯一 consumer 或明确 fail-closed stop。
- Workflow mode 与 standalone mode 必须使用同一正向行为、AI Gate 和 script boundary；standalone mode 不得弱化门禁。

### R3. AI 与 Script 边界

- AI 必须负责 scope、充分性、finding、pass/block、revision action 和 route 判断。
- Python/shell 只能作为 executor、validator 或 recorder。
- Recorder/validator 必须在 AI review 或 human confirmation 后运行；脚本返回值不得替代语义审查。

### R4. 公共 API 与状态边界

- 新增 Guru Team 公共 workflow skill id 必须使用 `guru-<action>-<object>`。
- Skill id、external exit id、schema id 和 script command 必须被视为团队公共 API；破坏性调整必须新建 id 或记录迁移。
- Active task、workspace journal、平台 prompt、业务私有状态、secret 和本机绝对路径不得写入公共 skill package。
- Pre-task 结果必须保持 repo side-effect-free；task 创建后只能写 task-local tracked artifact，本机映射只能写 gitignored runtime。

### R5. 拆分判定

- `AGENTS.md` 必须列出强制 skill 化条件：多出口/re-entry、多轮交互或 recovery、AI Gate 与 recorder/validator 共存、多入口复用、能独立完成完整能力。
- `AGENTS.md` 必须列出禁止形式化拆分条件：单条确定性 script、纯 breadcrumb/route、只重复其它 SSOT 的包装文本。

## 非功能约束

- 新规则必须与 `AGENTS.md` 现有“Markdown 定义流程，脚本执行事实”“必须保留的 AI 判断门禁”“官方 Trellis 优先”一致。
- 新规则不得声明本次已实现任何 skill、installer、validator 或 workflow route。
- 新规则不得包含其它 issue 的实现顺序、验收或范围。
- 文案必须使用确定性约束，不得把弱约束写成执行合同。

## Docs SSOT 状态

- 状态：`complete_docs`。根 `AGENTS.md` 本身就是本次仓库级 AI 行为规范的 durable SSOT。
- 策略：`ssot_first`，本 task 直接修改该 durable SSOT；task artifact 只保存变更依据和审查证据。

## Acceptance Criteria

- [ ] 只有根 `AGENTS.md` 存在业务变更。
- [ ] `AGENTS.md` 明确 global workflow SSOT、step-local skill SSOT 和 explicit mandatory invocation。
- [ ] `AGENTS.md` 明确 closed-loop skill 顺序、workflow/standalone mode 和 typed exit 唯一 consumer。
- [ ] `AGENTS.md` 明确 AI judgment 先于 recorder/validator，script 不承担 semantic pass/route。
- [ ] `AGENTS.md` 明确 stable naming/public API、package 状态边界、强制拆分和禁止拆分条件。
- [ ] 新增规则不声称已交付任何未实现的 runtime、installer、schema 或 skill。
- [ ] Markdown 结构、术语和现有章节不存在矛盾或重复 SSOT。
- [ ] `git diff --check` 通过。
