# #376 Base-continuity command Design contribution

- `D376-CONT-01`：Reconcile 将 base pair 与 authority/task-content facts 分开判定；普通无关 base delta
  保留原 `resume_target`，真实 authority/content drift 保持 planning/implementation/full-review 路由。
- `D376-CONT-02`：`execute-base-reconciliation` 只接受 branch-bound clean worktree、expected task/base
  heads、prior review、candidate tree 与目标 commit message；执行前后验证 ancestry/tree，并只创建本地 commit。
- `D376-CONT-03`：reconciliation receipt 与 private pair checkpoint 只保留后续 checker 直接消费的
  identity；不记录用户授权。commit 已形成时 recovery 先校验 current-pair checkpoint，再应用普通 stale guard。
- `D376-CONT-04`：Review Branch `base_continuity` 以 prior full review 和 current reconciled HEAD 为两个
  不同字段；gate review commit 绑定 current HEAD，public output 删除 Publication/router 不消费的 prior-review 字段。
- `D376-CONT-05`：Publication schema 与 `guru-reviewed-content-1.0` 不放宽；真实跨 Skill integration 调用
  Publication recorder、checker 与 public wrapper，证明 continuity-reviewed current HEAD 可得到 `ready`。
- `D376-CONT-06`：Architecture/RDT `.46` promotion 只增加本能力及 23/97/78 graph；`.45` 正文与 release
  facts 不改，只增加 `superseded` / `successor=.46` lifecycle locator，并将其 Design manifest 的错误
  `command_count: 81` 校正为真实历史值 `77`；Evolution target、Issue #108 sidecars 和完整
  Release/upgrade matrix 保持原 owner 与历史边界。
