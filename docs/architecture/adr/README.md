# ADR Index

| ADR | 状态 | 决策 |
| --- | --- | --- |
| `ADR-001` | accepted | official Trellis extension surfaces first；Markdown/Skill 与 deterministic runtime 分层 |
| `ADR-002` | accepted | RDT 与 Architecture 保持独立 semantic owners，Bootstrap 只做编排与 cross-review |
| `ADR-003` | accepted | current main as-built 与 stable released baseline 分开版本化 |
| `ADR-004` | accepted | `.trellis/spec` 只做 minimal locator/usage projection |
| `ADR-005` | accepted; promotion timing superseded by ADR-030 | 双维 authority 只在 task-local change contract 相交；shared current 由 expected-current-bound single writer 在 independent review 后 promotion，并强制 post-promotion re-entry |
| `ADR-006` | accepted | base selection 与 authority checkout binding 分离；detached session 只作为 invocation shell，selected-base checkout 独占同步与 equality authority |
| `ADR-007` | accepted | Finalizer extension source checkout 与 target reviewed checkout 独立绑定；closed `self_hosted|installed` modes |
| `ADR-008` | accepted | normal-scenario 与 solution-mechanism 资格由独立 semantic owners 承接，OS primitive 不得成为业务 authority |
| `ADR-009` | accepted | Publication 独占 Issue reference/closure intent；Finalizer执行 reviewed payload，GitHub执行默认分支closing keyword，Merge验证live result；不保留跨 owner aggregate 或 compatibility reader |
| `ADR-010` | accepted | 归档复审在原四个 owner 内保持只读；原 H、当前 A、复审 B 与 PR 快照/新 payload 判断独立，普通 profiles 不放宽 |
| `ADR-011` | accepted | 唯一workflow continuation block拥有active-task detailed route；lost result回原producer或fresh semantic owner，upstream保持thin-entry ownership |
| `ADR-012` | accepted | Active Task Delivery由Review/Publish/Merge三个单写owner承接；merge trailer与GitHub/Git identity形成跨分支事实，task在Delivery后保持active，#434/#436边界不前移 |
| `ADR-013` | accepted | Post-Delivery Completion、Closure、Finish、Cleanup与Reactivate由五个独立owner承接；#436提供终态能力但不提前激活production graph，#434仍独占graph cutover |
| `ADR-014` | accepted | Stable task identity与official Trellis session store保持authority；独立binding owner承接resume/rebind/switch/reactivate/manual recovery，#434前保持workflow-deferred |
| `ADR-015` | accepted | TaskId/TaskRef/generation与stage evidence分离；Fork/Guru owner边界固定，base pair只服务operation-scoped consumer，不形成durable identity或第二store |
| `ADR-016` | accepted | 业务 Delivery 与 Task Completion/Closure/Finish/Cleanup 分离；同 TaskId 多次交付及新代 Reactivate，#434 原子图激活并退休旧边 |
| `ADR-017` | accepted; source restriction superseded by ADR-018 | 历史固定来源；current-only、唯一writers、固定恢复/回退锚点与删除出口仍有效 |
| `ADR-018` | accepted | 全部0.6.x/0.7.0系列实际合同分组升级；本地slice晋升后同源远端验收，整体仍open |

| `ADR-019` | accepted; 无因新reviewer片段由ADR-034窄替代 | Architecture Skill 拥有独立新评估方法；fresh subagent 执行，原 owner 保留下游 eligibility 与 promotion |

后续 supersede 时保留 predecessor/successor identity 与历史边界，不改写旧决策为 current evidence。

`ADR-005` 正文见 [`005-architecture-lifecycle-convergence.md`](./005-architecture-lifecycle-convergence.md)。
`ADR-006` 正文见 [`006-base-authority-checkout-routing.md`](./006-base-authority-checkout-routing.md)。
`ADR-007` 正文见 [`007-finalizer-extension-source-target-binding.md`](./007-finalizer-extension-source-target-binding.md)。
`ADR-008` 正文见 [`008-solution-mechanism-qualification.md`](./008-solution-mechanism-qualification.md)。
`ADR-009` 正文见 [`009-issue-reference-closure-ownership.md`](./009-issue-reference-closure-ownership.md)。
`ADR-010` 正文见 [`010-archived-review-authority.md`](./010-archived-review-authority.md)。
`ADR-011` 正文见 [`011-active-task-continuation-authority.md`](./011-active-task-continuation-authority.md)。
`ADR-012` 正文见 [`012-active-task-delivery-loop.md`](./012-active-task-delivery-loop.md)。
`ADR-013` 正文见 [`013-post-delivery-completion-finish.md`](./013-post-delivery-completion-finish.md)。
`ADR-014` 正文见 [`014-task-identity-session-binding.md`](./014-task-identity-session-binding.md)。
`ADR-015` 正文见 [`015-task-lifecycle-state-model.md`](./015-task-lifecycle-state-model.md)。
`ADR-016` 正文见 [`016-task-delivery-lifecycle.md`](./016-task-delivery-lifecycle.md)。

`ADR-017`正文见 [`017-legacy-installation-upgrade.md`](./017-legacy-installation-upgrade.md)。

`ADR-018` 正文见 [`018-legacy-installation-version-families.md`](./018-legacy-installation-version-families.md)。

`ADR-019` 正文见 [`019-independent-architecture-assessment.md`](./019-independent-architecture-assessment.md)。

`ADR-020`（accepted）：独立目标感知根因候选准入，normal/solution/root 与现有阶段完成 owners 分离。正文见 [`020-root-cause-qualification.md`](./020-root-cause-qualification.md)；ADR-008/019/005 的有效职责继续继承。

`ADR-021`（accepted）：隔离修改由原 task-free execution/C6 creation-only owners 承接，Guru caller 消费真实无 Task 返回，既有 primary recovery/Sync/绑定与独立副作用边界保持。正文见 [`021-checkout-isolation.md`](./021-checkout-isolation.md)。

`ADR-022`（accepted）：唯一 Author 写 Task planning，原 Architecture 的 candidate/final planning3.0 保持单 owner 与明确消费者，Approval 独立。正文见 [`022-unique-planning-author.md`](./022-unique-planning-author.md)。

`ADR-023`（accepted）：活动 Clarify scope_ready 先判断后交原 clear-router 薄投影，由同一 Author 写作；旧成功结果 fresh 重入。正文见 [`023-scope-ready-before-planning.md`](./023-scope-ready-before-planning.md)。

`ADR-024`（accepted）：公共Delivery拥有所有开发阶段与Planning；Guru语义门禁和私有发布事务独立，Task整体责任保持。正文见 [`024-task-delivery-public-authority.md`](./024-task-delivery-public-authority.md)。只替代ADR-022的Task规划/Task首次或resume激活片段、ADR-015/016中依赖Task开发status的执行路由；身份、generation、整体收尾与恢复责任继续继承。

`ADR-025`（accepted）：exact_source 来源资格与本次 retain_open/close 处置分离；Closure 仍独占动作，Finish 校验每项所需状态，aggregate 与 exact source fact 分开。正文见 [`025-retain-source-open-disposition.md`](./025-retain-source-open-disposition.md)；ADR-013/024 的原 owners 与公共模型职责保持。

| `ADR-026` | accepted | 原 Merge 归属真实手动合入事实，public writer 不变；原 Completion 保留实际候选/CI/整体证据判断，显式 query2 只读已记录事实 |

`ADR-027`（accepted）：独立单 checkout tools/selected legacy Task 维护；公共模型与恢复归 Trellis，原 owners 承接私有控制/runtime/业务职责，旧 Plan2 与 current-only 保持。正文见 [`027-independent-install-maintenance.md`](./027-independent-install-maintenance.md)。

`ADR-028`（accepted）：固定开发基线、Delivery 完整内容与 PR target 分离，原 owners 只按实际集成阻塞整合，并选择明确阶段适用 authority。正文见 [`028-fixed-content-baseline.md`](./028-fixed-content-baseline.md)。只替代 ADR-005 的普遍 CURRENT-advance stale 解释及 ADR-012 第7项的无条件 fresh Phase2 要求；当前其他条目中的默认追赶、latest-target 祖先资格与目标 SHA 全等由 ADR-028 中具名的 current successor 承接。ADR-013/024、历史正文、公共 Task/Delivery、独立语义判断、expected-head、真实事务与整体收尾责任保持。

`ADR-029`（accepted）：跨 owner 工程事实采用与当前完整独立语义判断分离；只窄补充 ADR-019 的命令执行限制和 Check same-owner-only，继承 ADR-028 适用性，原 owner、当前绑定、typed routes 与 private retirement 不变。正文见 [`029-cross-owner-validation-facts.md`](./029-cross-owner-validation-facts.md)。

| `ADR-030` | accepted | 受审分支晋升先于最终 Check；原 authority、committed 独立判断、完整 Review 与有界引用对齐保持 |

`ADR-030` 正文见 [`030-promotion-before-final-check.md`](./030-promotion-before-final-check.md)。

- [ADR-031：完整当前知识单元与两层栈来源](./031-current-effective-knowledge.md)

- [ADR-032：受管文本 LF 与精确 EOL 恢复](./032-managed-text-lf.md)；限定installer字节判定的窄后继，raw身份与用户编辑保护保持。

- [ADR-033：原 owners 提前提供 Draft 反馈](./033-early-draft-feedback.md)；早期有界提交、同PR状态往返与最终门禁分别承接。

- [ADR-034：候选适用性与完整覆盖](./034-candidate-applicability-and-coverage.md)；窄替代 ADR-019/029 及原 finding 流程的无因新 reviewer/相同完整重审，保留首次独立完整、当前正式结果、ADR-028/030/033 和原 owners。

- [ADR-KNOWLEDGE-FINAL-INTEGRATION：稳定身份与最终整合晋升](./knowledge-final-integration.md)；窄承接ADR-030时机与普通全局successor/总入口必写义务，保留最终质量与历史原义。

- [ADR-PORTABLE-SHARED-LIFECYCLE：共享生命周期与本机责任分离](./portable-shared-lifecycle.md)；窄承接 ADR-024/027 的恢复及指定正式 schema1 接受范围，保留公共 writer、原 owners、资源边界和完整最终质量链。

- [ADR-035：活动续接与scope两次承接](./035-current-continuation-scope-routing.md)；窄替代ADR-011/023/024的旧created/恢复/scope路由片段，保留公共模型、原producer和阶段owners。

- [ADR-CONTRACT-CONTINUITY：固定 before 缺失与维护回程](./contract-continuity.md)；原三个 authority locator 的真实历史缺失、固定 B..H 和同次 promotion 维护回程。

- [ADR-EXPLICIT-REVIEW-OBJECT：独立 final_plan 只读评审对象](./explicit-review-object.md)；窄替代普遍接收选择前置，保留普通执行恢复、原事实校验与相邻Approval资格。
