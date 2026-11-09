# #761 跨仓 DAG 追踪

状态：proposed，未晋升。适用基线与目标见 manifest；完整 resulting definitions 为 requirements.md、design.md、test.md。不修改共享根/current导航，不生成额外全局版本。

| 来源/行为 | 设计责任 | 验证 |
| --- | --- | --- |
| Issue #761 行为1、兼容验收 → R761-01 | D761-01 | T761-01/05 |
| 行为2 → R761-02 | D761-01 | T761-02 |
| 行为3/4、跨仓验收 → R761-03 | D761-02 | T761-01/04/05 |
| 行为5、环境验收 → R761-04 | D761-03 | T761-03/04 |
| 原R731-01..06（全部保留） | 原D731-01..05 | 原T731-01..07 |

Architecture沿用 guru-trellis-architecture 的现有AI/Markdown控制面与确定性工具边界。最终实现及proposed内容仍由原独立Architecture与候选Check审查，无impact时不制造贡献/ADR。原RDT owner仅在candidate_checked后final_integration重读真实current、整合并回读，再由implementation重绑候选进入最终质量链。真实行为结果由原测试轨迹和Task/PR提供；本文件不复制审查历史或预填通过。
