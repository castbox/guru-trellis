# Completion / Closure / Finish 测试策略

知识单元：`RDT-TST-COMPLETION`。状态：`current`。固定前驱 RDT `.109` / Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`。需求：[RDT-REQ-COMPLETION](../../requirements/current/completion-closure.md)；设计：[RDT-DES-COMPLETION](../../design/current/completion-closure.md)。保留 `TST-004/010`、`SCN-003` 的历史与终态能力关系，旧Finalizer推定由原后继替代。

## 整体范围与证据场景

| Test identity / trace | 输入和正常动作 | 预期结果 |
| --- | --- | --- |
| T531-06 / T454-D436-01 | 多slice均terminal但有unallocated/变更scope，或一个full merge | whole-scope仍独立判断，未完成不completed；completed仅交Closure；phase/artifact/merge不等pass。 |
| T383-01 / R383-06/07 | feature、diagnosis、mitigation、implementation-only与production修复目标分别完成/缺口 | feature不强加production；未知原因不抹除已满足诊断/缓解，但要求定位原因的诊断仍unfinished；code/test不冒充production/root-cause。 |
| T383-01 / R383-08 | 同输入、合法严格等价证据、一次性不可安全重放或证据不足 | AI比较原关键条件/路径/状态/结果；不强迫危险replay/授权外部写；不足为evidence_pending并留acquisition owner/condition。 |
| T531-06 / R531-06 | 无currentDelivery、已有全部交付仅待证据；新证据到达 | 不造空Delivery；pending保持Task active，refresh重读当前scope/facts；无新证据不重放旧completed。 |
| BEH-557-02 / T557链 | 原Merge记录人工actual head不同于published，CI pending/failed或新增路径 | 比较实际完整差额和当前要求，保留CI真实状态及非必要项边界；必要缺口回owner/pending，不重复merge。 |
| BEH567-06 / BEH569-09 | 旧cutoff后出现无关提交/已知同Task新Delivery | 无关不要求重query/integrate；必要新facts只补缺口；旧cutoff不证明新facts，无必要时不设history前置。 |

## Closure、终态与恢复场景

| Test identity / trace | 输入和正常动作 | 预期结果 |
| --- | --- | --- |
| T547-01/02 / R547-01..05 | exact_source Task整体scope完成，但source仍有显式责任 | 原source不变；retain_open provider OPEN、零close、public no_mutation/source_result=null；Finish合法接续。 |
| T547-03/04 | no_issue、reference_only及exact_source close/already_closed、混合source retain+另一Issue close | 空集/no authority零mutation；already_closed不重复close；aggregate closed不等source_closed；动作逐Issue资格正确。 |
| T547-04/05 / R547-06/07 | semantic blocked、输出丢失、requiredOPEN被关闭/requiredCLOSED被reopen/source改变 | blocked无新transaction/provider；恢复同结果无重复close；drift回Closure fresh review，Finish不擅自close/reopen。 |
| T454-D436-03 / T547-02 | Closure当前且状态一致；archive/bookkeeping事务输出丢失 | exactscope/history/限制进入唯一archive；schema2 retired字段不写；无closing keywords/Deliverytrailers；remote验证后success，无重复archive/PR/merge。 |
| T454-D436-04 | 当前seal的owned资源，caller/unknown/peer资源、仍有consumer、执行checkout在删除目标内 | 仅fresh reviewed精确owned资源可删；保留其它资源；换保留checkout或manual route；失败不撤回先前三项完成。 |
| T454-D436-05 / T531-06 | sealed正常archiveReactivate、manual archive/未完Finish控制、新gen仅验证 | 同TaskId/source递增generation/重建binding，唯一active；旧receipts/session不授权；三种恢复分路，validation不造businessDelivery。 |

## 证据归属

共同因果语义和场景期望以 [canonical causal spec](../../../trellis/presets/guru-team/spec/workflow/causal-completion-semantics.md) 为准。只用正常支持路径和普通状态变化验证，不引入攻击/压力模型。历史 [#383 Test](../../requirements-design-test-contributions/383-causal-completion-semantics/test.md)、[#547 Test](../../requirements-design-test-contributions/547-retain-source-open/test.md)、[#454 D436 Test](../../requirements-design-test-contributions/454-task-lifecycle-d436/test.md)、[#531 Test](../../requirements-design-test-contributions/531-task-delivery-lifecycle/test.md) 保留原样及原适用candidate；workflow fixture不等业务生产效果。

本轮 T331-02/V331-B 一致修订和 T331-03/V331-C 并行/旧Task实验覆盖知识迁移对本能力的影响。全部实际结果、first failure/修复与未验证边界只写 [#331 test](../../requirements-design-test-contributions/331-current-effective-knowledge/test.md)，此处不预填通过。完整接口/执行断言按各终态package当前合同选择，不能用归档存在或link check代替whole-task判断。
