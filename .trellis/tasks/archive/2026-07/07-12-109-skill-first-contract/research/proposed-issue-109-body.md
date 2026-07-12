# #109 拟更新正文

## 背景

Trellis 官方把 skill 定义为 capability/phase 级 reusable workflow module，并由 `.trellis/workflow.md` 负责 phase、skill routing 和全局顺序：

- https://docs.trytrellis.app/advanced/custom-skills.md
- https://docs.trytrellis.app/advanced/custom-workflow.md
- https://docs.trytrellis.app/advanced/architecture.md

Guru Team 当前把部分完整步骤同时展开在 workflow、skills、prompts 和平台入口中，容易形成多份 SSOT、跨平台漂移和大型单 task。必须先建立仓库级强制原则，再独立建设通用闭环合同与 Canonical 分发基础设施，最后改造具体 skills 和 workflow。

## 目标

只修改根 `AGENTS.md`，建立 Skill-first 闭环流程模块化强制规范：

1. `.trellis/workflow.md` 是全局 phase 顺序、mandatory skill invocation、跨 skill transition 和 fail-closed stop 的唯一 SSOT。
2. 每个可独立命名的完整步骤由一个 step-local skill 作为内部行为 SSOT；workflow、command、prompt、breadcrumb 和平台 launcher 不得复制 skill 内部步骤。
3. Mandatory workflow step 必须由 workflow 按 stable skill id 显式加载，不得只依赖 frontmatter auto-match。
4. Skill 内部必须按“正向行为 → AI Review Gate → human confirmation（命中时）→ recorder/validator → typed exit”形成闭环。
5. AI 判断先发生；script 只能作为 executor、validator、recorder，不能决定 scope、充分性、pass/block、revision action 或 route。
6. Workflow 只消费稳定 external exits；每个 exit 必须有唯一 consumer 或明确 fail-closed stop。
7. Workflow mode 与 standalone mode 必须使用同一正向行为、AI Gate 和 script boundary；standalone mode 不得成为弱化门禁的旁路。
8. Skill id、external exit id、schema id 和 script command 是团队公共 API；破坏性调整必须迁移或新建 id。
9. Task/request/private/runtime state 不得写入公共 skill package；pre-task 结果保持 side-effect-free，task 创建后只写 task-local tracked artifact。

## Skill 命名

Guru Team 新增公共 workflow skills 使用：

```text
guru-<action>-<object>
```

- 不包含只属于某个 workflow 的 phase number。
- 不使用无法表达行为对象的 `gate`、`handoff`、`helper`、`utils`。
- Action 与 object 必须让独立调用者仅从 id 判断主要用途。
- 不复用 Trellis 官方 bundled skill id。

## 强制 Skill 化条件

一个 workflow step 命中以下任一条件时，必须独立为闭环 skill：

- 有自身 entry preconditions、两个及以上 external exits 或明确 re-entry。
- 包含多轮 AI 交互、revision、recovery 或 internal loop。
- 同时包含 AI judgment Gate 和 machine recorder/validator。
- 被多个 workflow state、command、prompt 或平台入口复用。
- 能作为独立能力完成 planning、实现、check 和回归验收。

以下情况不得为了形式创建 skill：

- 单条 deterministic script 调用且没有 AI judgment。
- 只显示 breadcrumb 或调用下一个 stable skill 的薄 routing。
- 只重复其它 skill/Docs SSOT 的包装文本。

## Scope

要做：

- 只修改根 `AGENTS.md`，增加稳定、简洁、强制的 Skill-first 模块化原则。
- 审核新增原则与现有“Markdown 定义流程，脚本执行事实”“Companion Script 的允许角色”“必须保留的 AI 判断门禁”一致。

不做：

- 不设计或实现具体 skill 的完整闭环合同。
- 不确定 canonical package 目录、platform adapter、installer manifest 或 managed hash。
- 不修改 workflow、preset、overlay、skill、script、schema、README、requirements/spec 或测试。
- 不实现任何具体业务 skill 或 workflow chain。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。

上述通用闭环合同、Canonical package 和 deterministic distribution 由 #120 承接。

## Acceptance Criteria

- 根 `AGENTS.md` 明确 global workflow SSOT、step-local skill SSOT、explicit mandatory invocation、closed-loop 顺序、typed exits 和 script boundary。
- 根 `AGENTS.md` 明确 workflow/standalone mode 使用同一门禁。
- 根 `AGENTS.md` 明确强制 skill 化与禁止形式化拆分条件。
- 根 `AGENTS.md` 明确 stable naming/public API 和 package state boundary。
- 业务 diff 只有根 `AGENTS.md`。
- 新增原则不声称已交付未实现的 runtime、installer、schema、validator 或 skill。
- `git diff --check` 通过。
