# #454 C5 Session And Resource Control Design Contribution

状态：`contribution_candidate`。采用 `target_native`，关联
`architecture-contribution-454-task-lifecycle-state-model-c5-v1`，expected current 为
`current-main-0.6.17-guru.62`。

- `D454-C5-01`：`session_adapter.py` 接受 official session module/port，不复制其 filesystem、Git discovery 或
  TaskId-to-TaskRef resolver。adapter 验证 exact TaskLifecycleDTO，构造 schema-2 record，委托 official
  `repository_facts/session_path/read_record/write_record/resolve_task_identity`，再向 consumer 投影 path-free result。
- `D454-C5-02`：context key resolution 是 invocation capability，不是 task authority。无 key 返回
  `explicit_task_mode`；write error 返回 session-specific failure并保留 caller 已完成的 lifecycle result。
- `D454-C5-03`：`resource_ledger.py` 在
  `<git-common-dir>/trellis/task-resources/<task-id>/<generation>.json` 维护 closed ledger。ledger revision 只服务
  mutation/recovery；每个 resource incarnation 拥有稳定 id、kind、origin、ownership、portable ref、binding
  epoch/revision、state 与 role。active-missing 只接受 exact whole-ledger successor；remote-delivery lost-output
  recovery 只要求 exact current incarnation 仍与 current branch/epoch/revision 一致，不因无关合法 ledger mutation
  失效。两者均直接从 ledger 只读 rematerialize，不新增 transaction store。
- `D454-C5-04`：ledger 直接实现 C4 `OwnershipPort`。`read_current` 只投影 current branch resource set；snapshot/
  restore 使用 exact bytes；establish/rebind 在写前验证 expected ledger revision 与 current epoch/revision/branch，
  写后重新读取并投影 `OwnershipCurrent`。
- `D454-C5-05`：active missing recovery 以 current `BranchBinding` 与 fresh live resource facts为输入，把 mutation 前
  已存在的 local branch/worktree/remote 统一记为 caller-owned。terminal missing 不走该方法，只形成 manual-selection
  resolution。
- `D454-C5-06`：rebind 把旧 current incarnations 变为 retired。Guru-owned 进入 cleanup-pending，caller-owned 保留；
  target resources按本次 acquisition facts建立 current incarnation。unresolved-ref 查询拒绝尚未收敛的同 ref复用。
- `D454-C5-07`：Finish seal schema只接收 current lifecycle、finish result 与 ledger revision/inventory identity；
  Cleanup resolution schema分别表达 ordinary cleanup set、manual selection required 与 already-clean states，不把用户
  选择或授权写入 ledger。
- `D454-C5-08`：普通 cleanup projection 过滤 retained handoff control refs，并只返回 Guru-owned cleanup-pending
  incarnations。manual terminal cleanup 是独立用户定向路径，不把选择反写成历史 Guru ownership。
- `D454-C5-09`：三个 C5 schema 固定 ledger、Finish seal input 与 Cleanup resolution；mutation rollback/recovery
  由 runtime exact snapshot 和 successor recognition承接，不制造无人消费的 checkpoint schema。session record继续由
  official schema-2 primitive拥有，不新增 Guru session schema。
- `D454-C5-10`：registry 只增加一个 planned row。完整 package composition、consumer closure、workflow/standalone
  parity、installed/platform projection 与 production activation继续由 E434交付。

本 slice 不新增 ADR。`ADR-015` 已拥有 TaskId/lifecycle 与 framework-extension boundary。
