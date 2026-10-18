# #454 D436 Terminal Lifecycle Test Contribution

Status: reviewed and promoted acceptance scope, not a claim that post-promotion gates passed. Required focused and composition evidence:

- `T454-D436-01` (R01): all seven Completion outcomes, accepted-scope/Delivery merge lineage and evidence
  freshness; no premature complete from PR Ready, merge, deploy or historical archive; exact output DTOs.
- `T454-D436-02` (R02): no-Issue/reference-only no-mutation, exact Issue action-set close, output-loss
  recovery without second mutation, stale identity and external open/closed change re-entry.
- `T454-D436-03` (R03): current Closure reread before first terminal mutation, lifecycle-only archive
  bookkeeping allowlist, expected-head merge and remote archive post-state; Finish seal matches exact
  generation/result/HEAD and never deletes resources. Interruption must not report success.
- `T454-D436-04` (R04): normal Cleanup deletes only Guru-owned sealed resources, preserves caller-owned,
  converges already-absent, rejects stale generation/identity, and tests manual/machine-handoff exits.
- `T454-D436-05` (R05): same TaskId Reactivate with generation increment, reused/new checkout, same-
  month/cross-month archive route, old receipt invalidation, session recovery/source correction exits,
  source no-Issue/Issue preservation and no legacy mapping authority in the migrated package.
- `T454-D436-06` (R06): five package source/interface/schema/consumer closure, shared DTO/ledger
  composition, no production graph/selector/manifest/installed/platform mutation, task validation,
  touched-file line limits and `git diff --check`. Report historical package-integration failures and
  deferred E434 installer/matrix gates separately, without presenting them as passing.

After contribution promotion, rerun fresh Phase 2, Task Commit and independent full base-to-HEAD Branch
Review. These are distinct from focused package tests.
