# #600 架构晋升时机贡献

状态：`reviewed_promoted`（本贡献已在原执行分支经独立 Phase2 评估并晋升到 `.96`；后续整合门禁另行执行）；change_path：`target_native`。TaskId=`600-promotion-before-check`，generation=0；Delivery=`068749ef-f7d7-46b6-9715-a831441d8d35`。

当前比较起点为 `ab854ef29448910c332faadeec3c1a5dd810901d:docs/architecture/`，Architecture `.95/active`、constitution v1、change-contract v1。expected-current 只在原 Architecture owner 写前重读，不绑定用户授权。

## 与 main 的实际冲突整合

main@`9a10cb54c4a7eb8016d52b9bd5c3c2ec7de31807` 已拥有 #589 D7 的 `.96`。原 #600 分支内晋升及其比较起点保留于 `87176aea126cc9ade10f334eb379e0d35a053295`，不重新晋升同一贡献。本次整合保留 #589 的 ARCH-CUR-069 / ARCH-DOM-052 / ARCH-INT-055 / EVD-068，将 #600 当前组合投影后继为 ARCH-CUR-070 / ARCH-DOM-053 / ARCH-INT-056 / EVD-069，并使用 `.97` 组合身份。历史 `.96` 正文不回写。ADR-030 与 #589 上游内容计算、Guru 对象准备及恢复职责并存；本次不改变两项既有决定。

`.97` 组合候选包含真实依赖和源码变化。原 reviewed_promoted 只记录已经发生的晋升，不代表该新候选通过；整合后的 Architecture、Check、Task Commit 和独立 Review 必须取得当前结果。两项贡献的实际验证及未验证边界分别由各自唯一 Test 拥有。

## 决策与职责

贡献承接 #600 的晋升时机、结果适用性、窄修订及恢复迁移要求。唯一设计对象是当前 Delivery 的 design.md D600-01..06；本文件不复制流程正文。原 Architecture 负责独立评估、贡献/必要 ADR 和分支内晋升；Check、Commit、Branch Review、Delivery、Completion/Finish 各保留其职责。

[ADR-030](../adr/030-promotion-before-final-check.md)作为 ADR-005 晋升顺序片段的窄后继；ADR-019/028/029 保持。无新 GAP、并行 owner 或兼容双路径。

## 项目合同承接

| Concern | 适用性及证据 |
| --- | --- |
| authority-binding | applicable；Planning3.0 及显式版本化后继非 Planning入口，绑定上述起点和唯一 design。 |
| constitution-binding | applicable；constitution v1 的职责内聚、语义完整和最小必要复杂度，按真实候选判断，不做评分。 |
| boundary-and-decision | applicable；#600 §2-7，target_native，ADR-005 的窄后继与 ADR-019/028/029。 |
| owner-and-single-writer | applicable；原 semantic owners 不变；Architecture 单写 CURRENT，RDT 保留自己的 writer。 |
| compatibility-and-exit | applicable；旧完整安装固定继续，新完整安装成套切换；无 current dual reader，MIGRATION-600 分类在途接续。 |
| gap-and-deviation | applicable；无新 GAP；必须阻止新 CURRENT 掩盖原 authority 到候选的真实偏离。 |
| parallel-scope | applicable；本贡献/task/源码为隔离工作；不修改其他 Task 或在未重读 expected-current 时竞争共享正文。 |
| evidence-and-freshness | applicable；完整 worktree/committed candidate、受审拟写差额和本轮正式结果；命令事实与语义 pass 分离。 |
| review-and-promotion | applicable；候选独立评估先于设计写作；实现后独立评估拟晋升内容，最终 Check/committed Review 覆盖实际写入。本状态不证明这些未来步骤已发生。 |

## Before / After 与验证边界

Before：CURRENT 在 committed Review 后晋升，形成第二轮完整门禁。After：现有 Phase2 独立评估涵盖拟写差额，原 owner 写入分支，最终完整候选通过 Check/Commit/committed 独立判断及完整 Review。比较起点、独立性、no-change、finding 回程和必要恢复继续保留。

项目检查 descriptor 继续为 `guru-trellis-architecture-convergence:repository:1`，入口为 `docs/architecture/06-governance/change-contract.md`，结果合同为 `guru-project-architecture-check-result-2.0`。实际结果及未验证边界由 `docs/requirements-design-test-contributions/600-promotion-before-check/test.md` 单写；知识晋升不证明最终 Check、committed 独立判断、完整 Review、merge、部署或采用通过。
