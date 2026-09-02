# Technical Design

## 1. Design Principles

1. 四个 semantic Skill 继续独立拥有各自的判断与 typed exits；本任务只收敛每个 Skill 内的确定性调用面，不创建跨阶段事务 monolith。
2. AI 先完成 semantic review；stage facade 仅编排该 owner 已有 recorder/checker/executor/projection，不决定 scope、finding、route 或 readiness。
3. 同一 invocation、同一 authority identity、无中间 mutation 的事实可复用；跨 invocation、跨 Skill 或 mutation boundary 不复用 stale snapshot。
4. 可靠性能门禁使用 normalized operation counters；wall-clock 只用于区分 Agent、deterministic command、GitHub API 与外部 CI 的观察报告。
5. 新路径先证明与旧路径行为等价，再切换默认推荐入口；兼容命令和 stable public API 在迁移合同内保留。

## 2. Target Stage Shape

四个阶段采用相同的调用轮廓，但各自拥有独立 facade 和 package-local runtime：

```text
AI reads SKILL.md/contract and current public authority
  -> AI completes the stage semantic gate
  -> one read-only prepare/preview
  -> current exact confirmation when this stage owns a mutation boundary
  -> one stage-local facade invocation
       capture/recheck current facts
       record already-made semantic result
       validate objective bindings
       execute allowed deterministic transitions
       recover same-plan mapped exits internally
       project exactly one typed exit
  -> terminal exit stops the current Skill
```

Publication 没有独立 Git/GitHub mutation confirmation；其 facade 在 AI review 后完成 record/check/projection。Commit、Finalizer、Merge 继续使用各自独立的当前确认，不共享授权。

## 3. Package-Local Facades

### 3.1 Public Command Contract

每个 package 新增一个明确命名的 Happy Path command，或将现有 public invoke version 化为该 facade。最终命名由 implementation baseline 在不破坏当前 command registry 的前提下选择，但必须满足：

- `commands.json` 与 `interface.json` 只标记一个 `recommended_happy_path`；
- `SKILL.md` 给出完整正常调用序列、所需 public input 和 terminal exits；
- old record/check/execute/invoke commands 标记为 compatibility/testing/recovery，不作为 Agent 正常路径；
- facade 不接受授权字段，不接受预选 exit，不读取其它 Skill 的 private checkpoint。

若现有 invoke 已能安全扩展并保持旧 schema 行为，则通过新 input profile/version 收敛；若无法兼容，则新增 versioned command/schema。不得静默复用旧 ID 表达不同副作用语义。

### 3.2 Invocation Context

facade 创建 package-local `InvocationContext` 或等价 checked object，生命周期仅限当前进程：

```text
authority identity
normalized live facts
semantic-result locator supplied by current AI-owned step
objective validation receipt
operation counters
mutation/recovery receipt when applicable
```

它不写 tracked artifact，不跨 Skill 传递，也不成为 semantic authority。Mutation 前必须按现有合同执行一次 authoritative recheck；mutation 后必须重新捕获需要证明结果的事实，不能使用 mutation 前快照冒充结果。

## 4. Stage Designs

### 4.1 Commit

`prepare` 继续负责 AI path classification 的 deterministic canonicalization、Phase 2/task/HEAD binding、message normalization 和 candidate creation。确认后的 facade：

1. 重新校验 exact task/ref/HEAD/candidate freshness；
2. 使用 isolated index stage exact owned paths；
3. 运行真实 hooks 并验证 staged tree/message；
4. 创建 commit，并以 expected old ref 执行 `git update-ref`；
5. 刷新 live index，验证 parent/tree/path/message/worktree/unrelated preservation；
6. 检查已成功 mutation 的 recovery receipt，避免 stdout loss 后重复 commit；
7. 删除 candidate 与已消费 Phase 2 checkpoint并投影现有 `committed`/revision/block exit。

旧 `check-commit-messages`、`create-task-commit` 和 invoke 保留，用于 package tests、故障诊断及旧 installed caller。

### 4.2 Publication

AI 读取 live Issue ledger、Branch Review DTO、reviewed-content identity、PR metadata proposal、Docs SSOT、安全与部署影响后形成八维判断。Publication facade：

1. 一次构建 invocation-local publication snapshot；
2. 记录 AI 已完成的 dimensions/findings/conclusion；
3. checker 使用同一 snapshot 验证 branch-review/publication identity、ledger disposition、task/HEAD 和 output union；
4. projection 只消费 checked result，不再次读取完整 Git/GitHub/Trellis facts；
5. 输出现有 `ready`、`return_to_task_work` 或 `blocked` route。

metadata-only revision 重新进入 Publication owner，只失效受影响 dimensions；若 content、durable docs 或 reviewed commit 改变，则返回 task work/Branch Review 所有者，不在 facade 内自动降级。

### 4.3 Finalizer

Finalizer facade 以当前 preview plan 和 dialogue-local confirmation 为入口。它内部运行有界 transaction loop：

```text
validate confirmed plan identity
  -> execute current transition
  -> inspect checked typed result
  -> if mapped same-plan deterministic recovery/reprepare:
       rebuild exact input from package-owned state and live facts
       prove side-effect set and semantic authority unchanged
       continue
  -> else project terminal/re-entry exit
```

自动承接仅适用于当前 contract 已声明且无新选择的 `provenance_tail_required`、same-plan `reprepare_required`、stdout-loss recovery、已有 PR adoption 四类 route。以下任一变化立即停止并要求 owner 重做 preview/确认：close scope、PR title/body、base/head、publication/reviewed identity、side-effect set、new external choice 或 unknown/multiple/unmapped result。

loop 使用 package 自己的最小 transaction/checkpoint，不要求 Agent 手工读取 owner/runtime 或创建中间 review JSON。已有 #180/#191/#218/#311 correctness 与 recovery contracts 保持事实来源。

### 4.4 Merge

Merge facade 在确认后执行一个有界事务：

1. 捕获一次 pre-merge full snapshot：PR identity/state, base/head, expected SHA, checks/reviews, mergeability, repository policy, close keywords 与 expected Issue states；
2. checker 验证 AI gate result 与 snapshot/freshness/consumer；
3. 用 reviewed merge method 和 expected-head precondition 执行唯一 merge mutation；
4. 捕获一次 post-merge full snapshot：PR/merge commit/parents/message/remote base/Issue closure；
5. 恢复 mutation 已成功但 stdout 丢失的情况，不重复 merge；
6. 投影 `merged`、`closure_mismatch` 或当前兼容 terminal result，并清理临时 gate/body。

`closure_mismatch` 是 terminal：facade 报告默认/非默认 base、expected close scope、actual Issue state 和精确 follow-up，但不关闭 Issue。Workflow 的 terminal consumer 只展示结果并停止当前 Merge Skill。

## 5. CI Watcher

CI watcher 是 Merge package 可调用的独立 deterministic helper，不并入 Finalizer transaction：

- 输入为 repo、PR number、expected head SHA 和 required-check identity；
- 每次轮询验证 PR head 仍等于 expected head；
- 同一 watcher invocation 使用一种 polling mechanism，禁止并行/串行叠加 `gh run watch` 与 Agent while-loop；
- 输出为 `checks_succeeded`、`checks_failed`、`checks_pending_timeout` 或 `head_changed`；
- watcher receipt 支持同 head 恢复，但不跨 head 复用；
- watcher duration 单独计入 `external_ci_wait_ms`，不计入 stage orchestration overhead。

Watcher 只提供 facts，不决定 checks 是否充分、PR 是否 ready 或是否应 merge。

## 6. Measurement Model

### 6.1 Normalized Operations

baseline harness 对旧/新路径记录以下稳定类别，而不是匹配具体 shell 文本：

- `task.read`, `phase2.read`, `git.status`, `git.diff`, `git.ref.read`
- `github.pr.read`, `github.issue.read`, `github.checks.read`, `github.policy.read`
- `semantic.record`, `objective.check`, `public.project`
- `git.commit.mutate`, `git.ref.mutate`, `github.pr.mutate`, `github.merge.mutate`
- `recovery.inspect`, `watcher.poll`, `terminal.post_exit_operation`

每个 fixture 输出 before/after totals、按 authority 分类的 full snapshot 次数、mutation 次数和 terminal 后计数。硬门禁直接断言 command invocation 下降至少 50%、重复完整事实读取下降至少 70%、terminal 后计数为 0。

### 6.2 Wall-Clock Envelope

观测报告将总耗时拆成：

```text
agent_orchestration_ms
deterministic_command_ms
github_api_ms
external_ci_wait_ms
```

固定 fixture 或 5-10 次代表性运行计算 median。Wall-clock 未达目标时，报告环境与外部瓶颈；只要硬验收与 operation budget 通过，不将单次波动误判为实现失败。

## 7. Compatibility And Migration

1. Baseline 阶段冻结当前 old-path fixtures、typed outputs、mutation receipts 和 command registry。
2. 新 facade 使用新 command/profile/schema version，或在证明输入输出兼容后扩展现有 invoke；每个 public change 都提供 producer/consumer migration。
3. behavior-equivalence harness 对同一 fake/live-safe fixture 分别执行旧路径与新路径，比较 typed exit、DTO、blocker、mutation、recovery、temporary lifecycle 和 counters。
4. 只有全部硬等价断言通过，才更新 workflow、Skill 与平台 routing 的推荐 Happy Path。
5. 旧命令继续注册并通过 contract tests；后续删除需独立 migration Issue。

## 8. Failure And Recovery Matrix

| Condition | Expected behavior |
| --- | --- |
| Prepare/preview identity stale | 零 mutation，返回当前 owner 的 stale/re-entry route |
| AI semantic result missing/ambiguous | recorder/facade fail closed，不推断 pass/exit |
| Mutation-boundary facts changed | 零新 mutation，旧确认失效 |
| Deterministic step failed before mutation | 返回稳定 blocker，可用旧兼容命令有界诊断 |
| Mutation succeeded and output was lost | 从 exact live identity/receipt 恢复，不重复副作用 |
| Finalizer same-plan mapped recovery | facade 内自动承接，不增加确认 |
| Finalizer plan/scope/authority changed | 停止并重新 preview/确认 |
| Merge checks pending | 单一 expected-head watcher；稳定 pending/success/failure result |
| Merge succeeded, Issue not closed | terminal `closure_mismatch`，独立 closure follow-up |
| Any terminal exit | 当前 Skill 不再执行任何 operation |

## 9. Docs SSOT Plan

- Strategy: `ssot_first`。
- Durable workflow contract owners：`.trellis/spec/workflow/workflow-contract.md`、`skill-package-contract.md`、`data-contracts.md`、`companion-scripts.md`、`quality-guidelines.md`，用于定义 stage facade、invocation-local snapshot、operation budget、terminal stop、CI watcher 与兼容迁移。
- Product Requirements owner：`docs/requirements/guru-team-trellis-flow.md` 与 `docs/requirements/evolution/**`，记录用户可见 Happy Path、硬验收、性能观察目标与 #267 验证边界。
- Design owner：`docs/design/evolution/**`，记录四个 package-local facade、measurement model、watcher 和 migration design；若 Architecture owner 判定需要 task-local contribution，则按 `docs/architecture/06-governance/change-contract.md` 创建并在 Branch Review 后 promotion。
- Test owner：`docs/test/evolution/**`，记录 behavior-equivalence、operation-count、terminal-stop、recovery 与 installed/throwaway regression matrix。
- Package-local owner：四个 `trellis/skills/guru-team/packages/<skill>/references/contract.md`、`SKILL.md`、Interface/schema/commands/tests；通用规则只写 durable specs，stage-local 细节不复制到 workflow。
- Distribution projection：canonical 完成后通过 preset apply 同步 `.trellis/guru-team/**`、`.agents/skills/**`、`.codex/skills/**`、Claude/Cursor/shared destinations；安装副本不是 SSOT。
- `task.json`、ledger 与三份 planning docs 只保存 task scope/plan，不成为长期 product/design/test authority。

## 10. Architecture Impact

规划阶段的 Architecture review 结论为 `no_architecture_impact`：本任务改变四个公共 package 的推荐调用面和 package-local deterministic orchestration，但不改变 Architecture Baseline、五项设计原则、semantic owner、跨 Skill boundary、single-writer、架构决策或 GAP。Stage-local facade、最小 invocation state、兼容迁移与 operation budget 均直接承接现有 authority，因此不创建 task-local Architecture contribution 或 ADR；implementation discovery 若扩大这些边界，必须重新进入 Architecture owner。

## 11. Rollback

- Happy Path activation 是 package/workflow/registry/projection 的一致切换；任一 behavior-equivalence 或 installed validation 失败时，保持旧路径为默认。
- facade 可按 package 独立回滚，但 public schema/profile migration 必须 producer/consumer 一致回滚。
- 旧 commands、fixtures 和 schemas 在本 task 内不删除，因此回滚不要求业务仓库数据迁移。
- 无数据库、secret、deployment、container、Kubernetes 或基础设施迁移。
