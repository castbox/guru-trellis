# #669 Traceability 与替代范围

| 整体验收 | Requirement → Design | 验证 |
| --- | --- | --- |
| AC1 | R669-01/02/06 → D669-01/03 | T669-01/06 |
| AC2 | R669-03 → D669-02/03 | T669-02/06 |
| AC3 | R669-04 → D669-03 | T669-03/06 |
| AC4 | R669-05 → D669-01/02/03 | T669-02/04 |
| AC5 | R669-07 → D669-04 | T669-05/06 |

完整拟写在 manifest 所列三层目标对应的 `proposed/docs/`。当前完整前驱是 B 中同 locator；本次只新增已有实现恢复能力，不退休现有 clean-base 入口或改写原 schema。原稳定身份、条件、否定、历史与跨文档关系保持。

当前 RDT status=promoted，三层完整 current 与本次已审拟写一致。原独立 Architecture 和 candidate Check 已覆盖完整代码与隔离拟写；RDT owner 在 final_integration 实际写入并回读。Architecture 由原 owner 独立完成其整合，随后重绑完整 after；最终 Check/Review 和交付事实由其正式结果拥有，不要求正文递归回填自己的最终 pass。
