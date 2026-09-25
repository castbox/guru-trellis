# #454 C6/C7 Architecture Change Contract

Identity: `454-task-lifecycle-c6-c7-architecture-change-v1`. This task-local
contract consumes `guru-maintain-architecture-baseline:2.0`, current Architecture
`current-main-0.6.17-guru.63`, constitution
`guru-trellis-design-constitution-v1`, and project change contract
`guru-trellis-architecture-change-contract-v1`. The current requirement and
behavior authority is Issue #454 plus this task's approved `prd.md`, `design.md`,
and `implement.md`; the shared RDT authority remains `.63` until promotion.

| Concern | Applicability and C6/C7 decision |
| --- | --- |
| authority-binding | Applicable: this task uses the current `.63` baseline and the project contract; no earlier contribution is treated as current. |
| constitution-binding | Applicable: concept completeness, cohesion, minimum complexity, one-way debt convergence, and mature-practice applicability are reviewed against the current constitution. No exception is proposed. |
| boundary-and-decision | Applicable: `target_native` C6 creation composition and activation inputs consume C2/C3/C4/C5 primitives. `ADR-015` remains the decision; `ARCH-GAP-011` remains partial/open. |
| owner-and-single-writer | Applicable: future `guru-create-task` owns task creation and `guru-activate-task` owns activation; C6 shared runtime does not publish their packages. Architecture and RDT owners alone promote their respective shared current files. |
| compatibility-and-exit | Applicable: no parallel task/workspace mapping or path-authority reader/writer is added. Existing predecessor stays active until E434 atomically switches and retires it; C7 proves zero legacy access only in new Phase C code. |
| gap-and-deviation | Applicable: C6/C7 narrows `ARCH-GAP-011` without closing D443/D436/E434 or #434. No closed GAP is reopened or new deviation accepted. |
| parallel-scope | Applicable: this branch owns only its task-local contribution and C6/C7 runtime/schema/planned metadata. It does not edit production workflow, installed platform projection, or D443/D436/E434 assets. |
| evidence-and-freshness | Applicable: before `.63` has C2/D0/C3/C4/C5 substrate and four planned IDs; after this candidate has creation/activation inputs and six planned IDs. Tests, ownership, drift, static subtraction, task validation and failures must be read fresh at each gate. |
| review-and-promotion | Applicable: contribution `docs/architecture/contributions/454-task-lifecycle-state-model-c6-c7.md` and RDT counterpart remain isolated candidates until independent committed Branch Review. Promotion expects `.63`; any shared-current diff re-enters Phase 2, Task Commit, and full Branch Review. No new ADR. |

The sole project-check descriptor is
`guru-trellis-architecture-convergence:repository:1` at
`docs/architecture/06-governance/change-contract.md`, covering
`ARCH-GOV-006..009`, `ADR-005`, `ADR-009`, `ARCH-GAP-006`, and `ARCH-GAP-008`.
At each stage the Architecture owner determines applicability, before/after
satisfaction and blocking status from the current candidate or exact committed
range. This document is a review input, not a pass assertion.
