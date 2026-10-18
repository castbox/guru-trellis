# #154 规划正文需求增量

provenance=`source_confirmed`。唯一来源为 [Issue #154](https://github.com/castbox/guru-trellis/issues/154) 当前 R1–R7、V1–V7、AC1–AC10；本增量继承 RDT107 与 Architecture98。完整写作规则归 canonical Author package，本文只定位需求责任和追踪，不复制规则正文。

| Requirement / Behavior | 来源 | 增量责任 | Design | Test |
| --- | --- | --- | --- | --- |
| R154-01 / BEH154-01 | R1/R2、AC1/AC2 | 四类正文的章节、字段、适用条件、深度、裁剪及对应写作入口显式加载 | D154-01 / CON154-01 | T154-01/02 |
| R154-02 / BEH154-02 | R3/R4、AC3/AC4/AC5 | 按来源充分性调查与澄清，保留详细承诺、来源角色与唯一来源设计处置 | D154-01/02 / CON154-01/02 | T154-02/03 |
| R154-03 / BEH154-03 | R5、AC6/AC7 | 全量、部分、后续和返工 Delivery 的本批正文、前序事实、差额、剩余责任与 Completion 关系 | D154-01/02 / CON154-01/02 | T154-03/04 |
| R154-04 / BEH154-04 | R6、AC9 | 复用唯一清晰写作规范，原 owners 自检/审核，保持准确语义和义务强度 | D154-01/02 / CON154-01/02 | T154-02/03 |
| R154-05 / BEH154-05 | R7、AC1/AC7/AC8 | 原 Author 单写、完整过程示例、下游实际读取及原 owner 修订；保留身份、Policy、Docs Plan 与阶段接受边界 | D154-02 / CON154-02 | T154-02/03/04 |
| R154-06 / BEH154-06 | R7、§4.2、AC10 | canonical/dogfood/installed/声明平台定向验证和完整匹配采用，保留用户内容、reapply 与 sidecar 处理 | D154-03 / CON154-03 | T154-01/05 |

历史案例不并入本次功能验收。真实 Agent、确定性检查和安装结果分开；完整多平台升级/Release、业务自动升级、历史归档重写和新语言标准不在范围内。模板填充不晋升共享导航或创建空贡献；长期 RDT/Architecture 仍由原 owners 维护。
