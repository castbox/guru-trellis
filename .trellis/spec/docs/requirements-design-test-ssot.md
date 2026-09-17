# Requirements / Design / Test SSOT 使用规则

## Current identity

- version：`current-main-0.6.17-guru.53`
- status：`active`
- Requirements：`docs/requirements/README.md`
- Design：`docs/design/README.md`
- Test：`docs/test/README.md`
- Architecture inheritance：`docs/architecture/README.md`，`current-main-0.6.17-guru.53` / `active`
- source binding：reviewed #418 contribution + inherited immutable `current-main-0.6.17-guru.52` authority；current graph 23 Skills / 100 exits / 78 commands。当前四轴与固定 Fork 来源继承 `.52`，见三个 README 与 Architecture `ARCH-CUR-029/030`；新增只读复审决策为 `ADR-010`。retired internal API active-zero、普通 lifecycle、Constitution/GAP/#305 target 不变。本 projection 不记录远端动作或动态 Gate 状态。

## 读取与更新

依序读 Requirements -> Design -> Test -> Architecture，并通过 `REQ/BEH -> DES/CON -> TST/SCN/CASE -> ARCH/EVD` identity 跟踪，不复制 source prose。

普通 task 先调用 `guru-maintain-requirements-design-test-ssot:task_impact_sync`。`sync_required` 只进入 target-authored `promotion`；`revision_required` 回当前 planning/implementation owner；`baseline_incomplete` 回 Bootstrap/repair；`blocked` 停止。并行 task 默认写 `docs/requirements-design-test-contributions/<task-ref>/`，不直接竞争 shared current。

## Freshness

每次 gate 必须重读三个 README 的 current locator/version/status、Architecture public identity、live task delta 和 source binding。locator 不存在、版本不一致、traceability 断裂或 projection 落后时，不得沿用本页，进入 owner `repair`。软件四轴与 current knowledge identity 独立；`.53` snapshot 不证明 promotion-created diff 之后的 Phase 2/commit/Branch Review、Publication、push、PR、merge、tag、Release 或 Issue closure。R418/D418/T418 的 current delta 与双向 trace 在三层 `.53` authority 定义；R410/R408 及更早证据作为 inherited `.52` history 保留。
