# #392 Release v0.6.16-guru.1 Architecture contribution

## Identity And Authority Boundary

- contribution identity：`architecture-contribution-392-release-v0616-guru1-v2` / `reviewed_promoted`。
- requirement authority：live Issue #392 与 task `prd.md`。
- behavior authority：task `design.md`、`implement.md` 与后续 `.48` RDT successor。
- source/expected predecessor：`current-main-0.6.5-guru.47` / `immutable superseded`。
- promoted successor：`docs/architecture/README.md` /
  `current-main-0.6.5-guru.48` / `active`。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；ADR required：`false`。

本 contribution 定义 #392 已 promotion 的稳定 identity 与目标边界。它不记录 task HEAD、
动态 gate 结果、tag、smoke、Release、Issue closure、时间或用户授权；promotion identity
不证明任何后续 gate outcome。

## Boundary And Decision

immutable `.47` 记录固定 Fork 来源、CLI `0.6.16` 与 extension
`0.6.15-guru.40` 的过渡状态；正式 predecessor 仍为 `v0.6.15-guru.6`。promoted
`.48` 将 current release-facing surfaces 统一到 `v0.6.16-guru.1` /
`0.6.16-guru.41`，但该 mapping 不证明后续发布 gate、tag 或 GitHub Release 已完成。

目标边界以 `target_native` 直接演进 current mapping：

- canonical、dogfood、installed manifest 与 current 文档/fixture/validator 同步切换到
  extension `0.6.16-guru.41`；
- Trellis CLI 保持 `0.6.16`，framework source 保持
  `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`；
- Architecture/RDT 从 `.47` 派生 `.48`，`.47` 仅转为 immutable superseded
  authority；
- repository-private release orchestration 四平台投影直接演进为 pre-promotion committed
  review、serialized promotion、post-promotion fresh committed review 的唯一 Stage 1 路径；
- preparation PR 合并后重新冻结 `origin/main` exact candidate，Release Gate、tag、
  tag-pinned smoke 和 GitHub Release 只消费该 identity。

该决策不新增公共 Skill、typed exit、schema、compatibility adapter、双版本 parser、
第二发布状态机或 task-local release lifecycle artifact，因此不创建 ADR。

## Required Concerns

| Concern | Applicability | #392 stable contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | 绑定 Architecture 2.0、immutable `.47` predecessor、active `.48` successor、Issue #392 与 project change contract v1 |
| `constitution-binding` | `applicable` | 命中概念完整、职责隔离、最小复杂度与单向收敛；constitution identity 不变 |
| `boundary-and-decision` | `applicable` | `target_native` 直接演进 current release mapping，并派生 `.48` knowledge authority |
| `owner-and-single-writer` | `applicable` | task worktree 写 contribution 和 delivery；Architecture/RDT promotion owner 单写 shared current；tag、Release、Issue close 各自独立 |
| `compatibility-and-exit` | `applicable` | current consumers 同步迁移，不保留 dual-read、fallback 或 adapter；历史 released/superseded facts 原样保留 |
| `gap-and-deviation` | `applicable` | 关闭 `.47` 过渡状态与目标 release mapping 的差距，不关闭既有独立 GAP 或扩大 runtime owner |
| `parallel-scope` | `applicable` | task 只写 #392 delivery、contribution 与 `.48` successor；promotion 前不直接竞争 shared current，且不修改 #378 历史证据 |
| `evidence-and-freshness` | `applicable` | planning、Phase 2、committed branch、post-merge exact candidate、tag 与 Release 各自绑定 fresh identity；cross-SHA、FAIL、SKIP 或 stale 均停止 |
| `review-and-promotion` | `applicable` | contribution 随完整 task diff 接受独立 review；serialized promotion 绑定 expected `.47`，promotion-created diff 再进入 fresh Phase 2/commit/Branch Review |

## Owners And Single Writers

- release orchestration owner：repository-private `release-guru-trellis-version`，只编排
  preparation 与 post-merge exact-candidate 阶段。
- task lifecycle owners：Planning、Phase 2、Task Commit、Branch Review、Publication、
  Finalizer 与 Merge owner 保持原职责。
- task writer：`392-release-v0616-guru1` worktree。
- shared-current writer：Architecture/RDT serialized promotion owners；本 contribution
  不是直接修改 shared current 的授权。
- release mutation owners：annotated tag、tag-pinned smoke、GitHub Release、Issue close
  和 cleanup 分别读取 live authority 并进入独立动作边界。

## Before And After

- before：active `.47` 与 current release-facing surfaces 仍包含 predecessor mapping 或
  #378 的非发布过渡状态；canonical extension 为 `0.6.15-guru.40`。
- after：`.48` 是唯一 active Architecture/RDT knowledge identity；current surfaces 唯一
  映射 `v0.6.16-guru.1` / `0.6.16-guru.41` / CLI `0.6.16` / 固定 Fork
  full SHA，`.47` 保持 immutable superseded。
- preserved：公共 Skill I/O、typed exits、global workflow、release owner 边界、Fork source、CLI version、
  historical releases、#378 evidence、业务仓库与 npm package 均不改变。

## Project Check Contract And Planning Result

- descriptor identity：`guru-trellis-architecture-convergence:repository:1`。
- check identity/version：`guru-trellis-architecture-convergence@1`。
- refs：`ARCH-GOV-006..008`、`ADR-005`、`ARCH-GAP-006`。
- Planning evidence：live Issue #392、task planning、active `.47` Architecture/RDT、
  canonical manifest/source lock、本 contribution 与 repository-private release contract。
- Planning result：`pass / blocking=true`。当前方案只有一个 task writer、一个
  serialized shared-current writer 和一个 `.48` successor；无 ADR、dual writer、
  compatibility layer、公共 API 扩张或新增/恶化 deviation。

serialized promotion 只消费本 contribution 的 Planning semantic review、pre-promotion
delivery 的独立 committed full-diff Branch Review 与 expected `.47`；promotion-created
delivery diff 随后必须重新进入 Phase 2、task commit 与独立 committed full-diff Branch
Review。post-merge Release Gate 再绑定 fresh exact candidate。本 Planning 结果不替代
任何后续 gate，也不证明 tag 或 GitHub Release 已发布。

## Review And Promotion Boundary

- promotion identity：`reviewed_promoted`；`.47` 为 immutable superseded predecessor，
  `.48` 为 promoted/current active shared authority。
- expected predecessor：`current-main-0.6.5-guru.47`。
- promoted successor：`current-main-0.6.5-guru.48`。
- ADR：`required=false`。
- serialized promotion 已基于 expected `.47` 建立 `.48` shared current；该稳定 promotion
  identity 不保存或替代当时的动态 review result。promotion-created diff 必须由后续 owner
  接受 fresh Phase 2、task commit 与独立 committed full-diff Branch Review；live current
  advance、finding、project-check failure 或 stale identity 必须返回对应 owner route，不得覆盖。

## Explicit Boundaries

- 不发布 npm package，不修改 Trellis upstream、全局 npm 或 `node_modules`。
- 不创建、移动、删除或重写历史 tag、GitHub Release 或 `main` history。
- 不隐式升级、部署或写入业务仓库、数据库、容器、Kubernetes 或生产基础设施。
- 不复用 #378 focused evidence 作为 #392 exact-candidate Release Gate 证明。
