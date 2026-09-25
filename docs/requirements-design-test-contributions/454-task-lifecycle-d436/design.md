# #454 D436 Terminal Lifecycle Design Contribution

Status: reviewed and promoted from immutable `.65` to `.66/active`. C2-C7 own shared DTOs, live checkout/binding, official session port and resource ledger.
D436 changes only the five canonical package majors and their package-owned contracts.

- `D454-D436-01`: Completion separates AI semantic authoring from deterministic validation; its
  lifecycle/scope/merge-lineage/evidence input is closed. Preserve seven exit IDs and unique consumers;
  non-complete results hand off TaskArtifactDTO plus ReasonDTO, while `completed` yields ResultRefDTO.
- `D454-D436-02`: Closure freezes the current lifecycle, Completion ref, source relation, accepted scope,
  target, branch binding, evidence and exact action set before provider mutation. A same-owner transaction
  recovers only the same Issue/action result; `external_change_conflict` returns to Closure semantic
  review. Public output is minimal ResultRefDTO/TransactionRefDTO/ReasonDTO, never provider snapshots.
- `D454-D436-03`: Finish rereads each required-closed Issue before archive or ledger mutation. Its
  archive projection, allowlisted bookkeeping PR and expected-head merge establish terminal persistence;
  only then does the current-generation ledger seal the PR head, verify the separate target merge SHA,
  retire its branch binding and yield ResourceSealRefDTO. Closure refresh and manual
  cleanup are explicit exits. The bookkeeping PR does not recurse into Delivery or Completion.
- `D454-D436-04`: Cleanup's normal profile takes ResourceSealRefDTO only and asks the C5 ledger for
  eligible Guru-owned incarnations. Manual selection and machine-handoff are separate profiles with
  fresh revalidation; already-absent resources converge, while conflicts stop the affected action.
  Output carries CleanupResultRefDTO or ReasonDTO, not a caller-provided deletion inventory.
- `D454-D436-05`: Reactivate resolves exact normal archive identity and current base, then composes C3
  acquisition, C4 binding and C5 ledger for `g+1`. Source correction stays with its owner. Success
  routes only to Planning or declared recovery/resume owners; blocked carries ReasonDTO. Historical
  generation receipts remain historical and never form the new control state.
- `D454-D436-06`: Package-ready canonical contracts are not active graph authority. #434/E434 owns
  the atomic workflow/selector/manifest/installed/platform cutover and old-edge retirement.
