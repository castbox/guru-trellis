# Requirements / Design / Test SSOT 使用规则

## Current identity

- version：`current-main-0.6.17-guru.83`
- status：`active`
- Requirements / Design / Test：各层 `docs/**/README.md` 指向 `.83`，薄继承 immutable `.82` 并承接 reviewed #396 contribution。
- Architecture inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.82` / `active`；当前任务独立 Architecture owner 判定 no-impact 时不产生 contribution/ADR，新 candidate 仍独立评估。
- 结果 authority：`docs/requirements-design-test-contributions/396-draft-intake-recovery/test.md`；objective/native/分发、fresh gates 与 lifecycle 独立，知识晋升不推定后续完成。

## Predecessor identity and provenance

- version：`current-main-0.6.17-guru.77`
- status：`active`
- Requirements：`docs/requirements/README.md`
- Design：`docs/design/README.md`
- Test：`docs/test/README.md`
- Architecture inheritance：`docs/architecture/README.md`，`current-main-0.6.17-guru.77` / `active`
- source binding：reviewed #466 constitution/consumption contribution + immutable `.76` inheritance + ARCH-CUR-050/EVD-053；35 active Skills/159 exits/106 commands，零 planned，migration standalone-only，business33/153。当前正式 Fork `5c760463680ffc10a3f26957b330c57a4b0c3ff8` / CLI/core `0.7.0-castbox.3` / CI `37735554354`，Guru `0.7.0-guru.3` 未发布候选；Architecture ARCH-CUR-049/ARCH-DOM-034/ARCH-INT-037/ADR-018/closed ARCH-GAP-012/EVD-052。EVD-052仅证明 #503 source/代表性 clean-installed 候选，不是 #500 最终 Release gate；#503 唯一增量结果见 `docs/requirements-design-test-contributions/503-mixed-task-identity-reservation/test.md`。全部正常 `v0.6.x-guru.*` 和 `v0.7.0-guru.*` 来源按实际差异分组；历史 #495 唯一结果见 `docs/requirements-design-test-contributions/495-upgrade-version-families/test.md`。历史 `.75` Fork `cc5f9a30652be29cffee9acc7e14d5dc5daaf04c` / CI `37647767799` 与 EVD-051仅绑定精确远端 `ecd152add05dbeb6df1873f0917ca3a62914ca7a` 的同源验收；`.74`/EVD-050本地及更早固定来源证据保留为历史，首次失败与恢复不改写，不声明业务原始在途。晋升diff须freshPhase2/commit/独立完整BranchReview，后继HEAD不冒充同源重跑，merge/Completion/Closure/Finish/Release/真实业务安装/完整矩阵仍由各owner判断。
- Finalizer recovery mapping：`FIN454-C4-P1-004` 不创建新 RDT identity；它继续映射 `REQ-048 -> DES-046 -> TST-032/SCN-044`，以同一 unbound transaction、合法 predecessor tail、selected-base lineage、current review/Publication/live HEAD equality、无 Open PR 与 transaction-owned remote endpoints 构成最小充分绑定。

## 读取与更新

依序读 Requirements -> Design -> Test -> Architecture，并通过 `REQ/BEH -> DES/CON -> TST/SCN/CASE -> ARCH/EVD` identity 跟踪，不复制 source prose。

普通 task 先调用 `guru-maintain-requirements-design-test-ssot:task_impact_sync`。`sync_required` 只进入 target-authored `promotion`；`revision_required` 回当前 planning/implementation owner；`baseline_incomplete` 回 Bootstrap/repair；`blocked` 停止。并行 task 默认写 `docs/requirements-design-test-contributions/<task-ref>/`，不直接竞争 shared current。

## Freshness

每次 gate 重读三个 README 的 current locator/version/status、Architecture public identity、live task delta 与 source binding。缺失/冲突/trace断裂/projection落后进入原 owner repair。当前 RDT `.83` 薄继承 immutable `.82`，承接 R396/D396/T396 增量，Architecture继承 `.82/active`。软件四轴与知识版本独立；前驱历史身份及证据保持不可变。当前晋升diff须fresh Phase2/TaskCommit/独立完整BranchReview；Publication、merge、Completion、Closure、Finish及Release分别由原owners判断，不由知识晋升推定。
