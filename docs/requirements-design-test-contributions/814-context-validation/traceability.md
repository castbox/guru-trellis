# #814 context 采用追踪

| Requirement / Behavior | Design / Contract | Test / Scenario |
| --- | --- | --- |
| R814-01 / BEH814-CONTEXT | D814-01 / CON814-FACTS | T814-01 / S814-SCALE；T814-02 / S814-REJECT |
| R814-02 / BEH814-PROBES | D814-02 / CON814-ADOPTION | T814-03 / S814-PROBES；T814-04 / S814-DISTRIBUTE |
| 原R718-03/11、R769 | 原D718-03/06/07、D769；D814-02 | T814-02/03/04 |

目标仍为三个既有 runtime-location 完整单元，其稳定身份 RDT-REQ-RUNTIME-LOCATION、RDT-DES-RUNTIME-LOCATION、RDT-TST-RUNTIME-LOCATION不变。Requirements/Design/Test差额各自拥有一个完整新增章节；manifest定位同一固定before及这些唯一新增正文。完整after为固定before原文加对应章节，原R718/R760/R769/#813定义和所有历史观察均保留。

直接consumer：原RDT owner以本表检查必要跨层关系并整合；独立committed Review核完整before/after；Task Completion消费仍适用的真实工程及后续正式结果。本贡献没有删除/替换/拆分/迁移；不改共享README/index/全局版本，不建立第二current。整合后贡献仅保留为来源，日常读取以各current完整单元为准。
