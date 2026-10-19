# #637 候选适用性需求增量

状态：proposed；来源为 [Issue #637](https://github.com/castbox/guru-trellis/issues/637)八项行为及全部证据边界。比较起点为manifest中的RDT .113/Architecture .104和固定Git B。本文只拥有本Task差额，原完整定义仍由current生命周期单元拥有，后续由原owner晋升完整定义。

- R637-01 / BEH637-01：首次候选完整独立审核；后继以真实原覆盖、全部差额和受影响依赖形成精确当前完整结论，明确保留/失效/补充，不复制旧pass。
- R637-02 / BEH637-02：工程事实、当前语义判断和Git/PR事实分开。同树仅换内容绑定；无关target前进不整合或失效业务门禁；真实冲突审双方、组合和未改consumer。
- R637-03 / BEH637-03：原命令定义/版本、输入/依赖、环境、工具链、参数和期望适用且结果可核验时采用；变化/未知/缺失执行命中检查。文档改变行为同样纳入影响。
- R637-04 / BEH637-04：独立性由实际未参与当前实现的职责决定；同合规reviewer可先Architecture后Branch Review，各阶段仍亲自判断/正式产生当前结果，不重建无新事实的理解。
- R637-05 / BEH637-05：finding/整合后核闭合、修订和受影响覆盖，不无条件换新reviewer重做相同全量；原覆盖不足补审，组合影响不明完整审核。
- R637-06 / BEH637-06：Delivery Review、Publication、Merge各核当前payload/Issue/candidate/live事实，消费仍适用内容结论，不重做无变化的业务设计评审。
- R637-07 / BEH637-07：审核中base前进不换固定B/H；真实scope/前提/依赖变化回最早owner。同Delivery恢复，不造空提交、新身份或证明账本。
- R637-08 / BEH637-08：规则由原共享workflow合同单写，七owner显式读取；matching迁移窄替代旧冲突。公共结构保持，无第二reader、hash链、私有跨读或持久化授权。

合法覆盖来源为public Task/Delivery结果、真实原公开调用对象、精确Git和当前正文；原始命令结果单独核验。首次implementation_required没有passed full_review，refs只定位，已建立理解不替代覆盖；缺依据补审。退休checkpoint不重建、不跨owner读，不新增长期review/test账本。#636实际接口组合由本项承担，#638未来接口明确未验证交后项。Task Completion、Closure和Release保持独立。
