# Test Contribution

## Required Evidence

- `T378-01`: observed Fork checkout identity/build and no fallback tests.
- `T378-02`: canonical/installed session and main-hook tests, including two
  actual temporary Git worktrees.
- `T378-03`: source-record install/reapply/conflict preservation, source/installed
  inventory, ownership and drift tests.
- `T378-04`: real focused shell init and two same-candidate updates/reapplies.
- `T378-05`: standalone/full dispatcher compatibility tests and real installed
  closeout fixture entry calls; full historical execution remains unverified.

- Fixed commit identity and build provenance.
- Clean install and existing-project update/reapply using the Fork CLI.
- Canonical and installed resolver/hook regression for missing, unmatched,
  exact, stale, zero/one/multiple session and explicit child-agent cases.
- Platform parity, source/installed package validation, sidecar absence and
  dogfood drift.

## Boundaries

Business repositories, full release matrices, npm publication and deployment
remain outside this task's acceptance. Their status is reported separately.
