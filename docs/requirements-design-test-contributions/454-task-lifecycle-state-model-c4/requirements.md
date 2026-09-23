# #454 C4 Branch Association Requirements Contribution

状态：`contribution_candidate`。本 contribution 只承接 C4 branch association、establishment 与 rebind
substrate；expected current 为 `current-main-0.6.17-guru.61`，candidate successor 由 reviewed promotion
分配。它不激活 production
workflow，不交付完整 Skill package，也不重做 C1、C2、D0 或 C3。

- `R454-C4-01`：TaskBranchBinding 必须存放于 Git common-dir，并以 `TaskId + lifecycle_generation` 为 key。
  Durable record 严格只有 `schema_version`、`task_id`、`lifecycle_generation`、`binding_revision`、
  `branch_name` 五个字段；不得保存 binding epoch、path、HEAD、session 或 ownership。
- `R454-C4-02`：初始 binding revision 为 `0`；每次成功换绑严格递增 `1`。布尔、负数、非整数、stale
  expected revision 与同 branch no-op 均 fail closed。Branch name 使用 bare portable ref，拒绝 `refs/*`、
  reserved `guru-task-lifecycle/*` 与 Git 非法 ref。
- `R454-C4-03`：establishment 必须覆盖 binding/ownership 的四象限。已有一侧必须原样保留并使缺失侧采用
  相同 revision/branch；两侧均缺失时建立 revision 0；恢复前已存在的资源只能投影为 caller-owned。
- `R454-C4-04`：candidate 只来自 live registered worktree 与 `refs/heads/*`，并验证 repository common-dir、
  live ref/HEAD、exact task artifact、status、generation、branch exclusivity 与 unresolved resource incarnation。
  恰好一个 registered valid candidate 可进入 establishment；未注册 local branch 必须先走 checkout acquisition，
  零个或多个固定返回 selection-required。
- `R454-C4-05`：C4 只通过窄 `OwnershipPort` 消费 C5 current ownership 能力，不定义第二个 ledger、store、
  resource schema 或 ownership authority。
- `R454-C4-06`：rebind 只支持 `same_checkout_new_ref` 与 `existing_target`。前者允许 active dirty checkout，
  但 target ref 必须不存在，且 mutation 前后 HEAD、真实 Git index bytes、Git-visible working tree bytes 与
  status identity 保持一致；后者要求 source/target clean、target exact artifact 且 source HEAD 是 target HEAD 祖先。
- `R454-C4-07`：不同历史固定返回 named reconcile stop。Rebind 不执行 stash、merge、rebase、cherry-pick、
  reset、force push、commit migration 或 working-tree copy。
- `R454-C4-08`：同一 ref 若仍有未收敛 resource incarnation，不得成为新 target。换绑后旧 revision 的
  cleanup responsibility 由 ownership owner 保留，新 binding 与 current ownership revision/branch 必须一致。
- `R454-C4-09`：establishment 与 rebind transaction 必须捕获 exact control/Git pre-state。失败恢复 binding、
  ownership 与本 transaction 创建的 ref；成功后 output 丢失只读恢复同一结果，不得重复递增 revision。
- `R454-C4-10`：`guru-establish-task-branch-binding` 与 `guru-rebind-task-branch` 在 C4 仅作为 planned stable IDs。
  不创建 canonical package tree、active selector、workflow edge、installed copy 或平台 projection；E434 独占激活。

C5-C7、D443、D436、E434、#434 activation 与完整 Release matrix 均不属于本 contribution 的完成声明。
本 contribution 不授权 shared-current write。后续 reviewed promotion 产生的 successor diff 必须重新进入
fresh Phase 2、Task Commit 与完整 Branch Review。
