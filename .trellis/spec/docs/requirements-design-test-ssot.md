# Requirements / Design / Test SSOT 使用规则

## Current identity

- version：`current-main-0.6.17-guru.72`
- status：`active`
- Requirements：`docs/requirements/README.md`
- Design：`docs/design/README.md`
- Test：`docs/test/README.md`
- Architecture inheritance：`docs/architecture/README.md`，`current-main-0.6.17-guru.72` / `active`
- source binding：reviewed #495 migration candidate contribution + explicit immutable `current-main-0.6.17-guru.71` inheritance promoted to `current-main-0.6.17-guru.72`；current registry 为 35 active Skills / 159 exits / 106 commands，零 planned IDs；migration standalone-only，business workflow 保持 33 mandatory invokes / 153 exits。fixed Fork source 为 `8868c47c45fa1a9fa8f60fe30d641f70ff5c6ba1`，CLI/core `0.7.0-castbox.2`，Guru `0.7.0-guru.2` 是未发布候选。Architecture 增量见 `ARCH-CUR-049` / `ARCH-DOM-034` / `ARCH-INT-037` / `ADR-017` / open `ARCH-GAP-012` / `EVD-048`；`.71` 的 #490 与更早有效合同保持 immutable inheritance。promotion-created diff 须 fresh Phase 2/commit/不同 reviewer 完整 Branch Review；本地候选知识不证明 same-remote-HEAD `source_locked`/marketplace/preset provider、完整 `MIG-495-06`、merge/Completion、软件发布、真实业务安装或完整多平台 Release matrix。
- Finalizer recovery mapping：`FIN454-C4-P1-004` 不创建新 RDT identity；它继续映射 `REQ-048 -> DES-046 -> TST-032/SCN-044`，以同一 unbound transaction、合法 predecessor tail、selected-base lineage、current review/Publication/live HEAD equality、无 Open PR 与 transaction-owned remote endpoints 构成最小充分绑定。

## 读取与更新

依序读 Requirements -> Design -> Test -> Architecture，并通过 `REQ/BEH -> DES/CON -> TST/SCN/CASE -> ARCH/EVD` identity 跟踪，不复制 source prose。

普通 task 先调用 `guru-maintain-requirements-design-test-ssot:task_impact_sync`。`sync_required` 只进入 target-authored `promotion`；`revision_required` 回当前 planning/implementation owner；`baseline_incomplete` 回 Bootstrap/repair；`blocked` 停止。并行 task 默认写 `docs/requirements-design-test-contributions/<task-ref>/`，不直接竞争 shared current。

## Freshness

每次 gate 必须重读三个 README 的 current locator/version/status、Architecture public identity、live task delta 和 source binding。locator 不存在、版本不一致、traceability 断裂或 projection 落后时，不得沿用本页，进入 owner `repair`。软件四轴与 current knowledge identity 独立；`.72` candidate knowledge 不证明 promotion-created diff 之后的 fresh Phase 2、Task Commit、完整 Branch Review、Publication、push、PR、merge、tag、Release 或 Issue closure。`R495/D495/T495` current delta 与双向 trace 在三层 `.72` authority 定义；`R490/D490/T490` 沿 immutable `.71` 明确继承；`R481/D481/T481` 沿 immutable `.70` 明确继承；`.69` 的 `R467/D467/T467`、`R454-G7/D454-G7/T454-G7`、`R434/D434/T434` 与 C2-C7/D443/D436 作为 inherited history 保留。`ARCH-GAP-012` 保持 open，全部 `MIG-495-01..09` 最终验收仍属于同一任务；知识晋升不关闭迁移缺口。
