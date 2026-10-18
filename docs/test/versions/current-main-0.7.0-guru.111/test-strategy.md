# Test 当前 authority

版本：`current-main-0.7.0-guru.111`；状态：`active`。Architecture：`current-main-0.7.0-guru.102/active` / `docs/architecture/README.md`。前驱：`current-main-0.6.17-guru.110`。

## 适用范围与定位

| Scope identity | Status | Complete definition | Relations |
| --- | --- | --- | --- |
| RDT-LIFECYCLE | current | [Task/Delivery](../../current/task-delivery-lifecycle.md) | [迁移身份映射](../../../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md) |
| RDT-COMPLETION | current | [Completion/Closure](../../current/completion-closure.md) | 同上稳定身份及必要 R/D/T 关系 |
| RDT-KNOWLEDGE | current | [知识维护](../../current/knowledge-maintenance.md) | 两套原维护方、两层架构源 |
| RDT109-LEGACY | legacy_unmigrated | [原完整来源](../current-main-0.6.17-guru.109/test-strategy.md) | 仅未列入上述迁移范围的对象；不得用于覆盖已迁移对象 |

已迁移对象直接读取完整单元及其必要关联，不回放历史贡献拼接当前答案。前驱和贡献只用于来源、历史适用性及迁移核对。旧 Task 保持其明确阶段适用版本；需要本版的历史正文时使用固定 Git commit 读取，不跟随日后可变 current 目录。无关共享版本推进不强制重写。公共接口的完整规格仍归各原 canonical package，不能把本导航当接口替代品。

缺来源、断链、冲突或未完成迁移由原维护方说明受影响结论并 repair，保留可读原来源，不推定完整切换。具体方法见 [迁移合同](../../../../trellis/presets/guru-team/MIGRATION-331.md)。本版来源和必要追踪由 [#331 contribution](../../../requirements-design-test-contributions/331-current-effective-knowledge/traceability.md) 保留；实际验证及限制只由其 [Test](../../../requirements-design-test-contributions/331-current-effective-knowledge/test.md) 拥有。知识晋升不证明 Task Completion、软件 Release 或业务采用。

历史读取时，原维护方从该 Task 已确定的阶段适用 source/plan/candidate Git revision 定位包含本版完整正文的同一 tree，并在该 tree 解析版本页、current 正文及必要相对引用。只有版本 identity 而没有可验证 revision 时，沿原 owner 的 Git 历史定位本版受审完整正文的建立提交；不得用最近 HEAD 猜选。无法唯一定位则进入原 repair/blocked，不将旧版本页与 live current 混读。

## 版本身份后继

本版按 [Issue #626](https://github.com/castbox/guru-trellis/issues/626) 的内部版本要求，将 current identity 前缀调整为 `0.7.0-guru.###` 并递增序号。完整知识单元、稳定身份、已迁移范围、未迁移原来源和原验证归属保持。此版本映射不新增能力，不代表软件发布或重新完成 #331 的行为/成本验收。

前驱完整 tree 为 [`33f18a768c9c8d901f34b899934ac40c3d97cc5b`](https://github.com/castbox/guru-trellis/tree/33f18a768c9c8d901f34b899934ac40c3d97cc5b/docs/test)；读取前驱时在该 tree 一并解析版本页、current 正文及必要引用，不将旧 identity 跟随新导航解释。
