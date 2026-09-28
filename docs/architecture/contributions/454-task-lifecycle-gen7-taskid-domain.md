# #454 Generation 7 TaskId Domain Architecture Contribution

- Identity: `architecture-contribution-454-task-lifecycle-gen7-taskid-domain-v1`.
- State: candidate pending independent review; expected current is `current-main-0.6.17-guru.67/active`.
- Task: `454-task-lifecycle-state-model`, lifecycle generation 7.
- Change path: `target_native`; no new ADR is required.
- Source candidate: `castbox/Trellis@09994d21a462813c4d1a280cce7fe1bf803af019`, tree `73810704ee0cc72f295e8bc89a512344523124c9`, successful main CI `36414078546`.

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
| authority-binding | Applicable: the fixed Fork writes TaskId; Guru only validates and derives receipt refs. |
| constitution-binding | Applicable: the five current principle identities remain bound to the existing constitution. |
| boundary-and-decision | Applicable: `target_native` extends the accepted TaskId domain without changing `ADR-016` ownership. |
| owner-and-single-writer | Applicable: Fork is the sole task writer; Guru lifecycle is the sole receipt-ref projection writer; Architecture and RDT owners alone promote shared current. |
| compatibility-and-exit | Applicable: Git-valid TaskIds retain old refs, while legal Git-ref-invalid IDs use the separate namespace; no dual read or compatibility authority remains. |
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
TaskIds such as `task.lock`, `task.`, and `task..child`.
After: the official writer, Guru runtime/schema, installed package and
receipt-ref derivation agree on the exact domain. Existing Git-valid IDs keep
their previous ref identity. No legacy dual writer or adapter is retained.
The previous `.67` authority and #434 contribution are immutable inputs,
not targets for this candidate.

Review must check the full candidate diff, fixed Fork source/CI, package
tests, installed projection and shared R454/D454/T454 traceability. After
independent committed-range Branch Review, the Architecture and RDT owners
may serialize a successor promotion against the then-live expected current.
Promotion-created changes require a new Phase 2, commit and full Branch
Review. The multi-platform Release matrix remains outside this Issue.
