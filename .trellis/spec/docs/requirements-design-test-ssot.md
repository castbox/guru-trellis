# Requirements / Design / Test SSOT 使用规则

## Current identity

- version：`current-main-0.6.17-guru.63`
- status：`active`
- Requirements：`docs/requirements/README.md`
- Design：`docs/design/README.md`
- Test：`docs/test/README.md`
- Architecture inheritance：`docs/architecture/README.md`，`current-main-0.6.17-guru.63` / `active`
- source binding：reviewed #454 C5 contribution + inherited immutable `current-main-0.6.17-guru.62` authority promoted to `current-main-0.6.17-guru.63`；current registry 保持 32 packages / 142 exits / 102 commands与四个 planned IDs，production workflow 保持 22 mandatory invokes / 98 exits，fixed Fork source 为 `eb370008c7689d4e272ae626bd002190ecbb3296`。`.63` 完整继承 C2/D0/C3/C4，并增加 C5 path-free official session adapter、resource ledger、Finish seal input 与 Cleanup resolution substrate；C6-C7、D443、D436、E434、#434 activation 与 #410 Release Gate matrix 尚未完成或验证。focused lifecycle `113/113` 只证明提升前 candidate，preset `85/86` 未声明通过。
- Finalizer recovery mapping：`FIN454-C4-P1-004` 不创建新 RDT identity；它继续映射 `REQ-048 -> DES-046 -> TST-032/SCN-044`，以同一 unbound transaction、合法 predecessor tail、selected-base lineage、current review/Publication/live HEAD equality、无 Open PR 与 transaction-owned remote endpoints 构成最小充分绑定。

## 读取与更新

依序读 Requirements -> Design -> Test -> Architecture，并通过 `REQ/BEH -> DES/CON -> TST/SCN/CASE -> ARCH/EVD` identity 跟踪，不复制 source prose。

普通 task 先调用 `guru-maintain-requirements-design-test-ssot:task_impact_sync`。`sync_required` 只进入 target-authored `promotion`；`revision_required` 回当前 planning/implementation owner；`baseline_incomplete` 回 Bootstrap/repair；`blocked` 停止。并行 task 默认写 `docs/requirements-design-test-contributions/<task-ref>/`，不直接竞争 shared current。

## Freshness

每次 gate 必须重读三个 README 的 current locator/version/status、Architecture public identity、live task delta 和 source binding。locator 不存在、版本不一致、traceability 断裂或 projection 落后时，不得沿用本页，进入 owner `repair`。软件四轴与 current knowledge identity 独立；`.62` snapshot 不证明 `.63` promotion-created diff 之后的 fresh Phase 2、Task Commit、完整 Branch Review、Publication、push、PR、merge、tag、Release 或 Issue closure。R454-C5/D454-C5/T454-C5 的 current delta 与双向 trace 在三层 `.63` authority 定义；C6-C7、D443、D436、E434 仍是未完成边界，C2/D0/C3/C4 与更早 authority 作为 inherited history 保留。
