# 固定开发基线

来源：castbox/guru-trellis #567。本增量已按 expected RDT `.97` 晋升至 `.98`，继承 Architecture `.92/active` 与 ADR-028；默认追赶相关旧片段按本增量替代，其余有效合同继续继承。

| ID | 行为 |
| --- | --- |
| BEH567-01 | 开发基线、Delivery完整内容范围与PR target分离；D2消费真实前序Delivery结果，恢复原候选，不自动同步或重复D1。 |
| BEH567-02 | Planning、Activation、Check、Commit、Review、Publication、Completion/Finish默认零Reconcile；behind、远端SHA和无关整体版本前进不成为资格条件。 |
| BEH567-03 | 在途阶段固定候选和明确适用authority；真实scope、依赖、方案或立即适用规则变化由原owner处理。 |
| BEH567-04 | 实际冲突、必需检查具体集成失败、原Merge观察的既有服务器更新要求、明确依赖或主动同步才触发整合；固定一次目标，不追赶。 |
| BEH567-05 | 保留普通/resolved/committed/continuity/同操作恢复；原owner审必要差额和依赖，不重放无关门禁、不伪造结果或制造空提交。 |
| BEH567-06 | Completion核验全部scope与真实交付。历史截点只证明其覆盖，新增相关事实补缺；#569独占查询准备，不互设前置。 |
| BEH567-07 | canonical、匹配installed与声明平台投影一致；正常在途API变化有明确迁移，保留旧开发安装边界，不扩完整Release矩阵。 |
