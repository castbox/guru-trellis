# #454 C4 Branch Association Design Contribution

状态：`contribution_candidate`。采用 `target_native`，关联
`architecture-contribution-454-task-lifecycle-state-model-c4-v1`，expected current 为
`current-main-0.6.17-guru.61`，candidate successor 由 reviewed promotion 分配。

- `D454-C4-01`：`branch_store.py` 在 `<git-common-dir>/trellis/task-branches/<task-id>/<generation>.json`
  读写 closed five-field TaskBranchBinding。写入使用同目录临时文件替换；snapshot/restore 只服务当前 transaction。
- `D454-C4-02`：`TaskLifecycleKey` 与 `BranchBinding` 复用 C2 identity primitive；durable branch name 与 schema
  统一为 bare ref。C2 `BranchBindingRefDTO.binding_epoch` 保持不变，但它不是 durable record，也不进入 C4 output。
- `D454-C4-03`：`branch_resolution.py` 从 live common-dir facts 构建 registered-checkout/local-branch candidate，
  以稳定 candidate id 返回。`OwnershipPort` 只暴露 current read/snapshot/restore/establish/rebind 与 unresolved-ref
  查询，C4 不拥有 C5 ledger representation。
- `D454-C4-04`：establishment 先比较 binding 与 ownership current state，再按四象限约束 candidate branch 与
  revision。Mutation 后重新比较两侧；任何异常按 exact snapshots 逆序恢复。
- `D454-C4-05`：`git_facts.py` 的 checkout snapshot 绑定 HEAD、symbolic ref、真实 index 文件 bytes、Git-visible
  working-tree bytes 与 porcelain status。它不保存 machine path 到 durable authority。
- `D454-C4-06`：`rebind.py` 的 same-checkout route 只执行 `git switch -c <target>`；existing-target route 不修改
  Git content。两条 route 都在 mutation 前重建 fresh plan，随后先更新 ownership current revision，再推进 binding；
  post-state 必须 branch/revision 相等。
- `D454-C4-07`：same-checkout rollback 切回 source ref，并只在 target ref 仍指向 reviewed pre-state HEAD 且未被
  checkout 时删除本 transaction 创建的 target ref。Existing-target failure 只恢复 control state，不删除 caller resource。
- `D454-C4-08`：`recover_established_branch_binding` 与 `recover_rebind` 只读验证 exact successor state、live checkout、
  artifact、HEAD、cleanliness 与 ancestry，再重建结果；不调用 mutation owner，不增加 revision。
- `D454-C4-09`：两个 C4 JSON schema 分别固定 durable five-field record 与两条 closed rebind checkpoint route。
  Checkpoint 是 owner-private、短生命周期 activation input，不是 public DTO 或第二 authority。
- `D454-C4-10`：registry/extension manifest 只增加两个 planned rows。Package absence 与 installed/platform absence
  通过 source/preset regression 固定，完整 package composition 继续由 E434 交付。

本 slice 不新增 ADR。`ADR-015` 已拥有 TaskId/lifecycle 与 framework-extension boundary；C4 只实现该决策下的
branch substrate。Architecture/RDT owners 尚未执行 serialized promotion；后续 promotion-created diff 仍须
fresh Phase 2、Task Commit 与完整 Branch Review。
