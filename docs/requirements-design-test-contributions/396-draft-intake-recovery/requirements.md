# #396 需求增量

来源：[live #396](https://github.com/castbox/guru-trellis/issues/396)，合同 2026-10-10-r1；来源状态确认于本轮。增量属于 current .82 的 draft authoring/recovery 使用合同，不重新认领已有 runtime normalization/derivation。当前贡献已由 owner 审查晋升至 .83 knowledge authority；后续完整 gates 独立执行。

| Requirement / behavior | 增量责任 |
| --- | --- |
| R396-01 / BEH396-CHAIN | 实际 producer 公共输出经 Readiness record/check/invoke 到正式 ready。 |
| R396-02 / BEH396-IDENTITY | 同一草案直接消费原 producer locator，恢复不改 producer。 |
| R396-03 / BEH396-AUTHOR | 最小 authoring、完整 authority digest 和实际 receipt 替换。 |
| R396-04 / BEH396-MISTAKES | 区分五类正常误操作及允许忽略的 extras。 |
| R396-05 / BEH396-RECOVER | 错误身份/摘要拒绝；同范围重建 consumer 后可继续。 |
| R396-06 / BEH396-REFRESH | 正文变化真实刷新；缺前序如实停止或重入。 |
| R396-07 / BEH396-AGENT | 真实 Agent 独立 review 和无重复确认恢复。 |
| R396-08 / BEH396-DISTRIBUTE | canonical/dogfood/installed 与平台投影一致。 |
| R396-09 / BEH396-CAUSE | 历史错误、既有能力和剩余指导缺口分别归因。 |
| R396-10 / BEH396-CLOSE | 生命周期由原 owners 以真实结果闭环。 |

完整步骤合同由 [canonical readiness contract](../../../trellis/skills/guru-team/packages/guru-review-change-request/references/contract.md)拥有；[traceability](traceability.md)只承接 identity。结果只在 [test.md](test.md)；runtime 改动仅允许先复现独立合法缺陷，本候选无此改动。
