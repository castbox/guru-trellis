# #717 来源与追踪

状态：proposed。固定 source：404c841e9ca917b4680831aa0becd2e26d72fa0c。Direct Source：[Issue #717](https://github.com/castbox/guru-trellis/issues/717)；完整整体范围由 Task 根 PRD 拥有，本批 full D1 覆盖 AC1–AC5。manifest 定位完整拟写与必要导航，不复制未变 authority。

| Requirement / behavior | Design responsibility / contract | Test strategy / scenario | AC |
| --- | --- | --- | --- |
| R717-01 / BEH717-OWNER | D717-01 / CON717-COMMON | T717-01 / SC717-RULES | AC1/AC2 |
| R717-02 / BEH717-BOUNDARY | D717-02 / CON717-PROVIDER | T717-01/03 / SC717-RULES/DISTRIBUTE | AC2/AC5 |
| R717-03 / BEH717-ADOPTION | D717-03/04 / CON717-OBSERVE/DISTRIBUTE | T717-02/03 / SC717-NATIVE/DISTRIBUTE | AC3/AC4/AC5 |

共同规则详细行为唯一读 managed review-sufficiency spec；检索、测试价值、因果、完整知识和专业标准的原 owner 不变。原阶段职责由其各自 current contract 拥有。任务规划中的固定消费者和逐条迁移表不扩成长期台账。历史版本及其它当前单元保持原义。
