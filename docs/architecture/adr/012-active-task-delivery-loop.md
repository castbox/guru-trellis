# ADR-012: Active Task Delivery Loop ownership and identity

状态：`proposed`。来源：Issue #435 `2026-09-18-r3`、task planning 与 task-owned [Architecture contribution](../contributions/435-active-task-delivery-loop.md)。只有 independent committed full-diff review 和 expected-`current-main-0.6.17-guru.54` serialized promotion 能把本 ADR 变为 accepted。

## Context

Current lifecycle把 Publication、remote publication、task archive、Ready、Merge、Issue closure expectation与terminal response串成单次 closeout。该 topology不能表达同一 active task 的多个业务 Delivery；Merge发现task-work finding时必须恢复已归档task；历史发现又依赖当前branch/PR tail。#405暴露PR创建后binding/output loss，#407暴露base conflict适配完成后缺少contract-valid resolved merge commit入口。

父Issue #434要求唯一新 lifecycle：active task经历一个或多个Delivery cycles，随后由#436独立判断Completion、Closure、Finish与Cleanup。#435只能交付additive capability，不能提前切换production graph。

## Proposed Decision

1. 新增三个semantic owners：`guru-review-task-delivery`独占当前slice readiness与PR payload truth；`guru-publish-task-delivery`独占push/PR/Draft/Ready与同计划恢复；`guru-merge-task-delivery`独占merge readiness、confirmation、mutation、terminal recovery与Delivery result。
2. 每次Delivery merge后task保持active。`delivered`的唯一consumer是#436 Completion；它不表达task complete、Issue closure、archive、Finish或Cleanup。
3. Planning明确task scope、current delivery slice、remaining work与independent delivery conditions。Check、Task Commit、Branch Review保持原owner，只按approved slice判断满足性并继续审查完整candidate影响。
4. Delivery PR只使用`Refs`。Issue closure由#436 Completion后的独立Closure owner执行；Delivery Review/Publish/Merge不携带closing keyword且不调用Issue close API。
5. Cross-branch Delivery identity写入受控merge commit body的闭合versioned trailers：stable task identity、schema version、exact reviewed head。Discovery以GitHub PR/merge identity、merge commit、parents、repository/base与trailers交叉验证。PR body、current branch、remote branch存活和creation branch/base不构成identity authority。
6. 仓库必须支持Merge owner控制的merge-commit method与exact subject/body。仅支持squash/rebase时在mutation前blocked；不回退到ledger或弱identity。
7. #405 equal-head recovery迁移到Publish owner；#407 resolved-tree commit进入Reconcile owner并绑定fresh Phase 2。两者均保持same-mutation recovery与零重复side effect。
8. 新packages、schemas、consumers、tests与managed projections先additive交付，production workflow保持旧链。#434在#435/#436均ready后原子接通新图并退休旧edges；不存在old-output adapter或dual runtime graph。

## Rejected Alternatives

- Delivery ledger：增加长期writer、迁移与一致性责任，Git/GitHub immutable facts已满足直接consumer。
- PR body identity：payload可编辑且属于reviewer-readable publication内容，不能承载stable lifecycle identity。
- Current branch或branch name discovery：remote cleanup与Reactivate换branch会丢失历史或产生歧义。
- 覆盖task creation branch/base：破坏immutable creation history，并与#436 current workspace binding冲突。
- 复用旧Finalizer output并加adapter：形成双owner/双graph，违反#434 atomic cutover。
- Squash/rebase fallback：缺少受控merge commit trailer与稳定two-parent topology。
- Merge后直接Completion pass或archive：把Delivery success重新等同task completion。

## Consequences And Adoption Gate

新设计增加三个public Skill IDs及其closed schemas/consumers，并直接演进少量existing owner contracts。实现必须提供两个顺序Delivery、#405、#407、Reactivate new binding、bookkeeping exclusion、Refs-only、merge output loss、zero duplicate side effects与source/installed/projection evidence。

Task-local Architecture/RDT contributions必须先通过independent committed review，再由serialized owners按expected `.54` promotion。Promotion-created diff必须fresh重跑Phase 2、Task Commit与完整Branch Review。#434 cutover与#436 Completion/Finish E2E不由本ADR adoption证明；Release matrix也不由本任务证明。
