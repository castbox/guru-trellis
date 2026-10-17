# #600 需求增量

provenance=source_confirmed。唯一变更来源为 [#600](https://github.com/castbox/guru-trellis/issues/600) §2–7。RDT 比较起点为 `.103`，Architecture 为 `.95`；这两个身份只定位变更前 authority，不构成新行为已接受或实现完成的证明。

| Requirement / Behavior | 来源 | 增量责任 | Design | Test |
| --- | --- | --- | --- | --- |
| R600-01 / BEH600-01 | AC1 | 完整候选的独立 Architecture 评估、分支晋升先于最终 Check；committed 判断及完整 Review 保留 | D600-01 | T600-01 |
| R600-02 / BEH600-02 | AC2 | 晋升前 authority 与实际候选前后比较，不能以新 CURRENT 自证 | D600-01/02 | T600-02 |
| R600-03 / BEH600-03 | AC3 | 一致写入正常前进；变化、expected-current mismatch 和可恢复 partial/output-loss 分别由原 owner 承接 | D600-02 | T600-03 |
| R600-04 / BEH600-04 | AC4 | no-change 无额外贡献/ADR/阶段；多个 Delivery 独立闭环 | D600-01 | T600-04 |
| R600-05 / BEH600-05 | AC5 | finding 修复按真实影响回程；窄引用/状态对齐取得覆盖最终候选的正式结果 | D600-02/03 | T600-05 |
| R600-06 / BEH600-06 | AC6 | 来源可定位，状态准确；不为补最终 Review/SHA 循环写正文 | D600-01/04 | T600-06 |
| R600-07 / BEH600-07 | AC7 | 三类在途 Delivery 成套迁移、真实独立性与 finding lifecycle 保持 | D600-04 | T600-07 |
| R600-08 / BEH600-08 | AC8 | canonical/installed/platform/reapply/drift 一致，实际 AI 行为证据与机械证据分开 | D600-04 | T600-08 |

业务仓代码、生产环境、完整累计 Release/Upgrade 矩阵、通用增量审查平台、新审批链或审查账本不进入本增量。
