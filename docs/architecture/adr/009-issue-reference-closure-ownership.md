# ADR-009: Issue reference and closure ownership

状态：`accepted`。来源：Issue #247 reviewed Architecture contribution。Promotion input：
`current-main-0.6.5-guru.49`；current successor：`current-main-0.6.5-guru.50`。Independent reviewed range：
`origin/main@ec016827fac81d33faeacb307b0db76d5259dc28...9c3c00908446ac0fa86974cb9886f37917ac40ca`。

## Context

Task-local `issue-scope-ledger.json` 把 external work item reference、Issue closure intent、关闭执行和
结果验证聚合为跨阶段 authority。该 aggregate 迫使 Workspace、Planning、Commit、Review、Finalizer、
Merge、Finish 与 recovery 共享 `primary_issue`、`close_issues`、`related_issues`、`followup_issues` 等
分类，即使各 owner 只需要自己的 current authority 或 live facts。

移除 ledger 不能只做内部重构：current workflow 还需要明确 Issue-backed completed、remain-open、
no external work item 与 non-default-base PR 的长期关闭语义，以及谁判断、谁执行、谁验证。

## Decision

采用 `target_native` authority boundary，并直接演进受控 public Skill contracts：

1. requirement/scope/source reference 由 current user、live external authority 和对应 lifecycle
   semantic owner持有，不形成 task-local Issue classification aggregate；
2. Publication 是 Issue reference 与 closure intent 的唯一 semantic owner，基于 current requirement
   authority、reviewed diff、target/default branch 与 live Git/GitHub facts形成 reviewed PR body；
3. Issue-backed delivery 完整解决 current Issue 且 PR 目标为默认分支时，Publication 默认写入 GitHub
   closing keyword；remain-open 必须引用 current authority 中具体的合并后未完成条件；
4. 无 external work item 时不产生 Issue 引用或关闭效果；目标为非默认分支时当前 PR 只引用，后续进入
   默认分支的 Publication 基于届时 authority fresh 判断；
5. Finalizer 只绑定并执行 reviewed Publication payload，并向 Merge 投影 exact reviewed PR body 的
   最小 SHA-256 identity，不重新判断关闭范围；
6. GitHub 在 closing-keyword PR 进入默认分支时自动执行关闭；Merge 只做独立 readiness、expected-head、
   当前 merge confirmation 与 merge 后 live PR/Issue result verification；merge mutation 前必须验证 live
   body identity 与 Finalizer handoff 一致，不一致时直接 fail closed，由调用方重新进入 fresh
   Publication/Finalizer；Merge 不新增 reprepare typed exit，也不调用 Issue close API；
7. 旧 ledger、旧 task DTO/schema/invocation 不迁移、不 dual-read、不提供 adapter 或 compatibility reader。

## Consequences

- reference、closure intent、closure action 与 closure result 获得独立语义和 owner。
- public DTO 直接删除 ledger-era aggregate；current consumer必须读取自己的 authority 或最小 transition。
- preset/update 不拥有或主动触碰磁盘上的 legacy ledger；文件存在与否不影响 current runtime。
- Finalizer/Merge/Finish/Restore/Cleanup 不获得替代 closure decision authority。
- shared current 已由 Architecture promotion owner在 #247 committed review 后绑定 expected `.49` 串行提升为
  `.50`；promotion diff仍需 fresh Phase 2、commit 与 Branch Review。

## Rejected Alternatives

- 保留或重命名 ledger aggregate：继续形成跨 owner 第二 authority。
- nullable 旧字段、adapter、dual-read/write 或旧 task migration：与 #247 的 current-only contract冲突。
- 由 Finalizer 或 Merge重新判断关闭范围：会产生多个 semantic owner并使 Publication payload不再完整。
- workflow 调用 Issue close API补偿：绕过 GitHub closing-keyword 的默认分支语义与 live result验证。
- 在非默认分支 PR声称 closing keyword 会关闭 Issue：GitHub实际效果与声明不一致。

## Verification And Promotion

Acceptance 必须覆盖 active ledger inventory 为零、Publication 四路 effect、Finalizer payload binding、
Finalizer-to-Merge body identity continuity、body-only drift pre-mutation rejection、Merge live closure
verification、legacy absent/present 等价、current-only rejection、canonical/dogfood/
installed/Shared/Codex/Claude/Cursor parity，以及一个代表性 install/update 场景。完整多平台
exact-candidate Release matrix、tag、GitHub Release和生产业务仓验证保持 deferred。

本 decision 已随 `.50` serialized promotion 进入 current authority。该 promotion 只接受 reviewed #247
contribution 与 inherited immutable `.49`，不修改 #305 target、framework/CLI/extension/release独立版本轴，
也不证明 push、PR、merge、tag、GitHub Release、生产业务仓验证或 Issue closure。
