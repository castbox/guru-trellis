# #724 Architecture 隔离贡献

TaskId：724-codex-shared-skills；generation：0；Delivery：a831ddba-681c-480a-9eb9-1e350f48a43d。状态：promoted。原 Architecture owner 已完成本轮知识晋升；最终 Check 和 committed Review 尚待执行。

## Authority 与实际差额

适用 source 为42ffd32d70be3859a4493e084464738473c45dd6；baseline guru-trellis-architecture、constitution guru-trellis-design-constitution-v1、change-contract guru-trellis-architecture-change-contract-v1。实际独立 candidate_assessment 为 architecture_impact / target_native，decision refs ARCH-INT-006、ARCH-DOM-020、ARCH-STACK-SOURCE-001。

Codex 公共发现根收敛到 .agents/skills，平台适用性和 exact target selection 保持；旧根只用于原 owner 的一次性受管退出。目标完整、冲突保留、重试和验证分层的完整决策由 ADR-CODEX-SHARED-SKILLS 拥有。

## 本轮晋升 targets

相邻724-codex-shared-skills/proposed/ 保留完整后像：
- docs/architecture/04-integrations/distribution.md：窄修改 ARCH-INT-006。
- docs/architecture/03-domains/ownership.md：补齐 ARCH-DOM-020 的共享根及原迁移 owner 边界。
- docs/architecture/adr/codex-shared-skills.md：必要 ADR，说明理由、成本、替代和重审条件。
- docs/architecture/adr/README.md：仅新增该 ADR 导航。

本轮保留 Architecture root identity。原 owner 在 candidate_checked 后于 final_integration 比较实际前像，采用已审完整定义并保留其它有效条件。相邻 proposed 后像保留规划来源；ADR 状态在实际采用时改为 accepted。

## 适用 concerns 与验证边界

authority-binding、constitution-binding、boundary-and-decision、owner-and-single-writer、compatibility-and-exit、gap-and-deviation、parallel-scope、evidence-and-freshness、review-and-promotion 均适用。当前公开根是应用层安装决策；原 installer/maintenance 单写，用户内容/原生能力前置保留，旧消费者在同批迁移退出。不存在新 authority、双根兼容、锁或长期迁移状态。

实现主文件的3000行边界由原 owner 的机械提取承接；独立 phase2 审完整实现与 proposed targets，原 Check candidate_checked 后集成真实 targets、重绑候选并执行最终质量链。实际安装、native、正式 source-lock 与发布矩阵分别由本 D1 validation 记录。本贡献的晋升不证明最终 Check、committed Review、Delivery 或 Task 完成。

