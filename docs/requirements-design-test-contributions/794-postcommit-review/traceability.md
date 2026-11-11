# #794 关系、完整 targets 与整合边界

固定前驱为 Git `4d565c97b5abf634d76ede2d18eed0a57f13bb76` 的六个同路径完整单元。proposed targets中的相对引用按拟晋升 current位置解析，不在贡献目录登记第二 current。原 RDT-REQ/DES/TST-LIFECYCLE 与 RDT-REQ/DES/TST-KNOWLEDGE身份保持。

| 原要求/本批行为 | 完整设计责任 | 验证关系 |
| --- | --- | --- |
| Task R1/R7；R331-04、R600、R638、R711-04 | D331-04、D638-02/03、D711-03/04；原writer、targets、expected-current/readback、TaskCommit与固定after | T638-01..04、T711；D1 V1/V5/V7 |
| Task R2/R3/R7；R710-01/02/05/06 | D710-01/02/05/06；真实语义authoring、单次九维/Architecture/full_review及真实双槽 | T710-01/02/06/07/09；D1 V1/V5/V6 |
| Task R4/R5；R578、R648/R693 | D638/D648/D693；固定B、原覆盖与实际差额/冲突/consumer影响 | T638/T648/T693；D1 V3/V6 |
| Task R6/R7；R710-03/04/07、R711-08 | D710-03/04/07、D711-05；旧provider/准确结果恢复与matching采用 | T710-03/04/05/08、T711-05；D1 V2/V4/V7 |

生命周期新增R794-01..07 / BEH794与D794-01..05 / CON794由T794-01..07（对应D1 V1–V7）逐项承接，完整定义由对应单元拥有；本表只定位跨知识的真实必要关系。原#710/#711等专项次数及历史结果保留，不复制为本批验收或当前pass。

原RDT owner先读本贡献和六个实际targets，语义整合全部仍有效条件和必要R/D/T/Architecture关系，沿本Task当前适用provider合法写入/readback；本文不记录晋升或授权。无shared root/current README、全局版本或ADR index逐项登记。Architecture目标集由其原owner分别整合。
