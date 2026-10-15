# #566 Design 增量

本贡献记录责任与接口；逐步执行由 canonical Skill references 独占。公共算法仅调用匹配 Trellis CLI/Core maintenance API，不引入 Guru converter、第二生命周期或旧数据普通 dual-read。

| Identity | 唯一责任与边界 |
| --- | --- |
| D566-01 / CON566-01 | `guru-upgrade-tools` 持有单目标安装语义及 Guru 资产编排；原 Sync 只读选择事实复用，原 Sync 的 clean/fetch/ff不改义。目标选择先分支后checkout；冲突不降级候选。 |
| D566-02 / CON566-02 | 原 managed Python owner 为 tools-only 提供 checkout-local ignored pointer，primary/linked相同隔离；resolver先读本地override再原gitdir/common。已有override时后续activation更新同一effective路径，原fullupgrade备份恢复该独立路径；没有override时保留原默认activation，peer实际runtime不变。 |
| D566-03 / CON566-03 | `guru-maintain-legacy-task` 拥有显式所选 Task 的 convert/history_closeout/resume/rollback semantic闭环；公共maintenance执行公共模型、五份planning映射、固定operation、raw保存与公共carrier退役。 |
| D566-04 / CON566-04 | 原 Merge只读核实历史PR/head/merge/target/归属；Publish/Merge/Finish及旧inventory命中的其他原gate owner在独立legacy retirement入口处理各自控制。prepare核实准确归属并保存固定preimages；public preserved source可读后按Publish→Merge→Finish→其他所选owner执行，不依赖移除的active tree。未决外部事实保留note。 |
| D566-05 / CON566-05 | 转换后重新进入当前branch/checkout/session及下一实际owner；历史-only验证旧正常context不再选中。Reconcile仍独占业务差异判断，Completion仍独占业务完成判断。 |
| D566-06 / CON566-06 | tools和Task各有独立recovery_ref；原Guru私有checkpoint仅保留恢复不可重建输入/preimages与公共operation refs。兼容性检查在任何单侧工具恢复前完成；无授权字段、全仓hash包、全局事务或锁。 |

接口切换见 canonical `MIGRATION-566.md`，具体新profiles由各package Interface与消费合同定义。source_locked原锁不因本地#40候选而改变。所有安装能力结论以本贡献唯一 [Test](./test.md) 实际分层结果为准。
