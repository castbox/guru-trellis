# #329 Developer-free Trellis adoption Architecture contribution

## Identity And Authority Boundary

- contribution identity：`architecture-contribution-329-developer-free-trellis-v1` / `reviewed_promoted`。
- requirement authority：live Issue #329、task `prd.md` 与 #329 RDT contribution。
- behavior authority：task `design.md`、`implement.md` 与 #329 RDT contribution。
- promotion input：`docs/architecture/README.md` / expected `current-main-0.6.5-guru.48`。
- promoted successor：`current-main-0.6.5-guru.49` / `active`；`.48` 为 immutable superseded predecessor。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` / `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；ADR required：`false`。

本 candidate 把 current framework/source/identity lifecycle 从固定 Fork `0.6.16` 直接演进到包含
developer/workspace retirement 的固定 `0.6.17` source。它遵循现有 official-extension、
subtraction-first、single-writer 与 minimum-complexity 决策，不改变原则、owner 模型或 compatibility
exception，因此不新增 ADR。

## Boundary And Decision

- before：`.48` current mapping 为 repository target `v0.6.16-guru.1`、extension
  `0.6.16-guru.41`、CLI `0.6.16`、framework source `ad332e3...`；stock task/context/platform runtime
  仍消费 developer identity、workspace journal/index、session recording 或 `--mine`。
- after candidate：framework source 为
  `castbox/Trellis@a2003296b4c4ce46c50d72ead3b2ec9c317f69fc`、CLI `0.6.17`、package manager
  `pnpm@10.32.1`；official generated runtime 与
  Guru controlled consumers 使用 task metadata、Git/worktree facts、runtime mappings 和 explicit caller
  authority；legacy identity/workspace data 原字节保留且不消费。
- preserved：Guru extension/repository release axis、23 Skills / 97 exits 业务图、task checkout/worktree
  authority、latest released tag `v0.6.16-guru.1`、historical releases/archives、upstream retired command
  migration stubs 与独立 release owner。`v0.6.16-guru.1` 不包含本 candidate。

## Required Concerns

| Concern | Applicability | #329 candidate contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | 绑定 Architecture 2.0、active `.48`、Issue #329、RDT candidate 与 project change contract v1 |
| `constitution-binding` | `applicable` | 命中成熟官方扩展、概念完整、职责隔离、最小复杂度与单向收敛；constitution identity 不变 |
| `boundary-and-decision` | `applicable` | `target_native` 直接采用 developer-free `0.6.17` source，不建立第二 identity authority |
| `owner-and-single-writer` | `applicable` | task worktree 写 delivery/contributions；serialized Architecture/RDT owners 单写 shared current |
| `compatibility-and-exit` | `applicable` | controlled consumers 同步迁移并删除旧 Guru runtime path；无 adapter、fallback、dual-read/write |
| `gap-and-deviation` | `applicable` | 关闭 #329 描述的 source/identity lifecycle delta；不重开既有 closed GAP，不新增 owner/deviation |
| `parallel-scope` | `applicable` | #329 只写隔离 delivery/contributions；promotion 前不修改 `.48` shared current |
| `evidence-and-freshness` | `applicable` | source build、generation、focused、installed matrix、legacy bytes 与 full diff 各绑定 current candidate |
| `review-and-promotion` | `applicable` | contribution 先随 delivery 接受 independent committed review，再绑定 expected `.48` serialized promotion；created diff 重过全部 gate |

## Owners And Compatibility Exit

- framework generation owner：fixed `castbox/Trellis@a2003296...` checkout 的 official CLI。
- Guru canonical owner：workflow/Skill/preset/runtime/installer/spec 各现有 owner，直接迁移其 controlled consumers。
- task writer：`329-adopt-developer-free-trellis` worktree。
- shared current writer：Architecture/RDT serialized promotion owners。
- compatibility exit：旧 Guru developer/workspace runtime consumer 在本 task 退出；upstream retired stubs、
  negative/preservation tests 与 immutable history 按其明确职责保留。没有长期 compatibility layer。

## Project Check Contract And Planning Result

- descriptor identity：`guru-trellis-architecture-convergence:repository:1`。
- check identity/version：`guru-trellis-architecture-convergence@1`。
- refs：`ARCH-GOV-006..008`、`ADR-005`、`ARCH-GAP-006`。
- Planning evidence：live Issue #329、task planning、active `.48` Architecture/RDT、current source lock、
  upstream `0.6.17` migration authority、current consumer inventory 与本 contribution。
- Planning result：`pass / blocking=true`。方案固定一个 framework source、一个 task writer、一个
  shared-current writer 和一个 direct-evolution path；无 dual writer、compatibility layer、原则例外或
  新增/恶化 deviation。

## Review And Promotion Boundary

- promotion state：`reviewed_promoted`；expected input：`current-main-0.6.5-guru.48`；current successor：
  `current-main-0.6.5-guru.49`。
- 本 contribution 不记录或证明 Phase 2、matrix、publication、merge、tag、Release 或 Issue closure；
  这些动态结果由各自 stage 的 fresh evidence owner 承接。
- serialized promotion 已在 contribution 与 delivery 通过 independent committed review 后建立 `.49`；
  promotion-created diff 必须重新进入 fresh Phase 2、Task Commit 与完整 Branch Review。
- implementation 若扩大 public graph、owner、persistence、SDK、external 或 compatibility boundary，
  本 Planning result 立即 stale 并重新进入 Architecture owner。

## Explicit Boundaries

- 不修改 castbox/Trellis、原始 upstream、全局 npm 或 `node_modules`。
- 不删除、迁移、规范化或重写用户已有 identity/workspace/index/journal/agent-trace 数据。
- 不创建 tag/GitHub Release，不修改历史 release/ADR/contribution 正文。
- 不引入 hostile-input、TOCTOU、锁、并发压力、分布式协调或额外 fault injection。
