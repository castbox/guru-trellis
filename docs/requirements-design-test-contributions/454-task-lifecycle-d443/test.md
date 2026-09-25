# #454 D443 Bind Session Test Contribution

Status: candidate acceptance, not a record of passing tests. Bind package-local tests and real Git/official-session
fixtures must show:

- `T454-D443-01` (R01): generation 0 and later lifecycles; rename/move of TaskRef without stored-path change;
  live repository/branch/checkout identity derived from Phase C and official schema-2 session record exactness.
- `T454-D443-02` (R02): resume, missing-pointer rebind, distinct-task switch and switch-back, Reactivate invalidation
  of old generation, pointer-only manual recovery and same-target idempotent retry. Wrong task/repository/branch,
  stale generation, conflicting route and missing binding/ownership authority are zero-write stops.
- `T454-D443-03` (R03): five success schemas and projections, explicit_task_mode without a usable context key,
  ReasonDTO blocked; no TaskRef/path/branch/HEAD/session locator/authorization in output or stored payload.
- `T454-D443-04` (R04): package source validation, command/consumer closure, source/installed separation, zero
  legacy mapping reads/writes in target Bind, unchanged production graph/selector/manifest/installed projection,
  task validator, line count and `git diff --check` with exact command results. E434 installer/platform parity
  and #410 full Release matrix remain deferred and must not be reported as passing D443 checks.

Fresh Phase 2, Task Commit and complete base-to-HEAD Branch Review are distinct gates. A Docs promotion creates
new diff and invalidates earlier content gates until rerun.
