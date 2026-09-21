# #454 Task Lifecycle State Model Requirements Contribution

状态：`candidate_pending_review`。本 contribution 绑定 Issue #454、当前 task 与
`current-main-0.6.17-guru.58`，不是 shared current authority。当前实现状态覆盖 C2 shared lifecycle kernel
与 D0 stage-evidence contract correction；二者已形成 committed/reconciled candidate。任何 finding fix 后均须重建
fresh Phase 2、Task Commit 与完整 Branch Review；C3-C6、D443/D436 package migration 与 #434 activation 仍未完成。

- `R454-01`：每个 task 使用 immutable repository-local TaskId；TaskRef 是可变 locator。TaskId 必须能安全构造
  `refs/heads/guru-task-lifecycle/<TaskId>`，因此拒绝 `..`、trailing dot 与 `.lock` suffix。Rename、archive、
  Reactivate、branch rebind 与 checkout move 均不得改变 TaskId；exact duplicate 与 case-fold collision 必须拒绝。
- `R454-02`：`lifecycle_generation` 初始与 legacy missing value 均为 `0`；只有 Reactivate 能递增。Boolean、负数、
  浮点、字符串与 null 均非法，generation-sensitive handoff 使用 `TaskId + lifecycle_generation`。
- `R454-03`：Task source 使用封闭的 `IssueSource | NoIssueSource`；Delivery target 只表达 portable
  `owner/repository` 与 Git-valid branch relation，schema/runtime 必须使用同一值域。Source、scope、Completion 与
  Closure disposition 保持独立。
- `R454-04`：公共 handoff 使用 named closed DTO，只携带唯一 consumer 需要的字段。Machine path、session、
  authorization、generic evidence、resource list 与未声明 Git facts 不得进入 DTO。Machine handoff receipt 只使用
  `refs/heads/guru-task-lifecycle/<TaskId>`；cleanup 与 Delivery remaining-work state 使用 consumer 已声明的封闭枚举。
- `R454-05`：Fork official task/session primitives 是唯一 framework authority。Guru 只提供 schema、normalization、
  resolver adapter 与稳定错误，不复制 `.trellis/scripts/common/**`，不创建 durable identity index、第二 session store、
  workspace mapping reader、alias、dual-read 或 dual-write。
- `R454-06`：C2 canonical/preset durable SSOT、source lock、README source identity、task-owned RDT/Architecture candidate
  与 focused tests 必须一致。C2 不修改 registry、workflow graph、active manifest、installed/platform projection，
  也不声明 production activation 或完整 Release evidence。
- `R454-07`：Phase D0 必须让pre-review compatible base reconcile形成expected-head-bound committed merge HEAD；
  `post_check/post_commit`固定回fresh Phase 2。首次/full Branch Review要求selected base是review HEAD祖先；bounded
  continuity只承接已有prior full review。Old/new base SHA只属于当前operation与相邻consumer，不进入durable task
  identity。#459、#460/#462 只承接日期前缀TaskRef、created Issue provenance与same-result recovery行为保证，不复用
  predecessor workspace mapping、nested result/digest或legacy TaskId推断。

完整 #454 lifecycle 行为仍以 live Issue 与 approved task planning 为 authority。本 candidate 不授权 commit、push、
PR、merge、shared-current promotion 或 cleanup。
