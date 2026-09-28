# #454 Generation 7 TaskId Domain Architecture Contribution

- Identity: `architecture-contribution-454-task-lifecycle-gen7-taskid-domain-v1`.
- State: independently reviewed and promoted against expected `current-main-0.6.17-guru.67/active` to `.68/active`; post-promotion gates remain separate.
- Task: `454-task-lifecycle-state-model`, lifecycle generation 7.
- Change path: `target_native`; no new ADR is required.
- Current source candidate: `castbox/Trellis@a9e0b5dcb40e9dd0a54f990ad4d215e427939856`, tree `38a2e226a03ca7899ae3504bf3763dc1aac0cb35`, successful main CI `36486251351`. Fork PRs #18-#21 are merged and Issue #8 is closed; Guru package-ready verification and final review remain separate.

The official Trellis task writer owns the complete TaskId domain
`[A-Za-z0-9][A-Za-z0-9._-]*`. A TaskId is not a branch name, Git ref tail,
task directory slug, checkout path, Issue number, session key, assignee, or
developer identity. The writer validates explicit IDs and IDs derived from a
slug before creating the task. The Guru lifecycle kernel validates the same TaskId
domain. For a legal TaskId that cannot form the existing handoff Git ref,
Guru derives a deterministic ref in the separate
`guru-task-lifecycle-id/<sha256(TaskId UTF-8)>` namespace. Git-valid TaskIds
retain their existing ref. This projection does not make the ref the TaskId
authority or create a second task/session store.

The task writer remains in the fixed Fork; the Guru package owns only its
schema/runtime/installed projection and retained-control resource checks.
The current single-focus session pointer, task branch, checkout acquisition,
source relation and resource ledger remain independent owners. This change
does not require a session to retain multiple bindings or to release an old
binding before switching focus.

The official session reader in an installed Guru Team checkout also treats a
missing current TaskBranchBinding as `binding_required`. It cannot recover
current branch authority from an older checkout's task artifact. Ordinary
Trellis without Guru Team retains its existing no-binding fallback; neither
path creates an additional session binding record or history.

TaskBranchBinding has exactly five fields: schema version, TaskId, generation,
binding revision and branch name. No epoch token is stored in the binding,
resource ownership or public DTO. Cleanup revalidates selected live targets;
when local control records are missing, it refuses deletion of a branch still
carrying an active task artifact unless another retained local branch contains
that task commit and artifact. Reactivate accepts current `selected-*` Cleanup
receipts and completed older `manual-*` receipts for the same sealed Finish.

The full #454 review also closed two owner boundaries. The official task
create/archive store carries immutable TaskId and structured source without
`task.json.branch` as archive authority; the Guru dogfood task CLI projects
the same fixed Fork semantics. Its source writer validates exactly the Guru
reader's portable owner/repo domain before writing task metadata, including
the no-`.git` transport-suffix rule. The dogfood session reader consumes the
same five-field TaskBranchBinding as the lifecycle store. The existing Cleanup owner exposes a call-local
terminal resource candidate DTO when ownership is missing, then accepts
selected candidate IDs under fresh live validation and an exact deletion
confirmation. Its completed selection receipt is consumed by Reactivate for
the same TaskId, generation and Finish result. Candidate discovery never
reconstructs ownership or creates a durable locator. These are repairs to
existing owners, not new task/session binding concepts or new persistence.

Both successful normal Finish and the missing-ownership Finish route retain the
same minimal terminal result in ignored common-dir runtime. If only the
resource ledger is later lost, Cleanup validates that exact Finish identity
before offering call-local manual candidates; it never infers Guru ownership
from surviving Git resources. The terminal result also retains the portable
Finish branch as a liveness hint: a confirmed empty selection can seal a
zero-deletion Cleanup only after that branch is absent. An older result without
the hint remains on the manual candidate route; unrelated branches are never
deleted by an empty selection. Reactivate accepts the resulting exact
`selected-*` cleaned receipt even when the Finish transaction originally
completed through the normal owned-ledger route and that ledger was lost later.

## Project Change Contract

Requirement authority is the live #454 accepted TaskId pattern and this
task's PRD; behavior authority is the generation 7 design and implementation
plan. This contribution binds
`guru-maintain-architecture-baseline:2.0`,
`docs/architecture/README.md@current-main-0.6.17-guru.67/active`,
`guru-trellis-design-constitution-v1/current`, and
`guru-trellis-architecture-change-contract-v1`. The relevant current
decision is `ADR-016`; `ARCH-GAP-009/011` are inherited and must not worsen.
The concept/semantic-completeness, cohesion/change-isolation, minimum
complexity and debt-convergence principles apply. Mature-practice
applicability is satisfied by using the fixed official writer rather than a
Guru-side task writer.

| Required concern | Applicability and result |
| --- | --- |
| authority-binding | Applicable: the fixed Fork writes TaskId/source; Guru only validates or supplies its reviewed source and derives receipt refs. Cleanup uses live Git facts only for explicit candidate selection, not ownership inference. |
| constitution-binding | Applicable: the five current principle identities remain bound to the existing constitution. |
| boundary-and-decision | Applicable: `target_native` extends the accepted TaskId domain without changing `ADR-016` ownership. |
| owner-and-single-writer | Applicable: Fork is the sole task writer; Guru lifecycle is the sole receipt-ref projection writer and existing Cleanup owner handles selected deletion; Architecture and RDT owners alone promote shared current. |
| compatibility-and-exit | Applicable: Git-valid TaskIds retain old refs, while legal Git-ref-invalid IDs use the separate namespace. The new Cleanup public profile/exit directly follows live #454; no `manual` alias, branch-field read or dual authority remains. |
| gap-and-deviation | Applicable: no new, worsened or prematurely closed GAP; `ARCH-GAP-009/011` keep their current owner and exit conditions. |
| parallel-scope | Applicable: code, tests and this task-owned contribution may advance in the task branch; editing `.67` current or another task's contribution before promotion is forbidden. |
| evidence-and-freshness | Applicable: exact Fork commit/CI and candidate-bound tests plus source/installed projection are reviewed against this generation's diff. |
| review-and-promotion | Applicable: independent committed-range review precedes expected-current-bound promotion; promotion-created diff re-enters Phase 2 and Branch Review. |

Current and target semantic owners do not change. The single writer for each
shared current authority is its existing Architecture or RDT owner. No new
runtime persistence, legacy adapter, open-ended TaskId alias or separate
session binding record is introduced. The old Git-ref restriction is removed
from TaskId validation once the fixed Fork and Guru contracts agree; the
receipt-ref projection remains a deterministic private implementation detail.

Before: the old fixed Fork and Guru control-ref validation rejected legal
TaskIds such as `task.lock`, `task.`, and `task..child`; the newer Fork still
wrote retired branch metadata and its archive gate read that field. Cleanup
also lacked the specified terminal candidate DTO/profile.
After, independently reviewed committed-range candidate: the official writer,
Guru runtime/schema and installed package agree on TaskId/source; archive
does not depend on task branch metadata; Cleanup selection uses only current
Git candidates and preserves ownership boundaries. Existing Git-valid IDs
keep their previous ref identity. No legacy dual writer or adapter remains.
The previous `.67` authority and #434 contribution are immutable inputs,
not targets for this candidate.

The independent pre-promotion review checked the full committed candidate,
fixed Fork source/CI, package tests, installed projection and shared
R454/D454/T454 traceability. Architecture and RDT owners serialized the
`.67 -> .68` promotion against the expected current. Promotion-created
changes require a new Phase 2, commit and full Branch Review. The
multi-platform Release matrix remains outside this Issue.
