# #435 Active Task Delivery Loop Architecture contribution

## Identity And Authority Boundary

- candidate identity: `architecture-contribution-435-active-task-delivery-loop-v1`.
- lifecycle state: `reviewed_promoted`; absorbed by `current-main-0.6.17-guru.55`.
- source authority: Issue #435 contract `2026-09-18-r3`.
- task locator: `.trellis/tasks/09-18-435-active-task-delivery-loop`.
- related RDT contribution: `docs/requirements-design-test-contributions/435-active-task-delivery-loop/`.
- source/expected baseline: `docs/architecture/README.md` / predecessor `current-main-0.6.17-guru.54`; current successor `current-main-0.6.17-guru.55` / `active`.
- design constitution: `docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `docs/architecture/06-governance/change-contract.md` / `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.
- accepted decision: [ADR-012](../adr/012-active-task-delivery-loop.md).

This contribution records the stable target boundary and promotion provenance only. Independent committed full-diff review passed for `a410a97fad127b9cc9bce1680666f6149d3ba616...83909737ebb67fdc505d68e6bcb39acf759101c1`, and the Architecture owner serialized the expected `.54 -> .55` promotion. `.54` remains immutable history; this file does not become a second shared current authority.

## Before And Target

Before: Publication owns delivery readiness and Issue closure intent; Finalizer owns push, PR create/update, archive, Ready, recovery and Merge handoff; Merge owns terminal merge and closure verification. The task is archived before merge, so task-work findings require archived restore. Historical delivery is coupled to one task branch/PR tail and cannot represent repeated business Delivery cycles while the task remains active.

Target: three additive semantic packages own Delivery Review, Publish and Merge. Each successful Merge produces one Delivery result and leaves the same task active. #436 Completion is the only next lifecycle owner. Delivery history is reconstructed from controlled merge-commit trailers plus GitHub/Git identities across branches and Reactivate workspaces. #434 alone activates the graph and retires old edges after #435 and #436 are ready.

## Ownership And Single Writers

- `guru-review-task-delivery` owns slice readiness, PR payload truth, remaining-work disclosure and current upstream authority.
- `guru-publish-task-delivery` owns reviewed-head push, unique current PR, Draft/Ready transition and #405 recovery.
- `guru-merge-task-delivery` owns merge readiness, confirmation, expected-head mutation, trailer bytes, terminal recovery and Delivery result.
- existing Planning, Check, Task Commit, Branch Review and Reconcile owners keep their current responsibilities with narrow sliced-delivery/resolved-tree contract evolution.
- #436 owns Completion, Closure, Finish, Cleanup and Reactivate; #434 owns production graph activation and old-edge retirement.
- Architecture/RDT shared current retain serialized promotion single writers.

## Required Concerns

| Concern | Applicability | Candidate contract |
| --- | --- | --- |
| `authority-binding` | `applicable` | Bind Architecture 2.0, expected `.54`, live #435 r3, task planning and project change contract v1. |
| `constitution-binding` | `applicable` | Bind semantic completeness, cohesion/change isolation, minimum necessary complexity and one-way convergence by identity. |
| `boundary-and-decision` | `applicable` | Select `target_native`: split Delivery Review/Publish/Merge ownership and preserve Completion/Finish/Cutover boundaries. |
| `owner-and-single-writer` | `applicable` | Each semantic judgment and remote mutation has one owner; Merge alone writes the Delivery trailer/result; #436 alone completes the task. |
| `compatibility-and-exit` | `applicable` | Add new packages without adapters or active dual graph; #434 atomically activates and retires old edges after both implementation Issues. |
| `gap-and-deviation` | `applicable` | Introduce candidate GAP closure for premature archive/terminal coupling and cross-branch Delivery identity; do not reopen closed `ARCH-GAP-008`. |
| `parallel-scope` | `applicable` | #435 writes task-isolated packages/docs/tests/contributions; it does not modify #434/#436 task artifacts or shared current before promotion. |
| `evidence-and-freshness` | `applicable` | Bind #405/#407 regressions, two-cycle Delivery, Reactivate seed, exact merge identities, source/installed projections and current candidate/range. |
| `review-and-promotion` | `applicable` | Independent committed review precedes expected-`.54` promotion; promotion-created diff re-enters fresh Phase 2, Task Commit and Branch Review. |

## Identity And Compatibility Decision

The target uses a versioned merge-commit trailer carrying stable task identity and exact reviewed head. The Merge package now exposes one deterministic read-only discovery command that scans the fresh target-base first-parent merge history and cross-checks each matching trailer against GitHub PR/merge identity, repository/base, merge commit and parents. It does not read PR bodies or the current task branch/worktree. No Delivery ledger, current-branch-only lookup or mutation of task creation facts is introduced.

The old production graph remains current only until #434 cutover. This contribution creates no compatibility adapter and projects no old output into a new result. Existing in-flight old-chain tasks complete on the old version or receive explicit manual handling under #434 migration authority.

## Project Check And Promotion

- descriptor identity: `guru-trellis-architecture-convergence:repository:1`.
- check identity/version: `guru-trellis-architecture-convergence@1`.
- refs: `ARCH-GOV-006..010`, `ADR-005`, `ADR-009`, `ADR-011`, `ARCH-GAP-008`.
- before: `.54` production authority has the Publication/Finalizer/Merge terminal topology and the business-task workflow has 22 mandatory invokes / 98 external exits.
- after inventory: canonical and installed projections contain 26 active packages / 114 package exits / 96 commands, including the three additive Delivery packages and the Merge-owned read-only discovery command; the production business-task workflow remains 22 mandatory invokes / 98 external exits.
- after candidate: three additive `active` / `deferred` package owners, narrow existing-owner adaptations, #407 resolved-tree recovery and task-owned contribution/ADR; the business-task workflow remains 22 mandatory invokes / 98 external exits until #434.
- current result: Phase 2 and independent committed full-diff review confirm one owner per judgment/mutation, no dual runtime authority, no ledger, exact merge-trailer identity, target-base historical reconstruction independent of PR body and current binding, deferred production integration, source/installed/platform projection parity and one explicit cutover owner. Two-cycle, deleted-head-branch, Reactivate-style binding, bookkeeping exclusion, identity-drift, #405 recovery and #407 resolved-tree tests pass. Package, integration, preset, upgrade, ownership, closure, drift and repository checks passed; the known Finish-family failures reproduced unchanged from the task base and remain outside #435.
- promotion state: `reviewed_promoted`; shared current is `current-main-0.6.17-guru.55` and ADR-012 is accepted.
- expected current identity: predecessor `current-main-0.6.17-guru.54`; promoted successor `current-main-0.6.17-guru.55`.
- ADR: required because the task changes lifecycle owner topology, repeated Delivery semantics, task-active-after-merge behavior, durable Delivery identity and compatibility/cutover policy.

## Review Boundary

The reviewed source range proves the task-local implementation candidate and applicable project check before promotion. Promotion proves only that this reviewed additive capability entered `.55`; the promotion-created diff must repeat fresh Phase 2, Task Commit and independent Branch Review. Production graph activation, release and #436 completion flow remain outside this contribution. Any scope, owner, persistence, external integration or merge-policy expansion makes this result stale and re-enters the Architecture owner.
