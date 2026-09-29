# #467 v0.6.17-guru.2 Architecture Contribution

- Identity: `architecture-contribution-467-release-v0617-guru2-v1`.
- State: independently reviewed task-owned contribution; serialized promotion targets `current-main-0.6.17-guru.69/active` from `.68`.
- Authority: live `castbox/guru-trellis#467`, task `467-release-v0617-guru2`, and `guru-maintain-architecture-baseline:2.0`.
- Constitution: `docs/architecture/00-foundation/design-constitution.md@guru-trellis-design-constitution-v1/current`.
- Project contract: `docs/architecture/06-governance/change-contract.md@guru-trellis-architecture-change-contract-v1`.
- Change path: `target_native`; ADR required: false.

## Boundary

The repository target advances from released `v0.6.17-guru.1` to
`v0.6.17-guru.2`, and the extension from `0.6.17-guru.42` to
`0.6.17-guru.43`. Official CLI/core remains `0.6.17`; the reviewed Fork
source remains `castbox/Trellis@8336e78b8fafe2a4bc4ea3d01815a61cf4f08983`.
These are independent axes. The target tag is not a published fact until the
post-merge candidate gate, annotated tag and GitHub Release succeed.

The Guru task-creation preflight checks the proposed TaskId and TaskRef across
registered worktrees and branch artifacts. Unrelated duplicate legacy task
artifacts, malformed historical branch JSON and obsolete resource ledgers
cannot block creation of a distinct identity. An occupied target identity or
target ledger conflict still blocks. The official Fork remains the sole task
writer; Guru changes only its existing lifecycle preflight.

The predecessor-to-candidate upgrade also removes managed Skills and related
assets retired by the new registry. The installer uses prior managed hashes to
delete unchanged retired content; local modifications surface as conflicts and
remain untouched. One predecessor existing-install cell checks actual removal
without claiming the full multi-platform matrix.

## Project Change Contract

| Required concern | Applicability and decision |
| --- | --- |
| authority-binding | Applicable: bind #467, current .68 baseline, the constitution and project change contract. |
| constitution-binding | Applicable: mature practice, semantic completeness, cohesion, minimum complexity and debt convergence favor a narrow existing-owner correction. |
| boundary-and-decision | Applicable: `target_native` revises the existing preflight and release mapping; no new owner or ADR. |
| owner-and-single-writer | Applicable: Fork task writer and Guru preflight retain their distinct roles; Architecture/RDT owners alone promote shared current. |
| compatibility-and-exit | Applicable: successful unique TaskId creation and target collision failures retain their public routes; no dual reader or compatibility layer. |
| gap-and-deviation | Applicable: no existing GAP is closed, reopened or worsened by this release preparation. |
| parallel-scope | Applicable: task code, tests and contribution advance in the task branch; shared current is reserved for serialized promotion. |
| evidence-and-freshness | Applicable: focused preflight tests, canonical/installed parity, source and selected platform validation bind the preparation candidate; the later release gate binds a fresh exact main candidate. |
| review-and-promotion | Applicable: full committed Branch Review precedes promotion; promotion-created content requires fresh Phase 2, commit and full Branch Review. |

Before: unrelated historical residue can abort an otherwise valid task
creation, and current release-facing mapping names the predecessor.
After: target-specific identity conflicts still fail closed while unrelated
history is ignored, and current mapping names the new target. The predecessor
and prior Architecture/RDT versions remain historical authority. The full
multi-platform matrix and business production installation remain unverified
boundaries of this Issue.
