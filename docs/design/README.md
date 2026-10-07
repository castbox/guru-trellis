# Design SSOT

唯一 current authority 是 `current-main-0.6.17-guru.73` / `active`；[本版入口](./versions/current-main-0.6.17-guru.73/design-main.md)完整继承 immutable `.72` 有效合同，并承接 #495 [固定来源验收贡献](../requirements-design-test-contributions/495-legacy-installation-upgrade-acceptance/test.md)。Fork `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1` / CLI `0.7.0-castbox.2`，Guru `0.7.0-guru.2` 为未发布候选，Architecture `.73/active`。MIG-495-01..09 证据区分首次失败/恢复、真实 live PR/merge、旧正式 writer 构造快照与新固定 `6a563f5f` source_locked/provider/actual installed；不声明单轮七场景全通过。晋升 diff 仍须 fresh Phase2/commit/独立完整 Branch Review，后续 merge/Completion 不能复用晋升前 gate。软件发布、真实业务安装、完整累计矩阵保持独立未验证；下文 `.72` 及更早条目只作 immutable predecessor provenance。

历史 `.70` Design authority：[`versions/current-main-0.6.17-guru.70/design-main.md`](./versions/current-main-0.6.17-guru.70/design-main.md)。版本状态与 source binding 见同目录 `manifest.yaml`；#481 后的 registry（34 packages / 155 exits / 104 commands，零 planned）见 [`capability-inventory.md`](./versions/current-main-0.6.17-guru.70/capability-inventory.md)，引用链见 `traceability.md`，决策见 `decisions.md`。production workflow 为 33 mandatory invokes / 153 exits。Architecture 为 `.70` / `active`；`.69` 及更早版本保持 immutable。

`.62` Design source binding 同时承接 C4 范围内的 Finalizer provenance recovery guard：初始 reprepare 在无 predecessor transaction 时按真实 Git ancestry 接受 strict historical ancestor，并由 application-level replacement transaction 保存 exact `pre_push_remote_head`；后续 pre-mutation preflight 必须复用该 remote identity。该段只闭合 `REQ-048` / `TST-032` 的设计映射，不把 C4 变成 Finalizer、C5-C7 或 production activation。

`FIN454-C4-P1-004` 仍由 `DES-046` 处理：selected base 无变化时，以 predecessor tail/base lineage/current review equality 与无 Open PR证明 fresh-reviewed descendant；remote 只认 transaction-owned pre-push/Publication endpoints，terminal PR history 不参与 current classification。它不新增 schema、public DTO、selector 或 branch/session/path 绑定。

Design 只解释实现 ownership 与 contract，不覆盖 Requirements 或 Architecture。普通 task 通过 RDT `task_impact_sync` / contribution / `promotion` 更新 current。

| 状态 | 版本 | Locator |
| --- | --- | --- |
| `active` | `current-main-0.6.17-guru.73` | [design-main.md](./versions/current-main-0.6.17-guru.73/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.72` | [design-main.md](./versions/current-main-0.6.17-guru.72/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.71` | [`design-main.md`](./versions/current-main-0.6.17-guru.71/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.70` | [`design-main.md`](./versions/current-main-0.6.17-guru.70/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.69` | [`design-main.md`](./versions/current-main-0.6.17-guru.69/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.68` | [`design-main.md`](./versions/current-main-0.6.17-guru.68/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.67` | [`design-main.md`](./versions/current-main-0.6.17-guru.67/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.66` | [`design-main.md`](./versions/current-main-0.6.17-guru.66/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.65` | [`design-main.md`](./versions/current-main-0.6.17-guru.65/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.64` | [`design-main.md`](./versions/current-main-0.6.17-guru.64/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.63` | [`design-main.md`](./versions/current-main-0.6.17-guru.63/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.62` | [`design-main.md`](./versions/current-main-0.6.17-guru.62/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.61` | [`design-main.md`](./versions/current-main-0.6.17-guru.61/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.60` | [`design-main.md`](./versions/current-main-0.6.17-guru.60/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.59` | [`design-main.md`](./versions/current-main-0.6.17-guru.59/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.58` | [`design-main.md`](./versions/current-main-0.6.17-guru.58/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.57` | [`design-main.md`](./versions/current-main-0.6.17-guru.57/design-main.md) |
| `superseded` | `current-main-0.6.17-guru.56` | [`design-main.md`](./versions/current-main-0.6.17-guru.56/design-main.md) |
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

`.58` 作为 immutable predecessor 完整继承 `.57` 并吸收 reviewed #452 contribution；该 snapshot 的 Architecture identity 为 `.58/active`。平台 authority 只有 pinned upstream 22-platform inventory 与目标仓库 exact `selected_platforms` 两层；重复 `--platform` 选择 exact subset，公开 CLI 不提供全集安装选项，无 flag 默认及 `guru-trellis` dogfood 均为 Claude、Codex、Cursor，OpenCode 是 upstream inventory 普通成员。#434 独占 production graph activation；promotion-created combined diff 必须重新通过 fresh Phase 2、Task Commit、完整 Branch Review，且该 snapshot 不声明 implementation、tests 或完整 Release matrix 已通过。
