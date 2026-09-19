# Design SSOT

唯一 current Design authority：[`versions/current-main-0.6.17-guru.56/design-main.md`](./versions/current-main-0.6.17-guru.56/design-main.md)。版本状态与 source binding 见同目录 `manifest.yaml`；#436 current registry（31 packages / 136 exits / 101 commands）见 [`capability-inventory.md`](./versions/current-main-0.6.17-guru.56/capability-inventory.md)，引用链见 `traceability.md`，决策见 `decisions.md`。五个 lifecycle packages 保持 `deferred`，production workflow 为 22 mandatory invokes / 98 exits。Architecture 继承 `.56` / `active`；`.55` 及更早版本保持 immutable。

Design 只解释实现 ownership 与 contract，不覆盖 Requirements 或 Architecture。普通 task 通过 RDT `task_impact_sync` / contribution / `promotion` 更新 current。

| 状态 | 版本 | Locator |
| --- | --- | --- |
| `active` | `current-main-0.6.17-guru.56` | [`design-main.md`](./versions/current-main-0.6.17-guru.56/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.55` | [`design-main.md`](./versions/current-main-0.6.17-guru.55/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.54` | [`design-main.md`](./versions/current-main-0.6.17-guru.54/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.53` | [`design-main.md`](./versions/current-main-0.6.17-guru.53/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.52` | [`design-main.md`](./versions/current-main-0.6.17-guru.52/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.51` | [`design-main.md`](./versions/current-main-0.6.5-guru.51/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.50` | [`design-main.md`](./versions/current-main-0.6.5-guru.50/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.49` | [`design-main.md`](./versions/current-main-0.6.5-guru.49/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.48` | [`design-main.md`](./versions/current-main-0.6.5-guru.48/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.47` | [`design-main.md`](./versions/current-main-0.6.5-guru.47/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.46` | [`design-main.md`](./versions/current-main-0.6.5-guru.46/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.45` | [`design-main.md`](./versions/current-main-0.6.5-guru.45/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.44` | [`design-main.md`](./versions/current-main-0.6.5-guru.44/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.43` | [`design-main.md`](./versions/current-main-0.6.5-guru.43/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.42` | [`design-main.md`](./versions/current-main-0.6.5-guru.42/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.41` | [`design-main.md`](./versions/current-main-0.6.5-guru.41/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.40` | [`design-main.md`](./versions/current-main-0.6.5-guru.40/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.39` | [`design-main.md`](./versions/current-main-0.6.5-guru.39/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.38` | [`design-main.md`](./versions/current-main-0.6.5-guru.38/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.37` | [`design-main.md`](./versions/current-main-0.6.5-guru.37/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.36` | [`design-main.md`](./versions/current-main-0.6.5-guru.36/design-main.md) |
| `superseded` | `current-main-0.6.5-guru.35` | [`design-main.md`](./versions/current-main-0.6.5-guru.35/design-main.md) |
| `released-history` | `v0.6.5-guru.9` | [`README.md`](./versions/v0.6.5-guru.9/README.md) |

Released history 只固定 release identity；未从 tag 恢复的设计内容保持 `unverified`，不能用 current 设计倒填。

`.56/active` 完整继承 `.55` 并吸收 reviewed #436 contribution；Architecture 为 `.56/active`。#434 独占 production graph activation；#436 五个 terminal lifecycle packages 仍保持 deferred。promotion-created combined diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review；完整 Release matrix 保持 `unverified`。
