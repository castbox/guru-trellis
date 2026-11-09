# #769 tools冻结源恢复：Architecture贡献

状态proposed，Task `769-tools-peer-growth-recovery` generation 0，Delivery `638e1a19-c4cc-46da-8157-e19293774730`。固定before `a5f3ceeabbaccddae65935d97763f5a798f71ca9`；authority为guru-trellis-architecture / guru-trellis-design-constitution-v1 / guru-trellis-architecture-change-contract-v1。独立candidate_assessment为architecture_impact/target_native。完整方案由本Delivery design.md单写。

## 完整目标与职责

完整proposed目标为本目录proposed/docs/architecture/01-current/runtime-location.md和proposed/docs/architecture/adr/tools-frozen-source-recovery.md，分别对应原current完整单元与新ADR。原环境、来源、位置配置和迁移条件全部保留；新差额是peer增长及修复executor/原资产源分离。shared README、ownership、ADR index没有自身变更，不登记新主题。Author写隔离贡献；原Architecture owner独占final_integration晋升。

## 九concerns

| Concern | 判定与依据 |
| --- | --- |
| authority-binding | applicable：绑定上述固定before和当前阶段authority；当前候选不伪装为current。 |
| constitution-binding | applicable：AI/事实分层、单owner、最小状态与公共兼容；完整constitution由原reviewer独立读取。 |
| boundary-and-decision | applicable：ADR-027、ARCH-RUNTIME-LOCATION和新ADR；一个兼容profile薄复用原engine。 |
| owner-and-single-writer | applicable：tools原owner执行，AI判断，资产仍归原source；shared晋升只由原maintenance。 |
| compatibility-and-exit | applicable：schema1.0真实旧事务含#766；终态及原保留责任结束后明确迁移删除，无双写。 |
| gap-and-deviation | applicable：不新增或恶化GAP，不恢复已退出的第二authority；旧peer比较缺陷由本Issue闭环。 |
| parallel-scope | applicable：只写本Task隔离贡献和本包；不写其它Task/peer或共享主题登记。 |
| evidence-and-freshness | applicable：区分固定before、实际candidate、目标own验证及#766真实恢复；当前无实现pass。 |
| review-and-promotion | applicable：先独立final_plan/phase2及完整candidate Check，再原owner目标重读/写回/readback和最终质量链。 |

## 代价与观察截止

仅原保持检查、新公开profile/retry consumer和显式兼容合同；无新checkpoint字段、迁移平台或拓扑台账。完整proposed尚未晋升，实际实现/安装/现场恢复尚未验证。Task完成和Release不由本文建立。
