# Phase C Architecture Change Contract

## 1. Identity

- Task: `.trellis/tasks/09-20-454-task-lifecycle-state-model`
- Requirement authority: live `castbox/guru-trellis#454`
- Guru Architecture public contract: `guru-maintain-architecture-baseline:2.0`
- Current baseline: `current-main-0.6.17-guru.58`
- Constitution: `docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`
- Project change contract: `docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1`
- Change path: `target_native`
- Contribution id: `architecture-contribution-454-task-lifecycle-state-model-v1`
- Expected current identity: `current-main-0.6.17-guru.58`

## 2. Boundary and decision

Current boundary混合tracked task metadata、Fork session/task store、Guru workspace mappings与package-local resource
assumptions。Target boundary分为：

1. `castbox/Trellis` Fork独占official TaskId/TaskRef/generation/session primitives；
2. Guru lifecycle kernel独占branch association、checkout acquisition/resolution、resource ledger与shared DTO；
3. Phase D package owners消费substrate但不复制authority；
4. Phase E434独占production graph与distribution activation。

Decision refs：`ARCH-FND-001..006`、`ARCH-CUR-031`、`ARCH-INT-019`、ADR-011、Design Constitution五项原则。
本task关闭旧task_workspace/mapping GAP；不重开developer/workspace journal或第二session store。

## 3. Required concerns

| Concern | Applicability | Phase C contract |
| --- | --- | --- |
| authority-binding | applicable | 同时绑定Architecture 2.0、`.58`与change contract v1 |
| constitution-binding | applicable | 命中official extension surface、owner isolation、minimum complexity与one-way convergence |
| boundary-and-decision | applicable | Fork/Guru/D443/D436/E434边界固定，`target_native`唯一 |
| owner-and-single-writer | applicable | Fork写official primitives；Guru写substrate；E434写active graph/distribution |
| compatibility-and-exit | applicable | 不建dual-read；old production predecessor只保留至E434 atomic cutover |
| gap-and-deviation | applicable | 关闭task_workspace/mapping重复authority；禁止新增alternate store |
| parallel-scope | applicable | Phase C只写task-local contribution与canonical substrate；禁止shared current promotion竞争 |
| evidence-and-freshness | applicable | current-session admission；committed Planning identity；C0 pre-activation fresh reconcile；Fork exact commit；focused tests；Phase 2/full Branch Review |
| review-and-promotion | applicable | task-owned contribution先独立review，再expected-current serialized promotion |

## 4. Owner and single writer

- Framework primitive writer: `castbox/Trellis` Fork task；
- Guru substrate writer: #454 Phase C；
- Bind package writer: Phase D443；
- Reactivate/Completion/Closure/Finish/Cleanup writers: Phase D436；
- workflow/registry/manifest/installed/platform activation writer: Phase E434；
- shared Architecture/RDT promotion writer: serialized Architecture/RDT owners。

任一slice发现需要另一个writer时停止，返回Architecture implementation-discovery re-entry。

## 5. Compatibility and deletion

Compatibility layer: none。

Old production assets保留到E434的原因是避免partial activation，不是兼容承诺。删除条件：Phase D package-ready
identities通过；E434 fresh reconcile通过；old reader/writer/public-id consumer count为0；new graph/selector/manifest/
projection在同一activation candidate中完整。

## 6. Parallel scope

Allowed：Fork独立repository task、#454 canonical substrate、Phase D package tasks、#434 planning读取可并行进行，只要
不修改同一shared current或active selector。

Forbidden：并行修改Architecture current、RDT current、source lock、registry selector、active manifest、workflow
production edges或同一package major。

## 7. Before and after

Before：TaskId可被rename改写；session携带path/TaskRef；mapping、branch、checkout、ownership形成重复authority；
Fork/Guru边界未承接#454 target contract。

After candidate：Fork提供official immutable identity/path-free session；Guru提供单一branch/checkout/ledger substrate；
六个Phase C packages ready但inactive；Phase D/E边界保持；old production graph尚未切换。

## 8. Evidence and review

Planning evidence：live Issue、#454 design 01..12、#456 reconcile 01..04、ownership inventory、Fork source record、
Architecture `.58`。

Implementation evidence：Fork build/tests、Guru package/runtime/schema/eval tests、source preparation、ownership/drift/
sidecar、representative clean throwaway、zero-reader/writer inventory、3000-line report。

ADR：required。原因是本task改变framework/extension owner boundary、state authority和compatibility exit。Candidate
ADR在实施时写入task-owned contribution；shared ADR只在independent full-diff review后promotion。

Promotion state：`planned`。Planning不修改shared current。

## 9. Implementation admission boundary

本change contract不能用target architecture为当前task提供bootstrap authority。进入implementation前必须由current
production owners依次证明：exact current-session task association、fresh approved committed Planning identity、
post-plan pair guard与`guru-reconcile-task-base:post_plan`结果。Base reconciliation在task仍为`planning`时完成，
其`reconciled(resume_target=task_activation)`随后才进入activation。

任一current owner缺失、stale或entry preconditions不满足时保持Planning blocker。禁止直接写session record、
修补legacy mapping/base metadata、调用future Phase C/D package、直接执行upstream start或伪造recovery来跨越该
boundary。
