# ADR Index

| ADR | 状态 | 决策 |
| --- | --- | --- |
| `ADR-001` | accepted | official Trellis extension surfaces first；Markdown/Skill 与 deterministic runtime 分层 |
| `ADR-002` | accepted | RDT 与 Architecture 保持独立 semantic owners，Bootstrap 只做编排与 cross-review |
| `ADR-003` | accepted | current main as-built 与 stable released baseline 分开版本化 |
| `ADR-004` | accepted | `.trellis/spec` 只做 minimal locator/usage projection |
| `ADR-005` | accepted | 双维 authority 只在 task-local change contract 相交；shared current 由 expected-current-bound single writer 在 independent review 后 promotion，并强制 post-promotion re-entry |
| `ADR-006` | accepted | base selection 与 authority checkout binding 分离；detached session 只作为 invocation shell，selected-base checkout 独占同步与 equality authority |
| `ADR-007` | accepted | Finalizer extension source checkout 与 target reviewed checkout 独立绑定；closed `self_hosted|installed` modes |
| `ADR-008` | accepted | normal-scenario 与 solution-mechanism 资格由独立 semantic owners 承接，OS primitive 不得成为业务 authority |
| `ADR-009` | accepted | Publication 独占 Issue reference/closure intent；Finalizer执行 reviewed payload，GitHub执行默认分支closing keyword，Merge验证live result；不保留跨 owner aggregate 或 compatibility reader |
| `ADR-010` | accepted | 归档复审在原四个 owner 内保持只读；原 H、当前 A、复审 B 与 PR 快照/新 payload 判断独立，普通 profiles 不放宽 |
| `ADR-011` | accepted | 唯一workflow continuation block拥有active-task detailed route；lost result回原producer或fresh semantic owner，upstream保持thin-entry ownership |
| `ADR-012` | accepted | Active Task Delivery由Review/Publish/Merge三个单写owner承接；merge trailer与GitHub/Git identity形成跨分支事实，task在Delivery后保持active，#434/#436边界不前移 |
| `ADR-013` | accepted | Post-Delivery Completion、Closure、Finish、Cleanup与Reactivate由五个独立owner承接；#436提供终态能力但不提前激活production graph，#434仍独占graph cutover |
| `ADR-014` | accepted | Stable task identity与official Trellis session store保持authority；独立binding owner承接resume/rebind/switch/reactivate/manual recovery，#434前保持workflow-deferred |

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
