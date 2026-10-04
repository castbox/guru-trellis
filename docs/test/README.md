# Test Strategy / Test Plan SSOT

唯一 current authority 是 `current-main-0.6.17-guru.71` / `active`；本版[入口](./versions/current-main-0.6.17-guru.71/test-strategy.md)明确继承 immutable `.70` 的全部有效合同，仅追加已审查的 `R490/D490/T490` 与当前 Fork `9c36002a324c16a09a85b6aa5a380b74aabf801f`。Architecture 为 `.71/active`；旧 `.70` 及以下正文保留 predecessor provenance，不能覆盖本版 identity/source/验证边界。软件版本未由知识 promotion 发布，#489 独占 release proof。

历史 `.70` authority：[`versions/current-main-0.6.17-guru.70/test-strategy.md`](./versions/current-main-0.6.17-guru.70/test-strategy.md) 与 [`test-plan.md`](./versions/current-main-0.6.17-guru.70/test-plan.md)。`traceability.md` 连接 Requirements、Design、Architecture `.70/active` 和 evidence；`.69` 及更早版本保持 immutable。

历史 `.70` 状态：`superseded`。当时 `.70` 完整继承 immutable `.69` 并承接 #481 task-personnel retirement；`T481-01..07` 是本次增量的 current acceptance authority，`T467-01..06`、`T454-G7-01..10` 与 `T434-01..39` 是继承能力。提升前证据不能代替 promotion-created diff 的 fresh Phase 2、Task Commit 与完整 Branch Review。旧版本安装升级、完整多平台 Release Gate 与业务仓生产验证仍 `unverified`。

历史 `FIN454-C4-P1-004` 在相同 `TST-032/SCN-044` 下增加 same-base old-review/provenance-tail/two-finding-fix topology、terminal PR exclusion、Open PR rejection、两个 transaction endpoint、intermediate remote rejection 与 replacement transaction binding；当时 provenance `23/23`、recovery `48/48`、Finalizer package `113/113` 通过，raw preset apply 被三项 pre-E434 sidecar 阻塞。该前驱快照不代表当前 `.71`；`.67` 的 preset reapply、dogfood drift 与 installer/graph `118/118` 是独立历史证据，仍不替代本次 promotion-created diff 的正式门禁。

| 状态 | 版本 | Locator |
| --- | --- | --- |
| `active` | `current-main-0.6.17-guru.71` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.71/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.70` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.70/test-strategy.md) |
| `superseded` | `current-main-0.6.17-guru.69` | [`test-strategy.md`](./versions/current-main-0.6.17-guru.69/test-strategy.md) |
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

历史 `.68/active` 快照完整继承 immutable `.67` 并承接 #454 generation 7；其 Architecture 当时为 `.68/active`，现已由 `.70` 取代。当前 `.70` 的 promotion-created diff 仍须 fresh Phase 2、Task Commit 与完整 Branch Review；专门 Release matrix 和业务仓生产验证仍未验证。
