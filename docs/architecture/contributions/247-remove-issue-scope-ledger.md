# #247 Issue Scope Ledger retirement Architecture contribution

## Identity And Authority Boundary

- identity：`architecture-contribution-247-remove-issue-scope-ledger-v1` / `reviewed_promoted`。
- current authority：live Issue #247 `2026-09-13-r24`、current task planning 与 #247 RDT contribution。
- promotion input：immutable `current-main-0.6.5-guru.49`；current successor：active `.50`。
- change path：`dedicated_refactor_slice`；ADR：accepted `ADR-009`。

本 contribution 只删除 Issue Scope Ledger 并保持旧 lifecycle 端到端兼容。不恢复 #305，不实现
Refs-only、no-archive、active-task multi-Delivery、future Completion/Cleanup owner 或 #398 global graph。

## Boundary And Decision

before：Workspace、Planning/qualification、Commit/Review、Publication/Finalizer/Merge、Finish/Restore 和
installed validation 通过 task-local ledger 或 Issue arrays 交换跨阶段 authority。

after：ledger writer、reader、schema registration、aggregate DTO 与 ledger-only assets退出 current graph。
task identity来自 official task/Git/worktree/mapping；current semantic owners fresh 读取 requirement/source；
Publication 保留现有 reference/closing 判断；Finalizer 保留 preparation、push、PR、archive、Ready、handoff
和 recovery；Merge 保留 readiness、expected-head、closure verification 和四 exits；task-content finding
继续进入 archived Restore。legacy ledger inert，不迁移或读取。

选择 `dedicated_refactor_slice`，因为 r24 要求行为/API/规则、producer/consumer、edge、target/stop 与时点
保持不变，只收敛 ledger technical authority。无 ledger compatibility layer，也不创建未来 lifecycle owner。

## Required Concerns

| Concern | #247 r24 contract |
| --- | --- |
| authority-binding | 绑定 live r24、current planning、active `.50` 与 project contract v1。 |
| constitution-binding | 概念完整、职责隔离、最小复杂度、技术债单向收敛；constitution identity不变。 |
| boundary-and-decision | `dedicated_refactor_slice` 删除 aggregate，保留旧行为与 public graph。 |
| owner-and-single-writer | Publication、Finalizer、GitHub、Merge 各保留 current owner；不新增第二 writer。 |
| compatibility-and-exit | 同版本旧流程完整；ledger reader/adapter/dual-read 为零；四 Merge exits 与 Restore 保留。 |
| gap-and-deviation | `ARCH-GAP-008` 只关闭 ledger authority debt；提前归档/多 PR 局限继续作为未来工作。 |
| parallel-scope | 只写 #247 task/contribution/current `.50` 和直接投影，不修改其它 Issue。 |
| evidence-and-freshness | active-zero、legacy inert、old-flow E2E、capability、package/install/platform 与 full diff。 |
| review-and-promotion | r24 使旧 target-native gates stale；corrective candidate 必须 fresh Phase 2/commit/review。 |

## Owners And Single Writers

- task/workspace identity：official Trellis metadata、live Git/worktree 与 ignored mapping。
- requirement/scope/source reference：Phase 0 与 Planning semantic owners。
- PR payload/closure decision：Publication semantic owner，保留 close/reference-only/no-Issue paths。
- publication transaction：Finalizer 保留 current push/PR/archive/Ready/handoff/recovery。
- merge/result：Merge 保留 independent review、confirmation、expected-head、live closure verification 与四 exits。
- closure action：GitHub closing-keyword behavior；workflow 不调用 Issue close API。
- recovery：`guru-restore-archived-task` 只处理 current declared archived residue。
- shared current writer：serialized Architecture/RDT owner；task writer只写 #247 worktree。

## Project Check And Evidence State

此前基于 r19 `target_native` 的 Architecture、qualification、Phase 2、Branch Review 与测试结果只保留为
历史过程证据。live r24 已改变 implementation authority，因此这些 gate 对 current corrective diff stale。

r24 fresh gate 必须证明：

- 23 Skills / 97 exits / 78 commands、workflow invoke/exit/target/stop 与旧 success/recovery semantics不变；
- ledger writer/reader/precondition/registration/aggregate consumer为零，无 alias/hidden aggregate；
- Finalizer archive/Ready、Merge closure verification/four exits、archived Restore 在无 ledger 时可运行；
- `guru-ledger-free-runtime@1.0.0` canonical/installed projection一致；
- installed production wrappers 从无 task/无 ledger 到 current terminal 的代表性链路通过；
- migration precondition 未发现当前 #247 外依赖 ledger 的 active task 或 in-flight invocation。

## Known Limitations And Boundaries

- 旧流程提前归档、PR 冲突与同一 task 多 PR 接续局限未解决。
- 不迁移或 backfill historical/legacy ledger-bound task；不删除 inert legacy data。
- 不新增 public Skill、future lifecycle DTO、migration stop、global graph 或固定 Issue 依赖链。
- 不执行 commit、push、PR、merge、Issue close、tag、Release、Finish/archive current task 或 Cleanup。
- 完整多平台 exact-candidate Release matrix 与生产业务验证由 Release owner 后续执行。
