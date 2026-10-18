# #454 C3 Checkout Acquisition Provenance Contribution

## Identity And Review State

- contribution identity: `architecture-contribution-454-task-lifecycle-state-model-c3-provenance-v1`.
- lifecycle state: `reviewed_promoted`.
- source authority: live Issue #454 and the active C3 task planning.
- task locator: `.trellis/tasks/09-20-454-task-lifecycle-state-model`.
- related RDT contribution: `docs/requirements-design-test-contributions/454-task-lifecycle-state-model-c3-provenance/`.
- predecessor baseline: `current-main-0.6.17-guru.60` / `active`.
- promoted successor: `current-main-0.6.17-guru.61` / `active`.
- reviewed range: `origin/main@9c2238bad7e73ea4a1f23dddcb7e8e9204c244da...b816aca8d6520bf90c52c6210ff3155174da86f3`.
- design constitution: `guru-trellis-design-constitution-v1` / `current`.
- project change contract: `guru-trellis-architecture-change-contract-v1`.
- change path: `target_native`.

Independent Branch Review closed `BR454-C3-P2-010` and `BR454-C3-P2-011`
without a new P0-P3 finding. This contribution promotes only the provenance
continuity needed by C3 output-loss recovery. The original C3 contribution and
the `.60` authority remain immutable history.

## Boundary And Decision

The `.60` checkout substrate validated path, branch and HEAD but could not
distinguish the original transaction-created linked worktree from an honest
same-path, same-branch and same-HEAD replacement. Recovery could therefore
project `guru_owned` cleanup ownership onto a caller-created resource.

The successor adds one closed ordinary JSON marker in the linked worktree Git
administrative directory. The acquisition transaction is its sole writer and
the same acquisition owner's read-only output-loss recovery is its sole
reader. The marker binds transaction/result, task/generation, branch/HEAD,
target, disposition, action and ownership projection. Recovery requires exact
marker and fresh live-fact agreement.

The marker is not task, session, branch, workspace or resource-ledger
authority. It is not projected through a public DTO. Existing-checkout reuse
remains caller-owned and writes no marker. Direct handoff retires the marker
before invoking the consumer; worktree removal removes it with the original
Git administrative directory.

## Ownership And Compatibility

- `provision_linked_worktree` writes the marker only for a transaction-created
  linked worktree.
- `recover_checkout_acquisition` validates but never mutates the marker or Git
  state.
- direct `post_acquire` handoff removes the marker before consumer invocation.
- marker retirement or callback failure rolls back only this transaction's
  still-matching resources.
- caller-created replacements never inherit Guru cleanup ownership.

No alias, dual-read, durable path mapping, lock, inode, process, PID, signal,
FD or second ownership store is introduced. `ADR-015` remains the decision
owner; no new ADR is required.

## Evidence And Limits

Focused evidence includes checkout substrate `27/27`, complete task lifecycle
runtime `56/56`, Python compilation, task-lifecycle JSON parsing, ownership
`32 active + 1 planned`, task validation, workspace boundary, zero legacy
mapping/path-authority access, zero forbidden OS/process/lock mechanisms,
touched-file line limits and `git diff --check`.

The complete committed range closed both replacement-resource findings. It
covers successful output-loss recovery, different-path and same-path
replacement rejection, missing/mismatched marker rejection, successful-handoff
retirement and callback-failure rollback.

Package integration remains `19/20`; shared runtime remains `119/128`;
lifecycle integration remains `38/44`; preset remains 272 tests with 2 errors
and 3 skips. These failures do not execute the provenance-marker path and are
not claimed as passing. C4-C7, D443, D436, E434, production activation and the
complete multi-platform Release matrix remain pending or unverified.

The promotion-created `.61` diff must re-enter fresh Phase 2, Task Commit and
independent complete Branch Review before Publication.
