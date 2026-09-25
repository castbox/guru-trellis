# Test Strategy / Test Plan SSOT

当前 authority：[`versions/current-main-0.6.17-guru.64/test-strategy.md`](./versions/current-main-0.6.17-guru.64/test-strategy.md) 与 [`test-plan.md`](./versions/current-main-0.6.17-guru.64/test-plan.md)。`traceability.md` 连接 Requirements、Design、Architecture `.64/active` 和 evidence；`.63` 及更早版本保持 immutable。

状态：`active`。`.64` 完整继承 immutable `.63` 并承接 #454 C6/C7 非激活 substrate 与 subtraction。`T454-C6C7-01..07` 是 current acceptance authority，focused lifecycle `125/125` 只证明提升前 candidate；package integration `19/20` 与 managed fixture 不声明通过。promotion-created diff 必须由后续 owner独立完成 fresh Phase 2、Task Commit 与完整 Branch Review。D443、D436、E434、#434 activation、完整 Release Gate 与生产升级仍 `unverified`。

`FIN454-C4-P1-004` 在相同 `TST-032/SCN-044` 下增加 same-base old-review/provenance-tail/two-finding-fix topology、terminal PR exclusion、Open PR rejection、两个 transaction endpoint、intermediate remote rejection 与 replacement transaction binding；provenance `23/23`、recovery `48/48`、完整 Finalizer package `113/113` 通过。raw preset apply 仍由三项既有 pre-E434 sidecar 阻塞，专用 dogfood drift 通过；这些实现证据不声明 gate pass。

| 状态 | 版本 | Locator |
| --- | --- | --- |
| `active` | `current-main-0.6.17-guru.64` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.64/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.63` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.63/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.62` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.62/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.61` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.61/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.60` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.60/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.59` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.59/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.58` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.58/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.57` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.57/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.56` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.56/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.55` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.55/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.54` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.54/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.53` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.53/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.52` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.52/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.51` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.51/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.50` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.50/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.49` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.49/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.48` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.48/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.47` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.47/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.46` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.46/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.45` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.45/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.44` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.44/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.43` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.43/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.42` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.42/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.41` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.41/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.40` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.40/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.39` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.39/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.38` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.38/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.37` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.37/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.36` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.36/test-strategy.md) |
| `superseded` | `current-main-0.6.5-guru.35` | [`test-strategy.md`](./versions/current-main-0.6.5-guru.35/test-strategy.md) |
| `released-history` | `v0.6.5-guru.9` | [`README.md`](./versions/v0.6.5-guru.9/README.md) |

`.64/active` 完整继承 immutable `.63` 并吸收 reviewed #454 C6/C7 contribution；Architecture 为 `.64/active`。C6/C7 的提升前 focused 证据已建立；promotion-created diff 的 fresh gates 由后续 exact-range 结果独立证明。D443、D436、E434、#434 production activation 与完整发布矩阵保持独立且当前未验证。
