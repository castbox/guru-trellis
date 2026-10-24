# 来源、完整目标与替代追踪

固定 B=`e9583202b67750d7b3ec2b7eab4b037c0c52a226`；稳定RDT authority为guru-trellis-rdt。proposed/镜像提供三份完整目标，相对链接按最终目标解释；原promotion owner才写共享current。既有所有有效条件、身份和历史保留，不要求重放旧贡献拼接当前定义。

| Requirement / behavior | Design / contract | Test / scenario | 来源与完整目标 |
| --- | --- | --- | --- |
| R663-01 / BEH663-REPAIR | D663-01 / CON663-REPAIR | T663-01/06 | #663 F1/V1–V3；三层task-delivery-lifecycle完整单元 |
| R663-02 / BEH663-ARCHIVE | D663-02 / CON663-ARCHIVE | T663-02 | #663 F2/V6；正式example与原只读owner |
| R663-03 / BEH663-BEFORE | D663-03 / CON663-BEFORE | T663-03 | #663 F3/V7；固定B真实缺失、完整H及独立审核 |
| R663-04 / BEH663-MAINTENANCE | D663-04 / CON663-MAINTENANCE | T663-04 | #663 F4/V8；原promotion维护回程及repair对照 |
| R663-05 / BEH663-DISTRIBUTION | D663-05 / CON663-DISTRIBUTION | T663-05/06 | #663 V4–V5；当前全图实际组合及matching完整分发 |

Architecture命中change-contract的当前before比较条款和必要ADR-CONTRACT-CONTINUITY；不改变九concern、原descriptor/result、single-writer或无关GAP。未命中的knowledge-maintenance、completion-closure、native-compatibility及其导航/历史不修改。公共细粒度合同仍由canonical packages拥有；本贡献不成为第二schema或runtime状态。

普通Task旧适用源的读取、历史追溯与真实新能力采用边界保留。无公共状态机或长期adapter，旧失配输入从原owner fresh构造；不回填旧归档、固定版本或他方贡献。原生与受控证据不能互相替代，实际结果由本目录test.md拥有。
