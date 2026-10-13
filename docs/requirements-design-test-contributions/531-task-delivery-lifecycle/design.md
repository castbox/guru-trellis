# #531 设计责任增量

状态：reviewed_promoted，RDT .90继承immutable .89，Architecture .87；以下历史准入与candidate说明保持原身份。
公共模型和转换引用上游固定 candidate 的 delivery-contract；Guru 不复制 schema。

| Responsibility | 唯一 owner 与边界 |
| --- | --- |
| D531-01 | 上游公共 Task/Delivery authority；Guru `runtime/delivery_projection` 仅执行闭合公共 API 与最小 projection |
| D531-02 | `guru-create-delivery` 创建/select及同 owner 恢复；原唯一 Author 写 per-Delivery docs；Wording/Architecture/Approval 独立；`guru-activate-delivery` 唯一公共 Planning writer |
| D531-03 | Clarify/当前阶段 owner 判断范围修订、earliest-owner rework 和停止；公共接口执行，continuation只读路由 |
| D531-04 | Check、TaskCommit、Branch Review 各保留原 semantic owner；candidate事实与gate适用性分离，clean不新增commit |
| D531-05 | Review/Publish/Merge 保留中文 Refs-only、expected-head/CI/trailers和私有事务；真实结果经公共事实接口投影 |
| D531-06 | Completion判断整个scope；Closure处置来源，Finish归档，Cleanup精确资源；Reactivate公共新generation保留历史 |
| D531-07 | 上游D2拥有公共迁移；Guru upgrade/installer及原私有事务owner拥有自身迁移与安装诊断；单安装无双writer |
| D531-08 | global workflow/registry独占调用和consumer；平台入口只加载/路由；正式支持边界见 MIGRATION-531 |

具体阶段步骤只由相应 canonical Skill 定义。版本化 input/output 是各自独立合同，
相邻输出不传完整 aggregate、checkpoint、review历史或授权。设计在固定 API 下实施，
上游公共迁移已完成仍不代表Guru匹配私有迁移/联合证据或原业务切换通过。

最终绑定见manifest及managed task-delivery-migration合同。fresh templates、完整session拓扑、archived两factsprospective转换、tracked安装增量独立Git处置分别由原owner消费；既有业务提交不重复，future规划路径不预提交，五blob桥接仅服务TaskCommit。安装新HEAD freshCheck之后首次完整Review，不能由路径映射制造clean。

上游产品1e400140、当前mixed CLI5aeeb/Core45bb承接worktree副本公共合法处置；185e是前驱，不作为当前mixed安装绑定。
Upgrade 只盘点和透传原 branch_bindings raw snapshot、全部 eligible roots 与
common/local sessions；公共 executor 独占组判定和唯一 active authority。合法 defer
peer 的 Task/五规划/modes 与 binding 保持，不新增 Guru 私有迁移资产。旧候选
模板/checkpoint 在原来源恢复，来源或拓扑变化 fresh prepare；不重冻 rollback anchors。


## 当前局部差额（2026-10-14）

迁移当前绑定task design §17 mixed候选及§17.2；Plan2 artifact内容写入由上游拥有，Guru原TaskCommit只在私有来源关联中显式选择markdown_relative_links_v1。具体唯一合同见canonical guru-create-task-commit/references/contract.md的Explicit Markdown link projection compatibility；Planning只读正常新文档，不消费private bridge。无模式保持原bytes/modes，direct HEAD永远严格，真实改动仍dirty。当前installer managed spec闭合修复承接既有canonical bootstrap spec，不扩运行模型。历史候选/失败保持各自身份。

D531-08 的 native bundled参考仍归上游；当前Guru route优先级由原workflow-contract明确，禁止preset覆盖bundled参考。D531-01的Architecture回程区分同DeliveryKey/root的delivery_task_impact_sync与Task-only task_impact_sync；对应maintenance由原owner处理后重新评估，不改result标签。
