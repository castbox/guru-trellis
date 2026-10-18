# 候选证据与最终验收边界

版本：`current-main-0.6.17-guru.72`；状态：`active`；predecessor：`current-main-0.6.17-guru.71`。完整继承[不可变前驱合同](../current-main-0.6.17-guru.71/test-plan.md)；除下文明确修订的独立迁移边界外，既有 requirement/design/test、无人员模型、source disposition、owner、历史拒绝边界、NFR 与 trace 继续有效。前驱 source、计数和证据只表示历史快照。Architecture：`docs/architecture/README.md` / `current-main-0.6.17-guru.72` / `active`。知识版本不是软件发布。

当前结果唯一入口：[EVD-048](../../../architecture/evidence/current-evidence.md#evd-048495迁移候选与本地证据)。[原始贡献来源](../../../requirements-design-test-contributions/495-legacy-installation-upgrade/test.md)保留各轮证据及PR195来源补证，不能用早期待执行叙述覆盖本版状态。策略及逐requirement映射见本版strategy/trace。

| Acceptance | 当前证明与剩余 |
| --- | --- |
| MIG-495-01..05 | 精确旧来源preview、实际local升级、身份投影、planning及dirty unpublished dev的current owners/fresh Planning接续已定向验证；正式远端来源仍待同HEAD验收 |
| MIG-495-06 | 已有可执行只读诊断及PR195 exact旧来源核对；完整代表public旧PR/merge处置与genuine受支持来源旧Finalizer/Finish在途仍缺；不得用终态或模拟checkpoint替代 |
| MIG-495-07 | 普通部分写入后resume、实际写后rollback/旧runtime及新增meta/notes工作保护已验证，适用范围不包含Git/远端历史回写 |
| MIG-495-08 | source/installed/dogfood/platform、同候选current update/reapply、hash/drift/sidecar已验证；same-remote-HEAD source_locked public升级与同源marketplace/provider待候选PR固定HEAD后执行 |
| MIG-495-09 | mixed/deferred库存的正式creator、identity/branch/checkout/session接续及正常拒绝边界已验证，旧记录保留原字节而不成为lifecycle authority |

本次只晋升候选代码/合同与本地知识。promotion-created diff须fresh Architecture/Phase2、TaskCommit与不同reviewer完整origin/main...HEAD审查，之后Refs-only候选Delivery才固定remote source。正式验收失败留在同一任务修复并刷新适用gates；全部MIG01..09齐备前禁止merge/Completion。完整累计多平台矩阵、软件tag/Release和真实业务安装未执行，保持独立边界。
