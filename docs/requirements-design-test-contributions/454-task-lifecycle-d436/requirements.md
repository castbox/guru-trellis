# #454 D436 Terminal Lifecycle Requirements Contribution

Status: reviewed and promoted from immutable `.65` to `.66/active`. The live #454 contract and #456 `436-*` migration rows supersede
the predecessor package shape from the already closed historical #436; this slice does not activate #434.

- `R454-D436-01`: Completion reads the current TaskLifecycleKey, accepted scope identity, exact merged
  Delivery lineage, remaining work and current evidence slots. Seven existing outcomes remain distinct;
  only a semantic `completed` result can seed Closure. A PR, merge, deploy, test pass or archived task
  does not imply Completion.
- `R454-D436-02`: Closure consumes current Completion and source/scope/target/binding/evidence relations.
  No-Issue and reference-only roles do not mutate an Issue; exact close uses one frozen action set and
  same-transaction recovery. External change invalidates the decision and returns to semantic review.
- `R454-D436-03`: Finish requires current Closure action-set convergence, rereads required-closed Issues
  before any terminal mutation, persists one current archive via lifecycle-only bookkeeping, and seals
  exact generation/Finish result in the single resource ledger. It does not delete resources or create
  a business Delivery result.
- `R454-D436-04`: Normal Cleanup consumes only the current ResourceSealRefDTO and common-dir ledger,
  deletes only Guru-owned resources with fresh identity checks, and retains caller-owned/unknown
  resources. Missing terminal ownership enters explicit manual selection; machine-handoff inventory
  has a separate route. An older Finish cannot authorize current-generation cleanup.
- `R454-D436-05`: Reactivate preserves archived TaskId/source and original scope, establishes strictly
  increasing generation through shared acquisition/binding/ownership, and never reuses historical
  session/Finish/Cleanup authority. Planning remains the normal re-entry; session recovery, same-
  transaction resume and source correction are explicit exits, replacing direct historical routes.
- `R454-D436-06`: Five migrated canonical packages must close their schema/interface/consumer/runtime
  contracts and package-local tests. E434 alone switches production workflow, registry selector,
  active manifest and installed/platform projections. D436 does not claim Release matrix proof.
