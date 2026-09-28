# #454 Generation 7 TaskId Domain Requirements Contribution

Status: isolated candidate against `.67/active`; not promoted.

- `R454-G7-01`: Official `task.py create --task-id` and Guru lifecycle
  identity accept exactly `[A-Za-z0-9][A-Za-z0-9._-]*`, including
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
