# ADR-015: Task Lifecycle Identity And Stage-Evidence Ownership

状态：`accepted`。来源：Issue #454 reviewed contribution；提升：`.58 -> .59`。

## Context

Tracked task metadata、official task/session store、Guru runtime mappings 与 Git/worktree facts 曾同时承载
task identity、locator、base、HEAD、checkout、session 和 resource ownership。稳定性不同的事实被当成同一对象后，
rename、archive、Reactivate、base reconcile、Branch Review 与 cleanup 会产生重复 authority 和 stale handoff。

## Decision

TaskId 是 immutable repository-local identity；TaskRef 是 mutable locator；lifecycle generation 只由 Reactivate
递增。Fork official task/session primitives 独占 framework identity 与 persistence；Guru shared lifecycle catalog
和 runtime 只提供 package-neutral DTO、normalization、resolver adapter 与稳定错误，不建立 durable identity index、
第二 session store、workspace mapping reader、compatibility alias、dual-read 或 dual-write。

Base pair、old/new base SHA、integration commit 与 review anchors 只属于当前 operation 及其相邻 consumer，不进入
durable task identity。Pre-review compatible reconcile 创建 expected-head-bound two-parent committed HEAD；
`post_check` / `post_commit` 回 fresh Phase 2。首次/full Branch Review 要求 selected base 是 review HEAD 祖先；
bounded continuity 只承接已有 prior full review，并验证 base ancestry 与 candidate tree identity。

#454 `.59` current 只接受 C2 shared kernel 与 D0 stage-evidence correction。C3-C7、D443、D436 仍由后续
package/runtime migration owner承接，#434 独占最终 production graph activation 与旧 edge retirement。

## Consequences

Current authority 可以使用同一 lifecycle identity/value domain 与 stage-evidence lineage，但不能把 package存在、
promotion 或定向测试解释为完整 lifecycle 已实现。active registry 保持 32/142/102，production workflow 保持
22 mandatory invokes / 98 exits。Promotion-created diff 必须重新通过 fresh Phase 2、Task Commit 与独立完整
Branch Review；Publication、push、PR、merge、Release、Issue closure 和 Cleanup 均不由本 ADR 授权。
