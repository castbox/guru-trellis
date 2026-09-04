# #355 修复 Finalizer 多段合法演进后的既有 PR 恢复

## Goal

修复 Finalizer 在旧的、尚未绑定 PR 的
`ordinary_publication/push_content` transaction 经历合法 base evolution、task
commit 和 provenance metadata tail 后，无法识别既有 PR 并重新绑定当前
Publication 的问题。修复必须保留现有 provenance、changed paths、source
binding、reviewed-content、PR identity 和 scope 校验。

## Confirmed Facts

- Issue #355 当前为 Open，live 复现来自 #333 / PR #337；本 task 不修改 #333
  实现，不修改、关闭或合并 PR #337。
- 当前 `origin/main` 为 `64abb89418b543bd5323a2743e98652027475437`，已包含
  #342、#344、#347、#350、#353 的既有修复。
- 当前代码已有 direct provenance tail、纯 base evolution，以及 base evolution
  后单 tail 的正向测试，但 #355 的多段合法演进会在旧 transaction 的
  provenance-tail rebind 分类中落入 `provenance_tail_parent_mismatch` /
  `provenance_tail_transaction_rebind_invalid`。

## Requirements

1. 识别精确的旧未绑定 ordinary transaction、同一 task/repository/base/head/
   close scope、旧 Publication HEAD、远程分支和唯一 Open PR。
2. 对单一 provenance tail、base evolution、task commit 以及 base evolution 后
   单一 tail 的支持拓扑选择现有 reprepare/rebind 路径；不得把合法演进误判为
   transaction invalid。
3. provenance tail 仍必须通过现有 `provenance_tail_commit_errors()`；不得放宽
   direct-parent、changed-path、manifest allowlist、source binding、business
   delta、multi-tail 或 PR/remote identity 规则。
4. 在首个剩余外部 mutation 前写入 current-plan recovery transaction，并复用
   现有 push/bind/archive/Ready transaction engine；same-plan retry 不重复已完成
   mutation。
5. 保持 Finalizer public input/output、六个 typed exits、transaction schema 3.0、
   canonical/package/platform projection 和现有 Issue 边界兼容。

## Acceptance Criteria

- [ ] 真实 Git topology 覆盖旧未绑定 transaction 经 base evolution、task commit
  和单一 provenance tail 后的 preview/rebind 正向路径。
- [ ] 正向路径返回已有 `existing_pr_recovery` / `reprepare_required` 合同，且
  不删除 transaction、不创建第二个 PR、不重复 push。
- [ ] 旧 transaction 的 task/repo/base/branch/scope、PR、remote、Publication
  lineage、reviewed-content 和 archive state 漂移均在首个 mutation 前 fail closed。
- [ ] direct tail、纯 base evolution、composed base evolution plus tail 的既有
  测试继续通过；invalid parent、extra path、manifest drift、business delta、
  multi-tail 和 stale PR/remote 测试继续阻断。
- [ ] canonical runtime/test 与 preset projection 同步，定向测试、preset apply、
  dogfood drift、`git diff --check` 和 `.new`/`.bak` 零残留检查通过。

## Out Of Scope

- 不修改 #333、PR #337 或任何外部仓库状态；不执行 push、PR mutation、merge 或
  Issue closure。
- 不改变 public DTO、typed exit、transaction mode/stage 或引入新的 verifier/
  Release Gate/full Throwaway matrix。
- 不处理 hostile-input、TOCTOU、并发锁、压力竞态、跨平台原子性或 fault injection。

## Docs SSOT Plan

采用 `delta_first`：先以 task-local 规划和测试作为行为承接；若实现改变现有
Finalizer 语义，再更新 `trellis/skills/guru-team/packages/guru-finalize-task`
的 canonical contract 及直接命中的 workflow data-contract/quality spec，并通过
preset apply 同步安装投影。若 public contract、schema、架构边界均不变，记录
no-change，不制造无效架构文档。

## Open Questions

无阻塞性用户决策。实现机制、是否需要 contract/spec 文字同步和最终验证边界由
Phase 1/2 语义检查根据当前代码与真实 Git topology 判定。
