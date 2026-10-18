# Current Capability Inventory

派生日期：2026-08-19；source：`trellis/skills/guru-team/registry.json` 与各 package `interface.json`；source baseline：`5c059f49…` + #260 compatibility task delta（精确 revision 为当前 Git HEAD）；provenance：`code_recovered` + #260 exact matrix evidence。

| Skill id | External exits |
| --- | --- |
| `guru-select-workflow-mode` | `standard_intake`, `task_free`, `blocked` |
| `guru-sync-base` | `synced`, `skipped`, `blocked` |
| `guru-discover-change-context` | `context_ready`, `refresh_base`, `blocked` |
| `guru-clarify-requirements` | `clear`, `needs_context`, `refresh_context`, `retarget_context`, `new_task`, `blocked` |
| `guru-review-contract-wording` | `pass`, `content_changed`, `blocked` |
| `guru-review-change-request` | `ready`, `clarify_requirements`, `review_wording`, `refresh_context`, `blocked` |
| `guru-create-task-workspace` | `created`, `refresh_review`, `blocked` |
| `guru-approve-task-plan` | `approved`, `revision_required`, `clarify_scope`, `blocked` |
| `guru-qualify-normal-scenario` | `classified`, `scope_confirmation_required`, `mechanism_revision_required`, `blocked` |
| `guru-execute-task-free-change` | `completed`, `resume_active_task`, `scope_change`, `location_required`, `reselect_mode`, `explicit_choice_required`, `blocked` |
| `guru-check-task` | `passed`, `implementation_required`, `planning_stale`, `blocked` |
| `guru-create-task-commit` | `committed`, `revision-required`, `blocked` |
| `guru-reconcile-task-base` | `reconciled`, `review_continuity_required`, `implementation_required`, `planning_stale`, `scope_confirmation_required`, `blocked` |
| `guru-review-branch` | `passed`, `continuity_passed`, `implementation_required`, `scope_confirmation_required`, `blocked` |
| `guru-review-task-publication` | `ready`, `return_to_task_work`, `blocked` |
| `guru-finalize-task` | `base_reconciliation_required`, `publication_review_stale`, `resume_finalization`, `reprepare_required`, `ready_for_merge`, `blocked` |
| `guru-merge-task-pr` | `merged`, `merge_blocked`, `closure_mismatch` |
| `guru-verify-extension-installation` | `verified`, `blocked` |
| `guru-maintain-requirements-design-test-ssot` | `ssot_current`, `sync_required`, `revision_required`, `baseline_incomplete`, `blocked` |
| `guru-maintain-architecture-baseline` | `baseline_current`, `sync_required`, `baseline_incomplete`, `architecture_conflict`, `contract_incomplete`, `fitness_regression`, `blocked` |
| `guru-bootstrap-repository-ssot` | `completed`, `baseline_incomplete`, `repair_required`, `blocked` |

## Registry、schema、command 与平台 closure

- 每行的 authoritative interface locator 是 `trellis/skills/guru-team/packages/<skill-id>/interface.json`；schema 与 consumer locator 由该 interface 声明，command 由同包 `commands.json` 声明。
- Registry 标记 21 个 package 为 `active`；20 个 workflow-integrated，`guru-verify-extension-installation` 为 `standalone_only`。
- Interface schema ids 当前包含 `guru-team-skill-interface-1.4`、`1.5`、`1.6`；完整 input/output schema id 列表以 `trellis/guru-team-extension.json` 为准。
- 支持平台由每个 registry entry 声明为 `shared`、`codex`、`cursor`、`claude`；canonical/installed/platform package bytes 由 preset inventory 与专项 distribution tests 校验。
- Workflow route/consumer closure 以 `trellis/workflows/guru-team/workflow.md` markers 与 interface consumer projection 为准。本 inventory 只索引 stable identity，不取代这些 public contracts。

Inventory freshness：registry entries、interface exits、manifest schema lists、workflow markers 或 source commit 发生变化时，本页必须经 RDT task-impact/promotion 更新，不能单独沿用旧计数。

#275 verifier 不再复制上述 package/command 数量；运行时从 canonical registry、interfaces 与 validator 输出派生 active ids、commands 和 complete-package set，并与 installed projection 做 exact equality。

## #260 compatibility result

- live-derived platforms：`claude`、`codex`、`cursor`；每个平台均完成 clean/existing 两个隔离 cell，6/6 passed。
- Trellis/project target：`0.6.15`；existing before：official `0.6.5` + `v0.6.5-guru.10` / extension `0.6.5-guru.36`。
- after extension：`0.6.5-guru.37`；active Skills=`21`，external exits=`89`，source/installed/platform interface/schema/command/route 集合无 blocking loss。
- 每个 cell执行 RDT 6-case/4-profile、Architecture 4-case/4-profile、Bootstrap 4-case/3-profile installed eval，并通过 Phase 0、workspace 与 closeout smoke。
- six-cell recursive sidecar count=`0`，template-hash unknown drift=`0`；已知 update backups 仅在 reconciliation 中出现并在最终状态移除。
- current-head dual PATH-runtime matrix SHA-256：`660422848f6efba9f1c3c6fcf2d9d23a1e8b710af8ffd10bf0f12e0954910f49`；workflow sample=`public_plus_local_candidate`，不等于 `.37` 已发布。Per-run wrapper summary digest包含临时 A/B fixture commit identity，因此不作为跨重跑稳定 capability identity。
