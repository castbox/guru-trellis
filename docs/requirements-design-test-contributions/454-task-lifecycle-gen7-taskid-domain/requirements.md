# #454 Generation 7 TaskId Domain Requirements Contribution

Status: reviewed promotion from immutable `.67` to `.68/active`; post-promotion gates remain independent.

- `R454-G7-01`: Official `task.py create` validates explicit `--task-id` and
  slug-derived TaskIds against exactly `[A-Za-z0-9][A-Za-z0-9._-]*` before
  task creation; Guru lifecycle identity accepts the same domain, including
  `task.lock`, `task.`, and `task..child`. Git-ref eligibility does not
  narrow the TaskId domain.
- `R454-G7-02`: Handoff receipt refs remain valid Git refs for every
  accepted TaskId. Existing Git-valid TaskIds retain their ref identity;
  legal Git-ref-invalid TaskIds receive a deterministic separate namespace.
  Ref derivation does not introduce a second TaskId, source, session, branch,
  checkout or resource authority.
- `R454-G7-03`: Canonical and installed package contracts, fixed Fork
  source lock and supported entry projections agree. The `.67` authority
  and historical #434 test claims remain immutable until reviewed promotion.
- `R454-G7-04`: Terminal Cleanup with missing ownership never infers a
  historical owner or deletes automatically. It exposes call-local live
  resource candidates with stable IDs and exact identity/HEAD facts; the
  `select_explicit_cleanup_targets` profile accepts selected candidate IDs,
  revalidates them, requires an exact deletion confirmation, and leaves
  unselected resources unchanged. Ledger loss after an ordinary successful
  Finish also reaches this route using the exact terminal Finish identity.
  After the Finish branch itself is absent, an explicitly confirmed empty
  selection records `cleaned` without deleting unrelated resources.
- `R454-G7-05`: The official task writer creates immutable TaskId and
  structured source without retired `branch` metadata; official rename and
  archive preserve TaskId/source/generation. A remote-backed ordinary archive
  does not require the retired task branch field. The Guru dogfood copy uses
  the same fixed official task CLI semantics.
- `R454-G7-06`: A completed explicit terminal Cleanup selection seals a
  result that Reactivate recognizes for the same TaskId, generation and Finish
  result, including normal Finish followed by ledger loss and confirmed empty
  selection; old completed manual receipts remain readable for prior generations.
- `R454-G7-07`: TaskBranchBinding uses only the five live Issue fields;
  neither resource ownership nor public DTO adds an epoch. Missing-control
  Cleanup cannot delete a local branch carrying an active task unless another
  retained branch contains the task commit and artifact.
- `R454-G7-08`: The official task source writer and Guru reader accept the
  same portable owner/repo domain before durable task creation. The dogfood
  session reader consumes the current five-field binding record.
