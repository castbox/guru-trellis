# 正式步骤跨会话交接实施计划

## 1. 输入与引用

读取整体 PRD、当前切片 prd.md、design.md，候选 Architecture 结论按 design 第 1 节。使用原 workflow 合同、既有 session 入口和影响单元。

## 2. 有依赖顺序的步骤与文件责任

1. 枚举 Planning、Phase 2、Branch Review、后续交付与收尾实际委派及接回，核实际正式 owner 所需状态。
2. 更新 canonical workflow 跨阶段规则与触发引用。在 Branch Review Skill 的阶段入口加入会话 gate 链接。同步匹配 workflow 与 Skill 分发。
3. 以两个真实独立评审流程验证，复用同一会话模型的已有状态测试。检查安装投影和 sidecar。
4. 通过原 knowledge owner 整合和读回当前 Architecture/RDT，再进入正式 TaskCommit 和独立完整审查。

## 3. 验证入口、输入与预期观察

V1 真实 Codex 子会话从正式派发运行候选 Architecture 和 Branch Review。观察缺 Task、缺 Delivery 或已匹配状态以及首次依赖调用。V2 用现有 test_receiving_session、read_continuation_context 和相应 Branch Review 测试验证正规状态。V3 运行 check-dogfood-overlay-drift.sh、source/installed package checks、阶段正文提取及 git diff --check。实际输出登记在实施证据。

## 4. 停止条件与适用回退点

身份冲突、没有真实独立评审者、现行 gate 缺失或安装前提不足时回原 owner。业务要求变化回 Clarify，候选设计变化回 Architecture。保留固定内容 B 和已完成合法效果。

## 5. Delivery Policy

full 覆盖 AC01–AC03。通过正常派发、接回和包投影的定向验证后交付，整个 Task 用实际 Delivery 和验证证据完成。无后继责任。

## 6. Docs SSOT Plan

delta_first。原 RDT owner 维护 Task/Delivery Lifecycle 三层既有单元，原 Architecture owner 维护 ARCH-CONTEXT-001 的接收会话职责差额。正式提交前整合和读回，提交后以真实前后范围审查。不存在独立发布、数据库迁移或服务部署。
