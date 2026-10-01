# #481 Task Personnel Retirement Architecture Contribution

## Identity

- Contribution identity: `architecture-contribution-481-retire-task-personnel-v1`.
- State: `independently_reviewed_promotion_candidate`; task: `.trellis/tasks/10-01-481-retire-task-personnel`.
- Source: `castbox/guru-trellis#481`; predecessor: `current-main-0.6.17-guru.69` / active.
- Guru contract: `guru-maintain-architecture-baseline:2.0`; project contract: `guru-trellis-architecture-change-contract-v1`; constitution: `guru-trellis-design-constitution-v1` / current.
- Change path: `target_native`; expected current identity: `current-main-0.6.17-guru.69`.
- Promotion: implementation, Phase 2 and independent committed full-diff Branch Review passed for `fb22d5cd5a61c6b92153a9e9454308c1c8335f8e`; expected `.69` current identity reviewed. The `.70` shared-authority diff requires fresh Phase 2, commit and full Branch Review before Publication.

## Boundary And Decision

The official Fork owns task.json shape and task/session primitives. Guru owns its create-task semantic gate, reviewed delivery input, TaskId/generation composition, TaskBranchBinding, Git common-dir resource ledger, and path-free session adapter. The selected install source is the exact built Fork commit containing upstream PR #24; the old source lock is predecessor evidence only. The public create-task task object directly loses creator and assignee, and the official create command receives no personnel arguments. The old public schema and old installed entry are unsupported; no alias, default personnel value, dual input, or migration writer is added.

The strict upstream task schema makes Guru's extra top-level delivery_target invalid. Guru keeps reviewed delivery target in its call-local create input, checks it against the current repository and selected delivery branch, and writes only official task metadata. Later Delivery and Publication owners use their own reviewed inputs and live Git/GitHub facts. They do not reconstruct a delivery target from task.json. The source Issue remains structured `source`, never a person or a scope-string substitute.

Current tasks and schema-valid archives enter normal lifecycle resolution. Retained old archives contribute only their `id` to TaskId collision checks. Explicit TaskId and strictly matched exact-source Issue lookup may locate an old archive solely to return unsupported-legacy. With no structured source, an exact finish-summary Issue index or canonical scope may serve that read-only lookup; conflict or multiplicity is ambiguous and no clue restores an old archive as a lifecycle candidate. The same boundary applies to Reactivate and Finish recovery. #454 session/branch binding and caller/guru ownership remain their existing single-writer stores and terminal retirement rules. #292 remains the Phase 1 author owner; current brainstorm only supplies requirement exploration.

## Required Concerns

| Concern | Applicability and task-owned decision |
| --- | --- |
| `authority-binding` | Applicable: bind the active `.69` Architecture and Guru 2.0/project v1 change contracts until reviewed promotion. |
| `constitution-binding` | Applicable: official extension use, complete task identity, minimal state, and one-way legacy retirement exercise `mature-practice-applicability`, `concept-semantic-completeness`, `minimum-necessary-complexity`, and `debt-one-way-convergence`; no principle exception is proposed. |
| `boundary-and-decision` | Applicable: direct update to task creation, inventory, archive, source pin, and installed projection; retain ADR-015's Fork/Guru ownership and close no unrelated GAP. |
| `owner-and-single-writer` | Applicable: Fork writes official task.json/session; Guru's existing owners write branch/ledger; task owns this contribution; Architecture owner alone promotes shared current. |
| `compatibility-and-exit` | Applicable: retire unsupported personnel inputs and task records immediately at the new source boundary; legacy archive lookup is read-only rejection with no compatibility execution or data rewrite. |
| `gap-and-deviation` | Applicable: remove the current mismatch between Guru personnel arguments/extra metadata and strict upstream schema. Complete Release matrix and production installs remain independently unverified; no closed GAP is reopened. |
| `parallel-scope` | Applicable: this task edits its own planning/contribution and later its scoped code/projections. Shared Architecture/RDT current authority changes require serialized promotion; #292 Phase 1 author work is excluded. |
| `evidence-and-freshness` | Applicable: before state is old source lock and personnel create path; after state requires source validator, real clean install, package/runtime and #454 regressions, dogfood/installed parity, reapply/drift and platform checks. Bind each gate to current task content and exact candidate. |
| `review-and-promotion` | Applicable: implementation and fresh Phase 2 precede contribution review; independent full committed range precedes promotion; promotion-created diff re-enters Phase 2, commit and Branch Review. ADR-015 already owns the identity/owner decision, so no new ADR is proposed. |

## Project Check

`guru-trellis-architecture-convergence:repository:1` is applicable and blocking. Before this candidate, Guru creation passed retired personnel fields to the old Fork, and some archive paths could admit old task metadata as lifecycle input. After this candidate, the verified PR #24 Fork owns the strict task shape, Guru creation passes no personnel argument, legacy archives reserve TaskIds and serve only read-only rejection diagnostics, and existing C4/C5/session stores retain their sole writers. The current contribution covers all required concerns above, adds no second state authority or open-ended compatibility path, and leaves shared `.69` untouched. The Phase 2 project check is `pass`; no new or worsened deviation or closed-GAP recurrence was found. A complete committed-range Branch Review and serialized promotion remain pending and must repeat this check against their own fresh evidence.

Current evidence: exact Fork source validator passed for `64fe9a15a68df1add3a2a7fd182f3d84e6eba4ac` and CLI/core `0.7.0-castbox.1`; task lifecycle 152/152, create-task 13/13, Reactivate 25/25, Finish 56/56, session 8/8 with one environment skip, checkout 4/4, branch 3/3, installer 101/101, and compatibility-contract 73/73 passed. A Codex clean focused install passed native loading, initial apply, two reapply operations, same-candidate update, template hashes and session binding. Dogfood drift and sidecar checks passed with no residual `.new` or `.bak`. Complete multi-platform Release/upgrade and predecessor-upgrade matrices, public remote marketplace installation, production installs, independent committed Branch Review and shared-current promotion are unverified here.
