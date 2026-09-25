# #454 D443 Bind Session Design Contribution

Status: reviewed and promoted. `ADR-015` and Phase C retain framework, identity, branch, checkout and resource
ownership. Bind owns semantic session route and a deterministic official session-port write/validation only.

- `D454-D443-01`: A profile-specific public input names TaskLifecycleDTO, current/target lifecycle as applicable,
  and the intended resume target. The AI judges the route; the runtime validates exact current task identity,
  branch association, checkout registration and task status using the shared substrate before invoking the official
  schema-2 session adapter. It does not parse legacy task/workspace mapping files or stored path/branch/HEAD hints.
  C4 binding and C3 live facts first identify the unique current checkout; only then does the official TaskId
  resolver inspect that checkout. A retained old-branch checkout with the same task artifact is noncurrent.
- `D454-D443-02`: Resume verifies an existing exact pointer. Rebind and Reactivate bind the selected lifecycle;
  switch checks the current source pointer before writing the distinct target. Manual recovery shares the same
  validation and writes only the missing pointer. An already identical pointer is a no-op success; a conflicting
  pointer requires the appropriate reviewed route rather than an implicit switch.
- `D454-D443-03`: Preserve five success exit/router IDs, add explicit_task_mode, and retain binding_blocked/stop.
  Each success schema and consumer projection carries TaskLifecycleDTO plus resume_target; blocked carries ReasonDTO.
  The consumer, not Bind, derives mutable TaskRef from TaskId and generation at its own invocation boundary.
- `D454-D443-04`: Canonical package major and package-owned source templates are the only D443 write surface.
  Registry selector, manifest, workflow target markers and managed installed/platform bytes remain old production
  until the E434 atomic switch. No parallel session store, adapter, alias or long-lived dual-read is introduced.
