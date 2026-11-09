# 修复 executor 与原冻结资产源的同事务恢复

Identity：`ADR-TOOLS-FROZEN-SOURCE-RECOVERY`。目标正文状态：accepted；来源Issue #769，Task 769-tools-peer-growth-recovery generation 0，Delivery 638e1a19-c4cc-46da-8157-e19293774730。适用before为a5f3ceeabbaccddae65935d97763f5a798f71ca9；原owner为guru-maintain-architecture-baseline。本正文只有经原Architecture final_integration晋升后生效；隔离目录中的候选不建立current。本文不预写实现或验收成功。

## 问题与决定

原tools事务固定source identity，修复后代码不能以原同源resume直接执行旧事务；原peer整字典比较又把正常新增peer视为旧值变化，令旧事务无法续接。选择在同一upgrade-tools owner新增recover_frozen_source，而不是改旧source或checkpoint。修复源提供当前executor；cp.source提供完整原资产包及原legacy helper/installer。当前engine明确以原logical资产package复用，所有原固定source/root/public pair/plan/ref/preimages/freshness继续校验。

原观测键逐项同值，新peer只核与原工具写集物理隔离，不刷新snapshot，不扩大backup或写/删除集。preset按原pending续接，complete只验证；原公共operation复用，rollback先核公共兼容。可恢复失败通过独立frozen_recovery_required保同action/ref回此profile。既有同源profile保持原义。

## 取舍、代价与退出

不采用重prepare、刷新备份、修改旧源或取消注册peer，它们破坏原事务承诺。不采用projected-only终态入口，因为它漏过合法早期恢复阶段并复制完成证明。薄复用原engine减少第二状态机；新增profile/schema/consumer/migration有真实旧schema1.0消费者，包括#766。无双写或数据转换。

兼容由upgrade-tools拥有；原事务终态且恢复保留责任结束后，通过明确迁移删除兼容路径。仍在途旧操作固定其原资产和计划；没有周期扫描、自动GC或通用事务迁移。若原阶段/资产布局、实际旧consumer或隔离合同变化，重新评估，不能静默弱化校验。

## 承接与验证边界

窄补充ADR-027的same-source恢复适用解释，保其单目标/peer隔离、source-target分别验证和public兼容先行。完整当前定义由ARCH-RUNTIME-LOCATION拥有，RDT运行时单元分别拥有行为/设计/实际观察。真实Git拓扑、旧owner事务与公共新入口、目标own验证及#766原操作恢复须分别成立；源码通过不代表现场恢复或完整Release矩阵。先独立Architecture与candidate Check，再原final_integration/readback、最终Check和committed Review。
