# #453 Requirements contribution

状态：reviewed_promoted；按 expected `.81` 晋升 `.82`，原 `.81` 为不可变 source/preimage。来源为 [live Issue #453](https://github.com/castbox/guru-trellis/issues/453) 的 `2026-10-10-r1`；完整目标、正式出口语义与验收由该源拥有。当前 Requirements 为 `.82/active`，薄继承不可变 `.81`。以下只定义稳定 trace identity 与源定位，不复制源正文。

| Identity | 源合同定位 / behavior |
| --- | --- |
| R453-01 | 预期范围：live semantic package inventory / BEH453-CLASSIFY |
| R453-02 | 目标 1、3：中间成功与正式出口边界 / BEH453-RECEIPT |
| R453-03 | Skill 类型：semantic/deterministic profile 保留 / BEH453-PROFILE |
| R453-04 | Skill 类型与正式出口语义：实际正向/非通过出口 consumer / BEH453-ROUTE |
| R453-05 | 目标 4、旧安装验收：controlled caller 与完整安装直接迁移 / BEH453-MIGRATE |
| R453-06 | 目标 5：canonical/preset/dogfood/platform 一致 / BEH453-DISTRIBUTE |
| R453-07 | 两个正常 Agent 回归：真实中间输出阶段声明 / BEH453-REPORT |
| R453-08 | 行为验收：合法接续与实际 consumer/stop / BEH453-CONTINUE |

前驱的 public Skill DTO、exit id、unique consumer、内部 owner/checkpoint 与 atomic/recovery 能力保持原身份；本次替换只针对 commands metadata 和 intermediate CLI transport。版本 1.0 commands schema 留作历史，不是当前运行路径。
