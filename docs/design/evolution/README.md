# Guru Trellis Evolution Design SSOT

状态：`design_ready_for_delivery_planning` / `fresh_design_review_passed` / `evolution_refactor_eligible`。本目录已基于
`REQ-REV-133..138` 修订历史 Design projection：#311/#312 prerequisite、installed publication terminal、
standalone verifier failure evidence 与 original-worktree continuity 已分别归入 two-stage eligibility、
Publish/Finish/Merge、Projection 和 Reconcile owner。Requirements 现为 52 UC / 83 REQ / 33 NFR / 23 current
capability / 13 target delta / 50 fixture；候选 Design 为 `EVO-DES-001..073`，50/50 fixture 均有 Design
mapping。原 `DES-REV-001..014` review 绑定仍然失效；当前完整候选已关闭 `DES-REV-001..043`，fresh 全稿
审核得到 open P1、blocking P2、P3 与 high-risk question 全部为 0，并通过确定性闭包，因此已成为
`design_ready_for_delivery_planning` / `fresh_design_review_passed` / `evolution_refactor_eligible`。#311/#312 merge、`.41`
RDT/Architecture/inventory fresh rebind、requirement/normal-path fixture successor 零差集与 merge 后 fresh
Requirements 双审已经 current；本 continuation 仍停留在 Phase 1，只完成 Design gate。它不表示 current runtime、
`.41` as-built Design（`.40` 仅为历史 comparison evidence）、preset、平台投影或
Release 已经改变。

读取顺序：

1. [`design-main.md`](./design-main.md)：系统边界、完整 workflow、RDT/Architecture 生命周期与状态模型；
2. [`contracts.md`](./contracts.md)：唯一 semantic owner、public input/output、typed exit、consumer 与 re-entry；
3. [`stock-and-distribution.md`](./stock-and-distribution.md)：17 个 stock asset 的选定动作、平台投影、安装与迁移；
4. [`capability-inventory.md`](./capability-inventory.md)：current capability 与 target successor 差集；
5. [`traceability.md`](./traceability.md)：Requirements -> Design -> Test fixture 追踪；
6. [`decisions.md`](./decisions.md)：设计取舍与未选方向；
7. [`delivery-plan.md`](./delivery-plan.md)：串行 delivery slices、依赖和 acceptance criteria。

Test authority 位于 [`../../test/evolution/`](../../test/evolution/README.md)。Architecture impact
位于 [`../../architecture/contributions/305-evolution-workflow-convergence.md`](../../architecture/contributions/305-evolution-workflow-convergence.md)。

本目录与 `docs/design/versions/current-main-0.6.5-guru.41/` 并存是 current/target 文档状态分离，
不是 runtime dual-read。任何实施、激活、promotion、commit、push、PR、merge 或 Release 都需要后续
独立授权和对应 gate。
