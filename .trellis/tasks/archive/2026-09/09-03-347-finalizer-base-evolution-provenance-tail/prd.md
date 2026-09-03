# #347 Finalizer base evolution 后 provenance tail 恢复

## 1. Goal

修复 `guru-finalize-task` 的组合恢复缺口：旧 owner-private transaction 已停在
`ordinary_publication/push_content` 且未绑定 PR，远程分支与唯一同仓库 Open PR 仍位于旧 Publication HEAD；
当前 Publication HEAD 先吸收合法 base evolution，再追加一个由现有 provenance validator 接受的
manifest-only metadata tail。Finalizer 必须继续复用 existing-PR strict-ancestor recovery，恰好推送一次当前
Publication HEAD，不得把合法 metadata tail 误判为 business drift。

Live authority：GitHub Issue #347，2026-09-03 当前 Open 正文。

## 2. Confirmed Facts

- 当前 selected base 为 `main@bc33c58febe74648036ed68c890abaa0be55f605`。
- 真实复现来自 #333 / PR #337：旧 Publication、remote 与 PR HEAD 为
  `db49b964e72b4f59f9ef8285dce2b54d8917db10`；base merge 为
  `e25b51d5fbd23b29f56a44a7cfb6f095f63453e7`；当前 Publication HEAD 为
  `193ae9d6a4e6d0d29762cd335e03846d85f58953`。
- 当前最后一个 commit 是单父提交，且只修改 `.trellis/guru-team/extension.json`；该 tail 已通过现有
  Publication provenance metadata 校验。
- `provenance_tail_transaction_rebind_errors()` 直接以旧 Publication HEAD 校验当前 Publication HEAD，因二者
  中间存在 base merge 而返回 `provenance_tail_parent_mismatch`。
- #344 的 `provenance_tail_transaction_rebind_is_base_evolution()` 比较
  `old-publication..current-publication` 与 `merge-base..current-base` 的完整 binary delta。组合拓扑多出合法
  manifest delta，故 comparison 返回 false。
- `provenance_tail_commit_errors()` 已定义一个合法 direct-child provenance tail 的父提交、changed path 与
  metadata allowlist 合同。本任务复用该函数，不增加第二套 provenance 判断。
- #342 direct-tail 与 #344 pure-base-evolution 已有 targeted tests；本任务补齐二者组合而不改变各自语义。

## 3. Requirements

### R347-01 组合拓扑资格

Finalizer 只在下列条件全部成立时识别组合恢复：

- predecessor transaction 为 `ordinary_publication/push_content`，`pr` 与 `adopted_pr` 均未绑定；
- predecessor 与 current plan 的 task、repository、base branch、head branch、Publication title/body、close scope
  精确一致；
- current Publication HEAD 是单父提交，且 `provenance_tail_commit_errors()` 以其直接父提交作为 reviewed head
  返回空错误集；
- 移除该合法 tail 后，旧 Publication HEAD 到 tail parent 的拓扑满足 #344 的 exact base-evolution binary-delta
  合同；
- remote 与唯一同仓库 Open PR HEAD 均满足 `== predecessor Publication HEAD`；tail parent 与 current Publication
  HEAD 均是 predecessor Publication HEAD 的严格后代；
- current Publication、plan、gate、Issue scope 与 task locator 均 fresh，archive 尚未开始，且不存在不同 PR
  binding 或 owner-state 冲突。

当前 validator 只接受一个 direct-child provenance tail，因此本 Issue 的“受支持序列”精确定义为一个该类
tail；多 tail 链不进入本次范围。

### R347-02 单一分类 authority

- provenance tail 的合法性只由 `provenance_tail_commit_errors()` 判定。
- base evolution 的合法性继续由 #344 exact binary-delta comparison 判定，但 comparison 的 current endpoint 改为
  已验证 tail 的直接父提交。
- 不使用 commit message、路径数量猜测、宽松 metadata 识别或新 business-drift classifier。
- 非候选拓扑保持现有 fail-closed 结果，不把真实 identity、scope、PR 或 transaction 冲突降级为 fallback。

### R347-03 Preview 与 mutation 顺序

Preview 必须完成组合资格与现有 strict-ancestor PR classification，并报告：

- 精确 predecessor、base-evolution endpoint、current Publication HEAD；
- `ancestry=strict_ancestor`、`push_required=true`；
- 唯一 PR identity、初始 Draft/Ready、metadata comparison、`metadata_update_required` 与 `ready_action`；
- 后续顺序为 current-plan-bound recovery transaction 写入、current Publication push、metadata convergence、
  archive、archive push、Ready handling。

Preview 不执行 Git/GitHub mutation，也不改写 #333 transaction。执行器必须在首个外部 mutation 前重读并验证
相同事实，再一次性写入 current-plan-bound existing-PR recovery transaction。

### R347-04 Side-effect 与 retry 保证

- current Publication HEAD 恰好 push 一次；旧 Publication HEAD push 次数为 0；PR create 次数为 0。
- title/body 已一致时 PR edit 次数为 0；合法 metadata 差异只收敛一次。
- Ready PR 保持 Ready；Draft PR只执行一次 Draft-to-Ready。
- archive move、archive commit/push 与 terminal `ready_for_merge` 复用现有 transaction engine。
- 同计划 retry 不重复已完成的 push、PR edit、archive 或 Ready mutation。

### R347-05 Fail-closed matrix

下列场景必须在首个 mutation 前阻断：非 provenance 文件变化、非法 manifest 字段、tail parent 不连续、tail 为
merge commit、多 tail 链、base delta comparison 返回 false、额外业务 commit、task/repo/base/head/title/body/scope drift、remote/PR
HEAD drift、多个 PR、fork PR、Closed/Merged PR、stale plan/gate/Publication、archive 已开始、不同 PR binding、未知
transaction mode/stage 或 transaction 字段冲突。

### R347-06 Canonical 与 projection

- canonical Finalizer runtime、tests 与合同为修改源头。
- 通过 preset apply 生成 dogfood installed、Shared、Codex、Claude、Cursor projection；不得直接维护生成副本。
- public Skill I/O、typed exit、transaction stage 与 schema identity 保持不变。实现若无法保持该约束，停止并返回
  Phase 1 重审。

## 4. Acceptance Criteria

- [ ] AC-347-01：真实 Git topology `旧 Publication -> base merge -> 合法 manifest-only tail` 返回
  existing-PR strict-ancestor recovery，且报告三个 endpoint 的精确 identity。
- [ ] AC-347-02：组合路径在首个外部 mutation 前写入 current-plan-bound recovery transaction。
- [ ] AC-347-03：组合路径 current Publication push 次数为 1，PR create 次数为 0；同计划 retry 不重复任何已完成
  mutation。
- [ ] AC-347-04：#342 单 direct-child tail 路径保持通过。
- [ ] AC-347-05：#344 pure base merge 与 multiple base commits 路径保持通过。
- [ ] AC-347-06：非法 metadata、非 provenance 文件、business drift、scope/PR/transaction drift 矩阵全部在 mutation
  前阻断。
- [ ] AC-347-07：Ready/Draft 与 metadata equal/convergence 组合完成 archive、archive push 和
  `ready_for_merge`。
- [ ] AC-347-08：canonical、dogfood installed、Shared/Codex/Claude/Cursor bytes 收敛，递归
  `.new/.bak/.rej/.orig` 计数为 0。
- [ ] AC-347-09：source/installed Finalizer targeted tests、finish-family integration、preset reapply、ownership、
  drift、package validation、task validation 与 `git diff --check` 通过。
- [ ] AC-347-10：#333 / PR #337 只作为复现 evidence；#333 transaction、#249 与 live PR state 均不发生 mutation。

## 5. Docs SSOT Plan

策略：`delta_first`。

- Phase 2 创建 `docs/requirements-design-test-contributions/347-finalizer-base-evolution-provenance-tail/`，记录本任务
  Requirements、Design、Test 与 traceability delta。
- 更新 canonical Finalizer `SKILL.md`、`references/contract.md`，并更新被组合恢复语义直接命中的
  `.trellis/spec/workflow/{data-contracts,companion-scripts,quality-guidelines}.md`。
- 使用 preset apply 同步 dogfood installed 与声明平台 projection；生成副本不作为独立 authority。
- 本任务不修改 shared Requirements/Design/Test current authority；task-owned contribution 在后续 RDT owner 流程中
  review 与 promotion。

## 6. Architecture Planning Impact

预期 route：`baseline_current/no_architecture_impact`。

本任务位于现有 Finalizer 单一 owner 与现有 transaction engine 内，只组合 #342 provenance validator 和 #344
base-evolution comparator；不新增 public DTO、typed exit、持久化类型、跨 package owner、依赖方向、GAP 或 ADR。
正式 route 由当前 `guru-maintain-architecture-baseline:task_impact_sync(stage=planning)` 决定。

## 7. Out Of Scope

- #333 业务实现、task、archive、owner-private transaction mutation 或 Issue closure。
- PR #337 的 edit、close、rebuild、merge 或远程分支删除。
- #249 的修改或关闭。
- 多 provenance tail 链、任意 metadata sequence 或宽松 business-drift recovery。
- Release Gate、完整多平台 Throwaway matrix、tag、GitHub Release、deployment 与 production proof。
- 恶意伪造、攻击模型、锁、TOCTOU、压力竞态或额外 crash-consistency 加固。
- commit、push、PR、merge、Issue closure 与 worktree cleanup。

## 8. Open Questions

无。Live Issue 与当前代码证据已确定组合拓扑、兼容路径、strict validation、side-effect 计数及验证边界。
