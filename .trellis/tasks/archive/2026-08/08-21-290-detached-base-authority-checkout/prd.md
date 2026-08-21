# #290 Codex detached checkout 下 base authority checkout 路由

## 目标

修复 `guru-sync-base` 把 Codex session checkout 直接当作 base 同步 authority 的组合缺陷。标准 Intake 中 session checkout 可处于 detached HEAD；选定 `selected_base` 后，只使用同一 Git common-dir 中绑定该 base branch 的 clean checkout 完成 fetch、fast-forward 与三向一致性验证。

本 task 只交付 `castbox/guru-trellis#290`。`#267` 的 Release Gate、tag、GitHub Release 和累计多平台发布矩阵不在本 task 中执行；`#283` 只作为历史复现背景，不继承其 review 或 checkpoint。

## 当前问题

当前 resolver 在 session checkout 上读取 symbolic branch 并要求 checkout clean；executor 随后要求该 branch `== selected_base`。正常 Codex detached worktree 因没有 symbolic branch，在 Issue/Docs/code/tests/history 读取前即返回 `blocked`，即使同一 repository 已存在唯一 clean `main` checkout。

这混淆了三种身份：

- Codex session checkout：调用外壳，detached HEAD 合法；
- base authority checkout：绑定 `refs/heads/<selected_base>`，负责同步和 fresh equality；
- Trellis task workspace：仅由后续 workspace gate 创建并承载 task change。

## 需求

- `R290-01`：base selection 必须保持固定优先级：显式 `base_branch`、config scalar、ordered existing candidate、remote default。
- `R290-02`：current branch 和 worktree availability 不得参与 base selection，也不得改变已选 base。
- `R290-03`：selected base 确定后，resolver 必须从同一 Git common-dir 的 registered worktrees 中查找绑定 `refs/heads/<selected_base>` 的 checkout。
- `R290-04`：session checkout 处于 detached HEAD 时继续处理；其 branch 不再作为 base authority 判断输入。
- `R290-05`：authority checkout 缺失、dirty、branch/HEAD/ref identity mismatch 时必须稳定 `blocked`，不得回退到其他 base。
- `R290-06`：authority checkout 已是当前 session checkout 时保持现有成功路径。
- `R290-07`：执行阶段的 Git mutation 集合仅包含 explicit refspec fetch 和 `merge --ff-only`；不得 checkout、switch、创建 branch/worktree、reset、rebase、stash 或 force update。
- `R290-08`：resolve、execute、validator 必须共享同一 selection/binding resolver 和同一 pre/post digest freshness 链。
- `R290-09`：成功后必须满足 authority checkout HEAD `==` local selected-base ref `==` remote-tracking ref，且 authority checkout clean。
- `R290-10`：`base_current.repo_locator` 必须指向实际 authority checkout；`synced`、`skipped`、`blocked` 及 downstream transition 保持兼容。
- `R290-11`：canonical package、dogfood installed package、Shared/Codex/Claude/Cursor 投影与 preset overlay 必须一致，reapply 后无 drift。
- `R290-12`：fresh equality 成立前不得读取 Intake authority 或创建 Issue、branch、worktree、task。

## Acceptance

- `AC-01`：显式 `release/1.3.0` 时，即使存在 clean `main` checkout，也只查找 `release/1.3.0` checkout。
- `AC-02`：config scalar `release/1.3.0` 保持与显式 base 相同的 selection/binding 语义。
- `AC-03`：`dev` 与 `main` 同时存在时先选 `dev`；缺少 `dev` checkout 时 blocked，不回退 `main`。
- `AC-04`：detached session + 唯一 clean selected-base checkout 可完成同步并把 authority path 投影给 Discovery。
- `AC-05`：selected-base checkout missing、dirty、branch/HEAD/ref mismatch 各自 fail closed。
- `AC-06`：session checkout 本身正确绑定 selected base 时继续通过。
- `AC-07`：behind-base 只执行 explicit fetch + `merge --ff-only`，同步后通过三向 equality。
- `AC-08`：base result schema、三个 typed exit 和 downstream transition 字段保持兼容；如实现证明无法兼容，必须先返回 planning revision，不能静默改 API。
- `AC-09`：package contract/runtime/unit/eval、canonical/dogfood/installed/platform projection、preset reapply/drift 全部通过。
- `AC-10`：完成一个代表性 Codex detached worktree 正常路径验证；该验证不是 #267 累计 Release Gate。
- `AC-11`：最终仓库不存在 `.new`、`.bak` 或 unknown sidecar。

## 非目标

- 不让 detached session checkout 直接承担 base 同步。
- 不根据现有 worktree 猜测或重选 base。
- 不自动创建或切换 base branch/worktree。
- 不修改业务 repository。
- 不扩展到恶意伪造、锁、TOCTOU、竞态压力、跨 OS crash-hardening。
- 不开始 `#267`，不发布 tag 或 Release。

## Docs SSOT Plan

- `strategy`: `delta_first`。
- Phase 2 在 `docs/requirements-design-test-contributions/290-detached-base-authority-checkout/` 创建 task-isolated Requirements/Design/Test/traceability delta，绑定 `BEH-001`、`DES-004`、`DES-008` 与本 task 的测试场景。
- Architecture 采用 `target_native`。Planning 已创建 task-owned contribution `docs/architecture/contributions/290-detached-base-authority-checkout.md`，记录三种 checkout identity、单一 base authority、before/after 和项目检查；该变更形成新的架构边界决策，ADR candidate 为 `docs/architecture/adr/006-base-authority-checkout-routing.md`。
- 普通实现阶段不直接编辑 shared current Requirements/Design/Test/Architecture authority。Phase 2 和 committed full-diff Branch Review 通过后，分别由 RDT `promotion` 与 Architecture `promotion` 串行更新 current；promotion diff 必须重新经过 fresh Phase 2、task commit 和独立 Branch Review。
- `.trellis/spec` 只在实现证明存在可复用契约缺口时做最小同步；不得把 active task 状态投影进 spec template。
- `#267` 的 release matrix、tag-pinned evidence 与发布文档保持 follow-up，不在本 Docs SSOT Plan 中执行。
