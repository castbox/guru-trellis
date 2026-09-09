# #378 Fixed Fork Runtime Architecture Contribution

## Identity And Authority

- Candidate: `architecture-contribution-378-pinned-fork-runtime-v1`.
- Task: `.trellis/tasks/09-09-378-pinned-fork-runtime`.
- Requirement: `castbox/guru-trellis#378` and the isolated RDT contribution at
  `docs/requirements-design-test-contributions/378-pinned-fork-runtime/`.
- Expected baseline: `docs/architecture/README.md`, `current-main-0.6.5-guru.46`.
- Constitution: `docs/architecture/00-foundation/design-constitution.md`,
  `guru-trellis-design-constitution-v1`, current.
- Change contract: `docs/architecture/06-governance/change-contract.md`,
  `guru-trellis-architecture-change-contract-v1`, concern set
  `guru-trellis-architecture-change-concerns-v1`.
- Change path: `target_native`. State: unpromoted candidate. Independent
  committed Branch Review and shared-authority promotion remain outstanding.

## Before And Candidate

The previous normal install used the original Trellis npm distribution and
left the missing-session resolver fallback enabled in the installed runtime.
Changing Git remotes alone did not bind those installed bytes to a Fork.

The candidate uses one managed source record and an explicitly supplied
`castbox/Trellis` checkout. The Fork's own build and Node CLI remain the only
framework implementation. The verifier checks HEAD, repository identity,
version/package-manager metadata and source/build template bytes. It does not
clone, package, copy dist, invent a launcher or fall back to another distribution.

Existing standalone callers inherit declared source configuration. Full
verification retains its capability catalog and representative output, using an
explicit predecessor checkout/SHA for historical cells. Focused verification
remains separate and cannot establish predecessor or full-matrix success.

Closeout fixture preparation belongs to the verifier; installed Planning,
Phase 2, Commit, Review and Publication entries own their actual operations.
Shared native adapter functions are not a planning or review API.

## Required Concerns

| Concern | Applicability | Candidate decision |
| --- | --- | --- |
| authority-binding | applicable | Bind Architecture 2.0, expected .46, live #378 and the existing project change contract. |
| constitution-binding | applicable | Apply source ownership, change isolation and minimum complexity; no additional framework implementation. |
| boundary-and-decision | applicable | target_native: source selection is explicit data, source validation is deterministic, approval remains AI-owned. |
| owner-and-single-writer | applicable | Fork owns framework templates; preset owns Guru projections; this task writes only its isolated contribution before promotion. |
| compatibility-and-exit | applicable | Remove the normal original npm source path; retain the standalone full catalog with explicit inputs, not a dual-source fallback. |
| gap-and-deviation | applicable | Address #378 source/installed mismatch; preserve the outstanding historical-matrix evidence boundary without claiming it closed. |
| parallel-scope | applicable | Preserve #388/#389, other tasks, source main, session files and the old stash; do not promote shared docs directly. |
| evidence-and-freshness | applicable | Bind the fixed Fork SHA and actual candidate bytes; separate focused install/update, source tests and fake-provider closeout evidence. |
| review-and-promotion | applicable | Complete current Phase 2 and independent committed review before serialized promotion; promotion changes require a fresh check. |

## Project Check

Descriptor: `guru-trellis-architecture-convergence:repository:1`;
check: `guru-trellis-architecture-convergence@1`; protocol is the current
change-contract Markdown. Rule refs are `ARCH-GOV-006..008`, `ADR-005` and
`ARCH-GAP-006`. No new architecture scoring script or detached approval ledger
is introduced.

The candidate adds a managed source record with direct installer/verifier
consumers, and repairs verifier-owned fixture composition. It retains one
framework source and one projection writer. No new concurrent writer, OS
identity authority, lock, runtime dual-read or implicit fallback is introduced.

Evidence: `test_fork_session_isolation.py`,
`test_verify_trellis_upgrade_contract.py`,
`test_verify_throwaway_python_routing.py`,
`test_installed_closeout_owner_boundary.py`, the source-lock installer test,
and actual focused shell execution recorded in the task implementation notes.
Full historical matrix and remote publication remain unverified; fake-provider
merge values are not remote delivery evidence.

## Promotion

No separate ADR is required: this applies the existing ownership and
minimum-complexity constitution without a new architectural pattern.
The shared .46 baseline is unchanged. Promotion must reconcile distribution
source/version statements and evidence boundaries after independent committed
review; no successor baseline is claimed here.
