# #811 追踪与替代

| Requirement | Design | Test |
| --- | --- | --- |
| REQ-811-01/02 | DES-811-01/02/03 | TST-811-01/03/05 |
| REQ-811-03/04 | DES-811-02/03/04 | TST-811-02/03 |
| REQ-811-05/06 | DES-811-01/05/06 | TST-811-03/04/06/07 |

稳定单元identity保留；DES-812-03仅在两种scope_confirmation_required的最小对象上由DES-811-01窄替代。
原R692/D692/T692只补确认target与authority的关系，不改变其他诊断、原始证据或当时结果。
manifest定位完整六个proposed targets，原maintenance promotion直接消费它们；不登记shared root/index。当前REQ-811-06/TST-811-05按最新live #811采用独立正常Task/Delivery接续，不再承接特定发布Task、版本或时间依赖；既有有效工程事实和历史观察保其证据边界。

原 RDT owner 已核六目标与固定 before 一致后整合完整定义并逐项读回。状态为 integrated_pending_review；独立 committed Review 仍待执行，保留上述 proposed 正文作为完整来源。
