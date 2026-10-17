# D1 执行计划

## Delivery Policy

staged：D1独立交付Guru历史/恢复读取优化与盘点/基准证据。入口为根accepted scope和原D1身份；出口为本批固定性能/资源标准及真实入口结果等价、Check和完整Review通过后独立PR交付。仍剩D2连续性、D3生命周期/联合回归及明确上游缺口；剩余责任由同Task的Completion owner保留，只有全scope完成才关闭#589。

## 次序

1. 完成修复前多规模测量、补全全步骤盘点与正式调用链计数；记录依赖/工具、预热与缓存、重复次数/汇总。
2. 已依据完整before冻结performance-contract.md：读取和原公开链至少改善20%；canonical RSS100/24MiB、installed/dogfood128/48MiB，后续不放宽。
3. 更新本三份文档，经Wording、finalArchitecture、Approval和原Activation后实现。
4. 原Merge内部元数据批量/唯一blob读取与调用内复用，更新真实caller，删除冗余读取路径。保留原hash与每份输入检查。
5. 正常路径测试覆盖特殊路径、mode、删除、空/二进制/大blob、duplicate/unique、正常missing/读取失败、对象准备隔离、ref相邻操作刷新、手动合并与丢失stdout恢复；history多Delivery用原公开入口生成并查询真实事实。
6. 同输入同口径after对照，报告读取/其他校验/网络/总耗时与所有Git/cat-file/show/ls-tree、对象/字节、Python/Git峰值内存。
7. 原apply同步dogfood并生成代表性installed；源/安装正式链、声明平台、mode、reapply/drift/sidecar定向验证。
8. fresh Check、Task Commit、独立完整BranchReview、DeliveryReview、Publish/Merge；每次说明剩余D2/D3与上游边界。

## Docs SSOT

no_docs_update_needed：本批不改变公共行为/合同/架构authority。性能实验和交付结果由本Delivery原文档承接，不复制既有Requirements/Design/Test语义。若实施发现合同变化，回原Author/Architecture/RDT owner判断，不直接扩大。
