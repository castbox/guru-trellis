# #435 Active Task Delivery Loop Design contribution

状态：`absorbed_historical_source`。本 contribution 已由 serialized RDT promotion 吸收到
`current-main-0.6.17-guru.55`；采用 `target_native`。Architecture contribution 已由独立 Architecture
owner 同步提升到 `.55/active`，[`ADR-012`](../../architecture/adr/012-active-task-delivery-loop.md) 已接受。

- `D435-01`：`guru-review-task-delivery` 使用 semantic profile：AI authoring -> private recorder -> objective
  checker -> one typed projection。成功投影退休 checkpoint；semantic output丢失必须 fresh重跑。
- `D435-02`：`guru-publish-task-delivery` 使用 Delivery-only transaction：`push_content -> bind_pr ->
  converge_metadata -> mark_ready -> ready`。每个 mutation前fresh reread并先持久化同计划恢复所需最小私有
  state；terminal `ready` 可零mutation重物化 DTO。
- `D435-03`：`guru-merge-task-delivery` 在 current semantic gate 后展示一次 exact action plan，使用
  `gh pr merge --merge --match-head-commit --subject --body-file`。post-read验证 exact message、parents、base与
  reviewed head；已合并事实支持零第二merge恢复。
- `D435-04`：Planning artifacts分别表达 `task_scope`、`delivery_slice`、`remaining_work` 与
  `independent_delivery_conditions`。Check/Branch Review 对完整 candidate 做影响检查并只对 current slice做
  满足性判断；Task Commit只消费 fresh Check。普通 remaining-work 推进不创建替代 task。
- `D435-05`：merge body使用 closed versioned trailers：`Guru-Task-Identity`、`Guru-Delivery-Schema: 1`、
  `Guru-Delivery-Head`。Discovery 从 target base history 解析并与 repository/base/PR/commit/parents交叉验证；
  不使用 ledger、PR body、current branch、remote branch存活或 task creation branch/base作为 identity authority。
- `D435-06`：Publish transaction以单一 current schema覆盖 initial、strict-ancestor adoption、#405 equal-head
  bind recovery、metadata convergence、Draft/Ready 与 terminal output loss。每次剩余 mutation前记录同计划恢复
  必需的最小 private state；旧 Finalizer transaction不被双读或转换。
- `D435-07`：Merge gate绑定 first live PR snapshot、expected head、pre-merge base、exact message/trailers与当前
  confirmation plan。Post-read验证 MERGED、exact message、ordered parents、base ref与Refs-only；terminal facts
  只恢复同一 `delivered` DTO，不执行第二次 merge。
- `D435-08`：Reconcile resolved-candidate profile绑定 HEAD、MERGE_HEAD、stage-0 tree、index digest、ordered
  parents、message、task/worktree/branch与fresh Phase 2。Executor只在 clean resolved Git state创建唯一 local
  merge commit，output loss只恢复同parents/tree/message commit，并继续完整 Branch Review。
- `D435-09`：canonical source包含三个新 package、现有 owner的最小合同变更、Reconcile扩展、workflow/spec/
  README、preset与tests；installer完整分发 Shared/Codex/Cursor/Claude projection。#435不改 production markers，
  #434独占原子激活；不新增 adapter、dual graph、squash/rebase fallback或Delivery ledger。
