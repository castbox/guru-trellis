# #435 Active Task Delivery Loop Requirements contribution

状态：`candidate`。本文是 task-owned delta，不是 shared current authority；只有 independent committed
full-diff review 通过后，serialized RDT promotion 才能把它吸收到 expected
`current-main-0.6.17-guru.54` successor。

- `R435-01`：新增 Delivery Review semantic owner，按 approved current slice 审查 requirement、Delivery
  policy、remaining work、independent delivery conditions、validation、RDT/Architecture、base 与 Branch
  Review；只输出 closed minimal typed exit。
- `R435-02`：新增 Delivery Publish owner，绑定 reviewed HEAD、repository/base/head branch 与 exact PR
  payload，执行一次 push/create-or-adopt/converge/Ready；#405 equal-head output loss 必须恢复同一 PR，零重复
  mutation。
- `R435-03`：新增 Delivery Merge owner，只允许 merge commit，以 expected head、checks、base、method 与
  exact subject/body 执行一次 mutation；merge body 必须携带 stable task、schema 1、reviewed head trailers，
  output loss 必须由 terminal live facts恢复同一 Delivery result。
- `R435-04`：同一 active task 必须支持多个顺序 Delivery cycles。每次 merge 后 task 保持 active，remaining
  work 不得被声明完成；Delivery packages 不拥有 Completion、Issue Closure、archive、Finish、Cleanup 或
  Reactivate。
- `R435-05`：Delivery history 必须跨 branch/worktree 重建，交叉验证 GitHub PR/merge、merge commit、parents、
  repository/base 与 exact trailers；PR body、current branch、remote branch存活和 task creation facts 不得替代
  identity authority。
- `R435-06`：Planning/Approval、Check、Task Commit、Branch Review 与 Reconcile 保持既有 owner。Sliced
  delivery 只改变 current satisfaction boundary，不弱化完整 candidate impact review；#407 resolved tree
  commit 必须绑定 fresh Phase 2 与 exact merge tree，并支持 same-commit recovery。
- `R435-07`：三个新 package 必须注册、安装并投影到 Shared/Codex/Cursor/Claude，但在 #434 前保持
  `deferred`；existing Publication/Finalizer/Merge/Restore production graph与mandatory markers不变。
- `R435-08`：验证必须覆盖 package contract/runtime/eval、两个顺序 Delivery、#405、#407、trailer parse、
  cross-branch discovery、Refs-only、bookkeeping exclusion、projection parity、representative clean install/reapply、
  ownership、dogfood drift与repository checks。

#434 独占 production graph原子切换与旧edge retirement；#436 独占 Completion、Closure、Finish、Cleanup与
Reactivate。本文不授权 commit、push、PR、merge、release 或 cleanup。
