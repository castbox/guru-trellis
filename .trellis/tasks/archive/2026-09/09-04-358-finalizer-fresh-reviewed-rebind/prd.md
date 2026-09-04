# #358 修复 Finalizer fresh reviewed task transaction rebind

## 1. Goal

修复 `guru-finalize-task` 对旧未绑定
`ordinary_publication/push_content` transaction 的正常恢复：当 current
Publication HEAD 本身已经是 fresh Phase 2、Task Commit、Branch Review 和
Publication 共同确认的 reviewed task-content HEAD，并且旧 PR/remote HEAD 是它的
严格祖先时，Finalizer 应以 current reviewed identity 取代旧 transaction，并复用
现有 `existing_pr_recovery`，而不是要求额外制造 provenance metadata tail。

Live authority：GitHub Issue #358，读取时间为 2026-09-04。

## 2. Confirmed Facts

- 基线为 `main@970a657fbb759dc2322d3b470bd1173ad1911de3`。
- #333 / PR #337 的 live 拓扑为
  `db49b964 -> a8453eaa -> d09e433a`；旧 transaction 的 Publication HEAD 为
  `db49b964...`，remote/PR HEAD 为 `a8453eaa...`，fresh reviewed/Publication HEAD
  为 `d09e433a...`。
- `d09e433a...` 是 closing fresh Branch Review finding 后产生的合法 task-content
  commit，已重新完成 Phase 2、Task Commit、fresh Branch Review、Publication 和
  Acceptance/Finish；它已经携带 current manifest/projection identity，不存在额外独立
  provenance tail。
- 当前 `classify_provenance_tail_transaction_rebind()` 先把 predecessor Publication
  到 current Publication 的整段提交链交给 `provenance_tail_commit_errors()`，因此
  task-content evolution 会产生 `provenance_tail_changed_paths_invalid` 和
  `provenance_tail_parent_mismatch`。
- `provenance_tail_transaction_rebind_is_reviewed_base_descendant()` 只从
  `provenance_tail_transaction_rebind_base_evolution_tail_parent()` 可达，导致“reviewed
  HEAD 就是 Publication HEAD”的路径无法进入 existing-PR strict-ancestor recovery。
- #342、#353、#355 已提供 direct-tail、reprepare、pure base evolution、base evolution
  plus tail、transaction-before-mutation、metadata convergence、archive/Ready 与 terminal
  retry 能力；本任务复用这些能力，不新增状态机。

## 3. Requirements

### R358-01 Fresh reviewed descendant eligibility

仅当以下条件全部成立时，current reviewed task-content HEAD 才能取代 predecessor：

- transaction 为未绑定的 `ordinary_publication/push_content`；
- task ref、repository、base branch、head branch、Publication payload 和 close scope
  仍满足现有精确校验或既有 metadata convergence 的受控差异合同；
- current `branch_review_commit` 与 `publication_head` 精确一致；
- selected base 与 predecessor Publication HEAD 都是 current reviewed HEAD 的祖先，且
  current selected base 不是 predecessor Publication HEAD 的祖先；
- unique same-repository Open PR 与 remote branch HEAD 精确一致，且该 HEAD 从 predecessor
  Publication HEAD 可达并是 current Publication HEAD 的严格祖先；
- current Publication 输入绑定 fresh reviewed-content、Branch Review 与 Publication
  identity，且 archive 尚未开始；
- 不依赖手工删除、改写或伪造 predecessor transaction。

### R358-02 Reuse existing recovery

资格成立后必须调用现有 `classify_existing_pr_recovery()`，并保持：

- `publication_mode=existing_pr_recovery`；
- `ancestry=strict_ancestor`、`push_required=true`；
- 精确 PR number/URL、pre-push remote HEAD、current Publication HEAD；
- current Publication title/body 的 metadata comparison、最多一次 convergence；
- Ready 保持 Ready，Draft 最多一次 Ready transition。

### R358-03 Transaction before mutation

执行器必须在 push、PR edit、archive、archive push 或 Ready mutation 前，持久化一个
current-plan-bound `existing_pr_recovery/push_content` transaction。same-plan retry 必须
复用该 transaction，不能重复已完成 mutation。

### R358-04 Compatibility and fail closed

- direct tail、pure base evolution、base evolution plus tail、equal-HEAD、metadata
  convergence、post-bind 和 terminal recovery 保持兼容。
- 未审 business drift、dirty reviewed path、非祖先 HEAD、scope/repository/branch/PR
  identity 漂移、多个或 fork PR、stale Publication/Branch Review、archive 冲突继续在
  mutation 前阻断。
- 不新增 public DTO、typed exit、transaction mode/stage 或 schema version。

## 4. Acceptance Criteria

- [ ] AC-358-01：无额外 provenance tail 的 fresh reviewed task-content HEAD 可通过
  transaction rebind classifier，并进入 strict-ancestor existing-PR recovery。
- [ ] AC-358-02：#333 / PR #337 去敏拓扑 preview 返回准确 PR、HEAD、metadata
  comparison、`ancestry=strict_ancestor` 和 `push_required=true`。
- [ ] AC-358-03：current Publication HEAD 恰好 push 一次，PR create 为 0，PR metadata
  edit 为 0 或 1，Ready transition 为 0 或 1。
- [ ] AC-358-04：recovery transaction 在首个外部 mutation 前写入；same-plan retry 不
  重复 push、PR edit、archive、archive push 或 Ready mutation。
- [ ] AC-358-05：未审 task/business drift、dirty path、invalid ancestry、scope/repo/
  branch/PR/Publication identity drift 均在 mutation 前阻断。
- [ ] AC-358-06：#342/#353/#355 已有正向和负向拓扑全部继续通过。
- [ ] AC-358-07：canonical、dogfood installed、Shared/Codex/Claude/Cursor 投影一致，
  targeted source/installed tests、ownership、drift、task validation、`git diff --check`
  与递归 sidecar-zero 检查通过。

## 5. Docs SSOT Plan

采用 `delta_first`：Phase 2 创建
`docs/requirements-design-test-contributions/358-finalizer-fresh-reviewed-rebind/`，记录
Requirements、Design、Test 和 traceability delta；同步更新 Finalizer canonical contract
以及直接命中的 workflow data-contract/companion-script/quality spec，再通过 preset apply
生成 dogfood installed 与平台投影。若实现证明某个 durable 文档无需变化，记录明确的
no-change 理由，不制造新 public API 或 ADR。

## 6. Architecture Planning Impact

预期 `baseline_current/no_architecture_impact`。本任务仅在现有 Finalizer owner 内补齐一个
current reviewed descendant 资格入口，随后复用现有 strict-ancestor classifier、private
transaction、metadata/archive/Ready engine 和六个 typed exits；不增加跨 package owner、依赖
方向、持久化类型、GAP 或 ADR。

## 7. Out Of Scope

- 修改、push、关闭或合并 PR #337。
- 吸收或关闭 #333、#249；#355 仅作为已交付前序能力。
- 放宽为任意 business drift、任意 strict ancestor 或多 PR adoption。
- Release Gate、tag、GitHub Release、deployment、production proof 或完整 Throwaway matrix。
- hostile-input、TOCTOU、锁、压力竞态、跨 OS 原子性或额外 fault injection。
- 本 task 的 commit、push、PR、merge、Issue closure 与 worktree cleanup。

## 8. Open Questions

无阻塞性产品决策。若实现必须改变 public DTO、typed exit、transaction schema/mode/stage
或跨 Skill owner，立即停止并重新进入 scope、Architecture 与 contract review。
