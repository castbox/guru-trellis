# Architecture Change Contract

Identity：`guru-trellis-architecture-change-contract-v1`；状态：`current`；required concern set：`guru-trellis-architecture-change-concerns-v1`。本文件是本仓库 task-local Architecture change contract 与 project-check protocol 的项目 authority；Guru Team public package只定义可复用 shape 和 routes。

## Required concerns

| Concern | Required current meaning |
| --- | --- |
| `authority-binding` | 同时绑定 `guru-maintain-architecture-baseline:2.0`、current baseline 与本 change-contract identity |
| `constitution-binding` | 绑定 current constitution locator、status、version/content identity 与实际命中的原则 refs |
| `boundary-and-decision` | 记录 requirement/behavior authority、current/target boundary、decision/GAP refs 与唯一 change path |
| `owner-and-single-writer` | 明确 current/target semantic owner、task writer 与 shared-current promotion single-writer |
| `compatibility-and-exit` | legacy/adapter 适用性、owner、可验证退出与旧实现删除条件；`target_native` 不保留 dual-read |
| `gap-and-deviation` | 区分计划关闭、保留、新增和恶化的 GAP/偏移，并为每项保留 owner 与 closure condition |
| `parallel-scope` | 列出允许的 task-isolated scope 与禁止竞争的 shared current/GAP/owner 范围 |
| `evidence-and-freshness` | 绑定 design responsibility、before/after、test/runtime/external evidence 与当前 invocation freshness |
| `review-and-promotion` | 绑定 contribution、必要 ADR、independent committed range、expected current 与 promotion state |

每项必须显式判定 `applicable|not_applicable` 并给出理由；architecture impact 不得以空值代替判断。范围、风险、authority、持久化、SDK、外部、owner 或架构边界扩大时，旧结果 stale 并重新进入 Architecture owner。

## Change paths and lifecycle

- `target_native`：新能力直接进入 target boundary，不新增 legacy authority 或 compatibility layer。
- `legacy_boundary_convergence`：仅在旧边界仍有真实依赖时保留局部 compatibility，并明确 remaining debt、owner、退出和删除条件。
- `dedicated_refactor_slice`：在行为/API/规则不变前提下，以单一主写的小切片收敛旧实现，要求可验证、可观测、可回滚和明确删除条件。
- `no_architecture_impact`：只记录 current baseline/constitution、task/stage 与可审核理由，不创建 contribution、ADR 或 project-check burden。

阶段顺序固定为 Planning impact/path -> qualified implementation discovery re-entry -> Phase 2 before/after + project checks -> task contribution/necessary ADR -> independent committed full-diff Branch Review -> expected-current-bound serialized promotion -> fresh Phase 2/commit/Branch Review -> Publication/Acceptance current consumption。未 promotion 的 `reviewed_candidate` 不得进入 Publication/Finish。

## Current project-check descriptor

- descriptor identity：`guru-trellis-architecture-convergence:repository:1`。
- check id/version：`guru-trellis-architecture-convergence` / `1`。
- entrypoint：`docs/architecture/06-governance/change-contract.md`；这是 AI 语义检查协议，不是替代判断的脚本。
- applicable scope：stage invocation、authority binding、path exclusivity、required concern completeness、before/after regression、single-writer、parallel stale、contribution/ADR review 与 promotion freshness。
- rule refs：`ARCH-GOV-006..008`；decision refs：`ADR-005`；gap refs：`ARCH-GAP-006`。
- result contract：`guru-project-architecture-check-result-2.0`；freshness source 是当前 task candidate 或 exact committed range。

稳定失败路由为：缺适用 contract/constitution/check facts -> `contract_incomplete`；与 current authority 冲突 -> `architecture_conflict`；新增或恶化偏移、owner 扩张、无退出双写或 closed GAP 重现 -> `fitness_regression`；baseline、constitution、contribution 或 expected-current stale -> `sync_required`。AI 根据 applicability 与 task 真实依赖决定 `blocking`，runtime 只验证 descriptor/result 一一绑定、locator、freshness 与 route consistency。
