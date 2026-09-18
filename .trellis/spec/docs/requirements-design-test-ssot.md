# Requirements / Design / Test SSOT 使用规则

## Current identity

- version：`current-main-0.6.17-guru.55`
- status：`active`
- Requirements：`docs/requirements/README.md`
- Design：`docs/design/README.md`
- Test：`docs/test/README.md`
- Architecture inheritance：`docs/architecture/README.md`，`current-main-0.6.17-guru.55` / `active`
- source binding：reviewed #435 contribution + inherited immutable `current-main-0.6.17-guru.54` authority；current registry 26 packages / 114 exits / 96 commands，production workflow保持22 mandatory invokes / 98 exits，fixed Fork source 为 `43fffc170927c85d9f7fc106cc5a059e80d4530b`。三个Delivery packages为active/deferred；#434独占production graph activation，#436独占Completion/Closure/Finish/Cleanup/Reactivate；#410 Release Gate matrix保持unverified。

## 读取与更新

依序读 Requirements -> Design -> Test -> Architecture，并通过 `REQ/BEH -> DES/CON -> TST/SCN/CASE -> ARCH/EVD` identity 跟踪，不复制 source prose。

普通 task 先调用 `guru-maintain-requirements-design-test-ssot:task_impact_sync`。`sync_required` 只进入 target-authored `promotion`；`revision_required` 回当前 planning/implementation owner；`baseline_incomplete` 回 Bootstrap/repair；`blocked` 停止。并行 task 默认写 `docs/requirements-design-test-contributions/<task-ref>/`，不直接竞争 shared current。

## Freshness

每次 gate 必须重读三个 README 的 current locator/version/status、Architecture public identity、live task delta 和 source binding。locator 不存在、版本不一致、traceability 断裂或 projection 落后时，不得沿用本页，进入 owner `repair`。软件四轴与 current knowledge identity 独立；`.54` snapshot 不证明 promotion-created diff 之后的 Phase 2/commit/Branch Review、Publication、push、PR、merge、tag、Release 或 Issue closure。R435/D435/T435 的 current delta 与双向 trace 在三层 `.55` authority 定义；R419/R418/R410/R408 及更早证据作为 inherited history 保留。
