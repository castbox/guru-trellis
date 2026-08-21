# #290 Architecture contribution

## Candidate identity and authority boundary

- candidate identity：`architecture-contribution-290-base-authority-checkout-v1`。
- source authority：Issue #290、`BEH-001`、`DES-004`、`DES-008`。
- serialized promotion source authority（gate 时）：`docs/architecture/README.md` /
  knowledge identity `current-main-0.6.5-guru.38` / `active`。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` /
  `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` /
  `guru-trellis-architecture-change-contract-v1` /
  `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；promotion state：`reviewed_promoted`；本 contribution
  已由 expected `.38` serialized promotion 纳入 `.39` CURRENT authority。
- expected current identity：`current-main-0.6.5-guru.38`。shared current 仅由
  Architecture promotion owner 在 independent committed full-diff review 后更新。

## Boundary and decision

Current boundary 把 Codex session checkout 同时用作 invocation shell 与 selected-base
decision checkout。detached session 没有 symbolic branch，因此即使同一 Git common-dir
存在 clean selected-base checkout，standard Intake 仍在 authority 读取前失败。

Target boundary 固定拆分为三种 identity：

1. session checkout 只承载调用，允许 detached；
2. base authority checkout 绑定 `refs/heads/<selected_base>`，独占 fetch、
   `merge --ff-only`、clean 与三向 equality；
3. Trellis task workspace 仅由后续 workspace gate 创建并承载 task change。

Base selection 先按 explicit、config scalar、ordered existing refs、remote default
确定 `selected_base`；authority binding 随后只在同一 common-dir 的 registered
worktrees 中查找该 exact branch。worktree availability 不参与 selection，binding
失败也不触发 fallback。

该边界由 ADR candidate
[`ADR-006`](../adr/006-base-authority-checkout-routing.md) 记录。它不引入 legacy
authority、dual-read、adapter 或第二套 resolver。

## Required concern review

| Concern | Applicability | #290 contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | 同时绑定 `guru-maintain-architecture-baseline:2.0`、`.38` baseline 与项目 change contract v1 |
| `constitution-binding` | `applicable` | 命中 `concept-semantic-completeness`、`cohesion-change-isolation`、`minimum-necessary-complexity`、`debt-one-way-convergence`；不复制原则正文 |
| `boundary-and-decision` | `applicable` | `target_native` 建立 session、base authority、task workspace 三种 identity 与 selected-base-first 决策 |
| `owner-and-single-writer` | `applicable` | `guru-sync-base` deterministic runtime 是 selection/binding/sync owner；task writer 是 `290-detached-base-authority-checkout`；shared current writer 是 promotion owner |
| `compatibility-and-exit` | `applicable` | public schemas 与 `synced/skipped/blocked` exits 不变；旧 session-branch coupling 在本 task 删除，不保留 dual-read |
| `gap-and-deviation` | `applicable` | 关闭 Issue #290 的 detached normal-path routing gap；不修改 `ARCH-GAP-001..006`，不承担 #267 |
| `parallel-scope` | `applicable` | 仅写 #290 worktree、canonical package、managed projection 与 task-owned contributions；禁止 review 前修改 shared current |
| `evidence-and-freshness` | `applicable` | Phase 2 绑定 complete candidate；Branch Review 绑定 `origin/main...HEAD` committed range；package/runtime/eval、projection、reapply/drift 与一个 detached wrapper 路径分别提供证据 |
| `review-and-promotion` | `applicable` | 本 contribution 与 ADR 先保持 candidate；independent review 后按 expected `.38` identity promotion，promotion diff 重新进入 Phase 2、commit 与 Branch Review |

## Before and after

- before：resolver 从 session checkout 读取 symbolic branch 并把它当作 decision
  checkout；detached session 返回 `blocked`。
- after：resolver 先选 base，再绑定同一 common-dir 的 exact branch checkout；
  execute/check/public handoff 全部使用该 authority root，detached session 只保留调用职责。
- preserved：selection precedence、explicit refspec fetch、ff-only、freshness chain、
  public schema、typed exits 与 downstream consumer shape。
- affected consumer：`guru-create-task-workspace.reviewed_base_freshness` 继续作为既有
  freshness consumer，按 producer provenance `source` 对 explicit/config/
  config-candidate/remote-default 的 current authority、selected base 与完整 candidates
  做 package-local exact revalidation；`prepare()` 不在 freshness 前重跑 config-only
  selection，也不导入 producer private runtime。这是既有边界的一致性修复，不新增
  public resolver、架构决策或 owner。

## Project check

- descriptor：`guru-trellis-architecture-convergence:repository:1` /
  `guru-trellis-architecture-convergence@1`。
- refs：`ARCH-GOV-006..008`、`ADR-005`、`ARCH-GAP-006`。
- Planning evidence：Issue #290、task `prd.md` / `design.md` / `implement.md`、本
  contribution 与 ADR-006 candidate。
- Planning result：`pass`。当前计划完整选择一个 path、一个 runtime owner、一个
  task writer 与一个 promotion owner；没有新增 legacy authority、dual writer 或
  closed GAP regression。
- Phase 2、Branch Review、Publication 与 Acceptance/Finish 必须基于各自 fresh
  candidate/range 重新执行，不复用本 Planning result。
- Implementation discovery：explicit override 与 remote-default downstream mismatch 经
  `guru-qualify-normal-scenario:phase2_candidate_set` 判定为 `qualified_current`；fresh
  Architecture impact sync 保持 `target_native` / `reviewed_candidate`，没有 owner、DTO、
  persistence、SDK、external 或 shared-current scope 扩张。
- Phase 2 cross-package evidence：workspace package 覆盖 explicit override、ordered
  `dev -> main` 与 remote-default normal paths；sync-base detached transitions 直接进入
  freshness consumer 并断言 `fresh` / `three_way_equal`。
- Fresh Phase 2 implementation result：canonical/installed workspace `6/6`、sync-base
  `15/15`、package integration `8/8`，source/installed validators、reapply、drift、
  projection equality 与 sidecar-zero 均通过；independent `trellis-check` 对完整 current
  candidate 给出 P0-P3 无 findings，observations 01/02/03 均不再复现。

## Promotion result

完整 task range `origin/main@ec4df880…d4165f26` 已通过 independent Branch Review，
Architecture project check 为 `pass`，open findings 为零。serialized promotion 绑定
expected `.38` 与 contribution pre-promotion SHA-256 `53c3e44a5b62d1c446d0534c9f55777014e99949ea56bd370d15af020946b0f7`，
激活 successor `.39`。promotion-created diff 必须 fresh 重走 Phase 2、commit 与 Branch
Review。promotion 不开始 #267，不创建 tag/Release，也不把发布矩阵写成 #290 completion evidence。
