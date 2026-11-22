# #900 架构贡献候选

Task `900-publication-readiness`，generation 0，Delivery `36e6d688-a226-45c7-9816-d93c9e5ca4a0`。依据 [#900](https://github.com/castbox/guru-trellis/issues/900)、本批[设计](design.md)和固定前驱 `f06eddb6ccf97ddd2d1a41c117692f5957cb2dc7`。这是隔离拟写，适用 `target_native`。

## 当前规范的改动

- ARCH-DOM-017 和相关 ARCH-DOM-029 的发布职责改为 Publication 单写 readiness 和 PublicationFact。Branch Review 仍单写 check/full_review，Architecture 仍独立提供发布资格，Merge 仍拥有合并和 Delivery 结果。
- ARCH-CUR-075 和 change-contract 中的当前顺序改为独立完整 Review、适用发布架构资格、Publication 内 readiness 和准确预览、确认后远端写入、独立 Merge。当前旧结果的持久 producer identity 保持其原义。已执行动作按原事实恢复。
- ARCH-INT-020 和相关接线由 Branch Review 及 Architecture 直接供给 Publication 准备。Publication 以前置及候选约束构建当前预览。失效回原职责。同一 Delivery 的已合并 PR 按是否已有正式 PublicationFact 区分原 Merge recovery 与合法 adopt。
- 合并后整体 Completion、Closure 和 Finish 按各自原入口处理。既有未验证边界和历史记录保持对应观察截止。

## 项目检查及晋升

九项 concern 在架构阶段按本对象判定。候选绑定当前权威和变化范围，保持旧 owner 到新 owner 的单写切换。选择直接迁移当前图，旧操作限定于固定原 provider 和现有合法恢复能力。范围内缺口由 AC1/AC2 关闭，未提出新全局 GAP。规划写在 Task 目录，原 Architecture owner 在工程验证后复核真实目标，将完整定义和受影响关系整合并读回。随后固定提交后的独立 Review 考察 before/after。发布、恢复及分发采用各自实际证据，见 [验证计划](implement.md)。新规则和当前入口的决策见 [ADR 候选](architecture-decision.md)。
