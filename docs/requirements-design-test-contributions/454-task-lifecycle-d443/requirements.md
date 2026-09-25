# #454 D443 Bind Session Requirements Contribution

Status: contribution candidate against `.64/active`. The accepted authority is live #454 and its target design,
with #456's `443-*` replace/retire inventory. The older #443 implementation and inherited `.64` D443 text
describe the predecessor, not the target. This candidate does not activate #434.

- `R454-D443-01`: Bind operates on exact TaskId and lifecycle generation, including 0. Session persistence remains
  the Fixed Fork schema-2 record of only those two fields. The current branch/checkout association and task artifact
  identity are resolved fresh through the Phase C substrate; no machine path or Git HEAD enters session authority.
- `R454-D443-02`: Resume, rebind, switch, Reactivate rebind and manual recovery each validate current lifecycle and
  current session route before writing. Manual recovery restores only a missing official session pointer, never task
  or workspace mappings; binding/ownership repair stays with their separate owners. A stale or conflicting target
  fails without a session write or business mutation.
- `R454-D443-03`: Five retained success exits hand off only TaskLifecycleDTO plus resume_target. Missing usable
  session context returns a distinct explicit_task_mode using the selected lifecycle, while blocked uses ReasonDTO.
  TaskRef, branch, checkout path, HEAD, session locator, resource ownership and authorization stay private.
- `R454-D443-04`: D443 produces a package-ready canonical contract without changing workflow consumers, registry
  selection, active manifest or installed/platform bytes. D436 follows this capability and E434 alone atomically
  integrates the six Bind routers with the complete #434 graph. No release/production compatibility is inferred.
