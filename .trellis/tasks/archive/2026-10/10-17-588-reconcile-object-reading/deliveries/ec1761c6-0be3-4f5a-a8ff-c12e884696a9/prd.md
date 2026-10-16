# Delivery D1：Reconcile 对象读取性能修复

整体需求以 ../../prd.md 的 AC01–AC10 为唯一验收责任。本 Delivery 完整承接全部十项，不拆剩余工作，不修改整体 accepted scope。

## 必须交付

批量且按唯一 blob 读取索引内容，保持逐路径摘要字节和 gitlink 语义；同次 invoke 复用实际不可变树的内容摘要，同时独立校验两份结果。保持普通整合、resolved baseline/candidate、连续性及原提交恢复入口。

实施前固定摘要和完整正式链的性能/资源数值标准与可重复的重复内容、不同内容大对象 fixture。以原实现和候选相同测量证明达到要求，并执行 canonical/dogfood/installed 正式链、适用 reapply/drift/platform/sidecar 验证。

## 交付边界

只修改原 Reconcile 确定性 owner、必要回归和测量用例、合同说明及受管副本。公共 API/schema/typed exit 不变，不引入持久缓存或跨包 private import。PR 仅 Refs #588；Issue 由 Completion 后 Closure 关闭。工具合并不声称软件正式发布或业务仓采用。

本 Delivery 无额外 normative design selection；Issue 的兼容要求和 #397/#579/#567 已存在合同必须由 design 的唯一 disposition 表逐项承接。
