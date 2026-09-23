# #454 C3 Checkout Acquisition Provenance Requirements Contribution

状态：`reviewed_promoted`。本 contribution 由 expected current
`current-main-0.6.17-guru.60` 提升到 successor
`current-main-0.6.17-guru.61`。原 C3 `.60` authority 保持 immutable；本增量
只闭合 output-loss recovery 的 transaction-origin 连续性。

- `R454-C3-10`：transaction-created linked worktree 必须携带一份闭合、owner-private、普通 JSON provenance marker，位置只在该 worktree 的 Git administrative directory；marker 绑定 transaction/result、task/generation、branch/HEAD、target、disposition、action 与 ownership projection，不进入 public DTO 或 durable lifecycle authority。
- `R454-C3-11`：read-only output-loss recovery 必须同时验证 fresh live Git facts 与 exact provenance marker。原资源被删除后，同路径或不同路径、同 branch/HEAD 的 caller replacement 缺少原 marker，必须 fail closed，且不得获得 `guru_owned` cleanup ownership。
- `R454-C3-12`：existing-checkout reuse 不写 marker；direct handoff 必须在 consumer invocation 前 retire marker。marker 创建、retirement 或 callback 失败时，只回滚本 transaction 创建且 identity 仍匹配的资源；recovery 本身不得修改 Git 或 marker。

本增量不引入 workspace mapping、resource ledger、branch/session store、锁、
inode、PID、process、FD、signal、并发或 crash-consistency 协议。C4-C7、
D443、D436、E434 与 production activation 保持独立后续范围。
