# ADR-009: Issue reference and closure ownership

状态：`accepted`，已按 live Issue #247 `2026-09-13-r24` 修订。Promotion input：
`current-main-0.6.5-guru.49`；current successor：`current-main-0.6.5-guru.50`。最初 reviewed range：
`origin/main@ec016827fac81d33faeacb307b0db76d5259dc28...9c3c00908446ac0fa86974cb9886f37917ac40ca`；
r24 corrective diff 必须重新完成 fresh Phase 2、commit 和 independent full-diff Branch Review。

## Context

Task-local `issue-scope-ledger.json` 把 external work item reference、Issue closure intent、关闭执行和
结果验证聚合为跨阶段 authority，迫使多个 owner 共享 `primary_issue`、`close_issues`、
`related_issues`、`followup_issues`。#247 删除该 aggregate，但 r24 明确要求当前旧 lifecycle 的行为、
public producer/consumer、edge、target/stop、archive、Ready、Merge 与 Restore 语义保持不变。

## Decision

采用 `dedicated_refactor_slice`：

1. requirement/scope/source reference 由 current user、live external authority 和对应 semantic owner持有，
   不形成 task-local Issue classification aggregate；
2. Publication 继续按 current authority 和 reviewed delivery 判断 reference 与 closure intent；Issue-backed
   completed/default-base 可写 closing keyword，reference-only 保持 empty close set，no-Issue 不制造引用；
3. Finalizer 保留 current preparation、push、PR create/update、official archive、Ready、handoff、existing-PR、
   lost-result、reprepare 与 terminal recovery，只删除 ledger 输入；
4. Finalizer 向 Merge 保留 archived locator、reviewed close set 所需步骤局部输入和 exact reviewed PR body
   SHA-256；这些字段只服务直接 consumer，不构成长期 scope aggregate；
5. GitHub 在 closing-keyword PR 进入默认分支时执行关闭。Merge 保留独立 readiness、expected-head、merge
   confirmation、post-merge closure verification 和四个 declared exits，不调用 Issue close API；
6. `phase2_reentry_required -> guru-restore-archived-task` 保持 current recovery；Restore 不成为正常多 PR
   lifecycle 的新 owner；
7. legacy ledger 不迁移、不 dual-read、不提供 adapter/compatibility reader；preset/update 不主动触碰；
8. canonical 与 installed manifest 声明 `guru-ledger-free-runtime@1.0.0`，只证明 ledger-free runtime 和
   current projection identity，不宣称新 lifecycle 或 Release 已完成。

## Consequences

- ledger writer、reader、registration、aggregate DTO 与 ledger-only assets退出 current graph。
- 旧 workflow 的 producer/consumer、23 Skills / 97 exits / 78 commands、target/stop 和行为时点保持。
- Finalizer 的提前归档、PR 冲突后接续和同一 task 多 PR 的限制仍是已知问题，由后续 Issue 渐进处理。
- historical archived completed tasks 不 backfill；legacy ledger absent/present-A/present-B 不影响 fresh result。
- `.50` 保持唯一 active authority；immutable `.49` 不回写。

## Rejected Alternatives

- 保留、改名或隐藏 ledger aggregate：继续形成跨 owner 第二 authority。
- Refs-only、禁止 Finalizer archive、Merge 后 task 保持 active 或 conservative Delivery consumer：属于
  r21/r22 已被 r24 废止的生命周期改造，不进入 #247。
- 由 Finalizer/Merge 重新判断 closure，或 workflow 调用 Issue close API：产生第二 closure owner。
- 引入 #398 migration stop/global graph，或要求 #248/#261/#293 等未来 package：破坏独立交付边界。

## Verification And Promotion

Acceptance 覆盖 active-zero inventory、task creation no-ledger、Publication close/reference-only/no-Issue、
Finalizer archive/Ready/recovery、Merge 四 exits、archived Restore、legacy absent/present 等价、capability
shape、canonical/dogfood/installed/platform parity，以及真实 production wrappers 的代表性旧流程 E2E。
完整多平台 Release matrix、tag、GitHub Release 和生产业务验证保持 deferred。
