# #396 设计增量

| Responsibility | 唯一 owner / locator |
| --- | --- |
| D396-01 最小输入 | [readiness package contract](../../../trellis/skills/guru-team/packages/guru-review-change-request/references/contract.md)的 Producer-Bound Draft Recipe；SKILL 仅导航，既有 JSON 示例共享同一 source identity。 |
| D396-02 receipt 与恢复 | 同一 package contract；原 recorder 派生、checker identity/freshness 和 invoke 正式出口维持原语义。 |
| D396-03 客观 replay | [stage0_fixtures.py](../../../trellis/skills/guru-team/adapters/eval/stage0_fixtures.py)的原 producer 链和 [test_stage0_fixtures.py](../../../trellis/skills/guru-team/adapters/eval/test_stage0_fixtures.py)。 |
| D396-04 native continuation | 原 [formal_exit_boundary.py](../../../trellis/skills/guru-team/adapters/eval/formal_exit_boundary.py)扩展事实输入；AI 另行阅读 transcript，不用脚本分数替代判断。 |
| D396-05 分发 | 原 preset 安装、reapply、ownership/drift 和 selected-platform 投影。 |

Architecture 继承 current .82/active；Planning owner 判定 no_architecture_impact/no_change，Phase2 仍须对最终候选重新评估。无新 Skill/API/store/schema/DTO/approval chain，未放宽 runtime 校验。完整实现细节仍由以上 owners 持有；[唯一结果](test.md)拥有验证与限制。
