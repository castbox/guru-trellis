# Test Strategy / Test Plan SSOT

当前 authority：[`versions/current-main-0.6.17-guru.62/test-strategy.md`](./versions/current-main-0.6.17-guru.62/test-strategy.md) 与 [`test-plan.md`](./versions/current-main-0.6.17-guru.62/test-plan.md)。`traceability.md` 连接 Requirements、Design、Architecture `.62/active` 和 evidence；`.61` 及更早版本保持 immutable。

状态：`active`。`.62` 完整继承 immutable `.61` 并承接 #454 C4 branch association/establishment/rebind substrate 及其 bounded Finalizer provenance recovery guard。`T454-C4-01..10` 是 current acceptance authority；`TST-032/SCN-044` 与 `test_provenance.py` 的执行级回归补充 strict-ancestor remote、exact `pre_push_remote_head` transaction binding 和 zero-remote-mutation 证明。focused lifecycle `93/93` 已建立，preset `85/86` 不声明通过。promotion-created diff 必须由后续 owner独立完成 fresh Phase 2、Task Commit 与完整 Branch Review。C5-C7、D443、D436、E434、#434 activation、完整 Release Gate 与生产升级仍 `unverified`。

| 状态 | 版本 | Locator |
| --- | --- | --- |
| `active` | `current-main-0.6.17-guru.62` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.62/test-strategy.md) |
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

`.62/active` 完整继承 immutable `.61` 并吸收 reviewed #454 C4 contribution；Architecture 为 `.62/active`。C4 的提升前 focused 证据已建立；promotion-created diff 的 fresh gates 由后续 exact-range 结果独立证明。C5-C7、D443、D436、E434、#434 production activation 与完整发布矩阵保持独立且当前未验证。
