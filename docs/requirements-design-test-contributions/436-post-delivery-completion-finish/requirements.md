# #436 Post-Delivery Completion And Finish Requirements contribution

状态：`reviewed_promoted`。本 contribution 已提升到 `current-main-0.6.17-guru.56`；`.55` 为 immutable predecessor。

- `R436-01`：`guru-review-task-completion` fresh 汇总 accepted scope、全部 Delivery facts、current authority、remaining work 与 evidence；只在全部完成时返回 `completed`，其余六个 closed exits 保持同一 task active 或明确阻塞。
- `R436-02`：`guru-complete-task-closure` 只消费 current Completion approval。no-Issue/reference-only/follow-up/parent 返回 `no_mutation`；exact source Issue 的关闭必须展示精确动作、独立确认并支持同一 transaction recovery。
- `R436-03`：`guru-finish-task` 只在 Closure 后执行。它以独立确认承接 local archive projection、bookkeeping commit/push/PR 与 expected-head merge，并仅在 remote target 验证唯一 archive、active removal 和 terminal metadata 后返回 `success`。
- `R436-04`：`guru-cleanup-task-resources` 只消费当前 Finish receipt，fresh 审查本轮 owned resources，独立确认后删除；失败不回滚 Completion/Closure/Finish，且保留用户 checkout、其它 task 与仍有 consumer 的状态。
- `R436-05`：`guru-reactivate-task` fresh 验证正常结束 archive、原 scope、历史 Delivery、current base 与恢复原因；保留 task/Issue identity，复用 clean exact workspace 或从当前 base 创建新 workspace，保证 active/archive 唯一副本并使旧 Finish receipt 失效。
- `R436-06`：五个 packages、closed schemas/consumers、canonical/installed/platform projections、lifecycle SSOT 与定向 tests 必须 additive 完整分发。#434 前 production graph 保持 22 invokes / 98 exits，不新增 adapter、ledger、dual graph 或旧 output reader。

完整多平台 Release matrix、#434 graph activation、shared RDT/Architecture promotion、Issue closure 与当前任务的 commit/push/PR/merge/cleanup 均不由本 contribution 自动授权。
