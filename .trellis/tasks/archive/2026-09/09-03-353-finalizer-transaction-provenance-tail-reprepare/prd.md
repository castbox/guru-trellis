# #353 修复 Finalizer 旧 transaction 遇到新 provenance tail 时的受支持 reprepare/rebind

## Goal

为正常恢复场景提供一个明确、可验证且幂等的 Finalizer reprepare/rebind 路径：旧的、未绑定 PR 的 `ordinary_publication/push_content` transaction 在 task、repository、base branch、head branch、close scope 仍一致，且当前 branch/remote/唯一 Open PR 已推进到一个合法 provenance metadata tail 时，不再错误返回 `provenance_tail_transaction_rebind_invalid`，而是返回并消费受支持的 `reprepare_required` 或等价的 current-plan recovery。

## Confirmed Facts

- Issue #353 为当前独立修复范围；#333、#342、#344、#347、#350 只作为 related boundary，不在本 task 修改或关闭。
- 当前 `classify_provenance_tail_transaction_rebind()` 已严格校验 provenance tail，但在旧 ordinary transaction 与新 tail 的组合恢复中仍可能同时产生 `provenance_tail_changed_paths_invalid`、`provenance_tail_parent_mismatch`，最终进入 `provenance_tail_transaction_rebind_invalid`。
- #342 已建立 direct-tail transaction rebind；#344/#347 已建立 base-evolution 与合法单 tail 的组合；#350 已允许特定组合中的 Publication metadata 演进。#353 只补足旧 transaction 需要重新准备 immutable plan 的入口与绑定语义。
- Finalizer contract 要求 provenance tail 的 allowlist、direct-parent、business-drift、multi-tail、live PR/remote identity 和 scope 校验继续 fail closed。

## Requirements

1. 当旧 transaction 是精确的、未绑定 PR 的 `ordinary_publication/push_content`，且当前合法 tail 只改变 provenance metadata 时，依据 current live Publication authority 重建 current-plan recovery transaction。
2. 只有 task/repository/base branch/head branch、reviewed content、close-Issue scope、Publication lineage、PR/remote identity 和 archive state 均保持合法时，才允许 `reprepare_required` 或 same-plan recovery；任何 authority 或 scope 漂移必须回到新的 Publication review或 fail closed。
3. provenance tail 必须先通过现有 `provenance_tail_commit_errors()`；不得放宽 changed-path allowlist、manifest allowlist、direct-parent、business delta、multi-tail 或 base-evolution binary-delta 规则。
4. reprepare preview 必须 side-effect-free；不得重复 push、PR 创建、PR edit、archive、archive push、Ready 或 Issue mutation。
5. execution 必须在首个剩余外部 mutation 前写入 current-plan recovery transaction，并按现有 transaction engine 继续；同一 plan 重试不得重复已完成 mutation。
6. 保持 Finalizer public input/output、六个 typed exits、transaction schema 3.0、canonical/installed/dogfood/platform projection 的兼容性；若必须变更 schema 或 public exit，先停止并报告 scope change。

## Acceptance Criteria

- [ ] 真实 Git topology 能复现旧未绑定 ordinary transaction、当前单一合法 provenance tail、相同 task/branch/close scope；preview 返回明确 `reprepare_required` 或合法 same-plan recovery，不再返回现有 invalid blocker。
- [ ] reprepare 从当前 immutable Publication authority 建立 plan，并绑定当前 publication HEAD；不把旧 transaction 的 PR/title/body/plan 当作新的 authority。
- [ ] direct-tail、pure base-evolution、composed base-evolution plus tail 的既有合法路径继续通过；Publication metadata 演进只在已声明 topology 中收敛。
- [ ] business/extra-path/invalid-manifest/parent-mismatch/multi-tail/identity/scope/PR/remote/archive drift 均在首个 mutation 前 fail closed。
- [ ] execution 顺序证明 transaction-before-mutation；push、PR create、metadata edit、archive、archive push、Ready 各自最多一次；same-plan retry 不重复。
- [ ] canonical 与 installed package tests、真实 topology integration tests、all-platform projection parity、preset reapply、dogfood drift、sidecar-zero 和 `.new`/`.bak` zero 检查通过。
- [ ] fresh full-diff Branch Review 无未关闭 P0-P3 finding。

## Out Of Scope

- 不修改或吸收 #333，不修改 PR #337 或其 owner-private transaction。
- 不放宽 provenance allowlist，不支持多 tail、任意 Publication rewrite、人工 transaction 修补或删除旧 transaction。
- 不改变 public DTO、typed exit、transaction mode/stage 或引入 verifier/Release Gate/完整 Throwaway matrix。
- 不处理恶意伪造、TOCTOU、锁、压力竞态、跨平台原子性或额外 fault injection。

## Docs SSOT Plan

采用 `delta_first`：先建立 task-owned RDT contribution，再按实际行为变化更新 Finalizer canonical contract、直接命中的 workflow data-contract/quality spec，并通过 preset apply 同步 installed/dogfood/platform projection。若最终确认 public contract、schema 或 architecture boundary 无变化，保留明确的 no-change 结论而不制造无效 ADR。

## Open Questions

无阻塞性用户决策。技术实现选择由 Phase 1 规划与 Phase 2 语义检查根据当前代码和 live topology 确定。
