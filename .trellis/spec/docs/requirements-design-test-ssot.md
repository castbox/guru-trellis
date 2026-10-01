# Requirements / Design / Test SSOT 使用规则

## Current identity

- version：`current-main-0.6.17-guru.70`
- status：`active`
- Requirements：`docs/requirements/README.md`
- Design：`docs/design/README.md`
- Test：`docs/test/README.md`
- Architecture inheritance：`docs/architecture/README.md`，`current-main-0.6.17-guru.70` / `active`
- source binding：reviewed #481 task-personnel retirement contribution + inherited immutable `current-main-0.6.17-guru.69` authority promoted to `current-main-0.6.17-guru.70`；current registry 为 34 packages / 155 exits / 104 commands，零 planned IDs，production workflow 为 33 mandatory invokes / 153 exits，fixed Fork source 为 `64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac`，CLI/core `0.7.0-castbox.1`。`.69` 的 #434/#454 graph 为 immutable inherited authority；promotion-created diff 须 fresh Phase 2/commit/完整 Branch Review。前一版本既有安装的退役受管资产删除、完整多平台 Release matrix 与业务仓生产验证未由本 projection 证明。
- Finalizer recovery mapping：`FIN454-C4-P1-004` 不创建新 RDT identity；它继续映射 `REQ-048 -> DES-046 -> TST-032/SCN-044`，以同一 unbound transaction、合法 predecessor tail、selected-base lineage、current review/Publication/live HEAD equality、无 Open PR 与 transaction-owned remote endpoints 构成最小充分绑定。

## 读取与更新

依序读 Requirements -> Design -> Test -> Architecture，并通过 `REQ/BEH -> DES/CON -> TST/SCN/CASE -> ARCH/EVD` identity 跟踪，不复制 source prose。

普通 task 先调用 `guru-maintain-requirements-design-test-ssot:task_impact_sync`。`sync_required` 只进入 target-authored `promotion`；`revision_required` 回当前 planning/implementation owner；`baseline_incomplete` 回 Bootstrap/repair；`blocked` 停止。并行 task 默认写 `docs/requirements-design-test-contributions/<task-ref>/`，不直接竞争 shared current。

## Freshness

每次 gate 必须重读三个 README 的 current locator/version/status、Architecture public identity、live task delta 和 source binding。locator 不存在、版本不一致、traceability 断裂或 projection 落后时，不得沿用本页，进入 owner `repair`。软件四轴与 current knowledge identity 独立；`.69` snapshot 不证明 `.70` promotion-created diff 之后的 fresh Phase 2、Task Commit、完整 Branch Review、Publication、push、PR、merge、tag、Release 或 Issue closure。`R481/D481/T481` current delta 与双向 trace 在三层 `.70` authority 定义；`.69` 的 `R467/D467/T467`、`R454-G7/D454-G7/T454-G7`、`R434/D434/T434` 与 C2-C7/D443/D436 作为 inherited history 保留。
