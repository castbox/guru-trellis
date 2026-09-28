# #454 Generation 7 TaskId Domain Test Contribution

Status: reviewed promotion to `.68/active`; results must be bound to the final reviewed diff.

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
- `T454-G7-05`: Exercise missing terminal ownership candidate discovery,
  stable IDs, selected-only deletion, changed HEAD, dirty worktree, current
  use, absent resources, normal-Finish ledger loss and independent confirmation through the canonical
  and installed Cleanup interface and current workflow projection. Verify a
  confirmed empty selection produces a `selected-*` cleaned receipt only
  after the Finish branch disappears, while unrelated branches remain intact.
- `T454-G7-06`: In the exact fixed Fork, exercise ordinary remote-backed
  task create/rename/archive with immutable TaskId, `no_issue` source and no
  retired branch dependency. Confirm Guru issue-sourced creation still writes
  its reviewed source, the dogfood official scripts match fixed Fork templates,
  and source-lock and installed regressions pass.
- `T454-G7-07`: Complete exact selected-target Cleanup after a manual Finish,
  then Reactivate the same archived task. Also complete confirmed empty
  Cleanup after normal Finish ledger loss and Reactivate from its `selected-*`
  receipt; stale or absent receipts remain blocked. Preserve the prior
  `manual-*` receipt regression.
- `T454-G7-08`: Validate five-field binding and resource records in source,
  installed and fixed Fork readers; reject retired six-field records. Exercise
  missing-control Cleanup with a still-active artifact, both without and with
  a retained branch containing that task commit and artifact.
- `T454-G7-09`: In the exact fixed Fork, reject source repo refs with a
  transport `.git` suffix or illegal leading component before task creation,
  and accept legal dotted and hyphenated names. Assert Guru dogfood task and
  session scripts match the fixed Fork templates and resolve a current
  generation 7 five-field session binding.
- `T454-G7-10`: In fixed Fork and Guru installed readers, remove the current
  binding while an old checkout still carries the task artifact. Guru
  continuation must report `binding_required`; ordinary Trellis no-binding
  fallback remains usable. Check exact source/template/dogfood byte parity.
