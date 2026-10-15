# #566 Requirements 增量

来源为 [Issue #566](https://github.com/castbox/guru-trellis/issues/566)，配对公共能力归 [Trellis #40](https://github.com/castbox/Trellis/issues/40)。本贡献承接 RDT `.96/active`，尚未晋升；既有完整 Plan2 与普通 current-only 合同保留。

| Identity | 当前行为承诺 |
| --- | --- |
| R566-01 / BEH566-01 | 工具升级只更新显式 checkout；省略目标时沿既有显式 base/config、有序 dev/develop/main/master、remote default 选定分支后才绑定唯一 checkout。不创建或切换分支/worktree，不因目标缺失降级。 |
| R566-02 / BEH566-02 | 工具、所选任务转换、仅历史收尾是独立操作。完整匹配来源加载维护入口；旧目标 parser/Identity/Continuation/Reconcile 不成为启动依赖。工具升级保留旧 Task、规划、归档、业务控制与 peer bytes/modes/runtime。 |
| R566-03 / BEH566-03 | AI 判断历史事实和未完成义务；公共 Task2、Delivery、session/binding、转换与恢复归 Trellis。Guru 原 owners 核实交付事实并处理准确归属的私有控制，旧 gate 不产生当前 pass。 |
| R566-04 / BEH566-04 | 继续执行需目标自身 native continuation 与下一实际 owner验证；已交付待验收进入 evidence_pending，不凭空创建 Delivery。仅历史保留先写入并读回 raw archive/note，再退役所选 carriers；不制造 Completion/Closure/Finish，不要求升级旧目标工具。 |
| R566-05 / BEH566-05 | 固定 operation/result/preimages，普通失败与结果丢失沿同次恢复，保留后续业务工作。工具回退先核对公共数据兼容性，再恢复 Guru 半边；不兼容写前阻塞，不扩大原备份。 |
| R566-06 / BEH566-06 | 使用真实来源身份和目标安装/native/reapply证据；版本号、暂存检查和公共 fixture 不代替 Guru 联合验证。local_candidate 仅隔离开发，source_locked 缺API时写前阻塞；业务安装、正式来源更新、发布与完整 Release矩阵独立。 |

每项设计和验证承接只由 [traceability.md](./traceability.md)引用，不在各层重复步骤。原业务 CMS 历史仅为来源情境，不是本任务业务写入范围。
