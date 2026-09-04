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

后续 supersede 时保留 predecessor/successor identity 与历史边界，不改写旧决策为 current evidence。

`ADR-005` 正文见 [`005-architecture-lifecycle-convergence.md`](./005-architecture-lifecycle-convergence.md)。
`ADR-006` 正文见 [`006-base-authority-checkout-routing.md`](./006-base-authority-checkout-routing.md)。
`ADR-007` 正文见 [`007-finalizer-extension-source-target-binding.md`](./007-finalizer-extension-source-target-binding.md)。
`ADR-008` 正文见 [`008-solution-mechanism-qualification.md`](./008-solution-mechanism-qualification.md)。
