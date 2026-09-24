# Requirements / Design / Test SSOT 使用规则

## Current identity

- version：`current-main-0.6.17-guru.62`
- status：`active`
- Requirements：`docs/requirements/README.md`
- Design：`docs/design/README.md`
- Test：`docs/test/README.md`
- Architecture inheritance：`docs/architecture/README.md`，`current-main-0.6.17-guru.62` / `active`
- source binding：reviewed #454 C4 contribution + inherited immutable `current-main-0.6.17-guru.61` authority promoted to `current-main-0.6.17-guru.62`；current registry 保持 32 packages / 142 exits / 102 commands并增加三个 planned IDs，production workflow 保持 22 mandatory invokes / 98 exits，fixed Fork source 为 `eb370008c7689d4e272ae626bd002190ecbb3296`。`.62` 完整继承 C2 shared lifecycle kernel、D0 stage-evidence correction、C3 checkout acquisition/provenance 与 C4 branch association/establishment/rebind substrate；C5-C7、D443、D436、E434、#434 production graph activation 与 #410 Release Gate matrix 仍未完成或未验证，focused lifecycle `93/93` 只证明提升前 candidate，preset `85/86` 未声明通过。

## 读取与更新

依序读 Requirements -> Design -> Test -> Architecture，并通过 `REQ/BEH -> DES/CON -> TST/SCN/CASE -> ARCH/EVD` identity 跟踪，不复制 source prose。

普通 task 先调用 `guru-maintain-requirements-design-test-ssot:task_impact_sync`。`sync_required` 只进入 target-authored `promotion`；`revision_required` 回当前 planning/implementation owner；`baseline_incomplete` 回 Bootstrap/repair；`blocked` 停止。并行 task 默认写 `docs/requirements-design-test-contributions/<task-ref>/`，不直接竞争 shared current。

## Freshness

每次 gate 必须重读三个 README 的 current locator/version/status、Architecture public identity、live task delta 和 source binding。locator 不存在、版本不一致、traceability 断裂或 projection 落后时，不得沿用本页，进入 owner `repair`。软件四轴与 current knowledge identity 独立；`.61` snapshot 不证明 `.62` promotion-created diff 之后的 fresh Phase 2、Task Commit、完整 Branch Review、Publication、push、PR、merge、tag、Release 或 Issue closure。R454-C4/D454-C4/T454-C4 的 current delta 与双向 trace 在三层 `.62` authority 定义；C5-C7、D443、D436、E434 仍是未完成边界，C2+D0+C3 与更早 authority 作为 inherited history 保留。
