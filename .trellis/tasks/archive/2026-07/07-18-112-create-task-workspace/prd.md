# #112 实现 `guru-create-task-workspace` 并完成 Intake workspace 闭环

## 目标

把 `guru-review-change-request:ready` 之后的 Issue、branch、worktree 与 Trellis
task 创建收敛到 active semantic Skill `guru-create-task-workspace`。该 Skill 必须消费
当前 checker-passed Intake evidence，完成命名、assignee、副作用计划、用户确认、精确
执行与结果校验，并将 portable evidence 写入新 task 的 tracked task-local artifacts。

## 来源与已确认事实

- Primary issue：<https://github.com/castbox/guru-trellis/issues/112>。
- 当前 task 同时承接 #99 与 #54；combined acceptance 全部通过后关闭 #112、#99、#54。
- #98 与 #53 保持 open；#132 负责 legacy Stage 0/platform-entry 收敛和最终关闭。
- #139 已合并到 fresh `main`；本 task 从
  `7036dc4ca92a376288564345c98f6c55d8dfe6b8` 创建，旧 #112 task 的 planning、代码、
  approval、Phase 2、Branch Review 与测试 evidence 全部废弃。
- Production registry 当前把 `guru-create-task-workspace` 标记为 `planned`，仓库没有该
  package；workflow 在 `guru-review-change-request:ready` 后按 missing-Skill gate 停止。
- 当前 `prepare-task` mutation path 仍通过 `.trellis/.developer` 推断 assignee，并在
  worktree 中复制或创建 developer identity；这与 #99/#54 的目标冲突。
- 本机 `trellis 0.6.5` 的 `-u/--user` 是官方 developer identity 参数。官方 clean init
  即使省略 `-u`，仍会从 Git 配置解析用户并创建 `.trellis/.developer` 与 workspace；
  Guru preset 必须保持官方支持不变，同时证明自身不读取、不创建、不恢复这些路径。
- Trellis 官方 custom workflow 文档确认：流程语义写入 `.trellis/workflow.md`；hook 与
  script 不承载 AI 判断。Marketplace workflow 与 Guru preset package 分发是两条独立安装链。

## 需求

### R1：公共 Skill 与 package 生命周期

- `guru-create-task-workspace` 必须从 `planned` 提升为 `active`，稳定 id 不变。
- Canonical package 必须位于
  `trellis/skills/guru-team/packages/guru-create-task-workspace/`，包含短 `SKILL.md`、
  interface、完整 contract、closed schema、去身份化 example、thin wrappers 与 contract tests。
- Package 必须声明 `judgment_mode=semantic`，并执行
  `forward_behavior -> ai_review_gate -> conditional_human_confirmation -> recorder_validator -> typed_exit`。
- Skill id、external exit、schema id 与 runtime command 均属于 Guru Team 公共 API；
  破坏性调整必须使用新 id 或提供迁移合同。

### R2：workflow 与 standalone mode 同约束

- Workflow mode 必须消费当前的 `guru-sync-base:synced`、
  `guru-discover-change-context:context_ready`、`guru-clarify-requirements:clear`、
  `guru-review-contract-wording:pass`、`guru-review-change-request:ready` evidence。
- Standalone mode 必须执行同一组 prerequisite、freshness、target authority、confirmation、
  recorder、executor 与 result checker 门禁。
- 任一 mandatory evidence 缺失、旧 schema、stale、target mismatch 或 consumer mismatch
  必须返回 `refresh_review`，并列出必须重跑的 prerequisite Skills；禁止绕过 review。

### R3：语义 owner 与副作用计划

- AI 必须拥有 task scope 展示、semantic branch/workspace/task 命名、assignee route、
  confirmation need、AI Review Gate、typed exit 与 recovery route 判断。
- 在副作用前，AI 必须展示 exact plan：repo、final issue/draft、GitHub mutation、base、branch、
  worktree、task、assignee、task-local artifacts、ignored runtime writes、executor command 与停止条件。
- GitHub issue mutation 与 workspace/task mutation 使用两个独立确认。Draft 创建调用只取得
  GitHub mutation 确认；issue 创建成功后本次调用立即停止，不复用 workspace/task 确认。
- 用户取消时返回 `cancelled` 且零副作用。用户要求改变 target、duplicate disposition 或
  closed-state disposition 时返回 `refresh_review` 且零副作用。

### R4：final target authority 与 issue 创建

- Skill 只能展示和消费 `guru-clarify-requirements` 已决定的 final open issue 或 reviewed draft；
  禁止在本 Skill 中选择 duplicate、改选 target、reopen issue 或创建 follow-up target。
- Reviewed draft 创建必须使用 exact reviewed title/body/labels，创建前重验 confirmation 与
  source digest，创建后立即重读 live issue。
- `created_issue_binding` 必须绑定 repo、number、canonical URL、`state=open`、title/body digest、
  `updated_at`、reviewed draft id/digest 与 creation confirmation digest。
- Issue 创建并通过 checker 后必须返回 `refresh_review`，从 `guru-sync-base` 针对新 open issue
  重跑完整 Intake chain；同一调用禁止创建 branch、worktree 或 task。
- 重入时必须验证 final issue 与 binding/draft identity 一致；普通失败恢复只能复用同一 live
  issue，禁止再次创建语义重复的 issue。

### R5：assignee 固定解析顺序

Guru task 创建必须得到非空 assignee，并显式传给
`task.py create --assignee <login>`。解析顺序固定为：

1. 显式输入 assignee。
2. Source issue 恰好一个 assignee 时使用该 GitHub login。
3. Source issue 没有 assignee 时读取当前 GitHub login。
4. Source issue 有多个 assignee，或 GitHub login 无法解析时，AI 向用户询问一个 assignee。

未得到 assignee 时禁止创建 issue 之外的任何 workspace/task 副作用。Assignee 只进入
`task.json`、portable task context 与审计字段，禁止成为目录 namespace 或 developer identity。

### R6：deterministic recorder、executor 与 checker

- Runtime 必须记录 canonical plan facts、upstream evidence digests、confirmation digests、
  naming、assignee、exact side effects 与 plan digest；pre-task plan 只经 stdout 传递。
- Exact executor 必须在每个 mutation 边界重验 base、live target、upstream evidence、plan digest
  与当前 Git/worktree/task facts；script 不判断 scope、命名质量语义或 route intent。
- Result checker 必须校验 created issue binding，或校验 branch/worktree/task、artifact bytes、
  schema、digest linkage、Git tracking、ignored runtime 与 workspace boundary。
- 普通中断后的重入必须复用 identity 完全一致的 branch/worktree/task；名称、base、issue、
  task locator 或 artifact content 冲突时返回 `blocked`，不得覆盖现有内容。
- Legacy `prepare-task` 不得保留第二条绕过 prerequisite review 的 mutation route。

### R7：portable task-local artifacts 与 runtime boundary

Task 创建成功后只能写入以下 tracked task-local Intake artifacts：

- `task-start-context.json`
- `issue-scope-ledger.json`
- `context-discovery.json`
- `issue-review.json`

要求：

- `context-discovery.json` 与 `issue-review.json` 必须保持 checker-passed canonical bytes。
- `task-start-context.json` 必须记录 final source-issue binding、prerequisite digest linkage、
  assignee、portable workspace/task identifiers 与 repo-relative artifact locator。
- `issue-scope-ledger.json` 必须承接 readiness scope conclusion 的 close/ref/followup 投影。
- Artifact 禁止包含绝对路径、existing worktrees、runtime path、developer identity path、完整
  preflight、secret、credential、签名 URL 或私有原始记录。
- 本机 mapping 只写 gitignored `.trellis/.runtime/guru-team/**`，删除后能从 Git/worktree/task
  facts 重建；禁止新增 tracked repo-level cache、fixed handoff、workspace journal 或 index。

### R8：取消 Guru developer identity 前置

- Guru preset apply/update/reapply 禁止读取、创建或恢复 `.trellis/.developer` 与
  `.trellis/workspace/**`。
- Guru task workspace executor 在 source 和 target 均缺失 `.trellis/.developer` 时必须按 R5
  创建 task；错误信息禁止要求运行 `init_developer.py`。
- Worktree 创建禁止复制或初始化 `.trellis/.developer`。
- README/install prompt 禁止要求 developer name，禁止使用 `TRELLIS_USER` 或 `trellis init -u`。
- 文档必须区分官方 Trellis identity 支持与 Guru 前置条件；本任务不删除官方脚本，不修改
  upstream-owned Trellis 文件，也不阻止用户单独使用官方 workspace journal。

### R9：thin Intake workflow 与 typed exits

Canonical workflow 固定为：

```text
tool-free route
-> guru-sync-base
-> guru-discover-change-context
-> guru-clarify-requirements
-> guru-review-contract-wording
-> guru-review-change-request
-> guru-create-task-workspace
-> Phase 1
```

- Workflow 只保留 stable id、entry evidence、mandatory invocation、typed exits、唯一 consumer
  与 fail-closed stop；禁止复制 package 内部 questions、naming、assignee、confirmation、schema
  或 executor 规则。
- `retarget_context` 必须回到 `guru-sync-base`，针对 selected issue 重跑完整 Intake chain。
- External exits 固定为：`created` -> Phase 1；`refresh_review` -> `guru-sync-base`；
  `cancelled` -> stop；`blocked` -> stop。
- Missing Skill、unknown、multiple、unmapped exit 或 consumer mismatch 必须 fail closed。

### R10：并行 task metadata 合并 Gate

Clean fixture 必须从同一 base 创建独立 task A 与 B，并完成以下步骤：

1. A、B 分别通过 production workspace executor 创建 branch/worktree/task 与四类 Intake artifacts。
2. A、B 分别生成 `finish-summary.json`，并通过 production task-local closeout 路径完成 active 到
   archive 的迁移。
3. A、B 分别提交完整 tracked diff，并记录 branch HEAD、diff range 与 changed paths。
4. Integration branch 执行 A -> B 合并，第二次合并不得因 Guru metadata 产生冲突。
5. 独立 integration branch 执行 B -> A 合并，第二次合并必须得到同一 metadata 结论。
6. 两个 diff 均禁止写 `.trellis/guru-team/handoff.json`、`.trellis/workspace/**`、
   `.trellis/.developer` 或其它 shared tracked runtime/index/cache。
7. AI Review evidence 必须确认 A 与 B 的 tracked Guru metadata path 交集为空。

该 Gate 只覆盖正常确定性 Git 合并；禁止扩张到并发进程压力、锁、原子写入、TOCTOU、
跨 OS、额外 fault injection 或恶意输入场景。

### R11：分发、安装、update 与 dogfood

- Canonical package 必须安装到 `.trellis/guru-team/skills/`、shared root 与已选择的
  Codex/Cursor/Claude roots，并通过 `run-skill-command` 绑定完整 extension runtime。
- `trellis/guru-team-extension.json` 必须同步 active ids、artifact schema ids、runtime commands、
  managed paths 与 patch version。
- Workflow marketplace、preset installer、README、durable specs、dogfood workflow、installed
  runtime 与平台 discovery copies 必须保持一致。
- 本任务禁止新增或改写 upstream-owned overlay；#132 独占 legacy overlay removal。
- Known managed update、unknown local edit、`.new/.bak`、source/installed validation、workflow
  reapply、preset reapply 与 clean throwaway 必须有自动化证据。

### R12：正常运行与数据边界

- 当前 scope 只覆盖正文列出的正常路径、常见操作错误、stale/mismatch、普通中断恢复、
  deterministic merge fixture 与 correctness/compatibility 边界。
- Hash、digest、freshness 与 live reread 只绑定版本和内容一致性，不构成 hostile-input
  security boundary。
- 仅靠手工伪造 artifact/hash/state 才能复现的场景属于 `out_of_scope`，禁止进入 acceptance、
  P0-P3 finding、required follow-up 或实现。
- 公共 package、schema、example、日志、task artifacts 与文档禁止包含 secret、private key、
  `.env`、数据库 URL、签名 URL、客户数据或本机绝对路径。

## 验收标准

- [ ] AC1：registry 把 `guru-create-task-workspace` 激活，完整 package/interface/schema/example/
  wrappers/tests 通过 source validation。
- [ ] AC2：workflow 与 standalone mode 的 prerequisite ids 一致，缺失或 stale evidence 只返回
  `refresh_review` 或 `blocked`，不存在 bypass route。
- [ ] AC3：AI Review Gate 与两类 confirmation 在 mutation 前完成；script 只记录、执行和校验
  deterministic facts。
- [ ] AC4：existing issue 路径只在 workspace/task 专用确认后创建或复用精确 workspace。
- [ ] AC5：reviewed draft 路径只创建一次 issue，生成 checker-passed binding，返回
  `refresh_review`，同一调用不创建 workspace/task。
- [ ] AC6：用户改变 target/disposition 时零副作用返回 `refresh_review`；取消时零副作用返回
  `cancelled`。
- [ ] AC7：assignee 四级解析矩阵通过；多 assignee 与 unresolved actor 在用户选择前零 workspace
  side effect。
- [ ] AC8：缺失 `.trellis/.developer` 时 task 创建成功，且 source/target 都不生成
  `.trellis/.developer` 或 `.trellis/workspace/**`。
- [ ] AC9：四类 task-local artifacts 的 bytes、schema、digest、trackability、portable path 与 final
  source-issue binding 通过 checker。
- [ ] AC10：runtime mapping 只位于 `.trellis/.runtime/guru-team/**` 且被 Git ignore；tracked diff
  不含 shared runtime/index/cache。
- [ ] AC11：`created`、`refresh_review`、`cancelled`、`blocked` 四出口各有唯一 consumer；missing/
  unknown/multiple/unmapped exit fail closed。
- [ ] AC12：A -> B 与 B -> A fixture 都通过，两个 task 的 tracked Guru metadata path 交集为空。
- [ ] AC13：README/install prompt 不要求 developer name；preset 在 identity/workspace 均缺失的
  initialized repo 中完成 apply/update/reapply 后仍不创建这些路径。
- [ ] AC14：canonical、installed、shared/Codex/Cursor/Claude copies、manifest、README、durable
  specs、workflow 与 runtime command inventory 无漂移。
- [ ] AC15：unit、package、preset、ownership、throwaway、dogfood drift、task validation 与
  `git diff --check` 全部通过，未处理 `.new/.bak` 集合为空。
- [ ] AC16：issue ledger 只关闭 #112、#99、#54；#98、#53 只作 related，#132 只作 follow-up。
- [ ] AC17：完整 diff 不含 malicious-input、threat model、stress concurrency、TOCTOU、lock、
  cross-OS、额外 fault injection 机制或用例。

## Docs 状态与影响

- docs state：`stale_docs`。
- Durable requirements/specs/README 仍把 `prepare-task`、handoff review 与 developer identity
  写成 active Intake 主路径，与本 task 的 Skill-first/no-developer 合同冲突。
- 同步策略、权威文件和 merge checkpoint 由 `design.md` 的 `Docs SSOT Plan` 独占定义。

## 范围外

- 不修改 Trellis upstream、全局 npm package 或 `node_modules`。
- 不新增或改写 upstream-owned Skill、Agent、Command、Prompt、Hook、runtime agent overlay。
- 不删除官方 `init_developer.py`、`.developer` 或 workspace journal 支持。
- 不实现 #129、#130、#131 或 #132 的 planning/check/review/platform-entry 收敛。
- 不关闭 #98、#53、#110、#111、#113、#114、#101、#128、#139。
- 不创建真实远程 PR 作为 merge fixture 的前置；使用本地 PR-equivalent Git merge。

## 阻塞问题

无。Live issue、fresh main、官方文档、当前 package/runtime/tests 与 prerequisite artifacts 已
确定实现边界。实现仍必须停在 post-planning approval 之后启动。
