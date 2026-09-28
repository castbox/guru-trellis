# #454 Generation 7 TaskId Domain Test Contribution

Status: isolated candidate; results must be bound to the final reviewed diff.

- `T454-G7-01`: In the exact fixed Fork, create tasks using `task.lock`,
  `task.`, `task..child` and ordinary Git-valid IDs; verify rejected IDs
  are outside the public pattern for explicit and slug-derived IDs before
  task creation. Confirm the pinned commit, tree and CI.
- `T454-G7-02`: Run Guru identity/schema/runtime tests for the same values,
  collisions and archive identity. Assert unchanged refs for Git-valid IDs
  and deterministic, valid, separate refs for Git-ref-invalid IDs.
- `T454-G7-03`: Run source/installed projection, package-ready and
  reapply/drift checks. Inspect sidecars and ensure no duplicate task/session
  authority, mapping reader or writer returns.
- `T454-G7-04`: Perform the full #454 workflow/selector/manifest/installed
  graph and lifecycle acceptance gates after promotion; do not substitute
  #434 or C3-C7 historical evidence. The full multi-platform Release matrix
  remains assigned to its dedicated gate.
