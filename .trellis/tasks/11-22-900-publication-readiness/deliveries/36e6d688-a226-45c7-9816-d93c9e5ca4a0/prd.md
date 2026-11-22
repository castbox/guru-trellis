# 发布入口收敛需求

## 1. 整体来源与术语

本 Delivery 采用[整体 PRD](../../prd.md)的已登记范围，覆盖 AC1 和 AC2。直接来源为 [#900](https://github.com/castbox/guru-trellis/issues/900) 的行为要求与验收。上位来源为 [#736](https://github.com/castbox/guru-trellis/issues/736) 第 8 项的 readiness 合并要求和 AC7 的发布部分。#794 是独立审查前置的历史依据。readiness 指 AI 判断该切片是否具备独立发布资格。发布事务处理实际远端写入和同次操作恢复。

## 2. 整体与本批目标、非目标

当前调用方需要先取得单独的 Delivery Review 结果，再进入 Publication。本批将 readiness 和准确预览纳入 Publication 的公开入口，并迁移相关正常、返工和续接路径。保留独立候选审查、架构资格、独立 Merge 确认、Task Completion 与 Closure。归档合并评估由其它范围承担。

## 3. 本批起点、前序结果、依赖与剩余责任

首个 Delivery 尚无前序结果。开发起点为 `origin/main@f06eddb6ccf97ddd2d1a41c117692f5957cb2dc7`。PR 目标为 `castbox/guru-trellis:main`。依赖原 Branch Review 的固定候选及 Architecture 的适用资格，复用发布事务和同一 PR 恢复。切片覆盖 #900 的全部功能范围。交付后仍需原 Task Completion 复核整个范围与实际证据，再走 Closure 和 Finish。

## 4. 本批调用方、场景与流程

- SC1。workflow 持有已通过独立审查的固定已提交候选。调用 Publication 后取得实际 readiness 与预览。确认当前预览后执行对应远端写入并回读。满足前置时可交付原 Merge。
- SC2。审查或架构资格失效时，Publication 回相应原职责。readiness 发现规划、实现或范围问题时，Publication 停止待执行远端动作并返回问题及原处理职责。
- SC3。同一 Delivery 已有发布状态或 PR 时，Publication 先回读事实，再恢复已完成动作或继续待执行动作。已合并 PR 直接交原 Merge 恢复。

## 5. 完整行为、条件与约束

- S-R1。发布入口核对当前适用的独立审查和架构资格。AI 用获批范围、实际交付与验证、剩余 Task 责任及未验证边界判断 readiness。
- S-R2。readiness 通过后展示准确的中文 PR 标题和正文，披露本次交付、剩余责任和未验证项。具有适用源 Issue 时使用 `Refs`。Closure 在整体完成后处理 Issue。
- S-R3。仅在本次候选及实质预览已确认后执行对应 push 和 PR 操作。相关候选或发布事实变化时刷新受影响结果。待执行写入或已展示预览实质变化时重新展示并确认。
- S-R4。有效的现有同 Delivery 事务与 PR 保留身份。回读已经完成的操作。剩余操作遵循当前前置和确认边界。只有当前候选和发布结果满足前置时才交 Merge。已合并接续走原 Merge 恢复。
- S-R5。同步受影响的公开调用、正常和回程路由、续接、最小调用示例、失败消费、兼容迁移及声明平台投影。

## 6. 本批验收、验证方式与未决项

- AC1（SC1，S-R1–S-R3、S-R5）。从正常公开入口提交已审候选，观察直接取得准确预览、确认前后的远端状态，以及符合前置时可被原 Merge 消费的发布结果。
- AC2（SC2、SC3，S-R3–S-R5）。通过真实入口验证前置失效、readiness 拒绝的回程及远端状态，覆盖受影响的在途操作，观察同一 PR、已完成动作回读和待执行动作续接。已合并接续可采用仍适用的原验证证据。
- 产品范围已有明确来源。公开合同版本、适配范围及迁移路径由方案与 Architecture 评估确定。

## 7. Canonical 引用与本轮差额

- `docs/requirements/current/task-delivery-lifecycle.md` 的交付事实与整体完成。更新 readiness 的入口责任，保留 Refs 和整体完成边界。
- `docs/design/current/task-delivery-lifecycle.md` 的 D636-02、D636-04/05。更新公开接续和存量恢复合同。
- `docs/test/current/task-delivery-lifecycle.md` 的 T636-02、T636-05、T636-06。补足从新入口看到的正常、停止、恢复及安装投影证据，保留适用历史证据边界。
- `docs/architecture/03-domains/ownership.md` 的 ARCH-DOM-017 与 `docs/architecture/01-current/system.md` 的 ARCH-CUR-075。评估 Publication 接管 readiness 后的 owner 与依赖边界。
