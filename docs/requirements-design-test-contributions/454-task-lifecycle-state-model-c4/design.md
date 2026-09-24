# #454 C4 Branch Association Design Contribution

状态：`reviewed_promoted`。采用 `target_native`，关联
`architecture-contribution-454-task-lifecycle-state-model-c4-v1`，expected current 为
`current-main-0.6.17-guru.61`，promoted successor 为 `current-main-0.6.17-guru.62`。

- `D454-C4-01`：`branch_store.py` 在 `<git-common-dir>/trellis/task-branches/<task-id>/<generation>.json`
  读写 closed six-field TaskBranchBinding。`binding_epoch` 是repository-local application control identity；写入
  使用同目录临时文件替换，snapshot/restore只服务当前transaction。
- `D454-C4-02`：`TaskLifecycleKey` 与 `BranchBinding` 复用 C2 identity primitive；durable branch name 与 schema
  统一为 bare ref。Durable record与C2 `BranchBindingRefDTO`共享epoch/revision identity；DTO只投影consumer所需的
  TaskLifecycleKey、epoch与revision，不携带branch/path/HEAD。
- `D454-C4-03`：`branch_resolution.py` 从 live common-dir facts 构建 registered-checkout/local-branch candidate，
  以call-local candidate id返回，并在遍历前排除retained `refs/heads/guru-task-lifecycle/*` control refs。
  Candidate id/label不进入mutation或recovery freshness。`OwnershipPort`的current read/snapshot/restore/establish/
  rebind携带epoch/revision/branch，另暴露unresolved-ref查询；C4不拥有C5 ledger representation。
- `D454-C4-04`：establishment 先比较 binding 与 ownership current state，再按四象限约束 candidate branch 与
  epoch/revision。单侧存续时补齐缺失侧并沿用epoch；两侧均缺失时生成new epoch/revision 0。Mutation后重新比较
  两侧epoch/revision/branch；任何异常按exact snapshots逆序恢复。
- `D454-C4-05`：`git_facts.py` 的 checkout snapshot 绑定 HEAD、symbolic ref、真实 index 文件 bytes、Git-visible
  working-tree bytes 与 porcelain status。Selection/plan另保存reviewed expected HEAD；执行和恢复fresh reread，
  candidate label相同不覆盖HEAD drift。它不保存machine path或HEAD到durable task authority。
- `D454-C4-06`：`rebind.py` 的 same-checkout route 只执行 `git switch -c <target>`；existing-target route 不修改
  Git content。两条route都在mutation前按expected source/target HEAD重建fresh plan，随后先更新ownership current
  epoch-preserving revision，再推进binding；post-state必须epoch/branch/revision相等。
- `D454-C4-07`：same-checkout rollback 切回 source ref，并只在 target ref 仍指向 reviewed pre-state HEAD 且未被
  checkout 时删除本 transaction 创建的 target ref。Existing-target failure 只恢复 control state，不删除 caller resource。
- `D454-C4-08`：`recover_established_branch_binding` 与 `recover_rebind` 只读验证 exact successor state、live checkout、
  artifact、binding epoch、expected HEAD、cleanliness 与 ancestry，再重建结果；不调用 mutation owner，不增加
  revision。完整control state丢失后的establishment recovery只接受new epoch/revision 0结果。
- `D454-C4-09`：两个 C4 JSON schema 分别固定 durable six-field record 与两条 closed rebind checkpoint route。
  Rebind checkpoint携带source epoch、expected source/target HEAD与successor revision。Checkpoint是owner-private、
  短生命周期 activation input，不是 public DTO 或第二 authority。
- `D454-C4-10`：registry/extension manifest 只增加两个 planned rows。Package absence 与 installed/platform absence
  通过 source/preset regression 固定，完整 package composition 继续由 E434 交付。

本 slice 不新增 ADR。`ADR-015` 已拥有 TaskId/lifecycle 与 framework-extension boundary；C4 只实现该决策下的
branch substrate。Architecture/RDT owners 已按 reviewed range `origin/main@77fa1a2...c7fab600` 串行执行
serialized promotion；promotion-created diff 仍须 fresh Phase 2、Task Commit 与完整 Branch Review。
