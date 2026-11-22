# #850 追踪与替代边界

来源为[Issue #850](https://github.com/castbox/guru-trellis/issues/850)和D1已批准PRD/design/implement，固定before=a72981db56d2070d8140b468cab3a97ae82effd3。原RDT owner维护本差额，Architecture继承docs/architecture/README.md / guru-trellis-architecture / active；它不拥有或复制Architecture正文。

| Task要求/验收 | 需求/行为 | 设计/合同 | 测试/场景 | 完整current目标 |
| --- | --- | --- | --- | --- |
| R01/R02；AC01/02/03 | R850-01/BEH850-CONTENT，保R153/R818有效责任 | D850-01/CON850-CONTENT、D153-02 | T850-01/SC850-CONTENT | 三层current/issue-content.md |
| R01/R03；AC01/03/04 | R850-02/BEH850-LOCAL，R819-02/03/04 | D850-02/CON850-LOCAL、D819-02/03 | T850-02/SC850-LOCAL、T819-03 | 三层current/local-fix-intake.md |
| R01/R02/R03；AC01/02/04 | R850-03/BEH850-PLANNING，R657/R679存续条件 | D850-03/CON850-PLANNING、D531/D679 | T850-03/SC850-PLANNING、T531-02 | 三层current/task-delivery-lifecycle.md |
| R04；AC04/05 | R850-04/BEH850-ADOPTION | D850-04/CON850-ADOPTION | T850-04/SC850-ADOPTION | 三层current/issue-content.md及上述必要关系 |

requirements.md/design.md/test.md给出已整合并读回的完整变更章节或稳定单元，九份current已写入，原同文件其余定义保持。R153/D153/T153、R818/D818/T818、R819/D819/T819、R657/D657/T657及R679/D679/T679身份和历史来源可继续检索；只窄替代其当前独立Wording/scan/receipt前置与直接consumer，不改原历史命令、失败、结果或观察截止。固定before同locator可恢复前驱完整语义，不保当前双reader。

新增R850/D850/T850只承接本次职责、入口、回程、内容修订和迁移。MIGRATION-850拥有精确版本表及旧provider退出；完整知识不要求普通读者拼接本贡献。无根/current索引、全局版本、其它Task贡献或共享journal写入。实际整合逐份readback后仅integrated_pending_review，TaskCommit和独立committed Review尚未发生。
