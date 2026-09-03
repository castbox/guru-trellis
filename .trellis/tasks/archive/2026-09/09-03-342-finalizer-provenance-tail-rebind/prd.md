# #342 修复 Finalizer provenance-tail transaction rebind

## 1. Goal

补齐 `guru-finalize-task` 的正常恢复路径：旧 owner-private transaction 已完成
`ordinary_publication/push_content`，其后当前 reviewed HEAD 只追加了一个合法 provenance metadata tail，且唯一
既有 PR 与远端仍停在旧 publication HEAD 时，Finalizer 应先受控重绑定当前 plan/transaction identity，再按
strict-ancestor existing-PR recovery 恰好推送一次新的 publication HEAD，而不是误入 current-transaction
base-evolution supersession 并阻断。

Live authority：GitHub Issue #342，2026-09-03 13:06:03 +08:00 当前正文。

## 2. Confirmed Facts

- 当前基线为 `main@21b3e1195cc2a8cf68c13a8f58487f32a5730bb5`。
- 真实复现来自 #333 / PR #337：旧 publication HEAD 为
  `db49b964e72b4f59f9ef8285dce2b54d8917db10`，当前 reviewed HEAD 为
  `a4a9a399d594aa7a12fa3171cb2b12a1e3576508`，两者之间仅为合法 provenance metadata tail。
- 旧 transaction 为 `mode=ordinary_publication`、`next_transition=push_content`、未绑定 PR；PR #337 和远端分支
  仍精确位于旧 publication HEAD。
- #338 已实现 exact current-plan `ordinary_publication/push_content` transaction 的 unbound equal-HEAD PR 接管，
  并提供 transaction binding、metadata convergence、archive 与 Ready 恢复机制；其 equal-HEAD classifier 要求
  remote/PR HEAD 必须与 rebuilt current plan 的 publication HEAD 一致，因此不能直接分类本任务的真实拓扑。
- 当前 preview 在 `finalization_validate_transaction_plan()` 失败后，先调用
  `finalizer_current_transaction_base_evolution_supersession_preflight()`；该 helper 只接受历史 `verify` stage，
  因此旧 `push_content` transaction 返回 `provenance_reprepare_base_evolution_mismatch`，尚未进入
  `finalization_existing_pr_recovery_context()`。
- `provenance_tail_commit_errors()` 已拥有 manifest-only provenance tail 的内容连续性校验；本任务复用该合同，
  不新增第二套 diff 分类权威。

## 3. Requirements

### R342-01 精确 rebind 资格

Finalizer 仅在下列条件全部成立时识别 provenance-tail transaction rebind：

- predecessor transaction 为 `ordinary_publication/push_content`，且 `pr`、`adopted_pr` 均未绑定；
- predecessor 与 current plan 的 task、repository、base/head branch 完全一致；current plan remote 另由 live
  repository/PR identity 校验，不把 transaction schema 3.0 中不存在的 remote 字段冒充 predecessor evidence；
- predecessor reviewed/publication HEAD 到 current reviewed/publication HEAD 的演进仅由
  `provenance_tail_commit_errors()` 认可的 manifest-only provenance metadata tail 构成；
- predecessor publication HEAD 与 live remote/PR HEAD 一致，current publication HEAD 是它的一个合法
  direct-child provenance tail；
- current Publication payload、plan/gate identity、Issue close scope 与 task locator 均 current；
- archive 尚未开始，不存在不同 PR binding、并行 transaction owner 或其它 owner-state 冲突。

任一条件失败时保持 fail closed，不删除、手工改写或宽松迁移 transaction。

### R342-02 Side-effect-free preview

Preview 必须先完成 transaction rebind 的完整资格判断，并报告重绑定后的 existing-PR recovery 计划：

- 精确 PR number/URL、repository/base/head/head-repository identity；
- predecessor/current reviewed 与 publication HEAD 连续性；
- `ancestry=strict_ancestor`、`push_required=true`，只推送一次新的 current publication HEAD，不得重复
  推送旧 publication HEAD；
- PR 原始 Draft/Ready 状态、title/body 字节比较、`metadata_update_required` 与 `ready_action`；
- 后续顺序为 owner-private transaction rebind/binding、current publication push、metadata convergence、archive、
  archive push、Ready handling。

Preview 不执行 Git/GitHub mutation，也不修改 owner-private transaction。

### R342-03 Mutation 前 transaction rebind

执行器必须在 PR edit、archive、commit、push 或 Ready mutation 前：

- 重新读取并验证 preview 所绑定的 live facts；
- 以旧 ordinary transaction 为受控 preimage，生成与 current plan 匹配且已绑定唯一 PR 的
  `existing_pr_recovery/push_content` transaction；
- 保留 task/repo/base/head branch、Publication payload、close scope 与 predecessor continuity；
- 只更新 current reviewed/publication/plan identity 所需字段；
- 复用现有 strict-ancestor classifier、#338 metadata/binding validation 和同一 recovery transaction engine，不创建
  第二套 recovery 状态机，也不调用硬编码 `equal/push_required=false` 的 #338 conversion。

### R342-04 Metadata、archive 与 Ready 恢复

- title/body 已一致时不执行 PR edit；存在合法 metadata 差异时只收敛一次到 current Publication payload。
- Ready PR 保持 Ready；Draft PR 仅执行一次 Draft-to-Ready。
- archive move、archive commit/push 和 terminal `ready_for_merge` 复用现有 Finalizer transaction。
- 同计划重试不得重复 current publication push、PR create/edit、archive move/commit/push 或 Ready mutation。

### R342-05 Fail-closed matrix

以下场景必须在首个 mutation 前阻断：业务内容变化、非 manifest-only tail、HEAD/ancestry drift、scope drift、
多个 PR、Closed/Merged PR、fork PR、repo/base/head/head-repository mismatch、title/body preview 后漂移、stale
Publication/plan/gate、archive 已开始、不同 PR binding、未知 transaction stage 或 transaction 字段冲突。

## 4. Acceptance Criteria

- [ ] AC-342-01：#333 / PR #337 去敏真实拓扑 preview 返回 provenance-tail rebind 后的
  `existing_pr_recovery`，并报告 `ancestry=strict_ancestor`、`push_required=true`、旧/new HEAD 精确值。
- [ ] AC-342-02：旧 `ordinary_publication/push_content` transaction 在任何外部 mutation 前一次性转换为
  current-plan-bound strict-ancestor recovery transaction。
- [ ] AC-342-03：合法 manifest-only provenance tail 通过；业务内容、额外文件或非法 manifest 字段变化阻断。
- [ ] AC-342-04：Ready/Draft 与 metadata equal/convergence 组合均完成 archive、archive push 和
  `ready_for_merge`。
- [ ] AC-342-05：current publication HEAD 只推送一次；同计划重试不重复该 push、PR create/edit、archive
  move/commit/push 或 Ready mutation。
- [ ] AC-342-06：HEAD、scope、PR 数量、fork、metadata、gate、archive 和 transaction 冲突矩阵均在 mutation 前阻断。
- [ ] AC-342-07：canonical、dogfood installed、Shared/Codex/Claude/Cursor 投影一致，递归 `.new`/`.bak` 为零。
- [ ] AC-342-08：Finalizer source/installed targeted tests、finish-family integration、preset reapply、ownership、
  drift、task validation 与 `git diff --check` 通过。
- [ ] AC-342-09：不修改 #333 业务实现、PR #337 live state 或 #249；不执行完整 Release/Throwaway matrix。

## 5. Docs SSOT Plan

策略：`delta_first`。

- Phase 2 创建 `docs/requirements-design-test-contributions/342-finalizer-provenance-tail-rebind/`，记录本任务的
  Requirements、Design、Test 与 traceability delta。
- Durable workflow contract 预计更新 canonical Finalizer `SKILL.md`、`references/contract.md`，以及直接命中的
  `.trellis/spec/workflow/{data-contracts,companion-scripts,quality-guidelines}.md`。
- 通过 preset apply 同步 dogfood installed 与 Shared/Codex/Claude/Cursor projection；不直接维护生成副本。
- 若实现不改变 public Skill I/O、typed exit、transaction schema 或 owner 边界，则保持 Interface/schema id/registry
  不变；发现上述变化时停止并重新进入 Architecture 与 scope review。

## 6. Architecture Planning Impact

预期 route：`baseline_current/no_architecture_impact`。

本任务修复现有 Finalizer 单一 owner 内的 transaction identity 恢复顺序，复用已有 single-tail validator、
strict-ancestor PR classifier、#338 metadata/binding validation、archive 与 Ready transaction；不新增公共 DTO、
typed exit、持久化类型、跨 package owner、依赖方向、GAP 或 ADR。

## 7. Out Of Scope

- #333 的业务实现、task、archive 或 Issue closure。
- PR #337 的修改、关闭、重建、合并或远端分支删除。
- #249 的修改或关闭。
- 任意 Open PR、任意手工 push、fork PR、scope mismatch 或跨计划状态的追认。
- Release Gate、tag、GitHub Release、deployment、production proof 与完整多平台 Throwaway matrix。
- 恶意伪造、攻击模型、锁、TOCTOU、压力竞态或额外 crash-consistency 加固。
- commit、push、PR、merge、Issue closure 与 worktree cleanup。

## 8. Open Questions

无。Live Issue #342 已明确 strict-ancestor recovery、current publication HEAD 单次推送、#338 equal-HEAD
路径保持不变，以及 scope、失败矩阵和验证边界。
