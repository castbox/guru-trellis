# #436 Post-Delivery Completion And Finish Design contribution

状态：`reviewed_promoted`。采用 `target_native`，关联 Architecture contribution `architecture-contribution-436-post-delivery-completion-finish-v1`，successor 为 `.56`。

- `D436-01`：Completion 使用 semantic owner authoring 和 closed public projection。`completed` 才携带 fresh `completion_ref`/Closure seed；evidence refresh 是 fresh profile，不能预填 pass 或伪造 Delivery。
- `D436-02`：Closure 将 source disposition 与 provider mutation 分离。`no_mutation` 和 `closed` 都产生真实 `closure_ref`；exact close transaction 只保存恢复同一 repo/Issue/action 所需的 owner-private state。
- `D436-03`：Finish 使用三阶段 transaction：archive projection、bookkeeping publication、expected-head merge。allowlist 只含 exact active/archive lifecycle paths；payload 禁止 closing keyword 与 Delivery trailer；post-check 读取 remote target branch。
- `D436-04`：Cleanup 的 semantic result绑定 current Finish receipt和 exact resource set；执行器只删除已确认且无 active consumer 的 branch/worktree/runtime targets，不修改 archive 或前序 terminal facts。
- `D436-05`：Reactivate 以 stable task id和 archive Git facts选择 `reuse` 或 `create` workspace plan，拒绝 base branch 作为 task branch；mutation移动唯一 archive副本、刷新 metadata/mappings/session binding并删除旧 Finish receipts。
- `D436-06`：五个 package 在 canonical registry 中保持 additive/deferred，installer 同步 Shared/Codex/Claude/Cursor 与 installed projections并消费匹配 canonical bytes 的 managed `.bak`。production workflow markers与旧 lifecycle edge保持不变。
- `D436-07`：public I/O 按 exit最小化并绑定唯一 consumer；复杂事实、provider snapshots、授权过程和 recovery internals保持 transient 或 ignored owner-private。脚本只验证 closed schema、identity、freshness、allowlist和确定性 mutation。
- `D436-08`：同月/跨月 rearchive使用显式 final `archive_ref`；旧 archive只能作为 reviewed deletion root。历史 Completion/Closure/Finish仅作历史事实，Reactivate 后必须 fresh重跑。
