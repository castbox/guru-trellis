# 固定候选与实际整合

| ID | 机制与责任 |
| --- | --- |
| DES567-01 | 原Author/实施owner选B；DeliveryProjection.content_base仅计算既有事实，恢复本Delivery候选优先，否则从真实前序delivery_result选HEAD祖先链唯一最大head；首轮用明确开发基线或一次观察目标的唯一merge-base。candidate固定OID并补全B..H路径。 |
| DES567-02 | workflow移除默认pair guard边；guard命令、schema和无消费者状态退出。各stage直接进入原consumer，不新增同义协调gate。 |
| DES567-03 | 原semantic owner选择阶段适用authority；digest/ref只做局部事实一致性。真实适用改变路由原owner；promotion写前expected-current单独保留。 |
| DES567-04 | Reconcile使用固定target OID，与内容B分离。原executor保留普通/resolved提交、精确树/parents/message及同操作恢复；新target前进不改变操作。 |
| DES567-05 | 实际实现/整合推进H时，原stage rework只清readiness，旧Check/full_review保留历史；begin_check绑定B..Hi使旧gate不适用。原Check与Review实际判断 prior evidence＋delta/依赖，记录当前结果和新predecessor。continuity本身不是full_review。 |
| DES567-06 | Merge绑定expected任务HEAD、目标branch与实际GitHub资格；旧target SHA不锁实际第一parent。Finish保留精确bookkeeping事务，用终态可达性恢复。私有schema转换与旧请求重新准备由MIGRATION-567单写。 |
| DES567-07 | Completion读取当前Task/generation与全部scope，仅补缺失Delivery事实和受影响结论；不实现历史查询。source+installed受控dogfood承担安装/reapply/drift证据，开发Task继续旧graph。 |

CON567-01：Markdown/Skill拥有scope、适用性、充分性、finding、route和真实审查；脚本不据base前进作语义裁决。公共Task/Delivery身份、真实内容、PR与同操作一致性保持。所有字段只服务实际consumer，无新长期账本。实现入口见traceability；迁移唯一合同为preset/MIGRATION-567.md。
