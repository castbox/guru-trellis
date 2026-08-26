# Guru Trellis Evolution Design SSOT

状态：`design_ready_for_delivery_planning` / `requirements_input_current` / `fresh_design_review_passed`。本目录已重新绑定
通过 `REQ-REV-011..132` fresh gate 的 `evolution-requirements-revision-2026-08-27` exact ready identity，
修订后的 exact candidate 已完成 fresh Evolution Design 全稿审核与确定性闭包，`DES-REV-001..014`
全部关闭，open P1、blocking P2、P3 与 high-risk question 均为 0。它描述待交付的新合同，
不表示 current runtime、`.40`
as-built Design、preset、平台投影或 Release 已经改变。

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

本目录与 `docs/design/versions/current-main-0.6.5-guru.40/` 并存是 current/target 文档状态分离，
不是 runtime dual-read。任何实施、激活、promotion、commit、push、PR、merge 或 Release 都需要后续
独立授权和对应 gate。
