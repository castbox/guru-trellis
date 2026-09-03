# #335 Repository-private release orchestration Architecture contribution

## Identity And Authority Boundary

- candidate identity：`architecture-contribution-335-repository-private-release-orchestration-v1`。
- source authority：live Issue #335 与 task `prd.md`。
- planning authority：task `design.md` 与稳定 `implement.md`。
- RDT behavior authority：`docs/requirements-design-test-contributions/335-release-guru-trellis-version/`
  的 `requirements.md`、`design.md`、`test.md` 与 `traceability.md`。
- current baseline：`docs/architecture/README.md` / `current-main-0.6.5-guru.42` / `active`。
- design constitution：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `current`。
- project change contract：`docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1` / `guru-trellis-architecture-change-concerns-v1`。
- change path：`target_native`；ADR required：`false`。

本 contribution 只定义稳定目标边界。它不记录 task HEAD、执行阶段、Gate 结果、finding closure、tag、smoke、Release、Issue closure、时间或用户授权，也不自行声明 review、promotion 或 current 状态。

## Boundary And Decision

当前仓库已经具备 standard intake、Phase 2、Task Commit、Branch Review、Publication、Finalizer、Merge、reviewed-content identity 与 exact-candidate release checks，但缺少一个只服务 `castbox/guru-trellis` 的正式发布编排入口。历史 release task 将 release notes、动态 checklist 和 lifecycle 结果写入 tracked task，可能在最终内容 Review 后继续制造 metadata commit，并使先前 Review identity stale。

目标边界新增 project-local `release-guru-trellis-version` Skill：

- preparation 阶段只组合现有 task lifecycle owners；
- merge 后重新冻结 `origin/main` exact candidate，并执行 release-specific gates；
- PR 与 Release payload 在相应副作用前由 live authority 即时生成和语义审查；
- release lifecycle 状态只存在于当前对话、live provider facts 和既有 owner-private runtime；
- repo-private Skill 不进入 Guru Team public package、marketplace、preset 或业务仓库 installed projection。

该决策不改变公共 Skill I/O、typed exits、global workflow phase order、Finalizer transaction、Merge owner 或 reviewed-content algorithm，因此不创建 ADR。

## Stage And Freshness Model

- preparation candidate 由 task worktree 中的实际交付、私有 Skill、durable contribution 和 tests
  构成；最终内容 commit 后由现有 Branch Review owner 对完整 base diff 做一次独立审查。
- Publication 与 Finalizer 继续消费各自现有最小 handoff。owner-private checkpoint、允许的
  lifecycle metadata 及其退休不进入 reviewed delivery identity，因此不会制造 tracked
  release-status commit 或二次内容 Review。
- preparation merge 后必须 fresh fetch `origin/main`，由 live merge/base facts 冻结新的 exact
  candidate；preparation HEAD、旧 Review、旧 Publication 和旧 release evidence 全部失效。
- Skill、source、durable docs、配置、schema、scripts 或 tests 发生变化时，受影响 gate stale 并
  回到对应 owner；cross-SHA、lineage gap、FAIL、SKIP 或未闭合 exit 均停止。

## Required Concerns

| Concern | Applicability | #335 stable contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | 绑定 Architecture 2.0、active `.42`、Issue #335 与 project change contract v1 |
| `constitution-binding` | `applicable` | 命中成熟扩展面、职责内聚、最小复杂度和单向收敛；不复制原则正文 |
| `boundary-and-decision` | `applicable` | `target_native` 新增 repo-private orchestration，不新增公共 workflow path |
| `owner-and-single-writer` | `applicable` | release Skill 只编排；现有 Phase 2/Commit/Review/Publication/Finalizer/Merge owners 继续单写各自结果 |
| `compatibility-and-exit` | `applicable` | 不建立 legacy adapter 或双读；现有 owner exits 原样消费，unknown/multiple/unmapped fail closed |
| `gap-and-deviation` | `applicable` | 关闭 release orchestration 缺口，不改变现有 Architecture GAP lifecycle 或 Release Gate ownership |
| `parallel-scope` | `applicable` | #335 只写本 contribution、私有 Skill、投影、测试和必要 docs；不接触 #332 或 shared current |
| `evidence-and-freshness` | `applicable` | delivery/Skill/durable/config/schema/script/test bytes 变化使 gate stale；owner-private lifecycle metadata 不改变 reviewed content identity |
| `review-and-promotion` | `applicable` | contribution 随 task 完整 diff 接受独立 Review；shared current 是否更新由现有 Architecture owner 串行决定 |

## Owners And Single Writers

- repository release orchestration owner：`release-guru-trellis-version`，只拥有 release-specific stage classification、fresh candidate freeze、gate composition 和动作边界。
- task lifecycle owners：standard intake、Phase 2、`guru-create-task-commit`、`guru-review-branch`、`guru-review-task-publication`、`guru-finalize-task`、`guru-merge-task-pr`，职责不变。
- release mutation owners：tag、tag-pinned smoke、GitHub Release、Issue closure 和 cleanup 各自保持独立动作与确认，不由一个持久化状态机合并。
- task writer：`335-release-guru-trellis-version` worktree。
- shared-current writer：仅现有 Architecture/RDT promotion owner；本 contribution 不是 shared current 写入授权。
- RDT contribution writer：当前 task 只写
  `docs/requirements-design-test-contributions/335-release-guru-trellis-version/`；RDT 与 Architecture
  是否 promotion 由两个现有 owner 串行判断。

## Before And After

- before：release 任务需要临时组合多个 owners，tracked planning/release metadata 容易与 reviewed delivery content 混合。
- after：一个无状态 repo-private Skill 固定 preparation 与 post-merge candidate 两阶段，并把所有生命周期证据留在现有 owner-private/live 边界；最终内容 commit 后一次完整 Branch Review 可直接进入 Publication 与 Finalizer。
- preserved：21 个公共 Guru Skill、公共 exits、marketplace/preset/installed graph、Finalizer/Merge transaction、版本轴和专门 Release Gate 矩阵 ownership。

## Project Check Contract

使用 `guru-trellis-architecture-convergence:repository:1` / `guru-trellis-architecture-convergence@1`，绑定 `ARCH-GOV-006..008`、`ADR-005`、`ARCH-GAP-006`。各 lifecycle stage 必须根据当前 task candidate 或 exact committed range 重新检查：authority/path 唯一、required concerns 完整、RDT traceability 闭合、无公共 package 泄漏、无 dual writer、无 tracked release-status loop、delivery drift 正确 stale、contribution/必要 promotion freshness 当前。

实现和验证证据由 Phase 2、独立完整 Branch Review 及后续 owner 在各自阶段即时读取。本文件不保存这些动态结果。

## Explicit Boundaries

- 不发布 `v0.6.15-guru.5`，不创建、移动或删除 tag/GitHub Release。
- 不修改、关闭、归档、清理或复用 Issue #332 的任何工作资源或证据。
- 不修改 Trellis upstream、全局 npm、`node_modules`、业务仓库或完整累计多平台 Release Gate 矩阵。
- 不把 repo-private Skill 提升为公共 `guru-*` workflow Skill，不新增 public schema、typed exit、runtime state machine 或 marketplace/preset projection。
