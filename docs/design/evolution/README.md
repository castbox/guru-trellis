# Guru Trellis Evolution Design SSOT

状态：`design_ready_for_delivery_planning` / `fresh_design_review_passed` /
`evolution_refactor_eligible`。本目录已基于
`REQ-REV-133..142` 修订 Design planning projection：#311/#312 prerequisite、installed publication terminal、
standalone verifier failure evidence 与 original-worktree continuity 已分别归入 two-stage eligibility、
Publish/Finish/Merge、Projection 和 Reconcile owner；PR #317 exact installed platform-set preservation 已投影到
既有 Publish/Finish/Projection responsibilities。Requirements 现为 52 UC / 84 REQ / 34 NFR / 24 current
capability / 13 target delta / 50 fixture；候选 Design 为 `EVO-DES-001..073`，50/50 fixture 均有 Design
mapping。原 `DES-REV-001..014` 与 pre-`REQ-REV-142` 的 `DES-REV-001..052` review 绑定均已 stale；本轮
planning projection 已完成 fresh Design 全稿审核与确定性闭包，P1/P2/P3 finding 与 high-risk open question
均为 0，因此 current 状态为 `design_ready_for_delivery_planning` / `fresh_design_review_passed` /
`evolution_refactor_eligible`。#311/#312 merge、`.44`
RDT/Architecture/inventory fresh rebind 与 requirement/normal-path fixture successor 零差集 projection 已同步，
fresh Requirements semantic、Strict technical 与确定性闭包审核已通过；`.42` 相对 `.41` 只增加 `.3/.39/CLI 0.6.15` candidate/target alignment，`.43` 增加 `CUR-CAP-024` repo-private release orchestration current facts，`.44` 增加 #332 `.5/.40/CLI 0.6.15` Release Gate facts并提升 #240/#348 reviewed owner/RDT/ADR authority；current public graph 为 23 Skills / 97 exits / 81 commands，这些变化均由既有 target deltas 承接，
`a41b8a34...9f560ec1` 只修正 #267 lifecycle evidence、dogfood provenance 与 archive/merge facts；
`9f560ec1...736ef333` material advance 新增 platform selection 保真，但未增加 Evolution UC、核心能力、
delta、fixture 或 Design responsibility，并把 latest stable current 修正为 `.2/.38/CLI 0.6.15`，`.3/.39`
仍 unverified；`736ef333...5650df47` 再次只修正 caller-inventory consistency、Issue disposition、dogfood
provenance 与 archive/merge facts。本 continuation 仍停留在 Phase 1 Requirements-to-Design boundary，并明确停在 fresh
Design review 前。它不表示 target runtime、`.44` as-built Design（`.43`/`.42`/`.41`/`.40` 仅为历史 comparison evidence）、preset、平台投影或
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

本目录与 `docs/design/versions/current-main-0.6.5-guru.44/` 并存是 current/target 文档状态分离，
不是 runtime dual-read。任何实施、激活、promotion、commit、push、PR、merge 或 Release 都需要后续
独立授权和对应 gate。
