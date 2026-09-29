# Test Strategy / Test Plan SSOT

当前 authority：[`versions/current-main-0.6.17-guru.69/test-strategy.md`](./versions/current-main-0.6.17-guru.69/test-strategy.md) 与 [`test-plan.md`](./versions/current-main-0.6.17-guru.69/test-plan.md)。`traceability.md` 连接 Requirements、Design、Architecture `.69/active` 和 evidence；`.68` 及更早版本保持 immutable。

状态：`active`。`.69` 完整继承 immutable `.68` 并承接 #467 preparation；`T467-01..06` 是本次增量的 current acceptance authority，`T454-G7-01..10` 与 `T434-01..39` 为继承的 current 能力。提升前 package/installed tests 不能代替 promotion-created diff 的 fresh Phase 2、Task Commit 与完整 Branch Review。前一正式版本既有安装清理仍待 Stage 2 实证；完整多平台 Release Gate 与业务仓生产验证仍 `unverified`。

历史 `FIN454-C4-P1-004` 在相同 `TST-032/SCN-044` 下增加 same-base old-review/provenance-tail/two-finding-fix topology、terminal PR exclusion、Open PR rejection、两个 transaction endpoint、intermediate remote rejection 与 replacement transaction binding；当时 provenance `23/23`、recovery `48/48`、Finalizer package `113/113` 通过，raw preset apply 被三项 pre-E434 sidecar 阻塞。该前驱快照不代表当前 `.68`；`.67` 的 preset reapply、dogfood drift 与 installer/graph `118/118` 是独立历史证据，仍不替代本次 promotion-created diff 的正式门禁。

| 状态 | 版本 | Locator |
| --- | --- | --- |
| `active` | `current-main-0.6.17-guru.69` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.69/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.68` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.68/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.67` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.67/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.66` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.66/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.65` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.65/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.64` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.64/test-strategy.md) |
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

当前 `.68/active` 完整继承 immutable `.67` 并承接 #454 generation 7；Architecture 为 `.68/active`。promotion-created diff 仍须 fresh Phase 2、Task Commit 与完整 Branch Review；专门 Release matrix 和业务仓生产验证仍未验证。
