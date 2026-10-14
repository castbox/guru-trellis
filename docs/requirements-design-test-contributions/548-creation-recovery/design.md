# #548 设计责任

| Responsibility | 唯一落点 |
| --- | --- |
| D548-01 | 原DeliveryProjection：明确key且官方resolver无key的call-local读取；有key只读官方session与原冲突合同 |
| D548-02 | 原Creation runtime及退休端口：同operation/UUID恢复，Author成功消费后由producer清理无keypending |
| D548-03 | Author/Wording/Architecture/Approval/Activation：原key输入到projection，原phase/scope门禁；qualification保持原明确paths |
| D548-04 | 原Upgrade owner/public Plan2：真实旧writer记录、完整inventory、逐记录defer及保留；没有HEAD identity不制造pass |
| D548-05 | 原canonical preset/platform projections及定向验证；主完整legacy与成套current样本分开 |

详细步骤由各canonical Skill独占。没有新public DTO、writer、selection store、兼容reader或恢复框架。来源设计处置只在Task design矩阵；Architecture before/after在[专属贡献](../../../.trellis/tasks/10-14-548-creation-recovery/architecture-contribution.md)，本文件只拥有RDT职责映射。
