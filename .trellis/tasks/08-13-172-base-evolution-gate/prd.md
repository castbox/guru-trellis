# #172 Base Evolution Gate 与集成就绪合同

## 目标

为在途 Trellis task 建立统一、事件驱动的 Base Evolution Gate。系统必须分别维护 authority validity、task-content validity 与 integration readiness；base SHA 变化本身不能产生 stale、reset、finding、pass 或 block 结论。

## 权威与现状

- Live authority：<https://github.com/castbox/guru-trellis/issues/172>，当前为 open。
- 任务基线：`main@40423d26908ead544285ee876ed44d86b5709f05`，包含 #169 的 semantic retrieval SSOT。
- #169 已由 PR #216 合并；新 Gate 必须引用 `.trellis/spec/workflow/semantic-retrieval.md`，不得复制中英文词表或查询策略。
- 当前仓库有 #179/#180 引入的 Publication/Finalizer 局部 base-evolution 恢复，但没有跨 active-task stable boundaries 的统一 pair owner、guard、六出口路由或 bounded continuity profile。
- #195 已把 public Skill runtime 收敛到 package-local ownership；新 Skill 不得读取其它 package private runtime，也不得恢复 shared compatibility dispatcher。
- #98 是 related umbrella，不是 duplicate。Issue Scope Ledger 只关闭 #172；#53、#98、#106、#132、#156、#157、#161、#164、#169、#179、#180 均为 related/history。

## 需求

### R1 三条独立时钟

实现和文档必须分别表达：

1. Authority clock：Issue、需求、Docs SSOT、acceptance 与用户确认的 scope。
2. Task-content clock：task branch 自身 planning、代码、测试和文档。
3. Integration clock：一个精确 `(task_head, base_head)` candidate 的 build、test、review 与 merge readiness。

任何时钟失效只能定向返回其 owner；integration pair 变化不能自动否定仍绑定同一 task-content HEAD 的 planning、Phase 2、Branch Review 或 Publication 结论。

### R2 廉价 pair guard

在每个 eligible boundary 先运行同一 deterministic guard：

- 每个边界对 selected base 最多一次 live ref observation。
- base 未变化时直接恢复原 `resume_target`，不调用 semantic Skill、不读 GitHub/Docs/history、不写 tracked/ignored artifact、不交互。
- 同一 `(task_head, base_head)` 的当前短生命周期结果只复用一次，不重复 scan/review。
- 两个边界间多个 base merge 作为一个累计 `old_base...new_base` delta 处理。
- task content 变化后形成新 pair，旧 integration 结论不得复用。

Guard 只观察 refs、pair 和 owner-private current checkpoint，不决定语义影响、证据充分性或 route。

### R3 `guru-reconcile-task-base` public Skill

新增 stable Skill id `guru-reconcile-task-base`，`judgment_mode=semantic`，拥有独立 contract、commands、runtime、schemas、examples、evals 和 tests。完整闭环为：

1. 校验 task/base identity、caller `resume_target` 与新 pair。
2. 读取 live authority、approved planning、task diff、累计 base delta、由 semantic-retrieval SSOT 选中的 Docs/code/tests 与 PR 状态。
3. 引用 #169 semantic retrieval SSOT 完成最小充分影响检索。
4. 分别判断 authority、task content 与 integration-only impact。
5. 构造或检查临时 integration candidate；不 merge/rebase task branch，不创建持久 ref/commit。
6. 选择与影响面匹配的 build/test/static validation。
7. 完成 AI Review Gate，返回一个且仅一个 typed exit。

六个 exit 各有独立最小 schema 与唯一 consumer：

- `reconciled` -> workflow `guru-base-reconciliation-router`，恢复原 `resume_target`。
- `review_continuity_required` -> `guru-review-branch` bounded base-continuity profile。
- `implementation_required` -> implementation owner，完成修改后进入 fresh `guru-check-task`。
- `planning_stale` -> Planning owner。
- `scope_confirmation_required` -> `guru-clarify-requirements`。
- `blocked` -> fail-closed stop。

### R4 Eligible boundaries 与路由

以下当前稳定边界必须使用同一 guard/router：

- `guru-approve-task-plan:approved` -> task activation。
- `guru-check-task:passed` -> `guru-create-task-commit`。
- `guru-create-task-commit:committed` -> `guru-review-branch`。
- `guru-review-branch:passed` -> `guru-review-task-publication`。
- `guru-review-task-publication:ready` -> `guru-finalize-task`，位于首个 publication side effect 之前。
- Finalizer 检测到 base-only mismatch -> `base_reconciliation_required` -> Gate -> 原 same-plan route。

未来 #106 merge authorization 只预留 consumer 合同，不在本任务实现 merge side effect。Workflow、prompt、command、breadcrumb 和 launcher 只拥有 mandatory invocation、guard/router 与 typed exits，不复制 Skill 内部判断。

### R5 Bounded Branch Review continuity

`guru-review-branch` 新增 bounded base-continuity profile：

- 复用同一 task-content HEAD 的既有 semantic review。
- 只独立审查由 semantic-retrieval SSOT 判定命中的 `old_base...new_base` delta、临时 candidate、冲突解决和受影响验证。
- 不伪造 reviewed HEAD，不要求 task branch 因 base merge 产生新 HEAD，不重放无关 task review。
- 发现 task content 必须改变时定向进入 implementation；发现 planning/authority 改变时返回真正 owner。
- continuity pass 只更新当前 pair 的 integration readiness。

### R6 重复 owner 迁移

以 current consumer inventory 为准，删除或委托被 Gate 替代的行为：

- `guru-sync-base` 保持 pre-task/standalone base sync，不进入 active-task 周期。
- Discovery/Clarification 不因 base-only drift 完整重跑 Intake 或自动解释为 scope change。
- `guru-check-task` 不得仅因 base identity 变化返回 `planning_stale`。
- Branch Review 不得因 base-only HEAD 差异自动丢弃 task-content review。
- Publication 的 stale 只表示自身 content/metadata evidence 过期。
- Finalizer 新增 `base_reconciliation_required`，不再把 base-only mismatch 映射为 `publication_review_stale` 或 generic `blocked`。

迁移必须针对 current schemas/typed exits/installed projections/private state，不批量重写既有 active tasks，不恢复 #195 删除的共享单体。

### R7 Public I/O 与状态边界

- 每个 exit 独立 output schema；public DTO 只携带唯一 consumer 无法重建的最小 pair/route identity。
- Live Git/GitHub facts、完整 scan/review、candidate、验证历史和 digest 一律保存在 owner-private runtime；R7 明确列出的最小 public projection 是唯一例外。
- 同一 pair 的复用结果只能是 gitignored、短生命周期且有明确下一 consumer 的 checkpoint；consumer 完成后删除。
- 不新增 tracked base-evolution report、handoff、assignment/liveness、授权记录、raw search report 或全链 hash bundle。
- 不持久化用户授权。Digest 只服务一个局部 deterministic consumer。

### R8 分发、兼容与验证

- 更新 canonical workflow、canonical package、registry/manifest、consumer packages、dogfood `.trellis/workflow.md`、`.agents/skills`、`.codex/skills`、`.claude/skills`、`.cursor/skills` 与声明支持的平台入口。
- 使用 preset apply/reapply 同步，不把 dogfood copy 当源头；处理 `.new/.bak` 并保证 overlay/managed-copy drift 为零。
- clean marketplace install、workflow init/preview/switch、preset apply/reapply、Trellis update/upgrade、platform discovery/behavior 必须真实执行。
- #132/#161 历史事件只能作为 current package-local runtime 的 replay fixture；旧 HEAD/digest 不是 current authority。

## 验收标准

- AC1：新 Skill 是完整 package-local semantic closed loop，六 exit 各自有最小 schema、唯一 consumer、workflow 与 standalone eval。
- AC2：unchanged pair 在所有 eligible boundaries 均为 0 semantic invocation、0 GitHub/Docs/history scan、0 artifact、0 interaction。
- AC3：N 次 base merge 在下一稳定边界最多形成一次累计 delta review，owner 执行中无 polling/抢占。
- AC4：覆盖 unchanged、unrelated delta、related-compatible/equivalent integration、build/test failure、textual/semantic conflict、authority change、upstream supersedes task、PR-ready base advance 与 non-ancestor/history rewrite。
- AC5：base SHA/path 命中本身不能生成 planning stale、finding、pass、reset 或 block；证据不足仍 fail closed。
- AC6：bounded continuity 不重放无关 task review；真实 task/planning 变化仍完成 fresh implementation、Phase 2、commit 与 Branch Review。
- AC7：Finalizer `base_reconciliation_required` 与 Publication content/metadata stale 在 schemas、runtime、eval 与 workflow route 中完全分离。
- AC8：既有 active task、旧 context/review/publication/finalizer state 只做一次最小 current migration，无 tracked rewrite/self-dirty。
- AC9：#132/#161 replay 在 current package-local runtime 下不伪造 state/HEAD，能自动恢复原 route或定向 implementation。
- AC10：被替代、冲突、重复或无 consumer 的 old fields/helpers/wrappers/schemas/examples/tests 被删除，public API migration 有明确版本合同。
- AC11：canonical/installed/dogfood/Shared/Codex/Claude/Cursor 与所有声明平台一致，registry/workflow count 与真实 graph 匹配。
- AC12：clean marketplace/preset install、init/preview/switch、apply/reapply、update/upgrade、managed hashes、`.new/.bak`、legacy cleanup、drift 和 README commands 全部通过。
- AC13：不生成 `implementation-handoff.md`、tracked review 文书循环、用户授权 artifact 或周期性 freshness 机制。
- AC14：PR/Issue close scope 只包含 #172。

## 非目标

- daemon、webhook listener、后台 polling、per-prompt freshness 或 agent 中途抢占。
- Gate 自动 merge/rebase、commit、push、PR、Ready、merge 或 Issue mutation。
- 修改 Trellis upstream、全局 npm 包或 `node_modules`。
- 实现 #106 Merge Executor/ruleset、#164 风险分级或 #53 tracked metadata 假冲突。
- 重做所有已关闭 Skill 的内部语义。
- 恶意 actor、故意伪造/篡改 state、对抗输入、锁、TOCTOU、竞态压力、fault injection、crash consistency 或跨 OS 原子性。

## Docs SSOT Plan

- 更新 `.trellis/spec/workflow/{workflow-contract,skill-package-contract,data-contracts,companion-scripts,quality-guidelines}.md` 的 canonical preset source；只在对应 owner 写一次长期合同。
- `semantic-retrieval.md` 保持唯一检索 SSOT，仅被新 Skill 引用。
- 更新 preset/workflow README 的 public package、安装、升级和操作说明，但不复制 step-local Skill 内部流程。
- 同步 dogfood installed specs 和 platform projections；不得手工维持与 canonical 不同的第二份规则。

## 开放问题

无。Live Issue、current code/tests、#169 SSOT、#179/#180 历史兼容与 #195 package-local 边界足以确定实现。
