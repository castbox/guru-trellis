# #180 压缩 Finalizer 与 PR 合并闭环，并以 #174 回放验证最少确认

## Goal

把 Guru Team 从最后一次 reviewed content commit 到 PR 合并、Issue 自动关闭的流程收敛为 AI-first 闭环：AI 直接消费 live Git/GitHub/Trellis facts，仅保留有直接 consumer 的最小状态；已有 Open Issue 的正常路径只需要 workspace/task、Finalizer、merge 三次 `确认继续`，且不减少语义门禁、外部验证或 fail-closed 约束。

## Background And Confirmed Facts

- Live authority 是 `castbox/guru-trellis#180`；它仍为 Open，且无评论改变当前范围。
- #179、#181、#191 已合并关闭，是本任务的已满足前置；#174/PR #176 仅提供 immutable replay evidence，本任务不修改、不重新打开也不重新关闭它们。
- 当前 global graph 为 14 个 mandatory Skills、54 个 exits、31 个 workflow/stop targets；`guru-finalize-task:published` 直接进入 finish response，没有 post-publication merge owner。
- 当前 Finalizer 使用 schema 3.0 `closeout-plan.json` 绑定发布 payload、transaction projection、恢复和 archive，并在终态长期保留；`marketplace-verification.json` 仍保存完整执行与语义证据。
- 当前 `guru-create-task-commit` 在 exact staging 和 semantic gate 后仍把普通本地 commit 当作 routine confirmation。
- GitHub 读写的唯一通道是 authenticated `gh`/`gh api`；Git transport 的唯一通道是 `git`。不得使用 GitHub App、MCP、connector 或 browser fallback。
- Markdown workflow/Skill 负责语义判断与路由；Python/shell 只负责 deterministic executor、validator 和最小 recorder。

## Requirements

### R1. 最小 Finalizer Transaction State

- 删除 `closeout-plan.json` 作为 tracked/archive/public authority 的当前合同与所有 current production 依赖。
- Finalizer 在当前会话能完成时不持久化 transaction state；需要 re-entry 时，只能写 owner-private、gitignored、task-scoped 的最小 transaction state。
- transaction state 只保存无法安全重推导且恢复下一 deterministic transition 必需的 identity、immutable publication input 和 stage；Git/GitHub/Trellis live facts、完整扫描、review history、授权、命令日志和冗余 digest bundle 不得进入。
- terminal `ready_for_merge` 必须删除 Finalizer 临时 state、gate、request 和 superseded files；`blocked` 仅当已声明的同 owner recovery consumer input schema 把该 state 列为必需输入时保留最小 current state，其余 blocker 删除私有状态；archive 不保留 transaction state。
- `finish-summary.json` 仅因 archived change-context 的直接 consumer 保留最小长期索引/摘要；不得重新引入 `context-discovery.json`、`finish-summary-index.json`、`pr-body.md` 或同义 handoff。

### R2. Immutable Ref Verification Exactly Once

- 对相同 target repository、immutable pushed ref、`branch_review_commit`、`publication_head`、extension source commit 和 capability profile，marketplace verification 只执行一次。
- executor 成功但 stdout 捕获失败时，Verifier 必须先从 command exit、remote/ref、isolated checkout 和 owner state 恢复；只有 identity 改变或证明不足时才重跑缺失验证。
- 后续 Finalizer consumer 直接消费 checker-passed 最小 verification result，不重新运行已通过的 command matrix，也不以普通 stale/re-entry/mapped exit 制造 `verification_required` 循环。
- 长期 verification artifact 只保留无法重推导且有历史/发布 consumer 的最小 identity、profile、结论、未验证边界和稳定结果 ref；完整 command/asset evidence 留在短生命周期 private runtime 并于消费完成后删除。

### R3. Finalizer Public API Migration

- 当前 `published` 语义迁移为 `ready_for_merge`：只表示唯一 PR 已发布、Ready、与 expected head 对齐，且 close issues 在 merge 前仍为 Open。
- Finalizer、finish launcher、workflow 和 companion scripts 不得调用 Issue close API/CLI；`close_issues` 只用于 PR body 的 `Closes #<n>`。
- 保留旧 `published` schema/example 作为 immutable legacy compatibility assets；current registry/interface/workflow 只选择 `ready_for_merge`，并在 contract/docs/tests 中提供显式迁移规则。legacy payload 不得静默进入 current route。
- `ready_for_merge` DTO 只携带 post-publication consumer 不可避免的 PR identity 与 expected head identity，不携带 transaction、review history、授权或长篇 handoff。

### R4. 独立 `guru-merge-task-pr` Closed Loop

- 新增 active stable Skill `guru-merge-task-pr`，`judgment_mode=semantic`，current exits 恰为 `merged`、`merge_blocked`、`closure_mismatch`。
- workflow mode 唯一消费 Finalizer `ready_for_merge`；standalone/re-entry 从 repo-bound PR URL/number 与 live GitHub facts 重建相同 entry evidence。
- 该 route 不进入 Phase 0、不调用 `guru-sync-base`、不 update/rebase PR branch、不同步本地 `main`、不清理 worktree/branch/task runtime。
- AI gate 必须读取并判断 PR Open + Ready、repo/base/head、expected head SHA、required checks/reviews、mergeability、repository merge policy、close keywords 与当前待关闭 Issue 状态。
- gate 通过后展示一次精确 merge action，并接受统一短语 `确认继续`；不得要求用户复制 SHA、digest、PR 编号或重新描述合并意图。
- deterministic executor 使用 policy 唯一确定的 merge method 与 expected head precondition 执行；identity、scope、method 或 authority 改变时旧确认失效。
- 合并后只读验证 PR=MERGED、actual head/merge identity、close issues=CLOSED/COMPLETED，且每个 Issue `closed_at >= PR merged_at`。
- GitHub 未按 close keyword 自动关闭时返回 `closure_mismatch`，不得自动手工关闭；merge 前 live gate 不满足返回 `merge_blocked`。

### R5. 普通 Task Commit 自动承接

- `guru-create-task-commit` 在以下事实全部成立时，semantic gate 后自动执行普通本地 commit，不 routine pause：专用 issue/task worktree 和 branch、非 default/protected/shared/other-task branch、remote branch 和 Open/Draft/Ready PR 均不存在、scope/purpose 唯一且无 authority 变化、Phase 2 或 finding closure current、exact staging 仅含 task-owned paths、commit message 可唯一推导、无 history rewrite 或特殊 Git operation。
- 自动 commit 后报告 commit SHA、实际 staged paths 和 mapped `committed` exit，并自动进入 Branch Review。
- same-scope restaging/fix/re-entry 自动承接现有恢复 route；共享/已发布/受保护分支、历史改写、scope 变化、无关文件或真实选择必须 fail closed 或请求当前精确选择。
- 不持久化自动提交授权、用户确认或授权 digest；不得把 ineligible commit 泛化为 `verification_required`。

### R6. 统一确认预算

- 已有 Open Issue happy path 恰为三次 `确认继续`：workspace/task、完整 Finalizer side-effect set、expected-head merge。
- 尚无 Issue happy path 恰为四次：先增加一次独立 Issue creation confirmation，再执行上述三次。
- Planning approval、task activation、implementation、Phase 2 check、Branch Review、routine local commit、mapped exit、stale reprepare 和只读 recovery 不增加 routine confirmation。
- Finalizer 与 merge 的确认不可合并；每次确认只绑定当前对话已展示的唯一 live plan，授权永不持久化。

### R7. Canonical、Dogfood 与安装一致性

- 同步 canonical workflow、dogfood workflow、registry/interface/package、consumer schemas、runtime、preset managed assets、extension manifest、README/spec 和 Codex/Claude/Cursor Guru entries。
- 新 graph 的 invoke/exit/target 数量、唯一 consumer、projection、current production manifest、eval corpus、source/installed package validation全部一致；unknown/multiple/unmapped exit fail closed。
- 修改 overlay/preset 后运行 canonical apply 和 dogfood drift checker，逐个处理 `.new`/`.bak`；不得修改 official Trellis 或 `node_modules`。

### R8. #174 受控端到端回放

- 使用 clean throwaway repository/installation 和受控 fixture，从最后一次 reviewed content commit 开始回放；历史 #174/PR #176 仅作为 immutable evidence，不作为可变 authority。
- 记录并机器断言 Branch Review 次数、confirmation 次数、commit confirmation 次数、verification execution 次数、Finalizer/merge exits 和 terminal artifacts。
- 回放必须覆盖 `ready_for_merge -> merge preview -> expected-head merge -> GitHub close keyword -> post-merge verification` 的真实事件顺序。
- 回放不得把本地 base 三方一致或合并后同步本地 `main` 当作前置条件。

## Docs SSOT Plan

- Strategy: `ssot_first`。
- 先更新 `.trellis/spec/workflow/{workflow-contract,skill-package-contract,data-contracts,companion-scripts,quality-guidelines}.md`，将新 transaction、verification、Finalizer migration、merge Skill、commit confirmation matrix 和 graph closure 写成 durable SSOT。
- 再按 SSOT 修改 canonical package/runtime/workflow；随后同步 `.trellis/workflow.md`、installed dogfood packages、preset/overlay、README 与三平台入口。
- Branch Review 只验证最终 reconciliation，不在 review 阶段首次合并 spec 或 docs。

## Acceptance Criteria

- [ ] AC1: current production 不创建、读取、移动、归档或注册 `closeout-plan.json`；legacy compatibility fixture 仅用于显式 migration/rejection 测试。
- [ ] AC2: terminal state 无 superseded Finalizer/Verifier input、checkpoint、result；archive 只含有直接长期 consumer 的最小文件。
- [ ] AC3: 相同 immutable pushed identity 的 marketplace executor 计数为 1；stdout 丢失恢复不整套重跑，identity 改变时才重新验证。
- [ ] AC4: Finalizer current exit 为 `ready_for_merge`，PR 已 Ready 且 expected head 一致，所有 close issues 在 merge 前仍 Open。
- [ ] AC5: `guru-merge-task-pr` 三个 exits、consumer projection、workflow/standalone entry、repo-bound `gh` read/mutation 和 expected-head merge 均通过 schema、contract 和 behavior tests。
- [ ] AC6: merge 成功后 PR=MERGED，GitHub 自动关闭全部 close issues，且 `closed_at >= merged_at`；异常得到 `closure_mismatch` 且无手工 close mutation。
- [ ] AC7: eligible task/finding-fix/revision commits 的 routine confirmation=0，exact staging 正确；不合格分支、历史改写、scope/authority 变化和无关文件保持 fail closed/真实选择边界。
- [ ] AC8: Open Issue 回放 confirmation=3，新 Issue 回放 confirmation=4；Planning、checks、review、commit、mapped recovery 均不增加次数。
- [ ] AC9: PR body 仅对 ledger `close_issues` 使用 `Closes #<n>`；related/followup 无 close keyword；Finalizer/launcher/runtime 无 Issue close mutation。
- [ ] AC10: graph closure、registry/interface、current production manifest、evals、canonical/dogfood/installed package和 Codex/Claude/Cursor discovery 一致。
- [ ] AC11: targeted unit/integration tests、source/installed package validators、ownership/drift、clean marketplace init、existing-project preview/switch、preset apply/reapply、official update/reapply、recursive zero-sidecar 全部通过。
- [ ] AC12: #174 controlled replay 证明一次完整 Branch Review、一次 immutable verification、零 commit confirmation、一次 Finalizer confirmation、一次 merge confirmation和无 terminal transaction artifacts。
- [ ] AC13: independent current-HEAD semantic Branch Review 对完整 `origin/main...HEAD` 无未关闭 P0-P3 finding。

## Out Of Scope

- 修改、重新打开或重新关闭 #174/PR #176，或复用其旧 worktree/branch/task runtime 作为 authority。
- 删除真实 external pushed-ref verification、Phase 2 check、Branch Review、Publication review 或 merge readiness semantic gate。
- 由 Finalizer/merge script 手工关闭 Issue，或自行模拟 GitHub close-keyword 机制。
- 把 merge 扩张为 Phase 0 intake、base refresh、branch update/rebase、本地 `main` 同步或资源清理。
- 自动 commit 到 default/protected/shared/published/scope-unknown branch，或授权 amend/rebase/reset/cherry-pick/merge commit/tag/signing change/force-push。
- 合并 Finalizer 和 merge 两次确认，或持久化授权信息。
- 恶意 actor、对抗输入、故意伪造/篡改、竞态、锁、TOCTOU、额外 fault injection、跨 OS crash consistency。

## Open Questions

无。Issue、live repository contracts 与已合并前置已足以进入实现规划。
