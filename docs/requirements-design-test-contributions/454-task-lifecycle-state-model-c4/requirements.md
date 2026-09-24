# #454 C4 Branch Association Requirements Contribution

状态：`reviewed_promoted`。本 contribution 只承接 C4 branch association、establishment 与 rebind
substrate；expected current 为 `current-main-0.6.17-guru.61`，promoted successor 为
`current-main-0.6.17-guru.62`。它不激活 production
workflow，不交付完整 Skill package，也不重做 C1、C2、D0 或 C3。

- `R454-C4-01`：TaskBranchBinding 必须存放于 Git common-dir，并以 `TaskId + lifecycle_generation` 为 key。
  Durable record 严格只有 `schema_version`、`task_id`、`lifecycle_generation`、`binding_epoch`、
  `binding_revision`、`branch_name` 六个字段；不得保存 path、HEAD、session 或 ownership payload。
- `R454-C4-02`：`binding_epoch` 是repository-local application control identity。每个new epoch从revision `0`
  开始；每次成功换绑保持epoch并严格递增revision `1`。布尔、负数、非整数、stale expected epoch/revision与
  同branch no-op均fail closed。Branch name使用bare portable ref，拒绝`refs/*`、reserved
  `guru-task-lifecycle/*`与Git非法ref。
- `R454-C4-03`：establishment 必须覆盖 binding/ownership 的四象限。已有一侧必须原样保留并使缺失侧采用
  相同 epoch/revision/branch；association与active ownership均缺失时才建立new epoch/revision 0；恢复前已
  存在的资源只能投影为 caller-owned。
- `R454-C4-04`：candidate 只来自 live registered worktree 与 `refs/heads/*`，并验证 repository common-dir、
  live ref/HEAD、exact task artifact、status、generation、branch exclusivity 与 unresolved resource incarnation。
  恰好一个 registered valid candidate 可进入 establishment；未注册 local branch 必须先走 checkout acquisition，
  零个或多个固定返回 selection-required。Retained `refs/heads/guru-task-lifecycle/*` control refs 必须在
  discovery 前排除。Candidate label/id只服务call-local展示和选择，不是freshness token。
- `R454-C4-05`：C4 只通过窄 `OwnershipPort` 消费 C5 current ownership 能力，不定义第二个 ledger、store、
  resource schema 或 ownership authority。
- `R454-C4-06`：rebind 只支持 `same_checkout_new_ref` 与 `existing_target`。前者允许 active dirty checkout，
  但 target ref 必须不存在，且 mutation 前后 HEAD、真实 Git index bytes、Git-visible working tree bytes 与
  status identity 保持一致；后者要求 source/target clean、target exact artifact 且 source HEAD 是 target HEAD 祖先。
  两条route的plan、mutation与recovery都必须绑定reviewed expected source/target HEAD并fresh验证。
- `R454-C4-07`：不同历史固定返回 named reconcile stop。Rebind 不执行 stash、merge、rebase、cherry-pick、
  reset、force push、commit migration 或 working-tree copy。
- `R454-C4-08`：同一 ref 若仍有未收敛 resource incarnation，不得成为新 target。换绑后旧 revision 的
  cleanup responsibility 由 ownership owner 保留，新 binding 与 current ownership epoch/revision/branch 必须一致。
- `R454-C4-09`：establishment 与 rebind transaction 必须捕获 exact control/Git pre-state。失败恢复 binding、
  ownership 与本 transaction 创建的 ref；成功后 output 丢失只读恢复同一epoch、successor revision和expected
  HEAD结果，不得重复递增 revision。Candidate label相同不能使HEAD已变化的mutation/recovery继续。
- `R454-C4-10`：`guru-establish-task-branch-binding` 与 `guru-rebind-task-branch` 在 C4 仅作为 planned stable IDs。
  不创建 canonical package tree、active selector、workflow edge、installed copy 或平台 projection；E434 独占激活。

本 contribution 的 provenance binding 还消费既有 Finalizer `REQ-048`：无 predecessor transaction 的首次
provenance reprepare 接受 absent、exact reviewed HEAD 或 strict historical ancestor remote；ahead、diverged 与
unknown/unprovable commit 在 mutation 前 fail closed。replacement transaction 必须保留 exact
`pre_push_remote_head`，随后 pre-mutation preflight 重新读取并校验同一 remote identity；该 guard 不新增 C4
public DTO、lifecycle ledger 或 activation edge。

`FIN454-C4-P1-002` 进一步约束 Reactivate branch reuse：合法 provenance tail 与
身份匹配的 `ordinary_publication/push_content` transaction 已存在时，该 transaction 是 current owner。没有 Open
PR 时，同 branch/base terminal PR 仅为历史事实，不是 current candidate。live remote 等于 transaction
`pre_push_remote_head` 时可执行一次到 `publication_head` 的 fast-forward；等于 `publication_head` 时作为合法
push-output-loss/converged state 继续同一 transaction recovery。remote 位于这两个 allowed heads 之外、
ahead/diverged/unknown/unprovable，出现 Open PR drift，或 transaction identity drift 时均 fail closed。不得新增
宽泛 fallback、PR 人工选择 API、force push、第二 ledger，也不得删除或改写 transaction。

C5-C7、D443、D436、E434、#434 activation 与完整 Release matrix 均不属于本 contribution 的完成声明。
Independent Branch Review 绑定 `origin/main@77fa1a2...c7fab600` 且 P0/P1/P2/P3 为 `0/0/0/0`；owners 已将
expected `.61` 串行提升到 `.62`。Promotion-created successor diff 必须重新进入 fresh Phase 2、Task Commit 与
完整 Branch Review。
