# Requirements / Design / Test SSOT 使用规则

## Current identity

- version：`current-main-0.6.17-guru.89`
- status：`active`
- Requirements / Design / Test：各层 `docs/**/README.md` 指向 `.89`，完整薄继承 immutable `.88` 并承接 reviewed #530 contribution。
- Architecture inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.86` / `active`。
- 结果 authority：`docs/requirements-design-test-contributions/530-clean-committed-reentry/test.md`；scope-required 分层结果、历史失败及未验证边界只由唯一 Test 拥有；晋升差异须 fresh Phase2/TaskCommit/不同 reviewer 完整 BranchReview。
- 双向 trace：`R530/BEH530 -> D530/CON530 -> T530`，durable canonical/contribution locators 拥有长期正文，不依赖 active Task 移动路径。

## Immutable .88 predecessor provenance

- version：`current-main-0.6.17-guru.88`
- status：`superseded`
- Requirements / Design / Test：各层 `docs/**/README.md` 指向 `.88`，完整薄继承 immutable `.87` 并承接 reviewed #292 contribution。
- Architecture inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.85` / `active`。
- 结果authority：`docs/requirements-design-test-contributions/292-unique-planning-author/test.md`；scope-required分层结果、历史失败及未验证边界仅由唯一Test拥有。晋升差异须fresh Phase2/TaskCommit/不同reviewer完整Branch；Delivery、Publication、Merge、Completion、Closure、Finish和Release各由原owners判断。
- Planning source identity：TaskId `292-unique-planning-author` / generation `0`；documents `prd.md`、`design.md#D2/#D9/#D10`、`implement.md#V1–V8`。长期合同与双向trace使用durable canonical/contribution locators，不依赖active task位置。

## Immutable .87 predecessor provenance

- version：`current-main-0.6.17-guru.87`
- status：`superseded`
- Requirements / Design / Test：各层 `docs/**/README.md` 指向 `.87`，薄继承 immutable `.86` 并承接 reviewed #535 contribution。
- Architecture inheritance：`docs/architecture/README.md` / `current-main-0.6.17-guru.84` / `active`。
- 结果authority：`docs/requirements-design-test-contributions/535-review-zero-candidates/test.md`；分层实际结果、首次失败与未验证边界由该文件拥有。晋升差额须fresh Phase2/TaskCommit/独立完整Branch；Delivery、Completion/Closure/Finish、#292恢复和Release独立。

## Predecessor identity and provenance

- version：`current-main-0.6.17-guru.77`
- status：`historical`
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

每次 gate 重读三个 README 的 current locator/version/status、Architecture public identity、live task delta 与 source binding。缺失/冲突/trace断裂/projection落后进入原 owner repair。当前 RDT `.89` 薄继承 immutable `.88`，承接 R530/BEH530、D530/CON530、T530 增量，Architecture 继承 `.86/active`。软件四轴与知识版本独立；前驱历史身份及证据保持不可变。当前晋升diff须fresh Phase2/TaskCommit/独立完整BranchReview；Publication、merge、Completion、Closure、Finish及Release分别由原owners判断，不由知识晋升推定。
