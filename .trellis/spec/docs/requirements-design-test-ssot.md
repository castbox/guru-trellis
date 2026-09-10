# Requirements / Design / Test SSOT 使用规则

## Current identity

- version：`current-main-0.6.5-guru.48`
- status：`active`
- Requirements：`docs/requirements/README.md`
- Design：`docs/design/README.md`
- Test：`docs/test/README.md`
- Architecture inheritance：`docs/architecture/README.md`，同版本、`active`
- source binding：reviewed `architecture-contribution-392-release-v0616-guru1-v2` + inherited immutable `current-main-0.6.5-guru.47` authority；current graph 23 Skills / 97 exits / 78 commands；current mapping `v0.6.16-guru.1` / extension `0.6.16-guru.41` / CLI `0.6.16` / fixed Fork `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`；#305 target authority 不变（精确 revision 由包含本 authority 的 Git object/tree identity 绑定；本 projection 不记录可变 HEAD、Gate、tag、Release 或 lifecycle 状态）

## 读取与更新

依序读 Requirements -> Design -> Test -> Architecture，并通过 `REQ/BEH -> DES/CON -> TST/SCN/CASE -> ARCH/EVD` identity 跟踪，不复制 source prose。

普通 task 先调用 `guru-maintain-requirements-design-test-ssot:task_impact_sync`。`sync_required` 只进入 target-authored `promotion`；`revision_required` 回当前 planning/implementation owner；`baseline_incomplete` 回 Bootstrap/repair；`blocked` 停止。并行 task 默认写 `docs/requirements-design-test-contributions/<task-ref>/`，不直接竞争 shared current。

## Freshness

每次 gate 必须重读三个 README 的 current locator/version/status、Architecture public identity、live task delta 和 source binding。locator 不存在、版本不一致、traceability 断裂或 projection 落后时，不得沿用本页，进入 owner `repair`。正式 predecessor `v0.6.15-guru.6` 与 target `v0.6.16-guru.1` / extension `0.6.16-guru.41` publication identity 不得覆盖 current knowledge identity；`.48` promotion 也不证明 tag、Release 或 smoke 已完成。
