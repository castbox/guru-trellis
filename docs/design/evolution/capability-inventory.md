# Evolution Capability Successor Inventory

状态：`design_ready_for_delivery_planning` / `fresh_design_review_passed` / `evolution_refactor_eligible`。本文件已从selected-base `.41`重新审核
`CUR-CAP-001..023`与`TARGET-DELTA-001..013`的Design successor。#311通过
`CUR-CAP-013/014/017/018/019`到达installed publication terminal与standalone verifier failure evidence，
#312通过`CUR-CAP-012`到达original-worktree clean-tracked continuation、unrelated-dirty isolation和真实blocker；
不建立第14个target delta。Current facts remain owned by
[`current-capability-inventory.md`](../../requirements/evolution/current-capability-inventory.md); this file owns
only target Design allocation.

## 1. Current Capability Successors

| Current id | Preservation decision | Target owner / Design responsibility | Planned fixture |
| --- | --- | --- | --- |
| `CUR-CAP-001` | preserve authority separation | RDT/Architecture owners; `EVO-DES-002,005,060..064` | `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-PROJECTION` |
| `CUR-CAP-002` | preserve requirement/source fidelity | `guru-clarify-requirements`; `EVO-DES-019..022` | `EVO-FIX-INTAKE-CLEAR`, `EVO-FIX-INTAKE-REVIEWED-DESIGN` |
| `CUR-CAP-003` | preserve exact intake/mode routing, replace graph shape | admission/router/mode owners, with bound host event identity/content carried directly to one of 37 registered lifecycle owners; Admission/Route Request/Answer/Current Work/History are included, while specialists retain original-caller ownership; `EVO-DES-006..021` | `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-TASK-FREE` |
| `CUR-CAP-004` | preserve exact base and context freshness | Sync/Discovery; `EVO-DES-019..020,038` | `EVO-FIX-BASE-REFRESH`, `EVO-FIX-DETACHED-READ` |
| `CUR-CAP-005` | preserve clarification/readiness semantics | Clarification/change-readiness; `EVO-DES-019,021` | `EVO-FIX-INTAKE-UNCLEAR`, `EVO-FIX-CHANGE-REQUEST` |
| `CUR-CAP-006` | preserve no-mutation current convergence; when an action remains, preserve its exact plan, semantic affirmation, named Stock action wait and owner-specific zero-side-effect refusal without identity repetition | all semantic Skills that may own a side effect, including Workspace, publication provenance-tail preparation, Stock maintenance and active disposition cleanup; `EVO-DES-022,030,035..036,041,044..055,069,072` | `EVO-FIX-NO-ISSUE`, `EVO-FIX-TASK-FREE`, `EVO-FIX-STOCK-MAINTENANCE`, `EVO-FIX-ACTIVE-DISPOSITION`, `EVO-FIX-SEMANTIC-CONFIRMATION` |
| `CUR-CAP-007` | preserve one complete planning approval | Plan author + approval; one exact compound confirmation covers task activation plus immediate entry into the approved implementation scope, then deterministic activation closes directly to Implementation; `EVO-DES-023..027` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-SEMANTIC-CONFIRMATION` |
| `CUR-CAP-008` | preserve only two explicit specialist families | specialist router/owners with closed original-caller continuations and fresh re-entry; `EVO-DES-018` | `EVO-FIX-WORDING-EXPLICIT`, `EVO-FIX-QUALIFY-EXPLICIT` |
| `CUR-CAP-009` | preserve full Architecture lifecycle | Architecture owner; `EVO-DES-024,029,031,060..063` | `EVO-FIX-ARCH-NO-IMPACT`, `EVO-FIX-ARCH-ALIGNED`, `EVO-FIX-ARCH-CONFLICT`, `EVO-FIX-ARCH-PROMOTION`, `EVO-FIX-ARCH-DOWNSTREAM-FRESHNESS` |
| `CUR-CAP-010` | preserve bounded task-free loop and escalation | mode/task-free owner; `EVO-DES-015,022` | `EVO-FIX-TASK-FREE`, `EVO-FIX-LATEST-INTENT` |
| `CUR-CAP-011` | preserve semantic Phase 2 and targeted validation | Implementation/Check owners; `EVO-DES-028..030` | `EVO-FIX-FULL-NORMAL`, `EVO-FIX-BRANCH-FINDING` |
| `CUR-CAP-012` | preserve exact commit/base reconciliation/full-diff review plus #312 original-worktree continuity | Commit/Reconcile/Review; `EVO-DES-030..032,071` keeps current-base tracked path-clean same-task files in the original worktree, leaves unrelated dirty untouched and preserves every real artifact/identity blocker | `EVO-FIX-BRANCH-FINDING`, `EVO-FIX-BASE-EVOLUTION`, `EVO-FIX-EVOLUTION-PREREQUISITE` |
| `CUR-CAP-013` | preserve truthful delivery readiness and two routes | delivery owners with separate provenance-tail/push/Draft-PR/Finish/archive/Ready/Merge actions and already-current no-mutation exits; none Acceptance carries only acceptance current and enters Finish without a delivery fact; `EVO-DES-033..036,072` | `EVO-FIX-FULL-NORMAL`, `EVO-FIX-NONE`, `EVO-FIX-SEMANTIC-CONFIRMATION`, `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION` |
| `CUR-CAP-014` | preserve expected-head/closure/terminal correctness | Publish/Finish/Merge/Closure owners with stage-local recovery, archive-bound `ready_for_merge`, none Finish as the sole none-route delivery-fact producer and live completed-state convergence; `EVO-DES-034..036,072` | `EVO-FIX-PROVIDER-RECOVERY`, `EVO-FIX-FINISH-RECOVERY`, `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION` |
| `CUR-CAP-015` | preserve queryable history and owned cleanup | history/Finish/Cleanup/disposition; `EVO-DES-036..042` | `EVO-FIX-HISTORY-RESUME`, `EVO-FIX-ACTIVE-DISPOSITION` |
| `CUR-CAP-016` | preserve RDT/Architecture bootstrap, contribution, promotion and minimal spec projection | three repository authority owners plus outstanding-only, already-current-aware Bootstrap `projection_refresh`, including zero-promotion `authority_only` repair for missing/stale authority locator/usage/freshness; `EVO-DES-023..024,031,060..064` | `EVO-FIX-SSOT-BOOTSTRAP`, `EVO-FIX-RDT-LIFECYCLE`, `EVO-FIX-ARCH-PROMOTION` |
| `CUR-CAP-017` | preserve canonical/dogfood/installed/host consistency and immutable installed source | projection/install/migration/Publish owners; standalone policy maintenance returns to fresh Projection validation, while installed publication separates immutable extension source from reviewed target; `EVO-DES-043..047,056..059,072` | `EVO-FIX-PROJECTION`, `EVO-FIX-STOCK-MAINTENANCE`, `EVO-FIX-CLEAN-INSTALL`, `EVO-FIX-MIGRATION`, `EVO-FIX-INSTALLED-PROVENANCE-PUBLICATION` |
| `CUR-CAP-018` | preserve live-derived inventory and separate loss/consistency gates | Projection validator owns standalone execution and `postcheck_failure` classification; `EVO-DES-043,059,073` | `EVO-FIX-PROJECTION`, `EVO-FIX-RELEASE`, `EVO-FIX-VERIFIER-FAILURE-EVIDENCE` |
| `CUR-CAP-019` | preserve evidence layers and minimal validation ownership | Check/Projection/Release owners; Projection binds non-null credential-safe failure before cleanup and Finish consumes none of it; `EVO-DES-030,043..048,065..067,073` | `EVO-FIX-PLAN-NORMAL`, `EVO-FIX-FULL-NORMAL`, `EVO-FIX-RELEASE`, `EVO-FIX-VERIFIER-FAILURE-EVIDENCE` |
| `CUR-CAP-020` | preserve normal parallel isolation and both delivery routes | admission/lifecycle/delivery/cleanup graph; `EVO-DES-033..042` | `EVO-FIX-PARALLEL`, `EVO-FIX-NONE` |
| `CUR-CAP-021` | preserve direct answer with zero change resources, including Trellis reference | admission/router/answer plus manifest-bound reference adapter; `EVO-DES-006..014,051..052` | `EVO-FIX-ENTRY-ROUTING`, `EVO-FIX-STOCK-COEXISTENCE` |
| `CUR-CAP-022` | preserve relevant Gitlink pointer/content freshness only | implementation/check/review; `EVO-DES-028..030` | `EVO-FIX-SUBMODULE-BOUNDARY`, `EVO-FIX-BRANCH-FINDING` |
| `CUR-CAP-023` | preserve narrow EOF-only observation exception | Branch Review; `EVO-DES-030` | `EVO-FIX-BRANCH-FINDING` |

No capability is accepted by name/count alone. The target can replace current private schemas, artifacts and
wrapper routes, but each row must remain observable through its listed owner and fixture. Current `21 Skills / 89
exits` is a selected-base `.41` source identity, not a target magic count.

## 2. Target Delta Allocation

| Delta | Target Design allocation | Primary acceptance |
| --- | --- | --- |
| `TARGET-DELTA-001` | one Guru clarification owner replaces brainstorm; non-file requests stay direct-answer | `EVO-DES-013..015,019`; intake/entry fixtures |
| `TARGET-DELTA-002` | Architecture is lazily loaded before first design writing and reconciles reviewed design | `EVO-DES-023..026`; Architecture planning fixtures |
| `TARGET-DELTA-003` | one plan author/one approval; only two explicit specialist families, with nine wording profiles, ten active four-result qualification profiles and one standalone three-result qualification profile | `EVO-DES-018,025..027`; Plan/wording/qualification fixtures |
| `TARGET-DELTA-004` | invocation envelope, stable authority-content prefix, owner-minimal projections and zero redundant gates/reads/artifacts | `EVO-DES-009..011,065..067`; Plan/Full/Long-output fixtures |
| `TARGET-DELTA-005` | lifecycle-bound latest intent carries its exact event ref to one of 37 closed owners; Admission/Route Request/Answer/Current Work/History are explicit members, specialists retain original-caller ownership, and isolation/disposition/durable history have unique owners | `EVO-DES-006..008,038..042`; entry/latest-intent/history/disposition fixtures |
| `TARGET-DELTA-006` | task-free has a closed loop and exact partial-work escalation before standard resources | `EVO-DES-015,022`; task-free fixture |
| `TARGET-DELTA-007` | target-native distribution, atomic migration and immutable Release replace legacy aggregate shapes while preserving installed source/target publication through archive-bound Ready/Merge and standalone pre-cleanup failure evidence | `EVO-DES-043..048,059,072..073`; projection/install/migration/Release/installed-publication/verifier-failure fixtures |
| `TARGET-DELTA-008` | repository RDT precedes task planning and remains current through downstream gates; reviewed code-spec deltas use Bootstrap-only outstanding projection and fresh full-diff review converges already-current work to double-none | `EVO-DES-023,025,029,031,060..064`; RDT/Bootstrap fixtures |
| `TARGET-DELTA-009` | parent route excludes submodules; explicit nested change is a new repository invocation | `EVO-DES-020,068`; submodule fixture |
| `TARGET-DELTA-010` | current-work resolution and disposition own retain/suspend/abandon/remote convergence/cleanup | `EVO-DES-016,038..042`; disposition/history fixtures |
| `TARGET-DELTA-011` | exact `9/1/2/5` stock roles with one successor/caller/consumer per asset, including manifest-bound meta replacement, review-trigger-bound update-spec replacement and Projection-owned standalone Stock maintenance that returns to fresh Projection validation | `EVO-DES-043,049..055`; stock coexistence/maintenance/projection fixtures |
| `TARGET-DELTA-012` | provenance-aware selected stock actions survive install/update/migration/reapply without user overwrite | `EVO-DES-049..059`; stock-maintenance fixture |
| `TARGET-DELTA-013` | one dialogue-local semantic confirmation contract first bypasses plan/confirmation/refusal for no-mutation current exits; when an action remains, it accepts clear affirmatives after an unchanged exact plan, scopes authority to that action, gives every explicit refusal one owner-specific zero-side-effect output, requires Stock mutation through its named profile-fixed wait instead of direct continuation-to-reentry, and forbids fixed prompt/password/hash/digest/task/path/branch/SHA/identity/summary/prescribed-wording challenges, script parsing and authorization persistence | `EVO-DES-054,069`; Semantic Confirmation and Stock Maintenance fixtures |

## 3. Subtraction And Replacement Ledger

| Current shape removed from target runtime | Successor | Exit condition |
| --- | --- | --- |
| stock `trellis-start/continue/finish-work/brainstorm/check/spec-bootstrap/update-spec/before-dev/meta` semantic surfaces | Guru admission/lifecycle/RDT/Architecture/implementation owners; update-spec -> Bootstrap projection refresh; meta -> reference manifest/adapter + change lifecycle | all nine concrete successors current; discoverable raw target count zero |
| normal Planning wording/qualification wrappers | `guru-plan-task` plus one `guru-approve-task-plan` | normal-path wrapper call count zero |
| task planning as repository Docs authority | repository RDT plus task-local projection/contribution | no task artifact consumed as shared authority |
| unnamed standard Phase 2 coordinator/stock autonomous implementer | `guru-implement-task` plus caller-bound worker | exactly one implementation owner per invocation |
| `guru-review-task-publication` aggregate | delivery route + readiness + acceptance owners | both routes preserve truthful readiness and unique terminal |
| `guru-verify-extension-installation` standalone-only shape | projection/clean/migration/Release owners | standalone and embedded ownership fixtures pass |
| Finalizer-owned publication/merge/closure/cleanup aggregate | provenance-tail preparation, branch push, PR create, Finish/archive/Ready, merge, closure and delivery-terminal Cleanup exact action owners | each confirmation/refusal/recovery is stage-local; Publish refusals use three action-local outputs and the distinct `task-publication-preparation-not-executed`, `task-branch-push-not-executed`, `task-pr-creation-not-executed` consumers; each failure re-enters only its exact owner |
| legacy registry/schema/private-result consumers | `guru-team-evolution-contract-1.0` | existing migration final validation proves zero legacy consumer before activation |

The subtraction ledger authorizes no deletion in this planning task. It defines the proof required by a future
implementation or migration slice.
