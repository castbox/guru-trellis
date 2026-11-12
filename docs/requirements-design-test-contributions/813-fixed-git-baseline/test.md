# #813 验证差额与截止

完整策略和真实观察位于 `proposed/docs/test/current/runtime-location.md` 的 T718-04/05/07/08 及 #813 节。58 项定向测试、真实旧 provider 边界、source/installed/drift、一个 clean 安装样本、同 App 目标原 operation reapply，以及实际 Agent 创建/恢复分别成立。clean 样本已 cleanup，reapply 与 Agent 使用各自明确对象，不冒称复用该样本。

保留原失败、历史测试截止、外部 provider 隔离与 local_candidate/formal_fork_source_lock 边界。此处没有正式 Check/Review、Merge 或 Task 完成结果；后继由原公共结果承接。
